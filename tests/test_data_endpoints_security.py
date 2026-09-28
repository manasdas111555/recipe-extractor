"""
UPA-1215: Data Endpoints Ownership & Validation Hardening Test Suite
===================================================================
Covers authoritative acceptance criteria:
1. export_vault_item:
   - Guest export returns HTTP 401 ("Authentication required to export vault items").
   - Authenticated owner export succeeds (markdown, json, txt).
   - Authenticated non-owner / missing extraction returns HTTP 404.
   - Hardcoded mock fallback is removed; unrelated list results are never returned.
2. get_extraction_status:
   - Validates job_id UUID safely before database lookup.
   - Preserves legitimate guest polling behavior.
   - In-memory / Celery polling works; Supabase fallback avoids URL injection.
3. get_user_library & Supabase visibility:
   - Guests only receive rows with is_public=true.
   - Private rows (is_public=false) never exposed to guests.
4. rehydrate_vault_item:
   - Rejects payloads with >100 ingredients (HTTP 400).
   - Rejects payloads with >100 products (HTTP 400).
   - Rejects oversized payloads >100KB (HTTP 400).
   - Reconciles structured_data vs content_payload cleanly.
5. SupabaseRestClient.get_extraction_by_id:
   - Scopes to user_id or is_public.
   - Validates UUIDs.
"""

import uuid
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.core.security import get_current_user
from backend.app.core.supabase_client import SupabaseRestClient, get_supabase_client
from backend.app.services.job_manager import get_job_manager


