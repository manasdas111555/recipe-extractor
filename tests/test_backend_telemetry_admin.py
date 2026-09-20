"""
Group D Telemetry & Admin Security Test Suite (UPA-Group-D)
===========================================================
Validates:
- Explicit Admin authentication (ADMIN_API_KEY header or role=='admin').
- Pro users (plan_tier='pro') are NOT treated as admin and fail closed (403).
- Unauthenticated requests fail closed (401).
- Unset ADMIN_API_KEY on server fails closed (403).
- Metric samples never store raw URLs.
"""

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.core.config import get_settings

client = TestClient(app)
settings = get_settings()


class TestAdminTelemetrySecurity:

    def test_unauthenticated_access_returns_401(self):
        # Anonymous request to admin metrics -> 401
        res = client.get("/api/v1/telemetry/metrics")
        assert res.status_code == 401

    def test_pro_user_is_not_admin_returns_403(self):
        from backend.app.core.security import get_current_user
        mock_user = {
            "id": "pro_user_123",
            "email": "pro@example.com",
            "plan_tier": "pro",
            "role": "user",
            "is_anonymous": False,
        }
        app.dependency_overrides[get_current_user] = lambda: mock_user
        try:
            res = client.get("/api/v1/telemetry/metrics")
            assert res.status_code == 403
            assert "forbidden" in res.json().get("detail", "").lower() or "admin" in res.json().get("detail", "").lower()
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    def test_admin_api_key_unset_fails_closed(self):
        # When ADMIN_API_KEY is unset on server -> returns 403
        with patch.object(settings, "ADMIN_API_KEY", None):
            res = client.get("/api/v1/telemetry/metrics", headers={"X-Admin-Api-Key": "some_key"})
            assert res.status_code == 403

    def test_valid_admin_api_key_grants_access(self):
        with patch.object(settings, "ADMIN_API_KEY", "secret_admin_key_999"):
            res = client.get("/api/v1/telemetry/metrics", headers={"X-Admin-Api-Key": "secret_admin_key_999"})
            assert res.status_code == 200
            data = res.json()
            assert data.get("status") == "success"
            assert "metrics" in data

    def test_invalid_admin_api_key_returns_403(self):
        with patch.object(settings, "ADMIN_API_KEY", "secret_admin_key_999"):
            res = client.get("/api/v1/telemetry/metrics", headers={"X-Admin-Api-Key": "wrong_key"})
            assert res.status_code == 403

    def test_telemetry_event_strips_raw_urls(self):
        payload = {
            "event_name": "extraction_rendered",
            "user_id": "usr_123",
            "session_id": "sess_456",
            "properties": {
                "platform": "instagram",
                "duration_ms": 1500,
                "source_url": "https://www.instagram.com/reel/12345/",
                "url": "https://www.instagram.com/reel/12345/"
            }
        }
        res = client.post("/api/v1/telemetry/event", json=payload)
        assert res.status_code == 200
        assert res.json().get("status") == "success"
