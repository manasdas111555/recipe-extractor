import re
import urllib.parse
import requests
from pathlib import Path
from typing import Tuple

def get_default_country_code() -> str:
    """
    Detects default country calling code from system locale.
    Defaults to +91 (India) if system locale is Indian or fallback.
    """
    try:
        import locale
        loc_tuple = locale.getlocale()
        loc = (loc_tuple[0] or "").upper() if loc_tuple else ""
        if "INDIA" in loc or "IN" in loc:
            return "+91"
        elif "US" in loc or "UNITED_STATES" in loc or "CANADA" in loc:
            return "+1"
        elif "UK" in loc or "UNITED_KINGDOM" in loc or "GB" in loc:
            return "+44"
        elif "AUSTRALIA" in loc or "AU" in loc:
            return "+61"
        elif "UAE" in loc or "AE" in loc:
            return "+971"
        elif "SINGAPORE" in loc or "SG" in loc:
            return "+65"
        elif "GERMANY" in loc or "DE" in loc:
            return "+49"
    except Exception:
        pass
    return "+91"

def format_phone_number(phone: str) -> str:
    """Clean phone number and format with country code."""
    phone = phone.strip().replace(" ", "").replace("-", "").replace("+", "")
    return phone


def validate_phone_number(country_code: str, local_number: str) -> Tuple[bool, str]:
    """
    Validates mobile phone number based on selected country calling code.
    Returns (is_valid, validation_message).
    """
    clean_cc = (country_code or "+91").strip().replace(" ", "").replace("-", "")
    if not clean_cc.startswith("+"):
        clean_cc = "+" + clean_cc
    
    clean_num = re.sub(r'[\s\-\(\)\.]', '', local_number or "")
    if clean_num.startswith("0"):
        clean_num = clean_num.lstrip("0")

    if not clean_num:
        return False, "Please enter a mobile phone number."
    
    if not clean_num.isdigit():
        return False, "Phone number must contain only numeric digits."

    # Country-specific validation rules
    if clean_cc in ["+91", "91"]:
        # India: exactly 10 digits starting with 6, 7, 8, or 9
        if len(clean_num) == 12 and clean_num.startswith("91"):
            clean_num = clean_num[2:]
        if len(clean_num) != 10:
            return False, f"Indian mobile numbers must be exactly 10 digits (entered {len(clean_num)} digits)."
        if clean_num[0] not in "6789":
            return False, "Indian mobile numbers must start with 6, 7, 8, or 9."
        return True, ""
    elif clean_cc in ["+1", "1"]:
        # US / Canada: exactly 10 digits
        if len(clean_num) != 10:
            return False, f"US/Canada numbers must be exactly 10 digits (entered {len(clean_num)} digits)."
        return True, ""
    elif clean_cc in ["+44", "44"]:
        # UK: 10 or 11 digits
        if len(clean_num) not in [10, 11]:
            return False, f"UK numbers must be 10 or 11 digits (entered {len(clean_num)} digits)."
        return True, ""
    elif clean_cc in ["+971", "971"]:
        # UAE: 9 digits
        if len(clean_num) != 9:
            return False, f"UAE numbers must be 9 digits (entered {len(clean_num)} digits)."
        return True, ""
    elif clean_cc in ["+65", "65"]:
        # Singapore: 8 digits
        if len(clean_num) != 8:
            return False, f"Singapore numbers must be 8 digits (entered {len(clean_num)} digits)."
        return True, ""
    else:
        # General international validation: 7 to 15 digits
        if len(clean_num) < 7 or len(clean_num) > 15:
            return False, f"International numbers must be between 7 and 15 digits (entered {len(clean_num)} digits)."
        return True, ""


def get_recipe_display_name(txt_file_path: str) -> str:
    """Extract readable recipe title from filename."""
    stem = Path(txt_file_path).stem
    return stem.replace("_", " ").strip()

