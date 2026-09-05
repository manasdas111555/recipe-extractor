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
    # Service Information
    PROJECT_NAME: str = "Universal Pro AI — API Gateway"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Supabase Data Layer
    SUPABASE_URL: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None

    # AI Multimodal Providers
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    MISTRALAI_API_KEY: Optional[str] = None

    # Monetization & Affiliate IDs
    AMAZON_AFFILIATE_TAG: str = "manasdas11155-21"
    EARNKARO_ID: str = "5608766"

    # Queue & Worker URLs
    REDIS_URL: str = "redis://localhost:6379/0"
    RESIDENTIAL_PROXY_URL: Optional[str] = None

    # CORS Allowed Origins
    CORS_ORIGINS: List[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore"
    )

_settings_instance: Optional[Settings] = None

def get_settings() -> Settings:
    """Returns singleton cached instance of application settings."""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
