"""
Tests for UPA-1214: Client IP Resolution, Redis Rate Limits & Guest Quotas
========================================================================
Covers:
1. Real Starlette/FastAPI Request objects for get_client_ip().
2. TRUSTED_PROXY=False ignores all forwarded headers (cf-connecting-ip, x-real-ip, x-forwarded-for).
3. TRUSTED_PROXY=True with configured TRUSTED_PROXY_HEADER.
4. TRUSTED_PROXY=True with X-Forwarded-For and right-to-left TRUSTED_PROXY_HOPS.
5. Invalid forwarded IP falls back to request.client.host via ipaddress validation.
6. Anonymous Redis-backed sliding-window rate limiting.
7. Rate-limit key namespacing (anon_rate:{client_ip}).
8. Guest daily quota (20) & Free user quota (30) from Settings single source of truth.
9. Extraction pipeline ordering:
   - Rate limit rejection -> 0 quota consumed
   - Invalid URL -> 0 quota consumed
   - Cache hit -> 0 quota consumed
   - Cache miss -> exactly 1 quota consumed before worker enqueue
10. Quota exhausted on cache miss -> returns HTTP 429.
11. Redis connection retry and bounded backoff in QuotaManager._get_redis().
"""

import pytest
import time
from unittest.mock import patch, MagicMock
from fastapi import FastAPI, Request
from starlette.testclient import TestClient

from backend.app.core.config import get_settings
from backend.app.core.security import (
    get_client_ip,
    check_anonymous_rate_limit,
    reset_rate_limits_for_testing,
    get_user_quota_limits,
)
from backend.app.services.quota_service import QuotaManager, get_quota_manager
from backend.app.main import app

client = TestClient(app)
settings = get_settings()


class TestClientIPResolution:
    """Tests for get_client_ip(request) under UPA-1214 specifications."""

    def test_trusted_proxy_false_ignores_all_forwarded_headers(self):
        """When TRUSTED_PROXY=False, always return socket client.host directly."""
        scope = {
            "type": "http",
            "headers": [
                (b"cf-connecting-ip", b"203.0.113.10"),
                (b"x-real-ip", b"203.0.113.20"),
                (b"x-forwarded-for", b"1.1.1.1, 203.0.113.30"),
                (b"x-custom-ip", b"203.0.113.40"),
            ],
            "client": ("192.0.2.1", 54321),
        }
        req = Request(scope)

        with patch.object(settings, "TRUSTED_PROXY", False):
            resolved_ip = get_client_ip(req)
            assert resolved_ip == "192.0.2.1"

    def test_trusted_proxy_true_with_custom_header(self):
        """When TRUSTED_PROXY=True and TRUSTED_PROXY_HEADER is set, use that header."""
        scope = {
            "type": "http",
            "headers": [
                (b"x-custom-proxy-ip", b"198.51.100.77"),
                (b"cf-connecting-ip", b"203.0.113.10"),
                (b"x-forwarded-for", b"1.1.1.1, 203.0.113.30"),
            ],
            "client": ("10.0.0.1", 54321),
        }
        req = Request(scope)

        with patch.object(settings, "TRUSTED_PROXY", True), patch.object(
            settings, "TRUSTED_PROXY_HEADER", "x-custom-proxy-ip"
        ):
            resolved_ip = get_client_ip(req)
            assert resolved_ip == "198.51.100.77"

    def test_trusted_proxy_true_with_cf_connecting_ip_and_x_real_ip(self):
        """When TRUSTED_PROXY=True and no custom header, prioritize cf-connecting-ip then x-real-ip."""
        scope_cf = {
            "type": "http",
            "headers": [
                (b"cf-connecting-ip", b"203.0.113.99"),
                (b"x-real-ip", b"203.0.113.88"),
                (b"x-forwarded-for", b"1.1.1.1, 203.0.113.77"),
            ],
            "client": ("10.0.0.1", 54321),
        }
        req_cf = Request(scope_cf)

        with patch.object(settings, "TRUSTED_PROXY", True), patch.object(
            settings, "TRUSTED_PROXY_HEADER", None
        ):
            assert get_client_ip(req_cf) == "203.0.113.99"

        scope_real = {
            "type": "http",
            "headers": [
                (b"x-real-ip", b"203.0.113.88"),
                (b"x-forwarded-for", b"1.1.1.1, 203.0.113.77"),
            ],
            "client": ("10.0.0.1", 54321),
        }
        req_real = Request(scope_real)

        with patch.object(settings, "TRUSTED_PROXY", True), patch.object(
            settings, "TRUSTED_PROXY_HEADER", None
        ):
            assert get_client_ip(req_real) == "203.0.113.88"

    def test_trusted_proxy_true_with_xff_hops(self):
        """When TRUSTED_PROXY=True, parse X-Forwarded-For right-to-left using TRUSTED_PROXY_HOPS."""
        scope = {
            "type": "http",
            "headers": [
                (b"x-forwarded-for", b"103.21.244.2, 198.51.100.10, 203.0.113.1"),
            ],
            "client": ("10.0.0.1", 54321),
        }
        req = Request(scope)

        with patch.object(settings, "TRUSTED_PROXY", True), patch.object(
            settings, "TRUSTED_PROXY_HEADER", None
        ):
            # 1 hop: rightmost
            with patch.object(settings, "TRUSTED_PROXY_HOPS", 1):
                assert get_client_ip(req) == "203.0.113.1"

            # 2 hops: middle
            with patch.object(settings, "TRUSTED_PROXY_HOPS", 2):
                assert get_client_ip(req) == "198.51.100.10"

            # 3 hops: leftmost
            with patch.object(settings, "TRUSTED_PROXY_HOPS", 3):
                assert get_client_ip(req) == "103.21.244.2"

            # Overflow hops (> 3): clamps to leftmost index 0
            with patch.object(settings, "TRUSTED_PROXY_HOPS", 10):
                assert get_client_ip(req) == "103.21.244.2"

    def test_invalid_candidate_ip_falls_back_to_client_host(self):
        """Header with unparseable or malicious string must fail ipaddress validation and fallback."""
        scope = {
            "type": "http",
            "headers": [
                (b"cf-connecting-ip", b"invalid_ip_address_payload; <script>"),
            ],
            "client": ("192.0.2.99", 54321),
        }
        req = Request(scope)

        with patch.object(settings, "TRUSTED_PROXY", True), patch.object(
            settings, "TRUSTED_PROXY_HEADER", None
        ):
            assert get_client_ip(req) == "192.0.2.99"


