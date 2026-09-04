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
    Retrieve Amazon Associates and Flipkart affiliate tags
    from environment variables, Streamlit secrets, or defaults.
    """
    amazon_tag = os.environ.get("AMAZON_AFFILIATE_TAG", "").strip()
    flipkart_tag = os.environ.get("FLIPKART_AFFILIATE_TAG", "").strip()
    
    if not amazon_tag:
        try:
            import streamlit as st
            amazon_tag = st.secrets.get("AMAZON_AFFILIATE_TAG", "").strip()
        except Exception:
            pass
            
    if not flipkart_tag:
        try:
            import streamlit as st
            flipkart_tag = st.secrets.get("FLIPKART_AFFILIATE_TAG", "").strip()
        except Exception:
            pass

    return {
        "amazon": amazon_tag,
        "flipkart": flipkart_tag
    }

def save_affiliate_tags(amazon_tag: str = "", flipkart_tag: str = ""):
    """Save affiliate tags to .env and active process environment."""
    lines = []
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            lines = [l for l in f.readlines() if not (l.startswith("AMAZON_AFFILIATE_TAG=") or l.startswith("FLIPKART_AFFILIATE_TAG="))]
    
    if amazon_tag.strip():
        lines.append(f"AMAZON_AFFILIATE_TAG={amazon_tag.strip()}\n")
        os.environ["AMAZON_AFFILIATE_TAG"] = amazon_tag.strip()
    if flipkart_tag.strip():
        lines.append(f"FLIPKART_AFFILIATE_TAG={flipkart_tag.strip()}\n")
        os.environ["FLIPKART_AFFILIATE_TAG"] = flipkart_tag.strip()

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

