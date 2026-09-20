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
import hmac
import hashlib
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.core.config import get_settings
from backend.app.services.url_validator import (
    validate_social_url,
    validate_merchant_redirect_url,
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


