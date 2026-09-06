"""
WhatsApp Cloud API Integration Service (UPA-402)
================================================
Implements Meta's official WhatsApp Business Cloud API webhook verification,
incoming message parsing, and asynchronous message delivery.
"""

import re
import logging
from typing import Optional, Dict, Any, Tuple
import requests

from backend.app.core.config import get_settings
from backend.app.services.job_manager import run_extraction_worker_sync

logger = logging.getLogger(__name__)

def format_whatsapp_cloud_message(
    title: str,
    summary: str,
    ingredients: list = None,
    steps: list = None,
    source_url: str = None,
    products: list = None
) -> str:
    """Formats structured extraction intelligence for WhatsApp Cloud API message body."""
    lines = [f"⚡ *{title.strip()}*\n"]
    if summary:
        clean_sum = summary.strip().split("\n\n")[0]
        lines.append(f"📋 *Summary:*\n{clean_sum}\n")
    if ingredients and len(ingredients) > 0:
        lines.append("🛒 *Ingredients / Key Items:*")
        for ing in ingredients[:8]:
            lines.append(f"• {ing}")
        lines.append("")
    if steps and len(steps) > 0:
        lines.append("📝 *Steps:*")
        for idx, s in enumerate(steps[:6], 1):
            lines.append(f"*{idx}.* {s}")
        lines.append("")
    if products and len(products) > 0:
        lines.append("🛍️ *1-Click Buy Links:*")
        for p in products[:3]:
            url = p.get("amazon_url") or p.get("blinkit_url") or p.get("flipkart_url")
            if url:
                lines.append(f"• {p['name']}: {url}")
        lines.append("")
    if source_url:
        lines.append(f"🔗 *Source:* {source_url}\n")
    lines.append("🚀 _Universal Pro AI · Instant Extraction_")
    return "\n".join(lines).strip()


VIDEO_URL_PATTERN = re.compile(
    r'(https?://(?:www\.)?(?:instagram\.com/(?:reel|reels|p)/[a-zA-Z0-9_-]+/?|'
    r'youtube\.com/(?:watch\?v=[a-zA-Z0-9_-]+|shorts/[a-zA-Z0-9_-]+/?)|'
    r'youtu\.be/[a-zA-Z0-9_-]+/?|'
    r'tiktok\.com/@[a-zA-Z0-9._-]+/video/\d+/?|'
    r'vt\.tiktok\.com/[a-zA-Z0-9]+/?))',
    re.IGNORECASE
)


def verify_whatsapp_webhook(mode: Optional[str], token: Optional[str], challenge: Optional[str]) -> Optional[str]:
    """
    Validates Meta WhatsApp Webhook handshake.
    Returns the challenge string if valid, otherwise None.
    """
    settings = get_settings()
    expected_token = settings.WHATSAPP_VERIFY_TOKEN or "universal_pro_verify_token"

    if mode == "subscribe" and token == expected_token and challenge:
        logger.info("[WhatsApp Cloud] Webhook verification handshake successful.")
        return challenge

    logger.warning("[WhatsApp Cloud] Webhook verification failed. Token mismatch.")
    return None


def extract_whatsapp_message(payload: Dict[str, Any]) -> Optional[Tuple[str, str, str]]:
    """
    Parses Meta WhatsApp Webhook payload.
    Returns (sender_phone, message_text, message_id) or None.
    """
    try:
        entries = payload.get("entry", [])
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                messages = value.get("messages", [])
                for msg in messages:
                    sender = msg.get("from")
                    msg_id = msg.get("id")
                    msg_type = msg.get("type")

                    text = ""
                    if msg_type == "text":
                        text = msg.get("text", {}).get("body", "")
                    elif msg_type == "interactive":
                        text = msg.get("interactive", {}).get("button_reply", {}).get("title", "")

                    if sender and text:
                        return sender, text.strip(), msg_id
    except Exception as e:
        logger.error(f"[WhatsApp Cloud] Error parsing incoming webhook: {e}")
    return None


