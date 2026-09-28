"""
FastAPI Extraction Endpoints (UPA-106 & UPA-107)
================================================
- POST /api/v1/extract: Enqueues extraction job with quota gating & SHA-256 cache check.
- GET /api/v1/extract/status/{job_id}: Real-time polling and progress tracker.
"""

import uuid
import hashlib
import logging
import os
import time
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import asyncio
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status, Request, Query
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse, Response
from pydantic import BaseModel, Field, field_validator, model_validator

from backend.app.core.config import get_settings
from backend.app.services.quota_service import get_quota_manager
from backend.app.core.security import get_current_user, check_anonymous_rate_limit
from backend.app.core.supabase_client import get_supabase_client
from backend.app.services.job_manager import get_job_manager, run_extraction_worker_sync
from backend.app.workers.celery_app import is_celery_broker_reachable, celery_app
from backend.app.workers.tasks import extract_video_task

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/extract", tags=["Extraction"])

class ExtractRequest(BaseModel):
    video_url: str = Field(..., description="Public video URL from Instagram, YouTube Shorts, or TikTok")
    preferred_language: Optional[str] = Field("en", description="Target output language code (e.g., 'en', 'hi', 'es')")
    domain_hint: Optional[str] = Field("auto", description="Domain classification hint: 'auto', 'recipe', 'kitchen_product', 'tech_diy', 'fitness_workout'")

    @model_validator(mode="before")
    @classmethod
    def normalize_url_payload(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "url" in data and ("video_url" not in data or not data.get("video_url")):
                data["video_url"] = data["url"]
        return data

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
    1. Enforces strict anonymous sliding-window rate limit (Redis-backed).
    2. Validates video URL structure, scheme, allowlist, and SSRF rules.
    3. Computes SHA-256 URL hash and checks PostgreSQL cache (0-cost).
    4. If cached, returns HTTP 200 with data immediately without consuming daily quota.
    5. If cache miss, consumes daily quota (guests and free users) and enqueues to worker pool.
    """
    settings = get_settings()

    # 1. Anonymous Tier Rate Limiter (Redis-backed sliding window per IP)
    if current_user.get("is_anonymous"):
        client_ip = current_user.get("client_ip", "127.0.0.1")
        anon_limit = getattr(settings, "ANONYMOUS_RATE_LIMIT_PER_MINUTE", 3)
        if not check_anonymous_rate_limit(client_ip, max_requests=anon_limit, window_seconds=60):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: Anonymous tier allows {anon_limit} requests per minute. Upgrade or authenticate for higher throughput."
            )

    # 2. Validate URL against Allowlist & SSRF rules (Before cache lookup & quota consumption)
    from backend.app.services.url_validator import validate_social_url, generate_stream_token
    is_valid_url, url_err, _, _ = validate_social_url(payload.video_url)
    if not is_valid_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid video URL: {url_err}"
        )

    # 3. Compute URL Hash for viral 0-cost caching
    canonical_url = payload.video_url.strip()
    url_hash = hashlib.sha256(canonical_url.encode("utf-8")).hexdigest()

    supabase = get_supabase_client()
    cached = supabase.get_cached_extraction(url_hash)

    if cached and cached.get("content_payload"):
        cache_id = cached.get("id", "cached")
        data_payload = cached.get("content_payload") or {}
        if isinstance(data_payload, dict):
            secret_key = settings.SECRET_KEY
            if secret_key:
                data_payload["stream_token"] = generate_stream_token(cache_id, secret_key, media_url=canonical_url)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "job_id": cache_id,
                "status": "completed",
                "is_cached": True,
                "message": "Viral cache hit! Intelligence retrieved in 0ms from PostgreSQL cache.",
                "poll_url": None,
                "data": data_payload
            }
        )

    # 4. Consume Daily Quota ONLY on Cache Miss (UPA-1214)
    is_anonymous = current_user.get("is_anonymous", False)
    is_pro = current_user.get("plan_tier") in ["pro", "unlimited"]
    daily_limit = current_user.get(
        "daily_quota_limit",
        getattr(settings, "DAILY_GUEST_QUOTA_LIMIT", 20) if is_anonymous else getattr(settings, "DAILY_FREE_QUOTA_LIMIT", 30)
    )

    # Backward compatibility for mocked user objects in existing test suites
    extractions_today = current_user.get("extractions_today", 0)
    if extractions_today >= daily_limit and not is_pro:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Daily extraction quota limit reached for free tier. Upgrade to Pro for unlimited extractions."
        )

    # Active Quota Consumption for non-pro users (both guest IP and authenticated users)
    if not is_pro:
        quota_manager = get_quota_manager()
        user_identifier = current_user.get("id") or current_user.get("user_id") or "user"
        tier_name = "guest" if is_anonymous else (current_user.get("plan_tier") or "free")
        allowed, usage, remaining = quota_manager.check_and_consume_quota(
            identifier=str(user_identifier),
            is_pro=is_pro,
            daily_limit=daily_limit,
            tier=tier_name
        )

        if not allowed:
            tier_label = "guest" if is_anonymous else "free"
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Daily extraction quota limit reached for {tier_label} tier. Upgrade to Pro for unlimited extractions."
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

    dispatched_via = "background_tasks"
    if is_celery_broker_reachable():
        try:
            extract_video_task.apply_async(
                kwargs={
                    "job_id": job_id,
                    "video_url": canonical_url,
                    "url_hash": url_hash,
                    "user_id": str(current_user.get("id")),
                    "preferred_language": payload.preferred_language or "en",
                    "domain_hint": payload.domain_hint or "auto"
                },
                task_id=job_id
            )
            dispatched_via = "celery_redis_queue"
            logger.info("[%s] Dispatched extraction task to Celery worker pool", job_id)
        except Exception as exc:
            logger.warning("[%s] Failed to enqueue to Celery, falling back to BackgroundTasks: %s", job_id, exc)
            background_tasks.add_task(
                run_extraction_worker_sync,
                job_id=job_id,
                video_url=canonical_url,
                url_hash=url_hash,
                user_id=str(current_user.get("id")),
                preferred_language=payload.preferred_language or "en",
                domain_hint=payload.domain_hint or "auto"
            )
    else:
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
            "message": f"Extraction job enqueued successfully ({dispatched_via}).",
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
    Checks in-memory JobManager, Celery AsyncResult (if active), and Supabase persistence.
    """
    job_manager = get_job_manager()
    job = job_manager.get_job(job_id)

    if job and (job.get("status") == "completed" or job.get("status") == "failed"):
        return ExtractStatusResponse(
            job_id=job["job_id"],
            status=job["status"],
            stage=job.get("stage"),
            progress_percent=job.get("progress_percent", 0),
            data=job.get("data"),
            error=job.get("error")
        )

    # Check Celery task state if broker is reachable
    if is_celery_broker_reachable():
        try:
            from celery.result import AsyncResult
            res = AsyncResult(job_id, app=celery_app)
            if res.state == "SUCCESS":
                task_result = res.result or {}
                if isinstance(task_result, dict) and (task_result.get("status") == "failed" or task_result.get("error")):
                    return ExtractStatusResponse(
                        job_id=job_id,
                        status="failed",
                        stage=task_result.get("stage", "failed"),
                        progress_percent=100,
                        data=None,
                        error=task_result.get("error", "Extraction failed.")
                    )
                return ExtractStatusResponse(
                    job_id=job_id,
                    status="completed",
                    stage="completed",
                    progress_percent=100,
                    data=task_result.get("data") if isinstance(task_result, dict) else None,
                    error=None
                )
            elif res.state == "PROGRESS":
                info = res.info or {}
                status_val = info.get("status", "processing")
                if status_val == "failed" or info.get("error"):
                    return ExtractStatusResponse(
                        job_id=job_id,
                        status="failed",
                        stage=info.get("stage", "failed"),
                        progress_percent=100,
                        data=None,
                        error=info.get("error", "Extraction failed.")
                    )
                return ExtractStatusResponse(
                    job_id=job_id,
                    status=status_val,
                    stage=info.get("stage", "processing"),
                    progress_percent=info.get("progress_percent", 50),
                    data=info.get("data"),
                    error=None
                )
            elif res.state == "FAILURE":
                return ExtractStatusResponse(
                    job_id=job_id,
                    status="failed",
                    stage="failed",
                    progress_percent=100,
                    data=None,
                    error=str(res.result)
                )
        except Exception as celery_check_err:
            logger.debug("[%s] Celery status check skipped: %s", job_id, celery_check_err)

    if job:
        return ExtractStatusResponse(
            job_id=job["job_id"],
            status=job["status"],
            stage=job.get("stage"),
            progress_percent=job.get("progress_percent", 0),
            data=job.get("data"),
            error=job.get("error")
        )

    # Fallback: check if job is stored in Supabase extractions table by ID
    supabase = get_supabase_client()
    if supabase.is_configured():
        try:
            import uuid as uuid_mod
            valid_job_uuid = str(uuid_mod.UUID(str(job_id)))
            import requests
            url = f"{supabase.base_url}/rest/v1/extractions"
            params = {"id": f"eq.{valid_job_uuid}", "select": "*"}
            r = requests.get(url, headers=supabase._get_headers(use_service_role=True), params=params, timeout=4)
            if r.status_code == 200 and r.json():
                rec = r.json()[0]
                return ExtractStatusResponse(
                    job_id=valid_job_uuid,
                    status=rec.get("status", "completed"),
                    stage="completed",
                    progress_percent=100,
                    data=rec.get("structured_data") or rec.get("content_payload"),
                    error=None
                )
        except Exception:
            pass

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Extraction job '{job_id}' not found."
    )


