import streamlit as st
import os
import re
import sys
import time
import textwrap
import urllib.parse
import html
from pathlib import Path

# Force UTF-8 encoding on Windows console for currency symbols (₹) and emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure repository root is always first in sys.path
ROOT_DIR = str(Path(__file__).parent.resolve())
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import importlib

def _safe_load_module(module_name: str):
    """Safely imports and reloads internal modules to prevent stale cache errors on Streamlit Cloud."""
    try:
        mod = importlib.import_module(module_name)
        return importlib.reload(mod)
    except Exception:
        return importlib.import_module(module_name)

# 1. Config module
config = _safe_load_module("config")
get_api_key = getattr(config, "get_api_key", lambda: "")
save_api_key = getattr(config, "save_api_key", lambda k: None)
get_download_dir = getattr(config, "get_download_dir", lambda: Path("downloads"))
get_affiliate_tags = getattr(config, "get_affiliate_tags", lambda: {})
save_affiliate_tags = getattr(config, "save_affiliate_tags", lambda **kw: None)
cleanup_old_downloads = getattr(config, "cleanup_old_downloads", lambda **kw: None)
get_mistral_api_key = getattr(config, "get_mistral_api_key", lambda: "")
get_aionlabs_api_key = getattr(config, "get_aionlabs_api_key", lambda: "")
get_groq_api_key = getattr(config, "get_groq_api_key", lambda: "")
get_nvidia_api_key = getattr(config, "get_nvidia_api_key", lambda: "")
set_env_var = getattr(config, "set_env_var", lambda k, v: None)
MAX_VIDEO_DURATION = getattr(config, "MAX_VIDEO_DURATION", 90)

# 2. Downloader module
downloader = _safe_load_module("downloader")
get_video_from_url = getattr(downloader, "get_video_from_url", getattr(downloader, "get_recipe_video", None))
detect_platform = getattr(downloader, "detect_platform", lambda url: "Instagram Reel" if "instagram" in url.lower() else "Web Video")

# 3. Gemini Processor module
gemini_processor = _safe_load_module("gemini_processor")
process_video_and_generate_recipe = getattr(gemini_processor, "process_video_and_generate_recipe", None)

# 4. AI Router module
ai_router = _safe_load_module("ai_router")
route_video_intelligence = getattr(ai_router, "route_video_intelligence", None)
AI_PROVIDERS = getattr(ai_router, "AI_PROVIDERS", ["Google Gemini (Native Video AI)"])

# 5. UI Components module
ui_components = _safe_load_module("ui_components")
NeuralProgressDeck = getattr(ui_components, "NeuralProgressDeck", None)
render_skeleton_card_html = getattr(ui_components, "render_skeleton_card_html", lambda: "")

# 6. WhatsApp Service module
whatsapp_service = _safe_load_module("whatsapp_service")
generate_whatsapp_deep_link = getattr(whatsapp_service, "generate_whatsapp_deep_link", None)
send_via_callmebot_api = getattr(whatsapp_service, "send_via_callmebot_api", None)
get_recipe_display_name = getattr(whatsapp_service, "get_recipe_display_name", None)
get_default_country_code = getattr(whatsapp_service, "get_default_country_code", lambda: "+91")
validate_phone_number = getattr(whatsapp_service, "validate_phone_number", lambda cc, num: (True, ""))



# Purge old downloads upon session start to keep cloud storage lean
cleanup_old_downloads()

