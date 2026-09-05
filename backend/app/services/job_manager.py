"""
Background Job Manager Service
==============================
Thread-safe in-memory job registry and task lifecycle executor for extraction jobs.
Tracks real-time progress percentages, stages, and outputs.
"""

import time
import logging
import threading
from typing import Optional, Dict, Any
from pathlib import Path

from backend.app.core.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

class JobManager:
    """Thread-safe registry for asynchronous extraction jobs."""

    def __init__(self):
        self._jobs: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def create_job(self, job_id: str, video_url: str, url_hash: str, user_id: str) -> Dict[str, Any]:
        """Registers a new job in queued status."""
        now = time.time()
        job = {
            "job_id": job_id,
            "status": "queued",
            "stage": "enqueued",
            "progress_percent": 5,
            "video_url": video_url,
            "url_hash": url_hash,
            "user_id": user_id,
            "created_at": now,
            "updated_at": now,
            "data": None,
            "error": None
        }
        with self._lock:
            self._jobs[job_id] = job
        return job

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves current job metadata by ID."""
        with self._lock:
            job = self._jobs.get(job_id)
            return dict(job) if job else None

    def update_job(
        self,
        job_id: str,
        status: Optional[str] = None,
        stage: Optional[str] = None,
        progress_percent: Optional[int] = None,
        data: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Updates job status, progress, stage, data or error."""
        with self._lock:
            if job_id not in self._jobs:
                return None
            job = self._jobs[job_id]
            if status is not None:
                job["status"] = status
            if stage is not None:
                job["stage"] = stage
            if progress_percent is not None:
                job["progress_percent"] = progress_percent
            if data is not None:
                job["data"] = data
            if error is not None:
                job["error"] = error
            job["updated_at"] = time.time()
            return dict(job)


_job_manager: Optional[JobManager] = None

def get_job_manager() -> JobManager:
    """Singleton getter for JobManager."""
    global _job_manager
    if _job_manager is None:
        _job_manager = JobManager()
    return _job_manager


def run_extraction_worker_sync(
    job_id: str,
    video_url: str,
    url_hash: str,
    user_id: str,
    preferred_language: str = "en",
    domain_hint: str = "auto"
):
    """
    Synchronous worker pipeline executed in BackgroundTasks.
    Stage 1: Downloading video stream and verifying duration.
    Stage 2: Multimodal neural vision and speech inference.
    Stage 3: Caching result in Supabase PostgreSQL extractions table.
    """
    manager = get_job_manager()
    supabase = get_supabase_client()

    try:
        # Step 1: Download Media
        manager.update_job(
            job_id,
            status="downloading",
            stage="downloading_media",
            progress_percent=25
        )

        from downloader import get_video_from_url
        dl_success, dl_result = get_video_from_url(video_url, preferred_engine="ytdlp")

        if not dl_success:
            manager.update_job(
                job_id,
                status="failed",
                stage="failed",
                progress_percent=100,
                error=f"Ingestion failed: {dl_result}"
            )
            return

        # Step 2: AI Reasoning & Slicing
        manager.update_job(
            job_id,
            status="processing",
            stage="multimodal_ai_inference",
            progress_percent=60
        )

        from ai_router import route_video_intelligence
        import config
        gemini_key = config.get_api_key()

        def on_status_update(msg: str):
            logger.info(f"[Job {job_id}] AI Status: {msg}")

        success, txt_path, text_output, final_video, meta = route_video_intelligence(
            video_path=dl_result,
            custom_gemini_key=gemini_key,
            status_callback=on_status_update,
            extraction_mode=domain_hint
        )

        if not success:
            manager.update_job(
                job_id,
                status="failed",
                stage="failed",
                progress_percent=100,
                error=f"AI extraction failed: {text_output}"
            )
            return

        # Step 3: Package Payload & Save to Supabase
        content_payload = {
            "title": meta.get("title", Path(txt_path).stem.replace("_", " ")),
            "domain": meta.get("domain", domain_hint),
            "language": preferred_language,
            "raw_text": text_output,
            "meta": meta,
            "file_url": str(txt_path)
        }

        # Attempt caching in Supabase
        db_record = {
            "user_id": None if user_id.startswith("guest_") else user_id,
            "source_url": video_url,
            "url_hash": url_hash,
            "domain": meta.get("domain", domain_hint),
            "status": "completed",
            "content_payload": content_payload
        }
        supabase.insert_extraction(db_record)
        supabase.increment_user_quota(user_id)

        # Mark job completed
        manager.update_job(
            job_id,
            status="completed",
            stage="completed",
            progress_percent=100,
            data=content_payload
        )
        logger.info(f"[Job {job_id}] Successfully extracted intelligence.")

    except Exception as e:
        logger.exception(f"[Job {job_id}] Unhandled worker exception: {e}")
        manager.update_job(
            job_id,
            status="failed",
            stage="failed",
            progress_percent=100,
            error=str(e)
        )
