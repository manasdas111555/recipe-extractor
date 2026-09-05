"""
Universal Pro AI — FastAPI Application Entry Point
==================================================
Decoupled API Gateway for asynchronous social video extraction,
multi-tenant user state, and contextual affiliate commerce.
"""

import sys
from pathlib import Path
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure root workspace is on python sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.core.config import get_settings
from backend.app.api.v1.router import router as api_v1_router

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Universal Pro AI API Gateway: Turns ephemeral social media video feeds "
        "(Instagram Reels, YouTube Shorts, TikTok) into structured, persistent, "
        "and commercially actionable utility."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount V1 Router
app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)

@app.get("/", tags=["General"])
async def root():
    """Root endpoint welcoming clients and directing to interactive documentation."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health",
        "api_v1": f"{settings.API_V1_PREFIX}/info"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """System health check endpoint used by uptime monitors and container orchestrators."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "integrations": {
            "supabase": bool(settings.SUPABASE_URL and settings.SUPABASE_ANON_KEY),
            "gemini": bool(settings.GEMINI_API_KEY),
            "groq": bool(settings.GROQ_API_KEY),
            "mistral": bool(settings.MISTRALAI_API_KEY)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
