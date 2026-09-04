import argparse
import sys
import os

# Configure Windows console to UTF-8 to prevent 'charmap' codec errors with currency symbols and emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from config import save_api_key, get_api_key
from downloader import get_video_from_url
from gemini_processor import process_video_and_generate_recipe
from whatsapp_service import dispatch_whatsapp

def main():
    parser = argparse.ArgumentParser(description="Universal Reel & Shorts AI Extractor CLI")
    parser.add_argument("--url", required=True, help="Instagram Reel or YouTube Shorts URL")
    parser.add_argument("--phone", required=False, default="", help="WhatsApp Phone Number with country code")
    parser.add_argument("--key", required=False, help="Gemini API Key")
    parser.add_argument("--mode", default="Auto-Detect", help="Extraction Mode: Auto-Detect, Recipe, Workout, Tech, Summary")
    parser.add_argument("--engine", choices=["indownloader", "ytdlp"], default="ytdlp", help="Video downloader engine choice")

    args = parser.parse_args()

    api_key = args.key or get_api_key()
    if not api_key:
        print("[Error] No Gemini API key provided. Pass --key or set GEMINI_API_KEY environment variable.")
        sys.exit(1)

    if args.key:
        save_api_key(args.key)

    print("==================================================")
    print("⚡ Universal Reel & Shorts AI Extractor CLI")
    print("==================================================")
    print(f"1. Downloading video from {args.url} using {args.engine}...")
    success, video_path = get_video_from_url(args.url, preferred_engine=args.engine)

    if not success:
        print(f"[Error] Failed downloading video: {video_path}")
        sys.exit(1)

    print(f"-> Video downloaded to: {video_path}")

    print(f"2. Uploading video to Gemini & extracting intelligence (Mode: {args.mode})...")
    res = process_video_and_generate_recipe(video_path, custom_api_key=api_key, extraction_mode=args.mode)
    gen_success = res[0]
    txt_path = res[1]
    recipe_text = res[2]
    final_video_path = res[3] if len(res) > 3 else video_path
    meta = res[4] if len(res) > 4 else {}

    if not gen_success:
        print(f"[Error] Gemini processing failed: {recipe_text}")
        sys.exit(1)

    print(f"-> Extracted Domain: {meta.get('category_name', 'General')}")
    print(f"-> Title: {meta.get('title', 'Unknown')}")
    print(f"-> Notes saved to: {txt_path}")
    print(f"-> Video saved to: {final_video_path}")

    products = meta.get("products", [])
    if products:
        print(f"\n🛍️ Featured Products Detected ({len(products)}):")
        for p in products:
            price_tag = f" ({p['price']})" if p.get("price") else ""
            print(f"  • {p['name']}{price_tag}")
            print(f"    Amazon: {p['amazon_url']}")

    print("\n--- Summary Preview ---")
    if meta.get("summary"):
        print(meta["summary"])
    print("------------------------\n")

    if args.phone:
        print(f"3. Generating WhatsApp link for: {args.phone}...")
        cat_code = meta.get("category", "RECIPE")
        wa_success, wa_msg = dispatch_whatsapp(args.phone, txt_path, recipe_text, category=cat_code, products=products)
        print(f"-> {wa_msg}")

    print("\nProcess finished successfully!")

if __name__ == "__main__":
    main()

