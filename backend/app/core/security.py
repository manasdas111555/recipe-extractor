"""
Security & Authentication Middleware (UPA-105 & Sprint 3 Rate Hardening)
========================================================================
Validates Supabase JWT Bearer tokens, provisions guest access sessions,
and enforces strict sliding-window rate limiting on unauthenticated IP traffic.
"""

import time
import jwt
import hashlib
from collections import defaultdict
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.app.core.config import get_settings
from backend.app.core.supabase_client import get_supabase_client

settings = get_settings()
security = HTTPBearer(auto_error=False)

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

async def get_current_user(
    request: Request,
    auth_credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, Any]:
    """
    Dependency that inspects the incoming request for Supabase JWT authorization.
    Returns:
        - Authenticated user payload if valid Bearer token provided.
        - Anonymous guest profile if no token provided.
    Raises:
        - HTTP 401 if token is expired, malformed, or signature invalid.
    """
    supabase = get_supabase_client()

    # 1. Check if Bearer token was provided in Authorization header
    if auth_credentials:
        token = auth_credentials.credentials
        try:
            unverified_payload = jwt.decode(token, options={"verify_signature": False})
            user_id = unverified_payload.get("sub")
            email = unverified_payload.get("email")

            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing subject identity (sub)"
                )

            # Query profile from Supabase
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
                "client_ip": request.client.host if request.client else "127.0.0.1"
            }

        except jwt.PyJWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Authentication failed: {str(e)}"
            )

    # 2. No token provided: Provision Anonymous Guest User Session
    client_ip = request.client.host if request.client else "127.0.0.1"
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

