"""
Sprint 14 Automated Grocery Cart Integration & Quick Commerce Deep Links Test Suite
==================================================================================
Tests AffiliateEngine merchant deep links, strict URL encoding (urllib.parse.quote_plus),
category-conditional storefront display, and owner revenue shield invariants (AGENTS.md Rule 3).
"""

import unittest
import urllib.parse
from pathlib import Path
from backend.app.services.affiliate_engine import get_affiliate_engine, AffiliateEngine


class TestSprint14CommerceIntegration(unittest.TestCase):
    def setUp(self):
        self.engine = get_affiliate_engine()

    def test_owner_amazon_affiliate_tag_shield(self):
        """Verify Amazon URLs enforce immutable owner tag 'manasdas11155-21' and quote_plus encoding."""
        url = self.engine.generate_amazon_url("Organic Paneer & Butter")
        self.assertIn("tag=manasdas11155-21", url)
        self.assertIn("Organic+Paneer+%26+Butter", url)

    def test_owner_earnkaro_affiliate_id_shield(self):
        """Verify EarnKaro URLs enforce immutable owner ID '5608766'."""
        url = self.engine.generate_earnkaro_url("https://www.flipkart.com/search?q=blender")
        self.assertIn("r=5608766", url)
        self.assertIn("earnkaro.com/deals", url)

    def test_quick_commerce_deep_links_encoding(self):
        """Verify Blinkit, Zepto, Swiggy Instamart, and JioMart deep links use quote_plus encoding."""
        item = "Amul Butter 500g & Spices"
        expected_encoded = urllib.parse.quote_plus(item)

        blinkit_url = self.engine.generate_blinkit_url(item)
        self.assertIn("blinkit.com/s/?q=", blinkit_url)
        self.assertIn(expected_encoded, blinkit_url)

        zepto_url = self.engine.generate_zepto_url(item)
        self.assertIn("zeptonow.com/search?q=", zepto_url)
        self.assertIn(expected_encoded, zepto_url)

        instamart_url = self.engine.generate_instamart_url(item)
        self.assertIn("swiggy.com/instamart/search?custom_back=true&query=", instamart_url)
        self.assertIn(expected_encoded, instamart_url)

        jiomart_url = self.engine.generate_jiomart_url(item)
        self.assertIn("jiomart.com/search/", jiomart_url)
        self.assertIn(expected_encoded, jiomart_url)

    def test_category_conditional_storefront_display(self):
        """Verify recipe category populates quick-commerce and suppresses fashion stores."""
        prod = {"name": "Garam Masala 100g"}

        # Recipe Category
        recipe_enriched = self.engine.enrich_product_links(prod, category="RECIPE")
        self.assertTrue(len(recipe_enriched["blinkit_url"]) > 0)
        self.assertTrue(len(recipe_enriched["zepto_url"]) > 0)
        self.assertEqual(recipe_enriched["myntra_url"], "")
        self.assertEqual(recipe_enriched["meesho_url"], "")

        # Fashion Category
        fashion_prod = {"name": "Floral Summer Dress"}
        fashion_enriched = self.engine.enrich_product_links(fashion_prod, category="FASHION")
        self.assertTrue(len(fashion_enriched["myntra_url"]) > 0)
        self.assertTrue(len(fashion_enriched["meesho_url"]) > 0)
        self.assertEqual(fashion_enriched["blinkit_url"], "")
        self.assertEqual(fashion_enriched["zepto_url"], "")

    def test_four_core_document_governance_contract_and_user_manual(self):
        """Verify 4-Core Document Governance Contract in AGENTS.md and User Manual files."""
        root_dir = self.engine.default_amazon_tag and (Path(__file__).resolve().parent.parent)
        agents_file = root_dir / "AGENTS.md"
        manual_file = root_dir / "docs" / "USER_MANUAL.md"
        faq_file = root_dir / "frontend" / "src" / "components" / "FaqSection.tsx"

        self.assertTrue(manual_file.exists(), "Missing docs/USER_MANUAL.md document")
        manual_content = manual_file.read_text(encoding="utf-8")
        self.assertIn("Universal Pro AI — Comprehensive User Manual", manual_content)
        self.assertIn("Hands-Free Cooking Mode", manual_content)
        self.assertIn("10-Minute Quick Commerce", manual_content)

        agents_content = agents_file.read_text(encoding="utf-8")
        self.assertIn("Mandatory 4-Core Document Governance Contract", agents_content)
        self.assertIn("docs/USER_MANUAL.md", agents_content)

        faq_content = faq_file.read_text(encoding="utf-8")
        self.assertIn("user_manual", faq_content)
        self.assertIn("Full User Guide", faq_content)


if __name__ == "__main__":
    unittest.main()
