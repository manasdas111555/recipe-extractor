"""
Unit Tests for Software & Digital Tool Filtering in Tutorials
=============================================================
Verifies:
1. Software, AI models, libraries, and plugins are filtered out of [PRODUCTS] for tutorials.
2. Software/AI tools are safely promoted to [RESOURCES & TUTORIALS] as documentation/learning resources.
3. Tutorials with only software tools omit the e-commerce Buy Links section entirely.
4. Physical hardware in tutorials (e.g. Raspberry Pi) retains Amazon/Flipkart links without Quick Commerce/Fashion.
5. WhatsApp deep links for software tutorials omit commercial buy links.
"""

import unittest
from gemini_processor import parse_extracted_content, format_downloadable_txt, build_product_store_links
from whatsapp_service import generate_whatsapp_deep_link
from backend.app.services.affiliate_engine import get_affiliate_engine

class TestTutorialStoreFiltering(unittest.TestCase):

    def test_parse_extracted_content_filters_software_from_products(self):
        """Verify software models, plugins, and libraries are not placed in products with store links."""
        sample_output = """
[CATEGORY]: TUTORIAL
[TITLE]: Claude Code Plugin Installer & AI Model Switching Guide
[SUMMARY]: A step-by-step tutorial on using Claude Code, a plugin installer for AI models.

[RESOURCES & TUTORIALS]:
- RESOURCE: Claude Code Tutorial | PLATFORM: YouTube | SEARCH: Claude Code tutorial
- RESOURCE: Claude-Mem Memory Feature Guide | PLATFORM: Documentation | SEARCH: Claude-Mem persistent context

[PRODUCTS]:
- PRODUCT: Claude Code Plugin Installer | PRICE: N/A (likely free or bundled with Claude AI) | SEARCH: Claude Code plugin installer download
- PRODUCT: GLM-5.0 AI Model (Zhongwen Large Model) | PRICE: N/A (free tier available) | SEARCH: GLM-5.0 AI model integration
- PRODUCT: Gemini AI Model | PRICE: N/A (free tier available) | SEARCH: Gemini AI model Claude Code integration

---
[DETAILS]:
1. Installing Plugins: Open interface.
"""
        meta = parse_extracted_content(sample_output)
        self.assertEqual(meta["category"], "TUTORIAL")
        
        # Products list must be EMPTY because all items are software/AI models
        self.assertEqual(len(meta["products"]), 0, "Software and AI models must not be placed in products list")
        
        # Resources list must have preserved them as learning resources
        resource_names = [r["name"] for r in meta["resources"]]
        self.assertIn("Claude Code Tutorial", resource_names)
        self.assertTrue(any("Gemini AI Model" in n for n in resource_names) or any("Claude Code Plugin Installer" in n for n in resource_names))

    def test_parse_extracted_content_keeps_hardware_in_tutorial(self):
        """Verify genuine physical hardware is retained with e-commerce links, but without Quick-Commerce or Fashion."""
        sample_output = """
[CATEGORY]: TUTORIAL
[TITLE]: Build a Smart Mirror with Raspberry Pi
[SUMMARY]: Tutorial on assembling a smart mirror using Raspberry Pi and a two-way glass.

[RESOURCES & TUTORIALS]:
- RESOURCE: MagicMirror2 Installation | PLATFORM: Documentation | SEARCH: MagicMirror2 setup guide

[PRODUCTS]:
- PRODUCT: Raspberry Pi 5 8GB | PRICE: ₹8,500 | SEARCH: Raspberry Pi 5 8GB board
- PRODUCT: Claude Code Plugin Installer | PRICE: N/A (free) | SEARCH: Claude Code plugin

---
[DETAILS]:
Step 1: Flash Raspberry Pi OS.
"""
        meta = parse_extracted_content(sample_output)
        self.assertEqual(len(meta["products"]), 1, "Only genuine physical hardware should remain")
        
        hardware_item = meta["products"][0]
        self.assertEqual(hardware_item["name"], "Raspberry Pi 5 8GB")
        self.assertIn("amazon.in", hardware_item["amazon_url"])
        
        # Must NOT contain Quick Commerce or Fashion stores
        self.assertEqual(hardware_item["blinkit_url"], "")
        self.assertEqual(hardware_item["zepto_url"], "")
        self.assertEqual(hardware_item["myntra_url"], "")
        self.assertEqual(hardware_item["meesho_url"], "")

    def test_format_downloadable_txt_omits_products_when_empty(self):
        """Verify downloadable .txt file omits Buy Links block when products list is empty."""
        meta = {
            "category": "TUTORIAL",
            "category_name": "Tutorial & How-To Guide",
            "emoji": "💻",
            "title": "Claude Code Guide",
            "summary": "Step-by-step tutorial on AI plugins.",
            "resources": [
                {
                    "name": "Claude Code Tutorial",
                    "platform": "YouTube",
                    "youtube_url": "https://youtube.com/watch?v=123",
                    "google_url": "https://google.com/search?q=claude",
                    "github_url": "https://github.com/search?q=claude"
                }
            ],
            "products": [],
            "details": "Step 1: Run installer."
        }
        txt = format_downloadable_txt(meta)
        self.assertNotIn("Featured Products & 1-Click Buy Links", txt)
        self.assertNotIn("Blinkit", txt)
        self.assertNotIn("Zepto", txt)
        self.assertNotIn("Amazon", txt)
        self.assertIn("Recommended YouTube Tutorials & Learning Links", txt)

    def test_whatsapp_deep_link_tutorial_omits_digital_software_buy_links(self):
        """Verify WhatsApp message generated for a tutorial with software products omits buy links."""
        products = [
            {
                "name": "Claude Code Plugin Installer",
                "price": "N/A (likely free)",
                "amazon_url": "https://www.amazon.in/s?k=Claude+Code",
                "blinkit_url": ""
            }
        ]
        wa_url = generate_whatsapp_deep_link(
            phone_number="+919876543210",
            recipe_txt_path="downloads/Claude_Code.txt",
            recipe_content="📋 Summary: Claude Code Guide.",
            category="TUTORIAL",
            products=products
        )
        self.assertNotIn("Featured%20Products", wa_url)
        self.assertNotIn("amazon.in", wa_url)
        self.assertNotIn("Blinkit", wa_url)

    def test_affiliate_engine_tutorial_routing(self):
        """Verify AffiliateEngine suppresses quick commerce and fashion on tutorials."""
        engine = get_affiliate_engine()
        enriched = engine.enrich_product_links({"name": "Soldering Station 60W"}, category="TUTORIAL")
        self.assertEqual(enriched["blinkit_url"], "")
        self.assertEqual(enriched["zepto_url"], "")
        self.assertEqual(enriched["myntra_url"], "")
        self.assertEqual(enriched["meesho_url"], "")
        self.assertIn("amazon.in", enriched["amazon_url"])
        self.assertIn("flipkart.com", enriched["flipkart_url"])

if __name__ == "__main__":
    unittest.main()
