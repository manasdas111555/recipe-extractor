"""
User Library & Vault API Router (UPA-503)
=========================================
Provides authenticated and guest users access to their saved extractions,
search, filtering, and export capabilities.
"""

import logging
import hashlib
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel, Field

from backend.app.core.security import get_current_user
from backend.app.core.supabase_client import get_supabase_client
from backend.app.services.affiliate_engine import get_affiliate_engine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/library", tags=["User Vault & Library"])


class RehydrateRequest(BaseModel):
    extraction_id: Optional[str] = Field(None, description="Vault item extraction UUID")
    canonical_url: Optional[str] = Field(None, description="Original content source URL for cache lookup")
    item: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Saved vault item payload without affiliate links")


from fastapi import APIRouter, Depends, Query, HTTPException, status, Request
from backend.app.core.security import get_current_user, get_client_ip
from backend.app.services.url_validator import (
    validate_social_url,
    generate_stream_token,
)
from backend.app.core.config import get_settings
import time
from collections import defaultdict

_REHYDRATE_IP_TIMESTAMPS = defaultdict(list)

@router.post("/rehydrate", summary="Re-hydrate Vault Item with Monetized Affiliate & Quick-Commerce Links")
async def rehydrate_vault_item(body: RehydrateRequest, request: Request):
    """
    When a saved item in the user's local vault is missing server-built affiliate URLs,
    this endpoint re-hydrates it by checking the server cache by canonical URL SHA-256 key,
    or using the backend AffiliateEngine to attach monetized buy & quick-commerce links.
    Enforces IP rate limiting and shared URL validation without triggering LLM inference.
    """
    client_ip = get_client_ip(request)
    from backend.app.services.quota_service import get_quota_manager
    allowed, count = get_quota_manager().check_generic_rate_limit(f"rehydrate:{client_ip}", limit=30, window_seconds=60)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded for vault item re-hydration (max 30 requests per minute)."
        )

    item_data = dict(body.item or {})

    # Bounded list & payload validation (max 100 ingredients / 100 products)
    raw_ingredients = item_data.get("ingredients") or []
    raw_products = item_data.get("products") or []
    if len(raw_ingredients) > 100 or len(raw_products) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rehydration payload exceeds maximum allowed item count (max 100 ingredients / products)."
        )

    # Maximum raw body size guard
    import json
    try:
        if len(json.dumps(item_data)) > 100_000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rehydration payload size exceeds maximum limit of 100KB."
            )
    except (TypeError, ValueError):
        pass

    supabase = get_supabase_client()
    affiliate_engine = get_affiliate_engine()

    target_url = body.canonical_url or item_data.get("source_url") or item_data.get("url")

    if target_url:
        is_valid, err, host, pinned_ip = validate_social_url(target_url)
        if is_valid:
            url_hash = hashlib.sha256(target_url.strip().encode("utf-8")).hexdigest()
            cached_record = supabase.get_cached_extraction(url_hash)

            if cached_record:
                # Reconcile structured_data vs content_payload
                cached_structured = cached_record.get("structured_data") or cached_record.get("content_payload")
                if cached_structured and isinstance(cached_structured, dict):
                    item_data = dict(cached_structured)
                if "source_url" not in item_data:
                    item_data["source_url"] = target_url

    # Mint fresh signed stream token for media playback
    settings = get_settings()
    ext_id = body.extraction_id or item_data.get("id") or "rehydrated_item"
    secret = settings.SECRET_KEY
    if secret:
        fresh_stream_token = generate_stream_token(ext_id, secret, media_url=target_url or "")
        item_data["stream_token"] = fresh_stream_token

    domain = item_data.get("classified_domain") or item_data.get("domain") or "RECIPE"
    
    # Re-hydrate products/ingredients with Affiliate Engine links
    ingredients = item_data.get("ingredients") or []
    enriched_ingredients = []
    for ing in ingredients:
        if isinstance(ing, str):
            ing_dict = {"name": ing}
        elif isinstance(ing, dict):
            ing_dict = dict(ing)
        else:
            continue
        
        # Check if affiliate links are missing or incomplete
        if not ing_dict.get("amazon_url") or not ing_dict.get("blinkit_url"):
            ing_dict = affiliate_engine.enrich_product_links(ing_dict, category=domain)
        enriched_ingredients.append(ing_dict)
    
    if enriched_ingredients:
        item_data["ingredients"] = enriched_ingredients

    products = item_data.get("products") or []
    enriched_products = []
    for prod in products:
        p_dict = dict(prod) if isinstance(prod, dict) else {"name": str(prod)}
        if not p_dict.get("amazon_url"):
            p_dict = affiliate_engine.enrich_product_links(p_dict, category=domain)
        enriched_products.append(p_dict)

    if enriched_products:
        item_data["products"] = enriched_products

    return {
        "status": "success",
        "rehydrated": True,
        "item": item_data
    }


