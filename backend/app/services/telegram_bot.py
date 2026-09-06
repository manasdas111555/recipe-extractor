"""
Telegram Ingestion Bot Service (UPA-401)
========================================
Parses incoming Telegram messages, detects social media video links,
dispatches video extraction, and responds with formatted notes & inline store buttons.
"""

import re
import logging
from typing import Optional, Dict, Any, List, Tuple
import requests

from backend.app.core.config import get_settings
from backend.app.services.job_manager import run_extraction_worker_sync
from backend.app.core.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

# Regex for detecting supported video URLs
VIDEO_URL_PATTERN = re.compile(
    r'(https?://(?:www\.)?(?:instagram\.com/(?:reel|reels|p)/[a-zA-Z0-9_-]+/?|'
    r'youtube\.com/(?:watch\?v=[a-zA-Z0-9_-]+|shorts/[a-zA-Z0-9_-]+/?)|'
    r'youtu\.be/[a-zA-Z0-9_-]+/?|'
    r'tiktok\.com/@[a-zA-Z0-9._-]+/video/\d+/?|'
    r'vt\.tiktok\.com/[a-zA-Z0-9]+/?))',
    re.IGNORECASE
)


def extract_url_from_text(text: str) -> Optional[str]:
    """Finds the first valid social media video URL in text."""
    if not text:
        return None
    match = VIDEO_URL_PATTERN.search(text)
    return match.group(1) if match else None


def format_telegram_markdown(result: Dict[str, Any], canonical_url: str) -> Tuple[str, List[List[Dict[str, str]]]]:
    """
    Formats extraction intelligence into readable Telegram Markdown
    and constructs an interactive inline button keyboard.
    """
    title = result.get("recipe_title") or result.get("title", "Extracted Intelligence")
    category = result.get("category_name", "Content Summary")
    summary = result.get("summary", "").strip()
    ingredients = result.get("ingredients", [])
    steps = result.get("steps") or result.get("instructions", [])
    products = result.get("products", [])

    msg_lines = [
        f"⚡ *{title}*",
        f"🏷️ _{category}_\n",
    ]

    if summary:
        clean_sum = summary.split("\n\n")[0]
        msg_lines.append(f"📋 *Summary:*\n{clean_sum}\n")

    if ingredients and len(ingredients) > 0:
        msg_lines.append("🛒 *Ingredients / Key Items:*")
        for ing in ingredients[:8]:
            msg_lines.append(f"  • {ing}")
        if len(ingredients) > 8:
            msg_lines.append(f"  _...and {len(ingredients) - 8} more_")
        msg_lines.append("")

    if steps and len(steps) > 0:
        msg_lines.append("📝 *Quick Steps:*")
        for idx, step in enumerate(steps[:5], 1):
            msg_lines.append(f"*{idx}.* {step}")
        if len(steps) > 5:
            msg_lines.append(f"_...and {len(steps) - 5} more steps in web app_")
        msg_lines.append("")

    msg_lines.append("🚀 _Powered by Universal Pro AI_")
    text_content = "\n".join(msg_lines)

    # Construct Inline Keyboard Buttons (PO Directive: Wrapped via /api/v1/affiliate/redirect)
    inline_keyboard = []

    # 1. Product Buy Link (Routed via /api/v1/affiliate/redirect for telemetry)
    primary_buy_url = None
    first_prod_name = "Product"
    merchant = "amazon"
    if products and len(products) > 0:
        first_prod = products[0]
        first_prod_name = first_prod.get("name", "Product")
        if first_prod.get("amazon_url"):
            primary_buy_url = first_prod["amazon_url"]
            merchant = "amazon"
        elif first_prod.get("blinkit_url"):
            primary_buy_url = first_prod["blinkit_url"]
            merchant = "blinkit"
        elif first_prod.get("flipkart_url"):
            primary_buy_url = first_prod["flipkart_url"]
            merchant = "flipkart"
        elif first_prod.get("zepto_url"):
            primary_buy_url = first_prod["zepto_url"]
            merchant = "zepto"
        elif first_prod.get("buy_url"):
            primary_buy_url = first_prod["buy_url"]
            merchant = "amazon" if "amazon" in primary_buy_url else "external"

    action_row = []
    if primary_buy_url:
        import urllib.parse
        from backend.app.core.config import get_settings
        settings = get_settings()
        encoded_dest = urllib.parse.quote_plus(primary_buy_url)
        encoded_item = urllib.parse.quote_plus(first_prod_name)
        redirect_wrapped_url = f"/api/v1/affiliate/redirect?url={encoded_dest}&merchant={merchant}&item_name={encoded_item}"
        
        action_row.append({
            "text": "🛒 Buy Ingredients (1-Click)",
            "url": redirect_wrapped_url
        })

    action_row.append({
        "text": "🔗 Source Video",
        "url": canonical_url
    })

    inline_keyboard.append(action_row)

    # 2. Web View Button (PO Directive: Option A - Bridge into Web App)
    web_app_url = "https://universalpro-stage.streamlit.app"
    inline_keyboard.append([{
        "text": "🌐 View Full Interactive Recipe",
        "url": web_app_url
    }])

    return text_content, inline_keyboard


