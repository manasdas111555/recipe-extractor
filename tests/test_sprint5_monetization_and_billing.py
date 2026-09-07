"""
Sprint 5 Automated Test Suite — Monetization, Quotas & Subscriptions
======================================================================
Verifies:
- UPA-601: Redis-backed Tiered Quota Enforcement (Guest, Free, Pro)
- UPA-602: Razorpay UPI AutoPay Subscription Checkout & Webhook Signature Verification
- UPA-603: Stripe Global Subscription Checkout & Webhook Signature Verification
- UPA-303: Outbound Click Telemetry Analytics API Endpoint
"""

import hmac
import hashlib
import json
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.core.config import get_settings
from backend.app.services.quota_service import QuotaManager
from backend.app.services.billing_service import BillingService

client = TestClient(app)
settings = get_settings()


class TestSprint5TieredQuotas:
    """Tests UPA-601 tiered daily quota limits and exhaustion behavior."""

    def test_quota_limits_by_tier(self):
        qm = QuotaManager()
        assert qm.get_limit_for_tier("guest") == 3
        assert qm.get_limit_for_tier("free") == 10
        assert qm.get_limit_for_tier("pro") == 999999

    def test_quota_exhaustion_guest(self):
        qm = QuotaManager()
        user_id = "test_guest_quota_user"
        qm.reset_quota(user_id)

        # Consumes 3 guest extractions
        for i in range(3):
            allowed, usage, remaining = qm.check_and_consume_quota(user_id, daily_limit=3)
            assert allowed is True
            assert usage == i + 1

        # 4th extraction attempt should fail
        allowed, usage, remaining = qm.check_and_consume_quota(user_id, daily_limit=3)
        assert allowed is False
        assert usage == 4
        assert remaining == 0

    def test_quota_exhaustion_free_user(self):
        qm = QuotaManager()
        user_id = "test_free_quota_user"
        qm.reset_quota(user_id)

        # Consumes 10 free user extractions
        for i in range(10):
            allowed, usage, remaining = qm.check_and_consume_quota(user_id, daily_limit=10)
            assert allowed is True

        # 11th extraction attempt should fail
        allowed, usage, remaining = qm.check_and_consume_quota(user_id, daily_limit=10)
        assert allowed is False

    def test_quota_pro_unlimited(self):
        qm = QuotaManager()
        user_id = "test_pro_user"
        allowed, usage, remaining = qm.check_and_consume_quota(user_id, is_pro=True)
        assert allowed is True
        assert remaining == 999999


