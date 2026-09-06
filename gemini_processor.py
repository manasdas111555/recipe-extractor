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
    "RECIPE": "🍳",
    "KITCHEN_FINDS": "🛍️",
    "EDUCATIONAL": "🎓",
    "TUTORIAL": "💻",
    "TECH_TUTORIAL": "💻",
    "PRODUCT_FINDS": "📦",
    "WORKOUT": "🏋️",
    "FINANCE_BUSINESS": "💰",
    "TRAVEL_GUIDE": "✈️",
    "BEAUTY_FASHION": "💄",
    "LIFE_HACKS": "💡",
    "KNOWLEDGE_SUMMARY": "💡",
    "GENERAL": "📝"
}

CATEGORY_NAMES = {
    "RECIPE": "Cooking Recipe",
    "KITCHEN_FINDS": "Kitchen & Home Finds",
    "EDUCATIONAL": "Educational & Concept Explainer",
    "TUTORIAL": "Tutorial & How-To Guide",
    "TECH_TUTORIAL": "Tutorial & How-To Guide",
    "PRODUCT_FINDS": "Product Unboxing & Finds",
    "WORKOUT": "Fitness & Workout Routine",
    "FINANCE_BUSINESS": "Finance & Business Insights",
    "TRAVEL_GUIDE": "Travel & Places Guide",
    "BEAUTY_FASHION": "Beauty, Skincare & Fashion",
    "LIFE_HACKS": "Life Hacks & Productivity",
    "KNOWLEDGE_SUMMARY": "Knowledge & Executive Summary",
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
    elif "recipe" in clean_mode or "cook" in clean_mode:
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
    elif "educational" in clean_mode or "academic" in clean_mode or "science" in clean_mode or "history" in clean_mode or "explainer" in clean_mode:
        return """
Analyze this video and extract comprehensive educational notes, core concepts, and recommended learning resources.
Structure your response strictly as follows:
[CATEGORY]: EDUCATIONAL
[TITLE]: <Clear, academic topic or concept title, max 6-8 words>
[SUMMARY]: <A 2-3 sentence executive overview explaining the core thesis, scientific principle, or historical topic>

[RESOURCES & TUTORIALS]:
For EVERY lecture series, academic paper, YouTube explainer, book, or online course cited or recommended to study this topic:
List each one in this exact line format:
- RESOURCE: <Lecture / Course / Book Name> | PLATFORM: <YouTube | Course | Book | Paper> | SEARCH: <Targeted search query to find and study this topic on YouTube, e.g. 'MIT physics lectures' or 'Khan Academy calculus'>
If no external learning resources are featured, write:
[RESOURCES & TUTORIALS]: NONE

[PRODUCTS]:
If any specific textbooks, study tools, lab equipment, or calculators are recommended:
- PRODUCT: <Item/Book Name> | PRICE: <Price if stated, or 'N/A'> | SEARCH: <Targeted search keywords to buy this item online>
If none, write:
[PRODUCTS]: NONE

---
[DETAILS]:
- Subject Area & Target Concept:
- Theoretical Foundations & In-Depth Explanation:
- Key Laws, Formulas, Dates or Core Definitions:
- Practical Analogies & Real-World Case Studies:
- Summary & Core Study Takeaways:
"""
    elif "tutorial" in clean_mode or "tech" in clean_mode or "code" in clean_mode or "how-to" in clean_mode or "howto" in clean_mode or "diy" in clean_mode:
        return """
Analyze this video and extract detailed step-by-step tutorial notes, procedures, and learning resources.
Structure your response as follows:
[CATEGORY]: TUTORIAL
[TITLE]: <Clear tutorial topic or project title, max 6-8 words>
[SUMMARY]: <A 2-3 sentence overview of what is taught, built, or scheduled>

[RESOURCES & TUTORIALS]:
For EVERY tutorial, lecture, course, framework, library, tool, or roadmap milestone mentioned or recommended in this video (especially YouTube tutorials, Stanford/MIT lectures, GitHub repos, documentation):
List each one in this exact line format:
- RESOURCE: <Tutorial or Course or Topic Name> | PLATFORM: <YouTube | GitHub | Documentation | Course> | SEARCH: <Targeted search query to find and watch this exact tutorial on YouTube, e.g. 'Stanford LLM lectures' or 'LangChain tutorial for beginners'>
If no external tutorials, courses, or tools are mentioned, write:
[RESOURCES & TUTORIALS]: NONE

[PRODUCTS]:
If any specific physical tech gadgets, hardware, devices, tools, craft supplies, or peripherals are featured or recommended to buy, list each one in this exact line format:
- PRODUCT: <Brand/Model Name> | PRICE: <Price or price range if stated, or 'N/A'> | SEARCH: <Targeted search keywords to buy this item online>
CRITICAL NEGATIVE GUARDRAIL: DO NOT list software, APIs, coding libraries, plugins, AI models, frameworks, or web tools under [PRODUCTS]. Software and AI models belong EXCLUSIVELY under [RESOURCES & TUTORIALS].
If no physical hardware or gadgets are featured, write:
[PRODUCTS]: NONE

---
[DETAILS]:
- Prerequisites & Tools Needed:
- Step-by-Step Instructions / Roadmap:
- Exact Commands / Code Snippets / Action Steps:
- Common Gotchas & Best Practices:
"""
    elif "workout" in clean_mode or "fitness" in clean_mode or "gym" in clean_mode:
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
    elif "finance" in clean_mode or "business" in clean_mode or "invest" in clean_mode or "money" in clean_mode:
        return """
Analyze this video and extract financial, investment, or business strategy insights.
Structure your response as follows:
[CATEGORY]: FINANCE_BUSINESS
[TITLE]: <Core financial topic or company title, max 6-8 words>
[SUMMARY]: <A 2-3 sentence executive overview of the financial strategy or market insight>

[RESOURCES & TUTORIALS]:
If any specific finance books, courses, YouTube analysis channels, or data platforms are recommended:
- RESOURCE: <Resource Name> | PLATFORM: <YouTube | Book | Course> | SEARCH: <Targeted YouTube search query>
If none, write:
[RESOURCES & TUTORIALS]: NONE

[PRODUCTS]:
If any books, financial tools, software, or planners are featured:
- PRODUCT: <Item/Book Name> | PRICE: <Price if stated, or 'N/A'> | SEARCH: <Targeted search keywords to buy this item online>
If none, write:
[PRODUCTS]: NONE

---
[DETAILS]:
- Market Context & Thesis:
- Key Numbers, Metrics & Financial Rules:
- Step-by-Step Strategy & Execution:
- Risk Factors, Pitfalls & Disclaimer:
"""
    elif "beauty" in clean_mode or "fashion" in clean_mode or "skincare" in clean_mode or "makeup" in clean_mode:
        return """
Analyze this video and extract beauty, skincare, or fashion styling details.
Structure your response as follows:
[CATEGORY]: BEAUTY_FASHION
[TITLE]: <Descriptive style or routine title, max 6-8 words>
[SUMMARY]: <A 2-3 sentence overview of the style, look, or skincare regimen>

[PRODUCTS]:
For EVERY cosmetic, skincare product, hair styling tool, or clothing item showcased:
- PRODUCT: <Brand & Shade / Product Name> | PRICE: <Price if stated, or 'N/A'> | SEARCH: <Targeted search keywords to buy this item online>
If none, write:
[PRODUCTS]: NONE

---
[DETAILS]:
- Skin/Hair Type & Look Objective:
- Product Application Order & Techniques:
- Step-by-Step Styling/Routine Guide:
- Pro-Tips & Common Mistakes:
"""
    elif "summary" in clean_mode or "knowledge" in clean_mode or "hack" in clean_mode or "productivity" in clean_mode:
        return """
Analyze this video and extract an executive summary with key takeaways and life hacks.
Structure your response as follows:
[CATEGORY]: LIFE_HACKS
[TITLE]: <Core topic title, max 6-8 words>
[SUMMARY]: <A 2-3 sentence executive summary>

[RESOURCES & TUTORIALS]:
If any specific lectures, YouTube tutorials, books, or online courses are recommended or cited, list each one in this line format:
- RESOURCE: <Resource Name> | PLATFORM: <YouTube | Book | Course> | SEARCH: <Targeted YouTube search query to find and study it>
If no external learning resources are featured, write:
[RESOURCES & TUTORIALS]: NONE

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

First, classify the video into one of these specific CATEGORIES:
- EDUCATIONAL: Academic concepts, science, history, deep dive explainers, theory, math, astronomy, or intellectual knowledge.
- TUTORIAL: Step-by-step how-to guides, coding, software walkthroughs, tech roadmaps, DIY crafts, editing, or hands-on procedures.
- KITCHEN_FINDS: Kitchen utensils, smart gadgets, food storage organizers, cookware reviews, or Amazon kitchen finds.
- RECIPE: Actual cooking, baking, seasoning, or food/drink preparation with edible ingredients and culinary steps.
- PRODUCT_FINDS: Consumer electronics, unboxings, everyday gadget hauls, tools, or lifestyle gear reviews.
- WORKOUT: Fitness routines, gym exercises, yoga, bodyweight movements, or sports training.
- FINANCE_BUSINESS: Personal finance, investing, stock market, crypto, business breakdowns, or economics.
- TRAVEL_GUIDE: Destinations, places to visit, restaurants, itinerary tips, or city guides.
- BEAUTY_FASHION: Makeup tutorials, skincare routines, hairstyle guides, or clothing outfit styling.
- LIFE_HACKS: Everyday life shortcuts, organization tricks, or productivity habits.
- GENERAL: Any other informative or entertainment content.

CRITICAL CLASSIFICATION RULES:
1. EDUCATIONAL vs TUTORIAL:
   - If the video explains a concept, science, history, or knowledge topic without hands-on build steps -> EDUCATIONAL.
   - If the video provides step-by-step instructions on how to build, code, fix, configure, or do something -> TUTORIAL.
2. KITCHEN_FINDS vs RECIPE:
   - If the video demonstrates kitchen utensils, storage organizers, gadgets, or Amazon finds, DO NOT classify it as RECIPE. Classify it as KITCHEN_FINDS!
   - Only classify as RECIPE if someone is actually preparing, seasoning, cooking, or baking food/drinks with edible ingredients.
3. PRODUCT_FINDS vs BEAUTY_FASHION:
   - If cosmetics, skincare, or fashion -> BEAUTY_FASHION.
   - If electronics, gadgets, or tools -> PRODUCT_FINDS.

Structure your response strictly as follows:
[CATEGORY]: <EDUCATIONAL | TUTORIAL | KITCHEN_FINDS | RECIPE | PRODUCT_FINDS | WORKOUT | FINANCE_BUSINESS | TRAVEL_GUIDE | BEAUTY_FASHION | LIFE_HACKS | GENERAL>
[TITLE]: <A clear, descriptive title-cased name for this video, max 6-8 words>
[SUMMARY]: <A 2-3 sentence executive summary of what this video demonstrates, explains, or reviews>

[RESOURCES & TUTORIALS]:
If this video recommends or mentions tutorials, lectures, courses, frameworks, libraries, tools, or learning roadmaps (e.g. YouTube tutorials, Stanford/MIT lectures, GitHub repos, documentation):
List each one in this exact line format:
- RESOURCE: <Tutorial or Course or Topic Name> | PLATFORM: <YouTube | GitHub | Documentation | Course> | SEARCH: <Targeted search query to find and watch this exact tutorial on YouTube, e.g. 'Stanford LLM lectures' or 'LangChain tutorial'>
If no external tutorials or learning resources are featured, write:
[RESOURCES & TUTORIALS]: NONE

[PRODUCTS]:
For EVERY physical item, physical gadget, cosmetic, book, or hardware tool showcased, reviewed, or unboxed in this video, list each one in this exact line format:
- PRODUCT: <Brand & Model / Item Name> | PRICE: <Price if stated or estimated, e.g. Under ₹1000, or 'N/A'> | SEARCH: <Targeted search query to find and buy this exact item online>

CRITICAL NEGATIVE GUARDRAIL: DO NOT list software, APIs, coding libraries, plugins, AI models, frameworks, or web services under [PRODUCTS]. Software and AI models belong EXCLUSIVELY under [RESOURCES & TUTORIALS]. If no tangible physical products or hardware equipment are featured, write:
[PRODUCTS]: NONE

---
[DETAILS]:
(Provide rich, comprehensive, actionable details tailored to the category):
- If EDUCATIONAL: Core concepts, theoretical foundations, key definitions, real-world examples, and key study takeaways.
- If TUTORIAL: Prerequisites & tools, step-by-step procedures/roadmap, exact commands/code, and tips/pitfalls.
- If KITCHEN_FINDS or PRODUCT_FINDS: List each item with key features, usability tips, and pros/cons.
- If RECIPE: Full ingredients with exact measurements, equipment needed, prep & cook time, step-by-step instructions, and chef tips.
- If WORKOUT: Target muscles, equipment needed, warm-up, each exercise with sets x reps and rest intervals, and form cues.
- If FINANCE_BUSINESS: Key financial thesis, metrics/formulas, step-by-step strategy, and risk factors.
- If TRAVEL_GUIDE: Place names, exact locations, recommendations, pricing, and itinerary tips.
- If BEAUTY_FASHION: Target look, product order, step-by-step routine, and pro tips.
- If LIFE_HACKS or GENERAL: Core principles, bulleted step-by-step breakdown, and actionable takeaways.

Be thorough, precise, and practical. Do not omit crucial steps, tutorial names, or product names.
"""

def build_product_store_links(search_query: str, affiliate_tags: dict = None, category: str = "RECIPE") -> dict:
    """
    Constructs 1-click store search links with affiliate/aggregator parameters.
    Contextually routes storefronts based on verified domain category:
    - RECIPE / Culinary: Quick Commerce (Blinkit, Zepto, Instamart, JioMart) + Amazon Fresh / Grocery + BigBasket. (Strictly omits fashion stores).
    - BEAUTY_FASHION / OOTD: Myntra, AJIO, Meesho, Amazon Fashion.
    - KITCHEN_FINDS / GADGET / TECH / GENERAL: Amazon Prime, Flipkart, Shopsy, Google Shopping.
    Supports direct tags as well as Cuelinks and EarnKaro aggregators.
    """
    if affiliate_tags is None:
        affiliate_tags = {}

    clean_q = search_query.strip()
    encoded_q = urllib.parse.quote_plus(clean_q)
    cuelinks_id = (affiliate_tags.get("cuelinks") or "").strip()
    earnkaro_id = (affiliate_tags.get("earnkaro") or "").strip()
    cat_upper = (category or "RECIPE").upper()

    is_recipe = any(c in cat_upper for c in ["RECIPE", "COOK", "BAKE", "CULINARY", "FOOD"])
    is_fashion = any(c in cat_upper for c in ["BEAUTY_FASHION", "FASHION", "OOTD", "STYLE", "BEAUTY", "APPAREL"])
    is_tutorial = any(c in cat_upper for c in ["TUTORIAL", "TECH_TUTORIAL", "EDUCATIONAL", "CODE", "DIY", "HOWTO", "HOW-TO"])

    # --- 1. Amazon ---
    amz_tag = (affiliate_tags.get("amazon") or "").strip()
    amz_param = f"&tag={urllib.parse.quote_plus(amz_tag)}" if amz_tag else ""
    if is_recipe:
        amazon_url = f"https://www.amazon.in/s?k={encoded_q}&i=now-store{amz_param}"
    elif is_fashion:
        amazon_url = f"https://www.amazon.in/s?k={encoded_q}&i=apparel{amz_param}"
    else:
        amazon_url = f"https://www.amazon.in/s?k={encoded_q}{amz_param}"
    amazon_global_url = f"https://www.amazon.com/s?k={encoded_q}{amz_param}"

    # --- 2. Flipkart ---
    raw_flp_url = f"https://www.flipkart.com/search?q={encoded_q}"
    flp_tag = (affiliate_tags.get("flipkart") or "").strip()
    if cuelinks_id:
        flipkart_url = f"https://linksredirect.com/?cid={urllib.parse.quote_plus(cuelinks_id)}&url={urllib.parse.quote_plus(raw_flp_url)}"
    elif earnkaro_id:
        flipkart_url = f"https://ekaro.in/enlinks?r={urllib.parse.quote_plus(earnkaro_id)}&url={urllib.parse.quote_plus(raw_flp_url)}"
    elif flp_tag:
        flipkart_url = f"https://www.flipkart.com/search?q={encoded_q}&affid={urllib.parse.quote_plus(flp_tag)}"
    else:
        flipkart_url = raw_flp_url

    # --- 3. Fashion Marketplaces (Myntra, Meesho, AJIO, Nykaa) ---
    # Suppressed for recipes and tutorials; populated for fashion or general/all categories
    if is_fashion or (cat_upper not in ["RECIPE", "CULINARY", "COOKING", "FOOD"] and not is_recipe and not is_tutorial):
        raw_myntra_url = f"https://www.myntra.com/{encoded_q}"
        if cuelinks_id:
            myntra_url = f"https://linksredirect.com/?cid={urllib.parse.quote_plus(cuelinks_id)}&url={urllib.parse.quote_plus(raw_myntra_url)}"
        elif earnkaro_id:
            myntra_url = f"https://ekaro.in/enlinks?r={urllib.parse.quote_plus(earnkaro_id)}&url={urllib.parse.quote_plus(raw_myntra_url)}"
        else:
            myntra_url = raw_myntra_url

        msh_tag = (affiliate_tags.get("meesho") or "").strip()
        raw_meesho_url = f"https://www.meesho.com/search?q={encoded_q}"
        if cuelinks_id:
            meesho_url = f"https://linksredirect.com/?cid={urllib.parse.quote_plus(cuelinks_id)}&url={urllib.parse.quote_plus(raw_meesho_url)}"
        elif earnkaro_id:
            meesho_url = f"https://ekaro.in/enlinks?r={urllib.parse.quote_plus(earnkaro_id)}&url={urllib.parse.quote_plus(raw_meesho_url)}"
        elif msh_tag:
            meesho_url = f"https://www.meesho.com/search?q={encoded_q}&utm_source=affiliate&utm_campaign={urllib.parse.quote_plus(msh_tag)}"
        else:
            meesho_url = raw_meesho_url

        raw_ajio_url = f"https://www.ajio.com/search/?text={encoded_q}"
        if cuelinks_id:
            ajio_url = f"https://linksredirect.com/?cid={urllib.parse.quote_plus(cuelinks_id)}&url={urllib.parse.quote_plus(raw_ajio_url)}"
        elif earnkaro_id:
            ajio_url = f"https://ekaro.in/enlinks?r={urllib.parse.quote_plus(earnkaro_id)}&url={urllib.parse.quote_plus(raw_ajio_url)}"
        else:
            ajio_url = raw_ajio_url

        raw_nykaa_url = f"https://www.nykaa.com/search/result/?q={encoded_q}"
        if cuelinks_id:
            nykaa_url = f"https://linksredirect.com/?cid={urllib.parse.quote_plus(cuelinks_id)}&url={urllib.parse.quote_plus(raw_nykaa_url)}"
        elif earnkaro_id:
            nykaa_url = f"https://ekaro.in/enlinks?r={urllib.parse.quote_plus(earnkaro_id)}&url={urllib.parse.quote_plus(raw_nykaa_url)}"
        else:
            nykaa_url = raw_nykaa_url
    else:
        # Contextual suppression for non-fashion domains
        myntra_url = ""
        meesho_url = ""
        ajio_url = ""
        nykaa_url = ""

    # --- 4. Value Commerce & Google Shopping ---
    raw_shopsy_url = f"https://www.shopsy.in/search?q={encoded_q}"
    if cuelinks_id:
        shopsy_url = f"https://linksredirect.com/?cid={urllib.parse.quote_plus(cuelinks_id)}&url={urllib.parse.quote_plus(raw_shopsy_url)}"
    elif earnkaro_id:
        shopsy_url = f"https://ekaro.in/enlinks?r={urllib.parse.quote_plus(earnkaro_id)}&url={urllib.parse.quote_plus(raw_shopsy_url)}"
    else:
        shopsy_url = raw_shopsy_url

    google_shopping_url = f"https://www.google.com/search?tbm=shop&q={encoded_q}"

    # --- 5. Quick Commerce & Grocery ---
    # Suppressed for tutorials and fashion; populated for recipes and general/all
    if is_recipe or (not is_tutorial and not is_fashion):
        blinkit_url = f"https://blinkit.com/s/?q={encoded_q}"
        zepto_url = f"https://www.zeptonow.com/search?q={encoded_q}"
        instamart_url = f"https://www.swiggy.com/instamart/search?custom_back=true&query={encoded_q}"
        jiomart_url = f"https://www.jiomart.com/search/{encoded_q}"
        bigbasket_url = f"https://www.bigbasket.com/ps/?q={encoded_q}"
    else:
        blinkit_url = ""
        zepto_url = ""
        instamart_url = ""
        jiomart_url = ""
        bigbasket_url = ""

    return {
        # Core
        "amazon_url": amazon_url,
        "amazon_global_url": amazon_global_url,
        "flipkart_url": flipkart_url,
        # Fashion (conditionally populated)
        "myntra_url": myntra_url,
        "meesho_url": meesho_url,
        "ajio_url": ajio_url,
        "nykaa_url": nykaa_url,
        # Tech & Value Commerce
        "shopsy_url": shopsy_url,
        "google_shopping_url": google_shopping_url,
        # Quick Commerce & Grocery
        "blinkit_url": blinkit_url,
        "zepto_url": zepto_url,
        "instamart_url": instamart_url,
        "jiomart_url": jiomart_url,
        "bigbasket_url": bigbasket_url
    }

def parse_extracted_content(raw_text: str, affiliate_tags: dict = None) -> dict:
    """
    Parses structured Gemini response into clean fields: category, title, summary, products, details, and safe filename.
    Attaches affiliate tracking tags to Amazon, Flipkart, and Meesho links if configured.
    """
    if affiliate_tags is None:
        affiliate_tags = get_affiliate_tags()

    category = "RECIPE"
    title = "Extracted_Content"
    summary = ""
    details = raw_text
    products = []
    promoted_software_resources = []

    cat_match = re.search(r'\[CATEGORY\]:\s*([A-Za-z_]+)', raw_text, re.IGNORECASE)
    if cat_match:
        found_cat = cat_match.group(1).upper().strip()
        if any(c in found_cat for c in ["EDUCATIONAL", "EDUCATION", "EXPLAINER", "ACADEMIC", "SCIENCE", "HISTORY", "THEORY"]):
            category = "EDUCATIONAL"
        elif any(c in found_cat for c in ["TUTORIAL", "TECH_TUTORIAL", "TECH", "CODE", "PROGRAMMING", "HOW_TO", "HOWTO", "DIY", "GUIDE"]):
            category = "TUTORIAL"
        elif any(c in found_cat for c in ["KITCHEN_FINDS", "KITCHEN_FIND", "KITCHEN_GADGET", "HOME_FIND"]):
            category = "KITCHEN_FINDS"
        elif any(c in found_cat for c in ["PRODUCT_FINDS", "PRODUCT_FIND", "UNBOXING", "PRODUCT_REVIEW", "HAUL", "AMAZON_FIND"]):
            category = "PRODUCT_FINDS"
        elif any(c in found_cat for c in ["WORKOUT", "FITNESS", "EXERCISE", "GYM", "YOGA"]):
            category = "WORKOUT"
        elif any(c in found_cat for c in ["FINANCE_BUSINESS", "FINANCE", "BUSINESS", "INVESTING", "MONEY", "CRYPTO", "STOCKS"]):
            category = "FINANCE_BUSINESS"
        elif any(c in found_cat for c in ["TRAVEL_GUIDE", "TRAVEL", "PLACE", "RESTAURANT", "FOOD_GUIDE", "ITINERARY"]):
            category = "TRAVEL_GUIDE"
        elif any(c in found_cat for c in ["BEAUTY_FASHION", "BEAUTY", "SKINCARE", "MAKEUP", "FASHION", "STYLE", "GROOMING"]):
            category = "BEAUTY_FASHION"
        elif any(c in found_cat for c in ["LIFE_HACKS", "LIFE_HACK", "PRODUCTIVITY", "HACK", "HABIT"]):
            category = "LIFE_HACKS"
        elif any(c in found_cat for c in ["KNOWLEDGE_SUMMARY", "KNOWLEDGE", "SUMMARY", "BOOK"]):
            category = "EDUCATIONAL"
        elif any(c in found_cat for c in ["RECIPE", "COOK", "BAKE"]):
            category = "RECIPE"
        else:
            category = "GENERAL"
    else:
        # Fallback category detection if [CATEGORY] tag is omitted in output
        header_sample = raw_text[:400].upper()
        if any(k in header_sample for k in ["EDUCATIONAL", "EXPLAINER", "CONCEPT", "SCIENCE", "HISTORY", "THEORY", "LECTURE", "ACADEMIC"]):
            category = "EDUCATIONAL"
        elif any(k in header_sample for k in ["TUTORIAL", "TECH TUTORIAL", "TECH_TUTORIAL", "ROADMAP", "PROGRAMMING", "AI ENGINEER", "LLM", "HOW TO", "HOW-TO", "DIY", "💻"]):
            category = "TUTORIAL"
        elif any(k in header_sample for k in ["KITCHEN FINDS", "KITCHEN_FINDS", "KITCHEN GADGET", "HOME FINDS"]):
            category = "KITCHEN_FINDS"
        elif any(k in header_sample for k in ["PRODUCT FINDS", "AMAZON FINDS", "UNBOXING", "HAUL"]):
            category = "PRODUCT_FINDS"
        elif any(k in header_sample for k in ["WORKOUT", "FITNESS", "EXERCISE", "ROUTINE", "GYM", "YOGA"]):
            category = "WORKOUT"
        elif any(k in header_sample for k in ["FINANCE", "BUSINESS", "INVESTING", "STOCKS", "MONEY", "CRYPTO"]):
            category = "FINANCE_BUSINESS"
        elif any(k in header_sample for k in ["TRAVEL GUIDE", "TRAVEL_GUIDE", "ITINERARY", "PLACES TO VISIT"]):
            category = "TRAVEL_GUIDE"
        elif any(k in header_sample for k in ["BEAUTY", "SKINCARE", "MAKEUP", "FASHION", "HAIRSTYLE"]):
            category = "BEAUTY_FASHION"
        elif any(k in header_sample for k in ["LIFE HACK", "PRODUCTIVITY", "HACK", "SUMMARY", "BOOK SUMMARY"]):
            category = "LIFE_HACKS"
        elif any(k in header_sample for k in ["RECIPE", "INGREDIENTS", "COOKING", "CHEF", "PREP TIME", "BAKING"]):
            category = "RECIPE"
        else:
            category = "RECIPE"



    title_match = re.search(r'\[TITLE\]:\s*(.+)', raw_text, re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = extract_apt_recipe_title(raw_text)

    summary_match = re.search(r'\[SUMMARY\]:\s*(.+?)(?=\n---\n|\[DETAILS\]|\[PRODUCTS\]|\[RESOURCES(?:\s*&\s*TUTORIALS)?\]|$)', raw_text, re.DOTALL | re.IGNORECASE)
    if summary_match:
        summary = summary_match.group(1).strip()
        summary = re.sub(r'\[(?:RESOURCES(?:\s*&\s*TUTORIALS)?|PRODUCTS)\]:.*', '', summary, flags=re.DOTALL | re.IGNORECASE).strip()

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

                # Digital/Software Guardrail: Exclude software, AI models, plugins, APIs from e-commerce products
                is_tutorial_cat = category in ["TUTORIAL", "TECH_TUTORIAL", "EDUCATIONAL", "LIFE_HACKS"]
                is_digital_tool = any(kw in p_name_clean.lower() for kw in [
                    "ai model", "model", "plugin", "installer", "api", "framework",
                    "library", "llm", "software", "repo", "repository", "package",
                    "extension", "sdk", "algorithm", "prompt", "token", "cli",
                    "sqlite", "claude-mem", "claude code", "gemini", "gpt",
                    "deepseek", "kimi", "glm", "llama", "mistral", "chatgpt"
                ]) or any(kw in (p_price or "").lower() for kw in ["free", "bundled", "open source", "n/a (likely free", "free tier"])

                if is_tutorial_cat and is_digital_tool:
                    promoted_software_resources.append({
                        "name": p_name_clean,
                        "platform": "Documentation",
                        "query": p_search_clean
                    })
                    continue

                links = build_product_store_links(p_search_clean, affiliate_tags, category=category)
                prod_entry = {
                    "name": p_name_clean,
                    "price": p_price if p_price and p_price.upper() not in ["N/A", "NONE", "NOT SPECIFIED"] else "",
                    "query": p_search_clean,
                }
                prod_entry.update(links)
                products.append(prod_entry)

    # Secondary Fallback: If no products were captured via [PRODUCTS] section but items are described in details
    if len(products) == 0 and category in ["KITCHEN_FINDS", "PRODUCT_FINDS", "BEAUTY_FASHION", "GENERAL"]:
        fallback_matches = re.findall(r'(?:^|\n)(?:###\s*\d+\.|\d+\.|\*)\s*\*\*([^*\n:]+)\*\*', raw_text)
        for f_item in fallback_matches:
            item_clean = f_item.strip()
            if len(item_clean) > 3 and not any(k in item_clean.lower() for k in ["features", "uses", "tips", "pros", "cons", "details", "summary", "instructions"]):
                links = build_product_store_links(item_clean, affiliate_tags, category=category)
                fallback_entry = {
                    "name": item_clean,
                    "price": "",
                    "query": item_clean,
                }
                fallback_entry.update(links)
                products.append(fallback_entry)



    # Extract Resources & Tutorials section (for TECH_TUTORIAL, Roadmaps, Courses, etc.)
    resources = []
    res_section_match = re.search(r'\[RESOURCES & TUTORIALS\]:\s*(.+?)(?=\n---\n|\[PRODUCTS\]|\[DETAILS\]|\[CATEGORY\]|\[TITLE\]|\[SUMMARY\]|$)', raw_text, re.DOTALL | re.IGNORECASE)
    if not res_section_match:
        res_section_match = re.search(r'\[RESOURCES\]:\s*(.+?)(?=\n---\n|\[PRODUCTS\]|\[DETAILS\]|$)', raw_text, re.DOTALL | re.IGNORECASE)

    if res_section_match:
        res_text = res_section_match.group(1).strip()
        if res_text.upper() != "NONE" and not res_text.upper().startswith("NONE"):
            for line in res_text.splitlines():
                line = line.strip()
                if not line or line.startswith(('#', '=')) or line.upper() == "NONE":
                    continue
                r_match = re.search(r'RESOURCE:\s*([^|]+)(?:\|\s*PLATFORM:\s*([^|]+))?(?:\|\s*SEARCH:\s*(.+))?', line, re.IGNORECASE)
                if r_match:
                    r_name = r_match.group(1).strip()
                    r_plat = (r_match.group(2) or "YouTube").strip()
                    r_search = (r_match.group(3) or "").strip() or r_name
                else:
                    cleaned_line = re.sub(r'^[-*•\d\.]+\s*', '', line).strip()
                    if len(cleaned_line) > 3 and not cleaned_line.startswith('['):
                        r_name = cleaned_line
                        r_plat = "YouTube"
                        r_search = f"{cleaned_line} tutorial"
                    else:
                        continue

                r_name_clean = re.sub(r'[*_#"\u201c\u201d\']', '', r_name).strip()
                r_search_clean = re.sub(r'[*_#"\u201c\u201d\']', '', r_search).strip()
                if not r_name_clean:
                    continue

                encoded_q = urllib.parse.quote_plus(r_search_clean)
                resources.append({
                    "name": r_name_clean,
                    "platform": r_plat,
                    "query": r_search_clean,
                    "youtube_url": f"https://www.youtube.com/results?search_query={encoded_q}",
                    "google_url": f"https://www.google.com/search?q={encoded_q}",
                    "github_url": f"https://github.com/search?q={encoded_q}"
                })

    # Fallback for TUTORIAL, EDUCATIONAL, LIFE_HACKS or Roadmaps:
    # If no explicit [RESOURCES & TUTORIALS] were captured, extract topics from roadmap steps/bullets
    if len(resources) == 0 and category in ["TUTORIAL", "TECH_TUTORIAL", "EDUCATIONAL", "LIFE_HACKS", "KNOWLEDGE_SUMMARY", "FINANCE_BUSINESS", "GENERAL"]:
        step_matches = re.findall(r'(?:^|\n)(?:[-*•\d\.]+|###)\s*\*\*([^*\n:]+):\*\*\s*([^\n]+)', raw_text)
        for s_title, s_desc in step_matches:
            clean_s_title = re.sub(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|\&|\s|-|\d+\.)+', '', s_title, flags=re.IGNORECASE).strip(' -:')
            if not clean_s_title or any(k in clean_s_title.lower() for k in ["prerequisite", "tools", "instructions", "summary", "gotchas", "best practice"]):
                continue

            # Check if description mentions specific lectures/channels in parentheses (e.g., Stanford Engineering LLM lectures)
            specific_mention = re.search(r'\((?:e\.g\.,?|watch|see)\s*([^\)]+)\)', s_desc, re.IGNORECASE)
            if specific_mention:
                mention_text = specific_mention.group(1).strip()
                if any(m in mention_text.lower() for m in ["lecture", "tutorial", "course", "youtube", "stanford", "mit", "channel", "video"]):
                    yt_query = mention_text
                else:
                    yt_query = f"{clean_s_title} tutorial {mention_text}"
            else:
                yt_query = f"{clean_s_title} tutorial"

            encoded_q = urllib.parse.quote_plus(yt_query)
            resources.append({
                "name": clean_s_title,
                "platform": "YouTube",
                "query": yt_query,
                "youtube_url": f"https://www.youtube.com/results?search_query={encoded_q}",
                "google_url": f"https://www.google.com/search?q={encoded_q}",
                "github_url": f"https://github.com/search?q={encoded_q}"
            })

    # Merge any digital software items that were promoted from [PRODUCTS]
    if promoted_software_resources:
        existing_names = {r.get("name", "").lower() for r in resources}
        for psr in promoted_software_resources:
            if psr["name"].lower() not in existing_names:
                enc_q = urllib.parse.quote_plus(psr["query"])
                resources.append({
                    "name": psr["name"],
                    "platform": psr.get("platform", "Documentation"),
                    "query": psr["query"],
                    "youtube_url": f"https://www.youtube.com/results?search_query={enc_q}",
                    "google_url": f"https://www.google.com/search?q={enc_q}",
                    "github_url": f"https://github.com/search?q={enc_q}"
                })
                existing_names.add(psr["name"].lower())

    details_match = re.search(r'(?:\[DETAILS\]:|---\s*\n\[DETAILS\]:)\s*(.+)', raw_text, re.DOTALL | re.IGNORECASE)
    if details_match:
        details = details_match.group(1).strip()
        details = re.sub(r'\[PRODUCTS\]:\s*.+', '', details, flags=re.DOTALL | re.IGNORECASE).strip()
        details = re.sub(r'\[RESOURCES & TUTORIALS\]:\s*.+', '', details, flags=re.DOTALL | re.IGNORECASE).strip()
        details = re.sub(r'\[RESOURCES\]:\s*.+', '', details, flags=re.DOTALL | re.IGNORECASE).strip()

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
        "resources": resources,
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


def format_downloadable_txt(meta: Dict[str, Any]) -> str:
    """
    Formats structured intelligence into a clean, complete, downloadable .txt file.
    Guarantees actionable YouTube tutorial links, Google/GitHub links, and Shoppable product buy links are included.
    """
    formatted = f"""==================================================
{meta.get('emoji', '📝')} {meta.get('title', 'Extracted Content')} ({meta.get('category_name', 'General Intelligence')})
==================================================
"""
    if meta.get("summary"):
        clean_sum = meta['summary'].strip()
        clean_sum = re.sub(r'\[(?:RESOURCES(?:\s*&\s*TUTORIALS)?|PRODUCTS)\]:.*', '', clean_sum, flags=re.DOTALL | re.IGNORECASE).strip()
        formatted += f"\n📋 Summary:\n{clean_sum}\n"

    if meta.get("resources") and len(meta["resources"]) > 0:
        formatted += f"\n{'='*50}\n🎓 Recommended YouTube Tutorials & Learning Links:\n{'='*50}\n"
        for idx, r in enumerate(meta["resources"], 1):
            plat = r.get("platform", "YouTube")
            formatted += f"{idx}. {r.get('name', 'Tutorial')} ({plat})\n"
            if r.get("youtube_url"):
                formatted += f"   • ▶️ Watch on YouTube: {r['youtube_url']}\n"
            if r.get("google_url"):
                formatted += f"   • 🔍 Google Search: {r['google_url']}\n"
            if r.get("github_url") and any(k in f"{r.get('name', '')} {r.get('platform', '')}".lower() for k in ["github", "code", "project", "repo", "framework", "library", "git", "api"]):
                formatted += f"   • 🐙 GitHub Search: {r['github_url']}\n"
            formatted += "\n"

    if meta.get("products") and len(meta["products"]) > 0:
        cat_str = str(meta.get("category", "") or meta.get("category_name", "")).upper()
        is_recipe = any(k in cat_str for k in ["RECIPE", "FOOD", "COOKING"])
        is_fashion = any(k in cat_str for k in ["FASHION", "BEAUTY", "STYLE", "CLOTH"])
        formatted += f"\n{'='*50}\n🛍️ Featured Products & 1-Click Buy Links:\n{'='*50}\n"
        for idx, p in enumerate(meta["products"], 1):
            price_str = f" ({p['price']})" if p.get("price") else ""
            formatted += f"{idx}. {p['name']}{price_str}\n"
            if p.get("amazon_url"):
                amz_lbl = "Amazon Fresh" if is_recipe else ("Amazon Fashion" if is_fashion else "Amazon")
                formatted += f"   • {amz_lbl}: {p['amazon_url']}\n"
            if p.get("flipkart_url"):
                formatted += f"   • Flipkart: {p['flipkart_url']}\n"
            if p.get("myntra_url"):
                formatted += f"   • Myntra: {p['myntra_url']}\n"
            if p.get("meesho_url"):
                formatted += f"   • Meesho: {p['meesho_url']}\n"
            if p.get("ajio_url"):
                formatted += f"   • AJIO: {p['ajio_url']}\n"
            if p.get("blinkit_url"):
                formatted += f"   • Blinkit (10-Min): {p['blinkit_url']}\n"
            if p.get("zepto_url"):
                formatted += f"   • Zepto (10-Min): {p['zepto_url']}\n"
            if p.get("instamart_url"):
                formatted += f"   • Swiggy Instamart: {p['instamart_url']}\n"
            if p.get("bigbasket_url"):
                formatted += f"   • BigBasket: {p['bigbasket_url']}\n"
            if p.get("google_shopping_url"):
                formatted += f"   • Compare Stores: {p['google_shopping_url']}\n"
            formatted += "\n"

    clean_details = meta.get("details", "").strip()
    if clean_details:
        formatted += f"\n{'='*50}\nDetailed Steps & Notes:\n{'='*50}\n\n{clean_details}\n"

    return formatted


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

        # Step 3: Model execution priority covering all Gemini models in your account
        preferred_candidates = [
            "gemini-3.5-flash",       # Verified ultra-fast (1.5s - 13.5s) with full multimodal video & product extraction
            "gemini-3.6-flash",       # Gemini 3.6 Flash
            "gemini-3.7-flash",       # Gemini 3.7 Flash
            "gemini-3.8-flash",       # Gemini 3.8 Flash
            "gemini-3.5-flash-lite",  # Gemini 3.5 Flash Lite
            "gemini-3.1-pro",         # Gemini 3.1 Pro
            "gemini-3.1-flash-lite",  # Gemini 3.1 Flash Lite
            "gemini-3-flash",         # Gemini 3 Flash
            "gemini-2.5-flash",       # Gemini 2.5 Flash
            "gemini-2.5-pro",         # Gemini 2.5 Pro
            "gemini-2.5-flash-lite",  # Gemini 2.5 Flash Lite
            "gemini-2.0-flash",       # Gemini 2.0 Flash
            "gemini-2.0-flash-lite",  # Gemini 2.0 Flash Lite
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
        formatted_file_content = format_downloadable_txt(meta)


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

