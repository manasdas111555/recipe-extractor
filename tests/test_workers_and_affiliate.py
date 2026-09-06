"""
Sprint 2 Unit & Integration Test Suite (UPA-201 to UPA-205, UPA-301, UPA-302)
=============================================================================
Validates:
- Celery worker app configuration, task serialization, and broker reachability
- Worker media downloader with 360p constraints and guaranteed disk cleanup
- Residential proxy rotator and fallback logic
- AffiliateEngine monetization links (Amazon tag, EarnKaro redirect, Pro tag override)
- Quick-commerce 10-minute cart deep links (Blinkit, Zepto, Swiggy Instamart, JioMart)
- FastAPI dual-mode extraction queue dispatcher and polling status
"""

import sys
import os
import unittest
import urllib.parse
from pathlib import Path
from unittest.mock import patch, MagicMock

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.core.config import get_settings
from backend.app.workers.celery_app import celery_app, is_celery_broker_reachable
from backend.app.workers.media_downloader import ProxyRotator, managed_worker_download, MAX_WORKER_DURATION
from backend.app.services.affiliate_engine import get_affiliate_engine, AffiliateEngine
from backend.app.services.job_manager import get_job_manager
from fastapi.testclient import TestClient
from backend.app.main import app


class TestCeleryWorkerConfig(unittest.TestCase):
    """UPA-201: Celery Application and Queue Configuration Tests."""

    def test_celery_task_serialization_json(self):
        """Verify Celery task and result serialization is strictly JSON."""
        self.assertEqual(celery_app.conf.task_serializer, "json")
        self.assertEqual(celery_app.conf.result_serializer, "json")
        self.assertIn("json", celery_app.conf.accept_content)

    def test_celery_execution_time_limits(self):
        """Verify Celery hard execution timeout is 180 seconds."""
        settings = get_settings()
        self.assertEqual(celery_app.conf.task_time_limit, settings.CELERY_TASK_TIMEOUT)
        self.assertEqual(celery_app.conf.task_time_limit, 180)
        self.assertEqual(celery_app.conf.task_soft_time_limit, 165)

    def test_celery_task_tracking_enabled(self):
        """Verify task_track_started is enabled for real-time progress polling."""
        self.assertTrue(celery_app.conf.task_track_started)
        self.assertTrue(celery_app.conf.task_acks_late)

    def test_broker_reachable_check_returns_bool(self):
        """Verify is_celery_broker_reachable gracefully returns boolean without crashing."""
        reachable = is_celery_broker_reachable(timeout_seconds=0.2)
        self.assertIsInstance(reachable, bool)


class TestMediaDownloaderAndProxies(unittest.TestCase):
    """UPA-202 & UPA-203: Worker Media Downloader & Proxy Rotation Tests."""

    def test_max_worker_duration_limit(self):
        """Verify max duration guardrail limit is 90 seconds."""
        self.assertEqual(MAX_WORKER_DURATION, 90)

    def test_proxy_rotator_round_robin(self):
        """Verify ProxyRotator rotates through comma-separated proxies."""
        proxies_str = "http://proxy1:8080, http://proxy2:8080, http://proxy3:8080"
        rotator = ProxyRotator(proxies_str)
        self.assertEqual(len(rotator.proxies), 3)
        self.assertEqual(rotator.get_proxy(), "http://proxy1:8080")
        self.assertEqual(rotator.get_proxy(), "http://proxy2:8080")
        self.assertEqual(rotator.get_proxy(), "http://proxy3:8080")
        self.assertEqual(rotator.get_proxy(), "http://proxy1:8080")  # loops back

    def test_proxy_rotator_empty(self):
        """Verify ProxyRotator returns None when no proxies are configured."""
        rotator = ProxyRotator(None)
        self.assertIsNone(rotator.get_proxy())

    def test_managed_worker_download_cleanup_guarantee(self):
        """Verify managed_worker_download context manager unlinks file upon completion."""
        test_dir = Path(ROOT_DIR) / "downloads"
        test_dir.mkdir(parents=True, exist_ok=True)
        fake_video = test_dir / "test_fake_worker_video.mp4"
        fake_video.write_bytes(b"dummy video data for cleanup test")
        self.assertTrue(fake_video.exists())

        with patch("backend.app.workers.media_downloader.download_worker_media", return_value=(True, str(fake_video))):
            with managed_worker_download("https://instagram.com/reel/dummy123") as (success, fpath):
                self.assertTrue(success)
                self.assertEqual(fpath, str(fake_video))
                self.assertTrue(os.path.exists(fpath))

        # After exiting context manager block, file MUST be unlinked
        self.assertFalse(fake_video.exists(), "Managed worker download failed to delete temp file in finally block!")


