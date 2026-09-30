"""
JWT ES256 JWKS Verification Test Suite (UPA-1212)
===================================================
Validates:
1. Valid ES256 token signed with EC P-256 key pair and verified against JWKS passes authentication.
2. Forged signature fails authentication (401).
3. Expired token (exp in past) fails authentication (401).
4. Token with wrong audience (aud != "authenticated") fails authentication (401).
5. Token with algorithm 'none' fails authentication (401).
6. Token with algorithm 'HS256' fails authentication (401).
"""

import time
import pytest
import jwt
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

from backend.app.main import app
from backend.app.core.config import get_settings

client = TestClient(app)
settings = get_settings()

# Generate a local EC P-256 key pair for test mocking
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

pem_public = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)


def create_es256_token(payload: dict, key=private_key, alg="ES256", kid="test-key-id") -> str:
    """Helper to mint a JWT signed with ES256 and custom kid header."""
    headers = {"kid": kid, "alg": alg}
    return jwt.encode(payload, key, algorithm=alg, headers=headers)


@pytest.fixture(autouse=True)
def mock_jwks_client():
    """Mocks PyJWKClient to return our local EC public key for kid 'test-key-id'."""
    mock_signing_key = MagicMock()
    mock_signing_key.key = public_key

    mock_client = MagicMock()
    mock_client.get_signing_key_from_jwt.return_value = mock_signing_key

    with patch("backend.app.core.security.get_jwks_client", return_value=mock_client):
        yield mock_client


def test_valid_es256_token_authenticated_successfully():
    payload = {
        "sub": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "email": "es256@universalpro.ai",
        "aud": "authenticated",
        "iss": "https://example.supabase.co/auth/v1",
        "exp": int(time.time()) + 3600
    }
    token = create_es256_token(payload)

    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    user = res.json().get("user", {})
    assert user.get("id") == "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    assert user.get("is_anonymous") is False


def test_forged_signature_returns_401():
    payload = {
        "sub": "user_forged_123",
        "aud": "authenticated",
        "iss": "https://example.supabase.co/auth/v1",
        "exp": int(time.time()) + 3600
    }
    # Sign with a different random private key
    other_key = ec.generate_private_key(ec.SECP256R1())
    forged_token = create_es256_token(payload, key=other_key)

    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {forged_token}"})
    assert res.status_code == 401
    assert "authentication failed" in res.json().get("detail", "").lower()


def test_expired_token_returns_401():
    payload = {
        "sub": "user_expired_123",
        "aud": "authenticated",
        "iss": "https://example.supabase.co/auth/v1",
        "exp": int(time.time()) - 100 # Expired 100s ago
    }
    expired_token = create_es256_token(payload)

    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert res.status_code == 401
    assert "authentication failed" in res.json().get("detail", "").lower()


def test_wrong_audience_returns_401():
    payload = {
        "sub": "user_wrong_aud_123",
        "aud": "unauthenticated_guest", # Wrong audience
        "iss": "https://example.supabase.co/auth/v1",
        "exp": int(time.time()) + 3600
    }
    wrong_aud_token = create_es256_token(payload)

    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {wrong_aud_token}"})
    assert res.status_code == 401
    assert "authentication failed" in res.json().get("detail", "").lower()


def test_algorithm_hs256_token_rejected_with_401():
    payload = {
        "sub": "user_hs256_123",
        "aud": "authenticated",
        "exp": int(time.time()) + 3600
    }
    hs256_token = jwt.encode(payload, "some-secret-key", algorithm="HS256")

    orig_env = settings.ENVIRONMENT
    try:
        settings.ENVIRONMENT = "production"
        res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {hs256_token}"})
        assert res.status_code == 401
        assert "prohibited" in res.json().get("detail", "").lower() or "authentication failed" in res.json().get("detail", "").lower()
    finally:
        settings.ENVIRONMENT = orig_env


def test_algorithm_none_token_rejected_with_401():
    payload = {
        "sub": "user_none_123",
        "aud": "authenticated",
        "exp": int(time.time()) + 3600
    }
    none_token = jwt.encode(payload, "", algorithm="none")

    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {none_token}"})
    assert res.status_code == 401
    assert "prohibited" in res.json().get("detail", "").lower() or "authentication failed" in res.json().get("detail", "").lower()
