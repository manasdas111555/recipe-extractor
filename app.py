import streamlit as st
import os
import sys
import time
from pathlib import Path

# Force UTF-8 encoding on Windows console for currency symbols (₹) and emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import importlib

try:
    from config import (
        get_api_key, 
        save_api_key, 
        get_download_dir, 
        get_affiliate_tags, 
        save_affiliate_tags, 
        cleanup_old_downloads,
        get_mistral_api_key,
        get_aionlabs_api_key,
        get_groq_api_key,
        get_nvidia_api_key,
        set_env_var,
        MAX_VIDEO_DURATION
    )
except ImportError:
    import config
    importlib.reload(config)
    from config import (
        get_api_key, 
        save_api_key, 
        get_download_dir, 
        get_affiliate_tags, 
        save_affiliate_tags, 
        cleanup_old_downloads,
        get_mistral_api_key,
        get_aionlabs_api_key,
        get_groq_api_key,
        get_nvidia_api_key,
        set_env_var,
        MAX_VIDEO_DURATION
    )

from downloader import get_video_from_url, detect_platform
from gemini_processor import process_video_and_generate_recipe
from ai_router import route_video_intelligence, AI_PROVIDERS

try:
    from whatsapp_service import (
        generate_whatsapp_deep_link, 
        send_via_callmebot_api, 
        get_recipe_display_name,
        get_default_country_code
    )
except ImportError:
    import whatsapp_service
    importlib.reload(whatsapp_service)
    from whatsapp_service import (
        generate_whatsapp_deep_link, 
        send_via_callmebot_api, 
        get_recipe_display_name,
        get_default_country_code
    )



# Purge old downloads upon session start to keep cloud storage lean
cleanup_old_downloads()

