"""
Unit Tests for FastAPI Extraction Endpoints (UPA-106 & UPA-107)
==============================================================
Validates:
- TC-API-EXT-01: Malformed and invalid URL rejection (HTTP 422)
- TC-API-EXT-02: Daily quota gating for free-tier users (HTTP 429)
- TC-API-EXT-03: Zero-cost viral cache hit return (HTTP 200)
- TC-API-EXT-04: Asynchronous job enqueue on cache miss (HTTP 202)
- TC-API-EXT-05: Real-time job status polling (HTTP 200)
- TC-API-EXT-06: Non-existent job polling returns HTTP 404
- TC-API-EXT-07: JobManager thread-safe state lifecycle
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.job_manager import get_job_manager
from backend.app.core.security import get_current_user

class TestApiExtraction(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.job_manager = get_job_manager()

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_tc_api_ext_01_invalid_url_rejected(self):
        """TC-API-EXT-01: Malformed URL returns HTTP 422."""
        res = self.client.post("/api/v1/extract", json={"video_url": "ftp://not-supported"})
        self.assertEqual(res.status_code, 422)

        res2 = self.client.post("/api/v1/extract", json={"video_url": "too-short"})
        self.assertEqual(res2.status_code, 422)

    def test_tc_api_ext_02_quota_limit_enforced(self):
        """TC-API-EXT-02: User exceeding daily quota receives HTTP 429."""
        def mock_user_over_quota():
            return {
                "id": "mock-user-1",
                "email": "user@example.com",
                "tier": "free",
                "extractions_today": 5,
                "daily_quota_limit": 5,
                "is_active": True
            }

        app.dependency_overrides[get_current_user] = mock_user_over_quota

        res = self.client.post(
            "/api/v1/extract",
            json={"video_url": "https://www.youtube.com/shorts/DPdivoOcXHM"}
        )
        self.assertEqual(res.status_code, 429)
        self.assertIn("quota limit reached", res.json()["detail"].lower())

    @patch("backend.app.api.v1.extract.get_supabase_client")
    def test_tc_api_ext_03_cache_hit_returns_http_200(self, mock_get_supabase):
        """TC-API-EXT-03: Viral recipe cache hit returns 200 with is_cached=True in 0ms."""
        mock_supabase = MagicMock()
        mock_supabase.get_cached_extraction.return_value = {
            "id": "cached-rec-123",
            "url_hash": "dummyhash",
            "content_payload": {
                "title": "Cached Palak Paneer",
                "domain": "RECIPE",
                "ingredients": ["Paneer", "Palak", "Spices"]
            }
        }
        mock_get_supabase.return_value = mock_supabase

        res = self.client.post(
            "/api/v1/extract",
            json={"video_url": "https://www.youtube.com/shorts/DPdivoOcXHM"}
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["is_cached"])
        self.assertEqual(data["status"], "completed")
        self.assertEqual(data["data"]["title"], "Cached Palak Paneer")

    @patch("backend.app.api.v1.extract.run_extraction_worker_sync")
    @patch("backend.app.api.v1.extract.get_supabase_client")
    def test_tc_api_ext_04_cache_miss_enqueues_job_http_202(self, mock_get_supabase, mock_worker):
        """TC-API-EXT-04: Cache miss enqueues asynchronous job returning HTTP 202."""
        mock_supabase = MagicMock()
        mock_supabase.get_cached_extraction.return_value = None
        mock_get_supabase.return_value = mock_supabase

        res = self.client.post(
            "/api/v1/extract",
            json={"video_url": "https://www.youtube.com/shorts/uxj8ZlWoJzo"}
        )
        self.assertEqual(res.status_code, 202)
        data = res.json()
        self.assertFalse(data["is_cached"])
        self.assertEqual(data["status"], "queued")
        self.assertIn("job_id", data)
        self.assertIn("/api/v1/extract/status/", data["poll_url"])
        mock_worker.assert_called_once()

    def test_tc_api_ext_05_status_polling(self):
        """TC-API-EXT-05: Real-time status polling returns current job state and progress."""
        # Create a job in manager
        job = self.job_manager.create_job(
            job_id="test-poll-job-1",
            video_url="https://www.youtube.com/shorts/uxj8ZlWoJzo",
            url_hash="somehash",
            user_id="guest_test"
        )
        self.job_manager.update_job(
            job_id="test-poll-job-1",
            status="processing",
            stage="multimodal_ai_inference",
            progress_percent=65
        )

        res = self.client.get("/api/v1/extract/status/test-poll-job-1")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["job_id"], "test-poll-job-1")
        self.assertEqual(data["status"], "processing")
        self.assertEqual(data["stage"], "multimodal_ai_inference")
        self.assertEqual(data["progress_percent"], 65)

    def test_tc_api_ext_06_status_not_found(self):
        """TC-API-EXT-06: Unknown job_id returns HTTP 404 Not Found."""
        res = self.client.get("/api/v1/extract/status/non-existent-uuid-999")
        self.assertEqual(res.status_code, 404)

    def test_tc_api_ext_07_job_manager_lifecycle(self):
        """TC-API-EXT-07: Verify in-memory thread-safe state lifecycle transitions."""
        job = self.job_manager.create_job(
            job_id="lifecycle-test-1",
            video_url="https://instagram.com/reel/abc1234/",
            url_hash="hash1234",
            user_id="user_123"
        )
        self.assertEqual(job["status"], "queued")
        self.assertEqual(job["progress_percent"], 5)

        updated = self.job_manager.update_job(
            "lifecycle-test-1",
            status="completed",
            stage="completed",
            progress_percent=100,
            data={"result": "success"}
        )
        self.assertEqual(updated["status"], "completed")
        self.assertEqual(updated["progress_percent"], 100)
        self.assertEqual(updated["data"]["result"], "success")

        # Non-existent update returns None
        self.assertIsNone(self.job_manager.update_job("non-existent", status="completed"))

if __name__ == "__main__":
    unittest.main()
