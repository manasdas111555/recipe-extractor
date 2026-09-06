"""
Affiliate Click-Through & Telemetry Router
==========================================
Handles outbound merchant redirects and logs telemetry events into Supabase.
UPA-303: Outbound Affiliate Click Telemetry & Redirect.
"""

import logging
import datetime
from typing import Optional
from urllib.parse import urlparse
from fastapi import APIRouter, Query, HTTPException, BackgroundTasks, Request
from fastapi.responses import RedirectResponse

from backend.app.core.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/affiliate", tags=["Affiliate & Monetization"])


def _record_affiliate_click(click_payload: dict):
    """Background task to insert click telemetry into Supabase."""
    try:
        supabase = get_supabase_client()
        supabase.log_affiliate_click(click_payload)
    except Exception as e:
        logger.error(f"Failed to record affiliate click: {e}")


@router.get("/redirect", summary="Track and redirect outbound affiliate links")
def affiliate_redirect(
    request: Request,
    url: str = Query(..., description="Target merchant affiliate URL to redirect to"),
    merchant: str = Query("unknown", description="Merchant name (e.g., amazon, flipkart, blinkit, zepto)"),
    item_name: Optional[str] = Query(None, description="Product or ingredient name"),
    extraction_id: Optional[str] = Query(None, description="Associated extraction UUID if available"),
    user_id: Optional[str] = Query(None, description="User UUID if authenticated"),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Validates outbound affiliate link, asynchronously records click telemetry,
    and issues an instant HTTP 307 Temporary Redirect to the merchant store.
    """
    # 1. URL Safety Validation
    parsed = urlparse(url)
    if parsed.scheme not in ["http", "https"] or not parsed.netloc:
        raise HTTPException(
            status_code=400,
            detail="Invalid redirect URL. Must be an absolute HTTP/HTTPS URL."
        )

    # 2. Extract Client Metadata
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")

    # 3. Prepare Telemetry Payload
    click_payload = {
        "merchant": merchant.lower().strip(),
        "item_name": item_name.strip() if item_name else None,
        "target_url": url,
        "extraction_id": extraction_id,
        "user_id": user_id,
        "client_ip": client_ip,
        "user_agent": user_agent[:255] if user_agent else None,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    # 4. Asynchronous Non-Blocking Telemetry Write
    background_tasks.add_task(_record_affiliate_click, click_payload)

    # 5. Instant 307 Redirect (Preserves destination URL & HTTP method)
    return RedirectResponse(url=url, status_code=307)