def send_whatsapp_cloud_message(to_phone: str, text: str) -> bool:
    """
    Sends a text message using Meta's WhatsApp Cloud API.
    Endpoint: https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages
    """
    settings = get_settings()
    phone_id = settings.WHATSAPP_PHONE_NUMBER_ID
    access_token = settings.WHATSAPP_ACCESS_TOKEN

    if not phone_id or not access_token:
        logger.warning("[WhatsApp Cloud] WhatsApp credentials not configured. Message skipped.")
        return False

    url = f"https://graph.facebook.com/v19.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_phone,
        "type": "text",
        "text": {
            "preview_url": True,
            "body": text[:4096]  # Meta text body ceiling
        }
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=8)
        if resp.status_code in [200, 201]:
            logger.info(f"[WhatsApp Cloud] Message successfully dispatched to {to_phone}")
            return True
        else:
            logger.error(f"[WhatsApp Cloud] API error {resp.status_code}: {resp.text}")
            return False
    except Exception as e:
        logger.error(f"[WhatsApp Cloud] Network failure calling Graph API: {e}")
        return False


def process_whatsapp_video_extraction(sender_phone: str, video_url: str):
    """Background extraction runner that replies back to user on WhatsApp."""
    send_whatsapp_cloud_message(
        to_phone=sender_phone,
        text=f"⏳ *Universal Pro AI:* Analyzing your video...\nExtracting steps, ingredient checklist, and 1-click buy links."
    )

    try:
        job = run_extraction_worker_sync(
            video_url=video_url,
            preferred_language="en",
            domain_hint="auto"
        )

        if job.get("status") == "completed" and job.get("result_data"):
            result_data = job["result_data"]
            title = result_data.get("title", "Structured Notes")
            summary = result_data.get("summary", "")
            ingredients = result_data.get("ingredients", [])
            steps = result_data.get("steps", [])
            products = result_data.get("products", [])

            # Use our self-contained WhatsApp Cloud formatter
            formatted_text = format_whatsapp_cloud_message(
                title=title,
                summary=summary,
                ingredients=ingredients,
                steps=steps,
                source_url=video_url,
                products=products
            )

            send_whatsapp_cloud_message(
                to_phone=sender_phone,
                text=formatted_text
            )
        else:
            err_msg = job.get("error_message") or "Could not extract video content."
            send_whatsapp_cloud_message(
                to_phone=sender_phone,
                text=f"❌ *Extraction Failed:*\n{err_msg}\nPlease verify the video is public."
            )
    except Exception as e:
        logger.error(f"[WhatsApp Cloud] Extraction worker error: {e}")
        send_whatsapp_cloud_message(
            to_phone=sender_phone,
            text=f"❌ *Server Error:* Unable to complete extraction ({str(e)})."
        )


def handle_whatsapp_incoming(payload: Dict[str, Any], background_tasks = None) -> Dict[str, Any]:
    """
    Main webhook handler for incoming WhatsApp Cloud API events.
    Must acknowledge to Meta within 2000ms.
    """
    parsed = extract_whatsapp_message(payload)
    if not parsed:
        return {"status": "ignored", "reason": "non_message_event"}

    sender_phone, text, msg_id = parsed

    # Check for social media video URL
    match = VIDEO_URL_PATTERN.search(text)
    if not match:
        welcome_msg = (
            "👋 *Welcome to Universal Pro AI on WhatsApp!*\n\n"
            "Simply send or forward any *Instagram Reel*, *YouTube Short*, or *TikTok* link to receive:\n\n"
            "📋 Structured recipes & workout steps\n"
            "🛒 1-Click Amazon, Blinkit, and Flipkart buy links\n"
            "⚡ Turnaround in <3 seconds!"
        )
        send_whatsapp_cloud_message(sender_phone, welcome_msg)
        return {"status": "ok", "action": "welcome_sent"}

    video_url = match.group(1)

    # Dispatch extraction asynchronously
    if background_tasks:
        background_tasks.add_task(process_whatsapp_video_extraction, sender_phone, video_url)
    else:
        process_whatsapp_video_extraction(sender_phone, video_url)

    return {"status": "enqueued", "sender": sender_phone, "video_url": video_url}
