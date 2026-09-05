# 🛡️ Universal Pro AI — System Architecture & Disaster Recovery (DR) Manual

**Product**: Universal Reel & Shorts AI Extractor (Universal Pro AI)  
**Document Type**: Living Disaster Recovery (DR) Plan & Technical Specification  
**Current Milestone**: Sprint 1 (Day 6 of 90-Day Roadmap)  
**Recovery Time Objective (RTO)**: $\le 5\text{ minutes}$ (Site restored)  
**Recovery Point Objective (RPO)**: $\le 1\text{ hour}$ (Data loss minimal to zero)  
**Last Updated**: September 2026  

---

## 🧭 Executive Summary

This document details:
1. **What has been developed** to date and how each component operates.
2. **Where every piece of data, code, and secret lives**.
3. **Emergency Runbooks** providing step-by-step instructions to recover from catastrophic events (server crashes, database drops, laptop loss, API key compromises, or scraping bans).

---

## 🏛️ System Inventory & Component Blueprint

```
                                    ┌────────────────────────────────────────────────────────┐
                                    │                     GIT REPOSITORY                     │
                                    │      https://github.com/manasdas111555/recipe-extractor │
                                    └──────────────┬───────────────────┬─────────────────────┘
                                                   │                   │
                     ┌─────────────────────────────┘                   └──────────────────────────────┐
                     ▼                                                                                ▼
     ┌───────────────────────────────┐                                                ┌───────────────────────────────┐
     │      STAGING ENVIRONMENT      │                                                │     PRODUCTION ENVIRONMENT    │
     │  Branch: `staging`            │                                                │  Branch: `main` (Protected)   │
     │  App: universalpro-stage       │                                                │  App: manas-recipe-extractor  │
     │  URL: .streamlit.app          │                                                │  URL: .streamlit.app          │
     └───────────────┬───────────────┘                                                └───────────────┬───────────────┘
                     │                                                                                │
                     └─────────────────────────────┬──────────────────────────────────────────────────┘
                                                   ▼
                                    ┌────────────────────────────────────────────────────────┐
                                    │                 DATA & PERSISTENCE LAYER               │
                                    │  Supabase Managed PostgreSQL 15+ (Project: scrqvbgjy...) │
                                    │  • profiles (Users, Quotas, Custom Affiliate Tags)     │
                                    │  • extractions (Payloads, SHA-256 URL Cache)           │
                                    │  • affiliate_clicks (Monetization Telemetry)          │
                                    │  • Row Level Security (RLS) & Atomic RPC Quotas        │
                                    └────────────────────────────────────────────────────────┘
```

### 1. Active Infrastructure & Endpoints

