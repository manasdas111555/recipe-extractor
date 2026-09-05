"""
Unit Tests for FastAPI Gateway Skeleton (UPA-104)
=================================================
Validates:
1. FastAPI app initializes cleanly with OpenAPI docs and CORS middleware.
2. Root endpoint (GET /) returns API metadata.
3. Health check endpoint (GET /health) returns 200 OK and integration status.
4. V1 info endpoint (GET /api/v1/info) returns domain taxonomy.
5. Settings loader properly loads configuration from environment.
"""

import sys
import unittest
from pathlib import Path
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.main import app
from backend.app.core.config import get_settings

class TestApiGateway(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.settings = get_settings()

    def test_settings_loader(self):
        """Verify settings loader reads configuration."""
        self.assertIsNotNone(self.settings.PROJECT_NAME)
        self.assertEqual(self.settings.VERSION, "1.0.0")
        self.assertEqual(self.settings.API_V1_PREFIX, "/api/v1")
        self.assertEqual(self.settings.AMAZON_AFFILIATE_TAG, "manasdas11155-21")
        self.assertEqual(self.settings.EARNKARO_ID, "5608766")

    def test_root_endpoint(self):
        """Verify GET / returns welcome payload and docs link."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("welcome", data["message"].lower())
        self.assertEqual(data["docs"], "/docs")
        self.assertEqual(data["health"], "/health")

    def test_health_check_endpoint(self):
        """Verify GET /health returns 200 OK and healthy status."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["version"], "1.0.0")
        self.assertIn("integrations", data)
        self.assertIn("supabase", data["integrations"])
        self.assertIn("gemini", data["integrations"])

    def test_v1_info_endpoint(self):
        """Verify GET /api/v1/info returns domain taxonomy and route map."""
        response = self.client.get("/api/v1/info")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["api_version"], "v1")
        self.assertIn("recipe", data["supported_domains"])
        self.assertIn("tech_diy", data["supported_domains"])
        self.assertIn("fitness_workout", data["supported_domains"])

    def test_openapi_docs_accessible(self):
        """Verify OpenAPI JSON schema is generated cleanly."""
        response = self.client.get("/openapi.json")
        self.assertEqual(response.status_code, 200)
        schema = response.json()
        self.assertEqual(schema["info"]["title"], self.settings.PROJECT_NAME)
        self.assertIn("/health", schema["paths"])
        self.assertIn("/api/v1/info", schema["paths"])

if __name__ == "__main__":
    unittest.main()
