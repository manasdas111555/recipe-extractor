import streamlit as st
import os
from pathlib import Path

from config import get_api_key, save_api_key, get_download_dir
from downloader import get_recipe_video
from gemini_processor import process_video_and_generate_recipe
from whatsapp_service import generate_whatsapp_deep_link, send_via_callmebot_api, get_recipe_display_name

st.set_page_config(
    page_title="Instagram Reel Recipe AI Extractor",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark Theme CSS
st.markdown("""
<style>
    .main-header {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #FF512F 0%, #DD2476 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #9CA3AF;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .stCard {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
    }
    .wa-btn {
        display: inline-block;
        background-color: #25D366;
        color: white !important;
        font-weight: bold;
        padding: 12px 24px;
        border-radius: 8px;
        text-decoration: none;
        font-size: 1.1rem;
        margin-top: 10px;
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

model_choice = st.sidebar.selectbox(
    "Gemini Model",
    options=["gemini-3.8-flash", "gemini-3.1-pro-preview", "gemini-2.5-flash", "gemini-2.5-flash-lite"],
    index=0,
    help="Default is gemini-3.8-flash (latest frontier model). You can also toggle gemini-3.1-pro-preview or gemini-2.5-flash."
)

st.sidebar.markdown("---")
st.sidebar.markdown("☁️ **Deployment**: Hosted on **Streamlit Community Cloud** (100% Free Domain)")

# Main UI
st.markdown("<div class='main-header'>Instagram Reel Recipe Extractor</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Automated recipe downloading, Gemini AI transcription, `.txt` file generation, and WhatsApp sharing</div>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    reel_url = st.text_input("🔗 Paste Instagram Reel Link", placeholder="https://www.instagram.com/reel/C3abc123xyz/")
    process_btn = st.button("🚀 Extract Recipe & Generate .TXT File", type="primary", use_container_width=True)

with col2:
    st.markdown("### 📋 Automation Workflow")
    st.markdown("""
    1. 🌐 Paste Instagram Reel Link
    2. 📥 Download HD Video
    3. 🤖 Upload to Gemini AI & process prompt
    4. 📝 Save `.txt` recipe file with dish name
    5. 📱 Send recipe & caption to WhatsApp
    """)

if process_btn:
    if not reel_url or "instagram.com" not in reel_url:
        st.error("Please enter a valid Instagram Reel URL.")
    elif not api_key_input:
        st.error("Please enter your Gemini API Key in the sidebar.")
    else:
        status_box = st.status("Processing Recipe Request...", expanded=True)

        # Step 1 & 2: Download Video
        status_box.write("⏳ **Step 1 & 2**: Downloading Reel video...")
        success, video_result = get_recipe_video(reel_url, preferred_engine="ytdlp")

        if not success:
            status_box.update(label="❌ Video Download Failed", state="error")
            st.error(f"Download Error: {video_result}")
        else:
            status_box.write("✅ Video downloaded successfully!")

            # Step 3, 4 & 5: Upload to Gemini & Generate TXT
            gemini_success, txt_filepath, recipe_text = process_video_and_generate_recipe(
                video_result, 
                custom_api_key=api_key_input,
                status_callback=status_box.write,
                model_preference=model_choice
            )

            if not gemini_success:
                status_box.update(label="❌ Gemini AI Processing Failed", state="error")
                st.error(f"Gemini Error: {recipe_text}")
            else:
                recipe_name = get_recipe_display_name(txt_filepath)
                status_box.update(label=f"🎉 Recipe extracted for: {recipe_name}!", state="complete")
                st.balloons()
                st.success(f"Recipe extracted successfully: **{recipe_name}**!")

                st.markdown("---")
                
                # WhatsApp Action Buttons
                st.subheader("📱 Forward to WhatsApp")
                
                if callmebot_key and phone_number_input:
                    wa_sent, wa_msg = send_via_callmebot_api(phone_number_input, txt_filepath, recipe_text, callmebot_key)
                    if wa_sent:
                        st.success(wa_msg)
                    else:
                        st.warning(f"CallMeBot API Notice: {wa_msg}")
                
                if phone_number_input:
                    wa_url = generate_whatsapp_deep_link(phone_number_input, txt_filepath, recipe_text)
                    st.markdown(f'<a href="{wa_url}" target="_blank" class="wa-btn">📲 Tap to Send Recipe File & Caption on WhatsApp</a>', unsafe_allow_html=True)
                else:
                    st.info("💡 Enter your WhatsApp Phone Number in the sidebar to send directly to your phone!")

                st.markdown("---")
                st.subheader("📖 Extracted Recipe Text Preview")
                st.text_area("Recipe Content", recipe_text, height=300)

                with open(txt_filepath, "r", encoding="utf-8") as file_data:
                    st.download_button(
                        label=f"💾 Download {os.path.basename(txt_filepath)}",
                        data=file_data.read(),
                        file_name=os.path.basename(txt_filepath),
                        mime="text/plain",
                        type="secondary"
                    )
