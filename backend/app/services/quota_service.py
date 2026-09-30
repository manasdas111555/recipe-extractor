"""
Quota & Rate Limiting Service
=============================
Enforces daily extraction limits for anonymous users and free-tier accounts.
UPA-601: Redis-backed Daily Quota Middleware with In-Memory Dual-Mode Fallback.
"""

import time
import logging
import datetime
import threading
from typing import Tuple, Dict, Optional, Any
import redis

from backend.app.core.config import get_settings

logger = logging.getLogger(__name__)

# Single source of truth aliases resolving from Settings (UPA-1214)
GUEST_DAILY_LIMIT = getattr(get_settings(), "DAILY_GUEST_QUOTA_LIMIT", 20)
FREE_AUTH_DAILY_LIMIT = getattr(get_settings(), "DAILY_FREE_QUOTA_LIMIT", 30)
PRO_DAILY_LIMIT = 999999


class QuotaManager:
    """
    Tracks and enforces daily extraction quotas per user or IP address.
    Supports Redis distributed caching with an in-memory fallback for offline dev.
    """

    def __init__(self):
        self.settings = get_settings()
        self._redis_client: Optional[redis.Redis] = None
        self._redis_checked = False
        self._last_redis_attempt = 0.0
        self._retry_cooldown = 5.0
        self._in_memory_lock = threading.Lock()
        self._in_memory_quotas: Dict[str, Any] = {}
        self._current_day_str: str = datetime.date.today().isoformat()

    def _get_redis(self, max_retries: int = 2, initial_backoff: float = 0.05) -> Optional[redis.Redis]:
        """Lazy-connects to Redis with bounded retry/backoff; returns None if Redis is unreachable."""
        if self._redis_client is not None:
            return self._redis_client

        now = time.time()
        # If recently failed, respect bounded cooldown before retrying to prevent thrashing
        if self._redis_checked and (now - self._last_redis_attempt < self._retry_cooldown):
            return None

        self._last_redis_attempt = now
        self._redis_checked = True
        redis_url = self.settings.REDIS_URL or "redis://localhost:6379/0"

        for attempt in range(1, max_retries + 1):
            try:
                client = redis.Redis.from_url(redis_url, socket_timeout=1.5, socket_connect_timeout=1.5)
                client.ping()
                self._redis_client = client
                logger.info("[QuotaManager] Connected to Redis for distributed quota tracking.")
                return self._redis_client
            except Exception as e:
                logger.warning(f"[QuotaManager] Redis connection attempt {attempt}/{max_retries} failed: {e}")
                if attempt < max_retries:
                    time.sleep(initial_backoff * attempt)

        logger.warning("[QuotaManager] Redis unavailable after retries. Using in-memory fallback quota store.")
        self._redis_client = None
        return None

    def _format_key(self, identifier: str) -> str:
        """Constructs daily partition key: quota:{identifier}:{YYYY-MM-DD}"""
        today = datetime.date.today().isoformat()
        clean_id = identifier.strip().replace(":", "_")
        return f"quota:{clean_id}:{today}"

    def get_limit_for_tier(self, tier: str) -> int:
        """Resolves daily extraction limit for a given user tier string."""
        clean_tier = tier.lower().strip()
        if clean_tier in ["pro", "creator", "business", "enterprise"]:
            return PRO_DAILY_LIMIT
        elif clean_tier in ["free", "user", "authenticated"]:
            return getattr(self.settings, "DAILY_FREE_QUOTA_LIMIT", 30)
        else:  # guest / anonymous
            return getattr(self.settings, "DAILY_GUEST_QUOTA_LIMIT", 20)

    def check_and_consume_quota(
        self,
        identifier: str,
        is_pro: bool = False,
        daily_limit: Optional[int] = None,
        tier: Optional[str] = None
    ) -> Tuple[bool, int, int]:
        """
        Atomically inspects and consumes one extraction from daily quota.
        
        Returns:
            Tuple[allowed (bool), current_usage (int), remaining (int)]
        """
        if tier:
            clean_t = tier.lower().strip()
            if clean_t in ["pro", "creator", "business", "enterprise"]:
                is_pro = True
            elif daily_limit is None:
                daily_limit = self.get_limit_for_tier(clean_t)

        limit = daily_limit or self.settings.DAILY_FREE_QUOTA_LIMIT

        # Pro users have unlimited extractions
        if is_pro:
            return True, 0, 999999

        key = self._format_key(identifier)
        r = self._get_redis()

        # 1. Distributed Redis Storage
        if r:
            try:
                pipe = r.pipeline()
                pipe.incr(key)
                pipe.expire(key, 86400)  # 24 hour TTL
                results = pipe.execute()
                current_count = int(results[0])

                if current_count > limit:
                    remaining = 0
                    allowed = False
                else:
                    remaining = max(0, limit - current_count)
                    allowed = True

                return allowed, current_count, remaining
            except Exception as e:
                logger.warning(f"[QuotaManager] Redis error during quota check ({e}). Falling back to memory.")
                # Fall through to in-memory handling

        # 2. In-Memory Dual-Mode Fallback
        with self._in_memory_lock:
            today_str = datetime.date.today().isoformat()
            if self._current_day_str != today_str:
                self._in_memory_quotas.clear()
                self._current_day_str = today_str

            current_count = self._in_memory_quotas.get(key, 0) + 1
            self._in_memory_quotas[key] = current_count

            if current_count > limit:
                return False, current_count, 0
            else:
                remaining = max(0, limit - current_count)
                return True, current_count, remaining

    def get_quota_status(
        self,
        identifier: str,
        is_pro: bool = False,
        daily_limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Returns non-consuming status inspection of remaining extractions."""
        limit = daily_limit or self.settings.DAILY_FREE_QUOTA_LIMIT
        if is_pro:
            return {"allowed": True, "usage": 0, "remaining": 999999, "limit": 999999, "tier": "pro"}

        key = self._format_key(identifier)
        r = self._get_redis()
        current_count = 0

        if r:
            try:
                val = r.get(key)
                if val:
                    current_count = int(val)
            except Exception:
                current_count = self._in_memory_quotas.get(key, 0)
        else:
            with self._in_memory_lock:
                current_count = self._in_memory_quotas.get(key, 0)

        remaining = max(0, limit - current_count)
        return {
            "allowed": current_count < limit,
            "usage": current_count,
            "remaining": remaining,
            "limit": limit,
            "tier": "free"
        }

    def reset_quota(self, identifier: str):
        """Administrative method to reset quota for a test or specific user."""
        key = self._format_key(identifier)
        r = self._get_redis()
        if r:
            try:
                r.delete(key)
            except Exception:
                pass
        with self._in_memory_lock:
            self._in_memory_quotas.pop(key, None)

    def check_generic_rate_limit(self, key: str, limit: int = 30, window_seconds: int = 60) -> Tuple[bool, int]:
        """
        Generic sliding-window rate limiter utilizing Redis with in-memory fallback.
        Returns (is_allowed, current_count).
        """
        import time
        r = self._get_redis()
        bucket = int(time.time() // window_seconds)
        redis_key = f"rate_limit:{key}:{bucket}"

        if r:
            try:
                pipeline = r.pipeline()
                pipeline.incr(redis_key)
                pipeline.expire(redis_key, window_seconds + 5)
                results = pipeline.execute()
                count = int(results[0])
                return count <= limit, count
            except Exception as e:
                logger.warning(f"[QuotaManager] Redis rate limit error ({e}). Falling back to memory.")

        with self._in_memory_lock:
            now = time.time()
            cutoff = now - window_seconds
            raw_ts = self._in_memory_quotas.get(redis_key, [])
            timestamps = raw_ts if isinstance(raw_ts, list) else []
            timestamps = [t for t in timestamps if t > cutoff]
            timestamps.append(now)
            self._in_memory_quotas[redis_key] = timestamps
            count = len(timestamps)
            return count <= limit, count

    def reset_rate_limits_for_testing(self):
        """Helper to clear in-memory rate limits and quota state for testing."""
        with self._in_memory_lock:
            self._in_memory_quotas.clear()


_quota_manager: Optional[QuotaManager] = None

def get_quota_manager() -> QuotaManager:
    """Returns singleton instance of QuotaManager."""
    global _quota_manager
    if _quota_manager is None:
        _quota_manager = QuotaManager()
    return _quota_manager