def get_category_header(recipe_name: str, category: str = "RECIPE") -> Tuple[str, str]:
    """Returns (header_caption, emoji_icon) based on category."""
    cat = (category or "RECIPE").upper()
    if "EDUCATIONAL" in cat or "ACADEMIC" in cat or "EXPLAINER" in cat or "SCIENCE" in cat:
        return f"Here is educational explainer & study notes for - {recipe_name} !", "🎓"
    elif "TUTORIAL" in cat or "TECH" in cat or "CODE" in cat or "HOW_TO" in cat or "DIY" in cat:
        return f"Here is tutorial guide & learning links for - {recipe_name} !", "💻"
    elif "KITCHEN" in cat:
        return f"Here is kitchen finds & product buy links for - {recipe_name} !", "🛍️"
    elif "PRODUCT" in cat or "UNBOXING" in cat or "HAUL" in cat:
        return f"Here is product finds & buy links for - {recipe_name} !", "📦"
    elif "WORKOUT" in cat or "FITNESS" in cat or "EXERCISE" in cat:
        return f"Here is workout routine for - {recipe_name} !", "🏋️"
    elif "FINANCE" in cat or "BUSINESS" in cat or "INVEST" in cat:
        return f"Here is finance & business breakdown for - {recipe_name} !", "💰"
    elif "TRAVEL" in cat or "PLACE" in cat:
        return f"Here is travel guide for - {recipe_name} !", "✈️"
    elif "BEAUTY" in cat or "FASHION" in cat or "SKINCARE" in cat:
        return f"Here is beauty & style guide for - {recipe_name} !", "💄"
    elif "HACK" in cat or "PRODUCTIVITY" in cat:
        return f"Here is life hacks & productivity tips for - {recipe_name} !", "💡"
    elif "KNOWLEDGE" in cat or "SUMMARY" in cat:
        return f"Here is key summary notes for - {recipe_name} !", "💡"
    elif "GENERAL" in cat:
        return f"Here is key takeaways for - {recipe_name} !", "📝"
    else:
        return f"Here is recipe file for - {recipe_name} !", "🍳"


def generate_whatsapp_deep_link(phone_number: str, recipe_txt_path: str, recipe_content: str, category: str = "RECIPE", products: list = None, resources: list = None) -> str:
    """
    Generates a WhatsApp Deep Link (wa.me / api.whatsapp.com).
    When opened on mobile or web, it opens WhatsApp with caption, clickable links & content pre-filled!
    Prioritizes clickable tutorial/resource links and shoppable product links at the top so they are never truncated.
    """
    clean_phone = format_phone_number(phone_number)
    recipe_name = get_recipe_display_name(recipe_txt_path)
    header, icon = get_category_header(recipe_name, category)
    top_header = f"{icon} *{header}*"
    
    # 1. Build Clickable Resource / Tutorial Links
    resource_section = ""
    if resources and len(resources) > 0:
        resource_section = "🎓 *Recommended YouTube Tutorials & Learning Links:*\n"
        for r in resources[:5]:
            r_name = r.get("name", "").strip()
            yt_url = r.get("youtube_url", "").strip()
            plat = r.get("platform", "").strip()
            plat_str = f" ({plat})" if plat and plat.lower() != "youtube" else ""
            resource_section += f"• *{r_name}*{plat_str}\n  ▶️ Watch: {yt_url}\n"

    # 2. Build Clickable Product & Quick-Commerce Links
    product_section = ""
    if products and len(products) > 0:
        product_section = "🛍️ *Featured Products & 1-Click Buy Links:*\n"
        for p in products[:5]:
            price_tag = f" ({p['price']})" if p.get("price") else ""
            product_section += f"• *{p['name']}*{price_tag}\n  🛒 Amazon: {p['amazon_url']}\n"
            if p.get("flipkart_url"):
                product_section += f"  ⚡ Flipkart: {p['flipkart_url']}\n"
            if p.get("myntra_url"):
                product_section += f"  🛍️ Myntra: {p['myntra_url']}\n"
            if p.get("meesho_url"):
                product_section += f"  🌸 Meesho: {p['meesho_url']}\n"
            if p.get("blinkit_url"):
                product_section += f"  ⚡ 10-Min Delivery: {p['blinkit_url']}\n"

    links_parts = []
    if resource_section:
        links_parts.append(resource_section.strip())
    if product_section:
        links_parts.append(product_section.strip())
    links_block = "\n\n".join(links_parts).strip()

    # 3. Extract precise summary (omit the voluminous raw translation/detailed steps)
    raw_text = recipe_content or ""
    summary_match = re.search(r'📋\s*Summary:\s*(.+?)(?=\n\s*(?:={3,}|[🎓🛍️A-Z#])|\Z)', raw_text, re.DOTALL | re.IGNORECASE)
    if summary_match:
        summary_text = summary_match.group(1).strip()
    else:
        # If no explicit summary header, extract clean initial lines
        clean_first_para = re.sub(r'={3,}.*?={3,}', '', raw_text, flags=re.DOTALL).strip()
        summary_text = clean_first_para[:450].strip()

    # Strip any internal prompt tags if present
    summary_text = re.sub(r'\[(?:RESOURCES(?:\s*&\s*TUTORIALS)?|PRODUCTS)\]:.*', '', summary_text, flags=re.DOTALL | re.IGNORECASE).strip()

    # 4. Assemble message: Header -> Precise Summary -> Actionable Links -> Download Notice
    msg_parts = [top_header]
    if summary_text:
        msg_parts.append(f"📋 *Summary:*\n{summary_text}")
    if links_block:
        msg_parts.append(links_block)
    
    msg_parts.append("💡 _Full detailed steps, code & notes available in the downloaded .txt file!_")
    full_message = "\n\n".join(msg_parts).strip()
        
    encoded_text = urllib.parse.quote(full_message)
    return f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_text}"

