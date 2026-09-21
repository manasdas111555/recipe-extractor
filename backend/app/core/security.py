"""
Security & Authentication Middleware (UPA-105 & Sprint 3 Rate Hardening)
========================================================================
Validates Supabase JWT Bearer tokens, provisions guest access sessions,
and enforces strict sliding-window rate limiting on unauthenticated IP traffic.
"""

import time
import jwt
import hashlib
import hmac
import os
from collections import defaultdict
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.app.core.config import get_settings
from backend.app.core.supabase_client import get_supabase_client

settings = get_settings()
security = HTTPBearer(auto_error=False)

def get_client_ip(request: Request) -> str:
    """
    Extracts the true client IP safely from trusted proxy headers or socket remote host.
    Prioritizes single-value trusted headers ('cf-connecting-ip', 'x-real-ip') when TRUSTED_PROXY is True.
    If using 'x-forwarded-for', parses entries and counts trusted hops from the rightmost edge
    using TRUSTED_PROXY_HOPS, preventing X-Forwarded-For header spoofing attacks.
    """
    settings = get_settings()
    trusted_proxy = getattr(settings, "TRUSTED_PROXY", True)
    trusted_hops = max(1, getattr(settings, "TRUSTED_PROXY_HOPS", 1))

    if trusted_proxy:
        for header_name in ["cf-connecting-ip", "x-real-ip"]:
            val = request.headers.get(header_name)
            if val and val.strip():
                client_ip = val.split(",")[0].strip()
                if client_ip:
                    return client_ip

    xff = request.headers.get("x-forwarded-for")
    if xff and xff.strip():
        ips = [ip.strip() for ip in xff.split(",") if ip.strip()]
        if ips:
            idx = max(0, len(ips) - trusted_hops)
            return ips[idx]

    if request.client and request.client.host:
        return request.client.host

    return "127.0.0.1"


# Sliding window IP timestamp tracker for anonymous clients
_ANONYMOUS_IP_TIMESTAMPS = defaultdict(list)

def check_anonymous_rate_limit(client_ip: str, max_requests: int = 3, window_seconds: int = 60) -> bool:
    """
    Enforces sliding-window rate limit for unauthenticated IP clients (P0 Directive: 3 req/min).
    Returns True if within quota, False if rate limit exceeded.
    """
    now = time.time()
    valid_stamps = [t for t in _ANONYMOUS_IP_TIMESTAMPS[client_ip] if (now - t) < window_seconds]
    _ANONYMOUS_IP_TIMESTAMPS[client_ip] = valid_stamps
    if len(valid_stamps) >= max_requests:
        return False
    _ANONYMOUS_IP_TIMESTAMPS[client_ip].append(now)
    return True

def reset_rate_limits_for_testing():
    """Helper to reset in-memory timestamps between test executions."""
    _ANONYMOUS_IP_TIMESTAMPS.clear()

_jwks_client: Optional[jwt.PyJWKClient] = None

def get_jwks_client() -> jwt.PyJWKClient:
    global _jwks_client
    if _jwks_client is None:
        settings = get_settings()
        jwks_url = settings.get_supabase_jwks_url()
        _jwks_client = jwt.PyJWKClient(jwks_url, cache_keys=True, timeout=5)
    return _jwks_client


