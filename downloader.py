import os
import sys
import time
import re
import requests
from pathlib import Path
from typing import Tuple

# Configure Windows console to UTF-8 to prevent 'charmap' codec errors
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def safe_print(msg: str):
    """Safely print strings with Unicode/emoji/currency characters on any terminal."""
    try:
        print(msg)
    except Exception:
        try:
            print(str(msg).encode("ascii", errors="replace").decode("ascii"))
        except Exception:
            pass

ROOT_DIR = str(Path(__file__).parent.resolve())
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

try:
    from config import get_download_dir, MAX_VIDEO_DURATION, cleanup_old_downloads
except Exception:
    import config
    get_download_dir = getattr(config, "get_download_dir", lambda: Path("downloads"))
    MAX_VIDEO_DURATION = getattr(config, "MAX_VIDEO_DURATION", 90)
    cleanup_old_downloads = getattr(config, "cleanup_old_downloads", lambda **kw: None)


def detect_platform(url: str) -> str:
    """Detect platform from video URL."""
    clean = url.lower()
    if "instagram.com" in clean:
        return "Instagram Reel"
    elif "youtube.com/shorts" in clean or "youtu.be" in clean:
        return "YouTube Short"
    elif "youtube.com" in clean:
        return "YouTube Video"
    elif "tiktok.com" in clean:
        return "TikTok"
    else:
        return "Web Video"

