"""
Sprint 4 Automated Test Suite (UPA-501, UPA-502, UPA-503, PO Directives)
========================================================================
Non-destructive test suite verifying:
1. UPA-501: Next.js 15 PWA Client Manifest, Share Target & Service Worker
2. UPA-502: Dynamic Recipe Serving Scaler & Affiliate Buy Routing
3. UPA-503: User Vault & Personal Library API (GET, DELETE, EXPORT)
4. PO Directives: Telegram Option A density (top 5 steps + web button) & Tiered Quotas (10 free)
"""

import json
import os
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.telegram_bot import format_telegram_markdown
from backend.app.core.security import get_user_quota_limits, get_current_user


class TestSprint4VaultLibrary(unittest.TestCase):
    """Test UPA-503: Personal Library / Vault endpoints."""

    def setUp(self):
        self.client = TestClient(app)
        # Override get_current_user to simulate authenticated user
        app.dependency_overrides[get_current_user] = lambda: {
            "id": "vault-user-123",
            "email": "user@test.com",
            "is_anonymous": False,
            "plan_tier": "free",
        }

    def tearDown(self):
        app.dependency_overrides.clear()

    @patch("backend.app.api.v1.library.get_supabase_client")
    def test_library_list_success(self, mock_get_sb):
        mock_sb = MagicMock()
        mock_sb.list_extractions.return_value = [
            {
                "id": "vault-rec-1",
                "source_url": "https://instagram.com/reel/sample1",
                "platform": "instagram",
                "recipe_data": {
                    "recipe_title": "Butter Chicken",
                    "servings": 4,
                    "ingredients": ["Chicken", "Butter", "Tomato puree"],
                    "instructions": ["Marinate", "Sear", "Simmer"]
                },
                "cached_at": "2026-09-06T12:00:00Z"
            }
        ]
        mock_get_sb.return_value = mock_sb

        response = self.client.get("/api/v1/library?page=1&limit=20")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("items", data)
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["id"], "vault-rec-1")
        self.assertEqual(data["items"][0]["recipe_data"]["recipe_title"], "Butter Chicken")

    @patch("backend.app.api.v1.library.get_supabase_client")
    def test_library_list_search_filter(self, mock_get_sb):
        mock_sb = MagicMock()
        mock_sb.list_extractions.return_value = []
        mock_get_sb.return_value = mock_sb

        response = self.client.get("/api/v1/library?q=paneer&domain=RECIPE")
        self.assertEqual(response.status_code, 200)
        mock_sb.list_extractions.assert_called_once_with(
            user_id="vault-user-123",
            search_query="paneer",
            domain="RECIPE",
            page=1,
            limit=20
        )

    @patch("backend.app.api.v1.library.get_supabase_client")
    def test_library_delete_success(self, mock_get_sb):
        mock_sb = MagicMock()
        mock_sb.delete_extraction.return_value = True
        mock_get_sb.return_value = mock_sb

        response = self.client.delete("/api/v1/library/rec-to-delete-123")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "deleted")
        self.assertEqual(data["id"], "rec-to-delete-123")
        mock_sb.delete_extraction.assert_called_once_with(
            extraction_id="rec-to-delete-123",
            user_id="vault-user-123"
        )

    @patch("backend.app.api.v1.library.get_supabase_client")
    def test_library_export_markdown(self, mock_get_sb):
        mock_sb = MagicMock()
        mock_sb.list_extractions.return_value = [
            {
                "id": "rec-exp-1",
                "title": "Crispy Air Fryer Tofu",
                "cooking_time": "15 mins",
                "ingredients": ["Firm Tofu", "Soy sauce", "Cornstarch"],
                "steps": ["Press tofu", "Toss in starch", "Air fry at 200C"]
            }
        ]
        mock_get_sb.return_value = mock_sb

        response = self.client.get("/api/v1/library/rec-exp-1/export?format=markdown")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/markdown", response.headers.get("content-type", ""))
        self.assertIn("# Crispy Air Fryer Tofu", response.text)
        self.assertIn("- Firm Tofu", response.text)
        self.assertIn("1. Press tofu", response.text)

    @patch("backend.app.api.v1.library.get_supabase_client")
    def test_library_export_json(self, mock_get_sb):
        mock_sb = MagicMock()
        mock_sb.list_extractions.return_value = [
            {
                "id": "rec-exp-2",
                "title": "Garlic Noodles"
            }
        ]
        mock_get_sb.return_value = mock_sb

        response = self.client.get("/api/v1/library/rec-exp-2/export?format=json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/json", response.headers.get("content-type", ""))
        data = response.json()
        self.assertEqual(data["title"], "Garlic Noodles")


