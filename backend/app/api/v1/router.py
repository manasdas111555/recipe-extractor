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

from fastapi import Depends
from backend.app.core.security import get_current_user
from backend.app.api.v1.extract import router as extract_router
from backend.app.api.v1.affiliate import router as affiliate_router
from backend.app.api.v1.webhooks import router as webhooks_router
from backend.app.api.v1.library import router as library_router

# Mount Sub-Routers
router.include_router(extract_router)
router.include_router(affiliate_router)
router.include_router(webhooks_router)
router.include_router(library_router)

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

