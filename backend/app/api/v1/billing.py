"""
Billing & Subscription Router (UPA-602 & UPA-603)
==================================================
Endpoints for creating subscription checkout sessions (Razorpay / Stripe)
and querying user subscription status.
"""

import logging
from typing import Optional, Literal
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from backend.app.core.security import get_current_user
from backend.app.services.billing_service import get_billing_service, BillingService
from backend.app.services.quota_service import get_quota_manager, QuotaManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/billing", tags=["Billing & Subscriptions"])


class CheckoutRequest(BaseModel):
    provider: Literal["razorpay", "stripe"] = Field("razorpay", description="Payment gateway provider")
    plan_id: Optional[str] = Field(None, description="Optional custom plan or price ID override")
    success_url: Optional[str] = Field("http://localhost:3000/dashboard", description="Redirect URL after payment")
    cancel_url: Optional[str] = Field("http://localhost:3000/pricing", description="Redirect URL if canceled")


@router.post("/checkout", summary="Create Subscription Checkout Session")
async def create_checkout_session(
    body: CheckoutRequest,
    current_user: dict = Depends(get_current_user),
    billing_service: BillingService = Depends(get_billing_service)
):
    """
    Creates a subscription checkout payload for India (Razorpay) or Global (Stripe).
    Returns provider-specific checkout parameters and session URLs.
    """
    user_id = current_user.get("id", "guest_user")
    
    if body.provider == "razorpay":
        session = billing_service.create_razorpay_subscription(
            user_id=user_id,
            plan_id=body.plan_id
        )
    else:
        session = billing_service.create_stripe_checkout_session(
            user_id=user_id,
            price_id=body.plan_id,
            success_url=body.success_url or "http://localhost:3000/dashboard",
            cancel_url=body.cancel_url or "http://localhost:3000/pricing"
        )

    return {
        "status": "success",
        "checkout_session": session
    }


@router.get("/subscription", summary="Get User Subscription & Quota Status")
async def get_subscription_status(
    current_user: dict = Depends(get_current_user),
    quota_manager: QuotaManager = Depends(get_quota_manager)
):
    """
    Returns active subscription tier, quota limits, current daily usage,
    and upgrade recommendations.
    """
    user_id = current_user.get("id", "guest_user")
    tier = current_user.get("tier", "free")
    is_pro = tier in ["pro", "creator", "business"]

    quota_info = quota_manager.get_quota_status(
        identifier=user_id,
        is_pro=is_pro,
        daily_limit=quota_manager.get_limit_for_tier(tier)
    )

    return {
        "status": "success",
        "user_id": user_id,
        "subscription": {
            "tier": tier,
            "is_pro": is_pro,
            "quota": quota_info
        }
    }
