import streamlit as st
import os
import sys
from pathlib import Path

# Force UTF-8 encoding on Windows console for currency symbols (₹) and emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from config import get_api_key, save_api_key, get_download_dir
from downloader import get_video_from_url, detect_platform
from gemini_processor import process_video_and_generate_recipe
from whatsapp_service import generate_whatsapp_deep_link, send_via_callmebot_api, get_recipe_display_name

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

api_key_input = st.sidebar.text_input("Gemini API Key", value=get_api_key(), type="password", help="Get free key at aistudio.google.com")
if api_key_input and api_key_input != get_api_key():
    save_api_key(api_key_input)
    st.sidebar.success("API Key saved!")

phone_number_input = st.sidebar.text_input("WhatsApp Phone Number", value="", placeholder="919876543210")
callmebot_key = st.sidebar.text_input("CallMeBot API Key (Optional for Auto-SMS)", value="", type="password", help="Get free key by sending 'I allow callmebot to send me messages' to +34 644 44 20 70 on WhatsApp")

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

model_choice = st.sidebar.selectbox(
    "Gemini Model",
    options=["gemini-3.8-flash", "gemini-3.1-pro-preview", "gemini-2.5-flash", "gemini-2.5-flash-lite"],
    index=0,
    help="Default is gemini-3.8-flash (latest frontier model). You can also toggle gemini-3.1-pro-preview or gemini-2.5-flash."
)

st.sidebar.markdown("---")
st.sidebar.markdown("☁️ **Deployment**: Hosted on **Streamlit Community Cloud** (100% Free Domain)")

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
    3. 🤖 **Gemini 3.8 Multi-Modal AI** (Auto-classifies content)
    4. 📝 **Generate Structured Notes** (Apt title & `.txt` file)
    5. 📱 **Forward to WhatsApp** (File download + direct sharing)
    """)

if process_btn:
    if not reel_url or not reel_url.strip().startswith("http"):
        st.error("Please enter a valid video URL (e.g. Instagram Reel or YouTube Short).")
    elif not api_key_input:
        st.error("Please enter your Gemini API Key in the sidebar.")
    else:
        clean_url = reel_url.strip()
        detected_plat = detect_platform(clean_url)
        status_box = st.status(f"Processing {detected_plat} Request...", expanded=True)

        # Step 1 & 2: Download Video
        status_box.write(f"⏳ **Step 1 & 2**: Downloading {detected_plat} stream...")
        success, video_result = get_video_from_url(clean_url, preferred_engine="ytdlp")

        if not success:
            status_box.update(label="❌ Video Download Failed", state="error")
            st.error(f"Download Error: {video_result}")
        else:
            status_box.write("✅ Video stream downloaded successfully!")

            # Step 3, 4 & 5: Upload to Gemini & Generate Structured Notes
            gemini_res = process_video_and_generate_recipe(
                video_result, 
                custom_api_key=api_key_input,
                status_callback=status_box.write,
                model_preference=model_choice,
                extraction_mode=mode_choice
            )
            gemini_success = gemini_res[0]
            txt_filepath = gemini_res[1]
            recipe_text = gemini_res[2]
            final_video_path = gemini_res[3] if len(gemini_res) > 3 else video_result
            meta = gemini_res[4] if len(gemini_res) > 4 else {}

            if not gemini_success:
                status_box.update(label="❌ Gemini AI Processing Failed", state="error")
                st.error(f"Gemini Error: {recipe_text}")
            else:
                cat_name = meta.get("category_name", "Extracted Content")
                cat_emoji = meta.get("emoji", "📝")
                cat_code = meta.get("category", "RECIPE")
                item_title = meta.get("title", get_recipe_display_name(txt_filepath))

                status_box.update(label=f"🎉 {cat_name} Extracted: {item_title}!", state="complete")
                st.balloons()
                
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
