# Instagram Reel Recipe Extractor & WhatsApp Bot 🍳

Automated cloud web application that downloads Instagram Reel recipes, uses Gemini 2.5 Flash AI to transcribe the step-by-step recipe, saves a clean `.txt` file with the dish name, and forwards it to WhatsApp.

---

## 🚀 How to Deploy on Streamlit Community Cloud (Free Domain)

### Step 1: Create a Free GitHub Repository
1. Go to [GitHub.com](https://github.com) and click **New Repository**.
2. Name it `recipe-extractor` and set it to **Public**.
3. Upload/push all files from this directory (`app.py`, `config.py`, `downloader.py`, `gemini_processor.py`, `whatsapp_service.py`, `requirements.txt`, `.streamlit/config.toml`).

---

### Step 2: Deploy on Streamlit Cloud (100% Free)
1. Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
2. Click **New App** -> Select your `recipe-extractor` repository.
3. Set **Main file path** to `app.py`.
4. Click **Advanced Settings** / **Secrets** and add your Gemini API Key:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```
5. Click **Deploy!**

---

## 🎉 Your Free Custom Domain URL
Within 60 seconds, your app will be live with your free HTTPS domain URL:
`https://your-recipe-app.streamlit.app`

Bookmark this link on your iPhone, Android, or laptop to extract recipes anytime, anywhere!

---

## 📋 Features

- 🌐 **Instagram Reel HD Video Downloader**
- 🤖 **Gemini 2.5 Flash Multimodal Video AI**
- 📝 **Apt Recipe File Naming** (`Black_Fiery_Smoky_Chili_Chicken.txt`)
- 📲 **1-Click WhatsApp Mobile Delivery** with custom caption:
  `Here is recipe file for - Black Fiery Smoky Chili Chicken !`
- 💾 **Direct `.txt` File Download Button**
