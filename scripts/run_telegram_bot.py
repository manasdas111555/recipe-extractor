"""
Telegram Bot Long-Polling Runner
================================
Runs the Telegram Bot locally using long-polling (getUpdates).
Enables local development on Windows without needing ngrok or a public HTTPS URL.

Usage:
    python scripts/run_telegram_bot.py
"""

import os
import sys
import time
import logging
from pathlib import Path
import requests

# Ensure repository root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from backend.app.core.config import get_settings
from backend.app.services.telegram_bot import handle_telegram_update

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("telegram_runner")


def run_bot_polling():
    settings = get_settings()
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        logger.error("❌ TELEGRAM_BOT_TOKEN is not set in .env or environment variables.")
        logger.info("👉 Add TELEGRAM_BOT_TOKEN=your_bot_token to .env to use the Telegram Bot.")
        sys.exit(1)

    api_url = f"https://api.telegram.org/bot{token}"

    # 1. Verify Bot Identity
    try:
        me_resp = requests.get(f"{api_url}/getMe", timeout=10).json()
        if not me_resp.get("ok"):
            logger.error(f"❌ Failed to connect to Telegram: {me_resp.get('description')}")
            sys.exit(1)
        bot_info = me_resp["result"]
        logger.info(f"🤖 Connected as @{bot_info.get('username')} ({bot_info.get('first_name')})")
    except Exception as e:
        logger.error(f"❌ Network error connecting to Telegram API: {e}")
        sys.exit(1)

    # 2. Clear webhook so long-polling works smoothly
    try:
        requests.post(f"{api_url}/deleteWebhook", json={"drop_pending_updates": False}, timeout=10)
        logger.info("✅ Cleared any active webhooks. Switching to long-polling mode.")
    except Exception as e:
        logger.warning(f"⚠️ Warning deleting webhook: {e}")

    logger.info("🚀 Telegram Bot is running! Waiting for reels and videos... (Press Ctrl+C to stop)")

    offset = None
    while True:
        try:
            params = {"timeout": 20}
            if offset is not None:
                params["offset"] = offset

            resp = requests.get(f"{api_url}/getUpdates", params=params, timeout=25)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("ok"):
                    updates = data.get("result", [])
                    for update in updates:
                        update_id = update.get("update_id")
                        offset = update_id + 1
                        logger.info(f"📨 Processing incoming update ID: {update_id}")
                        handle_telegram_update(update, background_tasks=None)
            elif resp.status_code == 409:
                logger.warning("⚠️ Conflict: Another instance of the bot is running. Waiting 5s...")
                time.sleep(5)
            else:
                logger.error(f"⚠️ getUpdates returned HTTP {resp.status_code}: {resp.text}")
                time.sleep(3)
        except KeyboardInterrupt:
            logger.info("\n🛑 Telegram Bot stopped by user.")
            break
        except Exception as e:
            logger.error(f"⚠️ Polling loop error: {e}")
            time.sleep(3)


if __name__ == "__main__":
    run_bot_polling()
