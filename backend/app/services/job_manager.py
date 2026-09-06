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
    domain_hint: str = "auto",
    custom_affiliate_tags: Optional[Dict[str, str]] = None
):
    """
    Synchronous worker pipeline executed in BackgroundTasks.
    Delegates to unified execute_extraction_pipeline to ensure identical
    360p limits, proxy rotation, disk cleanup, affiliate synthesis, and Supabase sync.
    """
    try:
        from backend.app.workers.tasks import execute_extraction_pipeline
        return execute_extraction_pipeline(
            job_id=job_id,
            video_url=video_url,
            url_hash=url_hash,
            user_id=user_id,
            preferred_language=preferred_language,
            domain_hint=domain_hint,
            custom_affiliate_tags=custom_affiliate_tags
        )
    except Exception as e:
        logger.exception(f"[Job {job_id}] Unhandled background worker exception: {e}")
        manager = get_job_manager()
        manager.update_job(
            job_id,
            status="failed",
            stage="failed",
            progress_percent=100,
            error=str(e)
        )

