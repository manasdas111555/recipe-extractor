"""
Core Application Configuration
==============================
Loads environment settings, API keys, and service configurations
using Pydantic Settings with automatic .env discovery.
"""

import os
from typing import List, Optional
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_FILE = ROOT_DIR / ".env"

class Settings(BaseSettings):
    # Service Information & Admin Security
    PROJECT_NAME: str = "Universal Pro AI - API Gateway"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    ADMIN_API_KEY: Optional[str] = None
    TRUSTED_PROXY: bool = False
    TRUSTED_PROXY_HOPS: int = 1
    ALLOW_DB_WRITES: bool = False

    # Supabase Data Layer
    SUPABASE_URL: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None
    SUPABASE_JWKS_URL: Optional[str] = None
    SUPABASE_JWT_ISSUER: Optional[str] = None
    SUPABASE_JWT_AUDIENCE: str = "authenticated"
    SUPABASE_JWT_ALGORITHMS: List[str] = ["ES256"]

    def get_supabase_jwks_url(self) -> str:
        if self.SUPABASE_JWKS_URL:
            return self.SUPABASE_JWKS_URL
        if not self.SUPABASE_URL:
            raise ValueError("Configuration error: Missing required setting 'SUPABASE_URL' or 'SUPABASE_JWKS_URL'.")
        base = self.SUPABASE_URL.rstrip("/")
        return f"{base}/auth/v1/.well-known/jwks.json"

    def get_supabase_jwt_issuer(self) -> str:
        if self.SUPABASE_JWT_ISSUER:
            return self.SUPABASE_JWT_ISSUER
        if not self.SUPABASE_URL:
            raise ValueError("Configuration error: Missing required setting 'SUPABASE_URL' or 'SUPABASE_JWT_ISSUER'.")
        base = self.SUPABASE_URL.rstrip("/")
        return f"{base}/auth/v1"

    # AI Multimodal Providers
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    MISTRALAI_API_KEY: Optional[str] = None

    # Monetization & Affiliate IDs
    AMAZON_AFFILIATE_TAG: str = "manasdas11155-21"
    EARNKARO_ID: str = "5608766"

    # Queue & Worker Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    CELERY_TASK_TIMEOUT: int = 180
    USE_PROXIES: bool = False
    RESIDENTIAL_PROXY_URL: Optional[str] = None
    MAX_MEDIA_DOWNLOAD_MB: int = 50
    MEDIA_DOWNLOAD_RESOLUTION: str = "360"

    # Chat Ingestion & Webhook Settings (Sprint 3)
    SECRET_KEY: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_WEBHOOK_SECRET: Optional[str] = None
    WHATSAPP_VERIFY_TOKEN: Optional[str] = None
    WHATSAPP_ACCESS_TOKEN: Optional[str] = None
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = None
    WHATSAPP_APP_SECRET: Optional[str] = None

    # Quota & Rate Limiting (Sprint 3 & 5)
    DAILY_GUEST_QUOTA_LIMIT: int = 3
    DAILY_FREE_QUOTA_LIMIT: int = 10

    # Billing & Subscriptions — Razorpay (Sprint 5)
    RAZORPAY_KEY_ID: Optional[str] = None
    RAZORPAY_KEY_SECRET: Optional[str] = None
    RAZORPAY_WEBHOOK_SECRET: Optional[str] = None
    RAZORPAY_PLAN_PRO_299_INR: str = "plan_pro_299_inr"

    # Billing & Subscriptions — Stripe (Sprint 5)
    STRIPE_API_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_PRICE_PRO_499_USD: str = "price_pro_499_usd"

    # CORS Allowed Origins
    CORS_ORIGINS: List[str] = []

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def model_post_init(self, __context):
        env_name = (self.ENVIRONMENT or "development").lower()

        if env_name in ["development", "development_strict"]:
            if not self.SECRET_KEY:
                raise ValueError("Local development environment error: SECRET_KEY is missing. Please create a local .env file or set SECRET_KEY.")
        elif env_name in ["test", "testing"]:
            # In test environment, all settings must be supplied via environment variables (e.g. conftest.py)
            pass
        else:
            required_secrets = {
                "SECRET_KEY": self.SECRET_KEY,
                "SUPABASE_URL": self.SUPABASE_URL,
                "SUPABASE_ANON_KEY": self.SUPABASE_ANON_KEY,
                "SUPABASE_SERVICE_ROLE_KEY": self.SUPABASE_SERVICE_ROLE_KEY,
            }
            for key_name, val in required_secrets.items():
                if not val:
                    raise ValueError(f"Production environment setup failure: Missing required secret environment variable '{key_name}'")


_settings_instance: Optional[Settings] = None

def get_settings() -> Settings:
    """Returns singleton cached instance of application settings."""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance


# Re-export legacy configuration helpers for backwards compatibility
try:
    from app.services.config import (
        MAX_VIDEO_DURATION,
        get_download_dir,
        ensure_download_dir,
        get_youtube_cookie_file,
        cleanup_old_downloads,
        get_env_var,
        set_env_var,
        get_api_key,
        save_api_key,
        get_mistral_api_key,
        get_aionlabs_api_key,
        get_groq_api_key,
        get_nvidia_api_key,
        get_affiliate_tags,
        save_affiliate_tags
    )
except ImportError:
    try:
        from backend.app.services.config import (
            MAX_VIDEO_DURATION,
            get_download_dir,
            ensure_download_dir,
            get_youtube_cookie_file,
            cleanup_old_downloads,
            get_env_var,
            set_env_var,
            get_api_key,
            save_api_key,
            get_mistral_api_key,
            get_aionlabs_api_key,
            get_groq_api_key,
            get_nvidia_api_key,
            get_affiliate_tags,
            save_affiliate_tags
        )
    except ImportError:
        pass

