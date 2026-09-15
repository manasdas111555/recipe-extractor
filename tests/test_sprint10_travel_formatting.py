import pytest
import sys
import os

# Add parent directory to path to import gemini_processor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gemini_processor import parse_extracted_content, format_downloadable_txt


def test_travel_itinerary_parsing():
    sample_text = """[CATEGORY]: TRAVEL_GUIDE
[REEL_LANGUAGE]: English
[AUDIO_SONG]: Ocean Waves Varkala

[TITLE]: Varkala 3-Day Itinerary Guide

[SUMMARY]: A comprehensive 3-day travel itinerary for Varkala, Kerala, India featuring beach hopping, cliff cafes, and sunset spots.

[GOOGLE_MAPS_LOCATIONS]:
- Inda Hotel | SEARCH: Inda Hotel Varkala
- Black Sand Beach | SEARCH: Black Sand Beach Varkala

[DETAILS]:
Day 1:
- Activity 1: Fly into Trivandrum, drive 1 hour to Varkala, and check into Inda Hotel | LOCATION: Inda Hotel Varkala | SEARCH: Inda Hotel Varkala
- Activity 2: Visit North Cliff for cafe hopping and sunset view | LOCATION: North Cliff Varkala | SEARCH: North Cliff Varkala

Day 2:
- Activity 1: Enjoy breakfast at Inda Cafe | LOCATION: Inda Cafe Varkala | SEARCH: Inda Cafe Varkala
- Activity 2: Go beach hopping at Black Sand Beach and Odayam Beach | LOCATION: Black Sand Beach Varkala | SEARCH: Black Sand Beach Varkala

[PRODUCTS]:
NONE

[RESOURCES & TUTORIALS]:
NONE
"""

    parsed = parse_extracted_content(sample_text)
    assert parsed["category"] == "TRAVEL_GUIDE"
    assert parsed["title"] == "Varkala 3-Day Itinerary Guide"
    assert "travel_itinerary" in parsed
    
    itinerary = parsed["travel_itinerary"]
    assert len(itinerary) == 2
    assert itinerary[0]["day"] == "Day 1"
    assert len(itinerary[0]["activities"]) == 2
    assert "Trivandrum" in itinerary[0]["activities"][0]["description"]
    assert "Inda+Hotel+Varkala" in itinerary[0]["activities"][0]["maps_url"]
    
    assert itinerary[1]["day"] == "Day 2"
    assert len(itinerary[1]["activities"]) == 2
    assert "Black Sand Beach" in itinerary[1]["activities"][1]["description"]

    # Test downloadable txt formatting
    txt_output = format_downloadable_txt(parsed)
    assert "Day-by-Day Travel Itinerary" in txt_output
    assert "Day 1:" in txt_output
    assert "Activity 1 :" in txt_output
    assert "Google Maps:" in txt_output
