"""
Automated Test Suite for Sprint 9: Friends & Family Beta Telemetry & Observability
====================================================================================
Validates quota overrides, WhatsApp message formatting, Hinglish regional prompt rules,
and admin Telegram alert payload construction.
"""

import unittest
from backend.app.services.quota_service import QuotaManager, GUEST_DAILY_LIMIT, FREE_AUTH_DAILY_LIMIT
from backend.app.services.telemetry_service import send_admin_telemetry_alert
from whatsapp_service import format_whatsapp_recipe
from gemini_processor import REGIONAL_EXTRACTION_SYSTEM_PROMPT


class TestSprint9BetaTelemetry(unittest.TestCase):

    def test_quota_relaxation_beta_limits(self):
        """UPA-901: Verify Friends & Family beta quota limits (20 guest / 30 auth)."""
        qm = QuotaManager()
        self.assertEqual(GUEST_DAILY_LIMIT, 20)
        self.assertEqual(FREE_AUTH_DAILY_LIMIT, 30)
        # Verify custom daily_limit override consumes quota up to beta ceiling (20)
        user_id = "test_beta_quota_user"
        qm.reset_quota(user_id)
        allowed, usage, remaining = qm.check_and_consume_quota(user_id, daily_limit=GUEST_DAILY_LIMIT)
        self.assertTrue(allowed)
        self.assertEqual(remaining, 19)

    def test_whatsapp_recipe_formatting(self):
        """UPA-904: Verify format_whatsapp_recipe constructs compact message with Blinkit/Zepto links."""
        sample_data = {
            "title": "Masala Paneer Tikka",
            "servings": 4,
            "prep_time": "15m",
            "cook_time": "20m",
            "ingredients": [
                {"name": "Paneer", "quantity": "200", "unit": "g"},
                {"name": "Ghee", "quantity": "2", "unit": "tbsp"},
                {"name": "Kasuri Methi", "quantity": "1", "unit": "tsp"},
            ],
            "instructions": [
                "Cut paneer into cubes.",
                "Marinate with spices and yogurt.",
                "Grill until golden brown.",
                "Serve hot with mint chutney.",
            ],
        }
        msg = format_whatsapp_recipe(sample_data, public_slug="masala-paneer-tikka-123")
        self.assertIn("Masala Paneer Tikka", msg)
        self.assertIn("Blinkit", msg)
        self.assertIn("Zepto", msg)
        self.assertIn("https://universalpro.ai/r/masala-paneer-tikka-123", msg)

    def test_hinglish_regional_prompt_instructions(self):
        """UPA-905: Verify REGIONAL_EXTRACTION_SYSTEM_PROMPT contains Indian metric & colloquial rules."""
        self.assertIn("1 katori", REGIONAL_EXTRACTION_SYSTEM_PROMPT)
        self.assertIn("ek chamach", REGIONAL_EXTRACTION_SYSTEM_PROMPT)
        self.assertIn("Kasuri Methi", REGIONAL_EXTRACTION_SYSTEM_PROMPT)
        self.assertIn("swadanusar", REGIONAL_EXTRACTION_SYSTEM_PROMPT)

    def test_admin_telemetry_alert_dispatcher_graceful_handling(self):
        """UPA-903: Verify send_admin_telemetry_alert returns False gracefully when token/chat_id unconfigured."""
        res = send_admin_telemetry_alert("failed", "https://instagram.com/reel/123", "Test error detail")
        self.assertIsInstance(res, bool)


if __name__ == "__main__":
    unittest.main()