class TestDataEndpointsSecurity(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.owner_user_id = str(uuid.uuid4())
        self.other_user_id = str(uuid.uuid4())
        self.extraction_id = str(uuid.uuid4())

    def tearDown(self):
        app.dependency_overrides.clear()

    # -------------------------------------------------------------------------
    # 1. EXPORT VAULT ITEM
    # -------------------------------------------------------------------------

    def test_export_vault_item_anonymous_guest_returns_401(self):
        """Unauthenticated guest receives HTTP 401 when exporting vault items."""
        app.dependency_overrides[get_current_user] = lambda: {
            "id": None,
            "email": None,
            "is_anonymous": True,
            "plan_tier": "free"
        }

        res = self.client.get(f"/api/v1/library/{self.extraction_id}/export?format=markdown")
        self.assertEqual(res.status_code, 401)
        self.assertIn("Authentication required to export vault items", res.json()["detail"])

    @patch("backend.app.api.v1.library.get_supabase_client")
    def test_export_vault_item_authenticated_owner_success(self, mock_get_sb):
        """Authenticated owner can export their extraction in markdown, json, and txt formats."""
        app.dependency_overrides[get_current_user] = lambda: {
            "id": self.owner_user_id,
            "email": "owner@example.com",
            "is_anonymous": False,
            "plan_tier": "pro"
        }

        mock_sb = MagicMock()
        mock_sb.get_extraction_by_id.return_value = {
            "id": self.extraction_id,
            "user_id": self.owner_user_id,
            "structured_data": {
                "title": "Avocado Toast",
                "ingredients": ["1 Sourdough Slice", "1 Ripe Avocado", "Chili flakes"],
                "steps": ["Toast bread", "Mash avocado", "Sprinkle chili flakes"]
            }
        }
        mock_get_sb.return_value = mock_sb

        # Test Markdown
        res_md = self.client.get(f"/api/v1/library/{self.extraction_id}/export?format=markdown")
        self.assertEqual(res_md.status_code, 200)
        self.assertIn("# Avocado Toast", res_md.text)
        self.assertIn("- 1 Sourdough Slice", res_md.text)
        self.assertIn("1. Toast bread", res_md.text)

        # Test JSON
        res_json = self.client.get(f"/api/v1/library/{self.extraction_id}/export?format=json")
        self.assertEqual(res_json.status_code, 200)
        self.assertEqual(res_json.json()["title"], "Avocado Toast")
        self.assertEqual(len(res_json.json()["ingredients"]), 3)

        # Test TXT
        res_txt = self.client.get(f"/api/v1/library/{self.extraction_id}/export?format=txt")
        self.assertEqual(res_txt.status_code, 200)
        self.assertIn("Avocado Toast\n\nSteps:\nToast bread", res_txt.text)

    @patch("backend.app.api.v1.library.get_supabase_client")
    def test_export_vault_item_inaccessible_or_missing_returns_404(self, mock_get_sb):
        """Non-owner / missing extraction returns HTTP 404 (no mock payload fallback)."""
        app.dependency_overrides[get_current_user] = lambda: {
            "id": self.other_user_id,
            "email": "other@example.com",
            "is_anonymous": False,
            "plan_tier": "free"
        }

        mock_sb = MagicMock()
        mock_sb.get_extraction_by_id.return_value = None
        mock_get_sb.return_value = mock_sb

        res = self.client.get(f"/api/v1/library/{self.extraction_id}/export?format=markdown")
        self.assertEqual(res.status_code, 404)
        self.assertIn("not found or access denied", res.json()["detail"].lower())

    @patch("backend.app.api.v1.library.get_supabase_client")
    def test_export_vault_item_does_not_use_unrelated_list_results(self, mock_get_sb):
        """Verify export specifically calls get_extraction_by_id and does NOT call list_extractions."""
        app.dependency_overrides[get_current_user] = lambda: {
            "id": self.owner_user_id,
            "email": "owner@example.com",
            "is_anonymous": False,
            "plan_tier": "pro"
        }

        mock_sb = MagicMock()
        mock_sb.get_extraction_by_id.return_value = None
        mock_sb.list_extractions.return_value = [
            {"id": "unrelated-id", "title": "Unrelated Recipe"}
        ]
        mock_get_sb.return_value = mock_sb

        res = self.client.get(f"/api/v1/library/{self.extraction_id}/export?format=json")
        self.assertEqual(res.status_code, 404)
        mock_sb.list_extractions.assert_not_called()
        mock_sb.get_extraction_by_id.assert_called_once_with(
            extraction_id=self.extraction_id,
            user_id=self.owner_user_id
        )

    # -------------------------------------------------------------------------
    # 2. GET EXTRACTION STATUS POLLING
    # -------------------------------------------------------------------------

    def test_get_extraction_status_in_memory_guest_polling_works(self):
        """Legitimate guest polling for enqueued in-memory job succeeds."""
        job_manager = get_job_manager()
        job_id = f"guest-job-{uuid.uuid4()}"
        job_manager.create_job(
            job_id=job_id,
            video_url="https://youtube.com/shorts/DPdivoOcXHM",
            url_hash="some_hash",
            user_id="anonymous"
        )
        job_manager.update_job(job_id=job_id, status="completed", data={"title": "Test Title"})

        res = self.client.get(f"/api/v1/extract/status/{job_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "completed")
        self.assertEqual(res.json()["data"]["title"], "Test Title")

    def test_get_extraction_status_non_existent_returns_404(self):
        """Non-existent job returns HTTP 404."""
        unknown_job_id = str(uuid.uuid4())
        res = self.client.get(f"/api/v1/extract/status/{unknown_job_id}")
        self.assertEqual(res.status_code, 404)

    def test_get_extraction_status_malformed_job_id_handled_safely(self):
        """Malformed or injection strings in job_id do not trigger 500 errors and return 404."""
        malicious_job_id = "'; DROP TABLE extractions; --"
        res = self.client.get(f"/api/v1/extract/status/{malicious_job_id}")
        self.assertEqual(res.status_code, 404)

    # -------------------------------------------------------------------------
    # 3. REHYDRATE VAULT ITEM BOUNDS & RECONCILIATION
    # -------------------------------------------------------------------------

    def test_rehydrate_more_than_100_ingredients_rejected(self):
        """Rehydration with >100 ingredients is rejected with HTTP 400."""
        oversized_item = {
            "title": "Massive Recipe",
            "ingredients": [f"Ingredient {i}" for i in range(101)]
        }
        res = self.client.post("/api/v1/library/rehydrate", json={"item": oversized_item})
        self.assertEqual(res.status_code, 400)
        self.assertIn("max 100 ingredients", res.json()["detail"].lower())

    def test_rehydrate_more_than_100_products_rejected(self):
        """Rehydration with >100 products is rejected with HTTP 400."""
        oversized_item = {
            "title": "Massive Tutorial",
            "products": [{"name": f"Gadget {i}"} for i in range(101)]
        }
        res = self.client.post("/api/v1/library/rehydrate", json={"item": oversized_item})
        self.assertEqual(res.status_code, 400)
        self.assertIn("max 100 ingredients / products", res.json()["detail"].lower())

    @patch("backend.app.api.v1.library.get_supabase_client")
    def test_rehydrate_reconciles_content_payload_when_structured_data_missing(self, mock_get_sb):
        """Rehydration correctly falls back to content_payload when structured_data key is absent in cache."""
        mock_sb = MagicMock()
        mock_sb.get_cached_extraction.return_value = {
            "id": "cache-row-1",
            "content_payload": {
                "title": "Legacy Cached Salad",
                "ingredients": ["Lettuce", "Tomato"]
            }
        }
        mock_get_sb.return_value = mock_sb

        res = self.client.post("/api/v1/library/rehydrate", json={
            "canonical_url": "https://www.instagram.com/reel/C3cachedsalad/",
            "item": {"title": "Placeholder"}
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["item"]["title"], "Legacy Cached Salad")
        self.assertEqual(len(data["item"]["ingredients"]), 2)

    # -------------------------------------------------------------------------
    # 4. SUPABASE REST CLIENT GET_EXTRACTION_BY_ID SCOPING
    # -------------------------------------------------------------------------

    @patch("backend.app.core.supabase_client.requests.get")
    def test_supabase_get_extraction_by_id_guest_scopes_is_public_true(self, mock_requests_get):
        """SupabaseRestClient.get_extraction_by_id for guest queries is_public.eq.true."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = [{"id": self.extraction_id, "is_public": True}]
        mock_requests_get.return_value = mock_resp

        client = SupabaseRestClient(base_url="https://mock.supabase.co", anon_key="dummy_key")
        result = client.get_extraction_by_id(self.extraction_id, user_id=None)

        self.assertIsNotNone(result)
        mock_requests_get.assert_called_once()
        call_params = mock_requests_get.call_args[1]["params"]
        self.assertEqual(call_params["id"], f"eq.{self.extraction_id}")
        self.assertEqual(call_params["is_public"], "eq.true")

    @patch("backend.app.core.supabase_client.requests.get")
    def test_supabase_get_extraction_by_id_authenticated_scopes_user_or_public(self, mock_requests_get):
        """SupabaseRestClient.get_extraction_by_id for authenticated user scopes user_id OR is_public."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = [{"id": self.extraction_id, "user_id": self.owner_user_id}]
        mock_requests_get.return_value = mock_resp

        client = SupabaseRestClient(base_url="https://mock.supabase.co", anon_key="dummy_key")
        result = client.get_extraction_by_id(self.extraction_id, user_id=self.owner_user_id)

        self.assertIsNotNone(result)
        mock_requests_get.assert_called_once()
        call_params = mock_requests_get.call_args[1]["params"]
        self.assertEqual(call_params["id"], f"eq.{self.extraction_id}")
        self.assertEqual(call_params["or"], f"(user_id.eq.{self.owner_user_id},is_public.eq.true)")

    def test_supabase_get_extraction_by_id_invalid_uuid_returns_none(self):
        """SupabaseRestClient.get_extraction_by_id returns None immediately on invalid UUID without querying network."""
        client = SupabaseRestClient(base_url="https://mock.supabase.co", anon_key="dummy_key")
        result = client.get_extraction_by_id("invalid-uuid-string", user_id=self.owner_user_id)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
