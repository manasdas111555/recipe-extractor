import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# Load local .env if available
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

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

def get_api_key() -> str:
    """Retrieve Gemini API Key from Streamlit Secrets or environment."""
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("GEMINI_API_KEY", "").strip()
        except Exception:
            pass
    return key

def save_api_key(api_key: str):
    """Save Gemini API Key locally."""
    env_content = f"GEMINI_API_KEY={api_key.strip()}\n"
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)
    os.environ["GEMINI_API_KEY"] = api_key.strip()
