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

    def test_parse_extracted_content_tech_tutorial_explicit_resources(self):
        sample = """
[CATEGORY]: TECH_TUTORIAL
[TITLE]: 7-Day AI Engineer Roadmap
[SUMMARY]: A weekly plan to become an AI engineer.

[RESOURCES]:
- RESOURCE: Stanford CS229 Machine Learning | PLATFORM: YouTube | SEARCH: Stanford CS229 Machine Learning Andrew Ng
- RESOURCE: LangChain Crash Course | PLATFORM: YouTube | SEARCH: LangChain for beginners tutorial
- RESOURCE: Build RAG with ChromaDB | PLATFORM: YouTube | SEARCH: RAG tutorial ChromaDB Python

---
[DETAILS]:
Day 1: Foundations.
Day 2: LangChain.
"""
        meta = parse_extracted_content(sample)
        self.assertIn(meta["category"], ["TUTORIAL", "TECH_TUTORIAL"])
        self.assertIn("resources", meta)
        self.assertEqual(len(meta["resources"]), 3)
        res1 = meta["resources"][0]
        self.assertEqual(res1["name"], "Stanford CS229 Machine Learning")
        self.assertIn("youtube.com/results?search_query=", res1["youtube_url"])
        self.assertIn("Stanford+CS229", res1["youtube_url"])
        self.assertIn("google.com/search?q=", res1["google_url"])
        self.assertIn("github.com/search?q=", res1["github_url"])

    def test_parse_extracted_content_tech_tutorial_fallback_roadmap(self):
        # Similar to user's real-world screenshot notes where model didn't output [RESOURCES] block
        sample = """
==================================================
💻 Roadmap to Become an AI Engineer in One Week (Tech Tutorial)
==================================================

📋 Summary:
This video presents a structured 7-day learning schedule to transition into AI engineering.

==================================================
Detailed Steps & Notes:
==================================================

**Step-by-Step Weekly Roadmap:**
* **Monday - LLM Fundamentals:** Study foundational LLM concepts and theory (e.g., Stanford Engineering LLM lectures).
* **Tuesday - LangChain:** Learn the LangChain framework for chaining together prompts, memory, and LLMs.
* **Wednesday - RAG (Retrieval-Augmented Generation):** Master RAG architectures, vector databases, and embeddings.
* **Thursday - AI Agents:** Explore autonomous AI agent frameworks, prompt engineering for agents.
* **Friday - LangGraph:** Deep dive into stateful multi-agent workflows and graph-based agent orchestration.
* **Saturday & Sunday - Hands-On GitHub Projects:** Spend the weekend building open-source AI agent projects.
"""
        meta = parse_extracted_content(sample)
        self.assertIn(meta["category"], ["TUTORIAL", "TECH_TUTORIAL"])
        self.assertIn("resources", meta)
        self.assertGreaterEqual(len(meta["resources"]), 5)
        # Verify first resource captures Stanford / LLM Fundamentals
        first = meta["resources"][0]
        self.assertIn("youtube.com/results?search_query=", first["youtube_url"])
        self.assertTrue(
            "Stanford" in first["name"] or "LLM Fundamentals" in first["name"],
            f"Expected Stanford or LLM Fundamentals in resource name, got: {first['name']}"
        )

    def test_parse_extracted_content_educational_concept(self):
        sample = """
[CATEGORY]: EDUCATIONAL
[TITLE]: How Quantum Computing Actually Works
[SUMMARY]: An academic explainer on qubits, superposition, and quantum entanglement.
"""
        meta = parse_extracted_content(sample)
        self.assertEqual(meta["category"], "EDUCATIONAL")
        self.assertEqual(meta["emoji"], "🎓")
        self.assertEqual(meta["category_name"], "Educational & Concept Explainer")

    def test_parse_extracted_content_tutorial_diy(self):
        sample = """
[CATEGORY]: TUTORIAL
[TITLE]: How to Build a Custom Mechanical Keyboard
[SUMMARY]: Step-by-step soldering, lubing, and assembly guide for custom keyboard builds.
"""
        meta = parse_extracted_content(sample)
        self.assertEqual(meta["category"], "TUTORIAL")
        self.assertEqual(meta["emoji"], "💻")
        self.assertEqual(meta["category_name"], "Tutorial & How-To Guide")

    def test_parse_extracted_content_finance_and_beauty(self):
        sample_fin = """
[CATEGORY]: FINANCE_BUSINESS
[TITLE]: Index Funds vs Dividend Stocks
[SUMMARY]: Comparison of long-term compound growth.
"""
        meta_fin = parse_extracted_content(sample_fin)
        self.assertEqual(meta_fin["category"], "FINANCE_BUSINESS")
        self.assertEqual(meta_fin["emoji"], "💰")

        sample_beauty = """
[CATEGORY]: BEAUTY_FASHION
[TITLE]: 5-Minute Daily Glass Skin Routine
[SUMMARY]: Clean Korean skincare routine.
"""
        meta_beauty = parse_extracted_content(sample_beauty)
        self.assertEqual(meta_beauty["category"], "BEAUTY_FASHION")
        self.assertEqual(meta_beauty["emoji"], "💄")




