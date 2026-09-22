"""
Supabase Direct REST API Client
===============================
Ultra-lightweight, resilient HTTP client interface to Supabase PostgreSQL.
Uses standard HTTP/REST endpoints with service_role / anon key authorization.
"""

import logging
import datetime
import uuid
from typing import Optional, Dict, Any, List
import requests
from backend.app.core.config import get_settings

logger = logging.getLogger(__name__)


class SupabaseDbError(Exception):
    """Raised when Supabase database is configured but unreachable or encounters an HTTP error."""
    pass

class SupabaseRestClient:
    def __init__(self, base_url: Optional[str] = None, anon_key: Optional[str] = None, service_role_key: Optional[str] = None):
        self.settings = get_settings()
        self.base_url = (base_url or self.settings.SUPABASE_URL or "").rstrip("/")
        self.anon_key = anon_key or self.settings.SUPABASE_ANON_KEY or ""
        self.service_key = service_role_key or self.settings.SUPABASE_SERVICE_ROLE_KEY or self.anon_key

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

    def is_write_allowed(self) -> bool:
        """Returns True if database write operations are enabled via settings."""
        return self.is_configured() and bool(getattr(self.settings, "ALLOW_DB_WRITES", False))

    def get_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Fetch user profile from public.profiles table."""
        if not self.is_configured() or not user_id:
            return None
        try:
            uuid.UUID(str(user_id))
        except (ValueError, TypeError):
            logger.debug("Bypassing profile fetch for non-UUID user_id: %s", user_id)
            return None

        url = f"{self.base_url}/rest/v1/profiles"
        params = {"id": f"eq.{user_id}", "select": "*"}
        try:
            r = requests.get(url, headers=self._get_headers(use_service_role=True), params=params, timeout=5)
            if r.status_code == 200:
                data = r.json()
                return data[0] if data else None
            else:
                logger.error("Supabase get_profile failed [HTTP %s]: %s", r.status_code, r.text[:200])
        except Exception as e:
            logger.error(f"Error fetching Supabase profile for {user_id}: {e}")
        return None

    def get_cached_extraction(self, url_hash: str) -> Optional[Dict[str, Any]]:
        """Query public.extractions for existing completed extraction by SHA-256 url_hash."""
        if not self.is_configured() or not url_hash:
            return None
        url = f"{self.base_url}/rest/v1/extractions"
        params = {"url_hash": f"eq.{url_hash}", "status": "eq.completed", "select": "*"}
        try:
            r = requests.get(url, headers=self._get_headers(use_service_role=False), params=params, timeout=5)
            if r.status_code == 200:
                data = r.json()
                return data[0] if data else None
            else:
                logger.error("Supabase get_cached_extraction failed [HTTP %s]: %s", r.status_code, r.text[:200])
        except Exception as e:
            logger.error(f"Error querying extraction cache for {url_hash}: {e}")
        return None

    def insert_extraction(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Insert new extraction record into public.extractions."""
        if not self.is_write_allowed():
            logger.info("Supabase writes disabled (ALLOW_DB_WRITES=False); skipping DB extraction insert.")
            return payload

        user_id = payload.get("user_id")
        valid_user_id = None
        if user_id:
            try:
                valid_user_id = str(uuid.UUID(str(user_id)))
            except (ValueError, TypeError):
                valid_user_id = None

        db_row = {
            "id": payload.get("id"),
            "user_id": valid_user_id,
            "source_url": payload.get("source_url") or payload.get("url", ""),
            "url_hash": payload.get("url_hash", ""),
            "source_platform": payload.get("source_platform", "other"),
            "classified_domain": payload.get("classified_domain") or payload.get("domain_category", "recipe"),
            "raw_transcript": payload.get("raw_transcript"),
            "structured_data": payload.get("structured_data") or payload.get("content_payload", {}),
            "status": payload.get("status", "completed"),
            "error_message": payload.get("error_message"),
            "processing_time_ms": payload.get("processing_time_ms"),
            "is_public": False
        }
        url = f"{self.base_url}/rest/v1/extractions"
        try:
            r = requests.post(url, headers=self._get_headers(use_service_role=True), json=db_row, timeout=5)
            if r.status_code in [200, 201]:
                data = r.json()
                return data[0] if data else payload
            else:
                logger.error("Supabase insert_extraction failed [HTTP %s]: %s", r.status_code, r.text[:200])
        except Exception as e:
            logger.error(f"Error inserting extraction to Supabase: {e}")
        return payload

    def increment_user_quota(self, user_id: str) -> bool:
        """Call atomic RPC procedure to increment user daily extractions count."""
        if not self.is_write_allowed():
            return True
        try:
            valid_uuid = str(uuid.UUID(str(user_id)))
        except (ValueError, TypeError):
            logger.debug("Skipping RPC quota increment for non-UUID user_id: %s", user_id)
            return True

        url = f"{self.base_url}/rest/v1/rpc/increment_user_extraction_count"
        try:
            r = requests.post(
                url,
                headers=self._get_headers(use_service_role=True),
                json={"user_uuid": valid_uuid},
                timeout=5
            )
            if r.status_code in [200, 204]:
                return True
            else:
                logger.error("Supabase RPC increment_user_quota failed [HTTP %s]: %s", r.status_code, r.text[:200])
                return False
        except Exception as e:
            logger.error(f"Error incrementing quota for user {user_id}: {e}")
            return False

    def log_affiliate_click(self, click_data: Dict[str, Any]) -> bool:
        """Logs an affiliate click event into public.affiliate_clicks."""
        if not self.is_write_allowed():
            logger.info("Supabase writes disabled (ALLOW_DB_WRITES=False); affiliate click logged locally.")
            return True

        user_id = click_data.get("user_id")
        valid_user_id = None
        if user_id:
            try:
                valid_user_id = str(uuid.UUID(str(user_id)))
            except (ValueError, TypeError):
                valid_user_id = None

        db_row = dict(click_data)
        db_row["user_id"] = valid_user_id

        url = f"{self.base_url}/rest/v1/affiliate_clicks"
        try:
            r = requests.post(url, headers=self._get_headers(use_service_role=True), json=db_row, timeout=5)
            if r.status_code in [200, 201, 204]:
                return True
            else:
                logger.error("Supabase log_affiliate_click failed [HTTP %s]: %s", r.status_code, r.text[:200])
                return False
        except Exception as e:
            logger.error(f"Error logging affiliate click to Supabase: {e}")
            return False

    def save_extraction(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Alias for insert_extraction."""
        return self.insert_extraction(payload)

    def increment_daily_quota(self, user_id: str) -> bool:
        """Alias for increment_user_quota."""
        return self.increment_user_quota(user_id)

    @staticmethod
    def _escape_postgrest_val(val: str, for_or: bool = False) -> str:
        """
        Escapes PostgREST filter reserved characters: %, _, (, ), comma, and double quotes.
        Directive 4: Single-column filters must NOT double-quote the value (classified_domain=ilike.*x*).
        Only or=(...) values are double-quoted.
        """
        s = str(val)
        escaped = s.replace("\\", "\\\\") \
                   .replace("%", "\\%") \
                   .replace("_", "\\_") \
                   .replace("(", "\\(") \
                   .replace(")", "\\)") \
                   .replace(",", "\\,")
        if for_or:
            escaped = escaped.replace('"', '""')
            return f'"{escaped}"'
        else:
            escaped = escaped.replace('"', '\\"')
            return escaped

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

        valid_user_id: Optional[str] = None
        if user_id:
            try:
                valid_user_id = str(uuid.UUID(str(user_id)))
            except (ValueError, TypeError):
                valid_user_id = None

        offset = max(0, (page - 1) * limit)
        params: Dict[str, Any] = {
            "select": "*",
            "order": "created_at.desc",
            "limit": limit,
            "offset": offset
        }

        if valid_user_id:
            params["or"] = f'(user_id.eq.{valid_user_id},is_public.eq.true)'
        else:
            params["is_public"] = "eq.true"

        if domain and domain != "all":
            clean_domain = self._escape_postgrest_val(domain, for_or=False)
            params["classified_domain"] = f'ilike.*{clean_domain}*'

        if search_query:
            clean_q = self._escape_postgrest_val(search_query, for_or=True)
            params["or"] = f'(source_url.ilike.*{clean_q}*,raw_transcript.ilike.*{clean_q}*)'

        url = f"{self.base_url}/rest/v1/extractions"
        try:
            r = requests.get(url, headers=self._get_headers(use_service_role=False), params=params, timeout=5)
            if r.status_code == 200:
                return r.json()
            else:
                logger.error("Supabase list_extractions failed [HTTP %s]: %s", r.status_code, r.text[:200])
        except Exception as e:
            logger.error(f"Error listing extractions: {e}")
        return []

    def delete_extraction(self, extraction_id: str, user_id: str) -> bool:
        """Deletes an extraction owned by the user."""
        if not self.is_write_allowed():
            return True
        try:
            uuid.UUID(str(extraction_id))
            uuid.UUID(str(user_id))
        except (ValueError, TypeError):
            logger.warning(f"Invalid UUID for delete_extraction: id={extraction_id}, user_id={user_id}")
            return False

        url = f"{self.base_url}/rest/v1/extractions"
        params = {"id": f"eq.{extraction_id}", "user_id": f"eq.{user_id}"}
        try:
            r = requests.delete(url, headers=self._get_headers(use_service_role=True), params=params, timeout=5)
            if r.status_code in [200, 204]:
                return True
            else:
                logger.error("Supabase delete_extraction failed [HTTP %s]: %s", r.status_code, r.text[:200])
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
        """Updates user profile subscription tier in public.profiles."""
        if not self.is_write_allowed():
            logger.info(f"[Supabase] Tier for user {user_id} updated locally to {tier}.")
            return True

        try:
            valid_uuid = str(uuid.UUID(str(user_id)))
        except (ValueError, TypeError):
            logger.warning(f"Invalid UUID for update_user_subscription: {user_id}")
            return False

        url = f"{self.base_url}/rest/v1/profiles"
        params = {"id": f"eq.{valid_uuid}"}
        payload = {
            "plan_tier": tier,
            "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        try:
            r = requests.patch(
                url,
                headers=self._get_headers(use_service_role=True),
                params=params,
                json=payload,
                timeout=5
            )
            if r.status_code in [200, 204]:
                return True
            else:
                logger.error("Supabase update_user_subscription failed [HTTP %s]: %s", r.status_code, r.text[:200])
                return False
        except Exception as e:
            logger.error(f"Error updating subscription tier for user {user_id}: {e}")
            return False

    def get_affiliate_analytics(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Queries affiliate_clicks table to return aggregate click telemetry analytics."""
        if not self.is_configured():
            return {"total_clicks": 0, "merchants": {}, "items_clicked": 0}

        url = f"{self.base_url}/rest/v1/affiliate_clicks"
        params = {"select": "merchant,target_url,item_name"}
        if user_id:
            try:
                params["user_id"] = f"eq.{uuid.UUID(str(user_id))}"
            except (ValueError, TypeError):
                return {"total_clicks": 0, "merchants": {}, "items_clicked": 0}

        try:
            r = requests.get(url, headers=self._get_headers(use_service_role=True), params=params, timeout=5)
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
            else:
                logger.error("Supabase get_affiliate_analytics failed [HTTP %s]: %s", r.status_code, r.text[:200])
        except Exception as e:
            logger.error(f"Error fetching affiliate analytics: {e}")

        return {"total_clicks": 0, "merchants": {}, "items_clicked": 0}

    def get_public_extraction_by_slug_or_id(self, slug_or_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a public extraction by UUID or title slug."""
        if not self.is_configured() or not slug_or_id:
            return None

        url = f"{self.base_url}/rest/v1/extractions"
        is_uuid = False
        try:
            uuid.UUID(str(slug_or_id))
            is_uuid = True
        except (ValueError, TypeError):
            is_uuid = False

        if is_uuid:
            params = {"is_public": "eq.true", "id": f"eq.{slug_or_id}", "limit": 1}
        else:
            clean_slug = self._escape_postgrest_val(slug_or_id, for_or=False)
            params = {"is_public": "eq.true", "slug": f"eq.{clean_slug}", "limit": 1}

        try:
            r = requests.get(url, headers=self._get_headers(use_service_role=False), params=params, timeout=5)
            if r.status_code == 200:
                data = r.json()
                return data[0] if data else None
            elif r.status_code >= 500:
                logger.error("Supabase get_public_extraction DB error [HTTP %s]: %s", r.status_code, r.text[:200])
                raise SupabaseDbError(f"Supabase HTTP {r.status_code}")
            else:
                logger.error("Supabase get_public_extraction failed [HTTP %s]: %s", r.status_code, r.text[:200])
                return None
        except SupabaseDbError:
            raise
        except Exception as e:
            logger.error(f"Error retrieving public extraction {slug_or_id}: {e}")
            raise SupabaseDbError(f"Network error accessing Supabase: {e}")

    def list_public_extraction_slugs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Returns indexed public extraction slugs and metadata for SEO sitemap generation."""
        if not self.is_configured():
            return []

        url = f"{self.base_url}/rest/v1/extractions"
        params = {
            "is_public": "eq.true",
            "select": "id,created_at,structured_data",
            "order": "created_at.desc",
            "limit": limit
        }
        try:
            r = requests.get(url, headers=self._get_headers(use_service_role=False), params=params, timeout=5)
            if r.status_code == 200:
                data = r.json()
                results = []
                for row in data:
                    content = row.get("structured_data", {})
                    title = content.get("title", f"Recipe {row.get('id')[:8]}")
                    slug = "-".join("".join(c for c in title.lower() if c.isalnum() or c.isspace()).split())
                    results.append({
                        "slug": slug or row.get("id"),
                        "title": title,
                        "category": content.get("category", "recipe"),
                        "updated_at": row.get("created_at")
                    })
                return results
            elif r.status_code >= 500:
                logger.error("Supabase list_public_extraction_slugs DB error [HTTP %s]: %s", r.status_code, r.text[:200])
                raise SupabaseDbError(f"Supabase HTTP {r.status_code}")
            else:
                logger.error("Supabase list_public_extraction_slugs failed [HTTP %s]: %s", r.status_code, r.text[:200])
                return []
        except SupabaseDbError:
            raise
        except Exception as e:
            logger.error(f"Error listing public extraction slugs: {e}")
            raise SupabaseDbError(f"Network error accessing Supabase: {e}")

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

        if self.is_write_allowed():
            try:
                valid_uuid = str(uuid.UUID(str(user_id)))
            except (ValueError, TypeError):
                return True

            url = f"{self.base_url}/rest/v1/profiles"
            params = {"id": f"eq.{valid_uuid}"}
            payload: Dict[str, Any] = {
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
            if custom_amazon_tag is not None:
                payload["custom_amazon_tag"] = custom_amazon_tag.strip()
            if custom_earnkaro_id is not None:
                payload["custom_earnkaro_id"] = custom_earnkaro_id.strip()

            try:
                r = requests.patch(url, headers=self._get_headers(use_service_role=True), params=params, json=payload, timeout=5)
                if r.status_code in [200, 204]:
                    return True
                else:
                    logger.error("Supabase update_creator_tags failed [HTTP %s]: %s", r.status_code, r.text[:200])
                    return False
            except Exception as e:
                logger.error(f"Error updating creator tags for user {user_id}: {e}")
                return False

        return True

    def record_telemetry_event(self, event_data: Dict[str, Any]) -> bool:
        """Records product conversion funnel and growth telemetry events."""
        if not hasattr(self, "_in_memory_telemetry"):
            self._in_memory_telemetry = []
        self._in_memory_telemetry.append(event_data)

        if self.is_write_allowed():
            url = f"{self.base_url}/rest/v1/telemetry_events"
            try:
                r = requests.post(url, headers=self._get_headers(use_service_role=True), json=event_data, timeout=5)
                if r.status_code in [200, 201, 204]:
                    return True
                else:
                    logger.error("Supabase record_telemetry_event failed [HTTP %s]: %s", r.status_code, r.text[:200])
                    return False
            except Exception as e:
                logger.error(f"Error recording telemetry event to Supabase: {e}")
                return False

        return True

    def log_beta_telemetry(
        self,
        source_platform: str,
        source_url: str,
        classified_domain: Optional[str] = None,
        turnaround_time_ms: Optional[int] = None,
        status: str = "completed"
    ) -> bool:
        """Logs beta telemetry into public.beta_telemetry_feed table."""
        if not self.is_write_allowed():
            return True
        url = f"{self.base_url}/rest/v1/beta_telemetry_feed"
        payload = {
            "source_platform": source_platform,
            "source_url": source_url,
            "classified_domain": classified_domain or "general",
            "turnaround_time_ms": turnaround_time_ms or 0,
            "status": status
        }
        try:
            r = requests.post(url, headers=self._get_headers(use_service_role=True), json=payload, timeout=5)
            if r.status_code in [200, 201, 204]:
                return True
            else:
                logger.error("Supabase log_beta_telemetry failed [HTTP %s]: %s", r.status_code, r.text[:200])
                return False
        except Exception as e:
            logger.error(f"Error logging beta telemetry: {e}")
            return False

    def get_telemetry_funnel(self) -> Dict[str, Any]:
        """Calculates conversion funnel counts and drop-off metrics."""
        events = list(getattr(self, "_in_memory_telemetry", []))
        if self.is_configured():
            url = f"{self.base_url}/rest/v1/telemetry_events"
            params = {"select": "event_name,created_at"}
            try:
                r = requests.get(url, headers=self._get_headers(use_service_role=True), params=params, timeout=5)
                if r.status_code == 200:
                    events.extend(r.json())
                else:
                    logger.error("Supabase get_telemetry_funnel failed [HTTP %s]: %s", r.status_code, r.text[:200])
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