@router.get("", summary="Get Paginated User Extractions & Vault")
async def get_user_library(
    q: Optional[str] = Query(None, description="Search keyword in URL or transcript"),
    domain: Optional[str] = Query(None, description="Filter by domain (recipe, tech_tutorial, etc.)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    """
    Returns user's saved extractions with search and category filtering.
    If anonymous guest, returns public viral cache items.
    """
    supabase = get_supabase_client()
    user_id = current_user.get("id") if not current_user.get("is_anonymous") else None

    items = supabase.list_extractions(
        user_id=user_id,
        search_query=q,
        domain=domain,
        page=page,
        limit=limit
    )

    return {
        "status": "success",
        "page": page,
        "limit": limit,
        "count": len(items),
        "is_anonymous": current_user.get("is_anonymous", True),
        "items": items
    }


@router.delete("/{extraction_id}", summary="Delete an Extraction from Vault")
async def delete_vault_item(
    extraction_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Deletes an extraction from the user's personal library."""
    if current_user.get("is_anonymous"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to modify personal library."
        )

    supabase = get_supabase_client()
    success = supabase.delete_extraction(
        extraction_id=extraction_id,
        user_id=current_user["id"]
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not delete extraction or item not found."
        )

    return {"status": "deleted", "id": extraction_id}


@router.get("/{extraction_id}/export", summary="Export Extraction to Markdown or Text")
async def export_vault_item(
    extraction_id: str,
    format: str = Query("markdown", description="Export format: 'markdown', 'txt', or 'json'"),
    current_user: dict = Depends(get_current_user)
):
    """Exports structured extraction into Markdown, plain text, or raw JSON."""
    if current_user.get("is_anonymous"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to export vault items"
        )

    supabase = get_supabase_client()
    item_record = supabase.get_extraction_by_id(
        extraction_id=extraction_id,
        user_id=current_user.get("id")
    )
    if not item_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Extraction '{extraction_id}' not found or access denied."
        )

    # Reconcile structured payload
    structured = (
        item_record.get("structured_data")
        or item_record.get("content_payload")
        or item_record
    )
    if not isinstance(structured, dict):
        structured = item_record

    title = structured.get("title") or structured.get("recipe_title") or item_record.get("title") or "Saved Extraction"
    ingredients = structured.get("ingredients") or []
    steps = structured.get("steps") or structured.get("instructions") or []

    export_payload = {
        "id": extraction_id,
        "title": title,
        "ingredients": ingredients,
        "steps": steps,
        **{k: v for k, v in structured.items() if k not in ("id", "title", "ingredients", "steps")}
    }

    fmt = format.lower()
    if fmt == "json":
        return JSONResponse(content=export_payload)
    elif fmt == "txt":
        step_lines = [str(s) for s in steps] if isinstance(steps, list) else [str(steps)]
        content = f"{title}\n\nSteps:\n" + "\n".join(step_lines)
        return PlainTextResponse(content=content, media_type="text/plain")
    else:
        # Markdown default
        md = f"# {title}\n\n"
        if ingredients and isinstance(ingredients, list):
            md += "## Ingredients\n" + "\n".join(
                f"- {i.get('name') if isinstance(i, dict) else str(i)}" for i in ingredients
            ) + "\n\n"
        if steps and isinstance(steps, list):
            md += "## Steps\n" + "\n".join(f"{idx}. {s}" for idx, s in enumerate(steps, 1)) + "\n"
        return PlainTextResponse(content=md, media_type="text/markdown")
