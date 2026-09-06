"""
Sprint 3 Automated Test Suite (UPA-303, UPA-401, UPA-402, UPA-601)
===================================================================
Non-destructive test suite verifying:
1. UPA-303: Outbound Affiliate Click Telemetry & HTTP 307 Redirect
2. UPA-401: Telegram Ingestion Bot Webhook & URL Parsing
3. UPA-402: WhatsApp Cloud API Handshake & Message Receiver
4. UPA-601: Redis & In-Memory Dual-Mode Quota Manager Limit Enforcement
"""

import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.telegram_bot import extract_url_from_text, format_telegram_markdown
from backend.app.services.whatsapp_cloud import verify_whatsapp_webhook, extract_whatsapp_message
from backend.app.services.quota_service import QuotaManager


class TestSprint3AffiliateRedirect(unittest.TestCase):
    """Test UPA-303: Outbound affiliate link tracking and 307 redirect."""

    def setUp(self):
        self.client = TestClient(app)

    def test_affiliate_redirect_valid_url(self):
        target_url = "https://www.amazon.in/dp/B08N5WRWNW?tag=manasdas11155-21"
        response = self.client.get(
            f"/api/v1/affiliate/redirect?url={target_url}&merchant=amazon&item_name=Cast+Iron+Skillet",
            follow_redirects=False
        )
        self.assertEqual(response.status_code, 307)
        self.assertEqual(response.headers.get("location"), target_url)

    def test_affiliate_redirect_rejects_unsafe_scheme(self):
        unsafe_url = "javascript:alert(1)"
        response = self.client.get(
            f"/api/v1/affiliate/redirect?url={unsafe_url}&merchant=unknown",
            follow_redirects=False
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid redirect URL", response.json().get("detail", ""))


class TestSprint3TelegramBot(unittest.TestCase):
    """Test UPA-401: Telegram Ingestion Bot URL extraction and webhook controller."""

    def setUp(self):
        self.client = TestClient(app)

    def test_extract_url_from_text_patterns(self):
        # Instagram
        ig_text = "Hey check this recipe https://www.instagram.com/reel/C1234567890/ it looks amazing!"
        self.assertEqual(extract_url_from_text(ig_text), "https://www.instagram.com/reel/C1234567890/")

        # YouTube Shorts
        yt_text = "Look at this https://youtube.com/shorts/abcdef12345"
        self.assertEqual(extract_url_from_text(yt_text), "https://youtube.com/shorts/abcdef12345")

        # TikTok
        tt_text = "Viral hack: https://www.tiktok.com/@chef/video/1234567890123456789"
        self.assertEqual(extract_url_from_text(tt_text), "https://www.tiktok.com/@chef/video/1234567890123456789")

        # No URL
        plain_text = "Hello how are you today?"
        self.assertIsNone(extract_url_from_text(plain_text))

    @patch("backend.app.services.telegram_bot.send_telegram_message")
    def test_telegram_webhook_start_command(self, mock_send):
        mock_send.return_value = True
        payload = {
            "update_id": 10001,
            "message": {
                "message_id": 1,
                "chat": {"id": 123456},
                "text": "/start"
            }
        }
        response = self.client.post("/api/v1/webhooks/telegram", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "ok")
        self.assertEqual(data.get("result", {}).get("action"), "welcome")
        mock_send.assert_called_once()

    @patch("backend.app.services.telegram_bot.process_telegram_video_extraction")
    def test_telegram_webhook_reel_submission(self, mock_extract):
        payload = {
            "update_id": 10002,
            "message": {
                "message_id": 2,
                "chat": {"id": 987654},
                "text": "Extract this reel: https://www.instagram.com/reel/C9876543210/"
            }
        }
        response = self.client.post("/api/v1/webhooks/telegram", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "ok")
        self.assertEqual(data.get("result", {}).get("status"), "enqueued")


class TestSprint3WhatsAppCloudAPI(unittest.TestCase):
    """Test UPA-402: Meta WhatsApp Cloud API verification and webhook processing."""

    def setUp(self):
        self.client = TestClient(app)

    def test_whatsapp_verification_handshake_success(self):
        response = self.client.get(
            "/api/v1/webhooks/whatsapp?hub.mode=subscribe&hub.verify_token=universal_pro_verify_token&hub.challenge=115599"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "115599")

    def test_whatsapp_verification_handshake_failure(self):
        response = self.client.get(
            "/api/v1/webhooks/whatsapp?hub.mode=subscribe&hub.verify_token=wrong_token&hub.challenge=115599"
        )
        self.assertEqual(response.status_code, 403)

    @patch("backend.app.services.whatsapp_cloud.send_whatsapp_cloud_message")
    def test_whatsapp_incoming_welcome_message(self, mock_send):
        mock_send.return_value = True
        payload = {
            "object": "whatsapp_business_account",
            "entry": [{
                "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                "changes": [{
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {"display_phone_number": "12345", "phone_number_id": "67890"},
                        "messages": [{
                            "from": "919876543210",
                            "id": "wamid.HBgL...==",
                            "timestamp": "1725000000",
                            "text": {"body": "Hi there!"},
                            "type": "text"
                        }]
                    },
                    "field": "messages"
                }]
            }]
        }
        response = self.client.post("/api/v1/webhooks/whatsapp", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "received")
        self.assertEqual(data.get("result", {}).get("action"), "welcome_sent")


class TestSprint3QuotaManager(unittest.TestCase):
    """Test UPA-601: Redis & In-memory dual-mode quota limit enforcement."""

    def setUp(self):
        self.quota_mgr = QuotaManager()
        # Force in-memory fallback for isolated testing
        self.quota_mgr._redis_client = None
        self.quota_mgr._redis_checked = True

    def test_in_memory_quota_exhaustion(self):
        test_id = "test_user_quota_999"
        self.quota_mgr.reset_quota(test_id)

        # 1st request -> allowed (remaining: 2)
        allowed, usage, rem = self.quota_mgr.check_and_consume_quota(test_id, is_pro=False, daily_limit=3)
        self.assertTrue(allowed)
        self.assertEqual(usage, 1)
        self.assertEqual(rem, 2)

        # 2nd request -> allowed (remaining: 1)
        allowed, usage, rem = self.quota_mgr.check_and_consume_quota(test_id, is_pro=False, daily_limit=3)
        self.assertTrue(allowed)
        self.assertEqual(usage, 2)
        self.assertEqual(rem, 1)

        # 3rd request -> allowed (remaining: 0)
        allowed, usage, rem = self.quota_mgr.check_and_consume_quota(test_id, is_pro=False, daily_limit=3)
        self.assertTrue(allowed)
        self.assertEqual(usage, 3)
        self.assertEqual(rem, 0)

        # 4th request -> blocked (ceiling reached)
        allowed, usage, rem = self.quota_mgr.check_and_consume_quota(test_id, is_pro=False, daily_limit=3)
        self.assertFalse(allowed)
        self.assertEqual(usage, 4)
        self.assertEqual(rem, 0)

    def test_pro_tier_unlimited_quota(self):
        test_id = "test_pro_user_888"
        allowed, usage, rem = self.quota_mgr.check_and_consume_quota(test_id, is_pro=True, daily_limit=3)
        self.assertTrue(allowed)
        self.assertGreater(rem, 1000)

    def test_webhooks_health_endpoint(self):
        client = TestClient(app)
        response = client.get("/api/v1/webhooks/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertIn("telegram", data)
        self.assertIn("whatsapp", data)


if __name__ == "__main__":
    unittest.main()
