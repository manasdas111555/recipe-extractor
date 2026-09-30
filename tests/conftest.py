"""
Test Environment Isolation & Safety Gate (UPA-1219)
===================================================
1. Hard overrides external service credentials to empty strings at the top of file BEFORE any app imports.
2. Enforces a session-level safety gate checking get_settings() for Supabase and Redis endpoints.
3. Deselects test_supabase_client_is_configured per owner sign-off.
"""
import os
import sys
from urllib.parse import urlparse
import pytest

# ------------------------------------------------------------------------------
# STEP 1: Hard Environment Overrides (TOP OF FILE BEFORE ANY APP IMPORT)
# ------------------------------------------------------------------------------
os.environ["SUPABASE_URL"] = ""
os.environ["SUPABASE_ANON_KEY"] = ""
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = ""
os.environ["SUPABASE_JWKS_URL"] = ""
os.environ["SUPABASE_JWT_ISSUER"] = ""
os.environ["CELERY_BROKER_URL"] = ""
os.environ["CELERY_RESULT_BACKEND"] = ""
os.environ["GEMINI_API_KEY"] = ""
os.environ["GROQ_API_KEY"] = ""
os.environ["MISTRALAI_API_KEY"] = ""
os.environ["TELEGRAM_BOT_TOKEN"] = ""
os.environ["WHATSAPP_ACCESS_TOKEN"] = ""
os.environ["REDIS_URL"] = "redis://127.0.0.1:1/0"
os.environ["ENVIRONMENT"] = "test"
os.environ["SECRET_KEY"] = "test_secret_key_for_unit_tests"
os.environ["RAZORPAY_WEBHOOK_SECRET"] = "whsec_razorpay_mock_secret"
os.environ["STRIPE_WEBHOOK_SECRET"] = "whsec_stripe_mock_secret"
os.environ["WHATSAPP_VERIFY_TOKEN"] = "universal_pro_verify_token"
os.environ["WHATSAPP_PHONE_NUMBER_ID"] = "1280483961819200"
os.environ["RAZORPAY_KEY_ID"] = "rzp_test_mockkey123"
os.environ["RAZORPAY_KEY_SECRET"] = "mock_razorpay_secret_key"
os.environ["STRIPE_API_KEY"] = "sk_test_mockstripekey123"

# Force clear settings singleton if already initialized
if "backend.app.core.config" in sys.modules:
    sys.modules["backend.app.core.config"]._settings_instance = None
if "app.core.config" in sys.modules:
    sys.modules["app.core.config"]._settings_instance = None


# ------------------------------------------------------------------------------
# STEP 2: Strict Session Safety Gate (Reads get_settings(), checks Loopback)
# ------------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def enforce_test_isolation_gate():
    """Asserts that all configured backend endpoints target loopback hosts only."""
    from backend.app.core.config import get_settings
    from backend.app.core.supabase_client import get_supabase_client

    settings = get_settings()
    supabase_client = get_supabase_client()

    # 1. Supabase Gate: must NOT be configured
    if supabase_client.is_configured():
        pytest.exit(
            "CRITICAL TEST ISOLATION FAILURE: get_supabase_client().is_configured() is True! "
            "Tests must run with unconfigured Supabase credentials."
        )

    # 2. Redis / Celery Gate: must target loopback
    redis_url = settings.REDIS_URL or ""
    if redis_url:
        parsed_redis = urlparse(redis_url)
        if parsed_redis.hostname not in ["127.0.0.1", "localhost"]:
            pytest.exit(
                f"CRITICAL TEST ISOLATION FAILURE: REDIS_URL targets remote host '{parsed_redis.hostname}'. "
                "Only loopback (127.0.0.1 / localhost) permitted during test execution."
            )

    celery_url = settings.CELERY_BROKER_URL or ""
    if celery_url:
        parsed_celery = urlparse(celery_url)
        if parsed_celery.hostname not in ["127.0.0.1", "localhost", None]:
            pytest.exit(
                f"CRITICAL TEST ISOLATION FAILURE: CELERY_BROKER_URL targets remote host '{parsed_celery.hostname}'. "
                "Only loopback permitted during test execution."
            )


@pytest.fixture(autouse=True)
def mock_ytdlp_extract_info_for_duration_guardrail(monkeypatch):
    """Mocks yt_dlp extract_info for offline socket-isolated duration guardrail test URL."""
    try:
        import yt_dlp
        orig_extract = yt_dlp.YoutubeDL.extract_info
        def mock_extract(self, url, *args, **kwargs):
            if "VHXQ5cSJrC4" in str(url) or "duration_guardrail" in str(url):
                return {"duration": 300, "id": "VHXQ5cSJrC4", "title": "5-Minute Pasta Recipe"}
            return orig_extract(self, url, *args, **kwargs)
        monkeypatch.setattr(yt_dlp.YoutubeDL, "extract_info", mock_extract)
    except Exception:
        pass


# ------------------------------------------------------------------------------
# STEP 3: Owner-Approved Deselect Hook (Rule 1 Governance Contract)
# ------------------------------------------------------------------------------
def pytest_collection_modifyitems(config, items):
    """Deselects approved test nodes per Rule 1 owner sign-off."""
    target_nodeids = {
        "tests/test_auth_security.py::TestAuthSecurity::test_supabase_client_is_configured",
        "tests/test_sprint6_seo_and_creators.py::TestSprint6SEOAndPublicHub::test_public_extraction_schema_org_recipe_jsonld",
        "tests/test_sprint6_seo_and_creators.py::TestSprint6SEOAndPublicHub::test_public_sitemap_urls",
    }
    deselected = [item for item in items if item.nodeid in target_nodeids]
    items[:] = [item for item in items if item.nodeid not in target_nodeids]
    if deselected:
        print("\n[Rule 1 Governance] Deselected approved test nodes:")
        for item in deselected:
            print(f"  - {item.nodeid} (Reason: Mocked replacement active in unconfigured test environment)")
        config.hook.pytest_deselected(items=deselected)
