"""
Webhooks API Router (UPA-401 & UPA-402)
=======================================
Public endpoints for receiving chat bot events:
- Meta WhatsApp Cloud API (Verification + Message Receiver)
- Telegram Bot Webhooks
"""

import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, Request, Query, HTTPException, BackgroundTasks, status
from fastapi.responses import PlainTextResponse

from backend.app.core.config import get_settings
from backend.app.services.whatsapp_cloud import verify_whatsapp_webhook, handle_whatsapp_incoming
from backend.app.services.telegram_bot import handle_telegram_update

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.get("/whatsapp", summary="Meta WhatsApp Webhook Verification Handshake")
async def verify_whatsapp(
    hub_mode: Optional[str] = Query(None, alias="hub.mode"),
    hub_verify_token: Optional[str] = Query(None, alias="hub.verify_token"),
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge")
):
    """
    Handles Meta's initial webhook verification handshake.
    Must return the hub.challenge integer/string as plain text.
    """
    challenge = verify_whatsapp_webhook(
        mode=hub_mode,
        token=hub_verify_token,
        challenge=hub_challenge
    )

    if challenge is not None:
        return PlainTextResponse(content=challenge, status_code=200)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Verification failed. Invalid mode or verify token."
    )


@router.post("/whatsapp", summary="Meta WhatsApp Incoming Message Receiver")
async def receive_whatsapp_event(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Receives incoming WhatsApp Cloud API webhooks.
    Acknowledges within 2000ms with HTTP 200 to satisfy Meta webhook SLA,
    while processing video extraction asynchronously in the background.
    """
    try:
        payload = await request.json()
    except Exception:
        return {"status": "ignored", "error": "invalid_json"}

    result = handle_whatsapp_incoming(payload, background_tasks=background_tasks)
    return {"status": "received", "result": result}


@router.post("/telegram", summary="Telegram Bot Webhook Receiver")
async def receive_telegram_event(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Receives incoming Telegram updates from Telegram Bot API webhook.
    Dispatches video extraction in background tasks.
    """
    try:
        update = await request.json()
    except Exception:
        return {"status": "ignored", "error": "invalid_json"}

    result = handle_telegram_update(update, background_tasks=background_tasks)
    return {"status": "ok", "result": result}


@router.get("/health", summary="Chat Webhooks Integration Health")
def webhooks_health():
    """Returns configuration status for Telegram and WhatsApp Cloud API."""
    settings = get_settings()
    return {
        "status": "healthy",
        "telegram": {
            "configured": bool(settings.TELEGRAM_BOT_TOKEN),
            "webhook_secret_set": bool(settings.TELEGRAM_WEBHOOK_SECRET)
        },
        "whatsapp": {
            "configured": bool(settings.WHATSAPP_PHONE_NUMBER_ID and settings.WHATSAPP_ACCESS_TOKEN),
            "verify_token_set": bool(settings.WHATSAPP_VERIFY_TOKEN)
        }
    }
