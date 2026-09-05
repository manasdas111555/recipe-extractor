"""
Unit Tests for Supabase Auth & JWT Middleware (UPA-105)
======================================================
Validates:
1. Anonymous guest access provisions a free trial guest profile.
2. Authenticated requests with Supabase JWT Bearer tokens decode properly.
3. Malformed or invalid JWT tokens return HTTP 401 Unauthorized.
4. Supabase REST client configuration and methods work as expected.
"""

import sys
import time
import unittest
import jwt
from pathlib import Path
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.main import app
from backend.app.core.supabase_client import get_supabase_client

class TestAuthSecurity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.supabase = get_supabase_client()

    def test_anonymous_guest_user(self):
        """Verify unauthenticated requests receive a guest profile with free tier quota."""
        response = self.client.get("/api/v1/auth/me")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        user = data["user"]
        self.assertTrue(user["is_anonymous"])
        self.assertTrue(user["id"].startswith("guest_"))
        self.assertEqual(user["plan_tier"], "free")
        self.assertEqual(user["daily_quota_limit"], 3)

    def test_authenticated_user_with_valid_jwt(self):
        """Verify requests with a valid mock Supabase JWT are authenticated correctly."""
        mock_payload = {
            "sub": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "email": "creator@universalpro.ai",
            "role": "authenticated",
            "exp": int(time.time()) + 3600
        }
        mock_token = jwt.encode(mock_payload, "test-secret", algorithm="HS256")

        headers = {"Authorization": f"Bearer {mock_token}"}
        response = self.client.get("/api/v1/auth/me", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        user = data["user"]
        self.assertFalse(user["is_anonymous"])
        self.assertEqual(user["id"], "a1b2c3d4-e5f6-7890-abcd-ef1234567890")
        self.assertEqual(user["email"], "creator@universalpro.ai")

    def test_malformed_jwt_token_rejected(self):
        """Verify requests with malformed tokens return HTTP 401."""
        headers = {"Authorization": "Bearer not-a-valid-token-string"}
        response = self.client.get("/api/v1/auth/me", headers=headers)
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertIn("detail", data)

    def test_supabase_client_is_configured(self):
        """Verify Supabase client detects credentials loaded from .env."""
        self.assertTrue(self.supabase.is_configured())
        self.assertTrue(self.supabase.base_url.startswith("https://"))
        self.assertGreater(len(self.supabase.anon_key), 20)

if __name__ == "__main__":
    unittest.main()
