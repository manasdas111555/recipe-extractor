# 🌐 Universal Pro AI — Environments & Deployment Guide

This guide details the **3-Tier Environment Architecture** for Universal Pro AI, the automated safety gates, and instructions for configuring the cloud staging instance.

---

## 🏛️ Environment Topology

| Dimension | 🛠️ Development (Dev) | 🧪 Testing & Staging (Staging) | 🚀 Production (Prod) |
| :--- | :--- | :--- | :--- |
| **Git Branch** | **`Dev`** | **`staging`** | **`main`** *(Protected)* |
| **Hosting Platform** | Local Workstation | Streamlit Cloud (Staging App) | Streamlit Cloud (Primary App) |
| **Access URL** | `http://localhost:8501` | `https://manas-recipe-extractor-staging.streamlit.app/` | `https://manas-recipe-extractor.streamlit.app/` |
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
   - **App URL**: `manas-recipe-extractor-staging` (or customized)
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