class TestWhatsAppService(unittest.TestCase):
    def test_phone_number_formatting(self):
        self.assertEqual(format_phone_number("+91 98765-43210"), "919876543210")
        self.assertEqual(format_phone_number("  8056804940  "), "8056804940")

    def test_parse_extracted_content_kitchen_finds_and_fallback_products(self):
        sample = """
[CATEGORY]: KITCHEN_FINDS
[TITLE]: 5 Smart Amazon Kitchen Gadgets
[SUMMARY]: Unboxing essential smart kitchen gadgets found on Amazon.

---
[DETAILS]:
1. **Electric Spice Grinder**:
Effortless push-button pepper and salt grinder.
Price: Under ₹499

2. **Oil Dispenser with Silicone Brush**:
Drizzle or brush cooking oil with zero mess.
Price: ₹299

3. **Multi-Blade Herb Scissors**:
Quickly snip fresh herbs directly into food.
Price: ₹349
"""
        meta = parse_extracted_content(sample)
        self.assertEqual(meta["category"], "KITCHEN_FINDS")
        self.assertEqual(meta["emoji"], "🛍️")
        self.assertEqual(meta["title"], "5 Smart Amazon Kitchen Gadgets")
        self.assertEqual(len(meta["products"]), 3)
        self.assertEqual(meta["products"][0]["name"], "Electric Spice Grinder")
        self.assertIn("amazon.in/s?k=", meta["products"][0]["amazon_url"])
        self.assertIn("flipkart.com/search?q=", meta["products"][0]["flipkart_url"])
        self.assertEqual(meta["products"][1]["name"], "Oil Dispenser with Silicone Brush")

    def test_category_headers(self):
        h, icon = get_category_header("Quantum Physics", "EDUCATIONAL")
        self.assertIn("educational", h.lower())
        self.assertEqual(icon, "🎓")

        h, icon = get_category_header("Docker Setup", "TUTORIAL")
        self.assertIn("tutorial", h.lower())
        self.assertEqual(icon, "💻")

        h, icon = get_category_header("Pasta", "RECIPE")
        self.assertIn("recipe", h.lower())
        self.assertEqual(icon, "🍳")

        h, icon = get_category_header("Smart Chopper", "KITCHEN_FINDS")
        self.assertIn("kitchen", h.lower())
        self.assertEqual(icon, "🛍️")

        h, icon = get_category_header("Amazon Unboxing", "PRODUCT_FINDS")
        self.assertIn("product", h.lower())
        self.assertEqual(icon, "📦")

        h, icon = get_category_header("Leg Workout", "WORKOUT")
        self.assertIn("workout", h.lower())
        self.assertEqual(icon, "🏋️")

        h, icon = get_category_header("Index Funds", "FINANCE_BUSINESS")
        self.assertIn("finance", h.lower())
        self.assertEqual(icon, "💰")

        h, icon = get_category_header("Skincare Routine", "BEAUTY_FASHION")
        self.assertIn("beauty", h.lower())
        self.assertEqual(icon, "💄")

        h, icon = get_category_header("Morning Habits", "LIFE_HACKS")
        self.assertIn("hacks", h.lower())
        self.assertEqual(icon, "💡")


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

    def test_generate_whatsapp_deep_link_with_resources(self):
        resources = [
            {
                "name": "Stanford LLM Fundamentals",
                "platform": "YouTube",
                "youtube_url": "https://www.youtube.com/results?search_query=Stanford+LLM+Fundamentals+tutorial"
            },
            {
                "name": "LangChain Framework",
                "platform": "YouTube",
                "youtube_url": "https://www.youtube.com/results?search_query=LangChain+Framework+tutorial"
            }
        ]
        url = generate_whatsapp_deep_link(
            "918056804940",
            "C:/downloads/Roadmap.txt",
            "Step-by-step roadmap notes...",
            category="TECH_TUTORIAL",
            resources=resources
        )
        self.assertTrue(url.startswith("https://api.whatsapp.com/send?phone=918056804940"))
        decoded = urllib.parse.unquote(url)
        self.assertIn("Recommended YouTube Tutorials", decoded)
        self.assertIn("Stanford LLM Fundamentals", decoded)
        self.assertIn("https://www.youtube.com/results?search_query=Stanford+LLM+Fundamentals+tutorial", decoded)

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


