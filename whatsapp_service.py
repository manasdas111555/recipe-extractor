import urllib.parse
import requests
from pathlib import Path
from typing import Tuple

def format_phone_number(phone: str) -> str:
    """Clean phone number and format with country code."""
    phone = phone.strip().replace(" ", "").replace("-", "").replace("+", "")
    return phone

def get_recipe_display_name(txt_file_path: str) -> str:
    """Extract readable recipe title from filename."""
    stem = Path(txt_file_path).stem
    return stem.replace("_", " ").strip()

def generate_whatsapp_deep_link(phone_number: str, recipe_txt_path: str, recipe_content: str) -> str:
    """
    Generates a WhatsApp Deep Link (wa.me / api.whatsapp.com).
    When opened on mobile or web, it opens WhatsApp with the caption & recipe pre-filled!
    """
    clean_phone = format_phone_number(phone_number)
    recipe_name = get_recipe_display_name(recipe_txt_path)
    
    # Message format
    header = f"Here is recipe file for - {recipe_name} !"
    full_message = f"🍳 *{header}*\n\n{recipe_content}"
    
    # Truncate if exceptionally long for URL safety
    if len(full_message) > 3000:
        full_message = full_message[:2950] + "\n\n...(Full recipe available in downloadable .txt file)"
        
    encoded_text = urllib.parse.quote(full_message)
    return f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_text}"

def send_via_callmebot_api(phone_number: str, recipe_txt_path: str, recipe_content: str, api_key: str) -> Tuple[bool, str]:
    """
    Sends WhatsApp message directly via free CallMeBot API.
    Get free API key by sending 'I allow callmebot to send me messages' to +34 644 44 20 70 on WhatsApp.
    """
    if not api_key:
        return False, "CallMeBot API key not provided."
        
    clean_phone = format_phone_number(phone_number)
    recipe_name = get_recipe_display_name(recipe_txt_path)
    header = f"Here is recipe file for - {recipe_name} !"
    full_message = f"🍳 *{header}*\n\n{recipe_content[:1500]}"
    
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
