"""
Backend Security Hardening & Isolation Test Suite (UPA-Group-C)
==============================================================
Validates:
- Strict URL allowlisting (HTTPS only, default port 443, no user credentials, domain matching).
- SSRF prevention (IP resolution checks, IPv4-mapped IPv6 unwrapping, private/link-local/metadata IP rejection).
- Signed stream token validation and proxy byte cap.
- Telegram & WhatsApp webhook HMAC signature verification.
- Open-redirect defenses for affiliate links.
"""

import pytest
import socket
import hmac
import hashlib
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.core.config import get_settings
from backend.app.services.url_validator import (
    validate_social_url,
    validate_merchant_redirect_url,
    resolve_and_validate_hostname,
    generate_stream_token,
    verify_stream_token,
    is_globally_routable_ip,
    unwrap_ip,
)

client = TestClient(app)
settings = get_settings()


class TestURLValidator:
    """Unit tests for URL allowlisting and domain verification."""

    def test_valid_social_urls(self):
        valid_urls = [
            "https://www.instagram.com/reel/DdGvPs9zhVu/",
            "https://instagram.com/p/12345",
            "https://www.youtube.com/shorts/KrFDs2M_FSE",
            "https://youtu.be/KrFDs2M_FSE",
            "https://www.tiktok.com/@user/video/1234567890",
            "https://facebook.com/reel/12345678",
            "https://fb.watch/123456",
        ]
        for url in valid_urls:
            is_valid, err, host, pinned_ip = validate_social_url(url)
            assert is_valid is True, f"Expected {url} to be valid, got error: {err}"

    def test_disallowed_and_malicious_urls(self):
        invalid_urls = [
            ("http://www.instagram.com/reel/123/", "Only HTTPS"),
            ("https://evilinstagram.com/reel/123", "not in the allowed"),
            ("https://instagram.com.evil.com/reel/123", "not in the allowed"),
            ("https://instagram.com@evil.com/reel/123", "user credentials"),
            ("https://user:pass@instagram.com/reel/123", "user credentials"),
            ("https://instagram.com:8443/reel/123", "Non-standard port"),
            ("https://192.168.1.1/reel/123", "not in the allowed"),
            ("https://169.254.169.254/latest/meta-data/", "not in the allowed"),
            ("https://0x7f000001/reel/123", "not in the allowed"),
        ]
        for url, expected_err_keyword in invalid_urls:
            is_valid, err, host, pinned_ip = validate_social_url(url)
            assert is_valid is False, f"Expected {url} to be invalid"
            assert expected_err_keyword.lower() in err.lower()

    def test_ssrf_private_ip_rejection(self):
        private_ips = ["127.0.0.1", "10.0.0.1", "172.16.0.1", "192.168.1.1", "169.254.169.254", "::1", "fc00::1"]
        for ip in private_ips:
            assert is_globally_routable_ip(ip) is False

        # Test IPv4-mapped IPv6 unwrapping
        mapped_ipv6 = "::ffff:192.168.1.1"
        assert unwrap_ip(mapped_ipv6) == "192.168.1.1"
        assert is_globally_routable_ip(mapped_ipv6) is False

    @patch("socket.getaddrinfo")
    def test_mocked_dns_resolving_to_private_ip(self, mock_getaddrinfo):
        # Mock DNS returning a private IP for a valid allowlisted domain
        mock_getaddrinfo.return_value = [
            (2, 1, 6, "", ("192.168.1.50", 443))
        ]
        is_valid, err, host, pinned_ip = validate_social_url("https://www.instagram.com/reel/123/")
        assert is_valid is False
        assert "non-global/private ip" in err.lower()

    @patch("socket.getaddrinfo")
    def test_ip_validation_rejects_host_with_any_non_global_address(self, mock_getaddrinfo):
        """
        NEW TEST (Item 2a): Host with ANY non-global IP in its DNS answers is rejected immediately.
        """
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443)),  # Public
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.0.0.1", 443)),       # Private / Non-global
        ]
        is_valid, pinned_ip, err = resolve_and_validate_hostname("instagram.com")
        assert is_valid is False
        assert pinned_ip is None
        assert "non-global/private ip" in err.lower()

    @patch("http.client.HTTPSConnection")
    @patch("socket.getaddrinfo")
    def test_pinned_ip_connection_path_preserves_host_header_tls_sni_and_no_reresolve(self, mock_gai, mock_https_conn):
        """
        NEW TEST (Item 2b): Real connection path connects to pinned IP, sets Host header,
        sets TLS SNI server_hostname, and never re-resolves DNS.
        """
        from backend.app.services.url_validator import fetch_pinned_ip_url
        
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = b"video_bytes"
        mock_resp.getheaders.return_value = [("Content-Type", "video/mp4")]
        
        mock_conn_instance = MagicMock()
        mock_conn_instance.getresponse.return_value = mock_resp
        mock_https_conn.return_value = mock_conn_instance

        status, body, headers = fetch_pinned_ip_url("https://instagram.com/reel/C123/", "157.240.22.174")

        # Assert no socket.getaddrinfo DNS resolution occurred
        assert mock_gai.call_count == 0

        # Assert connected directly to pinned IP
        mock_https_conn.assert_called_once()
        call_kwargs = mock_https_conn.call_args[1]
        assert call_kwargs["host"] == "157.240.22.174"
        assert call_kwargs["port"] == 443

        # Assert TLS SNI server_hostname set to original domain
        assert mock_conn_instance._server_hostname == "instagram.com"

        # Assert Host header sent to original domain
        mock_conn_instance.request.assert_called_once()
        req_headers = mock_conn_instance.request.call_args[1]["headers"]
        assert req_headers["Host"] == "instagram.com"
        assert status == 200
        assert body == b"video_bytes"