def send_via_callmebot_api(phone_number: str, recipe_txt_path: str, recipe_content: str, api_key: str, category: str = "RECIPE", products: list = None, resources: list = None) -> Tuple[bool, str]:
    """
    Sends WhatsApp message directly via free CallMeBot API with precise summary, product buy links and YouTube tutorial links.
    """
    if not api_key:
        return False, "CallMeBot API key not provided."
        
    clean_phone = format_phone_number(phone_number)
    recipe_name = get_recipe_display_name(recipe_txt_path)
    header, icon = get_category_header(recipe_name, category)
    top_header = f"{icon} *{header}*"
    
    product_section = ""
    if products and len(products) > 0:
        product_section = "🛍️ *Featured Products:*\n"
        for p in products[:3]:
            product_section += f"• {p['name']}: {p['amazon_url']}\n"

    resource_section = ""
    if resources and len(resources) > 0:
        resource_section = "🎓 *Recommended Tutorials:*\n"
        for r in resources[:3]:
            resource_section += f"• {r['name']}: {r['youtube_url']}\n"

    links_parts = []
    if resource_section:
        links_parts.append(resource_section.strip())
    if product_section:
        links_parts.append(product_section.strip())
    links_block = "\n\n".join(links_parts).strip()

    raw_text = recipe_content or ""
    summary_match = re.search(r'📋\s*Summary:\s*(.+?)(?=\n\s*(?:={3,}|[🎓🛍️A-Z#])|\Z)', raw_text, re.DOTALL | re.IGNORECASE)
    if summary_match:
        summary_text = summary_match.group(1).strip()
    else:
        clean_first_para = re.sub(r'={3,}.*?={3,}', '', raw_text, flags=re.DOTALL).strip()
        summary_text = clean_first_para[:450].strip()

    summary_text = re.sub(r'\[(?:RESOURCES(?:\s*&\s*TUTORIALS)?|PRODUCTS)\]:.*', '', summary_text, flags=re.DOTALL | re.IGNORECASE).strip()

    msg_parts = [top_header]
    if summary_text:
        msg_parts.append(f"📋 *Summary:*\n{summary_text}")
    if links_block:
        msg_parts.append(links_block)
    msg_parts.append("💡 _Full detailed notes available in the downloaded .txt file!_")
    full_message = "\n\n".join(msg_parts).strip()
    
    encoded_text = urllib.parse.quote(full_message)
    url = f"https://api.callmebot.com/whatsapp.php?phone={clean_phone}&text={encoded_text}&apikey={api_key}"
    
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200 and "Message queued" in resp.text or "ok" in resp.text.lower():
            return True, f"Successfully sent WhatsApp message to {phone_number} via CallMeBot API!"
        else:
            return False, f"CallMeBot API Response: {resp.text}"
    except Exception as e:
        return False, f"CallMeBot API Request Error: {str(e)}"

def dispatch_whatsapp(phone_number: str, recipe_txt_path: str, recipe_content: str, category: str = "RECIPE", products: list = None, resources: list = None, callmebot_api_key: str = None) -> Tuple[bool, str]:
    """
    Unified WhatsApp dispatcher for CLI and automated workflows.
    If callmebot_api_key is provided, attempts direct API message.
    Otherwise, generates and returns the pre-filled WhatsApp deep link.
    """
    if callmebot_api_key:
        return send_via_callmebot_api(phone_number, recipe_txt_path, recipe_content, callmebot_api_key, category=category, products=products, resources=resources)
    
    deep_link = generate_whatsapp_deep_link(phone_number, recipe_txt_path, recipe_content, category=category, products=products, resources=resources)
    return True, f"WhatsApp link generated: {deep_link}"