class TestSprint5RazorpayBilling:
    """Tests UPA-602 Razorpay Subscription creation and webhook signature handling."""

    def test_create_razorpay_subscription(self):
        bs = BillingService()
        sub = bs.create_razorpay_subscription(user_id="user_rzp_123")
        assert sub["status"] == "success"
        assert sub["provider"] == "razorpay"
        assert sub["amount"] == 29900  # ₹299 in paise
        assert sub["currency"] == "INR"
        assert sub["user_id"] == "user_rzp_123"

    def test_razorpay_signature_verification_success_and_failure(self):
        bs = BillingService()
        secret = "test_razorpay_webhook_secret_key"
        payload_bytes = b'{"event": "subscription.activated", "user_id": "user_rzp_123"}'
        
        valid_sig = hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()
        invalid_sig = "invalid_signature_hex"

        assert bs.verify_razorpay_signature(payload_bytes, valid_sig, secret=secret) is True
        assert bs.verify_razorpay_signature(payload_bytes, invalid_sig, secret=secret) is False

    def test_razorpay_webhook_subscription_activated(self):
        secret = settings.RAZORPAY_WEBHOOK_SECRET or "whsec_razorpay_mock_secret"
        payload = {
            "event": "subscription.activated",
            "payload": {
                "subscription": {
                    "entity": {
                        "id": "sub_rzp_test_123",
                        "notes": {"user_id": "user_rzp_activate_456"}
                    }
                }
            }
        }
        body_bytes = json.dumps(payload).encode("utf-8")
        sig = hmac.new(secret.encode("utf-8"), body_bytes, hashlib.sha256).hexdigest()

        response = client.post(
            "/api/v1/webhooks/razorpay",
            content=body_bytes,
            headers={"X-Razorpay-Signature": sig, "Content-Type": "application/json"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["result"]["action"] == "upgraded"
        assert data["result"]["tier"] == "pro"

    def test_razorpay_webhook_subscription_halted(self):
        secret = settings.RAZORPAY_WEBHOOK_SECRET or "whsec_razorpay_mock_secret"
        payload = {
            "event": "subscription.halted",
            "payload": {
                "subscription": {
                    "entity": {
                        "id": "sub_rzp_test_123",
                        "notes": {"user_id": "user_rzp_halt_789"}
                    }
                }
            }
        }
        body_bytes = json.dumps(payload).encode("utf-8")
        sig = hmac.new(secret.encode("utf-8"), body_bytes, hashlib.sha256).hexdigest()

        response = client.post(
            "/api/v1/webhooks/razorpay",
            content=body_bytes,
            headers={"X-Razorpay-Signature": sig, "Content-Type": "application/json"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"]["action"] == "downgraded"
        assert data["result"]["tier"] == "free"

    def test_razorpay_webhook_invalid_signature_returns_401(self):
        response = client.post(
            "/api/v1/webhooks/razorpay",
            content=b'{"event":"test"}',
            headers={"X-Razorpay-Signature": "invalid_sig", "Content-Type": "application/json"}
        )
        assert response.status_code == 401


class TestSprint5StripeBilling:
    """Tests UPA-603 Stripe Subscription creation and webhook signature handling."""

    def test_create_stripe_checkout_session(self):
        bs = BillingService()
        session = bs.create_stripe_checkout_session(user_id="user_stripe_123")
        assert session["status"] == "success"
        assert session["provider"] == "stripe"
        assert session["amount"] == 499  # $4.99 in cents
        assert session["currency"] == "USD"

    def test_stripe_signature_verification_success_and_failure(self):
        bs = BillingService()
        secret = "whsec_stripe_mock_secret_key"
        payload_bytes = b'{"type": "customer.subscription.created"}'
        timestamp = "1700000000"
        
        signed_payload = f"{timestamp}.".encode("utf-8") + payload_bytes
        valid_v1 = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
        
        valid_header = f"t={timestamp},v1={valid_v1}"
        invalid_header = f"t={timestamp},v1=bad_v1_signature"

        assert bs.verify_stripe_signature(payload_bytes, valid_header, secret=secret) is True
        assert bs.verify_stripe_signature(payload_bytes, invalid_header, secret=secret) is False

    def test_stripe_webhook_customer_subscription_created(self):
        secret = settings.STRIPE_WEBHOOK_SECRET or "whsec_stripe_mock_secret"
        payload = {
            "type": "customer.subscription.created",
            "data": {
                "object": {
                    "id": "sub_stripe_test_123",
                    "status": "active",
                    "metadata": {"user_id": "user_stripe_active_123"}
                }
            }
        }
        body_bytes = json.dumps(payload).encode("utf-8")
        timestamp = "1700000000"
        signed_payload = f"{timestamp}.".encode("utf-8") + body_bytes
        v1_sig = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
        sig_header = f"t={timestamp},v1={v1_sig}"

        response = client.post(
            "/api/v1/webhooks/stripe",
            content=body_bytes,
            headers={"Stripe-Signature": sig_header, "Content-Type": "application/json"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["result"]["action"] == "upgraded"
        assert data["result"]["tier"] == "pro"

    def test_stripe_webhook_customer_subscription_deleted(self):
        secret = settings.STRIPE_WEBHOOK_SECRET or "whsec_stripe_mock_secret"
        payload = {
            "type": "customer.subscription.deleted",
            "data": {
                "object": {
                    "id": "sub_stripe_test_123",
                    "status": "canceled",
                    "metadata": {"user_id": "user_stripe_canceled_123"}
                }
            }
        }
        body_bytes = json.dumps(payload).encode("utf-8")
        timestamp = "1700000000"
        signed_payload = f"{timestamp}.".encode("utf-8") + body_bytes
        v1_sig = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
        sig_header = f"t={timestamp},v1={v1_sig}"

        response = client.post(
            "/api/v1/webhooks/stripe",
            content=body_bytes,
            headers={"Stripe-Signature": sig_header, "Content-Type": "application/json"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"]["action"] == "downgraded"
        assert data["result"]["tier"] == "free"

    def test_stripe_webhook_invalid_signature_returns_401(self):
        response = client.post(
            "/api/v1/webhooks/stripe",
            content=b'{"type":"test"}',
            headers={"Stripe-Signature": "t=123,v1=bad_sig", "Content-Type": "application/json"}
        )
        assert response.status_code == 401


class TestSprint5BillingEndpoints:
    """Tests /api/v1/billing endpoints."""

    def test_billing_checkout_razorpay(self):
        response = client.post(
            "/api/v1/billing/checkout",
            json={"provider": "razorpay"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["checkout_session"]["provider"] == "razorpay"
        assert data["checkout_session"]["amount"] == 29900

    def test_billing_checkout_stripe(self):
        response = client.post(
            "/api/v1/billing/checkout",
            json={"provider": "stripe"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["checkout_session"]["provider"] == "stripe"
        assert data["checkout_session"]["amount"] == 499

    def test_billing_subscription_status(self):
        response = client.get("/api/v1/billing/subscription")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "subscription" in data
        assert "quota" in data["subscription"]


class TestSprint5AffiliateAnalytics:
    """Tests UPA-303 /api/v1/affiliate/analytics endpoint."""

    def test_affiliate_analytics_endpoint(self):
        response = client.get("/api/v1/affiliate/analytics")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "analytics" in data
        assert "total_clicks" in data["analytics"]
