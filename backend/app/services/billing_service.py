"""
Billing & Subscription Management Service
==========================================
UPA-602 & UPA-603: Manages subscription sessions, webhooks, HMAC signature verification,
and tier provisioning for Razorpay (India ₹299/mo) and Stripe (Global $4.99/mo).
"""

import hmac
import hashlib
import logging
import uuid
from typing import Dict, Any, Optional

from backend.app.core.config import get_settings
from backend.app.core.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)


class BillingService:
    """
    Unified Subscription & Payment Engine for Razorpay & Stripe.
    Handles HMAC webhook signature validation and user tier upgrades/downgrades.
    """

    def __init__(self):
        self.settings = get_settings()
        self.supabase = get_supabase_client()

    # =========================================================================
    # RAZORPAY BILLING & WEBHOOKS (UPA-602)
    # =========================================================================

    def create_razorpay_subscription(
        self,
        user_id: str,
        plan_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Creates a Razorpay subscription session payload for India (UPI AutoPay / Cards).
        Default Plan: ₹299/month (29900 paise).
        """
        target_plan = plan_id or self.settings.RAZORPAY_PLAN_PRO_299_INR
        sub_id = f"sub_rzp_{uuid.uuid4().hex[:12]}"
        
        subscription_payload = {
            "status": "success",
            "provider": "razorpay",
            "subscription_id": sub_id,
            "plan_id": target_plan,
            "amount": 29900,  # ₹299 in paise
            "currency": "INR",
            "key_id": self.settings.RAZORPAY_KEY_ID,
            "user_id": user_id,
            "notes": {
                "user_id": user_id,
                "tier": "pro"
            }
        }
        logger.info(f"[BillingService] Created Razorpay subscription {sub_id} for user {user_id}")
        return subscription_payload

    def verify_razorpay_signature(
        self,
        payload_bytes: bytes,
        signature: str,
        secret: Optional[str] = None
    ) -> bool:
        """
        Validates HMAC-SHA256 signature from Razorpay webhook header `X-Razorpay-Signature`.
        """
        webhook_secret = secret or self.settings.RAZORPAY_WEBHOOK_SECRET
        if not webhook_secret or not signature:
            logger.warning("[BillingService] Missing Razorpay webhook secret or signature.")
            return False

        try:
            expected_sig = hmac.new(
                webhook_secret.encode("utf-8"),
                payload_bytes,
                hashlib.sha256
            ).hexdigest()
            return hmac.compare_digest(expected_sig, signature)
        except Exception as e:
            logger.error(f"[BillingService] Error verifying Razorpay signature: {e}")
            return False

    def handle_razorpay_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes Razorpay webhook events and updates user subscription tier in Supabase.
        """
        event_type = payload.get("event", "unknown")
        entity_data = payload.get("payload", {}).get("subscription", {}).get("entity", {})
        if not entity_data:
            entity_data = payload.get("payload", {}).get("payment", {}).get("entity", {})

        notes = entity_data.get("notes", {})
        user_id = notes.get("user_id") or payload.get("user_id")
        sub_id = entity_data.get("id") or entity_data.get("subscription_id")

        if not user_id:
            logger.warning(f"[BillingService] Razorpay event {event_type} received without user_id in notes.")
            return {"status": "ignored", "reason": "missing_user_id"}

        # Upgrade Events
        if event_type in ["subscription.activated", "subscription.charged", "payment.captured"]:
            success = self.supabase.update_user_subscription(
                user_id=user_id,
                tier="pro",
                provider="razorpay",
                subscription_id=sub_id
            )
            logger.info(f"[BillingService] User {user_id} upgraded to PRO tier via Razorpay event {event_type}")
            return {"status": "processed", "action": "upgraded", "tier": "pro", "user_id": user_id, "success": success}

        # Downgrade Events
        elif event_type in ["subscription.halted", "subscription.cancelled", "payment.failed"]:
            success = self.supabase.update_user_subscription(
                user_id=user_id,
                tier="free",
                provider="razorpay",
                subscription_id=sub_id
            )
            logger.info(f"[BillingService] User {user_id} downgraded to FREE tier via Razorpay event {event_type}")
            return {"status": "processed", "action": "downgraded", "tier": "free", "user_id": user_id, "success": success}

        return {"status": "ignored", "event": event_type}

    # =========================================================================
    # STRIPE BILLING & WEBHOOKS (UPA-603)
    # =========================================================================

    def create_stripe_checkout_session(
        self,
        user_id: str,
        price_id: Optional[str] = None,
        success_url: str = "http://localhost:3000/dashboard?session_id={CHECKOUT_SESSION_ID}",
        cancel_url: str = "http://localhost:3000/pricing"
    ) -> Dict[str, Any]:
        """
        Creates a Stripe Checkout Session payload for Global Subscribers ($4.99/mo).
        """
        target_price = price_id or self.settings.STRIPE_PRICE_PRO_499_USD
        session_id = f"cs_test_{uuid.uuid4().hex[:14]}"

        checkout_payload = {
            "status": "success",
            "provider": "stripe",
            "session_id": session_id,
            "checkout_url": f"https://checkout.stripe.com/pay/{session_id}",
            "price_id": target_price,
            "amount": 499,  # $4.99 in cents
            "currency": "USD",
            "user_id": user_id,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "metadata": {
                "user_id": user_id,
                "tier": "pro"
            }
        }
        logger.info(f"[BillingService] Created Stripe checkout session {session_id} for user {user_id}")
        return checkout_payload

    def verify_stripe_signature(
        self,
        payload_bytes: bytes,
        sig_header: str,
        secret: Optional[str] = None
    ) -> bool:
        """
        Validates HMAC-SHA256 signature from Stripe header `Stripe-Signature` (t=timestamp,v1=sig).
        """
        webhook_secret = secret or self.settings.STRIPE_WEBHOOK_SECRET
        if not webhook_secret or not sig_header:
            logger.warning("[BillingService] Missing Stripe webhook secret or Stripe-Signature header.")
            return False

        try:
            # Parse header components t=...,v1=...
            header_items = dict(item.split("=", 1) for item in sig_header.split(",") if "=" in item)
            timestamp = header_items.get("t")
            v1_sig = header_items.get("v1")

            if not timestamp or not v1_sig:
                return False

            signed_payload = f"{timestamp}.".encode("utf-8") + payload_bytes
            expected_sig = hmac.new(
                webhook_secret.encode("utf-8"),
                signed_payload,
                hashlib.sha256
            ).hexdigest()

            return hmac.compare_digest(expected_sig, v1_sig)
        except Exception as e:
            logger.error(f"[BillingService] Error verifying Stripe signature: {e}")
            return False

    def handle_stripe_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes Stripe webhook events (`customer.subscription.*`, `checkout.session.completed`).
        """
        event_type = payload.get("type", "unknown")
        data_obj = payload.get("data", {}).get("object", {})

        metadata = data_obj.get("metadata", {})
        user_id = metadata.get("user_id") or data_obj.get("client_reference_id") or payload.get("user_id")
        sub_id = data_obj.get("subscription") or data_obj.get("id")

        if not user_id:
            logger.warning(f"[BillingService] Stripe event {event_type} received without user_id.")
            return {"status": "ignored", "reason": "missing_user_id"}

        status = data_obj.get("status")

        # Upgrade Events
        if event_type in ["checkout.session.completed", "customer.subscription.created", "customer.subscription.updated"]:
            if status in ["active", "paid", None]:
                success = self.supabase.update_user_subscription(
                    user_id=user_id,
                    tier="pro",
                    provider="stripe",
                    subscription_id=sub_id
                )
                logger.info(f"[BillingService] User {user_id} upgraded to PRO tier via Stripe event {event_type}")
                return {"status": "processed", "action": "upgraded", "tier": "pro", "user_id": user_id, "success": success}

        # Downgrade Events
        if event_type == "customer.subscription.deleted" or status in ["canceled", "unpaid"]:
            success = self.supabase.update_user_subscription(
                user_id=user_id,
                tier="free",
                provider="stripe",
                subscription_id=sub_id
            )
            logger.info(f"[BillingService] User {user_id} downgraded to FREE tier via Stripe event {event_type}")
            return {"status": "processed", "action": "downgraded", "tier": "free", "user_id": user_id, "success": success}

        return {"status": "ignored", "event": event_type}


_billing_service: Optional[BillingService] = None

def get_billing_service() -> BillingService:
    """Returns singleton instance of BillingService."""
    global _billing_service
    if _billing_service is None:
        _billing_service = BillingService()
    return _billing_service
