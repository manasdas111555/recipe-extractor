import argparse
import sys
from config import save_api_key, get_api_key
from downloader import get_recipe_video
from gemini_processor import process_video_and_generate_recipe
from whatsapp_service import dispatch_whatsapp

def main():
    parser = argparse.ArgumentParser(description="Instagram Reel Recipe Extractor CLI")
    parser.add_argument("--url", required=True, help="Instagram Reel URL")
    parser.add_argument("--phone", required=True, help="WhatsApp Phone Number with country code")
    parser.add_argument("--key", required=False, help="Gemini API Key")
    parser.add_argument("--engine", choices=["indownloader", "ytdlp"], default="indownloader", help="Video downloader engine choice")

    args = parser.parse_args()

    api_key = args.key or get_api_key()
    if not api_key:
        print("[Error] No Gemini API key provided. Pass --key or set GEMINI_API_KEY environment variable.")
        sys.exit(1)

    if args.key:
        save_api_key(args.key)

    print("==================================================")
    print("Instagram Reel Recipe Extractor & WhatsApp Bot")
    print("==================================================")
    print(f"1. Downloading reel using {args.engine} engine...")
    success, video_path = get_recipe_video(args.url, preferred_engine=args.engine)

    if not success:
        print(f"[Error] Failed downloading video: {video_path}")
        sys.exit(1)

    print(f"-> Video downloaded to: {video_path}")

    print("2. Uploading video to Gemini & generating recipe txt...")
    gen_success, txt_path, recipe_text = process_video_and_generate_recipe(video_path, custom_api_key=api_key)

    if not gen_success:
        print(f"[Error] Gemini processing failed: {recipe_text}")
        sys.exit(1)

    print(f"-> Recipe saved to: {txt_path}")
    print("\n--- Recipe Preview ---")
    print(recipe_text[:500] + ("..." if len(recipe_text) > 500 else ""))
    print("----------------------\n")

    print(f"3. Forwarding to WhatsApp number: {args.phone}...")
    wa_success, wa_msg = dispatch_whatsapp(args.phone, txt_path, recipe_text)
    print(f"-> WhatsApp result: {wa_msg}")

    print("\nProcess finished!")

if __name__ == "__main__":
    main()