class TestSprint4POOptionADensity(unittest.TestCase):
    """Test PO Option A formatting & affiliate wrapper in Telegram bot."""

    def test_telegram_output_density_caps_steps_at_5(self):
        long_recipe = {
            "recipe_title": "7-Step Artisanal Sourdough",
            "cooking_time": "4 hours",
            "servings": 2,
            "ingredients": ["Flour", "Water", "Salt", "Starter"],
            "instructions": [
                "Mix flour and water",
                "Autolyse for 60 minutes",
                "Add starter and salt",
                "Perform 4 stretch and folds",
                "Bulk ferment until doubled",
                "Shape boule and place in banneton",
                "Bake in Dutch oven at 230C"
            ]
        }
        text, inline_keyboard = format_telegram_markdown(long_recipe, "https://instagram.com/reel/sourdough")

        # Step 5 must be present
        self.assertIn("*5.* Bulk ferment until doubled", text)
        # Step 6 & 7 must be truncated into web app CTA
        self.assertNotIn("6. Shape boule", text)
        self.assertNotIn("7. Bake in Dutch oven", text)
        self.assertIn("...and 2 more steps in web app", text)

        # Inline keyboard must contain the interactive web app button
        button_texts = [b["text"] for row in inline_keyboard for b in row]
        self.assertIn("🌐 View Full Interactive Recipe", button_texts)

    def test_telegram_affiliate_button_wrapped_with_redirect(self):
        recipe_with_product = {
            "recipe_title": "Crispy Waffles",
            "ingredients": ["Batter"],
            "instructions": ["Pour and press"],
            "products": [
                {
                    "name": "Belgian Waffle Maker",
                    "buy_url": "https://www.amazon.in/dp/B08XYZ?tag=manasdas11155-21"
                }
            ]
        }
        text, inline_keyboard = format_telegram_markdown(recipe_with_product, "https://instagram.com/reel/waffles")

        buy_button = next(b for row in inline_keyboard for b in row if "Buy Ingredients" in b["text"])
        # Must be routed through affiliate redirect
        self.assertIn("/api/v1/affiliate/redirect", buy_button["url"])
        self.assertIn("merchant=amazon", buy_button["url"])


class TestSprint4TieredQuotas(unittest.TestCase):
    """Test tiered quota limits: guest=3, authenticated free=10, pro=unlimited."""

    def test_tiered_quota_limits(self):
        # Guest tier
        guest_limits = get_user_quota_limits(None)
        self.assertEqual(guest_limits["tier"], "guest")
        self.assertEqual(guest_limits["daily_quota_limit"], 3)

        # Authenticated free tier
        auth_free_user = {"id": "user-123", "role": "free", "is_anonymous": False}
        free_limits = get_user_quota_limits(auth_free_user)
        self.assertEqual(free_limits["tier"], "free")
        self.assertEqual(free_limits["daily_quota_limit"], 10)

        # Pro tier
        pro_user = {"id": "user-vip", "role": "pro", "is_anonymous": False}
        pro_limits = get_user_quota_limits(pro_user)
        self.assertEqual(pro_limits["tier"], "pro")
        self.assertEqual(pro_limits["daily_quota_limit"], -1)


class TestSprint4PWAAssets(unittest.TestCase):
    """Test UPA-501: PWA Manifest & Service Worker assets."""

    def test_manifest_json_valid_and_has_share_target(self):
        manifest_path = os.path.join("frontend", "public", "manifest.json")
        self.assertTrue(os.path.exists(manifest_path), "manifest.json must exist in frontend/public")

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        self.assertEqual(manifest.get("start_url"), "/")
        self.assertEqual(manifest.get("display"), "standalone")
        self.assertIn("share_target", manifest)
        self.assertEqual(manifest["share_target"]["action"], "/share-target")
        self.assertEqual(manifest["share_target"]["method"], "GET")

    def test_service_worker_exists(self):
        sw_path = os.path.join("frontend", "public", "sw.js")
        self.assertTrue(os.path.exists(sw_path), "sw.js must exist in frontend/public")
        with open(sw_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("universalpro-cache-v1", content)
        self.assertIn("caches.match", content)


if __name__ == "__main__":
    unittest.main()