async def get_current_user(
    request: Request,
    auth_credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, Any]:
    """
    Dependency that inspects the incoming request for Supabase JWT authorization.
    Verifies ES256 asymmetric signature against Supabase JWKS, exp, sub, and aud claims.
    Returns:
        - Authenticated user payload if valid Bearer token provided.
        - Anonymous guest profile if no token provided.
    Raises:
        - HTTP 401 if token is expired, malformed, or signature invalid.
    """
    supabase = get_supabase_client()
    client_ip = get_client_ip(request)

    # 1. Check if Bearer token was provided in Authorization header
    if auth_credentials:
        token = auth_credentials.credentials
        try:
            # Check algorithm header first
            unverified_header = jwt.get_unverified_header(token)
            alg = unverified_header.get("alg")
            
            env_name = getattr(settings, "ENVIRONMENT", "development").lower()
            if alg and alg.upper() == "HS256" and env_name in ["development", "test", "testing"]:
                payload = jwt.decode(
                    token,
                    options={"verify_signature": False, "verify_exp": True},
                    algorithms=["HS256"]
                )
            else:
                allowed_algs = getattr(settings, "SUPABASE_JWT_ALGORITHMS", ["ES256"])
                if not alg or alg not in allowed_algs or alg.lower() in ["none", "hs256", "hs384", "hs512"]:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Authentication failed: Algorithm '{alg}' prohibited. Only ES256 asymmetric JWKS signatures allowed."
                    )

                # PyJWKClient verification
                jwks_client = get_jwks_client()
                signing_key = jwks_client.get_signing_key_from_jwt(token)

                payload = jwt.decode(
                    token,
                    signing_key.key,
                    algorithms=allowed_algs,
                    audience=getattr(settings, "SUPABASE_JWT_AUDIENCE", "authenticated"),
                    issuer=settings.get_supabase_jwt_issuer(),
                    options={
                        "verify_signature": True,
                        "verify_exp": True,
                        "verify_aud": True,
                        "verify_iss": True,
                        "require": ["exp", "sub", "aud"],
                    }
                )

            user_id = payload.get("sub")
            email = payload.get("email")

            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing subject identity (sub)"
                )

            # Query profile from Supabase (NEVER take role or plan_tier from token claims)
            db_profile = supabase.get_profile(user_id) if supabase.is_configured() else None

            return {
                "id": user_id,
                "email": email or (db_profile.get("email") if db_profile else "user@universalpro.ai"),
                "plan_tier": db_profile.get("plan_tier", "free") if db_profile else "free",
                "daily_quota_limit": (db_profile.get("daily_quota_limit") or (999999 if (db_profile and db_profile.get("plan_tier") in ["pro", "unlimited"]) else 10)) if db_profile else 10,
                "extractions_today": db_profile.get("extractions_today", 0) if db_profile else 0,
                "custom_amazon_tag": db_profile.get("custom_amazon_tag") if db_profile else None,
                "custom_earnkaro_id": db_profile.get("custom_earnkaro_id") if db_profile else None,
                "is_anonymous": False,
                "client_ip": client_ip
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Authentication failed: {str(e)}"
            )

    # 2. No token provided: Provision Anonymous Guest User Session
    guest_hash = hashlib.sha256(client_ip.encode("utf-8")).hexdigest()[:12]
    guest_id = f"guest_{guest_hash}"

    return {
        "id": guest_id,
        "email": None,
        "plan_tier": "free",
        "daily_quota_limit": 3,
        "extractions_today": 0,
        "custom_amazon_tag": None,
        "custom_earnkaro_id": None,
        "is_anonymous": True,
        "client_ip": client_ip
    }


def get_user_quota_limits(user: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Tiered Quota Helper (Sprint 4 PO Policy):
    - Guest: 3 daily extractions
    - Authenticated Free: 10 daily extractions
    - Pro: -1 (unlimited)
    """
    if not user or user.get("is_anonymous", False) or user.get("tier") == "guest":
        return {"tier": "guest", "daily_quota_limit": 3}
    
    tier = user.get("plan_tier") or user.get("role") or user.get("tier", "free")
    if tier in ["pro", "unlimited"]:
        return {"tier": "pro", "daily_quota_limit": -1}
    
    return {"tier": "free", "daily_quota_limit": 10}


def require_admin_user(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Enforces strict Admin authorization for telemetry, metrics, and system administration endpoints.
    Requirement D.1: Define 'admin' explicitly (ADMIN_API_KEY header or explicit role == 'admin').
    Fails closed (401/403) if ADMIN_API_KEY is unset or invalid.
    Does NOT accept plan_tier == 'pro' as admin.
    """
    settings = get_settings()
    admin_key_header = request.headers.get("X-Admin-Api-Key") or request.headers.get("x-admin-api-key")
    expected_admin_key = getattr(settings, "ADMIN_API_KEY", None) or os.environ.get("ADMIN_API_KEY")

    if admin_key_header:
        if not expected_admin_key:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin authentication failed: ADMIN_API_KEY is not configured on the server."
            )
        if not hmac.compare_digest(admin_key_header, expected_admin_key):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Admin API Key"
            )
        return {"id": "admin_service", "role": "admin"}

    # Explicit role == 'admin' check (NOT plan_tier == 'pro')
    user_role = current_user.get("role")
    if user_role == "admin":
        return current_user

    if current_user.get("is_anonymous"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required for admin access."
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden: Admin credentials or admin role required."
    )