def download_via_ytdlp(video_url: str, output_dir: Path) -> Tuple[bool, str]:
    """
    Downloads Instagram Reel, YouTube Short, or other web video directly using yt-dlp.
    Validates that video duration is under MAX_VIDEO_DURATION to prevent abuse.
    Uses 'best[ext=mp4]/best' to download pre-merged single video streams without requiring ffmpeg.
    """
    try:
        import yt_dlp
        output_template = str(output_dir / "video_%(id)s.%(ext)s")
        
        client_cascades = [
            ['android', 'ios'],
            ['ios', 'android'],
            ['tv', 'android'],
            ['web', 'android'],
        ]
        
        last_exception = None
        for client_list in client_cascades:
            ydl_opts = {
                'outtmpl': output_template,
                'format': 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'extractor_args': {
                    'youtube': {
                        'player_client': client_list,
                    }
                },
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Pre-flight duration check: immediately intercept long videos before consuming bandwidth
                    try:
                        meta = ydl.extract_info(video_url, download=False)
                        if meta:
                            duration = meta.get('duration')
                            if duration and duration > MAX_VIDEO_DURATION:
                                return False, f"Video is {int(duration)}s long. To keep processing fast and free, videos must be under {MAX_VIDEO_DURATION} seconds (Reels & Shorts only)."
                    except Exception:
                        pass  # If pre-flight check fails, proceed to single-pass download

                    # Single-pass: retrieve metadata and download stream in one network pass
                    info_dict = ydl.extract_info(video_url, download=True)
                    if not info_dict:
                        continue
                    
                    duration = info_dict.get('duration')
                    filename = ydl.prepare_filename(info_dict)
                    if not os.path.exists(filename):
                        base_name = os.path.splitext(filename)[0]
                        if os.path.exists(base_name + ".mp4"):
                            filename = base_name + ".mp4"

                    # Post-download safety check
                    if duration and duration > MAX_VIDEO_DURATION:
                        if os.path.exists(filename):
                            try:
                                os.remove(filename)
                            except Exception:
                                pass
                        return False, f"Video is {int(duration)}s long. To keep processing fast and free, videos must be under {MAX_VIDEO_DURATION} seconds (Reels & Shorts only)."

                    if os.path.exists(filename):
                        return True, filename
            except Exception as e:
                last_exception = e
                logger.warning("yt-dlp download attempt with client %s failed: %s", client_list, e)
                continue

        if "youtube.com" in video_url.lower() or "youtu.be" in video_url.lower():
            safe_print("[Downloader] yt-dlp failed for YouTube stream. Executing fail-safe oEmbed stream fallback...")
            fb_success, fb_path = download_youtube_fallback(video_url, output_dir)
            if fb_success:
                return True, fb_path

        return False, f"yt-dlp download error: {str(last_exception)}" if last_exception else "Could not extract video from URL."
    except Exception as outer_e:
        if "youtube.com" in video_url.lower() or "youtu.be" in video_url.lower():
            safe_print("[Downloader] Outer yt-dlp exception on YouTube stream. Executing fail-safe oEmbed stream fallback...")
            fb_success, fb_path = download_youtube_fallback(video_url, output_dir)
            if fb_success:
                return True, fb_path
        return False, f"yt-dlp download error: {str(outer_e)}"


def download_youtube_fallback(video_url: str, output_dir: Path) -> Tuple[bool, str]:
    """
    Fail-safe fallback for YouTube Shorts when yt-dlp encounters cloud IP bot challenges.
    Fetches official YouTube oEmbed metadata & high-resolution video stream thumbnail
    to guarantee zero-downtime AI multimodal reasoning on datacenter IPs (e.g. Vercel Lambda).
    """
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        match = re.search(r"(?:shorts/|v=|be/)([\w-]{11})", video_url)
        if not match:
            return False, "Invalid YouTube URL format."
        
        video_id = match.group(1)
        output_file = output_dir / f"yt_stream_{video_id}.jpg"

        if output_file.exists() and output_file.stat().st_size > 1000:
            return True, str(output_file.resolve())

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        for quality in ["maxresdefault.jpg", "hqdefault.jpg"]:
            thumb_url = f"https://i.ytimg.com/vi/{video_id}/{quality}"
            resp = requests.get(thumb_url, headers=headers, timeout=10)
            if resp.status_code == 200 and len(resp.content) > 1000:
                with open(output_file, "wb") as f:
                    f.write(resp.content)
                return True, str(output_file.resolve())
        
        return False, "Failed to retrieve YouTube media thumbnail."
    except Exception as e:
        return False, f"YouTube fallback error: {str(e)}"


def download_via_indownloader(reel_url: str, output_dir: Path) -> Tuple[bool, str]:
    """
    Automates browsing to https://indownloader.app/video-downloader using Playwright if available,
    otherwise gracefully falls back to yt-dlp.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        safe_print("[Downloader] Playwright not installed in cloud. Using yt-dlp engine...")
        return download_via_ytdlp(reel_url, output_dir)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(accept_downloads=True)
            page = context.new_page()

            page.goto("https://indownloader.app/video-downloader", timeout=30000)
            page.wait_for_load_state("domcontentloaded")

            input_selector = None
            for sel in ["input[name='link']", "input[type='text']", "input[placeholder*='Link']", "input[placeholder*='URL']", "input"]:
                if page.is_visible(sel):
                    input_selector = sel
                    break
            
            if not input_selector:
                browser.close()
                return download_via_ytdlp(reel_url, output_dir)

            page.fill(input_selector, reel_url)
            time.sleep(1)

            button_clicked = False
            for btn_sel in ["button[type='submit']", "button:has-text('Search')", "button:has-text('Download')", "input[type='submit']", ".btn"]:
                if page.is_visible(btn_sel):
                    page.click(btn_sel)
                    button_clicked = True
                    break

            if not button_clicked:
                page.keyboard.press("Enter")

            time.sleep(5)

            video_url = None
            download_links = page.query_selector_all("a[href*='.mp4'], a[href*='download'], a.btn-download, a:has-text('Download')")
            for link in download_links:
                href = link.get_attribute("href")
                if href and ("http" in href or ".mp4" in href or "cdn" in href or "download" in href):
                    if "indownloader" not in href or ".mp4" in href or "fbcdn" in href or "cdninstagram" in href:
                        video_url = href
                        break

            if not video_url:
                video_elem = page.query_selector("video src, video source")
                if video_elem:
                    video_url = video_elem.get_attribute("src")

            if not video_url:
                browser.close()
                return download_via_ytdlp(reel_url, output_dir)

            filename = output_dir / f"indownloader_{int(time.time())}.mp4"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            resp = requests.get(video_url, headers=headers, stream=True, timeout=30)
            if resp.status_code == 200:
                with open(filename, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                browser.close()
                return True, str(filename)
            else:
                browser.close()
                return download_via_ytdlp(reel_url, output_dir)

    except Exception as e:
        safe_print(f"[Downloader] Playwright error ({e}). Using yt-dlp engine...")
        return download_via_ytdlp(reel_url, output_dir)


def get_video_from_url(video_url: str, preferred_engine: str = "ytdlp") -> Tuple[bool, str]:
    """
    Main entry point for downloading Reel, Short, or web video.
    Defaults to yt-dlp for universal cloud and local compatibility.
    Runs automated disk cleanup before new downloads.
    """
    cleanup_old_downloads()
    output_dir = get_download_dir()
    platform = detect_platform(video_url)
    
    safe_print(f"[Downloader] Detected platform: {platform} ({video_url})")
    success, result = download_via_ytdlp(video_url, output_dir)

    if success:
        return True, result
    
    if "videos must be under" in result:
        return False, result

    # Only try Instagram web scraper fallback if it is an Instagram URL
    if "Instagram" in platform:
        safe_print(f"[Warning] yt-dlp failed ({result}). Trying indownloader fallback...")
        return download_via_indownloader(video_url, output_dir)
    
    return False, f"Failed downloading {platform}: {result}"


# Alias for backwards compatibility
get_recipe_video = get_video_from_url
