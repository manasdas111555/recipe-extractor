# 🛡️ Universal Pro AI — System Architecture & Disaster Recovery (DR) Manual

**Product**: Universal Reel & Shorts AI Extractor (Universal Pro AI)  
**Document Type**: Living Disaster Recovery (DR) Plan & Technical Specification  
**Current Milestone**: Sprints 11–14 Completed (Safety, Cooking Mode, Scaling Engine & Commerce Integration)  
**Recovery Time Objective (RTO)**: $\le 5\text{ minutes}$ (Site restored)  
**Recovery Point Objective (RPO)**: $\le 1\text{ hour}$ (Data loss minimal to zero)  
**Last Updated**: September 18, 2026  

> [!NOTE]
> For the authoritative system-wide architecture baseline and Rule 21 documentation synchronization rules, see [System Architecture Baseline](file:///d:/Personal%20Projects/recipe-extractor/docs/architecture/SYSTEM_ARCHITECTURE.md).

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
| **Production Frontend (Primary)** | Vercel Edge Network | `https://universal-pro-ai.vercel.app` | Next.js 15 PWA web client, global CDN, HTTPS termination & origin IP shield |
| **Production Node (Dedicated)** | Oracle Cloud (OCI Hyderabad) | `140.245.214.28` (Ports 80, 443, 8000) | Always-on 24/7 Docker stack (FastAPI, Celery, Redis, Caddy) |
| **Production UI (Legacy Prototype)** | Streamlit Community Cloud `[HISTORICAL / DEPRECATED]` | [https://manas-recipe-extractor.streamlit.app/](https://manas-recipe-extractor.streamlit.app/) | v0 prototype extraction web app (Legacy) |
| **Staging UI (Legacy Prototype)** | Streamlit Community Cloud `[HISTORICAL / DEPRECATED]` | [https://universalpro-stage.streamlit.app/](https://universalpro-stage.streamlit.app/) | Legacy testing sandbox |
| **FastAPI Backend** | Local / Docker Daemon | `http://localhost:8000` (`/docs`, `/health`, `/api/v1/auth/me`) | Decoupled API Gateway for bots and PWAs |
| **Database** | Supabase (AWS Mumbai) | `https://scrqvbgjybnrvcpxbygf.supabase.co` | Multi-tenant PostgreSQL database with RLS |
| **Global Skills Root** | Local Agent Environment | `C:\Users\admin\.gemini\config\skills\` | 14 global agent skills (`frontend-design`, `theme-factory`, `shadcn`, `high-end-visual-design`, etc.) |
| **Visual Asset CDN** | Next.js Static Public (`public/`) | `hero_glass_artwork.jpg`, `hero_neural_bg.jpg` | 3D glass crystal artwork and ambient aurora background layers |

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
- **Primary Path**: Direct video upload to Google Gemini Cloud via Files API (`gemini-3.8-flash` flagship model).
- **Resilient Fallback Tier**: Sequential failover across active Flash models (`gemini-3.7-flash`, `gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`). Proactively pruned deprecated 404 endpoints (`gemini-3.1-pro`, `gemini-3-flash`, `gemini-2.5-*`) to prevent latency spikes per **AGENTS.md Rule 8**.
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
- **Asynchronous Extraction Router (`backend/app/api/v1/extract.py`)**:
  - `POST /api/v1/extract`: Validates URL, enforces daily quota (HTTP 429 when exceeded), computes SHA-256 `url_hash`, checks PostgreSQL cache (HTTP 200), and enqueues background worker jobs (HTTP 202).
  - `GET /api/v1/extract/status/{job_id}`: Real-time polling endpoint tracking progress percentage, stage lifecycle (`enqueued`, `downloading_media`, `multimodal_ai_inference`, `completed`, `failed`), and output payload.
- **Job Manager (`backend/app/services/job_manager.py`)**: Thread-safe in-memory job registry and background execution pipeline with automatic Supabase persistence.

### 4b. Mandatory Security Environment Variables & Network Egress Firewall Rules
- **Required Security Environment Variables & Secret Hygiene**:
  - `SECRET_KEY`: Mandatory HMAC signing secret for minting short-lived `/stream-video` tokens. Constant fallbacks removed; required at startup in non-dev/production environments.
  - `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`: Mandatory data layer settings. Non-dev environments refuse startup if missing, logging variable names only.
  - `SUPABASE_JWKS_URL`: Derived automatically as `{SUPABASE_URL}/auth/v1/.well-known/jwks.json` per project.
  - `ADMIN_API_KEY`: Secret token for accessing admin metrics and system telemetry (`X-Admin-Api-Key`).
  - `TELEGRAM_BOT_TOKEN` & `TELEGRAM_WEBHOOK_SECRET`: Standardized bot credentials per environment.
  - `WHATSAPP_VERIFY_TOKEN` & `WHATSAPP_ACCESS_TOKEN`: Standardized Meta WhatsApp Cloud API credentials.
  - `RAZORPAY_KEY_SECRET` & `STRIPE_WEBHOOK_SECRET`: Feature-gated payment secrets (return HTTP 503 if feature endpoint called without key).
  - `TRUSTED_PROXY`: Default `False` (ignores spoofed proxy headers); set `True` in production behind Vercel edge proxies.
  - `TRUSTED_PROXY_HOPS`: Number of trusted proxy hops counted from right edge of `X-Forwarded-For` (default `1`).
  - `CORS_ORIGINS`: Explicit allowed origin list (defaults empty, no `*` wildcard in production).
- **Telegram Webhook Secret Token Registration**:
  ```bash
  curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
    -d "url=https://universal-pro-ai.vercel.app/api/v1/webhooks/telegram" \
    -d "secret_token=${TELEGRAM_WEBHOOK_SECRET}"
  ```
- **Worker & API Container Egress Firewall Rules**:
  - Outbound traffic restricted to verified required service ports: **Port 443** (HTTPS for Gemini/Groq/Mistral AI, Supabase REST, Telegram/WhatsApp APIs, e-commerce hosts), **Port 6379/33816** (Celery + Upstash Redis broker), and **Port 5432/6543** (Supabase Direct PostgreSQL).
  - Hard egress drop rules applied on container network bridge (`iptables` / Docker network driver) blocking cloud metadata IP `169.254.169.254` and RFC1918 private ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.0/8`).
  - *Verification Distinction*: Backend unit tests (`tests/test_backend_security_hardening.py`) validate the application `url_validator` logic, while `scripts/verify_egress.py` (or `scripts/verify_egress.sh`) verifies the active container network firewall.
- **UPA-1218 Staging Isolation & Interim DB Rules**:
  - Separate Supabase project (`https://<staging_id>.supabase.co`) with manual owner execution of `backend/database/*.sql` (`01_schema.sql` through `05_views.sql`).
  - Separate Redis DB index (DB 1 vs DB 0), key prefix (`staging:` vs `prod:`), and Celery queue (`staging_default_queue` vs `prod_default_queue`).
  - Interim Rule: Zero agent schema mutations or data deletions. SQL files written by agent are applied ONLY by owner after DB backup; all changes must be additive and backward compatible (`UPA-1215` `is_public` nullable/defaulted).
  - Staging QA tests MUST NOT modify or delete production rows. Table inventory tracked for every change (`profiles`, `extractions`, `affiliate_clicks`).


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

### 📘 Runbook 6: Oracle Cloud Compute Node Failure & Reprovisioning
**Symptom**: The primary production server (`140.245.214.28`) becomes unresponsive via SSH or HTTP.

#### Step 1: Check Instance State in OCI Console
1. Log into [cloud.oracle.com](https://cloud.oracle.com/).
2. Navigate to **Compute** $\rightarrow$ **Instances** $\rightarrow$ select `universal-pro-ai-instance`.
3. If instance is stopped: click **Start**.
4. If instance is frozen: click **More actions** $\rightarrow$ **Reboot**.

#### Step 2: Container Recovery (1 Minute)
If server OS is healthy but web API is down:
```bash
ssh -i "path/to/ssh-key.key" ubuntu@140.245.214.28
cd recipe-extractor
docker compose restart
docker compose ps
```

#### Step 3: Complete Node Reprovisioning (Under 5 Minutes)
If the virtual machine was completely corrupted or terminated:
1. Follow [`ORACLE_CLOUD_DEPLOYMENT.md`](ORACLE_CLOUD_DEPLOYMENT.md) to launch a new `Canonical Ubuntu 24.04` instance in `universalpro-ai-vcn`.
2. Connect to the new IP and run the one-time server bootstrap:
   ```bash
   sudo apt update && sudo apt upgrade -y
   curl -fsSL https://get.docker.com | sudo sh
   sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile
   git clone https://github.com/manasdas111555/recipe-extractor.git
   cd recipe-extractor && nano .env && docker compose up -d --build
   ```
3. Update DNS / frontend backend proxy to the new IP. (RTO: $\le 5$ minutes).

---

### 📘 Runbook 7: Streamlit Cloud Sleep / Hibernation Failover
**Symptom**: Streamlit app displays `"Zzzz This app has gone to sleep due to inactivity"`.

#### Step 1: Immediate Manual Wakeup
1. Click the button on screen: **"Yes, get this app back up"**.
2. Or trigger the keep-alive workflow manually from GitHub:
   - Go to `https://github.com/manasdas111555/recipe-extractor/actions/workflows/keep_alive.yml`.
   - Click **Run workflow** $\rightarrow$ select branch `main` $\rightarrow$ click **Run workflow**.

#### Step 2: Permanent Fix
Point users and mobile PWAs to the dedicated Oracle Cloud production node (`http://140.245.214.28`) or the global Vercel Edge frontend (`https://universal-pro-ai.vercel.app`), which have zero hibernation timeouts.

---

### 📘 Runbook 8: Vercel Edge Frontend Failover & Redeployment
**Symptom**: Vercel frontend displays build errors or backend connection drops.

#### Step 1: Trigger Instant Redeployment in Vercel
1. Log into [vercel.com](https://vercel.com/dashboard).
2. Open project `universal-pro-ai`.
3. Go to **Deployments** $\rightarrow$ Click the `...` menu on the latest deployment $\rightarrow$ Click **Redeploy**.
4. (Optional: Check "Redeploy with existing build cache" off to force a clean build).

#### Step 2: Verify or Update Environment Variables
1. Go to **Project Settings** $\rightarrow$ **Environment Variables**.
2. Verify `NEXT_PUBLIC_API_URL` points to `http://140.245.214.28`.
3. If the Oracle Cloud IP ever changes, update this variable and click **Redeploy**.

---

### 📘 Runbook 9: YouTube Cloud IP Ingestion Failover & oEmbed Fallback
**Symptom**: Cloud ingestion returns `403 Forbidden` or `GVS PO Token required` when attempting YouTube Shorts downloads on serverless/datacenter IPs.

#### Step 1: Automatic oEmbed Multimodal Fallback
1. `download_youtube_fallback()` automatically triggers upon `yt-dlp` stream extraction failure.
2. The worker queries YouTube's official oEmbed endpoint (`https://www.youtube.com/oembed?url=...`).
3. High-resolution stream thumbnails (`maxresdefault.jpg` ➔ `sddefault.jpg` ➔ `hqdefault.jpg`) are downloaded to `/tmp/recipe_downloads/yt_stream_{video_id}.jpg` and sent directly to Gemini Multimodal Vision API for zero-downtime inference.

#### Step 2: Proxy Rotation Check (Optional)
1. If oEmbed thumbnail retrieval is ever throttled, verify `USE_PROXIES=true` and `RESIDENTIAL_PROXY_URL` in `.env`.
2. Residential proxy rotator will round-robin requests through clean ISP IP pools.

---

### 📘 Runbook 10: Vercel Preview Staging Protection Bypass
**Symptom**: Staging QA testing crawlers or browser agents hit `401 Unauthorized` on client-side JS chunks.

#### Step 1: Execute Bypass Parameter Protocol
1. Append Option A query parameters to all Vercel Preview URLs:
   ```text
   ?x-vercel-protection-bypass=<secret>&x-vercel-set-bypass-cookie=samesitenone
   ```
2. Vercel Edge issues the `_vercel_jwt` session cookie, unblocking all downstream script, asset, and API fetch requests.

---

### 📘 Runbook 11: Global Skills Directory & Frontend Visual Asset Recovery
**Symptom**: Agent skills are missing, or Next.js background textures (`hero_glass_artwork.jpg`, `hero_neural_bg.jpg`) fail to load.

#### Step 1: Global Skills Directory Restoration
If skills are lost or uninstalled:
1. Re-run global installer:
   ```powershell
   python scratch/install_skills.py
   ```
2. Or copy skill directories directly into `C:\Users\admin\.gemini\config\skills\<skill_name>\SKILL.md`.

#### Step 2: Static Visual Asset Recovery
If static assets in `frontend/public/` are missing:
1. Re-copy images from source scratch files:
   ```powershell
   copy "hero_neural_bg.jpg" "frontend\public\"
   copy "hero_ambient_glow.jpg" "frontend\public\"
   copy "hero_glass_artwork.jpg" "frontend\public\"
   ```
2. Run `npm run build` inside `frontend/` to re-generate the static CDN bundle.

---

### 📘 Runbook 12: Dual-Theme State Recovery & LocalStorage Reset
**Symptom**: User interface theme is locked or displays inconsistent colors between light/dark mode.

#### Step 1: Clear LocalStorage Theme Cache
1. Open Browser DevTools (F12) $\rightarrow$ Application $\rightarrow$ Local Storage.
2. Delete key `theme` or execute in browser console:
   ```js
   localStorage.removeItem('theme');
   document.documentElement.classList.remove('dark');
   ```
3. Refresh page. App resets cleanly to default Light Mode (`#F8FAFC`).

---

### 📘 Runbook 13: World-Class Dual-Theme Palette & Ceramic Token Restoration
**Symptom**: Theme CSS variables or card glassmorphism styles are missing or overridden.

#### Step 1: Ceramic & Obsidian Token Audit
Verify `frontend/src/app/globals.css` contains the mandatory `:root` and `html.dark` design tokens:
```css
:root {
  --bg-base: #F8FAFC;
  --bg-surface: rgba(255, 255, 255, 0.82);
  --shadow-card: 0 20px 40px -15px rgba(15, 23, 42, 0.06);
}
html.dark {
  --bg-base: #040711;
  --bg-surface: rgba(14, 20, 36, 0.78);
  --shadow-card: 0 20px 45px -10px rgba(0, 0, 0, 0.6);
}
```

#### Step 2: Rebuild Static Asset CSS Bundle
Run `npm run build` inside `frontend/` to generate optimized Tailwind & global CSS chunks.

---

### 📘 Runbook 14: Global Agent Skills Directory Restoration & Synchronization (`github.com/anthropics/skills`)
**Symptom**: Agent skills in `C:\Users\admin\.gemini\config\skills\` are corrupted, missing, or require synchronization with upstream repositories.

#### Step 1: Re-clone Anthropic Skills Repository
Execute in terminal:
```powershell
git clone https://github.com/anthropics/skills.git scratch/anthropics_skills
```

#### Step 2: Re-run Global Sync Automation
Run the python sync script to restore all 19 Anthropic skills (`academy-guide`, `algorithmic-art`, `brand-guidelines`, `canvas-design`, `claude-api`, `discernment-nudge`, `doc-coauthoring`, `docx`, `frontend-design`, `internal-comms`, `mcp-builder`, `pdf`, `pptx`, `skill-creator`, `slack-gif-creator`, `theme-factory`, `web-artifacts-builder`, `webapp-testing`, `xlsx`):
```powershell
python -c "
import os, shutil
src = r'scratch\anthropics_skills\skills'
dst = r'C:\Users\admin\.gemini\config\skills'
for s in os.listdir(src):
    s_path = os.path.join(src, s)
    if os.path.isdir(s_path):
        d_path = os.path.join(dst, s)
        if os.path.exists(d_path): shutil.rmtree(d_path)
        shutil.copytree(s_path, d_path)
print('Skills restored successfully!')
"
```

---

### 📘 Runbook 15: Automated WebApp Playwright Visual & E2E Testing Protocol (`webapp-testing` Skill)
**Symptom**: Need to perform automated visual regression testing or E2E UI verification across desktop and mobile viewports.

#### Step 1: Run Automated Playwright WebApp Test Script
Execute in terminal:
```powershell
python scratch/test_webapp_playwright.py
```

#### Step 2: Review Generated Visual Artifacts
Check the following output screenshot files in the brain artifact directory:
- `webapp_test_initial_light_mode.png` (Desktop 1440x900 Light Mode)
- `webapp_test_dark_mode.png` (Desktop 1440x900 Dark Mode)
---

### 📘 Runbook 16: Multi-LLM Council Provider Outage & Failover Recovery Protocol
**Symptom**: One or more council provider APIs (Gemini, Groq, or Mistral) experience a 503 capacity outage or rate limit HTTP 429 during Stage 1 parallel extraction.

#### Step 1: Automatic Single-Provider Graceful Fallback
- `LLMCouncilEngine` in [`backend/app/services/llm_council.py`](file:///d:/Personal%20Projects/recipe-extractor/backend/app/services/llm_council.py) automatically catches provider-level exceptions during Stage 1 `ThreadPoolExecutor` execution.
- If at least 1 provider succeeds, extraction proceeds seamlessly without failing the user request.
- The `parsed_json["council_meta"]` metadata object logs `mode: "single_provider_fallback"`.

#### Step 2: Emergency Router Direct Mode (If all fallback models hang)
If a major AI provider outage occurs:
1. Open Streamlit UI sidebar (or update API payload).
2. Switch **AI Reasoning Engine** from `"LLM Council"` to `"Auto-Universal (Gemini with Multi-Model Fallback)"` or direct `"Groq (Whisper-v3 + Llama 3.3 70B)"`.

---

### 📘 Runbook 17: Light Mode Contrast Audit & Visual Theme Recovery Protocol
**Symptom**: User interface text or step numbers appear washed out or unreadable in Light Mode on mobile viewports or standard displays.

#### Step 1: Verify Theme CSS Color Token Variables
Check [`frontend/src/app/globals.css`](file:///d:/Personal%20Projects/recipe-extractor/frontend/src/app/globals.css) to ensure Light & Dark Mode contrast tokens satisfy WCAG AA standards:
- Dark Mode Muted Text: `#94A3B8` (Slate-400, >7.2:1 AA contrast ratio against `#040711`)
- Light Mode Emerald Badge Text: `#047857` (Emerald-700, >5.1:1 AA contrast ratio)
- Headline Primary Text: `#0F172A` (Slate-900)
- Subheading & Body Copy: `#334155` (Slate-700)
- Active Filter Pills: `#10B981` (Solid Emerald) with `#FFFFFF` text.

#### Step 2: Verify Feathered Radial Mask on Background Textures
Ensure `.bg-glass-artwork` includes the radial gradient mask image:
```css
mask-image: radial-gradient(circle at center, rgba(0,0,0,1) 20%, rgba(0,0,0,0) 75%);
-webkit-mask-image: radial-gradient(circle at center, rgba(0,0,0,1) 20%, rgba(0,0,0,0) 75%);
```

#### Step 3: Verify Ghost-Card Surface Separation & Reduced Motion Engine
Ensure `.glass-panel` uses clean elevation shadows (`0 4px 16px rgba(...)`) without heavy dual border+shadow blur (`≥16px`), and verify `@media (prefers-reduced-motion: reduce)` disables animations and transforms.

#### Step 4: Verify Audit Persistence System
Ensure past and future UI/UX audit reports are stored in the [`ui-ux-audits/`](file:///d:/Personal%20Projects/recipe-extractor/ui-ux-audits) repository directory.

---

### 📘 Runbook 18: Beta Telemetry Feed & Real-Time Alert Recovery Protocol
**Symptom**: Beta user telemetry events fail to log to Supabase DB or Telegram admin notification channel is silent.

#### Step 1: Verify Supabase `beta_telemetry_feed` RLS & Table Schema
1. Connect to Supabase SQL Editor.
2. Execute table verification query:
   ```sql
   SELECT count(*) FROM public.beta_telemetry_feed;
   ```
3. If table is missing, re-apply [`database/009_beta_telemetry_feed.sql`](file:///d:/Personal%20Projects/recipe-extractor/database/009_beta_telemetry_feed.sql).

#### Step 2: Test Telemetry Service Exception Grace
Verify `send_admin_telemetry_alert()` in [`backend/app/services/telemetry_service.py`](file:///d:/Personal%20Projects/recipe-extractor/backend/app/services/telemetry_service.py) catches network timeouts and HTTP errors without interrupting main user extraction workflows.

---

### 📘 Runbook 19: Mobile Bot & Quick-Commerce Affiliate Failover Protocol
**Symptom**: Telegram or WhatsApp bot webhooks return 500 error or quick-commerce delivery links fail to format.

#### Step 1: Verify Bot Polling & Webhook Processes
1. Check Celery / Bot script status on production host:
   ```powershell
   python scripts/run_telegram_bot.py
   ```
2. Verify `TELEGRAM_BOT_TOKEN` and `WHATSAPP_API_TOKEN` in environment settings.

#### Step 2: Quick-Commerce Link Formatting Verification
Verify `whatsapp_service.py` formats Blinkit (`https://blinkit.com/s/?q=...`) and Zepto (`https://www.zeptonow.com/search?query=...`) search URLs with explicit `urllib.parse.quote_plus` encoding.

---

### 📘 Runbook 20: Multi-User Concurrency, Performance & Daily Processing Capacity Protocol (Sprint 10)
**Symptom**: Need to evaluate multi-user load performance, API SLAs, or compute daily processing caps for cloud scaling.

#### Step 1: Multi-User Concurrency Architecture
- **Stateless Web & Worker Layer**: FastAPI backend (`backend/app/main.py`) runs asynchronous non-blocking event loops with worker threads for I/O tasks (`BackgroundTasks` or Celery + Upstash Redis).
- **SHA-256 URL Hash Cache Index**: When multiple users submit the exact same Instagram Reel or YouTube Short URL, the worker queries Supabase SHA-256 URL hash index (`database/001_initial_schema.sql`). Identical URLs return instant cached results in **<150ms** with zero redundant video downloads or AI inference calls.
- **Per-IP & User Daily Quotas**: Enforced via `backend/app/services/quota_service.py` to prevent single-user denial-of-service or bot scraping spam.

#### Step 2: Performance SLAs & Benchmark Targets
- **First-Paint Video Preview SLA**: <1.5 seconds.
- **Multimodal AI Extraction Turnaround SLA**: <3.0 seconds (using Gemini Flash stream parsing and pre-flight duration caps).
- **Download Media Footprint**: Max 360p resolution (~3MB to 8MB per video file), immediately deleted in `finally:` block after frame extraction.

#### Step 3: Daily Processing Capacity Calculation Matrix
- **Free Tier Capacity Cap**: **1,500 reels/day** (governed by Google Gemini 1,500 RPD free tier ceiling).
- **Single Node Cloud Instance (4 CPU / 8GB RAM)**: **~20,000 reels/day** (assuming ~3s average worker execution across 4 parallel process threads).
- **Distributed Scale Tier (Celery + Redis + Gemini Pro/Flash API Paid Tier)**: **100,000+ reels/day** (linearly scalable by attaching worker container instances).

---

### 📘 Runbook 21: Dynamic Travel Itinerary Day-by-Day Activity & Google Maps Link Recovery Protocol
**Symptom**: Travel reels do not extract into day-by-day activities or Google Maps search links are broken.

#### Step 1: Verify Gemini Prompt Instruction Contract
- Check `gemini_processor.py` prompt instructions for `TRAVEL_GUIDE` category. Ensure prompt enforces `Day 1:` -> `- Activity 1: <Description> | LOCATION: <Place> | SEARCH: <Query>` structure.

#### Step 2: Verify Parser & Google Maps URL Encoding
- Check `parse_extracted_content` in `gemini_processor.py` and `parseTravelItinerary` helper in `frontend/src/app/page.tsx`.
- All location query strings passed to Google Maps URLs MUST be wrapped in `urllib.parse.quote_plus` / `encodeURIComponent` (`https://www.google.com/maps/search/?api=1&query={encoded_query}`).

#### Step 3: Execute Unit Verification
- Run `python -m pytest tests/test_sprint10_travel_formatting.py` to verify day extraction and activity link parsing (**169 / 169 PASSED**).

---

### 📘 Runbook 22: Universal Intelligence Vault Multi-Genre Recovery Protocol
**Symptom**: Items in Vault display default recipe badges or hardcoded labels for non-recipe extractions (Travel, Workout, Product Finds, Tutorials).

#### Step 1: Category Field Schema Verification
- Ensure extractions saved to `localStorage` (`upa_vault_items`) or Supabase `extractions` table include valid `category` strings (`TRAVEL_GUIDE`, `WORKOUT`, `PRODUCT_FINDS`, `TUTORIAL`, `RECIPE`).
- Verify `VaultLibrary.tsx` invokes `getCategoryBadge(item.category)` and `metaText` fallback logic.

#### Step 2: Automated Test Suite Verification
- Run `pytest tests/` to confirm 100% pass rate across category classification and vault item parsing (**191 / 191 PASSED**).

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
| `YOUTUBE_COOKIES_BASE64` | Base64-encoded Netscape `cookies.txt` string for YouTube auth | Exported from browser via *Get cookies.txt locally* extension |

---

## 📋 Living Maintenance Protocol

Whenever a new infrastructure component, database table, or third-party service is introduced (e.g. Celery workers in Sprint 2, WhatsApp webhook in Sprint 3, Razorpay in Sprint 5):
1. **Add the component to the System Inventory table**.
2. **Document the disaster recovery procedure in a new Runbook** (`Runbook 6`, `Runbook 7`, etc.).
3. **Commit the updated manual to version control** on `Dev` and promote through `staging`.
