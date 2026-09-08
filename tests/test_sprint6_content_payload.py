"""
Sprint 6 Content Payload & Details Verification Test
Verifies that execute_extraction_pipeline constructs content_payload
with details, parsed instructions, and media_url without any NameError or missing re imports.
"""

import unittest
from unittest.mock import MagicMock, patch
from backend.app.workers.tasks import execute_extraction_pipeline


class TestContentPayloadConstruction(unittest.TestCase):
    @patch("backend.app.workers.tasks.managed_worker_download")
    @patch("backend.app.workers.tasks.get_supabase_client")
    @patch("ai_router.route_video_intelligence")
    def test_payload_contains_details_and_parsed_instructions(
        self,
        mock_route_ai,
        mock_get_supabase,
        mock_download
    ):
        mock_download.return_value.__enter__.return_value = (True, "/tmp/test.mp4")
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase

        sample_details = """**Key Features & Specifications:**
- **Display:** 27-inch 4K UHD.
- **Refresh Rate:** 144Hz switches to 288Hz.
"""
        mock_meta = {
            "title": "MSI Monitor Review",
            "category": "PRODUCT_FINDS",
            "category_name": "Product Unboxing & Finds",
            "summary": "Dual mode monitor review.",
            "details": sample_details,
            "products": [],
            "resources": [],
            "timings": {}
        }
        mock_route_ai.return_value = (
            True,
            "/tmp/test.txt",
            "Full extracted text",
            "/tmp/test.mp4",
            mock_meta
        )

        res = execute_extraction_pipeline(
            job_id="test-job-123",
            video_url="https://www.instagram.com/reel/Dcxq0A2lgug/",
            url_hash="test-hash-123",
            user_id="user-1"
        )

        self.assertEqual(res["status"], "completed")
        data = res["data"]
        self.assertEqual(data["title"], "MSI Monitor Review")
        self.assertIn("details", data)
        self.assertEqual(data["details"], sample_details)
        self.assertIn("instructions", data)
        self.assertTrue(len(data["instructions"]) > 0)
        self.assertEqual(data["media_url"], "https://www.instagram.com/reel/Dcxq0A2lgug/")
        self.assertEqual(data["source_url"], "https://www.instagram.com/reel/Dcxq0A2lgug/")


if __name__ == "__main__":
    unittest.main()
