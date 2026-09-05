import os
import time
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# Load local .env if available
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Video duration limit (seconds) to prevent quota burn and abuse
MAX_VIDEO_DURATION = 90

def get_download_dir() -> Path:
    """
    Returns download folder path. Uses C:\\Users\\admin\\Downloads\\Reciepe if on local Windows,
    otherwise uses temp directory or local ./downloads on Streamlit Cloud.
    """
    local_target = Path(r"C:\Users\admin\Downloads\Reciepe")
    if os.name == "nt" and local_target.parent.exists():
        local_target.mkdir(parents=True, exist_ok=True)
        return local_target
    else:
        cloud_target = Path(__file__).parent / "downloads"
        cloud_target.mkdir(parents=True, exist_ok=True)
        return cloud_target

# Alias for backwards compatibility
ensure_download_dir = get_download_dir

def cleanup_old_downloads(max_age_minutes: int = 60):
    """
    Deletes temporary video and media files older than max_age_minutes
    to prevent cloud servers and local disks from running out of space.
    """
    try:
        download_dir = get_download_dir()
        if not download_dir.exists():
            return
        now = time.time()
        cutoff = now - (max_age_minutes * 60)
        for item in download_dir.iterdir():
            if item.is_file() and item.suffix.lower() in [".mp4", ".mkv", ".webm", ".tmp", ".part"]:
                try:
                    if item.stat().st_mtime < cutoff:
                        item.unlink(missing_ok=True)
                except Exception:
                    pass
    except Exception:
        pass

def get_env_var(var_name: str, default: str = "") -> str:
    """Retrieve environment variable, checking .env, process environment, and Streamlit secrets."""
    if env_path.exists():
        try:
            load_dotenv(env_path, override=True)
        except Exception:
            pass
    val = os.environ.get(var_name, "").strip()
    if not val:
        try:
            import streamlit as st
            val = st.secrets.get(var_name, "").strip()
        except Exception:
            pass
    return val or default

def set_env_var(var_name: str, value: str):
    """Safely updates or appends an environment variable in .env and active process environment."""
    var_name = var_name.strip()
    value = value.strip()
    lines = []
    found = False
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(f"{var_name}="):
                    lines.append(f"{var_name}={value}\n")
                    found = True
                else:
                    lines.append(line)
    if not found:
        lines.append(f"{var_name}={value}\n")
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    os.environ[var_name] = value

def get_api_key() -> str:
    """Retrieve Gemini API Key from Streamlit Secrets or environment."""
    return get_env_var("GEMINI_API_KEY")

def save_api_key(api_key: str):
    """Save Gemini API Key locally in .env."""
    set_env_var("GEMINI_API_KEY", api_key)

def get_mistral_api_key() -> str:
    """Retrieve Mistral API Key from environment or secrets."""
    return get_env_var("MISTRALAI_API_KEY")

def get_aionlabs_api_key() -> str:
    """Retrieve AionLabs API Key from environment or secrets."""
    return get_env_var("AIONLABS_AI_API_KEY")

def get_groq_api_key() -> str:
    """Retrieve Groq API Key from environment or secrets."""
    return get_env_var("GROQ_API_KEY")

def get_nvidia_api_key() -> str:
    """Retrieve NVIDIA API Key from environment or secrets."""
    return get_env_var("NVIDIA_API_KEY")

def get_affiliate_tags() -> dict:
    """
    Retrieve Amazon Associates, Flipkart, Meesho, and aggregator (Cuelinks/EarnKaro) affiliate tags
    from environment variables, Streamlit secrets, or defaults.
    """
    amazon_tag = os.environ.get("AMAZON_AFFILIATE_TAG", "").strip()
    flipkart_tag = os.environ.get("FLIPKART_AFFILIATE_TAG", "").strip()
    meesho_tag = os.environ.get("MEESHO_AFFILIATE_TAG", "").strip()
    cuelinks_id = os.environ.get("CUELINKS_ID", "").strip()
    earnkaro_id = os.environ.get("EARNKARO_ID", "").strip()
    
    try:
        import streamlit as st
        if not amazon_tag:
            amazon_tag = st.secrets.get("AMAZON_AFFILIATE_TAG", "").strip()
        if not flipkart_tag:
            flipkart_tag = st.secrets.get("FLIPKART_AFFILIATE_TAG", "").strip()
        if not meesho_tag:
            meesho_tag = st.secrets.get("MEESHO_AFFILIATE_TAG", "").strip()
        if not cuelinks_id:
            cuelinks_id = st.secrets.get("CUELINKS_ID", "").strip()
        if not earnkaro_id:
            earnkaro_id = st.secrets.get("EARNKARO_ID", "").strip()
    except Exception:
        pass

    return {
        "amazon": amazon_tag,
        "flipkart": flipkart_tag,
        "meesho": meesho_tag,
        "cuelinks": cuelinks_id,
        "earnkaro": earnkaro_id
    }

def save_affiliate_tags(amazon_tag: str = "", flipkart_tag: str = "", meesho_tag: str = "", cuelinks_id: str = "", earnkaro_id: str = ""):
    """Save affiliate and aggregator tags to .env and active process environment."""
    keys_to_clean = ["AMAZON_AFFILIATE_TAG=", "FLIPKART_AFFILIATE_TAG=", "MEESHO_AFFILIATE_TAG=", "CUELINKS_ID=", "EARNKARO_ID="]
    lines = []
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            lines = [l for l in f.readlines() if not any(l.startswith(k) for k in keys_to_clean)]
    
    def _add_tag(key: str, val: str):
        if val.strip():
            lines.append(f"{key}={val.strip()}\n")
            os.environ[key] = val.strip()

    _add_tag("AMAZON_AFFILIATE_TAG", amazon_tag)
    _add_tag("FLIPKART_AFFILIATE_TAG", flipkart_tag)
    _add_tag("MEESHO_AFFILIATE_TAG", meesho_tag)
    _add_tag("CUELINKS_ID", cuelinks_id)
    _add_tag("EARNKARO_ID", earnkaro_id)

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)