st.set_page_config(
    page_title="Universal Reel & Shorts AI Extractor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark Theme CSS
st.markdown("""
<style>
    .main-header {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #FF512F 0%, #DD2476 50%, #8E2DE2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #9CA3AF;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .wa-btn {
        display: inline-block;
        background-color: #25D366;
        color: white !important;
        font-weight: bold;
        padding: 12px 24px;
        border-radius: 8px;
        text-decoration: none;
        font-size: 1rem;
        margin-top: 10px;
    }
    .product-box {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar Settings
st.sidebar.image("https://img.icons8.com/color/96/instagram-reel.png", width=64)
st.sidebar.title("App Settings")

# Multi-Provider AI Keys Management
gemini_key = get_api_key()
mistral_key = get_mistral_api_key()
groq_key = get_groq_api_key()
nvidia_key = get_nvidia_api_key()
aionlabs_key = get_aionlabs_api_key()

active_providers = []
if gemini_key: active_providers.append("Gemini")
if mistral_key: active_providers.append("Mistral")
if groq_key: active_providers.append("Groq")
if nvidia_key: active_providers.append("NVIDIA")
if aionlabs_key: active_providers.append("AionLabs")

if active_providers:
    st.sidebar.success(f"🟢 Active Engines: {', '.join(active_providers)}")
else:
    st.sidebar.warning("⚠️ No AI API Key detected")

with st.sidebar.expander("🔑 Multi-Model API Keys", expanded=not bool(gemini_key or mistral_key or groq_key or nvidia_key)):
    st.caption("Configure free API keys for multi-model fallback:")
    g_input = st.text_input("Google Gemini API Key", value=gemini_key, type="password", help="Free tier from aistudio.google.com")
    m_input = st.text_input("Mistral AI API Key", value=mistral_key, type="password", help="Free tier from console.mistral.ai")
    gr_input = st.text_input("Groq API Key (Whisper + Llama)", value=groq_key, type="password", help="Free tier from console.groq.com")
    nv_input = st.text_input("NVIDIA API Key", value=nvidia_key, type="password", help="Free tier from build.nvidia.com")
    a_input = st.text_input("AionLabs API Key", value=aionlabs_key, type="password", help="API key from aionlabs.ai")

    if st.button("💾 Save All API Keys", use_container_width=True):
        if g_input: set_env_var("GEMINI_API_KEY", g_input)
        if m_input: set_env_var("MISTRALAI_API_KEY", m_input)
        if gr_input: set_env_var("GROQ_API_KEY", gr_input)
        if nv_input: set_env_var("NVIDIA_API_KEY", nv_input)
        if a_input: set_env_var("AIONLABS_AI_API_KEY", a_input)
        st.success("API keys saved and synced to .env!")
        st.rerun()

has_any_key = bool(gemini_key or mistral_key or groq_key or nvidia_key or aionlabs_key or g_input or m_input or gr_input or nv_input or a_input)

# WhatsApp Destination: Split into Country Code (defaulted by locale) + Mobile Number
st.sidebar.markdown("**WhatsApp Destination**")
col_cc, col_num = st.sidebar.columns([1, 2.3])
with col_cc:
    default_cc = get_default_country_code()
    country_code_input = st.text_input("Code", value=default_cc, help="Country calling code")
with col_num:
    local_phone_input = st.text_input("Phone Number", value="", placeholder="8056804940", help="Mobile number without country code")

phone_number_input = f"{country_code_input.strip()}{local_phone_input.strip()}" if local_phone_input.strip() else ""

callmebot_key = st.sidebar.text_input("CallMeBot API Key (Optional for Auto-SMS)", value="", type="password", help="Get free key by sending 'I allow callmebot to send me messages' to +34 644 44 20 70 on WhatsApp")

provider_choice = st.sidebar.selectbox(
    "AI Intelligence Provider",
    options=AI_PROVIDERS,
    index=0,
    help="Choose your AI pipeline. Google Gemini handles raw video natively. Mistral and Groq process extracted keyframes & audio."
)

if "gemini" in provider_choice.lower() or "auto" in provider_choice.lower():
    model_choice = st.sidebar.selectbox(
        "Gemini Model",
        options=["gemini-3.7-flash", "gemini-2.5-flash", "gemini-3.6-flash", "gemini-2.5-flash-lite", "gemini-3.8-flash", "gemini-3.1-pro-preview"],
        index=0,
        help="Default is gemini-3.7-flash (ultra-fast frontier model). If congested, it automatically cascades to fallback models."
    )
else:
    model_choice = "gemini-3.7-flash"

mode_choice = st.sidebar.selectbox(
    "Content Intelligence Mode",
    options=[
        "Auto-Detect (Universal AI)",
        "Cooking Recipe",
        "Fitness & Workout",
        "Tech & Coding Tutorial",
        "Travel & Food Guide",
        "Summary & Key Takeaways"
    ],
    index=0,
    help="Auto-Detect intelligently determines whether the video is a recipe, fitness routine, tech tutorial, or knowledge summary."
)

# Affiliate Monetization Tags Expander
with st.sidebar.expander("💼 Monetization & Affiliate IDs", expanded=False):
    st.caption("Earn 3%-10% commission whenever users click product links.")
    curr_tags = get_affiliate_tags()
    amz_tag_val = st.text_input("Amazon Associates Tag", value=curr_tags.get("amazon", ""), placeholder="yourtag-21")
    flp_tag_val = st.text_input("Flipkart Affiliate ID", value=curr_tags.get("flipkart", ""), placeholder="your_affid")
    if st.button("Save Affiliate Tags", use_container_width=True):
        save_affiliate_tags(amz_tag_val, flp_tag_val)
        st.success("Affiliate tags updated!")

st.sidebar.markdown("---")
st.sidebar.markdown(f"⏱️ **Limit**: Shorts & Reels <= {MAX_VIDEO_DURATION}s")
st.sidebar.markdown("☁️ **Deployment**: Hosted on **Streamlit Community Cloud** (100% Free)")



# Main UI
st.markdown("<div class='main-header'>Universal Reel & Shorts AI Extractor ⚡</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Turn any Instagram Reel or YouTube Short into structured recipes, workouts, tech tutorials, or knowledge notes!</div>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    reel_url = st.text_input(
        "🔗 Paste Instagram Reel or YouTube Shorts URL",
        placeholder="https://www.instagram.com/reel/... or https://youtube.com/shorts/..."
    )
    if reel_url and reel_url.strip():
        platform = detect_platform(reel_url.strip())
        st.caption(f"🎯 **Platform Detected**: `{platform}`")

    process_btn = st.button("⚡ Extract Intelligence & Generate .TXT Notes", type="primary", use_container_width=True)

with col2:
    st.markdown("### 📋 Automation Workflow")
    st.markdown("""
    1. 🌐 **Paste URL** (Instagram Reel or YouTube Short)
    2. 📥 **Download HD Stream** (Native single-pass download)
    3. ⚡ **Gemini 2.5 Multi-Modal AI** (Auto-classifies content with instant fallback)
    4. 📝 **Generate Structured Notes** (Apt title & `.txt` file)
    5. 📱 **Forward to WhatsApp** (File download + direct sharing)
    """)

if process_btn:
    if not reel_url or not reel_url.strip().startswith("http"):
        st.error("Please enter a valid video URL (e.g. Instagram Reel or YouTube Short).")
    elif not has_any_key:
        st.error("Please configure at least one AI API Key in the sidebar (Gemini, Mistral, or Groq).")
    else:
        start_time = time.perf_counter()
        clean_url = reel_url.strip()
        detected_plat = detect_platform(clean_url)
        status_box = st.status(f"Processing {detected_plat} with {provider_choice.split('(')[0].strip()}...", expanded=True)

        # Step 1 & 2: Download Video
        t_dl_start = time.perf_counter()
        status_box.write(f"⏳ **Step 1 & 2**: Downloading {detected_plat} stream...")
        success, video_result = get_video_from_url(clean_url, preferred_engine="ytdlp")
        dl_duration = time.perf_counter() - t_dl_start

        if not success:
            status_box.update(label="❌ Video Download Failed", state="error")
            st.error(f"Download Error: {video_result}")
        else:
            status_box.write(f"✅ Video stream downloaded in **{dl_duration:.1f}s**!")

            # Step 3, 4 & 5: AI Multimodal Processing via Central Router
            gemini_res = route_video_intelligence(
                video_path=video_result,
                provider=provider_choice,
                custom_gemini_key=gemini_key or g_input,
                custom_mistral_key=mistral_key or m_input,
                custom_groq_key=groq_key or gr_input,
                status_callback=status_box.write,
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

            if not gemini_success:
                status_box.update(label="❌ AI Intelligence Extraction Failed", state="error")
                st.error(f"Extraction Error: {recipe_text}")
            else:
                cat_name = meta.get("category_name", "Extracted Content")
                cat_emoji = meta.get("emoji", "📝")
                cat_code = meta.get("category", "RECIPE")
                item_title = meta.get("title", get_recipe_display_name(txt_filepath))
                timings = meta.get("timings", {})
                cloud_prep_time = timings.get('prep_s', 0.0) + timings.get('upload_s', 0.0)
                ai_duration = timings.get('inference_s', 0.0)
                model_display = timings.get('model_used', model_choice)

                status_box.update(label=f"🎉 {cat_name} Extracted in {total_elapsed:.1f}s: {item_title}!", state="complete")
                st.balloons()
                
                # High-Visibility Latency & Performance Benchmark
                st.markdown(f"#### ⚡ Latency & Execution Benchmark (`{total_elapsed:.1f}s` Total Turnaround)")
                b1, b2, b3, b4 = st.columns(4)
                b1.metric("⏱️ Total Turnaround", f"{total_elapsed:.1f}s")
                b2.metric("📥 Stream Download", f"{dl_duration:.1f}s")
                b3.metric("☁️ Cloud Upload & Prep", f"{cloud_prep_time:.1f}s")
                b4.metric(f"🧠 AI ({model_display})", f"{ai_duration:.1f}s")
                st.markdown("---")
                
                # Category Header Banner
                st.markdown(f"### {cat_emoji} {item_title}")
                st.markdown(f"<span class='badge-pill' style='background-color:#1E293B; color:#38BDF8; border:1px solid #38BDF8;'>🏷️ Detected Domain: {cat_name}</span>", unsafe_allow_html=True)
                
                if meta.get("summary"):
                    st.info(f"**Executive Summary**: {meta['summary']}")

                # Featured Products & 1-Click Purchase Links
                products_list = meta.get("products", [])
                if products_list:
                    st.markdown("### 🛍️ Featured Products & 1-Click Buy Links")
                    st.caption("AI identified the following products in this video. Click any store to view or purchase:")
                    
                    for prod in products_list:
                        p_name = prod["name"]
                        p_price = prod.get("price", "")
                        price_html = f"<span style='background-color:#064E3B; color:#34D399; border:1px solid #059669; font-size:0.8rem; padding:3px 9px; border-radius:12px; margin-left:8px; font-weight:600;'>💰 {p_price}</span>" if p_price else ""
                        
                        st.markdown(f"""
                        <div class="product-box">
                            <div style="font-size:1rem; font-weight:700; margin-bottom:8px; color:#F1F5F9;">
                                📦 {p_name} {price_html}
                            </div>
                            <div style="display:flex; gap:10px; flex-wrap:wrap;">
                                <a href="{prod['amazon_url']}" target="_blank" style="text-decoration:none; background:#FF9900; color:#111; font-weight:700; padding:6px 14px; border-radius:6px; font-size:0.85rem; display:inline-flex; align-items:center; gap:4px;">🛒 Amazon</a>
                                <a href="{prod['google_shopping_url']}" target="_blank" style="text-decoration:none; background:#4285F4; color:#fff; font-weight:700; padding:6px 14px; border-radius:6px; font-size:0.85rem; display:inline-flex; align-items:center; gap:4px;">🛍️ Google Shopping</a>
                                <a href="{prod['flipkart_url']}" target="_blank" style="text-decoration:none; background:#2874F0; color:#fff; font-weight:700; padding:6px 14px; border-radius:6px; font-size:0.85rem; display:inline-flex; align-items:center; gap:4px;">📦 Flipkart</a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("---")
                
                # WhatsApp & Download Action Buttons
                st.subheader(f"📱 Forward & Download {cat_name}")

                txt_filename = os.path.basename(txt_filepath)
                with open(txt_filepath, "r", encoding="utf-8") as file_data:
                    file_bytes = file_data.read()

                # Action columns
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

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
                    if final_video_path and os.path.exists(final_video_path):
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

                with col_btn3:
                    if phone_number_input:
                        wa_url = generate_whatsapp_deep_link(phone_number_input, txt_filepath, recipe_text, category=cat_code, products=products_list)
                        st.markdown(f'<a href="{wa_url}" target="_blank" class="wa-btn" style="text-align:center; display:block; margin-top:0; padding:10px 14px; font-size:0.95rem;">📲 Send to WhatsApp</a>', unsafe_allow_html=True)
                    else:
                        st.info("💡 Enter WhatsApp Number in sidebar!")

                # Native Mobile Document Share (Android & iOS)
                import json
                safe_filename = json.dumps(txt_filename)
                safe_content = json.dumps(recipe_text)
                safe_caption = json.dumps(f"Here is {cat_name.lower()} file for - {item_title} !")
                
                share_html = f"""
                <div style="margin: 10px 0;">
                    <button id="mobileShareBtn" style="
                        background: linear-gradient(135deg, #25D366, #128C7E);
                        color: white;
                        border: none;
                        padding: 12px 20px;
                        border-radius: 8px;
                        font-weight: 600;
                        font-size: 0.95rem;
                        cursor: pointer;
                        display: flex;
                        align-items: center;
                        gap: 8px;
                        width: 100%;
                        justify-content: center;
                        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.25);
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



                st.caption(f"ℹ️ **Sending Video + {cat_name} to WhatsApp**: Download both the `.txt` notes and `.mp4` video above and drag them into WhatsApp Web. On mobile, tap the green **Share .TXT Document** button!")

                # Local vs Cloud Storage Location Info
                storage_folder = os.path.dirname(txt_filepath)
                st.info(f"📂 **Stored Files Location**: `{storage_folder}`\n- `.txt` File: `{txt_filename}`\n- `.mp4` Video: `{os.path.basename(final_video_path) if final_video_path else 'Downloaded video'}`")

                if callmebot_key and phone_number_input:
                    wa_sent, wa_msg = send_via_callmebot_api(phone_number_input, txt_filepath, recipe_text, callmebot_key, category=cat_code, products=products_list)
                    if wa_sent:
                        st.success(wa_msg)
                    else:
                        st.warning(f"CallMeBot API Notice: {wa_msg}")

                st.markdown("---")

                col_preview1, col_preview2 = st.columns([1, 1])
                with col_preview1:
                    st.subheader(f"📖 Extracted {cat_name} Notes")
                    st.text_area("Detailed Content", recipe_text, height=380)
                with col_preview2:
                    st.subheader(f"🎬 {detected_plat} Preview")
                    if final_video_path and os.path.exists(final_video_path):
                        st.video(final_video_path)
                    else:
                        st.write("Video preview unavailable.")
