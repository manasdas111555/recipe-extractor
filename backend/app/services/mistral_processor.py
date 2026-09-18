import os
import sys
import time
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path
from typing import Tuple, Dict, Any, List

from config import get_mistral_api_key, ensure_download_dir, get_affiliate_tags
from media_utils import extract_audio_from_video, extract_keyframes
from gemini_processor import get_prompt_for_mode, parse_extracted_content, format_downloadable_txt, safe_print

def process_video_with_mistral(
    video_path: str,
    custom_api_key: str = None,
    status_callback = None,
    model_name: str = "mistral-small-latest",
    extraction_mode: str = "Auto-Detect",
    affiliate_tags: dict = None
) -> Tuple[bool, str, str, str, Dict[str, Any]]:
    """
    Extracts structured notes and intelligence using Mistral AI.
    Extracts keyframe images from the video and queries Mistral Vision / Chat API.
    """
    api_key = (custom_api_key or get_mistral_api_key()).strip()
    if not api_key:
        return False, "", "Mistral API Key is missing. Please enter your Mistral key in settings.", str(video_path), {}

    video_file_path = Path(video_path)
    if not video_file_path.exists():
        return False, "", f"Video file not found at {video_path}", str(video_path), {}

    output_dir = ensure_download_dir()

    def notify(msg: str):
        safe_print(f"[Mistral] {msg}")
        if status_callback:
            try:
                status_callback(msg)
            except Exception:
                pass

    t_start = time.perf_counter()
    notify("Extracting visual keyframes with FFmpeg...")
    ok_frames, frames, err_frames = extract_keyframes(video_file_path, num_frames=4)
    t_frame_end = time.perf_counter()
    frame_dur = t_frame_end - t_start

    prompt_instructions = get_prompt_for_mode(extraction_mode)
    prompt_text = f"""You are an expert content analyzer.
Analyze the following visual keyframes from this short video.
{prompt_instructions}
"""

    messages_content = [{"type": "text", "text": prompt_text}]

    # Attach keyframe images as base64 for multimodal visual analysis
    if ok_frames and frames:
        notify(f"Attached {len(frames)} visual frames ({frame_dur:.1f}s). Querying Mistral AI...")
        for fpath in frames[:4]:
            try:
                with open(fpath, "rb") as img_file:
                    b64_data = base64.b64encode(img_file.read()).decode("utf-8")
                    messages_content.append({
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{b64_data}"
                    })
            except Exception as read_err:
                safe_print(f"[Mistral] Could not read frame {fpath}: {read_err}")
    else:
        notify("Querying Mistral AI text engine...")

    # Candidate models to try in order of preference
    candidates = [model_name, "pixtral-12b-2409", "mistral-small-latest", "mistral-medium-latest"]
    unique_candidates = []
    for c in candidates:
        if c and c not in unique_candidates:
            unique_candidates.append(c)

    response_text = None
    successful_model = None
    t_infer_start = time.perf_counter()
    last_error = ""

    for candidate in unique_candidates:
        notify(f"Analyzing content with `{candidate}`...")
        payload = {
            "model": candidate,
            "messages": [
                {"role": "user", "content": messages_content}
            ],
            "temperature": 0.3
        }

        req = urllib.request.Request(
            "https://api.mistral.ai/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "UniversalReelExtractor/1.0"
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                choices = data.get("choices", [])
                if choices and choices[0].get("message", {}).get("content"):
                    response_text = choices[0]["message"]["content"].strip()
                    successful_model = candidate
                    notify(f"Successfully processed with `{candidate}`!")
                    break
        except urllib.error.HTTPError as http_err:
            err_body = http_err.read().decode("utf-8", errors="ignore")
            last_error = f"HTTP {http_err.code}: {err_body[:200]}"
            safe_print(f"[Mistral] {candidate} error: {last_error}")
            if http_err.code in [429, 503]:
                notify(f"⚠️ `{candidate}` busy ({http_err.code}). Trying next fallback model...")
                continue
            elif http_err.code == 400:
                # If image format rejected by this specific model, fallback to text-only prompt
                messages_content = [{"type": "text", "text": prompt_text}]
                continue
        except Exception as e:
            last_error = str(e)
            safe_print(f"[Mistral] Error with {candidate}: {last_error}")
            continue

    t_infer_end = time.perf_counter()
    infer_dur = t_infer_end - t_infer_start

    # Clean up temporary frames folder
    if ok_frames and frames:
        try:
            frames_dir = frames[0].parent
            for f in frames:
                f.unlink(missing_ok=True)
            frames_dir.rmdir()
        except Exception:
            pass

    if not response_text:
        return False, "", f"Mistral API Error: {last_error or 'No response received'}", str(video_file_path), {}

    meta = parse_extracted_content(response_text, affiliate_tags=affiliate_tags)
    meta["timings"] = {
        "upload_s": round(frame_dur, 2),
        "prep_s": 0.0,
        "inference_s": round(infer_dur, 2),
        "total_ai_s": round(time.perf_counter() - t_start, 2),
        "model_used": f"Mistral ({successful_model})"
    }

    apt_title = meta["clean_filename"]
    txt_filename = output_dir / f"{apt_title}.txt"

    formatted_file_content = format_downloadable_txt(meta)

    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(formatted_file_content)

    return True, str(txt_filename), formatted_file_content, str(video_file_path), meta