MEDIA_CACHE_DIR = Path(tempfile.gettempdir()) / "universalpro_media_cache"
MEDIA_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def cleanup_ephemeral_media_cache(max_age_seconds: int = 1800):
    """Deletes cached stream files older than 30 minutes to satisfy AGENTS.md Rule 4."""
    try:
        now = time.time()
        for f in MEDIA_CACHE_DIR.glob("*.*"):
            if f.is_file() and (now - f.stat().st_mtime > max_age_seconds):
                try:
                    f.unlink(missing_ok=True)
                except Exception:
                    pass
    except Exception:
        pass


def _download_stream_video_sync(target_url: str, output_dir: Path) -> Optional[str]:
    """Synchronous media downloader executed in worker thread via asyncio.to_thread."""
    try:
        from backend.app.workers.media_downloader import download_worker_media
        success, result_path = download_worker_media(
            video_url=target_url,
            output_dir=output_dir
        )
        if success and result_path and os.path.exists(result_path):
            return result_path
    except Exception as dl_err:
        logger.warning("download_worker_media failed in stream_video: %s", dl_err)

    try:
        from downloader import get_video_from_url
        dl_success, dl_file = get_video_from_url(target_url)
        if dl_success and dl_file and os.path.exists(dl_file):
            return dl_file
    except Exception as dl_err2:
        logger.warning("get_video_from_url fallback failed: %s", dl_err2)

    return None


