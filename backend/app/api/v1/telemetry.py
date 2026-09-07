"""
Growth Telemetry & Conversion Funnel Router (Sprint 6: UPA-703)
==============================================================
Ingests and analyzes conversion funnel events:
Video Shared -> Extraction Rendered -> Affiliate Clicked -> Paywall Hit -> Subscription Converted.
"""

import datetime
import logging
from typing import Optional, Dict, Any, Literal
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from backend.app.core.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/telemetry", tags=["Growth Telemetry"])

FunnelEventType = Literal[
    "video_shared",
    "extraction_rendered",
    "affiliate_outbound_clicked",
    "paywall_hit",
    "subscription_converted"
]


class TelemetryEventRequest(BaseModel):
    event_name: FunnelEventType = Field(..., description="Conversion funnel stage event name")
    user_id: Optional[str] = Field(None, description="Active user ID or anonymous session UUID")
    session_id: Optional[str] = Field(None, description="Client session ID")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Metadata (merchant, domain, currency)")


@router.post("/event", summary="Record Product Growth Telemetry Event")
async def record_event(body: TelemetryEventRequest):
    """
    Ingests product usage and growth events asynchronously into telemetry store.
    """
    supabase = get_supabase_client()
    event_payload = {
        "event_name": body.event_name,
        "user_id": body.user_id,
        "session_id": body.session_id,
        "properties": body.properties,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    success = supabase.record_telemetry_event(event_payload)
    if not success:
        logger.warning(f"[Telemetry] Failed to record event {body.event_name}")

    return {
        "status": "success",
        "event": body.event_name
    }


@router.get("/funnel", summary="Get Full Conversion Funnel Metrics")
async def get_conversion_funnel():
    """
    Calculates conversion rates across the 5 core product funnel stages:
    1. Video Shared (Top of funnel)
    2. Extraction Rendered
    3. Affiliate Outbound Clicked (Monetization intent)
    4. Paywall Hit (Quota exhaustion / Pro CTA)
    5. Subscription Converted (SaaS revenue)
    """
    supabase = get_supabase_client()
    metrics = supabase.get_telemetry_funnel()
    return {
        "status": "success",
        "funnel": metrics
    }
