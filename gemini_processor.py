import os
import sys
import re
import time
from pathlib import Path
from typing import Tuple

# Configure Windows console to UTF-8 to prevent 'charmap' codec errors with ₹ and emojis
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

from config import get_api_key, ensure_download_dir

CATEGORY_EMOJIS = {
    "RECIPE": "🍳",
    "WORKOUT": "🏋️",
    "TECH_TUTORIAL": "💻",
    "TRAVEL_GUIDE": "✈️",
    "KNOWLEDGE_SUMMARY": "💡",
    "GENERAL": "📝"
}

CATEGORY_NAMES = {
    "RECIPE": "Cooking Recipe",
    "WORKOUT": "Fitness Workout",
    "TECH_TUTORIAL": "Tech Tutorial",
    "TRAVEL_GUIDE": "Travel & Food Guide",
    "KNOWLEDGE_SUMMARY": "Knowledge & Summary",
    "GENERAL": "General Intelligence"
}

def get_prompt_for_mode(mode: str) -> str:
    """Returns specialized prompt based on selected extraction mode."""
    clean_mode = (mode or "Auto-Detect").lower()
    if "recipe" in clean_mode:
        return """
Analyze this video and extract a comprehensive cooking recipe.
Structure your response as follows:
[CATEGORY]: RECIPE
[TITLE]: <Exact dish name, max 6-8 words>
[SUMMARY]: <A 2-3 sentence overview of the dish, taste profile, and prep time>

---
[DETAILS]:
- Servings & Prep/Cook Time:
- Ingredients with exact measurements:
- Step-by-Step Cooking Instructions:
- Chef tips, substitutions & nutrition (if mentioned):
"""
    elif "workout" in clean_mode or "fitness" in clean_mode:
        return """
Analyze this video and extract the complete fitness workout routine.
Structure your response as follows:
[CATEGORY]: WORKOUT
[TITLE]: <Targeted workout title, max 6-8 words>
[SUMMARY]: <A 2-3 sentence overview of the targeted muscles and goal>

---
[DETAILS]:
- Target Muscle Groups & Equipment Needed:
- Warm-up & Setup:
- Exercise Routine (Exercise name, Sets x Reps, Rest interval):
- Form Cues, Technique Tips & Mistakes to Avoid:
"""
    elif "tech" in clean_mode or "tutorial" in clean_mode or "code" in clean_mode:
        return """
Analyze this video and extract detailed technical tutorial notes.
Structure your response as follows:
[CATEGORY]: TECH_TUTORIAL
[TITLE]: <Clear tech topic or tutorial title, max 6-8 words>
[SUMMARY]: <A 2-3 sentence overview of what is taught or built>

---
[DETAILS]:
- Prerequisites & Tools Used:
- Step-by-Step Instructions:
- Commands / Code Snippets:
- Common Gotchas & Best Practices:
"""
    elif "summary" in clean_mode or "knowledge" in clean_mode:
        return """
Analyze this video and extract an executive summary with key takeaways.
Structure your response as follows:
[CATEGORY]: KNOWLEDGE_SUMMARY
[TITLE]: <Core topic title, max 6-8 words>
[SUMMARY]: <A 2-3 sentence executive summary>

---
[DETAILS]:
- Core Thesis & Key Ideas:
- Detailed Breakdown & Bullet Points:
- Actionable Steps & Takeaways:
"""
    else:
        # Universal Auto-Detect Prompt
        return """
You are an expert Content Intelligence AI.
Analyze the uploaded video thoroughly and automatically classify and extract structured information tailored to its actual domain.

First, determine the CATEGORY of the video:
- RECIPE (cooking, baking, food prep, drinks)
- WORKOUT (exercises, fitness routines, gym, yoga)
- TECH_TUTORIAL (coding, software tools, computer guides, engineering)
- TRAVEL_GUIDE (places to visit, restaurants, travel itineraries, travel tips)
- KNOWLEDGE_SUMMARY (finance, business, life hacks, book summaries, educational)
- GENERAL (any other informative content)

Structure your response strictly as follows:
[CATEGORY]: <RECIPE | WORKOUT | TECH_TUTORIAL | TRAVEL_GUIDE | KNOWLEDGE_SUMMARY | GENERAL>
[TITLE]: <A clear, descriptive title-cased name for this video, max 6-8 words>
[SUMMARY]: <A 2-3 sentence executive summary of what this video demonstrates or teaches>

---
[DETAILS]:
(Provide rich, comprehensive, actionable details depending on the category):
- If RECIPE: Full ingredients with exact measurements, equipment needed, prep & cook time, step-by-step instructions, serving tips, and nutrition/calories if mentioned.
- If WORKOUT: Target muscles, equipment needed, warm-up, each exercise with sets x reps and rest intervals, and technique/form cues.
- If TECH_TUTORIAL: Tools & prerequisites, exact commands/code snippets, step-by-step walkthrough, and key notes.
- If TRAVEL_GUIDE: Place names, exact locations, recommendations, pricing/costs, and itinerary tips.
- If KNOWLEDGE_SUMMARY or GENERAL: Core principles, bulleted step-by-step breakdown, key quotes or insights, and actionable takeaways.

Be thorough, precise, and practical. Do not omit crucial steps or measurements.
"""

