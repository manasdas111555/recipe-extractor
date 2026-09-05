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
            "extract": f"{settings.API_V1_PREFIX}/extract (Queued in UPA-106)",
            "library": f"{settings.API_V1_PREFIX}/library",
            "webhooks": f"{settings.API_V1_PREFIX}/webhooks"
        }
    }
