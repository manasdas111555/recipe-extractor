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


def process_video_and_generate_recipe(video_path: str, custom_api_key: str = None) -> Tuple[bool, str, str]:
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

    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        print(f"[Gemini] Uploading video: {video_path}...")
        uploaded_file = client.files.upload(file=str(video_file_path))
        print(f"[Gemini] File uploaded ({uploaded_file.name}). Waiting for processing...")

        while uploaded_file.state.name == "PROCESSING":
            time.sleep(3)
            uploaded_file = client.files.get(name=uploaded_file.name)

        if uploaded_file.state.name == "FAILED":
            return False, "", "Gemini API failed to process video file."

        print("[Gemini] Generating recipe content...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[uploaded_file, PROMPT_TEXT]
        )

        recipe_content = response.text or "No recipe content generated."

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
        # Fallback for legacy SDK if needed
        try:
            import google.generativeai as legacy_genai
            legacy_genai.configure(api_key=api_key)

            print(f"[Gemini Legacy] Uploading video: {video_path}...")
            video_file = legacy_genai.upload_file(str(video_file_path))
            while video_file.state.name == "PROCESSING":
                time.sleep(3)
                video_file = legacy_genai.get_file(video_file.name)

            model = legacy_genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([video_file, PROMPT_TEXT])

            recipe_content = response.text or "No recipe content generated."
            apt_title = extract_apt_recipe_title(recipe_content)
            txt_filename = output_dir / f"{apt_title}.txt"

            with open(txt_filename, "w", encoding="utf-8") as f:
                f.write(recipe_content)

            return True, str(txt_filename), recipe_content
        except Exception as legacy_err:
            return False, "", f"Gemini API Error: {str(e)} (Fallback error: {str(legacy_err)})"
