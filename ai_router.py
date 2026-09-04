import os
import sys
import time
from pathlib import Path
from typing import Tuple, Dict, Any

from config import (
    get_api_key,
    get_mistral_api_key,
    get_groq_api_key,
    get_affiliate_tags
)
from gemini_processor import process_video_and_generate_recipe, safe_print
from mistral_processor import process_video_with_mistral
from groq_processor import process_video_with_groq

AI_PROVIDERS = [
    "Google Gemini (Native Video AI)",
    "Mistral AI (Vision + Audio Keyframes)",
    "Groq (Whisper-v3 + Llama 3.3 70B)",
    "Auto-Universal (Gemini with Multi-Model Fallback)"
]

def route_video_intelligence(
    video_path: str,
    provider: str = "Google Gemini (Native Video AI)",
    custom_gemini_key: str = None,
    custom_mistral_key: str = None,
    custom_groq_key: str = None,
    status_callback = None,
    gemini_model_preference: str = "gemini-2.5-flash",
    extraction_mode: str = "Auto-Detect",
    affiliate_tags: dict = None
) -> Tuple[bool, str, str, str, Dict[str, Any]]:
    """
    Central router that dispatches video extraction to the selected AI provider,
    handling automatic multi-provider fallback if requested.
    """
    prov = (provider or "Google Gemini").lower()
    tags = affiliate_tags or get_affiliate_tags()

    def notify(msg: str):
        safe_print(f"[Router] {msg}")
        if status_callback:
            try:
                status_callback(msg)
            except Exception:
                pass

    # 1. Direct Mistral AI Selection
    if "mistral" in prov and "auto" not in prov:
        notify("Routing to Mistral AI Engine...")
        return process_video_with_mistral(
            video_path=video_path,
            custom_api_key=custom_mistral_key or get_mistral_api_key(),
            status_callback=status_callback,
            extraction_mode=extraction_mode,
            affiliate_tags=tags
        )

    # 2. Direct Groq Selection
    if "groq" in prov and "auto" not in prov:
        notify("Routing to Groq (Whisper-v3 + Llama 3.3 70B) Engine...")
        return process_video_with_groq(
            video_path=video_path,
            custom_api_key=custom_groq_key or get_groq_api_key(),
            status_callback=status_callback,
            extraction_mode=extraction_mode,
            affiliate_tags=tags
        )

    # 3. Direct Google Gemini Selection
    if "gemini" in prov and "auto" not in prov:
        return process_video_and_generate_recipe(
            video_path=video_path,
            custom_api_key=custom_gemini_key or get_api_key(),
            status_callback=status_callback,
            model_preference=gemini_model_preference,
            extraction_mode=extraction_mode,
            affiliate_tags=tags
        )

    # 4. Auto-Universal Strategy: Gemini 2.5 Flash -> Mistral -> Groq
    notify("Auto-Universal Mode: Primary dispatch to Gemini 2.5 Flash...")
    gemini_res = process_video_and_generate_recipe(
        video_path=video_path,
        custom_api_key=custom_gemini_key or get_api_key(),
        status_callback=status_callback,
        model_preference=gemini_model_preference or "gemini-2.5-flash",
        extraction_mode=extraction_mode,
        affiliate_tags=tags
    )

    if gemini_res[0]:
        return gemini_res

    # If Gemini failed, try Mistral if key is available
    mistral_k = custom_mistral_key or get_mistral_api_key()
    if mistral_k:
        notify("⚠️ Gemini unavailable. Falling over to Mistral AI Vision Engine...")
        mistral_res = process_video_with_mistral(
            video_path=video_path,
            custom_api_key=mistral_k,
            status_callback=status_callback,
            extraction_mode=extraction_mode,
            affiliate_tags=tags
        )
        if mistral_res[0]:
            return mistral_res

    # If Mistral failed or no key, try Groq if key is available
    groq_k = custom_groq_key or get_groq_api_key()
    if groq_k:
        notify("⚠️ Falling over to Groq Whisper + Llama 3.3 70B Engine...")
        groq_res = process_video_with_groq(
            video_path=video_path,
            custom_api_key=groq_k,
            status_callback=status_callback,
            extraction_mode=extraction_mode,
            affiliate_tags=tags
        )
        if groq_res[0]:
            return groq_res

    # Return original Gemini error if fallbacks were unavailable or failed
    return gemini_res
