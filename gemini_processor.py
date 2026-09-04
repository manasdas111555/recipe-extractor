import os
import re
import time
from pathlib import Path
from typing import Tuple

from config import get_api_key, ensure_download_dir

PROMPT_TEXT = "Based on the uploaded video , create a txt file for the reciepe mentioned in the video."

def extract_apt_recipe_title(recipe_text: str) -> str:
    """
    Extracts a clean, descriptive recipe title from the generated text
    and sanitizes it into a valid Windows filename.
    """
    lines = [line.strip() for line in recipe_text.splitlines() if line.strip()]
    raw_title = "Recipe"

    for line in lines[:6]:
        # Strip markdown headings and symbols (#, **, *, -, etc.)
        cleaned = re.sub(r'^[#*_\-\s]+', '', line)
        cleaned = re.sub(r'[#*_\-\s]+$', '', cleaned)
        cleaned = re.sub(r'^(Title|Recipe|Name):\s*', '', cleaned, flags=re.IGNORECASE)

        if len(cleaned) > 3 and not cleaned.lower().startswith(("here is", "based on", "sure", "this recipe")):
            raw_title = cleaned
            break

    # Sanitize for Windows illegal filename characters (\ / : * ? " < > |)
    sanitized = re.sub(r'[\\/*?:"<>|]', '', raw_title)
    # Replace spaces and multiple underscores
    sanitized = re.sub(r'\s+', '_', sanitized)
    sanitized = re.sub(r'_+', '_', sanitized).strip('_')

    # Truncate length if excessively long
    if len(sanitized) > 60:
        sanitized = sanitized[:60].rstrip('_')

    return sanitized if sanitized else "Recipe"


def process_video_and_generate_recipe(video_path: str, custom_api_key: str = None, status_callback=None, model_preference: str = None) -> Tuple[bool, str, str]:
    """
    Uploads video to Gemini API, runs prompt, extracts apt recipe title,
    saves .txt file with apt name, and optionally renames video file to match.

    Returns (success, txt_filepath, recipe_text_or_error).
    """
    api_key = custom_api_key or get_api_key()
    if not api_key:
        return False, "", "Gemini API Key is missing. Please enter your API Key in settings."

    video_file_path = Path(video_path)
    if not video_file_path.exists():
        return False, "", f"Video file not found at {video_path}"

    output_dir = ensure_download_dir()

    def notify(msg: str):
        print(f"[Gemini] {msg}")
        if status_callback:
            try:
                status_callback(msg)
            except Exception:
                pass

    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        notify(f"Uploading video: `{video_file_path.name}` to Gemini...")
        uploaded_file = client.files.upload(file=str(video_file_path))
        notify(f"Video uploaded ({uploaded_file.name}). Waiting for file processing...")

        while uploaded_file.state.name == "PROCESSING":
            time.sleep(3)
            uploaded_file = client.files.get(name=uploaded_file.name)

        if uploaded_file.state.name == "FAILED":
            return False, "", "Gemini API failed to process video file."

        # Dynamically discover active models supported on this API key to prevent 404s
        available_model_names = []
        try:
            for m in client.models.list():
                name = getattr(m, 'name', '') or ''
                cleaned = name.replace('models/', '').strip()
                if cleaned:
                    available_model_names.append(cleaned)
        except Exception as list_err:
            print(f"[Gemini] Note: could not query model list dynamically: {list_err}")

        # Preferred modern candidate models (gemini-2.5-flash & gemini-3.1-pro-preview recommended by Google)
        preferred_candidates = ["gemini-2.5-flash", "gemini-3.1-pro-preview", "gemini-2.5-flash-lite"]
        
        # Exclude known deprecated models
        deprecated_models = {"gemini-2.5-pro", "gemini-1.5-flash", "gemini-2.0-flash"}

        if available_model_names:
            models_to_try = [
                m for m in preferred_candidates 
                if m in available_model_names and m not in deprecated_models
            ]
            if not models_to_try:
                models_to_try = [
                    m for m in available_model_names 
                    if m not in deprecated_models and any(k in m for k in ["3.1", "2.5", "flash", "pro"])
                ]
        else:
            models_to_try = preferred_candidates

        # If user explicitly preferred a model, ensure it's tried first
        if model_preference and model_preference in models_to_try:
            models_to_try.remove(model_preference)
            models_to_try.insert(0, model_preference)

        response = None
        attempt_log = []

        for model_name in models_to_try:
            notify(f"Requesting recipe generation with `{model_name}`...")
            model_succeeded = False
            # Try up to 3 attempts with exponential backoff for 503 high-demand traffic spikes
            for attempt in range(1, 4):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=[uploaded_file, PROMPT_TEXT]
                    )
                    if response and response.text:
                        notify(f"Successfully generated recipe with `{model_name}`!")
                        model_succeeded = True
                        break
                except Exception as gen_err:
                    err_str = str(gen_err)
                    print(f"[Gemini] Model {model_name} (attempt {attempt}) error: {err_str}")
                    is_busy = any(k in err_str.lower() for k in ["503", "unavailable", "high demand", "capacity", "resourceexhausted", "429"])
                    if is_busy and attempt < 3:
                        wait_sec = attempt * 3
                        notify(f"⚠️ `{model_name}` is experiencing high traffic (503). Retrying in {wait_sec}s (attempt {attempt}/3)...")
                        time.sleep(wait_sec)
                        continue
                    else:
                        attempt_log.append(f"{model_name}: {err_str}")
                        break

            if model_succeeded and response and response.text:
                break
            elif len(models_to_try) > 1:
                notify(f"🔄 `{model_name}` unavailable, trying next model...")

        # Best-effort cleanup of temporary uploaded video from Gemini File API
        try:
            client.files.delete(name=uploaded_file.name)
        except Exception:
            pass

        if not response or not response.text:
            error_details = " | ".join(attempt_log) if attempt_log else "No response generated."
            return False, "", f"Gemini API Error: {error_details}"

        recipe_content = response.text.strip()

        # Extract apt recipe title
        apt_title = extract_apt_recipe_title(recipe_content)
        txt_filename = output_dir / f"{apt_title}.txt"

        # Save TXT file with apt recipe title
        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(recipe_content)

        print(f"[Gemini] Saved recipe txt as: {txt_filename.name}")

        # Rename video file to match apt recipe title as well
        new_video_filename = output_dir / f"{apt_title}{video_file_path.suffix}"
        try:
            if video_file_path.exists() and not new_video_filename.exists():
                video_file_path.rename(new_video_filename)
                print(f"[Storage] Renamed video to match recipe title: {new_video_filename.name}")
        except Exception as rename_err:
            print(f"[Warning] Could not rename video file: {rename_err}")

        return True, str(txt_filename), recipe_content

    except Exception as e:
        return False, "", f"Gemini Processing Error: {str(e)}"

