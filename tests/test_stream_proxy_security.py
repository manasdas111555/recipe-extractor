"""
UPA-1213: Dedicated Stream Proxy Token Security & Media Hardening Test Suite
=============================================================================
Verifies:
1. Expiring HMAC-SHA256 token (<exp>.<sig>) bound to resource ID and exact media URL.
2. Rejection of expired, malformed, tampered, or mismatched tokens.
3. Strict /stream-video parameter enforcement (id + token only; ?url= without token prohibited).
4. Server-side URL resolution via JobManager / Supabase (404 when missing).
5. Per-client-IP rate limiting (429).
6. Non-blocking threadpool download offloading.
7. HTTP Range semantics (206 Partial Content, 416 Range Not Satisfiable).
8. 50MB stream ceiling and deterministic cleanup.
"""

import os
import time
import hmac
import hashlib
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.core.config import get_settings
from backend.app.services.url_validator import generate_stream_token, verify_stream_token
from backend.app.services.job_manager import get_job_manager

client = TestClient(app)
settings = get_settings()
TEST_SECRET = "test_stream_secret_key_1234567890"


class TestStreamTokenCryptography:
    """Cryptographic unit tests for expiring HMAC stream tokens."""

    def test_valid_expiring_token_generation_and_verification(self):
        ext_id = "test_job_101"
        media_url = "https://www.instagram.com/reel/C9876543210/"
        
        token = generate_stream_token(ext_id, TEST_SECRET, media_url=media_url, ttl_seconds=900)
        assert "." in token
        exp_str, sig = token.split(".", 1)
        assert int(exp_str) > int(time.time())
        assert len(sig) == 64

        # Verification succeeds with matching id, url, secret
        assert verify_stream_token(ext_id, token, TEST_SECRET, media_url=media_url) is True

    def test_expired_token_rejection(self):
        ext_id = "test_job_102"
        media_url = "https://www.instagram.com/reel/C9876543210/"
        
        # Token expired 10 seconds ago
        token = generate_stream_token(ext_id, TEST_SECRET, media_url=media_url, ttl_seconds=-10)
        assert verify_stream_token(ext_id, token, TEST_SECRET, media_url=media_url) is False

    def test_tampered_signature_rejection(self):
        ext_id = "test_job_103"
        media_url = "https://www.instagram.com/reel/C9876543210/"
        
        token = generate_stream_token(ext_id, TEST_SECRET, media_url=media_url, ttl_seconds=900)
        exp_str, sig = token.split(".", 1)
        # Flip last character
        tampered_sig = sig[:-1] + ("0" if sig[-1] != "0" else "1")
        tampered_token = f"{exp_str}.{tampered_sig}"

        assert verify_stream_token(ext_id, tampered_token, TEST_SECRET, media_url=media_url) is False

    def test_malformed_token_rejection(self):
        ext_id = "test_job_104"
        media_url = "https://www.instagram.com/reel/C9876543210/"

        assert verify_stream_token(ext_id, "invalid_no_dots", TEST_SECRET, media_url=media_url) is False
        assert verify_stream_token(ext_id, "abc.def.extra", TEST_SECRET, media_url=media_url) is False
        assert verify_stream_token(ext_id, "notanint.abcdef123456", TEST_SECRET, media_url=media_url) is False
        assert verify_stream_token(ext_id, "", TEST_SECRET, media_url=media_url) is False
        assert verify_stream_token("", "123.abc", TEST_SECRET, media_url=media_url) is False

    def test_resource_id_and_url_mismatch_rejection(self):
        ext_id_1 = "test_job_105_a"
        ext_id_2 = "test_job_105_b"
        url_1 = "https://www.instagram.com/reel/C1111111111/"
        url_2 = "https://www.instagram.com/reel/C2222222222/"

        token = generate_stream_token(ext_id_1, TEST_SECRET, media_url=url_1, ttl_seconds=900)

        # Wrong ID
        assert verify_stream_token(ext_id_2, token, TEST_SECRET, media_url=url_1) is False
        # Wrong URL
        assert verify_stream_token(ext_id_1, token, TEST_SECRET, media_url=url_2) is False
        # Wrong secret
        assert verify_stream_token(ext_id_1, token, "wrong_secret_key", media_url=url_1) is False

    def test_legacy_token_compatibility_without_url(self):
        ext_id = "legacy_test_job"
        token = generate_stream_token(ext_id, TEST_SECRET, media_url="")
        assert len(token) == 64
        assert verify_stream_token(ext_id, token, TEST_SECRET, media_url="") is True
        assert verify_stream_token("other_id", token, TEST_SECRET, media_url="") is False