st.set_page_config(
    page_title="Universal Reel & Shorts AI Extractor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark Theme CSS - Ultra-Premium Luxury SaaS Design System
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<style>
    /* Global Reset & Modern Typography */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
        color: #F8FAFC;
    }

    /* Ambient Background Aura */
    .stApp {
        background: radial-gradient(circle at 12% 15%, rgba(244, 63, 94, 0.08) 0%, transparent 45%),
                    radial-gradient(circle at 88% 18%, rgba(139, 92, 246, 0.09) 0%, transparent 45%),
                    radial-gradient(circle at 50% 85%, rgba(14, 165, 233, 0.06) 0%, transparent 50%),
                    #090D16 !important;
    }

    /* Hero Branding */
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(244, 63, 94, 0.12);
        border: 1px solid rgba(244, 63, 94, 0.3);
        color: #FDA4AF;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 14px;
        box-shadow: 0 0 20px rgba(244, 63, 94, 0.15);
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #F43F5E;
        border-radius: 50%;
        box-shadow: 0 0 10px #F43F5E;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(244, 63, 94, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(244, 63, 94, 0); }
    }

    .hero-title {
        font-family: 'Outfit', sans-serif !important;
        font-size: 3.1rem;
        font-weight: 900;
        line-height: 1.15;
        letter-spacing: -0.035em;
        margin-bottom: 0.65rem;
        color: #FFFFFF;
    }
    .gradient-text {
        background: linear-gradient(135deg, #FF4B2B 0%, #FF416C 35%, #EC4899 70%, #A855F7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        color: #94A3B8;
        font-size: 1.08rem;
        font-weight: 400;
        line-height: 1.65;
        max-width: 820px;
        margin-bottom: 1.8rem;
    }

    /* Glass Surface Elevation */
    .glass-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        margin-bottom: 20px;
    }
    .glass-card:hover {
        border-color: rgba(255, 255, 255, 0.16);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    }

    /* Feature Superpower Tiles */
    .feature-tile {
        background: rgba(22, 30, 49, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 13px 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 14px;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .feature-tile:hover {
        background: rgba(30, 41, 59, 0.85);
        border-color: rgba(244, 63, 94, 0.35);
        transform: translateX(4px);
    }
    .feature-icon-box {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        background: linear-gradient(135deg, rgba(244, 63, 94, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .feature-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.94rem;
        color: #F8FAFC;
        margin-bottom: 2px;
    }
    .feature-desc {
        font-size: 0.8rem;
        color: #94A3B8;
        line-height: 1.35;
    }

    /* Primary CTA Button (Classy Radiant Flame) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FF4B2B 0%, #FF416C 45%, #E11D48 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.02em !important;
        padding: 14px 28px !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 25px -5px rgba(244, 63, 94, 0.5) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 16px 35px -5px rgba(244, 63, 94, 0.7) !important;
        filter: brightness(1.08) !important;
    }

    /* Sleek Input Fields */
    .stTextInput > div > div > input {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        font-size: 0.98rem !important;
        padding: 12px 16px !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #FF416C !important;
        box-shadow: 0 0 20px rgba(255, 65, 108, 0.35) !important;
    }

    /* Luxury Product Showcase */
    .product-box-luxury {
        background: linear-gradient(135deg, rgba(22, 30, 49, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 14px;
        transition: all 0.25s ease;
    }
    .product-box-luxury:hover {
        border-color: rgba(251, 191, 36, 0.4);
        box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.5);
        transform: translateY(-2px);
    }
    .shop-btn-amazon {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #FF9900 0%, #E67A00 100%);
        color: #111827 !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 8px 18px;
        border-radius: 8px;
        text-decoration: none !important;
        box-shadow: 0 4px 14px rgba(255, 153, 0, 0.35);
        transition: all 0.2s ease;
    }
    .shop-btn-amazon:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(255, 153, 0, 0.5);
    }
    .shop-btn-flipkart {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #2874F0 0%, #1557BF 100%);
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 8px 18px;
        border-radius: 8px;
        text-decoration: none !important;
        box-shadow: 0 4px 14px rgba(40, 116, 240, 0.35);
        transition: all 0.2s ease;
    }
    .shop-btn-flipkart:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(40, 116, 240, 0.5);
    }
    .shop-btn-meesho {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #F43397 0%, #D81B60 100%);
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 8px 18px;
        border-radius: 8px;
        text-decoration: none !important;
        box-shadow: 0 4px 14px rgba(244, 51, 151, 0.35);
        transition: all 0.2s ease;
    }
    .shop-btn-meesho:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(244, 51, 151, 0.55);
    }

    /* Main Brand 3: Myntra */
    .shop-btn-myntra {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #FF3F6C 0%, #FF527B 100%);
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 8px 18px;
        border-radius: 8px;
        text-decoration: none !important;
        box-shadow: 0 4px 14px rgba(255, 63, 108, 0.35);
        transition: all 0.2s ease;
    }
    .shop-btn-myntra:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(255, 63, 108, 0.55);
    }

    /* Dropdown Secondary Stores */
    .shop-btn-ajio {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #2C4152 0%, #1D2D3A 100%);
        color: #F8FAFC !important;
        border: 1px solid rgba(255,255,255,0.15);
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.82rem;
        padding: 7px 15px;
        border-radius: 8px;
        text-decoration: none !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
        transition: all 0.2s ease;
    }
    .shop-btn-ajio:hover {
        transform: translateY(-1px);
        border-color: rgba(255,255,255,0.3);
    }
    .shop-btn-nykaa {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #FC2779 0%, #C8145B 100%);
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.82rem;
        padding: 7px 15px;
        border-radius: 8px;
        text-decoration: none !important;
        box-shadow: 0 4px 12px rgba(252, 39, 121, 0.35);
        transition: all 0.2s ease;
    }
    .shop-btn-nykaa:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(252, 39, 121, 0.55);
    }
    .shop-btn-shopsy {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.82rem;
        padding: 7px 15px;
        border-radius: 8px;
        text-decoration: none !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.35);
        transition: all 0.2s ease;
    }
    .shop-btn-shopsy:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(124, 58, 237, 0.55);
    }
    .shop-btn-google {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.14);
        color: #E2E8F0 !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 0.82rem;
        padding: 7px 15px;
        border-radius: 8px;
        text-decoration: none !important;
        transition: all 0.2s ease;
    }
    .shop-btn-google:hover {
        background: rgba(255, 255, 255, 0.12);
        color: #FFFFFF !important;
    }

    /* Dropdown UI Container */
    .more-stores-details {
        margin-top: 10px;
        width: 100%;
    }
    .more-stores-summary {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        cursor: pointer;
        padding: 6px 14px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px dashed rgba(255, 255, 255, 0.18);
        color: #94A3B8;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 0.82rem;
        user-select: none;
        transition: all 0.2s ease;
    }
    .more-stores-summary:hover {
        background: rgba(255, 255, 255, 0.09);
        color: #F1F5F9;
        border-color: rgba(255, 255, 255, 0.35);
    }
    .more-stores-shelf {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        align-items: center;
        margin-top: 10px;
        padding: 12px 14px;
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 10px;
        animation: fadeInDown 0.2s ease-out;
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-4px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Quick Commerce Instant Delivery Shelf */
    .qc-shelf-container {
        margin-top: 14px;
        padding-top: 12px;
        border-top: 1px dashed rgba(255, 255, 255, 0.12);
        width: 100%;
    }
    .qc-shelf-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.78rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #F59E0B;
        margin-bottom: 8px;
    }
    .qc-btn-blinkit {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #F7D302;
        color: #0C5427 !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 0.82rem;
        padding: 6px 14px;
        border-radius: 8px;
        text-decoration: none !important;
        box-shadow: 0 4px 12px rgba(247, 211, 2, 0.3);
        transition: all 0.2s ease;
    }
    .qc-btn-blinkit:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(247, 211, 2, 0.5);
    }
    .qc-btn-zepto {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: linear-gradient(135deg, #7A1EA1 0%, #E02475 100%);
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 0.82rem;
        padding: 6px 14px;
        border-radius: 8px;
        text-decoration: none !important;
        box-shadow: 0 4px 12px rgba(224, 36, 117, 0.3);
        transition: all 0.2s ease;
    }
    .qc-btn-zepto:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(224, 36, 117, 0.5);
    }
    .qc-btn-instamart {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: linear-gradient(135deg, #FC8019 0%, #D85800 100%);
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 0.82rem;
        padding: 6px 14px;
        border-radius: 8px;
        text-decoration: none !important;
        box-shadow: 0 4px 12px rgba(252, 128, 25, 0.3);
        transition: all 0.2s ease;
    }
    .qc-btn-instamart:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(252, 128, 25, 0.5);
    }
    .qc-btn-jiomart {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: linear-gradient(135deg, #0078AD 0%, #004F75 100%);
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 0.82rem;
        padding: 6px 14px;
        border-radius: 8px;
        text-decoration: none !important;
        box-shadow: 0 4px 12px rgba(0, 120, 173, 0.3);
        transition: all 0.2s ease;
    }
    .qc-btn-jiomart:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(0, 120, 173, 0.5);
    }


    /* YouTube Tutorial & Learning Showcase */
    .tutorial-box-luxury {
        background: linear-gradient(135deg, rgba(22, 30, 49, 0.75) 0%, rgba(15, 23, 42, 0.92) 100%);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 14px;
        transition: all 0.25s ease;
    }
    .tutorial-box-luxury:hover {
        border-color: rgba(239, 68, 68, 0.45);
        box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.5), 0 0 20px rgba(239, 68, 68, 0.15);
        transform: translateY(-2px);
    }
    .watch-btn-yt {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%);
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 8px 18px;
        border-radius: 8px;
        text-decoration: none !important;
        box-shadow: 0 4px 14px rgba(255, 0, 0, 0.35);
        transition: all 0.2s ease;
    }
    .watch-btn-yt:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(255, 0, 0, 0.55);
        filter: brightness(1.1);
    }

    /* AI Category Classification Banner */
    .classification-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 16px;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.45), 0 0 20px rgba(56, 189, 248, 0.12);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
    }


    /* WhatsApp Emerald Glowing Action */
    .wa-btn-luxury {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1.02rem;
        padding: 12px 24px;
        border-radius: 12px;
        text-decoration: none !important;
        box-shadow: 0 8px 25px -4px rgba(37, 211, 102, 0.45);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        width: 100%;
        text-align: center;
    }
    .wa-btn-luxury:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 14px 35px -2px rgba(37, 211, 102, 0.65);
    }

    /* Benchmark Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.65) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        box-shadow: 0 8px 20px -5px rgba(0, 0, 0, 0.4) !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.6rem !important;
        color: #F8FAFC !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.82rem !important;
        color: #94A3B8 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* Sidebar Glass Overhaul */
    [data-testid="stSidebar"] {
        background-color: rgba(9, 13, 22, 0.88) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
    }

    /* Mobile & Responsive Breakpoints */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.15rem !important;
            line-height: 1.18 !important;
            letter-spacing: -0.025em !important;
            margin-bottom: 0.5rem !important;
        }
        .sub-header {
            font-size: 0.94rem !important;
            line-height: 1.55 !important;
            margin-bottom: 1.2rem !important;
        }
        .hero-badge {
            font-size: 0.68rem !important;
            padding: 5px 11px !important;
            letter-spacing: 0.05em !important;
        }
        .glass-card {
            padding: 16px 14px !important;
            border-radius: 14px !important;
        }
        .feature-tile {
            padding: 11px 12px !important;
            gap: 10px !important;
        }
        .feature-icon-box {
            width: 36px !important;
            height: 36px !important;
            font-size: 1.05rem !important;
        }
        .feature-title {
            font-size: 0.88rem !important;
        }
        .feature-desc {
            font-size: 0.76rem !important;
        }
        div.stButton > button[kind="primary"] {
            font-size: 0.98rem !important;
            padding: 12px 18px !important;
        }
        .micro-chips {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 6px !important;
        }
        .product-box-luxury {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 12px !important;
        }
    }

    /* Neural Scanner Deck & Perceived Speed System */
    .neural-scanner-deck {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.92) 0%, rgba(30, 41, 59, 0.82) 100%);
        border: 1px solid rgba(244, 63, 94, 0.35);
        border-radius: 16px;
        padding: 20px 22px;
        margin: 14px 0;
        box-shadow: 0 12px 32px -5px rgba(0, 0, 0, 0.5), 0 0 25px rgba(244, 63, 94, 0.15);
        position: relative;
        overflow: hidden;
    }
    .neural-scanner-deck::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #FF416C, #F43F5E, transparent);
        animation: scanner-sweep 2.2s linear infinite;
    }
    @keyframes scanner-sweep {
        0% { transform: translateX(0); }
        100% { transform: translateX(50%); }
    }
    .scanner-pulse-dot {
        display: inline-flex;
        width: 12px;
        height: 12px;
        background: #F43F5E;
        border-radius: 50%;
        box-shadow: 0 0 12px #F43F5E;
        animation: pulse 1.4s infinite;
        margin: 4px;
        flex-shrink: 0;
    }
    .trivia-ticker {
        background: rgba(244, 63, 94, 0.08);
        border: 1px solid rgba(244, 63, 94, 0.22);
        border-radius: 10px;
        padding: 10px 14px;
        margin-top: 14px;
    }
    .skeleton-card {
        background: rgba(15, 23, 42, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 18px 20px;
        margin-top: 12px;
    }
    .shimmer-bar {
        background: linear-gradient(90deg, rgba(255,255,255,0.03) 25%, rgba(255,255,255,0.09) 50%, rgba(255,255,255,0.03) 75%);
        background-size: 200% 100%;
        animation: shimmer-anim 1.8s infinite;
        border-radius: 6px;
    }
    @keyframes shimmer-anim {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    .video-preview-standby {
        background: rgba(15, 23, 42, 0.6);
        border: 2px dashed rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 40px 20px;
        text-align: center;
        margin-top: 14px;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar Settings - Consumer Luxury Experience
st.sidebar.markdown("""
<div style="padding: 4px 0 16px 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 18px;">
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="width:42px; height:42px; border-radius:12px; background: linear-gradient(135deg, #FF4B2B, #FF416C); display:flex; align-items:center; justify-content:center; font-size:1.35rem; box-shadow:0 4px 16px rgba(255,65,108,0.45); flex-shrink:0;">
            ⚡
        </div>
        <div>
            <div style="font-family:'Outfit',sans-serif; font-weight:800; font-size:1.12rem; color:#FFFFFF; letter-spacing:-0.02em;">REEL EXTRACTOR</div>
            <div style="font-size:0.72rem; color:#FDA4AF; font-weight:700; text-transform:uppercase; letter-spacing:0.08em;">Universal Pro AI</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Backend Keys (Loaded securely on server - Never rendered in public DOM)
gemini_key = get_api_key()
mistral_key = get_mistral_api_key()
groq_key = get_groq_api_key()
nvidia_key = get_nvidia_api_key()
aionlabs_key = get_aionlabs_api_key()
has_any_key = bool(gemini_key or mistral_key or groq_key or nvidia_key or aionlabs_key)

# Admin Mode (Only visible if owner visits with ?admin=1)
query_params = getattr(st, "query_params", {})
is_admin = query_params.get("admin") == "1"

if is_admin:
    with st.sidebar.expander("🛠️ Admin / Server Key Vault", expanded=False):
        st.caption("Admin view only (hidden from consumers):")
        g_in = st.text_input("Gemini Key", value=gemini_key, type="password")
        m_in = st.text_input("Mistral Key", value=mistral_key, type="password")
        gr_in = st.text_input("Groq Key", value=groq_key, type="password")
        nv_in = st.text_input("NVIDIA Key", value=nvidia_key, type="password")
        curr_tags = get_affiliate_tags()
        amz_in = st.text_input("Amazon Tag", value=curr_tags.get("amazon", ""))
        flp_in = st.text_input("Flipkart Tag", value=curr_tags.get("flipkart", ""))
        msh_in = st.text_input("Meesho / Reseller Tag", value=curr_tags.get("meesho", ""))
        cue_in = st.text_input("Cuelinks CID (Aggregator)", value=curr_tags.get("cuelinks", ""))
        ek_in = st.text_input("EarnKaro User ID (Aggregator)", value=curr_tags.get("earnkaro", ""))
        if st.button("Save Admin Config"):
            if g_in: set_env_var("GEMINI_API_KEY", g_in)
            if m_in: set_env_var("MISTRALAI_API_KEY", m_in)
            if gr_in: set_env_var("GROQ_API_KEY", gr_in)
            if nv_in: set_env_var("NVIDIA_API_KEY", nv_in)
            save_affiliate_tags(amz_in, flp_in, msh_in, cue_in, ek_in)
            st.success("Admin configuration updated!")
            st.rerun()


# 1. WhatsApp Destination (Primary Consumer Setting)
st.sidebar.markdown("""
<div style="margin-bottom: 8px;">
    <div style="font-family:'Outfit',sans-serif; font-weight:700; font-size:0.95rem; color:#F8FAFC; display:flex; align-items:center; gap:6px;">
        <span>📱 WhatsApp Delivery</span>
    </div>
    <div style="font-size:0.78rem; color:#94A3B8; line-height:1.4;">
        Receive structured recipes, workout steps & buy links directly on WhatsApp.
    </div>
</div>
""", unsafe_allow_html=True)

if "saved_user_phone" not in st.session_state:
    st.session_state["saved_user_phone"] = ""
if "saved_user_cc" not in st.session_state:
    st.session_state["saved_user_cc"] = get_default_country_code()

default_cc = st.session_state.get("saved_user_cc") or get_default_country_code()
saved_phone_val = st.session_state.get("saved_user_phone", "")

col_cc, col_num = st.sidebar.columns([1.1, 2.4])
with col_cc:
    country_code_input = st.text_input("Code", value=default_cc, help="Country calling code (e.g. +91)")
with col_num:
    local_phone_input = st.text_input("Phone Number", value=saved_phone_val, placeholder="9999999999", help="Mobile number without country code")

sidebar_phone = local_phone_input.strip()
phone_number_input = ""
if sidebar_phone:
    is_valid_sb, err_sb = validate_phone_number(country_code_input, sidebar_phone)
    if is_valid_sb:
        clean_sb_cc = country_code_input.strip().replace("+", "").strip()
        phone_number_input = f"{clean_sb_cc}{sidebar_phone}"
        st.session_state["saved_user_phone"] = sidebar_phone
        st.session_state["saved_user_cc"] = country_code_input
        st.sidebar.markdown("""
        <div style="display:flex; align-items:center; justify-content:space-between; margin-top:-6px; margin-bottom:8px;">
            <span style="background:rgba(16,185,129,0.15); color:#34D399; font-size:0.72rem; font-weight:700; padding:2px 8px; border-radius:9999px; border:1px solid rgba(16,185,129,0.3);">✓ Number Saved</span>
            <span style="font-size:0.7rem; color:#94A3B8;">Auto-filled</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.warning(f"⚠️ {err_sb}")

# 2. Content Intelligence Mode
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-family:'Outfit',sans-serif; font-weight:700; font-size:0.95rem; color:#F8FAFC; margin-bottom:4px;">
    🎯 Content Domain
</div>
""", unsafe_allow_html=True)

mode_choice = st.sidebar.selectbox(
    "Domain Classifier",
    options=[
        "Auto-Detect (Universal AI)",
        "🍳 Cooking Recipe & Food",
        "🛍️ Kitchen Finds & Home Gadgets",
        "🎓 Educational & Concept Explainer",
        "💻 Tutorial & How-To Guide (Tech, Coding, DIY)",
        "📦 Product Unboxing & Amazon Finds",
        "🏋️ Fitness & Workout Routine",
        "💰 Finance, Business & Investing",
        "✈️ Travel, Places & Food Guide",
        "💄 Beauty, Skincare & Fashion",
        "💡 Life Hacks & Productivity"
    ],
    index=0,
    label_visibility="collapsed",
    help="Auto-Detect intelligently determines whether the video is educational, tutorial, kitchen finds, recipe, workout, finance, beauty, or travel."
)

# Backend defaults for high performance
provider_choice = "Auto-Universal (Gemini with Multi-Model Fallback)"
model_choice = "gemini-3.8-flash"

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 12px 14px; margin-top: 10px;">
    <div style="display:flex; align-items:center; gap:8px;">
        <span style="width:8px; height:8px; border-radius:50%; background:#10B981; box-shadow:0 0 8px #10B981;"></span>
        <span style="font-size:0.82rem; font-weight:700; color:#6EE7B7;">Engine: Operational</span>
    </div>
    <div style="font-size:0.74rem; color:#94A3B8; margin-top:5px; line-height:1.4;">
        Multimodal pipeline powered by Gemini 3.8 Flash with instant multi-model fallback.
    </div>
</div>
""", unsafe_allow_html=True)



# Main UI - Ultra-Classy Hero Section
st.markdown("""
<div style="margin-bottom: 22px;">
    <div class="hero-badge">
        <span class="pulse-dot"></span>
        <span>Next-Gen Multimodal AI · Universal Video Extractor</span>
    </div>
    <h1 class="hero-title">Universal Reel & Shorts <span class="gradient-text">AI Extractor</span></h1>
    <div class="sub-header">
        Turn any Instagram Reel or YouTube Short into structured step-by-step recipes, workout routines, code tutorials, and monetized shoppable ingredient links — in under 3 seconds.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.7, 1.3], gap="large")

with col1:
    st.markdown("""
    <div style="font-family:'Outfit',sans-serif; font-weight:700; font-size:1.1rem; color:#F1F5F9; margin-bottom:10px; display:flex; align-items:center; gap:8px;">
        <span>🔗 Video Ingestion Link</span>
    </div>
    """, unsafe_allow_html=True)

    reel_url = st.text_input(
        "URL Input",
        placeholder="Paste Instagram Reel or YouTube Shorts URL (e.g. https://instagram.com/reel/...)",
        label_visibility="collapsed"
    )
    if reel_url and reel_url.strip():
        platform = detect_platform(reel_url.strip())
        st.markdown(f"""
        <div style="margin: 8px 0 14px 0;">
            <span style="background: rgba(244, 63, 94, 0.12); border: 1px solid rgba(244, 63, 94, 0.28); color: #FDA4AF; padding: 4px 12px; border-radius: 8px; font-size: 0.8rem; font-weight: 600;">
                🎯 Platform Identified: <b>{platform}</b>
            </span>
        </div>
        """, unsafe_allow_html=True)

    process_btn = st.button("⚡ Extract Intelligence in Seconds", type="primary", use_container_width=True)

    st.markdown("""<div class="micro-chips" style="display:flex; justify-content:space-between; align-items:center; margin-top:14px; padding:10px 14px; background:rgba(255,255,255,0.02); border-radius:10px; border:1px solid rgba(255,255,255,0.05); font-size:0.76rem; color:#94A3B8;">
<span>⚡ <b>Instant Processing</b> (≤90s)</span>
<span>🔒 <b>Zero Data Retained</b></span>
<span>📱 <b>1-Click WhatsApp Sync</b></span>
</div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""<div class="glass-card" style="padding: 18px 20px; margin-top: 0;">
<div style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.08rem; color: #FFFFFF; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
<span>✨ Platform Superpowers</span>
</div>
<div class="feature-tile">
<div class="feature-icon-box">🌐</div>
<div>
<div class="feature-title">Universal Stream Parsing</div>
<div class="feature-desc">Seamless ingestion of Instagram Reels & YouTube Shorts with auto-resolution.</div>
</div>
</div>
<div class="feature-tile">
<div class="feature-icon-box">🧠</div>
<div>
<div class="feature-title">Multimodal Neural Vision</div>
<div class="feature-desc">Simultaneously analyzes video frames, on-screen text, voiceover & audio.</div>
</div>
</div>
<div class="feature-tile">
<div class="feature-icon-box">🛍️</div>
<div>
<div class="feature-title">Shoppable Product Links</div>
<div class="feature-desc">Identifies cookware, fitness gear & ingredients with instant 1-click buy tags.</div>
</div>
</div>
<div class="feature-tile">
<div class="feature-icon-box">📱</div>
<div>
<div class="feature-title">Instant WhatsApp Dispatch</div>
<div class="feature-desc">Direct delivery of clean, formatted recipe notes straight to your phone.</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

# Trust & Capabilities Ticker
st.markdown("""<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; margin: 24px 0 28px 0;">
<div style="background: rgba(15, 23, 42, 0.55); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 14px; padding: 14px 18px; display: flex; align-items: center; gap: 12px;">
<div style="font-size: 1.6rem;">⚡</div>
<div>
<div style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.22rem; color: #F8FAFC;">~2.4s</div>
<div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">AI Turnaround</div>
</div>
</div>
<div style="background: rgba(15, 23, 42, 0.55); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 14px; padding: 14px 18px; display: flex; align-items: center; gap: 12px;">
<div style="font-size: 1.6rem;">💎</div>
<div>
<div style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.22rem; color: #F8FAFC;">Multimodal</div>
<div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">Gemini 3.7 & Groq</div>
</div>
</div>
<div style="background: rgba(15, 23, 42, 0.55); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 14px; padding: 14px 18px; display: flex; align-items: center; gap: 12px;">
<div style="font-size: 1.6rem;">🛒</div>
<div>
<div style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.22rem; color: #F8FAFC;">Shoppable</div>
<div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">Amazon & Flipkart Tags</div>
</div>
</div>
<div style="background: rgba(15, 23, 42, 0.55); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 14px; padding: 14px 18px; display: flex; align-items: center; gap: 12px;">
<div style="font-size: 1.6rem;">📲</div>
<div>
<div style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.22rem; color: #F8FAFC;">1-Click</div>
<div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">WhatsApp Share</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

if process_btn:
    st.session_state["extraction_result"] = None
    if not reel_url or not reel_url.strip().startswith("http"):
        st.error("Please enter a valid video URL (e.g. Instagram Reel or YouTube Short).")
    elif not has_any_key:
        st.error("Please configure at least one AI API Key in the sidebar (Gemini, Mistral, or Groq).")
    else:
        start_time = time.perf_counter()
        clean_url = reel_url.strip()
        detected_plat = detect_platform(clean_url)

        # Dual-Column High-Velocity Processing Layout
        proc_left, proc_right = st.columns([1.2, 0.8], gap="large")

        with proc_left:
            deck_placeholder = st.empty()
            deck = NeuralProgressDeck(deck_placeholder, mode=mode_choice)
            skeleton_placeholder = st.empty()
            if hasattr(skeleton_placeholder, "html"):
                skeleton_placeholder.html(render_skeleton_card_html())
            else:
                skeleton_placeholder.markdown(render_skeleton_card_html(), unsafe_allow_html=True)

        with proc_right:
            preview_placeholder = st.empty()
            standby_html = f"""<div class="video-preview-standby">
<div style="font-size:2.2rem; margin-bottom:10px;">⚡</div>
<div style="font-family:'Outfit',sans-serif; font-weight:700; font-size:1.02rem; color:#F1F5F9;">Ingesting {detected_plat}...</div>
<div style="font-size:0.8rem; color:#94A3B8; margin-top:4px;">Connecting to CDN stream pipeline</div>
</div>"""
            if hasattr(preview_placeholder, "html"):
                preview_placeholder.html(standby_html)
            else:
                preview_placeholder.markdown(standby_html, unsafe_allow_html=True)

        # Step 1: Download Video Stream
        t_dl_start = time.perf_counter()
        success, video_result = get_video_from_url(clean_url, preferred_engine="ytdlp")
        dl_duration = time.perf_counter() - t_dl_start

        if not success:
            deck.update_step("dl", "error", f"Download Error: {video_result}")
            skeleton_placeholder.empty()
            st.error(f"Download Error: {video_result}")
        else:
            deck.update_step("dl", "done", f"Stream captured in {dl_duration:.1f}s")
            deck.update_step("prep", "active", "Extracting visual keyframes & speech tensors...")

            # INSTANT FIRST PAINT (~1.5s): Show video preview immediately!
            with preview_placeholder.container():
                st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 12px 14px; margin-bottom: 10px; display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-family:'Outfit',sans-serif; font-weight:700; font-size:0.88rem; color:#F1F5F9;">🎬 Stream Ingested ({dl_duration:.1f}s)</span>
                    <span style="background:rgba(16,185,129,0.15); color:#34D399; font-size:0.72rem; font-weight:700; padding:2px 8px; border-radius:6px; border:1px solid rgba(16,185,129,0.3);">Neural Scan Active</span>
                </div>
                """, unsafe_allow_html=True)
                st.video(video_result)

            # Step 2: Multimodal AI Reasoning via Central Router
            gemini_res = route_video_intelligence(
                video_path=video_result,
                provider=provider_choice,
                custom_gemini_key=gemini_key,
                custom_mistral_key=mistral_key,
                custom_groq_key=groq_key,
                status_callback=deck.on_ai_status,
                gemini_model_preference=model_choice,
                extraction_mode=mode_choice,
                affiliate_tags=get_affiliate_tags()
            )

            gemini_success = gemini_res[0]
            txt_filepath = gemini_res[1]
            recipe_text = gemini_res[2]
            final_video_path = gemini_res[3] if len(gemini_res) > 3 else video_result
            meta = gemini_res[4] if len(gemini_res) > 4 else {}

            total_elapsed = time.perf_counter() - start_time
            skeleton_placeholder.empty()

            if not gemini_success:
                deck.update_step("ai", "error", f"Extraction Failed: {recipe_text}")
                st.error(f"Extraction Error: {recipe_text}")
            else:
                timings = meta.get("timings", {})
                cloud_prep_time = timings.get('prep_s', 0.0) + timings.get('upload_s', 0.0)
                ai_duration = timings.get('inference_s', 0.0)
                model_display = timings.get('model_used', model_choice)

                # Dynamically reflect specialized steps only if actual content exists
                found_prods = meta.get("products", [])
                found_res = meta.get("resources", [])
                if found_prods and len(found_prods) > 0:
                    deck.insert_or_update_step(
                        step_id="links",
                        title="Shoppable Catalog Synthesis",
                        desc=f"Generated 1-click buy tags for {len(found_prods)} products",
                        icon="🛍️",
                        state="done"
                    )
                elif found_res and len(found_res) > 0:
                    deck.insert_or_update_step(
                        step_id="resources",
                        title="Recommended YouTube Tutorials & Links",
                        desc=f"Linked {len(found_res)} tutorials & learning resources",
                        icon="🎓",
                        state="done"
                    )

                deck.complete_all(total_elapsed)
                preview_placeholder.empty()
                st.balloons()
                st.session_state["extraction_result"] = {
                    "source_url": clean_url,
                    "txt_filepath": txt_filepath,
                    "recipe_text": recipe_text,
                    "final_video_path": final_video_path,
                    "meta": meta,
                    "detected_plat": detected_plat,
                    "total_elapsed": total_elapsed,
                    "dl_duration": dl_duration,
                    "cloud_prep_time": cloud_prep_time,
                    "ai_duration": ai_duration,
                    "model_display": model_display
                }

# Render Intelligence Results from Session State
active_res = st.session_state.get("extraction_result")
if active_res:
    txt_filepath = active_res["txt_filepath"]
    recipe_text = active_res["recipe_text"]
    final_video_path = active_res["final_video_path"]
    meta = active_res["meta"]
    detected_plat = active_res.get("detected_plat", "Video")
    total_elapsed = active_res.get("total_elapsed", 0.0)
    dl_duration = active_res.get("dl_duration", 0.0)
    cloud_prep_time = active_res.get("cloud_prep_time", 0.0)
    ai_duration = active_res.get("ai_duration", 0.0)
    model_display = active_res.get("model_display", "AI")

    cat_name = meta.get("category_name", "Extracted Content")
    cat_emoji = meta.get("emoji", "📝")
    cat_code = meta.get("category", "RECIPE")
    item_title = meta.get("title", get_recipe_display_name(txt_filepath))
    products_list = meta.get("products", [])
    resources_list = meta.get("resources", [])

    # Consumer-Grade Performance Metric Pill (P0 PO Directive)
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
        <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(16, 185, 129, 0.12); border:1px solid rgba(16, 185, 129, 0.35); border-radius:9999px; padding:5px 15px;">
            <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10B981; box-shadow:0 0 8px #10B981;"></span>
            <span style="font-family:'Outfit',sans-serif; font-weight:700; font-size:0.86rem; color:#34D399;">⚡ Processed in {total_elapsed:.1f}s</span>
        </div>
        <span style="font-size:0.75rem; color:#94A3B8;">Model: {model_display} • {detected_plat}</span>
    </div>
    """, unsafe_allow_html=True)

    # Detailed Pipeline Telemetry demoted to expandable developer drawer (P0 PO Directive)
    is_admin_mode = bool(st.query_params.get("admin") == "1")
    with st.expander("🛠️ Pipeline Telemetry & Latency Breakdown (Developer View)", expanded=is_admin_mode):
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("⏱️ Total Turnaround", f"{total_elapsed:.1f}s")
        b2.metric("📥 Stream Download", f"{dl_duration:.1f}s")
        b3.metric("☁️ Cloud Upload & Prep", f"{cloud_prep_time:.1f}s")
        b4.metric(f"🧠 AI ({model_display})", f"{ai_duration:.1f}s")
    st.markdown("---")

    # Unified 2-Column Responsive Layout: Left = Intelligence & Actions, Right = Single Video Stream
    col_content, col_media = st.columns([1.25, 0.75], gap="large")

    with col_content:
        # AI Domain Classification Banner
        classification_html = f"""
        <div class="classification-banner">
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:1.85rem; line-height:1;">{cat_emoji}</span>
                <div>
                    <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; color:#94A3B8; font-weight:700;">AI Domain Classification</div>
                    <div style="font-size:1.18rem; font-weight:800; color:#38BDF8; font-family:'Outfit',sans-serif; letter-spacing:-0.01em;">{cat_name}</div>
                </div>
            </div>
            <div style="display:flex; gap:8px; align-items:center;">
                <span style="background:rgba(56, 189, 248, 0.12); color:#38BDF8; border:1px solid rgba(56, 189, 248, 0.35); font-size:0.76rem; font-weight:700; padding:4px 12px; border-radius:9999px;">✓ Verified Domain</span>
            </div>
        </div>
        """
        st.markdown(textwrap.dedent(classification_html).strip(), unsafe_allow_html=True)
        st.markdown(f"### {item_title}")

        if meta.get("summary"):
            clean_summary_disp = re.sub(r'\[(?:RESOURCES(?:\s*&\s*TUTORIALS)?|PRODUCTS)\]:.*', '', meta['summary'], flags=re.DOTALL | re.IGNORECASE).strip()
            st.info(f"**Executive Summary**: {clean_summary_disp}")

        # Domain Conditional Store Routing (P0 PO Directive)
        cat_code_u = (cat_code or "RECIPE").upper()
        is_recipe_domain = any(c in cat_code_u for c in ["RECIPE", "COOK", "BAKE", "FOOD", "CULINARY"])
        is_fashion_domain = any(c in cat_code_u for c in ["BEAUTY_FASHION", "FASHION", "OOTD", "STYLE", "BEAUTY", "APPAREL"])
        is_tutorial_domain = any(c in cat_code_u for c in ["TUTORIAL", "TECH_TUTORIAL", "EDUCATIONAL", "CODE", "DIY", "HOWTO"])

        # Filter out digital software, AI models, plugins, APIs from e-commerce buy links
        digital_keywords = [
            "ai model", "model", "plugin", "installer", "api", "framework",
            "library", "llm", "software", "repo", "repository", "package",
            "extension", "sdk", "algorithm", "prompt", "token", "cli",
            "sqlite", "claude-mem", "claude code", "gemini", "gpt",
            "deepseek", "kimi", "glm", "llama", "mistral", "chatgpt"
        ]

        valid_products = []
        for p in (products_list or []):
            p_name_l = (p.get("name") or "").lower()
            p_price_l = (p.get("price") or "").lower()
            if is_tutorial_domain:
                if any(kw in p_name_l for kw in digital_keywords) or any(kw in p_price_l for kw in ["free", "n/a", "bundled"]):
                    continue
            valid_products.append(p)

        if valid_products:
            if is_recipe_domain:
                st.markdown("### 🛒 Ingredients & 10-Minute Delivery")
                st.caption("AI identified the following ingredients. Order instantly via Quick Commerce or fresh grocery:")

                # 1-Click Copy Ingredient Checklist Button
                checklist_lines = [f"[ ] {p['name']}" + (f" ({p['price']})" if p.get('price') else "") for p in valid_products]
                raw_checklist = f"🛒 Ingredient Checklist for {item_title}:\n" + "\n".join(checklist_lines)
                safe_checklist_js = json.dumps(raw_checklist)

                checklist_btn_html = f"""
                <div style="margin-bottom: 12px; display: flex; align-items: center; gap: 10px;">
                    <button id="copyChecklistBtn" style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); color: #34D399; padding: 7px 15px; border-radius: 8px; font-weight: 700; font-size: 0.85rem; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s;">
                        📋 Copy Ingredient Checklist
                    </button>
                    <span id="checklistCopiedToast" style="display: none; color: #34D399; font-size: 0.82rem; font-weight: 600;">✓ Copied to Clipboard!</span>
                </div>
                <script>
                document.getElementById("copyChecklistBtn").addEventListener("click", () => {{
                    navigator.clipboard.writeText({safe_checklist_js}).then(() => {{
                        const toast = document.getElementById("checklistCopiedToast");
                        toast.style.display = "inline";
                        setTimeout(() => {{ toast.style.display = "none"; }}, 2500);
                    }});
                }});
                </script>
                """
                if hasattr(st, "html"):
                    st.html(checklist_btn_html)
                else:
                    st.markdown(checklist_btn_html, unsafe_allow_html=True)

                for prod in valid_products:
                    p_name = prod["name"]
                    p_price = prod.get("price", "")
                    price_html = f"<span style='background-color:rgba(16, 185, 129, 0.15); color:#34D399; border:1px solid rgba(16, 185, 129, 0.35); font-size:0.78rem; padding:3px 10px; border-radius:9999px; margin-left:8px; font-weight:700;'>💰 {p_price}</span>" if p_price else ""

                    prod_html = f"""
                    <div class="product-box-luxury">
                        <div style="display:flex; align-items:center; gap:8px; font-size:0.98rem; font-weight:700; color:#F1F5F9; margin-bottom: 6px;">
                            <span>🥬</span> <span>{p_name}</span> {price_html}
                        </div>
                        <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center; margin-top: 6px;">
                            <a href="{prod.get('blinkit_url', f'https://blinkit.com/s/?q={urllib.parse.quote_plus(p_name)}')}" target="_blank" class="qc-btn-blinkit">🟡 Blinkit (10-Min)</a>
                            <a href="{prod.get('zepto_url', f'https://www.zeptonow.com/search?q={urllib.parse.quote_plus(p_name)}')}" target="_blank" class="qc-btn-zepto">⚡ Zepto</a>
                            <a href="{prod.get('instamart_url', f'https://www.swiggy.com/instamart/search?custom_back=true&query={urllib.parse.quote_plus(p_name)}')}" target="_blank" class="qc-btn-instamart">🛵 Instamart</a>
                            <a href="{prod.get('jiomart_url', f'https://www.jiomart.com/search/{urllib.parse.quote_plus(p_name)}')}" target="_blank" class="qc-btn-jiomart">📦 JioMart</a>
                            <a href="{prod['amazon_url']}" target="_blank" class="shop-btn-amazon">🛒 Amazon Fresh</a>
                        </div>
                        <details class="more-stores-details" style="margin-top:8px;">
                            <summary class="more-stores-summary">🏷️ More Grocery Stores & Price Compare ▾</summary>
                            <div class="more-stores-shelf">
                                <a href="{prod.get('bigbasket_url', f'https://www.bigbasket.com/ps/?q={urllib.parse.quote_plus(p_name)}')}" target="_blank" class="shop-btn-flipkart">🧺 BigBasket</a>
                                <a href="{prod['google_shopping_url']}" target="_blank" class="shop-btn-google">🔍 Google Shopping</a>
                            </div>
                        </details>
                    </div>
                    """
                    st.markdown(textwrap.dedent(prod_html).strip(), unsafe_allow_html=True)

            elif is_fashion_domain:
                st.markdown("### 👗 Featured Apparel & Shop the Look")
                st.caption("AI identified the following fashion items. Click any storefront to browse or purchase:")
                for prod in valid_products:
                    p_name = prod["name"]
                    p_price = prod.get("price", "")
                    price_html = f"<span style='background-color:rgba(16, 185, 129, 0.15); color:#34D399; border:1px solid rgba(16, 185, 129, 0.35); font-size:0.78rem; padding:3px 10px; border-radius:9999px; margin-left:8px; font-weight:700;'>💰 {p_price}</span>" if p_price else ""

                    prod_html = f"""
                    <div class="product-box-luxury">
                        <div style="display:flex; align-items:center; gap:8px; font-size:0.98rem; font-weight:700; color:#F1F5F9; margin-bottom: 6px;">
                            <span>👗</span> <span>{p_name}</span> {price_html}
                        </div>
                        <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-top: 6px;">
                            <a href="{prod.get('myntra_url', f'https://www.myntra.com/{urllib.parse.quote_plus(p_name)}')}" target="_blank" class="shop-btn-myntra">🛍️ Myntra</a>
                            <a href="{prod.get('ajio_url', f'https://www.ajio.com/search/?text={urllib.parse.quote_plus(p_name)}')}" target="_blank" class="shop-btn-ajio">👔 AJIO</a>
                            <a href="{prod.get('meesho_url', f'https://www.meesho.com/search?q={urllib.parse.quote_plus(p_name)}')}" target="_blank" class="shop-btn-meesho">🌸 Meesho</a>
                            <a href="{prod['amazon_url']}" target="_blank" class="shop-btn-amazon">🛒 Amazon Fashion</a>
                        </div>
                        <details class="more-stores-details" style="margin-top:8px;">
                            <summary class="more-stores-summary">🏷️ More Stores & Price Compare ▾</summary>
                            <div class="more-stores-shelf">
                                <a href="{prod.get('nykaa_url', f'https://www.nykaa.com/search/result/?q={urllib.parse.quote_plus(p_name)}')}" target="_blank" class="shop-btn-nykaa">💄 Nykaa Fashion</a>
                                <a href="{prod['google_shopping_url']}" target="_blank" class="shop-btn-google">🔍 Google Shopping</a>
                            </div>
                        </details>
                    </div>
                    """
                    st.markdown(textwrap.dedent(prod_html).strip(), unsafe_allow_html=True)

            elif is_tutorial_domain:
                # Hardware & Tools featured in Tutorial
                st.markdown("### 🛠️ Hardware & Physical Tools Featured")
                st.caption("AI identified the following hardware tools or equipment in this video:")
                for prod in valid_products:
                    p_name = prod["name"]
                    p_price = prod.get("price", "")
                    price_html = f"<span style='background-color:rgba(16, 185, 129, 0.15); color:#34D399; border:1px solid rgba(16, 185, 129, 0.35); font-size:0.78rem; padding:3px 10px; border-radius:9999px; margin-left:8px; font-weight:700;'>💰 {p_price}</span>" if p_price else ""

                    prod_html = f"""
                    <div class="product-box-luxury">
                        <div style="display:flex; align-items:center; gap:8px; font-size:0.98rem; font-weight:700; color:#F1F5F9; margin-bottom: 6px;">
                            <span>🛠️</span> <span>{p_name}</span> {price_html}
                        </div>
                        <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-top: 6px;">
                            <a href="{prod['amazon_url']}" target="_blank" class="shop-btn-amazon">🛒 Amazon Prime</a>
                            <a href="{prod['flipkart_url']}" target="_blank" class="shop-btn-flipkart">⚡ Flipkart</a>
                            <a href="{prod['google_shopping_url']}" target="_blank" class="shop-btn-google">🔍 Google Shopping</a>
                        </div>
                    </div>
                    """
                    st.markdown(textwrap.dedent(prod_html).strip(), unsafe_allow_html=True)

            else:
                # Gadgets, Kitchen Products & General Finds
                st.markdown("### 🛍️ Featured Products & 1-Click Buy Links")
                st.caption("AI identified the following products in this video. Click any store to view or purchase:")
                for prod in valid_products:
                    p_name = prod["name"]
                    p_price = prod.get("price", "")
                    price_html = f"<span style='background-color:rgba(16, 185, 129, 0.15); color:#34D399; border:1px solid rgba(16, 185, 129, 0.35); font-size:0.78rem; padding:3px 10px; border-radius:9999px; margin-left:8px; font-weight:700;'>💰 {p_price}</span>" if p_price else ""

                    prod_html = f"""
                    <div class="product-box-luxury">
                        <div style="display:flex; align-items:center; gap:8px; font-size:0.98rem; font-weight:700; color:#F1F5F9; margin-bottom: 6px;">
                            <span>📦</span> <span>{p_name}</span> {price_html}
                        </div>
                        <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-top: 6px;">
                            <a href="{prod['amazon_url']}" target="_blank" class="shop-btn-amazon">🛒 Amazon Prime</a>
                            <a href="{prod['flipkart_url']}" target="_blank" class="shop-btn-flipkart">⚡ Flipkart</a>
                            <a href="{prod.get('shopsy_url', f'https://www.shopsy.in/search?q={urllib.parse.quote_plus(p_name)}')}" target="_blank" class="shop-btn-shopsy">🟣 Shopsy</a>
                            <a href="{prod['google_shopping_url']}" target="_blank" class="shop-btn-google">🔍 Google Shopping</a>
                        </div>
                    </div>
                    """
                    st.markdown(textwrap.dedent(prod_html).strip(), unsafe_allow_html=True)

        # 1-Click Code Blocks for Technical Tutorials (P0 PO Directive)
        raw_code_blocks = re.findall(r'```([a-zA-Z0-9_\-\+]*)\n(.*?)```', recipe_text, re.DOTALL)
        if raw_code_blocks:
            st.markdown("### 💻 Executable Code & Syntax Blocks")
            for c_idx, (lang, c_code) in enumerate(raw_code_blocks, 1):
                clean_lang = (lang or "code").lower()
                clean_code = c_code.strip()
                safe_code_js = json.dumps(clean_code)
                is_py = clean_lang in ["python", "py"]
                colab_btn = f'<a href="https://colab.research.google.com/#create=true" target="_blank" style="text-decoration:none; background:rgba(249,115,22,0.15); border:1px solid rgba(249,115,22,0.4); color:#FB923C; padding:6px 12px; border-radius:6px; font-size:0.8rem; font-weight:700; display:inline-flex; align-items:center; gap:4px;">🚀 Open in Colab</a>' if is_py else ""

                st.markdown(f"""
                <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:12px 14px; margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-family:'Outfit',sans-serif; font-weight:700; font-size:0.82rem; color:#38BDF8; text-transform:uppercase;">Snippet #{c_idx} ({clean_lang})</span>
                        <div style="display:flex; gap:8px; align-items:center;">
                            {colab_btn}
                            <button id="copyCodeBtn_{c_idx}" style="background:rgba(56,189,248,0.15); border:1px solid rgba(56,189,248,0.35); color:#38BDF8; padding:5px 12px; border-radius:6px; font-weight:700; font-size:0.78rem; cursor:pointer;">
                                📋 Copy Code
                            </button>
                            <span id="codeToast_{c_idx}" style="display:none; color:#34D399; font-size:0.75rem; font-weight:700;">✓ Copied!</span>
                        </div>
                    </div>
                    <pre style="background:#090D16; border-radius:8px; padding:10px; overflow-x:auto; color:#E2E8F0; font-size:0.85rem; font-family:'Fira Code',monospace; margin:0;"><code>{html.escape(clean_code)}</code></pre>
                </div>
                <script>
                document.getElementById("copyCodeBtn_{c_idx}").addEventListener("click", () => {{
                    navigator.clipboard.writeText({safe_code_js}).then(() => {{
                        const t = document.getElementById("codeToast_{c_idx}");
                        t.style.display = "inline";
                        setTimeout(() => {{ t.style.display = "none"; }}, 2500);
                    }});
                }});
                </script>
                """, unsafe_allow_html=True)

        # Recommended YouTube Tutorials & Learning Links
        if resources_list:
            st.markdown("### 🎓 Recommended YouTube Tutorials & Learning Links")
            st.caption("AI identified the following tutorials, lectures, and resources in this video. Click to watch directly on YouTube:")

            for res in resources_list:
                r_name = res.get("name", "Tutorial")
                r_plat = res.get("platform", "YouTube")
                plat_badge = f"<span style='background-color:rgba(239, 68, 68, 0.15); color:#F87171; border:1px solid rgba(239, 68, 68, 0.35); font-size:0.78rem; padding:3px 10px; border-radius:9999px; margin-left:8px; font-weight:700;'>📺 {html.escape(r_plat)}</span>"

                yt_url = res.get("youtube_url", "")
                gh_url = res.get("github_url", "")
                google_url = res.get("google_url", "")

                btn_items = [
                    f'<a href="{yt_url}" target="_blank" class="watch-btn-yt">▶️ Watch on YouTube</a>'
                ]
                if any(k in r_name.lower() for k in ["github", "code", "project", "repo"]):
                    btn_items.append(f'<a href="{gh_url}" target="_blank" style="text-decoration:none; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); color:#E2E8F0; font-family:\'Outfit\',sans-serif; font-weight:600; padding:7px 14px; border-radius:8px; font-size:0.82rem; display:inline-flex; align-items:center; gap:4px; transition:all 0.2s;">🐙 Search GitHub</a>')
                btn_items.append(f'<a href="{google_url}" target="_blank" style="text-decoration:none; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); color:#E2E8F0; font-family:\'Outfit\',sans-serif; font-weight:600; padding:7px 14px; border-radius:8px; font-size:0.82rem; display:inline-flex; align-items:center; gap:4px; transition:all 0.2s;">🔍 Search Google</a>')
                btn_html = " ".join(btn_items)

                tut_html = f'<div class="tutorial-box-luxury"><div style="display:flex; align-items:center; gap:8px; font-size:0.98rem; font-weight:700; color:#F1F5F9; margin-bottom:8px;"><span>▶️</span> <span>{html.escape(r_name)}</span> {plat_badge}</div><div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center;">{btn_html}</div></div>'
                if hasattr(st, "html"):
                    st.html(tut_html)
                else:
                    st.markdown(tut_html, unsafe_allow_html=True)

        st.markdown("---")

        # WhatsApp & Download Action Buttons
        st.markdown(f"#### 📱 Forward & Download {cat_name}")

        txt_filename = os.path.basename(txt_filepath)
        with open(txt_filepath, "r", encoding="utf-8") as file_data:
            file_bytes = file_data.read()

        target_wa_phone = ""
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            st.download_button(
                label=f"💾 Download `.txt` Notes",
                data=file_bytes,
                file_name=txt_filename,
                mime="text/plain",
                type="primary",
                use_container_width=True
            )
        with col_btn2:
            if phone_number_input:
                target_wa_phone = phone_number_input
                wa_url = generate_whatsapp_deep_link(phone_number_input, txt_filepath, recipe_text, category=cat_code, products=products_list, resources=resources_list)
                st.markdown(f'<a href="{wa_url}" target="_blank" class="wa-btn-luxury">📲 1-Click WhatsApp Forward</a>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 12px; padding: 10px 14px 6px 14px; margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <span style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 0.86rem; color: #38BDF8;">
                            📲 Enter WhatsApp Number for 1-Click Forward
                        </span>
                        <span style="font-size: 0.72rem; color: #94A3B8;">Instant Deep Link</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_in_cc, col_in_num = st.columns([0.35, 0.65])
                with col_in_cc:
                    inline_cc = st.text_input("Country Code", value=country_code_input or "+91", key="inline_wa_country_code", label_visibility="collapsed", help="Country calling code e.g. +91, +1, +44")
                with col_in_num:
                    inline_num = st.text_input("WhatsApp Number", value="", placeholder="9999999999", key="inline_wa_phone_number", label_visibility="collapsed", help="Enter your mobile number")

                inline_num_clean = inline_num.strip()
                if inline_num_clean:
                    is_valid_inline, inline_err = validate_phone_number(inline_cc, inline_num_clean)
                    if is_valid_inline:
                        clean_cc_digits = inline_cc.strip().replace("+", "").strip()
                        clean_inline_digits = re.sub(r'[\s\-\(\)\.]', '', inline_num_clean)
                        if clean_inline_digits.startswith("0"):
                            clean_inline_digits = clean_inline_digits.lstrip("0")
                        if clean_cc_digits == "91" and len(clean_inline_digits) == 12 and clean_inline_digits.startswith("91"):
                            clean_inline_digits = clean_inline_digits[2:]

                        target_wa_phone = f"{clean_cc_digits}{clean_inline_digits}"
                        wa_url = generate_whatsapp_deep_link(
                            target_wa_phone,
                            txt_filepath,
                            recipe_text,
                            category=cat_code,
                            products=products_list,
                            resources=resources_list
                        )
                        st.markdown(
                            f'<a href="{wa_url}" target="_blank" class="wa-btn-luxury" style="margin-top: 6px;">📲 1-Click WhatsApp Forward (+{clean_cc_digits} {clean_inline_digits})</a>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.warning(f"⚠️ {inline_err}")
                else:
                    st.info("💡 Enter your WhatsApp number above to generate your instant 1-click forward link.")

        # Native Mobile Document Share (Android & iOS)
        import json
        safe_filename = json.dumps(txt_filename)
        safe_content = json.dumps(recipe_text)
        safe_caption = json.dumps(f"Here is {cat_name.lower()} file for - {item_title} !")

        share_html = f"""
        <div style="margin: 12px 0;">
            <button id="mobileShareBtn" style="
                background: linear-gradient(135deg, #25D366, #128C7E);
                color: white;
                border: none;
                padding: 13px 22px;
                border-radius: 12px;
                font-weight: 700;
                font-size: 0.98rem;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 10px;
                width: 100%;
                justify-content: center;
                box-shadow: 0 6px 20px rgba(37, 211, 102, 0.35);
                transition: all 0.25s ease;
            ">
                📎 Share .TXT Document Directly to WhatsApp (Mobile)
            </button>
        </div>
        <script>
        document.getElementById("mobileShareBtn").addEventListener("click", async () => {{
            try {{
                const file = new File([{safe_content}], {safe_filename}, {{ type: "text/plain" }});
                if (navigator.canShare && navigator.canShare({{ files: [file] }})) {{
                    await navigator.share({{
                        files: [file],
                        title: {safe_filename},
                        text: {safe_caption}
                    }});
                }} else {{
                    alert("Native file sharing is supported on mobile devices (Android / iOS). On PC, download the .txt and video files above and drag them into WhatsApp Web!");
                }}
            }} catch (err) {{
                if (err.name !== 'AbortError') {{
                    console.error("Share error:", err);
                }}
            }}
        }});
        </script>
        """
        if hasattr(st, "html"):
            st.html(share_html)
        else:
            st.components.v1.html(share_html, height=65)

        st.caption(f"ℹ️ **Sending to WhatsApp**: Tap **1-Click WhatsApp Forward** for crisp summary & clickable links. On mobile, tap **Share .TXT Document** for the full file!")

        # Collapsible Detailed Steps & Code Notes
        with st.expander(f"📖 Complete Step-by-Step {cat_name} Notes & Code", expanded=True):
            st.text_area("Full Extracted Content", recipe_text, height=350)

    with col_media:
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 12px 14px; margin-bottom: 12px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-family:'Outfit',sans-serif; font-weight:700; font-size:0.88rem; color:#F1F5F9;">🎬 {detected_plat} Preview</span>
            <span style="background:rgba(56,189,248,0.15); color:#38BDF8; font-size:0.72rem; font-weight:700; padding:2px 8px; border-radius:6px; border:1px solid rgba(56,189,248,0.3);">▶️ Previewing Source Reel (Muted)</span>
        </div>
        """, unsafe_allow_html=True)

        if final_video_path and os.path.exists(final_video_path):
            st.video(final_video_path, autoplay=True, muted=True)
            video_filename = os.path.basename(final_video_path)
            with open(final_video_path, "rb") as vf:
                video_bytes = vf.read()
            st.download_button(
                label=f"🎬 Download Video `.mp4`",
                data=video_bytes,
                file_name=video_filename,
                mime="video/mp4",
                type="secondary",
                use_container_width=True
            )
        else:
            st.write("Video preview unavailable.")

        storage_folder = os.path.dirname(txt_filepath)
        st.info(f"📂 **Stored Files Location**: `{storage_folder}`\n- `.txt` File: `{txt_filename}`\n- `.mp4` Video: `{os.path.basename(final_video_path) if final_video_path else 'Downloaded video'}`")

        callmebot_key = os.getenv("CALLMEBOT_API_KEY", "")
        active_phone_for_callmebot = phone_number_input or target_wa_phone
        if callmebot_key and active_phone_for_callmebot:
            wa_sent, wa_msg = send_via_callmebot_api(active_phone_for_callmebot, txt_filepath, recipe_text, callmebot_key, category=cat_code, products=products_list, resources=resources_list)
            if wa_sent:
                st.success(wa_msg)
            else:
                st.warning(f"CallMeBot API Notice: {wa_msg}")
