#!/usr/bin/env python3
"""
WhatsApp Bot Interactive Test Utility (Universal Pro AI)
=========================================================
Allows local developers and QA to test the WhatsApp Cloud API webhook
without needing a Meta Developer account or ngrok tunnel.

Usage:
  python scripts/test_whatsapp_bot.py
  python scripts/test_whatsapp_bot.py --url "https://www.instagram.com/reel/C1234567890/"
  python scripts/test_whatsapp_bot.py --greet
"""

import sys
import argparse
import requests
import json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_URL = "http://127.0.0.1:8000"

def test_webhook_handshake():
    print("\n👉 Step 1: Testing Meta Webhook Verification Handshake (GET)...")
    url = f"{BASE_URL}/api/v1/webhooks/whatsapp"
    params = {
        "hub.mode": "subscribe",
        "hub.verify_token": "universal_pro_verify_token",
        "hub.challenge": "CHALLENGE_ACCEPTED_777"
    }
    try:
        resp = requests.get(url, params=params, timeout=5)
        if resp.status_code == 200 and resp.text == "CHALLENGE_ACCEPTED_777":
            print("  ✅ PASS: Handshake verified! Meta would accept this endpoint.")
        else:
            print(f"  ❌ FAIL: Status {resp.status_code}, body: {resp.text}")
    except Exception as e:
        print(f"  ❌ ERROR: Could not connect to {BASE_URL}. Ensure FastAPI is running on port 8000.\n     Error: {e}")

def simulate_incoming_message(phone: str, message_body: str):
    print(f"\n👉 Step 2: Simulating Incoming WhatsApp Message from {phone}...")
    print(f"   Message content: \"{message_body}\"")
    
    post_url = f"{BASE_URL}/api/v1/webhooks/whatsapp"
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {
                        "display_phone_number": "1555001122",
                        "phone_number_id": "10001"
                    },
                    "messages": [{
                        "from": phone,
                        "id": "wamid.TEST_MSG_999",
                        "timestamp": "1725600000",
                        "type": "text",
                        "text": {"body": message_body}
                    }]
                },
                "field": "messages"
            }]
        }]
    }

    try:
        resp = requests.post(post_url, json=payload, timeout=5)
        print(f"  HTTP Response Code: {resp.status_code} (Meta SLA: < 2000ms)")
        print(f"  Server Response JSON: {json.dumps(resp.json(), indent=2)}")
    except Exception as e:
        print(f"  ❌ ERROR sending payload: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Universal Pro AI WhatsApp Bot")
    parser.add_argument("--url", help="Social video URL (Instagram, TikTok, YouTube Shorts)")
    parser.add_argument("--greet", action="store_true", help="Send a general greeting message without a URL")
    parser.add_argument("--phone", default="+919876543210", help="Simulated sender phone number")
    args = parser.parse_args()

    test_webhook_handshake()

    if args.greet or not args.url:
        simulate_incoming_message(args.phone, "Hello! How does this bot work?")
    
    if args.url:
        simulate_incoming_message(args.phone, f"Please extract this recipe: {args.url}")
    elif not args.greet:
        # Default sample URL test
        sample_reel = "https://www.instagram.com/reel/C8ButterChickenSample/"
        print("\n" + "=" * 60)
        simulate_incoming_message(args.phone, f"Hey check this out: {sample_reel}")
