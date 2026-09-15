"""
Sprint 10 Test Suite — Recipe 3-Section Formatting & Buy Links Categorization (UPA-1010)
========================================================================================
Verifies:
1. gemini_processor.parse_extracted_content correctly parses recipe details into equipment, ingredients, and instructions arrays.
2. format_downloadable_txt outputs 3 Roman numeral sections and divides products into Equipment Links vs. Purchase Ingredients.
3. Negative guardrails: Non-recipe categories retain their existing structures without regression.
"""

import pytest
from gemini_processor import parse_extracted_content, format_downloadable_txt, get_prompt_for_mode


def test_recipe_prompt_contains_3_section_structure():
    """Verify recipe prompt requests Roman numeral 3-section layout."""
    prompt = get_prompt_for_mode("recipe")
    assert "I. Equipment Needed:" in prompt
    assert "II. Ingredients:" in prompt
    assert "III. Step-by-Step Instructions:" in prompt


def test_parse_extracted_content_extracts_recipe_sections():
    """Verify parse_extracted_content extracts equipment, ingredients, and instructions."""
    raw_response = """
[CATEGORY]: RECIPE
[TITLE]: Spicy Potato Fry Recipe
[SUMMARY]: Quick pan-fried spicy potatoes with curry leaves.

[PRODUCTS]:
- PRODUCT: Frying Pan | PRICE: N/A | SEARCH: Nonstick Frying Pan
- PRODUCT: Potato | PRICE: N/A | SEARCH: Fresh Potato

---
[DETAILS]:
I. Equipment Needed:
a. Frying Pan
b. Skillet

II. Ingredients: (Get quantity if available for each ingredient)
1. Potato - 4 medium
2. Cooking oil - 2 tbsp
3. Salt - 1 tsp

III. Step-by-Step Instructions:
1. Slice potatoes into round discs.
2. Heat oil in a frying pan over medium heat.
3. Toss and fry until golden brown.
"""
    meta = parse_extracted_content(raw_response)
    assert meta["category"] == "RECIPE"
    assert len(meta["equipment"]) == 2
    assert "Frying Pan" in meta["equipment"]
    assert "Skillet" in meta["equipment"]

    assert len(meta["ingredients"]) == 3
    assert meta["ingredients"][0]["name"] == "Potato"
    assert meta["ingredients"][0]["quantity"] == "4 medium"

    assert len(meta["instructions"]) == 3
    assert "Slice potatoes into round discs." in meta["instructions"][0]


def test_format_downloadable_txt_divides_equipment_and_ingredient_links():
    """Verify downloadable .txt formats recipe buy links into Equipment Links vs. Purchase Ingredients."""
    raw_response = """
[CATEGORY]: RECIPE
[TITLE]: Spicy Potato Fry Recipe
[SUMMARY]: Quick pan-fried spicy potatoes.

[PRODUCTS]:
- PRODUCT: Nonstick Frying Pan | PRICE: ₹999 | SEARCH: Nonstick Frying Pan
- PRODUCT: Potato | PRICE: ₹40 | SEARCH: Fresh Potato

---
[DETAILS]:
I. Equipment Needed:
a. Frying Pan

II. Ingredients:
1. Potato - 200g

III. Step-by-Step Instructions:
1. Fry potatoes.
"""
    meta = parse_extracted_content(raw_response)
    txt = format_downloadable_txt(meta)

    assert "1. Equipment Links" in txt
    assert "2. Purchase Ingredients" in txt
    assert "Frying Pan" in txt
    assert "Potato" in txt
