"""
FastAPI Extraction Endpoints (UPA-106 & UPA-107)
================================================
- POST /api/v1/extract: Enqueues extraction job with quota gating & SHA-256 cache check.
- GET /api/v1/extract/status/{job_id}: Real-time polling and progress tracker.
"""

import uuid
import hashlib
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

from backend.app.core.security import get_current_user
from backend.app.core.supabase_client import get_supabase_client
from backend.app.services.job_manager import get_job_manager, run_extraction_worker_sync

router = APIRouter(prefix="/extract", tags=["Extraction"])

class ExtractRequest(BaseModel):
    video_url: str = Field(..., description="Public video URL from Instagram, YouTube Shorts, or TikTok")
    preferred_language: Optional[str] = Field("en", description="Target output language code (e.g., 'en', 'hi', 'es')")
    domain_hint: Optional[str] = Field("auto", description="Domain classification hint: 'auto', 'recipe', 'kitchen_product', 'tech_diy', 'fitness_workout'")

    @field_validator("video_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        clean = v.strip()
        if not (clean.startswith("http://") or clean.startswith("https://")):
            raise ValueError("video_url must start with http:// or https://")
        if len(clean) < 10:
            raise ValueError("video_url is too short to be a valid URL")
        return clean


class ExtractResponse(BaseModel):
    job_id: str
    status: str
    is_cached: bool
    message: str
    poll_url: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class ExtractStatusResponse(BaseModel):
    job_id: str
    status: str
    stage: Optional[str] = None
    progress_percent: int
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@router.post("", response_model=ExtractResponse, summary="Enqueue Extraction Job or Return Cached Hit")
async def enqueue_extraction(
    payload: ExtractRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """
    Submits a short-form video for multimodal extraction.
    1. Validates user daily quota (returns 429 if exceeded).
    2. Computes SHA-256 URL hash and checks PostgreSQL cache.
    3. If cached, returns HTTP 200 with zero-cost data immediately.
    4. If new, enqueues background extraction and returns HTTP 202 with job_id and poll_url.
    """
    extractions_today = current_user.get("extractions_today", 0)
    daily_limit = current_user.get("daily_quota_limit", 3)

    if extractions_today >= daily_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Daily extraction quota limit reached for free tier. Upgrade to Pro for unlimited extractions."
        )

    # Compute URL Hash for viral 0-cost caching
    canonical_url = payload.video_url.strip()
    url_hash = hashlib.sha256(canonical_url.encode("utf-8")).hexdigest()

    supabase = get_supabase_client()
    cached = supabase.get_cached_extraction(url_hash)

    if cached and cached.get("content_payload"):
        # Instant cache hit (0-cost)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "job_id": cached.get("id", "cached"),
                "status": "completed",
                "is_cached": True,
                "message": "Viral cache hit! Intelligence retrieved in 0ms from PostgreSQL cache.",
                "poll_url": None,
                "data": cached.get("content_payload")
            }
        )

    # Cache miss: Enqueue asynchronous worker job
    job_id = str(uuid.uuid4())
    job_manager = get_job_manager()
    job_manager.create_job(
        job_id=job_id,
        video_url=canonical_url,
        url_hash=url_hash,
        user_id=str(current_user.get("id"))
    )

    background_tasks.add_task(
        run_extraction_worker_sync,
        job_id=job_id,
        video_url=canonical_url,
        url_hash=url_hash,
        user_id=str(current_user.get("id")),
        preferred_language=payload.preferred_language or "en",
        domain_hint=payload.domain_hint or "auto"
    )

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "job_id": job_id,
            "status": "queued",
            "is_cached": False,
            "message": "Extraction job enqueued successfully.",
            "poll_url": f"/api/v1/extract/status/{job_id}",
            "data": None
        }
    )


@router.get("/status/{job_id}", response_model=ExtractStatusResponse, summary="Poll Extraction Job Status & Output")
async def get_extraction_status(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Polls the real-time status and stage of an enqueued extraction job.
    Returns current stage ('downloading_media', 'multimodal_ai_inference', 'completed', 'failed')
    and complete data payload once finished.
    """
    job_manager = get_job_manager()
    job = job_manager.get_job(job_id)

    if not job:
        # Fallback: check if job is stored in Supabase extractions table by ID
        supabase = get_supabase_client()
        if supabase.is_configured():
            try:
                import requests
                url = f"{supabase.base_url}/rest/v1/extractions?id=eq.{job_id}&select=*"
                r = requests.get(url, headers=supabase._get_headers(use_service_role=True), timeout=4)
                if r.status_code == 200 and r.json():
                    rec = r.json()[0]
                    return ExtractStatusResponse(
                        job_id=job_id,
                        status=rec.get("status", "completed"),
                        stage="completed",
                        progress_percent=100,
                        data=rec.get("content_payload"),
                        error=None
                    )
            except Exception:
                pass

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Extraction job '{job_id}' not found."
        )

    return ExtractStatusResponse(
        job_id=job["job_id"],
        status=job["status"],
        stage=job.get("stage"),
        progress_percent=job.get("progress_percent", 0),
        data=job.get("data"),
        error=job.get("error")
    )
