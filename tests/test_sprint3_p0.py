"""
Unit Tests for Sprint 3 (P0) PO Review Acceptance Tweaks
=========================================================
Tests:
1. Contextual Store Routing (Recipe vs Fashion vs Tech).
2. 1-Click WhatsApp formatting without fashion links on recipes.
3. WhatsApp include_commerce_links toggle.
4. Anonymous IP sliding-window rate limiter (3 req/min).
5. FastAPI /api/v1/extract HTTP 429 enforcement on 4th anonymous request.
"""

import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from gemini_processor import build_product_store_links, parse_extracted_content
from whatsapp_service import generate_whatsapp_deep_link
from backend.app.core.security import check_anonymous_rate_limit, reset_rate_limits_for_testing
from backend.app.main import app

class TestSprint3P0Directives(unittest.TestCase):

    def setUp(self):
        reset_rate_limits_for_testing()

    def tearDown(self):
        reset_rate_limits_for_testing()

    def test_contextual_store_routing_recipe(self):
        """Verify recipes strictly suppress fashion portals and include quick-commerce + grocery."""
        links = build_product_store_links("Garam Masala", category="RECIPE")
        
        # Fashion portals must be suppressed (empty string)
        self.assertEqual(links["myntra_url"], "", "Myntra must not be shown for cooking recipes")
        self.assertEqual(links["meesho_url"], "", "Meesho must not be shown for cooking recipes")
        self.assertEqual(links["ajio_url"], "", "AJIO must not be shown for cooking recipes")
        self.assertEqual(links["nykaa_url"], "", "Nykaa must not be shown for cooking recipes")
        
        # Quick commerce and grocery must be present
        self.assertIn("blinkit.com", links["blinkit_url"])
        self.assertIn("zeptonow.com", links["zepto_url"])
        self.assertIn("swiggy.com/instamart", links["instamart_url"])
        self.assertIn("amazon.in", links["amazon_url"])
        self.assertIn("bigbasket.com", links["bigbasket_url"])

    def test_contextual_store_routing_fashion(self):
        """Verify fashion category includes Myntra, AJIO, and Meesho."""
        links = build_product_store_links("Oversized Linen Shirt", category="BEAUTY_FASHION")
        
        self.assertIn("myntra.com", links["myntra_url"])
        self.assertIn("ajio.com", links["ajio_url"])
        self.assertIn("meesho.com", links["meesho_url"])
        self.assertIn("amazon.in", links["amazon_url"])

    def test_whatsapp_deep_link_recipe_omits_fashion(self):
        """Verify WhatsApp message generated for recipe contains no Myntra or Meesho links."""
        products = [
            {
                "name": "Paneer 200g",
                "price": "₹90",
                "amazon_url": "https://www.amazon.in/s?k=Paneer",
                "blinkit_url": "https://blinkit.com/s/?q=Paneer",
                "myntra_url": "",
                "meesho_url": ""
            }
        ]
        wa_url = generate_whatsapp_deep_link(
            phone_number="+919876543210",
            recipe_txt_path="downloads/Matar_Paneer.txt",
            recipe_content="📋 Summary: Delicious creamy restaurant style matar paneer.",
            category="RECIPE",
            products=products
        )
        
        self.assertNotIn("Myntra", wa_url)
        self.assertNotIn("Meesho", wa_url)
        self.assertIn("Blinkit", wa_url)

    def test_whatsapp_deep_link_include_commerce_toggle(self):
        """Verify setting include_commerce_links=False omits product buy links from WhatsApp message."""
        products = [
            {
                "name": "Paneer 200g",
                "price": "₹90",
                "amazon_url": "https://www.amazon.in/s?k=Paneer",
                "blinkit_url": "https://blinkit.com/s/?q=Paneer"
            }
        ]
        wa_url_off = generate_whatsapp_deep_link(
            phone_number="+919876543210",
            recipe_txt_path="downloads/Matar_Paneer.txt",
            recipe_content="📋 Summary: Quick Paneer.",
            category="RECIPE",
            products=products,
            include_commerce_links=False
        )
        self.assertNotIn("Featured%20Products", wa_url_off)
        self.assertNotIn("amazon.in", wa_url_off)
        self.assertNotIn("blinkit.com", wa_url_off)

    def test_sliding_window_rate_limiter_unit(self):
        """Verify sliding-window rate limiter allows 3 requests and rejects the 4th within 60s."""
        ip = "192.168.1.100"
        self.assertTrue(check_anonymous_rate_limit(ip, max_requests=3, window_seconds=60))
        self.assertTrue(check_anonymous_rate_limit(ip, max_requests=3, window_seconds=60))
        self.assertTrue(check_anonymous_rate_limit(ip, max_requests=3, window_seconds=60))
        # 4th request must be rejected
        self.assertFalse(check_anonymous_rate_limit(ip, max_requests=3, window_seconds=60))

    @patch("backend.app.api.v1.extract.get_supabase_client")
    def test_fastapi_extract_rate_limit_http_429(self, mock_sup):
        """Verify POST /api/v1/extract returns HTTP 429 when anonymous user submits >3 req/min."""
        mock_client = MagicMock()
        mock_client.get_cached_extraction.return_value = {
            "id": "cached-123",
            "content_payload": {"title": "Cached Recipe"}
        }
        mock_sup.return_value = mock_client
        
        client = TestClient(app)
        payload = {"video_url": "https://www.instagram.com/reel/C1234567890/"}

        # 1st request -> 200 (cache hit)
        r1 = client.post("/api/v1/extract", json=payload)
        self.assertIn(r1.status_code, [200, 202])

        # 2nd request -> 200
        r2 = client.post("/api/v1/extract", json=payload)
        self.assertIn(r2.status_code, [200, 202])

        # 3rd request -> 200
        r3 = client.post("/api/v1/extract", json=payload)
        self.assertIn(r3.status_code, [200, 202])

        # 4th request -> 429 Rate limit exceeded
        r4 = client.post("/api/v1/extract", json=payload)
        self.assertEqual(r4.status_code, 429)
        self.assertIn("Rate limit exceeded", r4.json()["detail"])

if __name__ == "__main__":
    unittest.main()
