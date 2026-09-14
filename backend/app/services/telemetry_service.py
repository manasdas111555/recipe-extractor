"""
Beta Telemetry & Silent Observability Service
=============================================
UPA-903: Dispatches instant alert notifications to developer private Telegram chat
and records passive telemetry into Supabase `beta_telemetry_feed`.
"""

import os
import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_TELEGRAM_CHAT_ID = os.getenv("ADMIN_TELEGRAM_CHAT_ID")


def send_admin_telemetry_alert(event_type: str, url: str, detail: str) -> bool:
    """
    Sends immediate alerts to private Telegram admin chat when extraction failures
    or negative user feedback occurs.
    """
    token = TELEGRAM_BOT_TOKEN or os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = ADMIN_TELEGRAM_CHAT_ID or os.getenv("ADMIN_TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logger.debug("[Telemetry] Telegram admin credentials not configured. Skipping alert.")
        return False

    icon = "🚨 FAILURE" if event_type == "failed" else "⚠️ NEGATIVE FEEDBACK"
    message = (
        f"{icon}\n"
        f"🔗 **URL**: {url}\n"
        f"📝 **Detail**: {detail}\n"
        f"⏱️ **Time**: Just now"
    )

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True,
            },
            timeout=3.0,
        )
        return response.status_code == 200
    except Exception as e:
        logger.warning(f"[Telemetry] Failed to dispatch admin alert: {e}")
        return False
