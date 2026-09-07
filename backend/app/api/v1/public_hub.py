"""
Public Extraction Hub & SEO Schema Engine (Sprint 6: UPA-701)
============================================================
Exposes publicly shared extractions with:
- Google-compliant Schema.org JSON-LD (Recipe, HowTo, Product)
- OpenGraph and Twitter card meta payloads
- Sitemap index generation for zero-CAC organic search traffic
"""

import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from backend.app.core.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/public", tags=["Public Hub & SEO"])


def build_schema_org_recipe(extraction: Dict[str, Any]) -> Dict[str, Any]:
    """
    Constructs Google-compliant Schema.org JSON-LD payload for Recipe and HowTo domains.
    Docs: https://developers.google.com/search/docs/appearance/structured-data/recipe
    """
    content = extraction.get("extracted_content", {})
    title = content.get("title") or extraction.get("title", "Universal AI Recipe")
    summary = content.get("summary") or content.get("description") or f"Learn how to make {title} with exact ingredients and step-by-step instructions."
    
    ingredients = content.get("ingredients", [])
    ingredient_strings: List[str] = []
    for ing in ingredients:
        if isinstance(ing, dict):
            qty = ing.get("quantity", "").strip()
            unit = ing.get("unit", "").strip()
            name = ing.get("name", "").strip()
            ingredient_strings.append(f"{qty} {unit} {name}".strip())
        elif isinstance(ing, str):
            ingredient_strings.append(ing.strip())

    steps = content.get("steps", [])
    recipe_instructions: List[Dict[str, str]] = []
    for idx, st in enumerate(steps, 1):
        text = st if isinstance(st, str) else st.get("instruction", "")
        recipe_instructions.append({
            "@type": "HowToStep",
            "name": f"Step {idx}",
            "text": text,
            "url": f"https://universalpro.ai/r/{extraction.get('slug', extraction.get('id'))}#step-{idx}"
        })

    prep_time = content.get("prep_time_minutes", 10)
    cook_time = content.get("cook_time_minutes", 20)
    servings = content.get("servings", 4)

    return {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": title,
        "description": summary,
        "prepTime": f"PT{prep_time}M",
        "cookTime": f"PT{cook_time}M",
        "totalTime": f"PT{prep_time + cook_time}M",
        "recipeYield": f"{servings} servings",
        "recipeCategory": content.get("category", "Main Course"),
        "recipeIngredient": ingredient_strings,
        "recipeInstructions": recipe_instructions,
        "keywords": f"{title}, cooking, recipe, homemade, {content.get('category', 'food')}",
        "url": f"https://universalpro.ai/r/{extraction.get('slug', extraction.get('id'))}"
    }


@router.get("/extractions/{slug_or_id}", summary="Get Public Extraction with SEO Schema.org JSON-LD")
async def get_public_extraction(slug_or_id: str):
    """
    Fetches a public extraction by URL slug or UUID.
    Generates Google Recipe Schema JSON-LD and OpenGraph metadata for SSR rendering.
    """
    supabase = get_supabase_client()
    extraction = supabase.get_public_extraction_by_slug_or_id(slug_or_id)

    if not extraction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Public extraction '{slug_or_id}' not found or is private."
        )

    schema_org = build_schema_org_recipe(extraction)
    content = extraction.get("extracted_content", {})
    title = content.get("title") or extraction.get("title", "Universal AI Recipe")
    desc = content.get("summary") or f"Quick instructions and ingredients for {title}."

    opengraph = {
        "og:title": f"{title} — Recipe & Instructions | Universal Pro AI",
        "og:description": desc,
        "og:type": "article",
        "og:url": f"https://universalpro.ai/r/{slug_or_id}",
        "twitter:card": "summary_large_image",
        "twitter:title": title,
        "twitter:description": desc
    }

    return {
        "status": "success",
        "extraction": extraction,
        "schema_org": schema_org,
        "opengraph": opengraph
    }


@router.get("/sitemap", summary="List Public Extraction Slugs for Dynamic Sitemap")
async def get_sitemap_urls(limit: int = Query(100, ge=1, le=1000)):
    """
    Returns public extraction slugs, categories, and updated timestamps
    for Next.js dynamic sitemap.ts generation.
    """
    supabase = get_supabase_client()
    slugs = supabase.list_public_extraction_slugs(limit=limit)
    return {
        "status": "success",
        "count": len(slugs),
        "urls": [
            {
                "url": f"https://universalpro.ai/r/{item['slug']}",
                "slug": item["slug"],
                "category": item.get("category", "recipe"),
                "last_modified": item.get("updated_at")
            }
            for item in slugs
        ]
    }