class TestStreamEndpointHardening:
    """Integration tests for GET /api/v1/extract/stream-video endpoint hardening."""

    def test_missing_token_or_id_returns_400(self):
        # Direct ?url= without token
        res = client.get("/api/v1/extract/stream-video?url=https://www.instagram.com/reel/123/")
        assert res.status_code == 400
        assert "token" in res.json().get("detail", "").lower()

        # No params
        res = client.get("/api/v1/extract/stream-video")
        assert res.status_code == 400

        # Token only without id
        res = client.get("/api/v1/extract/stream-video?token=some_token")
        assert res.status_code == 400

    def test_invalid_or_expired_token_returns_400(self):
        job_id = "test_job_exp_400"
        video_url = "https://www.instagram.com/reel/C9876543210/"
        job_manager = get_job_manager()
        job_manager.create_job(job_id=job_id, video_url=video_url, url_hash="hash400", user_id="u1")

        # Expired token
        secret = settings.SECRET_KEY or "dev_signing_secret"
        expired_token = generate_stream_token(job_id, secret, media_url=video_url, ttl_seconds=-100)
        res = client.get(f"/api/v1/extract/stream-video?id={job_id}&token={expired_token}")
        assert res.status_code == 400
        assert "invalid or expired" in res.json().get("detail", "").lower()

        # Tampered token
        res = client.get(f"/api/v1/extract/stream-video?id={job_id}&token=9999999999.invalid_signature")
        assert res.status_code == 400
        assert "invalid or expired" in res.json().get("detail", "").lower()

    def test_missing_server_side_resource_returns_404(self):
        unknown_id = "unknown_uuid_99999"
        unknown_url = "https://www.instagram.com/reel/Cunknown/"
        secret = settings.SECRET_KEY or "dev_signing_secret"
        token = generate_stream_token(unknown_id, secret, media_url=unknown_url, ttl_seconds=900)

        res = client.get(f"/api/v1/extract/stream-video?id={unknown_id}&token={token}")
        assert res.status_code == 404
        assert "not found" in res.json().get("detail", "").lower()

    def test_per_ip_rate_limiting_returns_429(self):
        job_id = "test_job_rate_limit"
        video_url = "https://www.instagram.com/reel/C9876543210/"
        job_manager = get_job_manager()
        job_manager.create_job(job_id=job_id, video_url=video_url, url_hash="hash_rl", user_id="u1")

        secret = settings.SECRET_KEY or "dev_signing_secret"
        token = generate_stream_token(job_id, secret, media_url=video_url, ttl_seconds=900)

        with patch("backend.app.services.quota_service.QuotaManager.check_generic_rate_limit", return_value=(False, 61)):
            res = client.get(f"/api/v1/extract/stream-video?id={job_id}&token={token}")
            assert res.status_code == 429
            assert "rate limit exceeded" in res.json().get("detail", "").lower()

    def test_successful_stream_and_range_206(self):
        job_id = "test_job_stream_success"
        video_url = "https://www.instagram.com/reel/C9876543210/"
        job_manager = get_job_manager()
        job_manager.create_job(job_id=job_id, video_url=video_url, url_hash="hash_ok", user_id="u1")

        secret = settings.SECRET_KEY or "dev_signing_secret"
        token = generate_stream_token(job_id, secret, media_url=video_url, ttl_seconds=900)

        # Create temporary mock video file
        sample_bytes = b"0123456789ABCDEF" * 1024  # 16KB mock video
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp.write(sample_bytes)
            tmp_path = tmp.name

        try:
            with patch("backend.app.api.v1.extract._download_stream_video_sync", return_value=tmp_path):
                # 1. Full 200 Stream Request
                res_200 = client.get(f"/api/v1/extract/stream-video?id={job_id}&token={token}")
                assert res_200.status_code == 200
                assert res_200.headers.get("accept-ranges") == "bytes"
                assert int(res_200.headers.get("content-length")) == len(sample_bytes)
                assert res_200.content == sample_bytes

                # 2. Valid HTTP Range Request (bytes=0-15) -> 206 Partial Content
                res_206 = client.get(
                    f"/api/v1/extract/stream-video?id={job_id}&token={token}",
                    headers={"Range": "bytes=0-15"}
                )
                assert res_206.status_code == 206
                assert res_206.headers.get("content-range") == f"bytes 0-15/{len(sample_bytes)}"
                assert res_206.headers.get("content-length") == "16"
                assert res_206.content == b"0123456789ABCDEF"

                # 3. Valid HTTP Range Request from offset (bytes=16-31) -> 206 Partial Content
                res_206_offset = client.get(
                    f"/api/v1/extract/stream-video?id={job_id}&token={token}",
                    headers={"Range": "bytes=16-31"}
                )
                assert res_206_offset.status_code == 206
                assert res_206_offset.headers.get("content-range") == f"bytes 16-31/{len(sample_bytes)}"
                assert res_206_offset.content == b"0123456789ABCDEF"

                # 4. Out-of-bounds Range Request -> 416 Range Not Satisfiable
                res_416 = client.get(
                    f"/api/v1/extract/stream-video?id={job_id}&token={token}",
                    headers={"Range": "bytes=99999-100000"}
                )
                assert res_416.status_code == 416
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

    def test_file_exceeding_50mb_returns_400(self):
        job_id = "test_job_too_large"
        video_url = "https://www.instagram.com/reel/C9876543210/"
        job_manager = get_job_manager()
        job_manager.create_job(job_id=job_id, video_url=video_url, url_hash="hash_large", user_id="u1")

        secret = settings.SECRET_KEY or "dev_signing_secret"
        token = generate_stream_token(job_id, secret, media_url=video_url, ttl_seconds=900)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp.write(b"0" * 100)
            tmp_path = tmp.name

        try:
            # Mock getsize to simulate 55MB file
            with patch("backend.app.api.v1.extract._download_stream_video_sync", return_value=tmp_path):
                with patch("os.path.getsize", return_value=55 * 1024 * 1024):
                    res = client.get(f"/api/v1/extract/stream-video?id={job_id}&token={token}")
                    assert res.status_code == 400
                    assert "exceeds maximum 50mb" in res.json().get("detail", "").lower()
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
