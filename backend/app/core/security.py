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
import uuid
import anyio
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
    If TRUSTED_PROXY is False: returns request.client.host directly and ignores ALL forwarded headers.
    If TRUSTED_PROXY is True:
      - If TRUSTED_PROXY_HEADER is configured, uses that single-value header.
      - Otherwise checks single-value headers ('cf-connecting-ip', 'x-real-ip') or parses
        'x-forwarded-for' counting trusted hops from the right (TRUSTED_PROXY_HOPS).
      - Validates the parsed IP using ipaddress.ip_address(); falls back to request.client.host if invalid.
    """
    settings = get_settings()
    trusted_proxy = getattr(settings, "TRUSTED_PROXY", False)
    trusted_header = getattr(settings, "TRUSTED_PROXY_HEADER", None)
    trusted_hops = max(1, getattr(settings, "TRUSTED_PROXY_HOPS", 1))

    if not trusted_proxy:
        if request.client and request.client.host:
            return request.client.host
        return "127.0.0.1"

    # TRUSTED_PROXY is True: evaluate proxy headers
    candidate_ip: Optional[str] = None

    if trusted_header:
        val = request.headers.get(trusted_header.lower())
        if val and val.strip():
            candidate_ip = val.split(",")[0].strip()
    else:
        for header_name in ["cf-connecting-ip", "x-real-ip"]:
            val = request.headers.get(header_name)
            if val and val.strip():
                candidate_ip = val.split(",")[0].strip()
                if candidate_ip:
                    break

        if not candidate_ip:
            xff = request.headers.get("x-forwarded-for")
            if xff and xff.strip():
                ips = [ip.strip() for ip in xff.split(",") if ip.strip()]
                if ips:
                    idx = max(0, len(ips) - trusted_hops)
                    candidate_ip = ips[idx]

    if candidate_ip:
        import ipaddress
        try:
            ipaddress.ip_address(candidate_ip)
            return candidate_ip
        except ValueError:
            pass

    if request.client and request.client.host:
        return request.client.host

    return "127.0.0.1"


def check_anonymous_rate_limit(client_ip: str, max_requests: Optional[int] = None, window_seconds: int = 60) -> bool:
    """
    Enforces sliding-window rate limit for unauthenticated IP clients (P0 Directive: 3 req/min).
    Uses Redis-backed QuotaManager with in-memory fallback.
    """
    from backend.app.services.quota_service import get_quota_manager
    settings = get_settings()
    limit = max_requests if max_requests is not None else getattr(settings, "ANONYMOUS_RATE_LIMIT_PER_MINUTE", 3)
    qm = get_quota_manager()
    allowed, count = qm.check_generic_rate_limit(f"anon_rate:{client_ip}", limit=limit, window_seconds=window_seconds)
    return allowed

def reset_rate_limits_for_testing():
    """Helper to reset rate limits between test executions."""
    from backend.app.services.quota_service import get_quota_manager
    get_quota_manager().reset_rate_limits_for_testing()

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
            unverified_header = jwt.get_unverified_header(token)
            alg = unverified_header.get("alg") if isinstance(unverified_header, dict) else None

            allowed_algs = getattr(settings, "SUPABASE_JWT_ALGORITHMS", ["ES256"])
            if not alg or alg not in allowed_algs or alg.lower() in ["none", "hs256", "hs384", "hs512"]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Authentication failed: Algorithm '{alg}' prohibited. Only ES256 asymmetric JWKS signatures allowed."
                )

            # PyJWKClient verification off the event loop
            jwks_client = get_jwks_client()
            signing_key = await anyio.to_thread.run_sync(jwks_client.get_signing_key_from_jwt, token)

            try:
                issuer = settings.get_supabase_jwt_issuer()
            except ValueError:
                issuer = None
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=allowed_algs,
                audience=getattr(settings, "SUPABASE_JWT_AUDIENCE", "authenticated"),
                issuer=issuer or None,
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_aud": True,
                    "verify_iss": bool(issuer),
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

            try:
                uuid.UUID(str(user_id))
            except (ValueError, TypeError):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: subject identity (sub) must be a valid UUID"
                )

            # Query profile from Supabase (NEVER take role or plan_tier from token claims)
            db_profile = supabase.get_profile(user_id) if supabase.is_configured() else None
            default_free_limit = getattr(settings, "DAILY_FREE_QUOTA_LIMIT", 30)

            return {
                "id": user_id,
                "email": email or (db_profile.get("email") if db_profile else "user@universalpro.ai"),
                "plan_tier": db_profile.get("plan_tier", "free") if db_profile else "free",
                "daily_quota_limit": (db_profile.get("daily_quota_limit") or (999999 if (db_profile and db_profile.get("plan_tier") in ["pro", "unlimited"]) else default_free_limit)) if db_profile else default_free_limit,
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
        "daily_quota_limit": getattr(settings, "DAILY_GUEST_QUOTA_LIMIT", 20),
        "extractions_today": 0,
        "custom_amazon_tag": None,
        "custom_earnkaro_id": None,
        "is_anonymous": True,
        "client_ip": client_ip
    }


def get_user_quota_limits(user: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Tiered Quota Helper (UPA-1214):
    - Guest: settings.DAILY_GUEST_QUOTA_LIMIT (default 20)
    - Authenticated Free: settings.DAILY_FREE_QUOTA_LIMIT (default 30)
    - Pro: -1 (unlimited)
    """
    settings = get_settings()
    if not user or user.get("is_anonymous", False) or user.get("tier") == "guest":
        return {"tier": "guest", "daily_quota_limit": getattr(settings, "DAILY_GUEST_QUOTA_LIMIT", 20)}
    
    tier = user.get("plan_tier") or user.get("role") or user.get("tier", "free")
    if tier in ["pro", "unlimited"]:
        return {"tier": "pro", "daily_quota_limit": -1}
    
    return {"tier": "free", "daily_quota_limit": getattr(settings, "DAILY_FREE_QUOTA_LIMIT", 30)}


def require_admin_user(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Enforces strict Admin authorization for telemetry, metrics, and system administration endpoints.
    Requirement D.1: Define 'admin' explicitly (ADMIN_API_KEY header or explicit role == 'admin').
    Fails closed (401/403) if ADMIN_API_KEY is unset or invalid.
    Does NOT accept plan_tier == 'pro' as admin.
    Rate limits admin authentication attempts using client IP (max 5 attempts per minute).
    """
    client_ip = get_client_ip(request)
    from backend.app.services.quota_service import get_quota_manager
    allowed, count = get_quota_manager().check_generic_rate_limit(f"admin_auth:{client_ip}", limit=5, window_seconds=60)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many admin authentication attempts. Please retry later."
        )

    settings = get_settings()
    admin_key_header = request.headers.get("X-Admin-Api-Key") or request.headers.get("x-admin-api-key")
    expected_admin_key = getattr(settings, "ADMIN_API_KEY", None) or os.environ.get("ADMIN_API_KEY")

    if admin_key_header:
        if not expected_admin_key:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin authentication failed: ADMIN_API_KEY is not configured on the server."
            )
        # Compare admin key as bytes using hmac.compare_digest
        if not hmac.compare_digest(admin_key_header.encode("utf-8"), expected_admin_key.encode("utf-8")):
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


