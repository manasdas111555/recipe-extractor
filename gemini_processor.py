import os
import sys
import re
import time
import urllib.parse
from pathlib import Path
from typing import Tuple, List, Dict


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

from config import get_api_key, ensure_download_dir, get_affiliate_tags


CATEGORY_EMOJIS = {
    "KITCHEN_FINDS": "🛍️",
    "PRODUCT_FINDS": "📦",
    "RECIPE": "🍳",
    "WORKOUT": "🏋️",
    "TECH_TUTORIAL": "💻",
    "TRAVEL_GUIDE": "✈️",
    "KNOWLEDGE_SUMMARY": "💡",
    "GENERAL": "📝"
}

CATEGORY_NAMES = {
    "KITCHEN_FINDS": "Kitchen & Home Finds",
    "PRODUCT_FINDS": "Product Unboxing & Finds",
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
    if "kitchen" in clean_mode or "home find" in clean_mode or "gadget" in clean_mode:
        return """
Analyze this video and extract all kitchen finds, tools, organizers, and home gadgets showcased.
Structure your response strictly as follows:
[CATEGORY]: KITCHEN_FINDS
[TITLE]: <Clear, descriptive title of the kitchen finds, max 6-8 words>
[SUMMARY]: <A 2-3 sentence overview of the products demonstrated and their primary benefits>

[PRODUCTS]:
For EVERY kitchen gadget, tool, organizer, cookware, or appliance featured or demonstrated, list each one in this exact line format:
- PRODUCT: <Exact Brand & Product Name> | PRICE: <Price if stated or estimated, e.g. Under ₹1000, or 'N/A'> | SEARCH: <Targeted search keywords to buy this item online>

---
[DETAILS]:
For each item showcased:
- Product Name:
- Key Features & Material:
- Everyday Uses in the Kitchen:
- Practical Usability Tips:
- Pros & Cons:
"""
    elif "unboxing" in clean_mode or "haul" in clean_mode or "product" in clean_mode:
        return """
Analyze this video and extract all products, unboxings, reviews, and gadgets showcased.
Structure your response strictly as follows:
[CATEGORY]: PRODUCT_FINDS
[TITLE]: <Clear product haul or unboxing title, max 6-8 words>
[SUMMARY]: <A 2-3 sentence overview of the items reviewed>

[PRODUCTS]:
For EVERY product, gadget, or item unboxed or demonstrated, list each one in this exact line format:
- PRODUCT: <Exact Brand & Product Name> | PRICE: <Price if stated or estimated, or 'N/A'> | SEARCH: <Targeted search keywords to buy this item online>

---
[DETAILS]:
For each product:
- Item Name & Brand:
- Specifications & Build Quality:
- Key Functionality & Value Proposition:
- Buyer Advice & Verdict:
"""
    elif "recipe" in clean_mode:
        return """
Analyze this video and extract a comprehensive cooking recipe.
Structure your response as follows:
[CATEGORY]: RECIPE
[TITLE]: <Exact dish name, max 6-8 words>
[SUMMARY]: <A 2-3 sentence overview of the dish, taste profile, and prep time>

[PRODUCTS]:
If any special kitchen gadgets, appliances, cookware, or branded gourmet ingredients are featured or recommended to buy, list each one in this exact line format:
- PRODUCT: <Brand/Item Name> | PRICE: <Price or price range if stated, or 'N/A'> | SEARCH: <Targeted search keywords to buy this item online>
If no specific purchasable products/gadgets are featured, write:
[PRODUCTS]: NONE

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

[PRODUCTS]:
If any specific workout gear, gym equipment, resistance bands, supplements, or shoes are featured or recommended to buy, list each one in this exact line format:
- PRODUCT: <Brand/Item Name> | PRICE: <Price or price range if stated, or 'N/A'> | SEARCH: <Targeted search keywords to buy this item online>
If no specific gear/equipment is featured, write:
[PRODUCTS]: NONE

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

[PRODUCTS]:
If any specific tech gadgets, hardware, devices, tools, or peripherals are featured or recommended to buy, list each one in this exact line format:
- PRODUCT: <Brand/Model Name> | PRICE: <Price or price range if stated, or 'N/A'> | SEARCH: <Targeted search keywords to buy this item online>
If no hardware or physical products are featured, write:
[PRODUCTS]: NONE

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

[PRODUCTS]:
If any specific books, gadgets, planners, tools, or hardware are featured or recommended to buy, list each one in this exact line format:
- PRODUCT: <Item/Book Name> | PRICE: <Price if stated, or 'N/A'> | SEARCH: <Targeted search keywords to buy this item online>
If no purchasable products are mentioned, write:
[PRODUCTS]: NONE

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
- KITCHEN_FINDS (kitchen gadgets, home organizers, kitchen tools, cookware reviews, Amazon kitchen finds)
- PRODUCT_FINDS (product unboxings, gadget hauls, Amazon finds, tool reviews, lifestyle gear)
- RECIPE (actual cooking, baking, dish preparation, edible recipes with ingredients)
- WORKOUT (exercises, fitness routines, gym, yoga)
- TECH_TUTORIAL (coding, software tools, computer guides, engineering)
- TRAVEL_GUIDE (places to visit, restaurants, travel itineraries, travel tips)
- KNOWLEDGE_SUMMARY (finance, business, life hacks, book summaries, educational)
- GENERAL (any other informative content)

CRITICAL INSTRUCTION FOR CLASSIFICATION:
If the video demonstrates kitchen utensils, storage organizers, gadgets, or Amazon finds, DO NOT classify it as RECIPE. Classify it as KITCHEN_FINDS or PRODUCT_FINDS!
Only classify as RECIPE if someone is actually preparing, seasoning, cooking, or baking food/drinks with edible ingredients.

Structure your response strictly as follows:
[CATEGORY]: <KITCHEN_FINDS | PRODUCT_FINDS | RECIPE | WORKOUT | TECH_TUTORIAL | TRAVEL_GUIDE | KNOWLEDGE_SUMMARY | GENERAL>
[TITLE]: <A clear, descriptive title-cased name for this video, max 6-8 words>
[SUMMARY]: <A 2-3 sentence executive summary of what this video demonstrates or reviews>

[PRODUCTS]:
For EVERY item, gadget, or product showcased, reviewed, or unboxed in this video, list each one in this exact line format:
- PRODUCT: <Brand & Model / Item Name> | PRICE: <Price if stated or estimated, e.g. Under ₹1000, or 'N/A'> | SEARCH: <Targeted search query to find and buy this exact item online>

If no specific purchasable products or equipment are featured, write:
[PRODUCTS]: NONE

---
[DETAILS]:
(Provide rich, comprehensive, actionable details depending on the category):
- If KITCHEN_FINDS or PRODUCT_FINDS: List each item with its key features, what it is used for, usability tips, and pros/cons.
- If RECIPE: Full ingredients with exact measurements, equipment needed, prep & cook time, step-by-step instructions, serving tips, and nutrition/calories if mentioned.
- If WORKOUT: Target muscles, equipment needed, warm-up, each exercise with sets x reps and rest intervals, and technique/form cues.
- If TECH_TUTORIAL: Tools & prerequisites, exact commands/code snippets, step-by-step walkthrough, and key notes.
- If TRAVEL_GUIDE: Place names, exact locations, recommendations, pricing/costs, and itinerary tips.
- If KNOWLEDGE_SUMMARY or GENERAL: Core principles, bulleted step-by-step breakdown, key insights, and actionable takeaways.

Be thorough, precise, and practical. Do not omit crucial steps or product names.
"""

def parse_extracted_content(raw_text: str, affiliate_tags: dict = None) -> dict:
    """
    Parses structured Gemini response into clean fields: category, title, summary, products, details, and safe filename.
    Attaches affiliate tracking tags to Amazon and Flipkart links if configured.
    """
    if affiliate_tags is None:
        affiliate_tags = get_affiliate_tags()

    category = "RECIPE"
    title = "Extracted_Content"
    summary = ""
    details = raw_text
    products = []

    cat_match = re.search(r'\[CATEGORY\]:\s*([A-Za-z_]+)', raw_text, re.IGNORECASE)
    if cat_match:
        found_cat = cat_match.group(1).upper().strip()
        if any(c in found_cat for c in ["KITCHEN_FINDS", "KITCHEN_FIND", "KITCHEN_GADGET", "HOME_FIND"]):
            category = "KITCHEN_FINDS"
        elif any(c in found_cat for c in ["PRODUCT_FINDS", "PRODUCT_FIND", "UNBOXING", "PRODUCT_REVIEW", "HAUL", "AMAZON_FIND"]):
            category = "PRODUCT_FINDS"
        elif any(c in found_cat for c in ["WORKOUT", "FITNESS", "EXERCISE"]):
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

    summary_match = re.search(r'\[SUMMARY\]:\s*(.+?)(?=\n---\n|\[DETAILS\]|\[PRODUCTS\]|$)', raw_text, re.DOTALL | re.IGNORECASE)
    if summary_match:
        summary = summary_match.group(1).strip()

    # Extract Products section
    prod_section_match = re.search(r'\[PRODUCTS\]:\s*(.+?)(?=\n---\n|\[DETAILS\]|\[CATEGORY\]|\[TITLE\]|\[SUMMARY\]|$)', raw_text, re.DOTALL | re.IGNORECASE)
    if not prod_section_match:
        prod_section_match = re.search(r'\[PRODUCTS\]:\s*(.+)', raw_text, re.DOTALL | re.IGNORECASE)

    if prod_section_match:
        prod_text = prod_section_match.group(1).strip()
        if prod_text.upper() != "NONE" and not prod_text.upper().startswith("NONE"):
            for line in prod_text.splitlines():
                line = line.strip()
                if not line or line.startswith(('#', '=')) or line.upper() == "NONE":
                    continue

                p_match = re.search(r'PRODUCT:\s*([^|]+)(?:\|\s*PRICE:\s*([^|]+))?(?:\|\s*SEARCH:\s*(.+))?', line, re.IGNORECASE)
                if p_match:
                    p_name = p_match.group(1).strip()
                    p_price = (p_match.group(2) or "").strip()
                    p_search = (p_match.group(3) or "").strip() or p_name
                else:
                    cleaned_line = re.sub(r'^[-*•\d\.]+\s*', '', line).strip()
                    if len(cleaned_line) > 3 and not cleaned_line.startswith('['):
                        p_name = cleaned_line
                        p_price = ""
                        p_search = cleaned_line
                    else:
                        continue

                p_name_clean = re.sub(r'[*_#]', '', p_name).strip()
                p_search_clean = re.sub(r'[*_#]', '', p_search).strip()
                if not p_name_clean:
                    continue

                amz_tag = (affiliate_tags.get("amazon") or "").strip()
                amz_param = f"&tag={urllib.parse.quote_plus(amz_tag)}" if amz_tag else ""
                flp_tag = (affiliate_tags.get("flipkart") or "").strip()
                flp_param = f"&affid={urllib.parse.quote_plus(flp_tag)}" if flp_tag else ""

                encoded_q = urllib.parse.quote_plus(p_search_clean)
                products.append({
                    "name": p_name_clean,
                    "price": p_price if p_price and p_price.upper() not in ["N/A", "NONE", "NOT SPECIFIED"] else "",
                    "query": p_search_clean,
                    "amazon_url": f"https://www.amazon.in/s?k={encoded_q}{amz_param}",
                    "amazon_global_url": f"https://www.amazon.com/s?k={encoded_q}{amz_param}",
                    "google_shopping_url": f"https://www.google.com/search?tbm=shop&q={encoded_q}",
                    "flipkart_url": f"https://www.flipkart.com/search?q={encoded_q}{flp_param}"
                })

    # Secondary Fallback: If no products were captured via [PRODUCTS] section but items are described in details
    if len(products) == 0 and category in ["KITCHEN_FINDS", "PRODUCT_FINDS", "GENERAL"]:
        fallback_matches = re.findall(r'(?:^|\n)(?:###\s*\d+\.|\d+\.|\*)\s*\*\*([^*\n:]+)\*\*', raw_text)
        for f_item in fallback_matches:
            item_clean = f_item.strip()
            if len(item_clean) > 3 and not any(k in item_clean.lower() for k in ["features", "uses", "tips", "pros", "cons", "details", "summary", "instructions"]):
                amz_tag = (affiliate_tags.get("amazon") or "").strip()
                amz_param = f"&tag={urllib.parse.quote_plus(amz_tag)}" if amz_tag else ""
                flp_tag = (affiliate_tags.get("flipkart") or "").strip()
                flp_param = f"&affid={urllib.parse.quote_plus(flp_tag)}" if flp_tag else ""
                encoded_q = urllib.parse.quote_plus(item_clean)
                products.append({
                    "name": item_clean,
                    "price": "",
                    "query": item_clean,
                    "amazon_url": f"https://www.amazon.in/s?k={encoded_q}{amz_param}",
                    "amazon_global_url": f"https://www.amazon.com/s?k={encoded_q}{amz_param}",
                    "google_shopping_url": f"https://www.google.com/search?tbm=shop&q={encoded_q}",
                    "flipkart_url": f"https://www.flipkart.com/search?q={encoded_q}{flp_param}"
                })


    details_match = re.search(r'(?:\[DETAILS\]:|---\s*\n\[DETAILS\]:)\s*(.+)', raw_text, re.DOTALL | re.IGNORECASE)
    if details_match:
        details = details_match.group(1).strip()
        details = re.sub(r'\[PRODUCTS\]:\s*.+', '', details, flags=re.DOTALL | re.IGNORECASE).strip()

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
        "products": products,
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
    extraction_mode: str = "Auto-Detect",
    affiliate_tags: dict = None
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
        from google.genai import types

        # Disable internal SDK retries (attempts=1) and set 25s timeout to prevent 155s hangs on congested models
        retry_opt = types.HttpRetryOptions(attempts=1)
        http_opt = types.HttpOptions(timeout=25000, retry_options=retry_opt)
        client = genai.Client(api_key=api_key, http_options=http_opt)
        prompt_text = get_prompt_for_mode(extraction_mode)

        # Step 1: Upload video to Gemini File API
        t_gemini_start = time.perf_counter()
        t_upload_start = time.perf_counter()
        notify(f"Uploading video: `{video_file_path.name}` to Gemini Cloud...")
        uploaded_file = client.files.upload(file=str(video_file_path))
        t_upload_end = time.perf_counter()
        upload_duration = t_upload_end - t_upload_start
        notify(f"Video uploaded in {upload_duration:.1f}s ({uploaded_file.name}). Preparing video...")

        # Step 2: Poll until video is in ACTIVE state (1s interval for minimum latency)
        t_poll_start = time.perf_counter()
        while uploaded_file.state.name == "PROCESSING":
            time.sleep(1)
            uploaded_file = client.files.get(name=uploaded_file.name)
            if time.perf_counter() - t_poll_start > 60:
                break
        t_poll_end = time.perf_counter()
        prep_duration = t_poll_end - t_poll_start

        if uploaded_file.state.name == "FAILED":
            return False, "", "Gemini API failed to process video file.", str(video_file_path), {}

        notify(f"Video ready in {prep_duration:.1f}s. Beginning multi-modal AI reasoning...")

        # Step 3: Model execution priority - Gemini 3.5 Flash / 3.6 Flash / 3.7 Flash
        preferred_candidates = [
            "gemini-3.5-flash",       # Verified ultra-fast (1.5s - 8.7s) with full multimodal video & product extraction
            "gemini-3.6-flash",       # Verified active in user AI Studio account
            "gemini-3.7-flash",       # Active in user AI Studio account
            "gemini-2.5-flash",       # Legacy backward-compatibility fallback
            "gemini-3.5-flash-lite",  # Fallback: lightweight
        ]

        models_to_try = list(preferred_candidates)

        # If user explicitly preferred a specific model from UI, place it at the front
        if model_preference:
            if model_preference in models_to_try:
                models_to_try.remove(model_preference)
            models_to_try.insert(0, model_preference)

        response = None
        attempt_log = []
        successful_model = None
        inference_duration = 0.0

        for model_name in models_to_try:
            notify(f"Analyzing video & extracting intelligence with `{model_name}`...")
            model_succeeded = False
            remaining_models = len(models_to_try) - (models_to_try.index(model_name) + 1)
            max_attempts = 1 if remaining_models > 0 else 2

            for attempt in range(1, max_attempts + 1):
                t_infer_start = time.perf_counter()
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=[uploaded_file, prompt_text]
                    )
                    if response and response.text:
                        inference_duration = time.perf_counter() - t_infer_start
                        successful_model = model_name
                        notify(f"Successfully processed video with `{model_name}` in {inference_duration:.1f}s!")
                        model_succeeded = True
                        break
                except Exception as gen_err:
                    err_str = str(gen_err)
                    safe_print(f"[Gemini] Model {model_name} (attempt {attempt}) error: {err_str}")
                    is_busy = any(k in err_str.lower() for k in ["503", "unavailable", "high demand", "capacity", "resourceexhausted", "429"])
                    
                    if is_busy and remaining_models > 0:
                        # Fast failover: don't stall for 9s if another healthy model is in line
                        notify(f"⚠️ `{model_name}` congested (503/429). Instantly switching to next model...")
                        attempt_log.append(f"{model_name}: {err_str}")
                        break
                    elif is_busy and attempt < max_attempts:
                        notify(f"⚠️ `{model_name}` congested (503). Retrying in 1.5s...")
                        time.sleep(1.5)
                        continue
                    else:
                        attempt_log.append(f"{model_name}: {err_str}")
                        break

            if model_succeeded and response and response.text:
                break
            elif remaining_models > 0:
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
        meta = parse_extracted_content(raw_content, affiliate_tags=affiliate_tags)

        meta["timings"] = {
            "upload_s": round(upload_duration, 2),
            "prep_s": round(prep_duration, 2),
            "inference_s": round(inference_duration, 2),
            "total_ai_s": round(time.perf_counter() - t_gemini_start, 2),
            "model_used": successful_model or "gemini-3.5-flash"
        }


        apt_title = meta["clean_filename"]
        txt_filename = output_dir / f"{apt_title}.txt"

        # Format clean .txt document
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
                formatted_file_content += f"   • Amazon: {p['amazon_url']}\n"
                formatted_file_content += f"   • Google Shopping: {p['google_shopping_url']}\n"
                formatted_file_content += f"   • Flipkart: {p['flipkart_url']}\n\n"

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

