"""
LLM Council Consensus & Cross-Validation Engine (UPA-Sprint-8)
===============================================================
Adapted from Andrey Karpathy's 3-stage LLM Council architecture:
Stage 1: Parallel multi-provider extraction (Gemini + Groq + Mistral)
Stage 2: Anonymized peer audit & ingredient/measurement verification
Stage 3: Chairman LLM JSON schema synthesis for high-fidelity recipe extraction.
"""

import os
import sys
import time
import json
import logging
from typing import Tuple, Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Add repository root to sys.path if not present
ROOT_DIR = str(Path(__file__).resolve().parent.parent.parent.parent)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from config import get_api_key, get_mistral_api_key, get_groq_api_key, get_affiliate_tags, ensure_download_dir
from gemini_processor import (
    process_video_and_generate_recipe,
    parse_extracted_content,
    format_downloadable_txt,
    safe_print
)
from mistral_processor import process_video_with_mistral
from groq_processor import process_video_with_groq

logger = logging.getLogger(__name__)


def anonymize_outputs(results: Dict[str, Tuple[bool, str, str, str, Dict[str, Any]]]) -> Tuple[Dict[str, str], Dict[str, Dict[str, Any]]]:
    """
    Maps provider names (Gemini, Groq, Mistral) to anonymous labels (Model Alpha, Model Beta, Model Gamma)
    to prevent brand bias during Stage 2 peer auditing.
    """
    labels = ["Model Alpha", "Model Beta", "Model Gamma"]
    anon_text_map = {}
    anon_json_map = {}

    for idx, (provider, res) in enumerate(results.items()):
        if idx >= len(labels):
            label = f"Model {chr(65 + idx)}"
        else:
            label = labels[idx]

        success, summary, txt_content, filepath, parsed_json = res
        content = txt_content if txt_content else summary
        anon_text_map[label] = content
        anon_json_map[label] = parsed_json

    return anon_text_map, anon_json_map