def send_telegram_message(
    chat_id: int,
    text: str,
    reply_markup: Optional[Dict[str, Any]] = None,
    parse_mode: str = "Markdown"
) -> bool:
    """Dispatches a message to Telegram using Bot API."""
    settings = get_settings()
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        logger.warning("[Telegram] TELEGRAM_BOT_TOKEN not configured. Skipping send.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        resp = requests.post(url, json=payload, timeout=8)
        if resp.status_code == 200:
            return True
        else:
            logger.error(f"[Telegram] Failed to send message: {resp.status_code} {resp.text}")
            # Fallback without parse_mode if markdown parsing fails
            if "can't parse entities" in resp.text.lower():
                payload.pop("parse_mode", None)
                requests.post(url, json=payload, timeout=8)
            return False
    except Exception as e:
        logger.error(f"[Telegram] Network error sending message: {e}")
        return False


def process_telegram_video_extraction(chat_id: int, video_url: str):
    """Background worker executing video extraction and replying on Telegram."""
    send_telegram_message(
        chat_id=chat_id,
        text=f"⏳ *Analyzing video:* `{video_url}`\nProcessing audio, visual steps, and shoppable ingredients with Universal Pro AI..."
    )

    try:
        job = run_extraction_worker_sync(
            video_url=video_url,
            preferred_language="en",
            domain_hint="auto"
        )

        if job.get("status") == "completed" and job.get("result_data"):
            result_data = job["result_data"]
            markdown_text, inline_keyboard = format_telegram_markdown(result_data, video_url)
            reply_markup = {"inline_keyboard": inline_keyboard} if inline_keyboard else None

            send_telegram_message(
                chat_id=chat_id,
                text=markdown_text,
                reply_markup=reply_markup
            )
        else:
            err_msg = job.get("error_message") or "Extraction could not be completed. Please check if the video is public and accessible."
            send_telegram_message(
                chat_id=chat_id,
                text=f"❌ *Extraction Failed:*\n{err_msg}"
            )
    except Exception as e:
        logger.error(f"[Telegram] Error processing extraction for chat {chat_id}: {e}")
        send_telegram_message(
            chat_id=chat_id,
            text=f"❌ *Error:* Unexpected server issue during extraction ({str(e)})."
        )


def handle_telegram_update(update: Dict[str, Any], background_tasks = None) -> Dict[str, Any]:
    """
    Main controller for incoming Telegram webhook updates.
    Handles /start, /help, and video links.
    """
    message = update.get("message") or update.get("edited_message")
    if not message:
        return {"status": "ignored", "reason": "no_message"}

    chat_id = message.get("chat", {}).get("id")
    text = (message.get("text") or message.get("caption") or "").strip()

    if not chat_id:
        return {"status": "ignored", "reason": "no_chat_id"}

    # Handle /start command
    if text.startswith("/start"):
        welcome_text = (
            "👋 *Welcome to Universal Pro AI Bot!*\n\n"
            "Send or share any *Instagram Reel*, *YouTube Short*, or *TikTok video* link here.\n\n"
            "✨ *What you get in <3 seconds:*\n"
            "• Clean structured recipe ingredients & steps\n"
            "• Workout exercise routines & reps\n"
            "• 1-Click Amazon, Blinkit, and Flipkart buy links\n"
            "• Complete actionable notes"
        )
        send_telegram_message(chat_id, welcome_text)
        return {"status": "ok", "action": "welcome"}

    # Handle /help command
    if text.startswith("/help"):
        help_text = (
            "ℹ️ *How to use Universal Pro AI Bot:*\n\n"
            "1. Copy any video link from Instagram, YouTube, or TikTok.\n"
            "2. Paste it directly into this chat.\n"
            "3. Receive structured steps and shoppable buy links automatically!"
        )
        send_telegram_message(chat_id, help_text)
        return {"status": "ok", "action": "help"}

    # Detect video link
    video_url = extract_url_from_text(text)
    if not video_url:
        send_telegram_message(
            chat_id,
            "💡 Please send a valid *Instagram Reel*, *YouTube Short*, or *TikTok* link."
        )
        return {"status": "ignored", "reason": "no_valid_url"}

    # Dispatch extraction asynchronously
    if background_tasks:
        background_tasks.add_task(process_telegram_video_extraction, chat_id, video_url)
    else:
        # Direct execution fallback
        process_telegram_video_extraction(chat_id, video_url)

    return {"status": "enqueued", "chat_id": chat_id, "video_url": video_url}
