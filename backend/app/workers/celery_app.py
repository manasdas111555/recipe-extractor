"""
Celery Worker Application Instance (UPA-201)
============================================
Initializes distributed task queue backed by Upstash Redis or local Redis broker.
Configures JSON serialization, task tracking, and hard 180s execution limits.
Includes broker health check utility for dual-mode API gateway dispatching.
"""

import logging
from typing import Optional
from celery import Celery
from backend.app.core.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()
broker_url = settings.CELERY_BROKER_URL or settings.REDIS_URL
backend_url = settings.CELERY_RESULT_BACKEND or settings.REDIS_URL

celery_app = Celery(
    "universal_pro_worker",
    broker=broker_url,
    backend=backend_url,
    include=["backend.app.workers.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=settings.CELERY_TASK_TIMEOUT,
    task_soft_time_limit=max(10, settings.CELERY_TASK_TIMEOUT - 15),
    result_expires=86400,  # 24 hours
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)


def is_celery_broker_reachable(timeout_seconds: float = 1.0) -> bool:
    """
    Fast, non-blocking check to determine if the Redis broker is reachable.
    Enables API gateway to gracefully fallback to in-memory BackgroundTasks if Redis is offline.
    """
    try:
        import redis
        client = redis.from_url(broker_url, socket_connect_timeout=timeout_seconds, socket_timeout=timeout_seconds)
        return client.ping()
    except Exception as exc:
        logger.debug("Celery Redis broker unreachable (%s): %s", broker_url, exc)
        return False