@router.get("/stream-video", summary="Stream Media File for In-Page Playback")
async def stream_video(
    request: Request,
    id: Optional[str] = Query(None),
    token: Optional[str] = Query(None),
    url: Optional[str] = Query(None)
):
    """
    Streams media content directly as HTML5 video to allow in-page playback.
    Requires signed token and extraction ID.
    Legacy ?url= query without token or passed as direct streaming parameter is rejected.
    Enforces per-client-IP rate limiting (429), strict 50MB byte ceiling, 90s duration cap,
    offloads blocking download to worker thread pool, and supports HTTP Range (206) requests.
    """
    # 1. Parameter presence & query hygiene validation
    if "url" in request.query_params or url is not None:
        raise HTTPException(
            status_code=400,
            detail="Client-supplied ?url= parameter is strictly prohibited on /stream-video. Streaming requires only 'id' and 'token' parameters."
        )

    if not token or not id:
        raise HTTPException(
            status_code=400,
            detail="Streaming requires signed token and id parameters."
        )

    # 2. Per-Client-IP Rate Limiting (P0 Security Directive)
    from backend.app.core.security import get_client_ip
    client_ip = get_client_ip(request)
    from backend.app.services.quota_service import get_quota_manager
    quota_manager = get_quota_manager()
    allowed, count = quota_manager.check_generic_rate_limit(f"stream:{client_ip}", limit=60, window_seconds=60)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded for video streaming (max 60 requests per minute)."
        )

    # 3. Initial Token Format & Basic Expiration Check (<exp>.<sig>)
    from backend.app.core.config import get_settings
    from backend.app.services.url_validator import verify_stream_token, validate_social_url

    secret_key = get_settings().SECRET_KEY
    if not secret_key:
        raise HTTPException(status_code=400, detail="Invalid or expired stream token.")

    if "." not in token:
        # Legacy raw token without expiration prefix is strictly rejected (UPA-1213)
        raise HTTPException(status_code=400, detail="Invalid or expired stream token.")

    parts = token.split(".", 1)
    if len(parts) != 2:
        raise HTTPException(status_code=400, detail="Invalid or expired stream token.")
    try:
        exp_val = int(parts[0])
        if exp_val < int(time.time()):
            raise HTTPException(status_code=400, detail="Invalid or expired stream token.")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid or expired stream token.")

    # 4. Server-Side Media URL Resolution (No Trust in Client URLs)
    target_url: Optional[str] = None
    job_manager = get_job_manager()
    job = job_manager.get_job(id)
    if job and job.get("video_url"):
        target_url = job["video_url"]

    if not target_url:
        supabase = get_supabase_client()
        if supabase.is_configured():
            cached = supabase.get_cached_extraction(id)
            if cached:
                target_url = cached.get("url") or (cached.get("content_payload") or {}).get("source_url") or (cached.get("structured_data") or {}).get("source_url")
            if not target_url:
                try:
                    import requests
                    db_url = f"{supabase.base_url}/rest/v1/extractions"
                    params = {"id": f"eq.{id}", "select": "*"}
                    r = requests.get(db_url, headers=supabase._get_headers(use_service_role=True), params=params, timeout=3)
                    if r.status_code == 200 and r.json():
                        rec = r.json()[0]
                        target_url = rec.get("url") or (rec.get("content_payload") or {}).get("source_url") or (rec.get("structured_data") or {}).get("source_url")
                except Exception:
                    pass

    if not target_url:
        raise HTTPException(status_code=404, detail="Media target URL not found for stream token.")

    # 5. Full Token Cryptographic Verification (Bound to ID and server-resolved URL)
    if not verify_stream_token(id, token, secret_key, media_url=target_url):
        raise HTTPException(status_code=400, detail="Invalid or expired stream token.")

    # 5. Shared SSRF Validation
    valid, err_msg, _, _ = validate_social_url(target_url)
    if not valid:
        raise HTTPException(status_code=400, detail=f"Target URL validation failed: {err_msg}")

    cleanup_ephemeral_media_cache()

    # 6. Non-Blocking Worker Thread Download / Retrieval
    video_file = await asyncio.to_thread(_download_stream_video_sync, target_url, MEDIA_CACHE_DIR)

    if not video_file or not os.path.exists(video_file):
        raise HTTPException(status_code=404, detail="Unable to stream media content.")

    file_size = os.path.getsize(video_file)
    max_stream_bytes = 50 * 1024 * 1024  # 50MB Cap (Rule 4)

    if file_size > max_stream_bytes:
        if os.path.exists(video_file):
            try:
                os.remove(video_file)
            except Exception:
                pass
        raise HTTPException(status_code=400, detail=f"Media file size ({file_size} bytes) exceeds maximum 50MB stream limit.")

    def stream_file_with_cleanup(filepath: str, start: int = 0, length: Optional[int] = None):
        """
        Streaming generator ensuring unskippable try...finally deterministic disk cleanup
        upon normal completion, streaming exception, or client disconnect (AGENTS.md Rule 4 & UPA-1213).
        """
        try:
            with open(filepath, "rb") as f:
                if start > 0:
                    f.seek(start)
                remaining = length if length is not None else float("inf")
                chunk_size = 64 * 1024
                while remaining > 0:
                    read_len = min(chunk_size, int(remaining)) if remaining != float("inf") else chunk_size
                    chunk = f.read(read_len)
                    if not chunk:
                        break
                    if remaining != float("inf"):
                        remaining -= len(chunk)
                    yield chunk
        finally:
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception:
                    pass

    # 7. HTTP Range Requests & 206 Partial Content (Smooth Seeking)
    range_header = request.headers.get("range")
    if range_header and range_header.startswith("bytes="):
        try:
            ranges = range_header.replace("bytes=", "").split("-")
            range_start = int(ranges[0]) if ranges[0] else 0
            range_end = int(ranges[1]) if len(ranges) > 1 and ranges[1] else file_size - 1
            if range_start < 0:
                range_start = max(0, file_size + range_start)
            range_end = min(range_end, file_size - 1)

            if range_start > range_end or range_start >= file_size:
                if os.path.exists(video_file):
                    try:
                        os.remove(video_file)
                    except Exception:
                        pass
                return Response(
                    status_code=416,
                    headers={"Content-Range": f"bytes */{file_size}"}
                )

            content_length = (range_end - range_start) + 1
            headers = {
                "Content-Range": f"bytes {range_start}-{range_end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(content_length),
                "Content-Type": "video/mp4",
            }
            return StreamingResponse(
                stream_file_with_cleanup(video_file, start=range_start, length=content_length),
                status_code=206,
                headers=headers,
                media_type="video/mp4"
            )
        except Exception as range_err:
            logger.warning("Error handling Range request, falling back to full stream: %s", range_err)

    # Standard 200 Streaming Response
    return StreamingResponse(
        stream_file_with_cleanup(video_file, start=0, length=file_size),
        status_code=200,
        media_type="video/mp4",
        headers={
            "Accept-Ranges": "bytes",
            "Content-Length": str(min(file_size, max_stream_bytes))
        }
    )


