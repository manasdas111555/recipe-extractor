"""
Universal Pro AI — Cloud App Keep-Alive & Wakeup Automation
============================================================
Pings Streamlit Community Cloud instances (Production & Staging)
to prevent automatic hibernation due to inactivity.
Can be executed locally or automatically via GitHub Actions cron.
"""

import sys
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("keep_alive")

URLS = [
    {
        "name": "Production App",
        "url": "https://manas-recipe-extractor.streamlit.app/"
    },
    {
        "name": "Staging App",
        "url": "https://universalpro-stage.streamlit.app/"
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}


def ping_and_wake(app_info: dict) -> bool:
    name = app_info["name"]
    url = app_info["url"]
    logger.info(f"Pinging {name} at {url}...")

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        status = response.status_code
        body_text = response.text

        is_sleeping = "This app has gone to sleep" in body_text or "Zzzz" in body_text

        if is_sleeping:
            logger.warning(f"⚠️  {name} is currently ASLEEP. Sending wake request...")
            # Pinging the health and websocket endpoints triggers Streamlit Cloud auto-wake
            requests.get(f"{url}_stcore/health", headers=HEADERS, timeout=15)
            requests.post(f"{url}_stcore/stream", headers=HEADERS, timeout=15)
            logger.info(f"✅ Wake request dispatched for {name}. It will spin up shortly.")
            return False
        else:
            logger.info(f"🟢 {name} is AWAKE and healthy (HTTP {status}). Inactivity timer refreshed!")
            return True

    except Exception as e:
        logger.error(f"❌ Failed to reach {name} ({url}): {e}")
        return False


def main():
    logger.info("=" * 60)
    logger.info("Universal Pro AI — Cloud Keep-Alive Routine")
    logger.info("=" * 60)

    all_awake = True
    for app_info in URLS:
        awake = ping_and_wake(app_info)
        if not awake:
            all_awake = False

    logger.info("=" * 60)
    if all_awake:
        logger.info("All applications are active and awake.")
    else:
        logger.info("Wake-up triggers sent to sleeping applications.")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