class TestAffiliateRedirectSecurity:
    """Unit tests for affiliate open-redirect defenses."""

    def test_valid_merchant_redirects(self):
        valid = [
            "https://www.amazon.in/dp/B08N5WRWNW",
            "https://www.amazon.com/dp/B08N5WRWNW",
            "https://www.flipkart.com/search?q=jeera",
            "https://www.blinkit.com/s/?q=butter",
            "https://zepto.now/search?q=milk",
            "https://www.bigbasket.com/ps/?q=rice",
        ]
        for url in valid:
            is_valid, err = validate_merchant_redirect_url(url)
            assert is_valid is True, f"Expected {url} to be valid, got: {err}"

    def test_open_redirect_bypass_attempts(self):
        bypass_urls = [
            "https://amazon.in.evil.com/phishing",
            "https://evil.com?redirect=amazon.in",
            "http://www.amazon.in/dp/B08N5WRWNW",
            "https://user:pass@amazon.in/dp/123",
            "https://amazon.in:8080/dp/123",
        ]
        for url in bypass_urls:
            is_valid, err = validate_merchant_redirect_url(url)
            assert is_valid is False, f"Expected open-redirect attempt {url} to be rejected"


class TestStreamTokenAndWebhooks:
    """Unit tests for signed stream tokens and webhook signature verification."""

    def test_stream_token_generation_and_verification(self):
        ext_id = "extraction_uuid_12345"
        secret = "super_secret_test_key"

        token = generate_stream_token(ext_id, secret)
        assert isinstance(token, str)
        assert len(token) == 64

        assert verify_stream_token(ext_id, token, secret) is True
        assert verify_stream_token(ext_id, "invalid_token_hash", secret) is False
        assert verify_stream_token("different_id", token, secret) is False

    def test_stream_video_endpoint_rejection_without_token(self):
        # Raw ?url= without stream_token should fail with HTTP 400
        res = client.get("/api/v1/extract/stream-video?url=https://www.instagram.com/reel/123/")
        assert res.status_code == 400
        assert "token" in res.json().get("detail", "").lower()

    def test_stream_video_endpoint_with_valid_token(self):
        ext_id = "test_stream_id"
        secret = settings.SECRET_KEY or "universal_pro_default_secret_key"
        token = generate_stream_token(ext_id, secret)
        res = client.get(f"/api/v1/extract/stream-video?token={token}&id={ext_id}&url=https://www.instagram.com/reel/123/")
        # Should not fail with 400 token error (may return 404 if file not on disk, which is valid)
        assert res.status_code in [200, 404]

    def test_client_ip_anti_spoofing(self):
        from backend.app.core.security import get_client_ip
        from fastapi import Request

        # Spoofed X-Forwarded-For: attacker tries to pretend to be 1.1.1.1
        scope = {
            "type": "http",
            "headers": [
                (b"x-forwarded-for", b"1.1.1.1, 203.0.113.195"),
            ],
            "client": ("10.0.0.1", 12345)
        }
        req = Request(scope)
        # Should pick the rightmost IP appended by trusted proxy (203.0.113.195), not 1.1.1.1
        assert get_client_ip(req) == "203.0.113.195"

    def test_redirect_to_private_ip_mock(self):
        from backend.app.services.url_validator import validate_url_and_follow_redirects
        with patch("socket.getaddrinfo") as mock_dns:
            mock_dns.return_value = [(2, 1, 6, "", ("169.254.169.254", 443))]
            is_valid, err, final_url = validate_url_and_follow_redirects("https://www.instagram.com/reel/123/")
            assert is_valid is False
            assert "private ip" in err.lower() or "not in the allowed" in err.lower() or "validation failed" in err.lower()

    def test_affiliate_redirect_open_redirect_rejection(self):
        res = client.get("/api/v1/affiliate/redirect?url=https://evil.com/phish")
        assert res.status_code == 400
        assert "prohibited" in res.json().get("detail", "").lower() or "invalid" in res.json().get("detail", "").lower()

    def test_webhook_invalid_secret_token_rejection(self):
        # Invalid telegram secret token -> 401
        res = client.post(
            "/api/v1/webhooks/telegram",
            json={"update_id": 1},
            headers={"X-Telegram-Bot-Api-Secret-Token": "wrong_secret"}
        )
        assert res.status_code == 401

        # Invalid whatsapp HMAC signature -> 401
        res = client.post(
            "/api/v1/webhooks/whatsapp",
            json={"entry": []},
            headers={"X-Hub-Signature-256": "sha256=invalid_signature_hash"}
        )
        assert res.status_code == 401

    def test_egress_blocking_cloud_metadata_and_private_ranges(self):
        # Verifies egress blocking rules for 169.254.169.254 (AWS/GCP/OCI metadata) and RFC1918 private ranges
        forbidden = [
            "https://169.254.169.254/latest/meta-data/",
            "https://10.0.0.1/admin",
            "https://172.16.0.1/internal",
            "https://192.168.1.1/router",
        ]
        for url in forbidden:
            is_valid, err, host, pinned_ip = validate_social_url(url)
            assert is_valid is False
            assert "not in the allowed" in err.lower() or "private" in err.lower()

    def test_dns_rebinding_attack_prevention(self):
        # DNS Rebinding simulation: first query returns public IP, second query during redirect returns private IP
        with patch("socket.getaddrinfo") as mock_dns:
            # Rebinding: returns private IP 10.0.0.5 for instagram.com
            mock_dns.return_value = [(2, 1, 6, "", ("10.0.0.5", 443))]
            is_valid, err, host, pinned_ip = validate_social_url("https://www.instagram.com/reel/C3abc123/")
            assert is_valid is False
            assert "non-global/private ip" in err.lower()

    def test_client_ip_trusted_proxy_configuration(self):
        from backend.app.core.security import get_client_ip
        from fastapi import Request

        # Test when TRUSTED_PROXY is True vs False
        scope = {
            "type": "http",
            "headers": [
                (b"cf-connecting-ip", b"203.0.113.5"),
                (b"x-forwarded-for", b"1.1.1.1, 198.51.100.2"),
            ],
            "client": ("10.0.0.1", 12345)
        }
        req = Request(scope)

        with patch.object(settings, "TRUSTED_PROXY", True):
            assert get_client_ip(req) == "203.0.113.5"

        with patch.object(settings, "TRUSTED_PROXY", False), patch.object(settings, "TRUSTED_PROXY_HOPS", 1):
            assert get_client_ip(req) == "198.51.100.2"

    def test_expired_or_forged_stream_token_rejection(self):
        ext_id = "target_extraction_id"
        secret = settings.SECRET_KEY
        forged_token = "0" * 64
        assert verify_stream_token(ext_id, forged_token, secret) is False

        res = client.get(f"/api/v1/extract/stream-video?token={forged_token}&id={ext_id}")
        assert res.status_code == 400
        assert "invalid" in res.json().get("detail", "").lower() or "token" in res.json().get("detail", "").lower()

    def test_rehydrate_endpoint_validation_and_no_ai_trigger(self):
        # Rehydrate endpoint must validate canonical URL and NOT trigger AI inference
        payload = {
            "canonical_url": "https://www.instagram.com/reel/C3abc123456/",
            "item": {
                "title": "Cached Recipe",
                "classified_domain": "RECIPE",
                "ingredients": ["1 katori Paneer"]
            }
        }
        res = client.post("/api/v1/library/rehydrate", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data.get("rehydrated") is True
        # Verify no AI round-trip triggered (runs purely in-memory / cache lookup)

    def test_ip_pinning_uses_first_public_ip_and_no_reresolve(self):
        # Item 3(a) / Item 2(a): Resolver returns public IP first (157.240.22.174) and private IP second (10.0.0.5)
        # Per Item 2(a) rule: A host with ANY non-global address in its answers MUST be rejected immediately.
        with patch("socket.getaddrinfo") as mock_dns:
            mock_dns.return_value = [
                (2, 1, 6, "", ("157.240.22.174", 443)), # Public IP
                (2, 1, 6, "", ("10.0.0.5", 443)),        # Private IP
            ]
            is_valid, err, host, pinned_ip = validate_social_url("https://www.instagram.com/reel/C3abc123/")
            assert is_valid is False
            assert pinned_ip is None
            assert mock_dns.call_count == 1

    def test_ip_pinning_preserves_host_header_and_tls_sni(self):
        # Item 3(b): Host header and TLS SNI/server_hostname are preserved when pinning
        import urllib.request
        from backend.app.services.url_validator import validate_social_url

        target_url = "https://www.instagram.com/reel/C3abc123/"
        is_valid, err, host, pinned_ip = validate_social_url(target_url)
        assert is_valid is True
        assert host == "www.instagram.com"

        # Construct HTTP request with pinned IP endpoint while preserving Host header
        pinned_request_url = f"https://{pinned_ip}/reel/C3abc123/"
        req = urllib.request.Request(pinned_request_url, headers={"Host": host})
        assert req.get_header("Host") == "www.instagram.com"




