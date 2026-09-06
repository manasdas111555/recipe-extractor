"""
Celery Extraction Tasks & Supabase Persistence (UPA-204 & UPA-205)
==================================================================
Distributed background worker tasks for video ingestion, multimodal AI inference,
monetization enrichment, and Supabase database synchronization.
Features:
- Primary multimodal AI routing (Gemini 2.5 Flash) with Whisper/Keyframe fallback
- Real-time progress updates through Celery task state
- 1-Click affiliate & 10-min quick-commerce link synthesis (UPA-301, UPA-302)
- Atomic Supabase persistence and user quota accounting (UPA-205)
"""

import os
import time
import logging
from typing import Optional, Dict, Any

from backend.app.workers.celery_app import celery_app
from backend.app.workers.media_downloader import managed_worker_download
from backend.app.services.affiliate_engine import get_affiliate_engine
from backend.app.core.supabase_client import get_supabase_client
from backend.app.services.job_manager import get_job_manager
import config

logger = logging.getLogger(__name__)


def execute_extraction_pipeline(
    job_id: str,
    video_url: str,
    url_hash: str,
    user_id: str,
    preferred_language: str = "en",
    domain_hint: str = "auto",
    custom_affiliate_tags: Optional[Dict[str, str]] = None,
    progress_callback: Optional[callable] = None
) -> Dict[str, Any]:
    """
    Unified extraction worker pipeline shared between Celery tasks and BackgroundTasks.
    Step 1: Download media stream (360p, max 50MB, proxy rotation, guaranteed disk cleanup)
    Step 2: Multimodal AI inference via Central Router (Gemini -> Mistral -> Groq/Whisper)
    Step 3: Enrich with multi-store affiliate & 10-minute quick-commerce cart deep links
    Step 4: Persist structured payload to Supabase database & update user daily quota
    """
    manager = get_job_manager()
    supabase = get_supabase_client()
    affiliate_engine = get_affiliate_engine()

    def update_progress(stage: str, percent: int, error: Optional[str] = None, data: Optional[dict] = None):
        manager.update_job(job_id, status="failed" if error else ("completed" if percent == 100 else "processing"), stage=stage, progress_percent=percent, data=data, error=error)
        if progress_callback:
            try:
                progress_callback(stage, percent, error, data)
            except Exception:
                pass

    update_progress("downloading_media", 20)

    # Context manager guarantees file is unlinked from disk upon exit
    with managed_worker_download(video_url) as (dl_success, dl_result):
        if not dl_success:
            err_msg = f"Media download failed: {dl_result}"
            logger.error("[%s] %s", job_id, err_msg)
            update_progress("failed", 100, error=err_msg)
            # Record failed extraction in Supabase
            try:
                supabase.save_extraction({
                    "id": job_id,
                    "user_id": user_id,
                    "url": video_url,
                    "url_hash": url_hash,
                    "status": "failed",
                    "error_message": err_msg
                })
            except Exception as db_err:
                logger.warning("[%s] Failed to record failure in Supabase: %s", job_id, db_err)
            return {"status": "failed", "error": err_msg}

        video_path = dl_result
        update_progress("multimodal_ai_inference", 55)

        # Step 2: Multimodal AI Reasoning via Central Router
        from ai_router import route_video_intelligence

        gemini_key = config.get_api_key()
        mistral_key = config.get_mistral_api_key()
        groq_key = config.get_groq_api_key()

        provider = "gemini" if gemini_key else ("mistral" if mistral_key else "groq")

        ai_res = route_video_intelligence(
            video_path=video_path,
            provider=provider,
            custom_gemini_key=gemini_key,
            custom_mistral_key=mistral_key,
            custom_groq_key=groq_key,
            extraction_mode=domain_hint or "auto",
            affiliate_tags=custom_affiliate_tags
        )

        ai_success = ai_res[0]
        txt_filepath = ai_res[1]
        recipe_text = ai_res[2]
        meta = ai_res[4] if len(ai_res) > 4 else {}

        if not ai_success:
            err_msg = f"Multimodal AI reasoning failed: {recipe_text}"
            logger.error("[%s] %s", job_id, err_msg)
            update_progress("failed", 100, error=err_msg)
            try:
                supabase.save_extraction({
                    "id": job_id,
                    "user_id": user_id,
                    "url": video_url,
                    "url_hash": url_hash,
                    "status": "failed",
                    "error_message": err_msg
                })
            except Exception:
                pass
            return {"status": "failed", "error": err_msg}

        update_progress("enriching_monetization_links", 80)

        # Step 3: Enrich with Affiliate & Quick Commerce Links (UPA-301, UPA-302)
        raw_products = meta.get("products", [])
        enriched_products = []
        for p in raw_products:
            enriched_products.append(affiliate_engine.enrich_product_links(p, user_affiliate_tags=custom_affiliate_tags))

        raw_resources = meta.get("resources", [])
        enriched_resources = []
        for r in raw_resources:
            enriched_resources.append(affiliate_engine.enrich_resource_links(r))

        meta["products"] = enriched_products
        meta["resources"] = enriched_resources

        content_payload = {
            "title": meta.get("title", "Extracted Content"),
            "category": meta.get("category", "RECIPE"),
            "category_name": meta.get("category_name", "Content"),
            "summary": meta.get("summary", ""),
            "full_text": recipe_text,
            "txt_filepath": txt_filepath,
            "products": enriched_products,
            "resources": enriched_resources,
            "timings": meta.get("timings", {}),
            "source_url": video_url,
            "url_hash": url_hash
        }

        # Step 4: Persist in Supabase PostgreSQL & Increment Daily Quota (UPA-205)
        update_progress("persisting_to_database", 90)
        try:
            supabase.save_extraction({
                "id": job_id,
                "user_id": user_id,
                "url": video_url,
                "url_hash": url_hash,
                "title": meta.get("title", "Extracted Content"),
                "domain_category": meta.get("category", "RECIPE"),
                "content_payload": content_payload,
                "status": "completed"
            })
            supabase.increment_daily_quota(user_id)
            logger.info("[%s] Saved extraction & updated quota for user %s", job_id, user_id)
        except Exception as db_exc:
            logger.warning("[%s] Supabase persistence notice: %s", job_id, db_exc)

        update_progress("completed", 100, data=content_payload)
        return {
            "status": "completed",
            "job_id": job_id,
            "data": content_payload
        }


@celery_app.task(bind=True, name="tasks.extract_video_task", max_retries=2, default_retry_delay=5)
def extract_video_task(
    self,
    job_id: str,
    video_url: str,
    url_hash: str,
    user_id: str,
    preferred_language: str = "en",
    domain_hint: str = "auto",
    custom_affiliate_tags: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Celery task wrapper updating distributed Celery state in Redis.
    """
    logger.info("Executing Celery extraction task %s for URL: %s", job_id, video_url)

    def on_progress(stage: str, percent: int, error: Optional[str] = None, data: Optional[dict] = None):
        self.update_state(
            state="PROGRESS" if percent < 100 else ("FAILURE" if error else "SUCCESS"),
            meta={
                "job_id": job_id,
                "stage": stage,
                "progress_percent": percent,
                "error": error,
                "data": data
            }
        )

    return execute_extraction_pipeline(
        job_id=job_id,
        video_url=video_url,
        url_hash=url_hash,
        user_id=user_id,
        preferred_language=preferred_language,
        domain_hint=domain_hint,
        custom_affiliate_tags=custom_affiliate_tags,
        progress_callback=on_progress
    )
