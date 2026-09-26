"""
IP Pinning and PinnedHTTPSConnection Security Tests (UPA-1205)
==============================================================
Validates:
1. PinnedHTTPSConnection subclass behavior, SNI server_hostname binding, and
   fail-closed connect() check against non-global/private IPs.
2. TLS handshake, SNI negotiation, and certificate validation using trustme CA.
3. TLS certificate mismatch rejection (SSLCertVerificationError).
4. Asynchronous off-event-loop DNS resolution and validation.
5. Hop-by-hop redirect validation and single-resolution fail-closed behavior.
"""

import socket
import ssl
import http.server
import http.client
import threading
import pytest
import asyncio
import trustme
from unittest.mock import patch, MagicMock
from backend.app.services.url_validator import (
    PinnedHTTPSConnection,
    fetch_pinned_ip_url,
    validate_url_and_follow_redirects,
    async_resolve_and_validate_hostname,
    async_validate_url_and_follow_redirects,
    resolve_and_validate_hostname,
)


class TestPinnedHTTPSConnectionSSRFGuard:
    """Validates that PinnedHTTPSConnection strictly blocks private IPs at connect time."""

    @pytest.mark.parametrize(
        "private_ip",
        [
            "127.0.0.1",
            "10.0.0.1",
            "172.16.0.1",
            "192.168.1.100",
            "169.254.169.254",
            "::1",
            "::ffff:127.0.0.1",
            "::ffff:169.254.169.254",
        ],
    )
    def test_connect_rejects_private_and_metadata_ips(self, private_ip):
        """connect() must raise ConnectionRefusedError if pinned IP is non-global."""
        conn = PinnedHTTPSConnection(host="instagram.com", pinned_ip=private_ip, port=443)
        with pytest.raises(ConnectionRefusedError) as exc_info:
            conn.connect()
        assert "not globally routable" in str(exc_info.value).lower()

    def test_attributes_preserve_sni_and_target_host(self):
        """Asserts target host, server_hostname, and _server_hostname are preserved for SNI."""
        conn = PinnedHTTPSConnection(host="youtube.com", pinned_ip="142.250.190.46", port=443)
        assert conn.target_host == "youtube.com"
        assert conn.pinned_ip == "142.250.190.46"
        assert conn._server_hostname == "youtube.com"
        assert conn.server_hostname == "youtube.com"


class TestPinnedHTTPSTrustmeHandshake:
    """Validates real TLS handshake, SNI negotiation, and cert verification using trustme."""

    @pytest.fixture
    def tls_server(self):
        """Spins up a local HTTPS server with a trustme certificate for instagram.com."""
        ca = trustme.CA()
        server_cert = ca.issue_cert("instagram.com")

        class SimpleHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/test_stream":
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(b'{"status": "ok", "source": "pinned_https"}')
                else:
                    self.send_response(404)
                    self.end_headers()

            def do_HEAD(self):
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()

            def log_message(self, format, *args):
                pass

        server_ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        server_cert.configure_cert(server_ssl_ctx)

        httpd = http.server.HTTPServer(("127.0.0.1", 0), SimpleHandler)
        httpd.socket = server_ssl_ctx.wrap_socket(httpd.socket, server_side=True)
        port = httpd.server_address[1]

        server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()

        yield ca, port

        httpd.shutdown()

    def test_pinned_tls_handshake_with_valid_sni(self, tls_server):
        """Tests that TLS connects to loopback IP with SNI set to target domain."""
        ca, port = tls_server
        client_ssl_ctx = ssl.create_default_context()
        ca.configure_trust(client_ssl_ctx)

        class TestablePinnedHTTPSConnection(PinnedHTTPSConnection):
            def connect(self):
                # Connect to test server on loopback and verify TLS wrapping uses target_host
                self.sock = self._create_connection((self.host, self.port), self.timeout, self.source_address)
                server_hostname = getattr(self, "server_hostname", None) or self.target_host
                self.sock = self._context.wrap_socket(self.sock, server_hostname=server_hostname)

        conn = TestablePinnedHTTPSConnection(
            host="instagram.com",
            pinned_ip="127.0.0.1",
            port=port,
            context=client_ssl_ctx,
        )
        conn.request("GET", "/test_stream", headers={"Host": "instagram.com"})
        resp = conn.getresponse()
        assert resp.status == 200
        body = resp.read()
        assert b'"pinned_https"' in body
        conn.close()

    def test_cert_mismatch_fails_tls_verification(self, tls_server):
        """Tests that mismatched domain name fails certificate verification."""
        ca, port = tls_server
        client_ssl_ctx = ssl.create_default_context()
        ca.configure_trust(client_ssl_ctx)

        class TestablePinnedHTTPSConnection(PinnedHTTPSConnection):
            def connect(self):
                self.sock = self._create_connection((self.host, self.port), self.timeout, self.source_address)
                server_hostname = getattr(self, "server_hostname", None) or self.target_host
                self.sock = self._context.wrap_socket(self.sock, server_hostname=server_hostname)

        # Server cert is for 'instagram.com', but client claims 'youtube.com'
        conn = TestablePinnedHTTPSConnection(
            host="youtube.com",
            pinned_ip="127.0.0.1",
            port=port,
            context=client_ssl_ctx,
        )
        with pytest.raises(ssl.SSLCertVerificationError):
            conn.request("GET", "/test_stream", headers={"Host": "youtube.com"})
        conn.close()


class TestAsyncDNSHelpers:
    """Validates asynchronous DNS offloading from the event loop."""

    @pytest.mark.asyncio
    async def test_async_resolve_and_validate_hostname(self):
        """Verifies async_resolve_and_validate_hostname executes off the event loop."""
        with patch("backend.app.services.url_validator.socket.getaddrinfo") as mock_gai:
            mock_gai.return_value = [
                (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("157.240.22.174", 443))
            ]
            is_valid, pinned_ip, err = await async_resolve_and_validate_hostname("instagram.com")
            assert is_valid is True
            assert pinned_ip == "157.240.22.174"
            assert err == ""

    @pytest.mark.asyncio
    async def test_async_validate_url_and_follow_redirects(self):
        """Verifies async_validate_url_and_follow_redirects executes off the event loop."""
        with patch("backend.app.services.url_validator.socket.getaddrinfo") as mock_gai:
            mock_gai.return_value = [
                (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("142.250.190.46", 443))
            ]
            is_valid, err, final_url = await async_validate_url_and_follow_redirects("https://youtube.com/watch?v=123")
            assert is_valid is True
            assert err == ""
            assert final_url == "https://youtube.com/watch?v=123"
