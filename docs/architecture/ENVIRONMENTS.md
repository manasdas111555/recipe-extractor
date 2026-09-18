# 🌐 Universal Pro AI — Environments & Deployment Guide

This guide details the **3-Tier Environment Architecture** for Universal Pro AI, the automated safety gates, and instructions for configuring the cloud staging instance.

---

## 🏛️ Environment Topology

| Dimension | 🛠️ Development (Dev) | 🧪 Testing & Staging (Staging) | 🚀 Production (Prod) |
| :--- | :--- | :--- | :--- |
| **Git Branch** | **`Dev`** | **`staging`** | **`main`** *(Protected)* |
| **Hosting Platform** | Local Workstation | Streamlit Cloud (Staging App) | Streamlit Cloud (Primary App) |
| **Access URL** | `http://localhost:8501` | `https://universalpro-stage.streamlit.app/` | `https://universalpro-ai.streamlit.app/` |
| **Primary Goal** | Fast feature development | Pre-production testing & cloud validation | 100% reliable consumer traffic |
| **Data / API Keys** | Local `.env` | Streamlit Cloud Secrets (Staging) | Streamlit Cloud Secrets (Production) |
| **Promotion Gate** | Manual commit | Automated CI + `scripts/verify_promotion.py` | Manual approval after Staging verification |

---

## 🔄 The Promotion Flow

```
[Local Dev Branch]
       │
       ▼ (Run local unit tests & quality gate)
python scripts/verify_promotion.py
       │
       ▼ (Promote Dev -> Staging)
python scripts/promote.py --to staging
       │
       ├─► GitHub Actions runs CI (.github/workflows/ci.yml)
       ├─► Streamlit Cloud auto-deploys to Staging URL
       ▼
[Verify Live Staging URL in Browser]
       │
       ▼ (Certified healthy)
python scripts/promote.py --to main
       │
       └─► Streamlit Cloud updates Production URL with 0 downtime
```

---

## ☁️ How to Set Up the Free Staging App on Streamlit Cloud

1. Log in to [share.streamlit.io](https://share.streamlit.io).
2. Click the **"Create app"** button (top-right).
3. Select:
   - **Repository**: `manasdas111555/recipe-extractor`
   - **Branch**: `staging`
   - **Main file path**: `app.py`
   - **App URL**: `universalpro-stage` (Streamlit disallows the word 'staging', so use 'stage')
4. Click **Advanced settings...** and paste your secrets:
   ```toml
   GEMINI_API_KEY = "..."
   AMAZON_ASSOCIATE_TAG = "manasdas11155-21"
   EARNKARO_USER_ID = "5608766"
   ```
5. Click **Deploy!**

Now, whenever code is pushed or promoted to `staging`, Streamlit Cloud automatically builds and tests your changes in this staging sandbox without touching your production website.

---

## 🛠️ CLI Automation Commands

### 1. Run Pre-Promotion Verification Locally
```powershell
python scripts/verify_promotion.py
```

### 2. Promote Dev to Staging
```powershell
python scripts/promote.py --to staging
```

### 3. Promote Staging to Production
```powershell
python scripts/promote.py --to main
```

---

## 🔐 How to Update Streamlit Cloud Secrets

Whenever you add new API keys, database credentials, or affiliate IDs (such as **Cuelinks**, **Supabase**, or **Gemini**), update your secrets on Streamlit Cloud:

### Method A: From the Live App in Your Browser (Fastest)
1. Open your live app:
   - **Production**: [manas-recipe-extractor.streamlit.app](https://manas-recipe-extractor.streamlit.app/)
   - **Staging**: [universalpro-stage.streamlit.app](https://universalpro-stage.streamlit.app/)
2. At the bottom-right corner of the page, click the **"Manage app"** button.
3. In the dock panel that slides open, click the **three dots menu (`⋮`)** next to your app name, then select **"Settings"**.
4. In the Settings modal, select the **"Secrets"** tab on the left.
5. Add or update your keys in the TOML editor (see template below).
6. Click **"Save"**. The app will automatically restart with the new secrets in ~5 seconds.

### Method B: From the Streamlit Cloud Dashboard
1. Go to [share.streamlit.io](https://share.streamlit.io) and log in.
2. In your list of deployed apps, locate the app card (**`manas-recipe-extractor`** or **`universalpro-stage`**).
3. Click the **three vertical dots (`⋮`)** on the far right of the app row $\rightarrow$ click **"Settings"**.
4. Click the **"Secrets"** tab on the left sidebar.
5. Add or update your keys, then click **"Save"**.

---

### 📋 Secrets Reference Template

#### For Production (`manas-recipe-extractor`):
```toml
GEMINI_API_KEY = "your_gemini_api_key"
AMAZON_AFFILIATE_TAG = "manasdas11155-21"
EARNKARO_ID = "5608766"
CUELINKS_ID = "317820"
MISTRALAI_API_KEY = "your_mistral_api_key"
GROQ_API_KEY = "your_groq_api_key"
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your_supabase_anon_key"
SUPABASE_SERVICE_ROLE_KEY = "your_supabase_service_role_key"
```

#### For Staging (`universalpro-stage`):
Same as above, but with Staging Channel ID:
```toml
CUELINKS_ID = "317821"
```

