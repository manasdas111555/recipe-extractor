import os
import sys
import time
import json
import urllib.request
import urllib.error
import mimetypes
from pathlib import Path
from typing import Tuple, Dict, Any

from config import get_groq_api_key, ensure_download_dir, get_affiliate_tags
from media_utils import extract_audio_from_video
from gemini_processor import get_prompt_for_mode, parse_extracted_content, safe_print

def _post_multipart_audio(url: str, api_key: str, file_path: Path, model: str = "whisper-large-v3") -> str:
    """Posts an audio file to Groq transcription endpoint using standard library multipart/form-data."""
    boundary = "----WebKitFormBoundaryGroqExtractor" + str(int(time.time()))
    body = bytearray()

    # Add model field
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(b'Content-Disposition: form-data; name="model"\r\n\r\n')
    body.extend(f"{model}\r\n".encode("utf-8"))

    # Add file field
    filename = file_path.name
    content_type = mimetypes.guess_type(str(file_path))[0] or "audio/mpeg"
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode("utf-8"))
    body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))

    with open(file_path, "rb") as f:
        body.extend(f.read())
    body.extend(b"\r\n")

    # Closing boundary
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "UniversalReelExtractor/1.0"
        }
    )

    with urllib.request.urlopen(req, timeout=45) as resp:
        res_data = json.loads(resp.read().decode("utf-8"))
        return res_data.get("text", "")

def process_video_with_groq(
    video_path: str,
    custom_api_key: str = None,
    status_callback = None,
    extraction_mode: str = "Auto-Detect",
    affiliate_tags: dict = None
) -> Tuple[bool, str, str, str, Dict[str, Any]]:
    """
    Extracts structured notes using Groq's high-speed Whisper-v3 (audio) + Llama 3.3 70B (reasoning).
    """
    api_key = (custom_api_key or get_groq_api_key()).strip()
    if not api_key:
        return False, "", "Groq API Key is missing. Please enter your Groq key in settings.", str(video_path), {}

    video_file_path = Path(video_path)
    if not video_file_path.exists():
        return False, "", f"Video file not found at {video_path}", str(video_path), {}

    output_dir = ensure_download_dir()

    def notify(msg: str):
        safe_print(f"[Groq] {msg}")
        if status_callback:
            try:
                status_callback(msg)
            except Exception:
                pass

    t_start = time.perf_counter()

    # Step 1: Extract Audio
    notify("Extracting audio track with FFmpeg...")
    ok_audio, audio_path, audio_err = extract_audio_from_video(video_file_path)
    if not ok_audio or not audio_path:
        return False, "", f"Audio extraction failed: {audio_err}", str(video_file_path), {}

    t_audio_end = time.perf_counter()
    audio_dur = t_audio_end - t_start

    # Step 2: Transcribe with Whisper-large-v3
    notify(f"Transcribing spoken audio with Groq Whisper-large-v3...")
    t_whisper_start = time.perf_counter()
    try:
        transcript = _post_multipart_audio(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            api_key=api_key,
            file_path=audio_path,
            model="whisper-large-v3"
        )
    except Exception as trans_err:
        # Cleanup audio
        audio_path.unlink(missing_ok=True)
        return False, "", f"Groq Whisper transcription failed: {str(trans_err)}", str(video_file_path), {}

    t_whisper_end = time.perf_counter()
    whisper_dur = t_whisper_end - t_whisper_start
    audio_path.unlink(missing_ok=True)

    if not transcript or not transcript.strip():
        transcript = "[No clear spoken dialogue detected in audio track. Video appears to be mostly background music or visual actions.]"

    notify(f"Transcribed speech in {whisper_dur:.1f}s. Generating structured notes with Llama 3.3 70B...")

    # Step 3: Inference with Llama 3.3 70B
    prompt_instructions = get_prompt_for_mode(extraction_mode)
    prompt_text = f"""The following is the exact audio transcript extracted from a short vertical video:
---
{transcript}
---

{prompt_instructions}
"""

    t_llama_start = time.perf_counter()
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.2
    }

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "UniversalReelExtractor/1.0"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            response_text = data["choices"][0]["message"]["content"].strip()
    except Exception as llama_err:
        return False, "", f"Groq Llama inference failed: {str(llama_err)}", str(video_file_path), {}

    t_llama_end = time.perf_counter()
    llama_dur = t_llama_end - t_llama_start

    meta = parse_extracted_content(response_text, affiliate_tags=affiliate_tags)
    meta["timings"] = {
        "upload_s": round(audio_dur, 2),
        "prep_s": round(whisper_dur, 2),
        "inference_s": round(llama_dur, 2),
        "total_ai_s": round(time.perf_counter() - t_start, 2),
        "model_used": "Groq (Whisper-v3 + Llama 3.3 70B)"
    }

    apt_title = meta["clean_filename"]
    txt_filename = output_dir / f"{apt_title}.txt"

    formatted_file_content = f"""==================================================
{meta['emoji']} {meta['title']} ({meta['category_name']})
==================================================
"""
    if meta.get("summary"):
        formatted_file_content += f"\n📋 Summary:\n{meta['summary']}\n"

    if meta.get("products") and len(meta["products"]) > 0:
        formatted_file_content += f"\n{'='*50}\n🛍️ Featured Products & 1-Click Purchase Links:\n{'='*50}\n"
        for idx, p in enumerate(meta["products"], 1):
            price_str = f" (Price: {p['price']})" if p.get("price") else ""
            formatted_file_content += f"{idx}. {p['name']}{price_str}\n"
            if p.get("buy_links"):
                for store, link in p["buy_links"].items():
                    formatted_file_content += f"   - {store}: {link}\n"
            formatted_file_content += "\n"

    formatted_file_content += f"\n{'='*50}\nDetailed Steps & Notes:\n{'='*50}\n\n{meta['details']}\n"

    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(formatted_file_content)

    return True, str(txt_filename), formatted_file_content, str(video_file_path), meta