class TestMultiProviderAndMedia(unittest.TestCase):
    def test_ffmpeg_available(self):
        from media_utils import get_ffmpeg_path
        path = get_ffmpeg_path()
        self.assertTrue(bool(path))

    def test_multi_provider_key_getters(self):
        from config import get_mistral_api_key, get_aionlabs_api_key, get_groq_api_key
        # Check getters execute without error
        mistral_k = get_mistral_api_key()
        aion_k = get_aionlabs_api_key()
        groq_k = get_groq_api_key()
        self.assertIsInstance(mistral_k, str)
        self.assertIsInstance(aion_k, str)
        self.assertIsInstance(groq_k, str)

    def test_ai_router_providers_list(self):
        from ai_router import AI_PROVIDERS
        self.assertIn("Google Gemini (Native Video AI)", AI_PROVIDERS)
        self.assertIn("Mistral AI (Vision + Audio Keyframes)", AI_PROVIDERS)
        self.assertIn("Groq (Whisper-v3 + Llama 3.3 70B)", AI_PROVIDERS)
        self.assertIn("Auto-Universal (Gemini with Multi-Model Fallback)", AI_PROVIDERS)


class TestNeuralProgressDeck(unittest.TestCase):
    class DummyPlaceholder:
        def __init__(self):
            self.content = ""
        def html(self, html_str):
            self.content = html_str
        def markdown(self, md_str, **kwargs):
            self.content = md_str

    def test_deck_auto_detect_has_no_shoppable_catalog_by_default(self):
        from ui_components import NeuralProgressDeck
        dummy = self.DummyPlaceholder()
        deck = NeuralProgressDeck(dummy, mode="Auto-Detect (Universal AI)")
        step_ids = [s["id"] for s in deck.steps]
        self.assertNotIn("links", step_ids, "Shoppable Catalog Synthesis should not be visible for generic/educational/recipe videos")
        self.assertIn("dl", step_ids)
        self.assertIn("prep", step_ids)
        self.assertIn("ai", step_ids)
        self.assertIn("dispatch", step_ids)

    def test_deck_product_domain_includes_shoppable_catalog(self):
        from ui_components import NeuralProgressDeck
        dummy = self.DummyPlaceholder()
        deck = NeuralProgressDeck(dummy, mode="🛍️ Kitchen Finds & Home Gadgets")
        step_ids = [s["id"] for s in deck.steps]
        self.assertIn("links", step_ids, "Product domains should include Shoppable Catalog Synthesis")

    def test_deck_dynamically_inserts_shoppable_catalog_when_products_found(self):
        from ui_components import NeuralProgressDeck
        dummy = self.DummyPlaceholder()
        deck = NeuralProgressDeck(dummy, mode="Auto-Detect (Universal AI)")
        self.assertNotIn("links", [s["id"] for s in deck.steps])
        
        # Simulate AI discovering 3 products
        deck.insert_or_update_step(
            step_id="links",
            title="Shoppable Catalog Synthesis",
            desc="Generated 1-click buy tags for 3 products",
            icon="🛍️",
            state="done"
        )
        step_ids = [s["id"] for s in deck.steps]
        self.assertIn("links", step_ids)
        self.assertEqual(deck.steps[-2]["id"], "links", "Links step should be inserted right before dispatch")


if __name__ == "__main__":
    unittest.main()


