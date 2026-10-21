#!/usr/bin/env python3
"""
Universal Pro AI — Staging Supabase Free-Tier Keep-Alive & Monitoring
======================================================================
Story / Ticket: UPA-1409
Environment: Staging (mzpkdmaxsuhwezsooidu.supabase.co)

Executes a lightweight, read-only PostgREST probe against the existing
public.extractions table on Staging Supabase to generate ordinary database
activity and mitigate Supabase Free-Tier 7-day inactivity project dormancy.

Key Invariants:
1. Strict Staging isolation: Only SUPABASE_STAGING_URL and SUPABASE_STAGING_ANON_KEY.
2. Hostname lock: Rejects any URL other than mzpkdmaxsuhwezsooidu.supabase.co.
3. Read-only probe: GET /rest/v1/extractions?select=id&limit=1.
4. Zero secret logging: Never prints keys, tokens, or row contents in logs.
5. Fails closed with non-zero exit code on missing config, HTTP errors, or timeouts.
"""

import sys
import os
import time
import logging
import urllib.parse
from typing import Dict, Any, Optional
import requests

# Force UTF-8 on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Constants
ALLOWED_STAGING_HOST = "mzpkdmaxsuhwezsooidu.supabase.co"
ALLOWED_STAGING_SCHEME = "https"
ENDPOINT_PATH = "/rest/v1/extractions"
DEFAULT_TIMEOUT_SECONDS = 15

# Configure structured logger
logger = logging.getLogger("staging_keep_alive")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] [STAGING-KEEP-ALIVE] %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def validate_staging_url(raw_url: Optional[str]) -> str:
    """
    Validate that the provided URL points strictly to the approved Staging
    Supabase project hostname via HTTPS.

    Rejects empty values, non-HTTPS schemes, unexpected hostnames (such as
    Production, localhost, or third-party targets).
    """
    if not raw_url or not isinstance(raw_url, str) or not raw_url.strip():
        raise ValueError("Missing or empty SUPABASE_STAGING_URL environment variable.")

    clean_url = raw_url.strip()
    parsed = urllib.parse.urlparse(clean_url)

    if parsed.scheme.lower() != ALLOWED_STAGING_SCHEME:
        raise ValueError(
            f"Invalid URL scheme '{parsed.scheme}'. Only HTTPS is permitted."
        )

    hostname = (parsed.hostname or "").lower()
    if hostname != ALLOWED_STAGING_HOST:
        raise ValueError(
            f"Host validation rejected: '{hostname}' does not match the authorized "
            f"Staging project host '{ALLOWED_STAGING_HOST}'. Cross-environment "
            f"probes and unexpected hosts are strictly prohibited."
        )

    # Return normalized base URL without trailing slash or path
    return f"{ALLOWED_STAGING_SCHEME}://{ALLOWED_STAGING_HOST}"


def validate_staging_key(raw_key: Optional[str]) -> str:
    """
    Validate that the provided API key is a non-empty string.
    Does not log or expose the key value.
    """
    if not raw_key or not isinstance(raw_key, str) or not raw_key.strip():
        raise ValueError("Missing or empty SUPABASE_STAGING_ANON_KEY environment variable.")
    clean_key = raw_key.strip()
    if len(clean_key) < 20:
        raise ValueError("SUPABASE_STAGING_ANON_KEY appears too short to be a valid token.")
    return clean_key


def probe_staging_supabase(
    base_url: str,
    anon_key: str,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> Dict[str, Any]:
    """
    Execute a minimal, read-only PostgREST probe against Staging Supabase.

    Endpoint: GET /rest/v1/extractions?select=id&limit=1
    Headers:
      - apikey: <anon_key>
      - Authorization: Bearer <anon_key>
      - Accept: application/json
      - User-Agent: UniversalProAI-KeepAlive/1.0 (Staging)

    Returns a structured dictionary with outcome metadata.
    Never includes secrets or database row payloads in the result.
    """
    # Defensive preflight validation
    validated_base = validate_staging_url(base_url)
    validated_key = validate_staging_key(anon_key)

    probe_url = f"{validated_base}{ENDPOINT_PATH}?select=id&limit=1"

    headers = {
        "apikey": validated_key,
        "Authorization": f"Bearer {validated_key}",
        "Accept": "application/json",
        "User-Agent": "UniversalProAI-KeepAlive/1.0 (Staging)",
    }

    start_time = time.perf_counter()
    try:
        response = requests.get(
            probe_url,
            headers=headers,
            timeout=timeout_seconds,
        )
        duration_ms = (time.perf_counter() - start_time) * 1000.0

        status_code = response.status_code

        if status_code == 200:
            try:
                data = response.json()
                if not isinstance(data, list):
                    return {
                        "success": False,
                        "status_code": status_code,
                        "duration_ms": duration_ms,
                        "error": "Unexpected response shape: expected a JSON array.",
                        "row_count": 0,
                    }
                # Success: treat both empty list [] and populated list as valid DB activity
                return {
                    "success": True,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                    "error": None,
                    "row_count": len(data),
                }
            except Exception as json_err:
                return {
                    "success": False,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                    "error": f"Failed to parse JSON response: {type(json_err).__name__}",
                    "row_count": 0,
                }
        else:
            return {
                "success": False,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "error": f"HTTP {status_code} returned by Staging PostgREST endpoint.",
                "row_count": 0,
            }

    except requests.exceptions.Timeout:
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "success": False,
            "status_code": None,
            "duration_ms": duration_ms,
            "error": f"Request timed out after {timeout_seconds} seconds.",
            "row_count": 0,
        }
    except requests.exceptions.RequestException as req_err:
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "success": False,
            "status_code": None,
            "duration_ms": duration_ms,
            "error": f"Network/connection error: {type(req_err).__name__}",
            "row_count": 0,
        }
    except Exception as exc:
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "success": False,
            "status_code": None,
            "duration_ms": duration_ms,
            "error": f"Unexpected error during probe: {type(exc).__name__}",
            "row_count": 0,
        }


def main() -> int:
    """CLI entrypoint for local execution and GitHub Actions workflow."""
    logger.info("Initializing Supabase Staging Free-Tier Keep-Alive probe...")
    logger.info(f"Target host: {ALLOWED_STAGING_HOST} | Endpoint: {ENDPOINT_PATH}?select=id&limit=1")

    raw_url = os.environ.get("SUPABASE_STAGING_URL")
    raw_key = os.environ.get("SUPABASE_STAGING_ANON_KEY")

    try:
        validated_url = validate_staging_url(raw_url)
        validated_key = validate_staging_key(raw_key)
    except ValueError as val_err:
        logger.error(f"Configuration validation failed: {val_err}")
        return 1

    result = probe_staging_supabase(validated_url, validated_key)

    if result["success"]:
        logger.info(
            f"PROBE SUCCESS: HTTP {result['status_code']} OK | "
            f"Duration: {result['duration_ms']:.2f}ms | "
            f"Rows observed: {result['row_count']} | "
            f"Activity refreshed on Staging database."
        )
        return 0
    else:
        logger.error(
            f"PROBE FAILED: HTTP {result.get('status_code', 'N/A')} | "
            f"Duration: {result['duration_ms']:.2f}ms | "
            f"Reason: {result['error']}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
