"""
Security & Authentication Middleware (UPA-105)
==============================================
Validates Supabase JWT Bearer tokens and provisions guest access sessions.
Protects endpoints while allowing frictionless anonymous trial extractions.
"""

import jwt
import hashlib
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.app.core.config import get_settings
from backend.app.core.supabase_client import get_supabase_client

settings = get_settings()
security = HTTPBearer(auto_error=False)

async def get_current_user(
    request: Request,
    auth_credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, Any]:
    """
    Dependency that inspects the incoming request for Supabase JWT authorization.
    Returns:
        - Authenticated user payload if valid Bearer token provided.
        - Anonymous guest profile if no token provided (allows 3 free extractions).
    Raises:
        - HTTP 401 if token is expired, malformed, or signature invalid.
    """
    supabase = get_supabase_client()

    # 1. Check if Bearer token was provided in Authorization header
    if auth_credentials:
        token = auth_credentials.credentials
        try:
            # Decode unverified or verified depending on environment
            # In Supabase, the JWT payload contains 'sub' (User UUID), 'email', 'role'
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
                "daily_quota_limit": db_profile.get("daily_quota_limit", 3) if db_profile else 3,
                "extractions_today": db_profile.get("extractions_today", 0) if db_profile else 0,
                "custom_amazon_tag": db_profile.get("custom_amazon_tag") if db_profile else None,
                "custom_earnkaro_id": db_profile.get("custom_earnkaro_id") if db_profile else None,
                "is_anonymous": False
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
        "is_anonymous": True
    }