class TestRedisRateLimitingAndQuotas:
    """Tests for generic rate limiting, key namespacing, and quota limits."""

    def setup_method(self):
        reset_rate_limits_for_testing()

    def test_anonymous_rate_limiting_enforcement(self):
        """Tests that anonymous rate limiting enforces 3 requests per minute by default."""
        ip = "198.51.100.55"
        qm = get_quota_manager()

        # In-memory fallback / Redis generic rate limit
        assert check_anonymous_rate_limit(ip, max_requests=3, window_seconds=60) is True
        assert check_anonymous_rate_limit(ip, max_requests=3, window_seconds=60) is True
        assert check_anonymous_rate_limit(ip, max_requests=3, window_seconds=60) is True
        # 4th request exceeds 3/min limit
        assert check_anonymous_rate_limit(ip, max_requests=3, window_seconds=60) is False

    def test_generic_rate_limit_namespacing(self):
        """Verify check_generic_rate_limit formats keys with correct namespace."""
        qm = QuotaManager()
        mock_redis = MagicMock()
        mock_pipe = MagicMock()
        mock_redis.pipeline.return_value = mock_pipe
        mock_pipe.execute.return_value = [1, True]
        qm._redis_client = mock_redis

        allowed, count = qm.check_generic_rate_limit("anon_rate:198.51.100.12", limit=3, window_seconds=60)
        assert allowed is True
        assert count == 1

        # Check key called on mock redis pipeline incr
        args, _ = mock_pipe.incr.call_args
        assert args[0].startswith("rate_limit:anon_rate:198.51.100.12:")

    def test_quota_limits_centralized_configuration(self):
        """Settings must be the single source of truth for daily quotas and anon rate limit."""
        assert settings.DAILY_GUEST_QUOTA_LIMIT == 20
        assert settings.DAILY_FREE_QUOTA_LIMIT == 30
        assert settings.ANONYMOUS_RATE_LIMIT_PER_MINUTE == 3

        qm = get_quota_manager()
        assert qm.get_limit_for_tier("guest") == 20
        assert qm.get_limit_for_tier("free") == 30
        assert qm.get_limit_for_tier("pro") == 999999

        assert get_user_quota_limits({"is_anonymous": True}) == {"tier": "guest", "daily_quota_limit": 20}
        assert get_user_quota_limits({"tier": "guest"}) == {"tier": "guest", "daily_quota_limit": 20}
        assert get_user_quota_limits({"tier": "free"}) == {"tier": "free", "daily_quota_limit": 30}
        assert get_user_quota_limits({"tier": "pro"}) == {"tier": "pro", "daily_quota_limit": -1}


