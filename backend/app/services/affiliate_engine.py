"""
Affiliate & Quick-Commerce Monetization Engine (UPA-301 & UPA-302)
==================================================================
Centralizes affiliate link generation and 10-minute quick-commerce deep links.
Supports:
- Amazon Associates tag formatting with URL query encoding
- EarnKaro aggregator wrapping for Flipkart, Meesho, AJIO, Nykaa
- Pro / Creator custom affiliate tag overrides
- 10-minute Quick-Commerce search deep links (Blinkit, Zepto, Swiggy Instamart, JioMart)
"""

import urllib.parse
from typing import Optional, Dict, Any
from backend.app.core.config import get_settings


class AffiliateEngine:
    """Monetization link generator for multi-store e-commerce & quick commerce."""

    def __init__(
        self,
        default_amazon_tag: Optional[str] = None,
        default_earnkaro_id: Optional[str] = None
    ):
        settings = get_settings()
        self.default_amazon_tag = default_amazon_tag or settings.AMAZON_AFFILIATE_TAG
        self.default_earnkaro_id = default_earnkaro_id or settings.EARNKARO_ID

    def generate_amazon_url(self, product_name: str, custom_tag: Optional[str] = None) -> str:
        """Generates Amazon search link with associates affiliate tag."""
        tag = custom_tag or self.default_amazon_tag
        query = urllib.parse.quote_plus(product_name.strip())
        return f"https://www.amazon.in/s?k={query}&tag={tag}"

    def generate_earnkaro_url(self, target_url: str, custom_id: Optional[str] = None) -> str:
        """Wraps target merchant URL inside EarnKaro monetization redirect."""
        ek_id = custom_id or self.default_earnkaro_id
        encoded = urllib.parse.quote_plus(target_url.strip())
        return f"https://earnkaro.com/deals?r={ek_id}&url={encoded}"

    def generate_flipkart_url(self, product_name: str, custom_id: Optional[str] = None) -> str:
        """Generates Flipkart search URL wrapped with EarnKaro redirect."""
        query = urllib.parse.quote_plus(product_name.strip())
        raw_url = f"https://www.flipkart.com/search?q={query}"
        return self.generate_earnkaro_url(raw_url, custom_id=custom_id)

    def generate_meesho_url(self, product_name: str, custom_id: Optional[str] = None) -> str:
        """Generates Meesho search URL wrapped with EarnKaro redirect."""
        query = urllib.parse.quote_plus(product_name.strip())
        raw_url = f"https://www.meesho.com/search?q={query}"
        return self.generate_earnkaro_url(raw_url, custom_id=custom_id)

    def generate_myntra_url(self, product_name: str) -> str:
        """Generates Myntra search URL."""
        query = urllib.parse.quote_plus(product_name.strip())
        return f"https://www.myntra.com/{query}"

    def generate_ajio_url(self, product_name: str, custom_id: Optional[str] = None) -> str:
        """Generates AJIO search URL wrapped with EarnKaro redirect."""
        query = urllib.parse.quote_plus(product_name.strip())
        raw_url = f"https://www.ajio.com/search/?text={query}"
        return self.generate_earnkaro_url(raw_url, custom_id=custom_id)

    def generate_nykaa_url(self, product_name: str, custom_id: Optional[str] = None) -> str:
        """Generates Nykaa search URL wrapped with EarnKaro redirect."""
        query = urllib.parse.quote_plus(product_name.strip())
        raw_url = f"https://www.nykaa.com/search/result/?q={query}"
        return self.generate_earnkaro_url(raw_url, custom_id=custom_id)

    def generate_google_shopping_url(self, product_name: str) -> str:
        """Generates Google Shopping comparative search URL."""
        query = urllib.parse.quote_plus(product_name.strip())
        return f"https://www.google.com/search?tbm=shop&q={query}"

    # --------------------------------------------------------------------------
    # UPA-302: 10-Minute Quick-Commerce Cart Deep Search Links
    # --------------------------------------------------------------------------

    def generate_blinkit_url(self, product_name: str) -> str:
        """Generates Blinkit 10-minute instant delivery search link."""
        query = urllib.parse.quote_plus(product_name.strip())
        return f"https://blinkit.com/s/?q={query}"

    def generate_zepto_url(self, product_name: str) -> str:
        """Generates Zepto 10-minute instant delivery search link."""
        query = urllib.parse.quote_plus(product_name.strip())
        return f"https://www.zeptonow.com/search?q={query}"

    def generate_instamart_url(self, product_name: str) -> str:
        """Generates Swiggy Instamart instant delivery search link."""
        query = urllib.parse.quote_plus(product_name.strip())
        return f"https://www.swiggy.com/instamart/search?custom_back=true&query={query}"

    def generate_jiomart_url(self, product_name: str) -> str:
        """Generates JioMart instant quick delivery search link."""
        query = urllib.parse.quote_plus(product_name.strip())
        return f"https://www.jiomart.com/search/{query}"

    # --------------------------------------------------------------------------
    # Product & Resource Payloads Enrichment
    # --------------------------------------------------------------------------

    def enrich_product_links(
        self,
        product: Dict[str, Any],
        user_affiliate_tags: Optional[Dict[str, str]] = None,
        category: str = "ALL"
    ) -> Dict[str, Any]:
        """
        Enriches a product dictionary with monetized e-commerce and quick-commerce URLs.
        Allows custom affiliate overrides for Pro and Creator tiers.
        Contextually suppresses irrelevant store links (e.g. no Myntra/Meesho on food recipes).
        """
        user_tags = user_affiliate_tags or {}
        custom_amz = user_tags.get("amazon_tag")
        custom_ek = user_tags.get("earnkaro_id")

        name = product.get("name", "Product").strip()
        enriched = dict(product)
        cat_u = (category or "ALL").upper()
        is_recipe = (cat_u != "ALL") and any(c in cat_u for c in ["RECIPE", "COOK", "BAKE", "CULINARY", "FOOD"])
        is_fashion = any(c in cat_u for c in ["BEAUTY_FASHION", "FASHION", "OOTD", "STYLE", "BEAUTY", "APPAREL"])

        enriched["amazon_url"] = self.generate_amazon_url(name, custom_tag=custom_amz)
        enriched["flipkart_url"] = self.generate_flipkart_url(name, custom_id=custom_ek)

        # Contextual Store Allocation (P0 Directive)
        if cat_u == "ALL" or is_fashion or not is_recipe:
            enriched["myntra_url"] = self.generate_myntra_url(name)
            enriched["meesho_url"] = self.generate_meesho_url(name, custom_id=custom_ek)
            enriched["ajio_url"] = self.generate_ajio_url(name, custom_id=custom_ek)
            enriched["nykaa_url"] = self.generate_nykaa_url(name, custom_id=custom_ek)
        else:
            enriched["myntra_url"] = ""
            enriched["meesho_url"] = ""
            enriched["ajio_url"] = ""
            enriched["nykaa_url"] = ""

        enriched["google_shopping_url"] = self.generate_google_shopping_url(name)

        # Quick Commerce links (always populated for instant fulfillment)
        enriched["blinkit_url"] = self.generate_blinkit_url(name)
        enriched["zepto_url"] = self.generate_zepto_url(name)
        enriched["instamart_url"] = self.generate_instamart_url(name)
        enriched["jiomart_url"] = self.generate_jiomart_url(name)
        enriched["bigbasket_url"] = f"https://www.bigbasket.com/ps/?q={urllib.parse.quote_plus(name)}"

        return enriched

    def enrich_resource_links(self, resource: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriches a tutorial / learning resource dictionary with YouTube, GitHub, and Google search queries.
        """
        name = resource.get("name", "Tutorial").strip()
        encoded = urllib.parse.quote_plus(name)
        enriched = dict(resource)
        enriched["youtube_url"] = f"https://www.youtube.com/results?search_query={encoded}+tutorial"
        enriched["google_url"] = f"https://www.google.com/search?q={encoded}+tutorial+guide"
        enriched["github_url"] = f"https://github.com/search?q={encoded}&type=repositories"
        return enriched


_affiliate_engine: Optional[AffiliateEngine] = None

def get_affiliate_engine() -> AffiliateEngine:
    """Singleton getter for AffiliateEngine."""
    global _affiliate_engine
    if _affiliate_engine is None:
        _affiliate_engine = AffiliateEngine()
    return _affiliate_engine
