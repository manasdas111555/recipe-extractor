import unittest
import os
import sys
import urllib.parse
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from downloader import detect_platform
from gemini_processor import parse_extracted_content, extract_apt_recipe_title
from whatsapp_service import (
    format_phone_number,
    get_recipe_display_name,
    get_category_header,
    generate_whatsapp_deep_link,
    dispatch_whatsapp
)

class TestPlatformDetection(unittest.TestCase):
    def test_instagram_reel_detection(self):
        urls = [
            "https://www.instagram.com/reel/Dc2q674MDEh/?utm_source=ig_web_copy_link",
            "https://instagram.com/reel/C2b7x/",
            "https://www.INSTAGRAM.COM/p/C3kL9/"
        ]
        for url in urls:
            self.assertEqual(detect_platform(url), "Instagram Reel")

    def test_youtube_shorts_detection(self):
        urls = [
            "https://www.youtube.com/shorts/dQw4w9WgXcQ",
            "https://youtube.com/shorts/abc123xyz?feature=share",
            "https://youtu.be/dQw4w9WgXcQ"
        ]
        for url in urls:
            self.assertEqual(detect_platform(url), "YouTube Short")

    def test_youtube_video_detection(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.assertEqual(detect_platform(url), "YouTube Video")

    def test_tiktok_detection(self):
        url = "https://www.tiktok.com/@user/video/7123456789"
        self.assertEqual(detect_platform(url), "TikTok")

    def test_generic_web_video(self):
        url = "https://example.com/videos/sample.mp4"
        self.assertEqual(detect_platform(url), "Web Video")


class TestGeminiProcessor(unittest.TestCase):
    def test_extract_recipe_title_sanitization(self):
        raw = "Title: Best Butter Chicken Under ₹500! *Must Try*"
        clean = extract_apt_recipe_title(raw)
        # Should sanitize ₹ to Rs_ and strip special characters
        self.assertNotIn("₹", clean)
        self.assertIn("Rs_", clean)
        self.assertNotIn("*", clean)

    def test_parse_extracted_content_with_products(self):
        sample = """
[CATEGORY]: GENERAL
[TITLE]: 3 Underrated Gadgets Under ₹1000
[SUMMARY]: This video presents three highly useful gadgets priced under ₹1000.

[PRODUCTS]:
- PRODUCT: Portronics 65W GaN Charger | PRICE: Under ₹1000 | SEARCH: Portronics 65W GaN Charger
- PRODUCT: Boat Stone 180 Mini Soundbar | PRICE: ₹899 | SEARCH: Boat Stone 180 Mini Soundbar
- PRODUCT: 3-in-1 MagSafe Phone Stand | PRICE: ₹599 | SEARCH: 3-in-1 MagSafe Foldable Desk Stand

---
[DETAILS]:
1. Portronics GaN Charger:
Fast charges laptops and phones.
2. Boat Stone 180:
Punchy bass in mini size.
3. 3-in-1 Stand:
Hands-free MagSafe mounting.
"""
        meta = parse_extracted_content(sample)
        self.assertEqual(meta["category"], "GENERAL")
        self.assertEqual(meta["title"], "3 Underrated Gadgets Under ₹1000")
        self.assertNotIn("₹", meta["clean_filename"])
        self.assertIn("Rs_", meta["clean_filename"])
        self.assertEqual(len(meta["products"]), 3)

        first_prod = meta["products"][0]
        self.assertEqual(first_prod["name"], "Portronics 65W GaN Charger")
        self.assertEqual(first_prod["price"], "Under ₹1000")
        self.assertIn("amazon.in/s?k=", first_prod["amazon_url"])
        self.assertIn("google.com/search?tbm=shop&q=", first_prod["google_shopping_url"])
        self.assertIn("flipkart.com/search?q=", first_prod["flipkart_url"])

    def test_parse_extracted_content_with_affiliate_tags(self):
        sample = """
[CATEGORY]: GENERAL
[TITLE]: 3 Underrated Gadgets
[SUMMARY]: Gadget summary.

[PRODUCTS]:
- PRODUCT: Portronics 65W GaN Charger | PRICE: ₹999 | SEARCH: Portronics 65W GaN Charger
"""
        affiliate_tags = {"amazon": "testtag-21", "flipkart": "testaffid"}
        meta = parse_extracted_content(sample, affiliate_tags=affiliate_tags)
        self.assertEqual(len(meta["products"]), 1)
        prod = meta["products"][0]
        self.assertIn("&tag=testtag-21", prod["amazon_url"])
        self.assertIn("&tag=testtag-21", prod["amazon_global_url"])
        self.assertIn("&affid=testaffid", prod["flipkart_url"])

    def test_parse_extracted_content_no_products(self):
        sample = """
[CATEGORY]: RECIPE
[TITLE]: Classic Italian Pasta Aglio e Olio
[SUMMARY]: A classic pasta with garlic, olive oil, and chili flakes.

[PRODUCTS]:
NONE

---
[DETAILS]:
- Spaghetti: 200g
- Garlic: 4 cloves
- Extra virgin olive oil: 3 tbsp
"""
        meta = parse_extracted_content(sample)
        self.assertEqual(meta["category"], "RECIPE")
        self.assertEqual(len(meta["products"]), 0)



class TestWhatsAppService(unittest.TestCase):
    def test_phone_number_formatting(self):
        self.assertEqual(format_phone_number("+91 98765-43210"), "919876543210")
        self.assertEqual(format_phone_number("  8056804940  "), "8056804940")

    def test_category_headers(self):
        h, icon = get_category_header("Pasta", "RECIPE")
        self.assertIn("recipe", h.lower())
        self.assertEqual(icon, "🍳")

        h, icon = get_category_header("Leg Workout", "WORKOUT")
        self.assertIn("workout", h.lower())
        self.assertEqual(icon, "🏋️")

        h, icon = get_category_header("Docker Setup", "TECH_TUTORIAL")
        self.assertIn("tutorial", h.lower())
        self.assertEqual(icon, "💻")

    def test_generate_whatsapp_deep_link_with_products(self):
        products = [
            {
                "name": "Portronics GaN Charger",
                "price": "₹999",
                "amazon_url": "https://www.amazon.in/s?k=Portronics+GaN+Charger"
            }
        ]
        url = generate_whatsapp_deep_link(
            "918056804940", 
            "C:/downloads/3_Gadgets.txt", 
            "Content details here...", 
            category="GENERAL", 
            products=products
        )
        self.assertTrue(url.startswith("https://api.whatsapp.com/send?phone=918056804940"))
        # Unquote URL to verify contents
        decoded = urllib.parse.unquote(url)
        self.assertIn("Portronics GaN Charger", decoded)
        self.assertIn("https://www.amazon.in/s?k=Portronics+GaN+Charger", decoded)

    def test_dispatch_whatsapp_cli_helper(self):
        success, msg = dispatch_whatsapp("918056804940", "C:/test.txt", "Some content", category="RECIPE")
        self.assertTrue(success)
        self.assertIn("https://api.whatsapp.com/send", msg)


class TestConfigAndGuardrails(unittest.TestCase):
    def test_max_video_duration_constant(self):
        from config import MAX_VIDEO_DURATION
        self.assertEqual(MAX_VIDEO_DURATION, 90)

    def test_affiliate_tags_retrieval(self):
        from config import get_affiliate_tags
        tags = get_affiliate_tags()
        self.assertIsInstance(tags, dict)
        self.assertIn("amazon", tags)
        self.assertIn("flipkart", tags)

    def test_cleanup_old_downloads(self):
        from config import cleanup_old_downloads, get_download_dir
        # Should execute safely without errors
        cleanup_old_downloads(max_age_minutes=60)


if __name__ == "__main__":
    unittest.main()

