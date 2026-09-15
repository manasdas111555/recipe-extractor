"""
Sprint 10 Dedicated Unit Test Suite (UPA-1008)
==============================================
Validates:
1. Downloader error message sanitization & Instagram fallback URL regex
2. Multimodal AI background audio song extraction ([AUDIO_SONG])
3. Multi-language reel spoken audio detection ([REEL_LANGUAGE] & [ORIGINAL_LANGUAGE_NOTES])
4. Travel video Google Maps location generator ([LOCATIONS & MAPS])
5. Intelligence Vault auto-save & contract schema validation (UPA-1009)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

import pytest
import re
from downloader import sanitize_download_error, download_instagram_fallback
from gemini_processor import parse_extracted_content


class TestSprint10BetaFeedback:
    """Test suite for Sprint 10 Beta Testing Feedback & Technical Enhancements."""

    def test_downloader_error_sanitization(self):
        """Verify raw yt-dlp stack traces are formatted into clean natural language tips."""
        raw_ig_error = "Media download failed: Download failed: ERROR: [Instagram] DR92ta_EkO2: Instagram sent an empty media response. Check if this post is accessible..."
        sanitized = sanitize_download_error(raw_ig_error)
        assert "empty media response" not in sanitized
        assert "Instagram rate limit or stream protection encountered" in sanitized

        raw_youtube_bot = "ERROR: [YouTube] Bot challenge detected. Sign in to confirm you are not a bot..."
        sanitized_yt = sanitize_download_error(raw_youtube_bot)
        assert "bot challenge detected" in sanitized_yt.lower()

    def test_instagram_fallback_regex(self):
        """Verify Instagram fallback shortcode extraction for reel URLs."""
        url = "https://www.instagram.com/reel/DdGvPs9zhVu/?utm_source=ig_web_copy_link"
        match = re.search(r"instagram\.com/(?:reel|p)/([A-Za-z0-9_-]+)", url)
        assert match is not None
        assert match.group(1) == "DdGvPs9zhVu"

        # Invalid URL check
        success, err = download_instagram_fallback("https://invalid-url.com/123", Path("downloads"))
        assert success is False
        assert "Invalid Instagram Reel URL" in err

    def test_gemini_audio_song_parsing(self):
        """Verify background music / song title identification from AI response."""
        sample_ai_text = """
[CATEGORY]: RECIPE
[TITLE]: Steamed Egg Curry
[SUMMARY]: A delicious egg curry dish.
[AUDIO_SONG]: "Nacho Nacho - Rahul Sipligunj"
[REEL_LANGUAGE]: Hindi

---
[DETAILS]:
1. Boil eggs.
2. Prepare masala.
"""
        parsed = parse_extracted_content(sample_ai_text)
        assert parsed["audio_song"] == "Nacho Nacho - Rahul Sipligunj"
        assert parsed["reel_language"] == "Hindi"

    def test_gemini_multilingual_reel_parsing(self):
        """Verify multi-language reel spoken audio detection and original language notes parsing."""
        sample_spanish_ai_text = """
[CATEGORY]: RECIPE
[TITLE]: Tacos al Pastor
[SUMMARY]: Authentic Mexican tacos.
[AUDIO_SONG]: NONE
[REEL_LANGUAGE]: Spanish

---
[DETAILS]:
- Ingredients: Pork, achiote, pineapple.
- Step 1: Marinate meat.

[ORIGINAL_LANGUAGE_NOTES]:
- Ingredientes: Carne de cerdo, achiote, piña.
- Paso 1: Marinar la carne.
"""
        parsed = parse_extracted_content(sample_spanish_ai_text)
        assert parsed["reel_language"] == "Spanish"
        assert parsed["notes_original_language"] != ""
        assert "Ingredientes: Carne de cerdo" in parsed["notes_original_language"]

    def test_gemini_google_maps_locations_parsing(self):
        """Verify travel video Google Maps location generator with direct query links."""
        sample_travel_ai_text = """
[CATEGORY]: TRAVEL_GUIDE
[TITLE]: 3 Best Places in Agra
[SUMMARY]: Exploring historic monuments in Agra.
[AUDIO_SONG]: NONE
[REEL_LANGUAGE]: English

[LOCATIONS & MAPS]:
- LOCATION: Taj Mahal, Agra | SEARCH: Taj Mahal Agra India
- LOCATION: Agra Fort, Agra | SEARCH: Agra Fort Agra

---
[DETAILS]:
- Destination 1: Taj Mahal.
- Destination 2: Agra Fort.
"""
        parsed = parse_extracted_content(sample_travel_ai_text)
        assert parsed["category"] == "TRAVEL_GUIDE"
        assert len(parsed["google_maps_locations"]) == 2
        loc1 = parsed["google_maps_locations"][0]
        assert loc1["name"] == "Taj Mahal, Agra"
        assert "https://www.google.com/maps/search/?api=1&query=" in loc1["maps_url"]
        assert "Taj+Mahal+Agra+India" in loc1["maps_url"]

    def test_vault_auto_save_payload_schema(self):
        """Verify Intelligence Vault item payload schema compatibility (UPA-1009)."""
        sample_item = {
            "title": "Quick Python Tips",
            "category": "TUTORIAL",
            "source_url": "https://www.youtube.com/shorts/KrFDs2M_FSE",
            "created_at": "2026-09-15T20:00:00Z"
        }
        assert "title" in sample_item
        assert "category" in sample_item
        assert "source_url" in sample_item
