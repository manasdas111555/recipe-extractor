"""
FastAPI V1 API Router
=====================
Aggregates all version 1 endpoints for Universal Pro AI.
"""

from fastapi import APIRouter
from backend.app.core.config import get_settings

router = APIRouter(prefix="", tags=["v1"])
settings = get_settings()

@router.get("/info", summary="API V1 Information")
async def get_v1_info():
    """Returns overview of version 1 endpoints and supported domains."""
    return {
        "api_version": "v1",
        "service": settings.PROJECT_NAME,
        "supported_domains": [
            "recipe",
            "kitchen_product",
            "tech_diy",
            "fitness_workout",
            "travel_guide",
            "beauty_skincare",
            "finance_business"
        ],
        "endpoints": {
            "auth": f"{settings.API_V1_PREFIX}/auth/me",
            "extract": f"{settings.API_V1_PREFIX}/extract (Queued in UPA-106)",
            "library": f"{settings.API_V1_PREFIX}/library",
            "webhooks": f"{settings.API_V1_PREFIX}/webhooks"
        }
    }

from fastapi import Depends, Body
from pydantic import BaseModel, Field
from typing import Optional
from backend.app.core.security import get_current_user
from backend.app.core.supabase_client import get_supabase_client
from backend.app.api.v1.extract import router as extract_router
from backend.app.api.v1.affiliate import router as affiliate_router
from backend.app.api.v1.webhooks import router as webhooks_router
from backend.app.api.v1.library import router as library_router
from backend.app.api.v1.billing import router as billing_router
from backend.app.api.v1.public_hub import router as public_hub_router
from backend.app.api.v1.telemetry import router as telemetry_router

# Mount Sub-Routers
router.include_router(extract_router)
router.include_router(affiliate_router)
router.include_router(webhooks_router)
router.include_router(library_router)
router.include_router(billing_router)
router.include_router(public_hub_router)
router.include_router(telemetry_router)


class ProfileUpdateRequest(BaseModel):
    custom_amazon_tag: Optional[str] = Field(None, description="Creator's Amazon Associates tag override")
    custom_earnkaro_id: Optional[str] = Field(None, description="Creator's EarnKaro affiliate ID override")


@router.get("/auth/me", summary="Get Current Authenticated or Guest Profile", tags=["Authentication"])
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    """
    Returns the active user profile based on Supabase JWT Bearer token.
    If unauthenticated, returns an anonymous guest session with free tier quota.
    """
    return {
        "status": "success",
        "user": current_user
    }


@router.patch("/auth/profile", summary="Update Creator Affiliate Tags Vault (Sprint 6: UPA-702)", tags=["Authentication"])
async def update_my_profile(
    body: ProfileUpdateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Updates the user's personal Creator Tag Vault (Amazon Associate Tag & EarnKaro ID).
    When sharing extractions, creator tags replace system defaults.
    """
    user_id = current_user.get("id", "guest_user")
    supabase = get_supabase_client()
    success = supabase.update_creator_tags(
        user_id=user_id,
        custom_amazon_tag=body.custom_amazon_tag,
        custom_earnkaro_id=body.custom_earnkaro_id
    )
    
    updated_user = dict(current_user)
    if body.custom_amazon_tag is not None:
        updated_user["custom_amazon_tag"] = body.custom_amazon_tag
    if body.custom_earnkaro_id is not None:
        updated_user["custom_earnkaro_id"] = body.custom_earnkaro_id

    return {
        "status": "success" if success else "error",
        "message": "Creator affiliate tags updated successfully.",
        "user": updated_user
    }


