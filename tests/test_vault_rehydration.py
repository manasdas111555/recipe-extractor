"""
Group E Vault Re-hydration Test Suite
=====================================
Validates Requirement E.2:
When a saved item in vault lacks server-built affiliate URLs, opening it re-hydrates
it via the backend endpoint (/api/v1/library/rehydrate), populating Amazon and quick-commerce buy links.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_vault_rehydrate_endpoint_attaches_affiliate_and_quick_commerce_links():
    # Item without server-built affiliate URLs
    bare_item = {
        "title": "Paneer Butter Masala",
        "classified_domain": "RECIPE",
        "ingredients": [
            "Paneer 200g",
            "Butter 2 tbsp",
            "Garam Masala 1 tsp"
        ]
    }

    response = client.post("/api/v1/library/rehydrate", json={
        "canonical_url": "https://www.instagram.com/reel/C3abc123456/",
        "item": bare_item
    })

    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"
    assert data.get("rehydrated") is True

    rehydrated_item = data.get("item", {})
    ingredients = rehydrated_item.get("ingredients", [])
    assert len(ingredients) == 3

    for ing in ingredients:
        assert "amazon_url" in ing
        assert "tag=manasdas11155-21" in ing["amazon_url"]
        assert "flipkart_url" in ing
        assert "r=5608766" in ing["flipkart_url"]
        assert "blinkit_url" in ing
        assert "zepto_url" in ing
