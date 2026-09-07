"""
Sprint 6 Automated Test Suite — SEO Growth Engine, Creator Network & Scale
===========================================================================
Verifies:
- UPA-701: Public Extraction Hub, Google Recipe Schema JSON-LD & Dynamic Sitemap
- UPA-702: Creator Custom Affiliate Tag Vault & Dynamic Injection with Default Fallbacks
- UPA-703: Product Funnel Growth Telemetry Ingestion & Conversion Reporting
"""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.affiliate_engine import AffiliateEngine

client = TestClient(app)


class TestSprint6SEOAndPublicHub:
    """Tests UPA-701 Public Extraction Hub, Schema.org Recipe JSON-LD, and Sitemap."""

    def test_public_extraction_schema_org_recipe_jsonld(self):
        response = client.get("/api/v1/public/extractions/crispy-air-fryer-samosa")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        # Verify Schema.org Recipe JSON-LD compliance
        schema = data["schema_org"]
        assert schema["@context"] == "https://schema.org"
        assert schema["@type"] == "Recipe"
        assert "name" in schema
        assert "prepTime" in schema
        assert "cookTime" in schema
        assert "recipeYield" in schema
        assert isinstance(schema["recipeIngredient"], list)
        assert len(schema["recipeIngredient"]) > 0
        assert isinstance(schema["recipeInstructions"], list)
        assert len(schema["recipeInstructions"]) > 0
        assert schema["recipeInstructions"][0]["@type"] == "HowToStep"

        # Verify OpenGraph metadata
        og = data["opengraph"]
        assert "og:title" in og
        assert "og:description" in og
        assert og["og:type"] == "article"

    def test_public_sitemap_urls(self):
        response = client.get("/api/v1/public/sitemap?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["count"] > 0
        assert "urls" in data
        assert any("crispy-air-fryer-samosa" in item["url"] for item in data["urls"])


class TestSprint6CreatorTagVault:
    """Tests UPA-702 Creator Custom Affiliate Tag Vault & Injection."""

    def test_profile_update_creator_tags(self):
        payload = {
            "custom_amazon_tag": "creatorpro-21",
            "custom_earnkaro_id": "creator_ek_7788"
        }
        response = client.patch("/api/v1/auth/profile", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["user"]["custom_amazon_tag"] == "creatorpro-21"
        assert data["user"]["custom_earnkaro_id"] == "creator_ek_7788"

    def test_creator_tag_affiliate_injection(self):
        ae = AffiliateEngine()
        creator_tags = {
            "amazon_tag": "creatorpro-21",
            "earnkaro_id": "creator_ek_7788"
        }
        product = {"name": "Garam Masala Powder", "quantity": "100", "unit": "g"}
        enriched = ae.enrich_product_links(product, user_affiliate_tags=creator_tags, category="RECIPE")

        # Must use creator custom tags
        assert "tag=creatorpro-21" in enriched["amazon_url"]
        assert "r=creator_ek_7788" in enriched["flipkart_url"]

    def test_default_affiliate_tag_fallback(self):
        ae = AffiliateEngine()
        product = {"name": "Cumin Seeds", "quantity": "200", "unit": "g"}
        # Without custom tags, immutable platform constants must be preserved
        enriched = ae.enrich_product_links(product, user_affiliate_tags=None, category="RECIPE")

        assert "tag=manasdas11155-21" in enriched["amazon_url"]
        assert "r=5608766" in enriched["flipkart_url"]


class TestSprint6GrowthTelemetry:
    """Tests UPA-703 Growth Telemetry & Funnel Reporting."""

    def test_telemetry_event_logging(self):
        payload = {
            "event_name": "video_shared",
            "user_id": "test_user_telemetry",
            "properties": {"platform": "instagram", "domain": "recipe"}
        }
        response = client.post("/api/v1/telemetry/event", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["event"] == "video_shared"

    def test_telemetry_funnel_aggregation(self):
        # Fire events for each stage
        for event_name in [
            "video_shared",
            "extraction_rendered",
            "affiliate_outbound_clicked",
            "paywall_hit",
            "subscription_converted"
        ]:
            client.post("/api/v1/telemetry/event", json={
                "event_name": event_name,
                "user_id": "funnel_test_user"
            })

        response = client.get("/api/v1/telemetry/funnel")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        funnel = data["funnel"]["funnel_counts"]
        assert funnel["video_shared"] >= 1
        assert funnel["extraction_rendered"] >= 1
        assert funnel["subscription_converted"] >= 1
        assert "conversion_rate_percent" in data["funnel"]