class TestAffiliateAndQuickCommerce(unittest.TestCase):
    """UPA-301 & UPA-302: Affiliate Link Engine & Quick-Commerce Deep Search Tests."""

    def setUp(self):
        self.engine = get_affiliate_engine()

    def test_amazon_affiliate_tag_generation(self):
        """Verify Amazon search link contains universal pro tag and URL encoding."""
        url = self.engine.generate_amazon_url("Cold Pressed Olive Oil")
        self.assertIn("amazon.in/s?k=Cold+Pressed+Olive+Oil", url)
        self.assertIn("tag=manasdas11155-21", url)

    def test_amazon_custom_affiliate_override(self):
        """Verify Pro / Creator tier can override default Amazon tag."""
        url = self.engine.generate_amazon_url("Whey Protein Isolate", custom_tag="creatorpro-21")
        self.assertIn("tag=creatorpro-21", url)
        self.assertNotIn("tag=manasdas11155-21", url)

    def test_earnkaro_redirect_wrapping(self):
        """Verify merchant URL is wrapped through EarnKaro with user ID."""
        target = "https://www.flipkart.com/search?q=Air+Fryer"
        ek_url = self.engine.generate_earnkaro_url(target)
        self.assertTrue(ek_url.startswith("https://earnkaro.com/deals?r=5608766&url="))
        decoded = urllib.parse.unquote(ek_url)
        self.assertIn(target, decoded)

    def test_flipkart_and_meesho_generation(self):
        """Verify Flipkart and Meesho URLs are wrapped via EarnKaro."""
        fk_url = self.engine.generate_flipkart_url("Non Stick Frying Pan")
        self.assertIn("earnkaro.com/deals", fk_url)
        self.assertIn("r=5608766", fk_url)

        meesho_url = self.engine.generate_meesho_url("Kitchen Apron")
        self.assertIn("earnkaro.com/deals", meesho_url)
        self.assertIn("r=5608766", meesho_url)

    def test_quick_commerce_10_min_deep_links(self):
        """UPA-302: Verify 10-minute delivery links for Blinkit, Zepto, Instamart, JioMart."""
        query = "Organic Kashmiri Saffron"

        blinkit = self.engine.generate_blinkit_url(query)
        self.assertIn("blinkit.com/s/?q=Organic+Kashmiri+Saffron", blinkit)

        zepto = self.engine.generate_zepto_url(query)
        self.assertIn("zeptonow.com/search?q=Organic+Kashmiri+Saffron", zepto)

        instamart = self.engine.generate_instamart_url(query)
        self.assertIn("swiggy.com/instamart/search?custom_back=true&query=Organic+Kashmiri+Saffron", instamart)

        jiomart = self.engine.generate_jiomart_url(query)
        self.assertIn("jiomart.com/search/Organic+Kashmiri+Saffron", jiomart)

    def test_enrich_product_links_complete_catalog(self):
        """Verify enrich_product_links generates all 7 store links + 4 quick-commerce links."""
        prod = {"name": "Espresso Coffee Machine", "price": "₹4,999"}
        enriched = self.engine.enrich_product_links(prod)

        expected_keys = [
            "amazon_url", "flipkart_url", "myntra_url", "meesho_url",
            "ajio_url", "nykaa_url", "google_shopping_url",
            "blinkit_url", "zepto_url", "instamart_url", "jiomart_url"
        ]
        for key in expected_keys:
            self.assertIn(key, enriched, f"Missing key '{key}' in enriched product links")
            self.assertTrue(enriched[key].startswith("http"), f"Invalid URL for '{key}': {enriched[key]}")

    def test_enrich_resource_links(self):
        """Verify enrich_resource_links generates YouTube, GitHub, and Google search queries."""
        res = {"name": "Docker Containerization Guide", "platform": "YouTube"}
        enriched = self.engine.enrich_resource_links(res)

        self.assertIn("youtube_url", enriched)
        self.assertIn("google_url", enriched)
        self.assertIn("github_url", enriched)
        self.assertIn("youtube.com/results?search_query=Docker+Containerization+Guide", enriched["youtube_url"])
        self.assertIn("github.com/search?q=Docker+Containerization+Guide", enriched["github_url"])


class TestDualModeDispatcherEndpoint(unittest.TestCase):
    """Integration test for FastAPI extraction enqueue & status polling."""

    def setUp(self):
        self.client = TestClient(app)

    def test_enqueue_extraction_guest_accepted(self):
        """Verify valid URL enqueues job with HTTP 202 Accepted and poll_url."""
        response = self.client.post(
            "/api/v1/extract",
            json={"video_url": "https://www.instagram.com/reel/C1234567890/"}
        )
        self.assertEqual(response.status_code, 202)
        body = response.json()
        self.assertIn("job_id", body)
        self.assertEqual(body["status"], "queued")
        self.assertIn("/api/v1/extract/status/", body["poll_url"])

    def test_get_extraction_status_polling(self):
        """Verify status polling retrieves job progress."""
        # First enqueue
        enq_resp = self.client.post(
            "/api/v1/extract",
            json={"video_url": "https://www.youtube.com/shorts/abcdef12345"}
        )
        job_id = enq_resp.json()["job_id"]

        # Then poll status
        status_resp = self.client.get(f"/api/v1/extract/status/{job_id}")
        self.assertEqual(status_resp.status_code, 200)
        status_body = status_resp.json()
        self.assertEqual(status_body["job_id"], job_id)
        self.assertIn(status_body["status"], ["queued", "downloading", "processing", "completed", "failed"])

    def test_get_extraction_status_not_found(self):
        """Verify non-existent job returns HTTP 404."""
        response = self.client.get("/api/v1/extract/status/non-existent-job-uuid-12345")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
