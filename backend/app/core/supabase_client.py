"""
Supabase Direct REST API Client
===============================
Ultra-lightweight, resilient HTTP client interface to Supabase PostgreSQL.
Uses standard HTTP/REST endpoints with service_role / anon key authorization.
"""

import logging
from typing import Optional, Dict, Any, List
import requests
from backend.app.core.config import get_settings

logger = logging.getLogger(__name__)

class SupabaseRestClient:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = (self.settings.SUPABASE_URL or "").rstrip("/")
        self.anon_key = self.settings.SUPABASE_ANON_KEY or ""
        self.service_key = self.settings.SUPABASE_SERVICE_ROLE_KEY or self.anon_key

    def _get_headers(self, use_service_role: bool = False) -> Dict[str, str]:
        key = self.service_key if use_service_role else self.anon_key
        return {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

    def is_configured(self) -> bool:
        """Returns True if Supabase credentials are configured."""
        return bool(self.base_url and (self.anon_key or self.service_key))

    def get_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Fetch user profile from public.profiles table."""
        if not self.is_configured():
            return None
        url = f"{self.base_url}/rest/v1/profiles?id=eq.{user_id}&select=*"
        try:
            r = requests.get(url, headers=self._get_headers(use_service_role=True), timeout=5)
            if r.status_code == 200:
                data = r.json()
                return data[0] if data else None
        except Exception as e:
            logger.error(f"Error fetching Supabase profile for {user_id}: {e}")
        return None

    def get_cached_extraction(self, url_hash: str) -> Optional[Dict[str, Any]]:
        """Query public.extractions for existing completed extraction by SHA-256 url_hash."""
        if not self.is_configured():
            return None
        url = f"{self.base_url}/rest/v1/extractions?url_hash=eq.{url_hash}&status=eq.completed&select=*"
        try:
            r = requests.get(url, headers=self._get_headers(use_service_role=False), timeout=5)
            if r.status_code == 200:
                data = r.json()
                return data[0] if data else None
        except Exception as e:
            logger.error(f"Error querying extraction cache for {url_hash}: {e}")
        return None

    def insert_extraction(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Insert new extraction record into public.extractions."""
        if not self.is_configured():
            return payload
        url = f"{self.base_url}/rest/v1/extractions"
        try:
            r = requests.post(url, headers=self._get_headers(use_service_role=True), json=payload, timeout=5)
            if r.status_code in [200, 201]:
                data = r.json()
                return data[0] if data else payload
        except Exception as e:
            logger.error(f"Error inserting extraction to Supabase: {e}")
        return payload

    def increment_user_quota(self, user_id: str) -> bool:
        """Call atomic RPC procedure to increment user daily extractions count."""
        if not self.is_configured():
            return True
        url = f"{self.base_url}/rest/v1/rpc/increment_user_extraction_count"
        try:
            r = requests.post(
                url,
                headers=self._get_headers(use_service_role=True),
                json={"user_uuid": user_id},
                timeout=5
            )
            return r.status_code in [200, 204]
        except Exception as e:
            logger.error(f"Error incrementing quota for user {user_id}: {e}")
            return False

    def log_affiliate_click(self, click_data: Dict[str, Any]) -> bool:
        """Logs an affiliate click event into public.affiliate_clicks."""
        if not self.is_configured():
            logger.info(f"Supabase not configured, affiliate click logged locally: {click_data}")
            return True
        url = f"{self.base_url}/rest/v1/affiliate_clicks"
        try:
            r = requests.post(url, headers=self._get_headers(use_service_role=True), json=click_data, timeout=5)
            return r.status_code in [200, 201, 204]
        except Exception as e:
            logger.error(f"Error logging affiliate click to Supabase: {e}")
            return False

    # Aliases for worker tasks compatibility
    save_extraction = insert_extraction
    increment_daily_quota = increment_user_quota


_supabase_client: Optional[SupabaseRestClient] = None

def get_supabase_client() -> SupabaseRestClient:
    """Returns singleton Supabase REST client instance."""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = SupabaseRestClient()
    return _supabase_client
