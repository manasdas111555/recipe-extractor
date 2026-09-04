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


def get_recipe_display_name(txt_file_path: str) -> str:
    """Extract readable recipe title from filename."""
    stem = Path(txt_file_path).stem
    return stem.replace("_", " ").strip()

def get_category_header(recipe_name: str, category: str = "RECIPE") -> Tuple[str, str]:
    """Returns (header_caption, emoji_icon) based on category."""
    cat = (category or "RECIPE").upper()
    if "WORKOUT" in cat or "FITNESS" in cat:
        return f"Here is workout routine for - {recipe_name} !", "🏋️"
    elif "TECH" in cat or "TUTORIAL" in cat or "CODE" in cat:
        return f"Here is tutorial notes for - {recipe_name} !", "💻"
    elif "TRAVEL" in cat or "PLACE" in cat:
        return f"Here is travel guide for - {recipe_name} !", "✈️"
    elif "KNOWLEDGE" in cat or "SUMMARY" in cat:
        return f"Here is summary notes for - {recipe_name} !", "💡"
    elif "GENERAL" in cat:
        return f"Here is key takeaways for - {recipe_name} !", "📝"
    else:
        return f"Here is recipe file for - {recipe_name} !", "🍳"

def generate_whatsapp_deep_link(phone_number: str, recipe_txt_path: str, recipe_content: str, category: str = "RECIPE", products: list = None) -> str:
    """
    Generates a WhatsApp Deep Link (wa.me / api.whatsapp.com).
    When opened on mobile or web, it opens WhatsApp with caption, content & purchase links pre-filled!
    """
    clean_phone = format_phone_number(phone_number)
    recipe_name = get_recipe_display_name(recipe_txt_path)
    header, icon = get_category_header(recipe_name, category)
    
    product_section = ""
    if products and len(products) > 0:
        product_section = "\n\n🛍️ *Featured Products & 1-Click Buy Links:*\n"
        for p in products[:5]:
            price_tag = f" ({p['price']})" if p.get("price") else ""
            product_section += f"• *{p['name']}*{price_tag}\n  🛒 Amazon: {p['amazon_url']}\n"
    
    full_message = f"{icon} *{header}*\n\n{recipe_content}{product_section}"
    
    # Truncate if exceptionally long for URL safety
    if len(full_message) > 3000:
        full_message = full_message[:2950] + "\n\n...(Full text available in downloadable .txt file)"
        
    encoded_text = urllib.parse.quote(full_message)
    return f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_text}"

def send_via_callmebot_api(phone_number: str, recipe_txt_path: str, recipe_content: str, api_key: str, category: str = "RECIPE", products: list = None) -> Tuple[bool, str]:
    """
    Sends WhatsApp message directly via free CallMeBot API with product buy links.
    """
    if not api_key:
        return False, "CallMeBot API key not provided."
        
    clean_phone = format_phone_number(phone_number)
    recipe_name = get_recipe_display_name(recipe_txt_path)
    header, icon = get_category_header(recipe_name, category)
    
    product_section = ""
    if products and len(products) > 0:
        product_section = "\n\n🛍️ *Products:*\n"
        for p in products[:3]:
            product_section += f"• {p['name']}: {p['amazon_url']}\n"

    full_message = f"{icon} *{header}*\n\n{recipe_content[:1200]}{product_section}"
    
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

def dispatch_whatsapp(phone_number: str, recipe_txt_path: str, recipe_content: str, category: str = "RECIPE", products: list = None, callmebot_api_key: str = None) -> Tuple[bool, str]:
    """
    Unified WhatsApp dispatcher for CLI and automated workflows.
    If callmebot_api_key is provided, attempts direct API message.
    Otherwise, generates and returns the pre-filled WhatsApp deep link.
    """
    if callmebot_api_key:
        return send_via_callmebot_api(phone_number, recipe_txt_path, recipe_content, callmebot_api_key, category=category, products=products)
    
    deep_link = generate_whatsapp_deep_link(phone_number, recipe_txt_path, recipe_content, category=category, products=products)
    return True, f"WhatsApp link generated: {deep_link}"


