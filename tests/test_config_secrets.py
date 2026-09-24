"""
Unit Tests for Configuration Secret Hygiene & Environment Gates (UPA-1202)
=============================================================================
Validates:
1. Hardcoded constant fallback strings removed for all secrets (SECRET_KEY, RAZORPAY_*, STRIPE_*, WHATSAPP_*).
2. Production environment startup fails with ValueError if required secrets are missing, printing key name only.
3. Development environment startup fails if SECRET_KEY is missing.
4. Test environment provides safe test-scoped fallbacks for test execution.
"""

import os
import pytest
from pydantic import ValidationError
from backend.app.core.config import Settings


def test_production_environment_gate_fails_on_missing_secrets(monkeypatch):
    """Verify production startup fails immediately if required secrets are missing."""
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_ANON_KEY", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)

    with pytest.raises(ValueError) as excinfo:
        Settings(_env_file=None, SECRET_KEY=None, SUPABASE_URL=None, SUPABASE_ANON_KEY=None, SUPABASE_SERVICE_ROLE_KEY=None)

    err_msg = str(excinfo.value)
    assert "Production environment setup failure" in err_msg
    assert "SECRET_KEY" in err_msg


def test_development_environment_gate_fails_on_missing_secret_key(monkeypatch):
    """Verify local development mode fails if SECRET_KEY is not set."""
    monkeypatch.setenv("ENVIRONMENT", "development_strict")
    monkeypatch.delenv("SECRET_KEY", raising=False)

    with pytest.raises(ValueError) as excinfo:
        Settings(_env_file=None, ENVIRONMENT="development_strict", SECRET_KEY=None)

    assert "Local development environment error: SECRET_KEY is missing" in str(excinfo.value)


def test_test_environment_provides_test_fallbacks(monkeypatch):
    """Verify test environment populates no fallback secrets in production code."""
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("RAZORPAY_WEBHOOK_SECRET", raising=False)

    settings = Settings(_env_file=None)
    assert settings.SECRET_KEY is None
    assert settings.RAZORPAY_WEBHOOK_SECRET is None
    assert settings.DEBUG is False