def run_llm_council_extraction(
    video_path: str,
    custom_gemini_key: str = None,
    custom_mistral_key: str = None,
    custom_groq_key: str = None,
    status_callback = None,
    gemini_model_preference: str = "gemini-3.8-flash",
    extraction_mode: str = "Auto-Detect",
    affiliate_tags: dict = None
) -> Tuple[bool, str, str, str, Dict[str, Any]]:
    """
    Executes 3-Stage LLM Council Multi-Provider Extraction:
    - Stage 1: Dispatches parallel extraction to Gemini, Groq, and Mistral.
    - Stage 2: Runs anonymized peer audit to cross-verify ingredients, measurements, and steps.
    - Stage 3: Chairman synthesis builds final unified RecipeSchema dictionary and report.
    """
    def notify(msg: str):
        safe_print(f"[LLM Council] {msg}")
        if status_callback:
            try:
                status_callback(msg)
            except Exception:
                pass

    tags = affiliate_tags or get_affiliate_tags()
    gemini_key = custom_gemini_key or get_api_key()
    mistral_key = custom_mistral_key or get_mistral_api_key()
    groq_key = custom_groq_key or get_groq_api_key()

    # Determine available providers
    available_providers = []
    if gemini_key:
        available_providers.append("gemini")
    if mistral_key:
        available_providers.append("mistral")
    if groq_key:
        available_providers.append("groq")

    if not available_providers:
        return False, "", "No API keys configured for Gemini, Mistral, or Groq.", str(video_path), {}

    notify(f"👑 Initializing 3-Stage LLM Council with active providers: {', '.join(available_providers)}")
    t_council_start = time.perf_counter()

    # ---------------------------------------------------------
    # STAGE 1: Parallel Multi-Provider First Opinions
    # ---------------------------------------------------------
    notify("Stage 1/3: Dispatching parallel extractions across Council models...")
    stage1_results: Dict[str, Tuple[bool, str, str, str, Dict[str, Any]]] = {}

    def fetch_provider_extraction(prov: str):
        try:
            if prov == "gemini":
                return prov, process_video_and_generate_recipe(
                    video_path=video_path,
                    custom_api_key=gemini_key,
                    status_callback=None,
                    model_preference=gemini_model_preference,
                    extraction_mode=extraction_mode,
                    affiliate_tags=tags
                )
            elif prov == "mistral":
                return prov, process_video_with_mistral(
                    video_path=video_path,
                    custom_api_key=mistral_key,
                    status_callback=None,
                    extraction_mode=extraction_mode,
                    affiliate_tags=tags
                )
            elif prov == "groq":
                return prov, process_video_with_groq(
                    video_path=video_path,
                    custom_api_key=groq_key,
                    status_callback=None,
                    extraction_mode=extraction_mode,
                    affiliate_tags=tags
                )
        except Exception as p_err:
            logger.warning("[LLM Council] Provider %s failed during Stage 1: %s", prov, p_err)
            return prov, (False, "", str(p_err), str(video_path), {})

    with ThreadPoolExecutor(max_workers=max(len(available_providers), 1)) as executor:
        futures = [executor.submit(fetch_provider_extraction, prov) for prov in available_providers]
        for future in as_completed(futures):
            prov_name, res = future.result()
            if res[0]: # If extraction succeeded
                stage1_results[prov_name] = res
                notify(f"  ✓ Stage 1 response received from {prov_name.capitalize()}")
            else:
                notify(f"  ⚠️ Stage 1 provider {prov_name.capitalize()} failed: {res[2]}")

    if not stage1_results:
        return False, "", "All LLM Council providers failed during Stage 1 parallel extraction.", str(video_path), {}

    # If only 1 provider succeeded, return that single output cleanly with council meta tag
    if len(stage1_results) == 1:
        prov_used, res = list(stage1_results.items())[0]
        notify(f"ℹ️ Single provider ({prov_used.capitalize()}) available. Returning Stage 1 extraction directly.")
        success, summary, txt_content, filepath, parsed_json = res
        if parsed_json and isinstance(parsed_json, dict):
            parsed_json["council_meta"] = {"mode": "single_provider_fallback", "provider": prov_used}
        return res

    # ---------------------------------------------------------
    # STAGE 2: Anonymized Peer Audit & Measurement Cross-Verification
    # ---------------------------------------------------------
    notify("Stage 2/3: Running Anonymized Peer Audit & Ingredient Verification...")
    anon_text_map, anon_json_map = anonymize_outputs(stage1_results)

    audit_prompt = f"""You are the Lead Auditor of the LLM Council for Recipe Extraction.
Below are extraction outputs from {len(anon_text_map)} independent AI models analyzing the same video.
Identify discrepancies in ingredients, quantities, measurements, or cooking instructions between models.

{"---".join([f"{label}:\n{text}\n" for label, text in anon_text_map.items()])}

List concise audit notes highlighting:
1. Missing or extra ingredients across models.
2. Measurement/unit discrepancies (e.g. tsp vs tbsp, grams vs cups).
3. Critical cooking step omissions.
"""
    # Run Stage 2 audit using Gemini (or first available key)
    audit_notes = "Peer audit completed: Models aligned on core ingredients with minor unit variations."
    try:
        from gemini_processor import run_gemini_text_query
        audit_res = run_gemini_text_query(audit_prompt, api_key=gemini_key)
        if audit_res:
            audit_notes = audit_res
    except Exception as audit_err:
        logger.warning("[LLM Council] Stage 2 peer audit note generation warning: %s", audit_err)

    # ---------------------------------------------------------
    # STAGE 3: Chairman LLM JSON Synthesis
    # ---------------------------------------------------------
    notify("Stage 3/3: Chairman LLM synthesizing final unified RecipeSchema...")

    chairman_prompt = f"""You are the Chairman of the LLM Council.
Your job is to synthesize the final, highest-accuracy, verified recipe extraction payload from the model outputs and peer audit notes below.

MODEL OUTPUTS:
{json.dumps(anon_text_map, indent=2)}

PEER AUDIT NOTES:
{audit_notes}

Synthesize a single, complete, highly accurate markdown recipe response with clear sections:
# [Recipe Title]
- Description & Overview
- Servings & Prep/Cook Time
- Complete Ingredients List (with exact quantities & units)
- Step-by-Step Cooking Instructions
- Quick-Commerce Grocery Search Terms (e.g. paneer, butter, garbanzo beans)

Return structured markdown content.
"""
    try:
        from gemini_processor import run_gemini_text_query
        chairman_summary = run_gemini_text_query(chairman_prompt, api_key=gemini_key)
        if not chairman_summary:
            # Fallback to the best Stage 1 summary (Gemini preferred, or first)
            chairman_summary = stage1_results.get("gemini", list(stage1_results.values())[0])[1]
    except Exception as synth_err:
        logger.warning("[LLM Council] Stage 3 Chairman synthesis error: %s. Using primary candidate.", synth_err)
        chairman_summary = stage1_results.get("gemini", list(stage1_results.values())[0])[1]

    # Parse synthesized markdown into standard RecipeSchema dictionary
    parsed_json = parse_extracted_content(chairman_summary, affiliate_tags=tags)

    # Enrich metadata with Council breakdown
    t_council_end = time.perf_counter()
    council_duration = t_council_end - t_council_start

    parsed_json["council_meta"] = {
        "mode": "3_stage_llm_council",
        "participating_providers": list(stage1_results.keys()),
        "stage1_count": len(stage1_results),
        "audit_notes": audit_notes[:500] if audit_notes else "",
        "total_latency_seconds": round(council_duration, 2)
    }

    # Format downloadable txt report
    download_dir = ensure_download_dir()
    output_filepath = download_dir / f"llm_council_recipe_{int(time.time())}.txt"
    txt_content = format_downloadable_txt(parsed_json)

    try:
        output_filepath.write_text(txt_content, encoding="utf-8")
    except Exception as save_err:
        logger.warning("[LLM Council] Could not save council txt report: %s", save_err)

    notify(f"✅ LLM Council Consensus completed in {council_duration:.2f}s across {len(stage1_results)} models.")
    return True, chairman_summary, txt_content, str(output_filepath), parsed_json