def parse_extracted_content(raw_text: str) -> dict:
    """
    Parses structured Gemini response into clean fields: category, title, summary, details, and safe filename.
    """
    category = "RECIPE"
    title = "Extracted_Content"
    summary = ""
    details = raw_text

    cat_match = re.search(r'\[CATEGORY\]:\s*([A-Za-z_]+)', raw_text, re.IGNORECASE)
    if cat_match:
        found_cat = cat_match.group(1).upper().strip()
        if any(c in found_cat for c in ["WORKOUT", "FITNESS", "EXERCISE"]):
            category = "WORKOUT"
        elif any(c in found_cat for c in ["TECH", "CODE", "PROGRAMMING", "TUTORIAL"]):
            category = "TECH_TUTORIAL"
        elif any(c in found_cat for c in ["TRAVEL", "PLACE", "RESTAURANT", "FOOD_GUIDE"]):
            category = "TRAVEL_GUIDE"
        elif any(c in found_cat for c in ["KNOWLEDGE", "FINANCE", "SUMMARY", "BOOK"]):
            category = "KNOWLEDGE_SUMMARY"
        elif any(c in found_cat for c in ["RECIPE", "COOK", "BAKE"]):
            category = "RECIPE"
        else:
            category = "GENERAL"

    title_match = re.search(r'\[TITLE\]:\s*(.+)', raw_text, re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = extract_apt_recipe_title(raw_text)

    summary_match = re.search(r'\[SUMMARY\]:\s*(.+?)(?=\n---\n|\[DETAILS\]|$)', raw_text, re.DOTALL | re.IGNORECASE)
    if summary_match:
        summary = summary_match.group(1).strip()

    details_match = re.search(r'(?:\[DETAILS\]:|---\s*\n\[DETAILS\]:)\s*(.+)', raw_text, re.DOTALL | re.IGNORECASE)
    if details_match:
        details = details_match.group(1).strip()

    # Sanitize title for filename & normalize currency symbols
    clean_title = title.replace('₹', 'Rs_').replace('$', 'USD_').replace('€', 'EUR_').replace('£', 'GBP_')
    clean_title = re.sub(r'[\\/*?:"<>|]', '', clean_title)
    clean_title = re.sub(r'^[#*_\-\s]+', '', clean_title)
    clean_title = re.sub(r'[#*_\-\s]+$', '', clean_title)
    clean_title = re.sub(r'\s+', '_', clean_title)
    clean_title = re.sub(r'_+', '_', clean_title).strip('_')
    if len(clean_title) > 60:
        clean_title = clean_title[:60].rstrip('_')
    if not clean_title:
        clean_title = "Extracted_Content"

    emoji = CATEGORY_EMOJIS.get(category, "📝")
    category_name = CATEGORY_NAMES.get(category, "General Intelligence")

    return {
        "category": category,
        "category_name": category_name,
        "emoji": emoji,
        "title": title,
        "summary": summary,
        "details": details,
        "clean_filename": clean_title,
        "raw_text": raw_text
    }

def extract_apt_recipe_title(recipe_text: str) -> str:
    """
    Extracts a clean, descriptive recipe title from the generated text
    and sanitizes it into a valid Windows filename.
    """
    lines = [line.strip() for line in recipe_text.splitlines() if line.strip()]
    raw_title = "Recipe"

    for line in lines[:6]:
        cleaned = re.sub(r'^[#*_\-\s]+', '', line)
        cleaned = re.sub(r'[#*_\-\s]+$', '', cleaned)
        cleaned = re.sub(r'^(Title|Recipe|Name):\s*', '', cleaned, flags=re.IGNORECASE)

        if len(cleaned) > 3 and not cleaned.lower().startswith(("here is", "based on", "sure", "this recipe", "[category", "[summary")):
            raw_title = cleaned
            break

    sanitized = raw_title.replace('₹', 'Rs_').replace('$', 'USD_').replace('€', 'EUR_').replace('£', 'GBP_')
    sanitized = re.sub(r'[\\/*?:"<>|]', '', sanitized)
    sanitized = re.sub(r'\s+', '_', sanitized)
    sanitized = re.sub(r'_+', '_', sanitized).strip('_')

    if len(sanitized) > 60:
        sanitized = sanitized[:60].rstrip('_')

    return sanitized if sanitized else "Recipe"


def process_video_and_generate_recipe(
    video_path: str, 
    custom_api_key: str = None, 
    status_callback=None, 
    model_preference: str = None,
    extraction_mode: str = "Auto-Detect"
) -> Tuple[bool, str, str, str, dict]:
    """
    Uploads video to Gemini API, runs intelligent prompt based on extraction mode,
    auto-classifies content, saves structured .txt file, and renames video file to match.

    Returns (success, txt_filepath, formatted_content_or_error, final_video_path, metadata_dict).
    """
    api_key = custom_api_key or get_api_key()
    if not api_key:
        return False, "", "Gemini API Key is missing. Please enter your API Key in settings.", str(video_path), {}

    video_file_path = Path(video_path)
    if not video_file_path.exists():
        return False, "", f"Video file not found at {video_path}", str(video_path), {}

    output_dir = ensure_download_dir()

    def notify(msg: str):
        safe_print(f"[Gemini] {msg}")
        if status_callback:
            try:
                status_callback(msg)
            except Exception:
                pass

    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        prompt_text = get_prompt_for_mode(extraction_mode)

        notify(f"Uploading video: `{video_file_path.name}` to Gemini...")
        uploaded_file = client.files.upload(file=str(video_file_path))
        notify(f"Video uploaded ({uploaded_file.name}). Waiting for file processing...")

        while uploaded_file.state.name == "PROCESSING":
            time.sleep(3)
            uploaded_file = client.files.get(name=uploaded_file.name)

        if uploaded_file.state.name == "FAILED":
            return False, "", "Gemini API failed to process video file.", str(video_file_path), {}

        # Dynamically discover active models supported on this API key to prevent 404s
        available_model_names = []
        try:
            for m in client.models.list():
                name = getattr(m, 'name', '') or ''
                cleaned = name.replace('models/', '').strip()
                if cleaned:
                    available_model_names.append(cleaned)
        except Exception as list_err:
            safe_print(f"[Gemini] Note: could not query model list dynamically: {list_err}")

        # Preferred modern candidate models (Gemini 3.8 Flash, 3.1 Pro Preview, 2.5 Flash)
        preferred_candidates = [
            "gemini-3.8-flash",
            "gemini-3.1-pro-preview",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite"
        ]
        
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
                    if m not in deprecated_models and any(k in m for k in ["3.8", "3.1", "3", "2.5", "flash", "pro"])
                ]
        else:
            models_to_try = list(preferred_candidates)

        # If user explicitly preferred a model, ensure it's tried first regardless of list filter
        if model_preference:
            if model_preference in models_to_try:
                models_to_try.remove(model_preference)
            models_to_try.insert(0, model_preference)

        response = None
        attempt_log = []

        for model_name in models_to_try:
            notify(f"Analyzing video & extracting intelligence with `{model_name}`...")
            model_succeeded = False
            # Try up to 3 attempts with exponential backoff for 503 high-demand traffic spikes
            for attempt in range(1, 4):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=[uploaded_file, prompt_text]
                    )
                    if response and response.text:
                        notify(f"Successfully processed video with `{model_name}`!")
                        model_succeeded = True
                        break
                except Exception as gen_err:
                    err_str = str(gen_err)
                    safe_print(f"[Gemini] Model {model_name} (attempt {attempt}) error: {err_str}")
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
            return False, "", f"Gemini API Error: {error_details}", str(video_file_path), {}

        raw_content = response.text.strip()
        meta = parse_extracted_content(raw_content)

        apt_title = meta["clean_filename"]
        txt_filename = output_dir / f"{apt_title}.txt"

        # Format clean .txt document
        formatted_file_content = f"""==================================================
{meta['emoji']} {meta['title']} ({meta['category_name']})
==================================================
"""
        if meta.get("summary"):
            formatted_file_content += f"\n📋 Summary:\n{meta['summary']}\n"
        formatted_file_content += f"\n{'='*50}\nDetailed Steps & Notes:\n{'='*50}\n\n{meta['details']}\n"

        # Save TXT file with utf-8 encoding
        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(formatted_file_content)

        safe_print(f"[Gemini] Saved {meta['category_name']} txt as: {txt_filename.name}")

        # Rename video file to match apt title
        new_video_filename = output_dir / f"{apt_title}{video_file_path.suffix}"
        final_video_path = str(video_file_path)
        try:
            if video_file_path.exists() and not new_video_filename.exists():
                video_file_path.rename(new_video_filename)
                final_video_path = str(new_video_filename)
                safe_print(f"[Storage] Renamed video to match title: {new_video_filename.name}")
            elif new_video_filename.exists():
                final_video_path = str(new_video_filename)
        except Exception as rename_err:
            safe_print(f"[Warning] Could not rename video file: {rename_err}")

        return True, str(txt_filename), formatted_file_content, final_video_path, meta

    except Exception as e:
        return False, "", f"Gemini Processing Error: {str(e)}", str(video_path), {}

