"""
Unit Tests for Staging Supabase Free-Tier Keep-Alive & Monitoring (UPA-1409)
=============================================================================
Validates:
1. URL validation enforces strict HTTPS and locks to mzpkdmaxsuhwezsooidu.supabase.co.
2. Rejection of Production URL, external hostnames, localhost, and non-HTTPS schemes.
3. Safe API key validation and absence of key exposure in errors/logs.
4. Correct PostgREST read-only query construction: GET /rest/v1/extractions?select=id&limit=1.
5. Correct Staging-only headers: apikey, Authorization Bearer, Accept, User-Agent.
6. Safe handling of successful response with rows and with empty list [].
7. Error handling for HTTP 401, 403, 429, 500, and 503.
8. Exception handling for timeouts, network/connection errors, and malformed JSON.
9. Zero secret leakage: keys and row contents are never printed in logs or results.
10. CLI main() exit codes (0 on success, 1 on validation error, 1 on probe failure).
11. Invariant protection: Production keep-alive files remain 100% unchanged.
12. Workflow YAML schema integrity and secret reference isolation.
"""

import os
import sys
import json
import logging
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import yaml
import requests

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "scripts"))

import staging_supabase_keep_alive as keep_alive  # noqa: E402

VALID_STAGING_URL = "https://mzpkdmaxsuhwezsooidu.supabase.co"
VALID_ANON_KEY = "mock_staging_anon_key_for_testing_purposes_only_12345"
PROD_SUPABASE_URL = "https://scrqvbgjybnrvcpxbygf.supabase.co"