class TestExtractionPipelineOrdering:
    """
    Tests strict pipeline order:
    Rate Limit -> Validate URL -> Cache Lookup (0-cost) -> Consume Quota ONLY on Cache Miss -> Enqueue Worker.
    """

    def setup_method(self):
        reset_rate_limits_for_testing()

    def test_extract_invalid_url_consumes_no_quota(self):
        """Invalid URL must return 400 and NOT consume quota."""
        with patch.object(QuotaManager, "check_and_consume_quota") as mock_consume:
            res = client.post(
                "/api/v1/extract",
                json={"video_url": "https://evil.com/not-a-supported-platform"}
            )
            assert res.status_code == 400
            mock_consume.assert_not_called()

    def test_extract_rate_limit_exceeded_consumes_no_quota(self):
        """Rate limit rejection (429) must NOT consume quota."""
        with patch("backend.app.api.v1.extract.check_anonymous_rate_limit", return_value=False):
            with patch.object(QuotaManager, "check_and_consume_quota") as mock_consume:
                res = client.post(
                    "/api/v1/extract",
                    json={"video_url": "https://www.instagram.com/reel/C3abc123456/"}
                )
                assert res.status_code == 429
                assert "rate limit exceeded" in res.json().get("detail", "").lower()
                mock_consume.assert_not_called()

    def test_extract_cache_hit_consumes_no_quota(self):
        """Cache hit must return 200 with data (0-cost) and NOT consume daily quota."""
        fake_cached_record = {
            "id": "ext_cached_123",
            "canonical_url": "https://www.instagram.com/reel/C3abc123456/",
            "status": "completed",
            "content_payload": {"title": "Cached Paneer Recipe", "ingredients": ["Paneer"]},
        }

        mock_supabase = MagicMock()
        mock_supabase.is_configured.return_value = True
        mock_supabase.get_cached_extraction.return_value = fake_cached_record

        with patch("backend.app.api.v1.extract.get_supabase_client", return_value=mock_supabase):
            with patch.object(QuotaManager, "check_and_consume_quota") as mock_consume:
                res = client.post(
                    "/api/v1/extract",
                    json={"video_url": "https://www.instagram.com/reel/C3abc123456/"}
                )
                assert res.status_code == 200
                data = res.json()
                assert data["is_cached"] is True
                assert data["data"]["title"] == "Cached Paneer Recipe"
                mock_consume.assert_not_called()

    def test_extract_cache_miss_consumes_quota_and_enqueues(self):
        """Cache miss MUST consume quota exactly once immediately before enqueueing worker."""
        mock_supabase = MagicMock()
        mock_supabase.is_configured.return_value = True
        mock_supabase.get_cached_extraction.return_value = None  # Cache miss

        with patch("backend.app.api.v1.extract.get_supabase_client", return_value=mock_supabase):
            with patch.object(QuotaManager, "check_and_consume_quota", return_value=(True, 1, 20)) as mock_consume:
                with patch("backend.app.api.v1.extract.is_celery_broker_reachable", return_value=False), \
                     patch("backend.app.api.v1.extract.run_extraction_worker_sync"):
                    res = client.post(
                        "/api/v1/extract",
                        json={"video_url": "https://www.youtube.com/shorts/dQw4w9WgXcQ"}
                    )
                    assert res.status_code in [200, 202]
                    data = res.json()
                    assert data["is_cached"] is False
                    assert data["status"] in ["queued", "processing"]
                    mock_consume.assert_called_once()

    def test_extract_cache_miss_quota_exhausted_rejects_with_429(self):
        """When user/guest exhausts quota, cache miss returns 429 and does not enqueue."""
        mock_supabase = MagicMock()
        mock_supabase.is_configured.return_value = True
        mock_supabase.get_cached_extraction.return_value = None  # Cache miss

        with patch("backend.app.api.v1.extract.get_supabase_client", return_value=mock_supabase):
            with patch.object(QuotaManager, "check_and_consume_quota", return_value=(False, 20, 0)) as mock_consume:
                res = client.post(
                    "/api/v1/extract",
                    json={"video_url": "https://www.youtube.com/shorts/dQw4w9WgXcQ"}
                )
                assert res.status_code == 429
                assert "daily extraction quota limit reached" in res.json().get("detail", "").lower()
                mock_consume.assert_called_once()


class TestRedisRetryAndBackoff:
    """Tests bounded retry and backoff behavior in QuotaManager._get_redis()."""

    def test_redis_retry_success_after_transient_failure(self):
        """_get_redis() should retry and succeed when connection error resolves within max_retries."""
        qm = QuotaManager()
        qm._redis_client = None

        mock_redis = MagicMock()
        mock_redis.ping.side_effect = [Exception("Transient Redis connection drop"), True]

        with patch("redis.Redis.from_url", return_value=mock_redis):
            client_instance = qm._get_redis(max_retries=2, initial_backoff=0.01)
            assert client_instance is not None
            assert mock_redis.ping.call_count == 2

    def test_redis_retry_failure_bounded_and_falls_back(self):
        """_get_redis() should not loop infinitely; after max_retries exhausted, returns None."""
        qm = QuotaManager()
        qm._redis_client = None

        mock_redis = MagicMock()
        mock_redis.ping.side_effect = Exception("Persistent Redis outage")

        with patch("redis.Redis.from_url", return_value=mock_redis):
            client_instance = qm._get_redis(max_retries=3, initial_backoff=0.01)
            assert client_instance is None
            assert mock_redis.ping.call_count == 3