| Component | Platform / Host | Access URL / Identifier | Purpose |
| :--- | :--- | :--- | :--- |
| **Production UI** | Streamlit Community Cloud | [https://manas-recipe-extractor.streamlit.app/](https://manas-recipe-extractor.streamlit.app/) | Customer-facing extraction web app |
| **Staging UI** | Streamlit Community Cloud | [https://universalpro-stage.streamlit.app/](https://universalpro-stage.streamlit.app/) | Pre-production testing sandbox |
| **FastAPI Backend** | Local / Docker Daemon | `http://localhost:8000` (`/docs`, `/health`, `/api/v1/auth/me`) | Decoupled API Gateway for bots and PWAs |
| **Database** | Supabase (AWS Mumbai) | `https://scrqvbgjybnrvcpxbygf.supabase.co` | Multi-tenant PostgreSQL database with RLS |
| **CI/CD Quality Gate**| GitHub Actions | Repository Actions Workflow (`ci.yml`) | Automated Python 3.10/3.11 test runner (45 tests) |

---

## 🛠️ What We Developed & How It Works

### 1. Presentation & Streamlit Runtime (`app.py`, `ui_components.py`)
- **Dynamic Platform Detection**: Identifies Instagram Reels, YouTube Shorts, and TikTok URLs on input paste.
- **Neural Scanner Perception Engine**: Displays dynamic progress states during AI processing to prevent perceived lag.
- **Multi-Store Affiliate Delivery Shelf**: 
  - Direct 1-click buy buttons for **Main 4 Brands**: Amazon, Flipkart, Myntra, Meesho.
  - Dropdown menu for extended marketplace lookups (Nykaa, Tata CLiQ, AJIO).
  - Quick-Commerce grocery delivery bar for **Blinkit, Zepto, and Swiggy Instamart**.
- **Dynamic Module Reloader (`_safe_load_module`)**: Resolves Streamlit Cloud stale cache `ImportError` bugs upon hot reload.

### 2. Multimodal Extraction Engine (`gemini_processor.py`, `downloader.py`)
- **Primary Path**: Direct video upload to Google Gemini 2.5 Flash via Files API.
- **Resilient Fallback Path**: If video direct upload fails or exceeds limits, extracts audio to Groq Whisper transcription and feeds video keyframes to Gemini Multimodal Vision.
- **Resolution Limiting**: `downloader.py` forces `360p` max resolution to save server memory, disk bandwidth, and prevent memory exhaustion.

### 3. Database Layer (`database/001_initial_schema.sql`)
- **`public.profiles`**: Tracks plan tier (`free`, `pro`, `business`), user quotas (3 free/day), and custom affiliate tags.
- **`public.extractions`**: Stores JSON schemas with a **B-Tree index on `url_hash` (SHA-256)** for instant zero-cost cache hits on viral reels.
- **Row Level Security (RLS)**: Enforces tenant isolation so users can only access their own records.
- **Database Trigger (`handle_new_user`)**: Auto-creates a profile record on user signup.
- **Atomic RPC Function (`increment_user_extraction_count`)**: Thread-safe daily quota counter.

### 4. Decoupled Backend Gateway (`backend/app/`)
- **FastAPI Core (`backend/app/main.py`)**: Boots with CORS, `/docs`, and `/health` system monitor.
- **Configuration Loader (`backend/app/core/config.py`)**: Uses Pydantic Settings with automatic `.env` discovery.
- **Supabase REST Client (`backend/app/core/supabase_client.py`)**: Direct HTTP client communicating with Supabase PostgreSQL without heavy SDKs.
- **Security Middleware (`backend/app/core/security.py`)**: Validates Supabase JWT Bearer tokens and provisions guest access sessions (`is_anonymous: True`, 3 free extractions).

### 5. Multi-Environment & CI/CD Pipeline (`scripts/`, `.github/`)
- **`scripts/verify_promotion.py`**: Executes syntax validation, isolated clean-process module imports, and the 45-test unit suite.
- **`scripts/promote.py`**: Enforces automated promotion gates:
  - `python scripts/promote.py --to staging` (Dev $\rightarrow$ Staging)
  - `python scripts/promote.py --to main` (Staging $\rightarrow$ Production)
- **`.github/workflows/ci.yml`**: GitHub Actions runs on every push and PR to `Dev`, `staging`, and `main`.

---

## 🚨 Emergency Disaster Recovery Runbooks

---

### 📘 Runbook 1: Production Website Down or Displaying Error
**Symptom**: `manas-recipe-extractor.streamlit.app` shows a red error banner or `Oh no. An error occurred`.

#### Step 1: Check Live Logs (30 Seconds)
1. Open [share.streamlit.io](https://share.streamlit.io) in your browser.
2. Click on the `manas-recipe-extractor` app.
3. Click the **"Manage app"** tab at the bottom-right and open **Logs**.
4. Identify the last traceback exception.

#### Step 2: Instant Cloud Reboot (60 Seconds)
1. In the bottom-right menu of the Streamlit dashboard, click the three dots `...`.
2. Click **"Reboot app"**.
3. If it is a stale module cache error (like `ISSUE-007`), the reboot clears Python's memory cache and boots clean.

#### Step 3: Emergency Rollback to Last Known Good Commit (2 Minutes)
If a bad commit reached `main`, rollback immediately:
```powershell
# On your local terminal:
git checkout main
git pull origin main
git revert HEAD --no-edit
git push origin main
```
*Streamlit Cloud will automatically rebuild from the reverted commit within 60 seconds.*

---

### 📘 Runbook 2: Accidental Database Table Drop / Supabase Corrupted
**Symptom**: API calls return HTTP 404 or `relation "public.extractions" does not exist`.

#### Step 1: Re-apply the Initial Schema Migration (60 Seconds)
1. Log in to [supabase.com/dashboard](https://supabase.com/dashboard).
2. Select your `universal-pro-ai` project.
3. Click **SQL Editor** (`>_`) in the left sidebar.
4. Open the file [database/001_initial_schema.sql](file:///d:/Personal%20Projects/recipe-extractor/database/001_initial_schema.sql) in your editor, copy all text, and paste into Supabase.
5. Click **Run**.
6. All 3 tables (`profiles`, `extractions`, `affiliate_clicks`), RLS policies, RPC functions, and triggers are recreated with `IF NOT EXISTS` safety.

#### Step 2: Verify Restoration
Run the connection check from terminal:
```powershell
python -c "import os, requests, dotenv; dotenv.load_dotenv(); url = os.getenv('SUPABASE_URL'); key = os.getenv('SUPABASE_ANON_KEY'); print(requests.get(f'{url}/rest/v1/profiles?select=*', headers={'apikey': key, 'Authorization': f'Bearer {key}'}).status_code)"
```
*Expected output: `200`.*

---

### 📘 Runbook 3: Developer Laptop Loss / Hard Drive Wipe
**Symptom**: Complete loss of your local machine. You need to set up the entire project on a new laptop from scratch.

#### Step 1: Clone the Repository (60 Seconds)
```powershell
git clone -b Dev https://github.com/manasdas111555/recipe-extractor.git
cd recipe-extractor
```

#### Step 2: Install Python & Dependencies (2 Minutes)
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

#### Step 3: Recreate Local `.env` (1 Minute)
Create a new file named `.env` and paste your backed-up secrets:
```env
GEMINI_API_KEY=your_gemini_key
AMAZON_AFFILIATE_TAG=manasdas11155-21
EARNKARO_ID=5608766
SUPABASE_URL=https://scrqvbgjybnrvcpxbygf.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

#### Step 4: Verify 100% System Health (30 Seconds)
```powershell
python scripts/verify_promotion.py
```
*Expected output: `ALL CHECKS PASSED! Codebase is certified safe.` (45 unit tests passing).*

---

### 📘 Runbook 4: Social Media Platform Scraper Rate Limit (HTTP 429)
**Symptom**: Reel downloads fail with `HTTP Error 429: Too Many Requests` from Instagram or YouTube.

#### Step 1: Upgrade `yt-dlp` to Latest Release
Social platforms frequently change internal APIs. Updating `yt-dlp` fixes 90% of scraper issues:
```powershell
pip install --upgrade yt-dlp
```

#### Step 2: Activate Residential Proxy Fallback
In `.env`, provide a rotating residential proxy URL:
```env
RESIDENTIAL_PROXY_URL=http://user:pass@proxy-gateway.com:8080
```
`downloader.py` will automatically route outgoing requests through the proxy pool.

---

### 📘 Runbook 5: API Key Compromise or Security Leak
**Symptom**: An API key was accidentally leaked or revoked.

#### Step 1: Rotate the Compromised Key at the Provider
- **Gemini Key**: Generate a new key in [Google AI Studio](https://aistudio.google.com/). Delete the compromised key.
- **Supabase Service Role Key**: In Supabase Dashboard $\rightarrow$ **Settings** $\rightarrow$ **API Keys** $\rightarrow$ Click **Generate new secret**.

#### Step 2: Update Local Environment
Update the key in your local `.env` file.

#### Step 3: Update Cloud Secrets (Streamlit Cloud)
1. Go to [share.streamlit.io](https://share.streamlit.io).
2. For both `manas-recipe-extractor` (Prod) and `universalpro-stage` (Staging):
   - Click **Settings** $\rightarrow$ **Secrets**.
   - Update the key and click **Save**.
   - Streamlit Cloud hot-reloads the new key instantly without downtime.

---

## 🔐 Secrets & Credentials Disaster Reference

> [!CAUTION]
> **Never commit `.env` to Git.** Store a copy of these keys in an encrypted password manager (1Password, Bitwarden, or Apple Keychain).

| Variable Name | Description | Where to Retrieve If Lost |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Powers primary multimodal video analysis | [Google AI Studio](https://aistudio.google.com/) |
| `SUPABASE_URL` | Endpoint for PostgreSQL database | [Supabase Dashboard](https://supabase.com/dashboard) $\rightarrow$ Settings $\rightarrow$ Data API |
| `SUPABASE_ANON_KEY` | Public client token for reading public extractions | Supabase Dashboard $\rightarrow$ Settings $\rightarrow$ API Keys |
| `SUPABASE_SERVICE_ROLE_KEY` | Master secret key for backend workers & quota updates | Supabase Dashboard $\rightarrow$ Settings $\rightarrow$ API Keys |
| `AMAZON_AFFILIATE_TAG` | Amazon Associates tag (`manasdas11155-21`) | [Amazon Associates Central](https://affiliate-program.amazon.in/) |
| `EARNKARO_ID` | EarnKaro publisher identifier (`5608766`) | [EarnKaro Dashboard](https://earnkaro.com/) |
| `GROQ_API_KEY` | Powers Whisper audio fallback transcription | [Groq Console](https://console.groq.com/) |
| `MISTRALAI_API_KEY` | Secondary text structuring fallback | [Mistral AI Console](https://console.mistral.ai/) |

---

## 📋 Living Maintenance Protocol

Whenever a new infrastructure component, database table, or third-party service is introduced (e.g. Celery workers in Sprint 2, WhatsApp webhook in Sprint 3, Razorpay in Sprint 5):
1. **Add the component to the System Inventory table**.
2. **Document the disaster recovery procedure in a new Runbook** (`Runbook 6`, `Runbook 7`, etc.).
3. **Commit the updated manual to version control** on `Dev` and promote through `staging`.