class TestStagingSupabaseKeepAlive(unittest.TestCase):
    """Test suite for Staging Supabase Keep-Alive probe."""

    def test_validate_staging_url_success(self):
        """Confirm valid Staging project URL passes and normalizes cleanly."""
        url = keep_alive.validate_staging_url(VALID_STAGING_URL)
        self.assertEqual(url, VALID_STAGING_URL)

        # Trailing slash should be stripped
        url_with_slash = keep_alive.validate_staging_url(f"{VALID_STAGING_URL}/")
        self.assertEqual(url_with_slash, VALID_STAGING_URL)

    def test_validate_staging_url_rejects_empty_or_none(self):
        """Reject empty or None URLs safely with ValueError."""
        for invalid in [None, "", "   ", 123]:
            with self.assertRaises(ValueError) as ctx:
                keep_alive.validate_staging_url(invalid)
            self.assertIn("Missing or empty", str(ctx.exception))

    def test_validate_staging_url_rejects_http_scheme(self):
        """Reject non-HTTPS schemes strictly."""
        with self.assertRaises(ValueError) as ctx:
            keep_alive.validate_staging_url("http://mzpkdmaxsuhwezsooidu.supabase.co")
        self.assertIn("Only HTTPS is permitted", str(ctx.exception))

    def test_validate_staging_url_rejects_production_host(self):
        """Strictly reject the Production Supabase host to prevent cross-environment probes."""
        with self.assertRaises(ValueError) as ctx:
            keep_alive.validate_staging_url(PROD_SUPABASE_URL)
        self.assertIn("Host validation rejected", str(ctx.exception))
        self.assertIn("Cross-environment probes", str(ctx.exception))

    def test_validate_staging_url_rejects_arbitrary_hosts(self):
        """Reject localhost, third-party hosts, or attacker-controlled hosts."""
        for host in [
            "https://localhost:8000",
            "https://127.0.0.1:5432",
            "https://example.com",
            "https://attacker.supabase.co",
        ]:
            with self.assertRaises(ValueError) as ctx:
                keep_alive.validate_staging_url(host)
            self.assertIn("Host validation rejected", str(ctx.exception))

    def test_validate_staging_key_success(self):
        """Valid non-empty token passes validation."""
        key = keep_alive.validate_staging_key(VALID_ANON_KEY)
        self.assertEqual(key, VALID_ANON_KEY)

    def test_validate_staging_key_rejects_empty_or_short(self):
        """Reject missing or suspiciously short keys."""
        for invalid in [None, "", "   "]:
            with self.assertRaises(ValueError) as ctx:
                keep_alive.validate_staging_key(invalid)
            self.assertIn("Missing or empty", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            keep_alive.validate_staging_key("short_token")
        self.assertIn("too short", str(ctx.exception))

    @patch("staging_supabase_keep_alive.requests.get")
    def test_probe_staging_supabase_query_construction_and_headers(self, mock_get):
        """Verify exact endpoint, query parameters, and header structure."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "00000000-0000-0000-0000-000000000001"}]
        mock_get.return_value = mock_response

        result = keep_alive.probe_staging_supabase(VALID_STAGING_URL, VALID_ANON_KEY)

        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 200)

        # Inspect call arguments to requests.get
        mock_get.assert_called_once()
        called_url, called_kwargs = mock_get.call_args

        expected_endpoint = (
            f"{VALID_STAGING_URL}/rest/v1/extractions?select=id&limit=1"
        )
        self.assertEqual(called_url[0], expected_endpoint)

        headers = called_kwargs["headers"]
        self.assertEqual(headers["apikey"], VALID_ANON_KEY)
        self.assertEqual(headers["Authorization"], f"Bearer {VALID_ANON_KEY}")
        self.assertEqual(headers["Accept"], "application/json")
        self.assertIn("UniversalProAI-KeepAlive", headers["User-Agent"])
        self.assertEqual(called_kwargs["timeout"], keep_alive.DEFAULT_TIMEOUT_SECONDS)

    @patch("staging_supabase_keep_alive.requests.get")
    def test_probe_staging_supabase_success_with_row(self, mock_get):
        """A 200 response with rows evaluates to success without logging row fields."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "test-uuid"}]
        mock_get.return_value = mock_response

        result = keep_alive.probe_staging_supabase(VALID_STAGING_URL, VALID_ANON_KEY)

        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 200)
        self.assertEqual(result["row_count"], 1)
        self.assertIsNone(result["error"])
        self.assertGreater(result["duration_ms"], 0.0)

    @patch("staging_supabase_keep_alive.requests.get")
    def test_probe_staging_supabase_success_empty_list(self, mock_get):
        """A 200 response with [] evaluates to success (database activity refreshed)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        result = keep_alive.probe_staging_supabase(VALID_STAGING_URL, VALID_ANON_KEY)

        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 200)
        self.assertEqual(result["row_count"], 0)
        self.assertIsNone(result["error"])

    @patch("staging_supabase_keep_alive.requests.get")
    def test_probe_staging_supabase_http_errors(self, mock_get):
        """HTTP error statuses (401, 403, 429, 500, 503) evaluate to failure."""
        for code in [401, 403, 429, 500, 503]:
            mock_response = MagicMock()
            mock_response.status_code = code
            mock_get.return_value = mock_response

            result = keep_alive.probe_staging_supabase(VALID_STAGING_URL, VALID_ANON_KEY)

            self.assertFalse(result["success"])
            self.assertEqual(result["status_code"], code)
            self.assertIn(f"HTTP {code}", result["error"])

    @patch("staging_supabase_keep_alive.requests.get")
    def test_probe_staging_supabase_timeout(self, mock_get):
        """Timeout exceptions are caught safely and fail cleanly."""
        mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")

        result = keep_alive.probe_staging_supabase(VALID_STAGING_URL, VALID_ANON_KEY)

        self.assertFalse(result["success"])
        self.assertIsNone(result["status_code"])
        self.assertIn("timed out", result["error"])

    @patch("staging_supabase_keep_alive.requests.get")
    def test_probe_staging_supabase_network_error(self, mock_get):
        """Connection errors are caught safely and fail cleanly."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Failed to resolve host")

        result = keep_alive.probe_staging_supabase(VALID_STAGING_URL, VALID_ANON_KEY)

        self.assertFalse(result["success"])
        self.assertIsNone(result["status_code"])
        self.assertIn("Network/connection error", result["error"])

    @patch("staging_supabase_keep_alive.requests.get")
    def test_probe_staging_supabase_malformed_json(self, mock_get):
        """Malformed JSON response fails cleanly."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "foo", 0)
        mock_get.return_value = mock_response

        result = keep_alive.probe_staging_supabase(VALID_STAGING_URL, VALID_ANON_KEY)

        self.assertFalse(result["success"])
        self.assertIn("Failed to parse JSON response", result["error"])

    @patch("staging_supabase_keep_alive.requests.get")
    def test_probe_staging_supabase_non_array_json(self, mock_get):
        """Non-list JSON response (e.g. error object) fails cleanly."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Invalid JWT"}
        mock_get.return_value = mock_response

        result = keep_alive.probe_staging_supabase(VALID_STAGING_URL, VALID_ANON_KEY)

        self.assertFalse(result["success"])
        self.assertIn("expected a JSON array", result["error"])

    @patch("staging_supabase_keep_alive.requests.get")
    def test_probe_zero_http_requests_when_url_invalid(self, mock_get):
        """Rejection of invalid host happens before issuing any HTTP request."""
        with self.assertRaises(ValueError):
            keep_alive.probe_staging_supabase(PROD_SUPABASE_URL, VALID_ANON_KEY)
        mock_get.assert_not_called()

    @patch.dict(
        os.environ,
        {
            "SUPABASE_STAGING_URL": VALID_STAGING_URL,
            "SUPABASE_STAGING_ANON_KEY": "secret_staging_key_1234567890_super_sensitive_token",
        },
        clear=True,
    )
    def test_probe_logs_never_contain_secrets_or_payload_data(self):
        """Ensure API keys and database rows are never emitted in logs."""
        secret_token = "secret_staging_key_1234567890_super_sensitive_token"
        sensitive_row_content = "confidential_video_title_or_user_id"

        with patch("staging_supabase_keep_alive.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = [{"id": sensitive_row_content}]
            mock_get.return_value = mock_response

            with self.assertLogs("staging_keep_alive", level="INFO") as cm:
                exit_code = keep_alive.main()
                self.assertEqual(exit_code, 0)

            log_output = " ".join(cm.output)
            self.assertNotIn(secret_token, log_output)
            self.assertNotIn(sensitive_row_content, log_output)

    @patch.dict(
        os.environ,
        {
            "SUPABASE_STAGING_URL": VALID_STAGING_URL,
            "SUPABASE_STAGING_ANON_KEY": VALID_ANON_KEY,
        },
        clear=True,
    )
    @patch("staging_supabase_keep_alive.probe_staging_supabase")
    def test_cli_main_success(self, mock_probe):
        """CLI main() returns 0 when probe succeeds."""
        mock_probe.return_value = {
            "success": True,
            "status_code": 200,
            "duration_ms": 125.4,
            "error": None,
            "row_count": 0,
        }
        exit_code = keep_alive.main()
        self.assertEqual(exit_code, 0)

    @patch.dict(os.environ, {}, clear=True)
    def test_cli_main_missing_config(self):
        """CLI main() returns 1 when required environment variables are unset."""
        exit_code = keep_alive.main()
        self.assertEqual(exit_code, 1)

    @patch.dict(
        os.environ,
        {
            "SUPABASE_STAGING_URL": VALID_STAGING_URL,
            "SUPABASE_STAGING_ANON_KEY": VALID_ANON_KEY,
        },
        clear=True,
    )
    @patch("staging_supabase_keep_alive.probe_staging_supabase")
    def test_cli_main_probe_failure(self, mock_probe):
        """CLI main() returns 1 when probe fails."""
        mock_probe.return_value = {
            "success": False,
            "status_code": 500,
            "duration_ms": 250.0,
            "error": "HTTP 500",
            "row_count": 0,
        }
        exit_code = keep_alive.main()
        self.assertEqual(exit_code, 1)

    def test_production_keep_alive_files_untouched(self):
        """Confirm that legacy Production keep-alive files are completely untouched."""
        prod_script = ROOT_DIR / "scripts" / "keep_alive.py"
        prod_workflow = ROOT_DIR / ".github" / "workflows" / "keep_alive.yml"

        self.assertTrue(prod_script.exists())
        self.assertTrue(prod_workflow.exists())

        # Check git diff on those specific files against HEAD
        diff_script = subprocess.run(
            ["git", "diff", "HEAD", "--", str(prod_script)],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
        )
        self.assertEqual(diff_script.stdout.strip(), "", "scripts/keep_alive.py has uncommitted changes!")

        diff_workflow = subprocess.run(
            ["git", "diff", "HEAD", "--", str(prod_workflow)],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
        )
        self.assertEqual(diff_workflow.stdout.strip(), "", ".github/workflows/keep_alive.yml has uncommitted changes!")

    def test_workflow_file_integrity(self):
        """Confirm that the new staging keep-alive workflow YAML is valid and properly isolated."""
        workflow_path = ROOT_DIR / ".github" / "workflows" / "staging_supabase_keep_alive.yml"
        self.assertTrue(workflow_path.exists(), "Workflow file does not exist!")

        content = workflow_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)

        # Name and triggers
        self.assertEqual(data.get("name"), "Supabase Staging Free-Tier Keep-Alive & Monitoring")
        triggers = data.get("on") or data.get(True)  # YAML parsers may interpret 'on' as boolean True
        self.assertIsNotNone(triggers)

        # Permissions
        permissions = data.get("permissions")
        self.assertEqual(permissions.get("contents"), "read")

        # Job configuration
        jobs = data.get("jobs", {})
        self.assertIn("staging-keep-alive", jobs)
        job = jobs["staging-keep-alive"]
        self.assertEqual(job.get("runs-on"), "ubuntu-latest")
        self.assertEqual(job.get("timeout-minutes"), 5)

        # Assert secret references
        self.assertIn("SUPABASE_STAGING_URL", content)
        self.assertIn("SUPABASE_STAGING_ANON_KEY", content)
        # Ensure production secrets are NOT referenced
        self.assertNotIn("SUPABASE_SERVICE_ROLE_KEY", content)
        self.assertNotIn("secrets.SUPABASE_URL", content)
        self.assertNotIn("secrets.SUPABASE_KEY", content)


if __name__ == "__main__":
    unittest.main()
