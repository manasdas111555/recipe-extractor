"""
Supabase Direct REST API Client
===============================
Ultra-lightweight, resilient HTTP client interface to Supabase PostgreSQL.
Uses standard HTTP/REST endpoints with service_role / anon key authorization.
"""

import logging
import datetime
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

    def list_extractions(
        self,
        user_id: Optional[str] = None,
        search_query: Optional[str] = None,
        domain: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Queries public.extractions with search and domain filtering."""
        if not self.is_configured():
            return []

        offset = max(0, (page - 1) * limit)
        filters = ["select=*"]
        if user_id:
            filters.append(f"or=(user_id.eq.{user_id},is_public.eq.true)")
        else:
            filters.append("is_public.eq.true")

        if domain and domain != "all":
            filters.append(f"classified_domain.ilike.%{domain}%")

        if search_query:
            filters.append(f"or=(source_url.ilike.%{search_query}%,raw_transcript.ilike.%{search_query}%)")

        filters.append("order=created_at.desc")
        filters.append(f"limit={limit}")
        filters.append(f"offset={offset}")

        query_str = "&".join(filters)
        url = f"{self.base_url}/rest/v1/extractions?{query_str}"
        try:
            r = requests.get(url, headers=self._get_headers(use_service_role=False), timeout=5)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            logger.error(f"Error listing extractions: {e}")
        return []

    def delete_extraction(self, extraction_id: str, user_id: str) -> bool:
        """Deletes an extraction owned by the user."""
        if not self.is_configured():
            return True
        url = f"{self.base_url}/rest/v1/extractions?id=eq.{extraction_id}&user_id=eq.{user_id}"
        try:
            r = requests.delete(url, headers=self._get_headers(use_service_role=True), timeout=5)
            return r.status_code in [200, 204]
        except Exception as e:
            logger.error(f"Error deleting extraction {extraction_id}: {e}")
            return False

    def update_user_subscription(
        self,
        user_id: str,
        tier: str,
        provider: Optional[str] = None,
        subscription_id: Optional[str] = None
    ) -> bool:
        """Updates user profile subscription tier and metadata in public.profiles."""
        if not self.is_configured():
            logger.info(f"[Supabase] Unconfigured: Tier for user {user_id} updated locally to {tier}.")
            return True

        url = f"{self.base_url}/rest/v1/profiles?id=eq.{user_id}"
        payload = {
            "tier": tier,
            "subscription_provider": provider,
            "subscription_id": subscription_id,
            "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        try:
            r = requests.patch(
                url,
                headers=self._get_headers(use_service_role=True),
                json=payload,
                timeout=5
            )
            return r.status_code in [200, 204]
        except Exception as e:
            logger.error(f"Error updating subscription tier for user {user_id}: {e}")
            return False

    def get_affiliate_analytics(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Queries affiliate_clicks table to return aggregate click telemetry analytics."""
        if not self.is_configured():
            return {
                "total_clicks": 0,
                "merchants": {},
                "items_clicked": 0
            }

        url = f"{self.base_url}/rest/v1/affiliate_clicks?select=merchant,target_url,item_name"
        if user_id:
            url += f"&user_id=eq.{user_id}"

        try:
            r = requests.get(url, headers=self._get_headers(use_service_role=True), timeout=5)
            if r.status_code == 200:
                rows = r.json()
                merchants_count: Dict[str, int] = {}
                for row in rows:
                    m = row.get("merchant", "unknown")
                    merchants_count[m] = merchants_count.get(m, 0) + 1
                return {
                    "total_clicks": len(rows),
                    "merchants": merchants_count,
                    "items_clicked": sum(1 for row in rows if row.get("item_name"))
                }
        except Exception as e:
            logger.error(f"Error fetching affiliate analytics: {e}")

        return {"total_clicks": 0, "merchants": {}, "items_clicked": 0}

    def _get_sample_public_extraction(self, slug_or_id: str) -> Dict[str, Any]:
        """Provides rich structured fallback extraction for SEO demo, tests, and seed slugs."""
        clean_title = slug_or_id.replace("-", " ").title()
        return {
            "id": f"ext_{slug_or_id[:16]}",
            "slug": slug_or_id,
            "title": clean_title,
            "classified_domain": "recipe",
            "is_public": True,
            "source_url": "https://www.instagram.com/reel/C123456789/",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "extracted_content": {
                "title": clean_title,
                "category": "Recipe",
                "cook_time_minutes": 25,
                "prep_time_minutes": 15,
                "servings": 4,
                "ingredients": [
                    {"name": "Potatoes", "quantity": "4", "unit": "medium"},
                    {"name": "Cumin seeds", "quantity": "1", "unit": "tsp"},
                    {"name": "Garam masala", "quantity": "1/2", "unit": "tsp"},
                    {"name": "Samosa pastry sheets", "quantity": "12", "unit": "sheets"}
                ],
                "steps": [
                    "Boil, peel, and mash the potatoes.",
                    "Heat oil in a pan and temper with cumin seeds.",
                    "Add mashed potatoes and spices, mix well, and cool.",
                    "Fold pastry sheets into cones, stuff with filling, and seal.",
                    "Air fry at 180C (350F) for 12-15 minutes until crispy and golden."
                ]
            }
        }

    def get_public_extraction_by_slug_or_id(self, slug_or_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a public extraction by UUID or title slug."""
        if self.is_configured():
            url = f"{self.base_url}/rest/v1/extractions?is_public=eq.true&or=(id.eq.{slug_or_id},url_hash.ilike.%{slug_or_id}%)&limit=1"
            try:
                r = requests.get(url, headers=self._get_headers(use_service_role=False), timeout=5)
                if r.status_code == 200 and r.json():
                    return r.json()[0]
            except Exception as e:
                logger.error(f"Error retrieving public extraction {slug_or_id}: {e}")

        # Return sample extraction fallback
        return self._get_sample_public_extraction(slug_or_id)

    def list_public_extraction_slugs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Returns indexed public extraction slugs and metadata for SEO sitemap generation."""
        default_slugs = [
            {
                "slug": "crispy-air-fryer-samosa",
                "title": "Crispy Air Fryer Samosa",
                "category": "recipe",
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
            {
                "slug": "high-protein-paneer-bhurji",
                "title": "High Protein Paneer Bhurji",
                "category": "recipe",
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
            {
                "slug": "10-minute-garlic-butter-noodles",
                "title": "10 Minute Garlic Butter Noodles",
                "category": "recipe",
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        ]

        if self.is_configured():
            url = f"{self.base_url}/rest/v1/extractions?is_public=eq.true&select=id,created_at,extracted_content&order=created_at.desc&limit={limit}"
            try:
                r = requests.get(url, headers=self._get_headers(use_service_role=False), timeout=5)
                if r.status_code == 200 and r.json():
                    results = []
                    for row in r.json():
                        content = row.get("extracted_content", {})
                        title = content.get("title", f"Recipe {row.get('id')[:8]}")
                        slug = "-".join("".join(c for c in title.lower() if c.isalnum() or c.isspace()).split())
                        results.append({
                            "slug": slug or row.get("id"),
                            "title": title,
                            "category": content.get("category", "recipe"),
                            "updated_at": row.get("created_at")
                        })
                    if results:
                        return results
            except Exception as e:
                logger.error(f"Error listing public extraction slugs: {e}")

        return default_slugs

    def update_creator_tags(
        self,
        user_id: str,
        custom_amazon_tag: Optional[str] = None,
        custom_earnkaro_id: Optional[str] = None
    ) -> bool:
        """Updates creator affiliate tag vault in public.profiles."""
        if not hasattr(self, "_in_memory_creator_tags"):
            self._in_memory_creator_tags = {}
        self._in_memory_creator_tags[user_id] = {
            "custom_amazon_tag": custom_amazon_tag,
            "custom_earnkaro_id": custom_earnkaro_id
        }

        if self.is_configured() and user_id != "guest_user":
            url = f"{self.base_url}/rest/v1/profiles?id=eq.{user_id}"
            payload: Dict[str, Any] = {
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
            if custom_amazon_tag is not None:
                payload["custom_amazon_tag"] = custom_amazon_tag.strip()
            if custom_earnkaro_id is not None:
                payload["custom_earnkaro_id"] = custom_earnkaro_id.strip()

            try:
                r = requests.patch(url, headers=self._get_headers(use_service_role=True), json=payload, timeout=5)
                if r.status_code in [200, 204]:
                    return True
            except Exception as e:
                logger.error(f"Error updating creator tags for user {user_id}: {e}")

        return True

    def record_telemetry_event(self, event_data: Dict[str, Any]) -> bool:
        """Records product conversion funnel and growth telemetry events."""
        if not hasattr(self, "_in_memory_telemetry"):
            self._in_memory_telemetry = []
        self._in_memory_telemetry.append(event_data)

        if self.is_configured():
            url = f"{self.base_url}/rest/v1/telemetry_events"
            try:
                r = requests.post(url, headers=self._get_headers(use_service_role=True), json=event_data, timeout=5)
                if r.status_code in [200, 201, 204]:
                    return True
            except Exception as e:
                logger.error(f"Error recording telemetry event to Supabase: {e}")

        return True

    def get_telemetry_funnel(self) -> Dict[str, Any]:
        """Calculates conversion funnel counts and drop-off metrics."""
        events = list(getattr(self, "_in_memory_telemetry", []))
        if self.is_configured():
            url = f"{self.base_url}/rest/v1/telemetry_events?select=event_name,created_at"
            try:
                r = requests.get(url, headers=self._get_headers(use_service_role=True), timeout=5)
                if r.status_code == 200:
                    events.extend(r.json())
            except Exception as e:
                logger.error(f"Error fetching remote telemetry events: {e}")

        counts = {
            "video_shared": 0,
            "extraction_rendered": 0,
            "affiliate_outbound_clicked": 0,
            "paywall_hit": 0,
            "subscription_converted": 0
        }
        for ev in events:
            name = ev.get("event_name")
            if name in counts:
                counts[name] += 1

        shared = max(1, counts["video_shared"])
        conversion_rate_pct = round((counts["subscription_converted"] / shared) * 100, 2)

        return {
            "funnel_counts": counts,
            "total_events": len(events),
            "conversion_rate_percent": conversion_rate_pct
        }

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
