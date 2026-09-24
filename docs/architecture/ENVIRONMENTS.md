# 🌐 Universal Pro AI — Environments & Deployment Guide

This guide details the **3-Tier Environment Architecture** for Universal Pro AI, the automated safety gates, and instructions for configuring the cloud staging instance.

> [!NOTE]
> For the authoritative system-wide architecture baseline and 5-tier evidence model, see [System Architecture Baseline](file:///d:/Personal%20Projects/recipe-extractor/docs/architecture/SYSTEM_ARCHITECTURE.md).

---

## 🏛️ Environment Topology

| Dimension | 🛠️ Development (Dev) | 🧪 Testing & Staging (Staging) | 🚀 Production (Prod) |
| :--- | :--- | :--- | :--- |
| **Git Branch** | **`Dev`** | **`staging`** | **`main`** *(Protected)* |
| **Frontend Host** | Local Workstation (`localhost:3000`) | Vercel Preview | Vercel Production |
| **Backend Host** | Local Workstation (`localhost:8000`) | Dedicated OCI Staging VM (`129.225.86.241`, Provisioned / SSH Verified) | OCI Production VM (`140.245.214.28`) |
| **Access URL** | `http://localhost:3000` | Vercel Preview URL | Production Web PWA |
| **Primary Goal** | Fast feature development | Pre-production testing & cloud validation | 100% reliable consumer traffic |
| **Data / API Keys** | Local `.env` | Environment Variables (Vercel / Staging Host) | Production Environment Variables (Vercel / OCI) |
| **Promotion Gate** | Manual commit | Automated CI + `scripts/verify_promotion.py` | Manual approval after Staging verification |

> [!NOTE]
> **Historical Note `[HISTORICAL / DEPRECATED]`**: Legacy Streamlit Cloud deployments (`universalpro-stage.streamlit.app` and `universalpro-ai.streamlit.app`) served as the v0 prototype and are replaced by the Next.js 15 PWA on Vercel and FastAPI Gateway on OCI.

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
Same as above, but with Staging credentials & channel IDs:
```toml
CUELINKS_ID = "317821"
SUPABASE_URL = "https://your-staging-project.supabase.co"
SUPABASE_ANON_KEY = "your_staging_supabase_anon_key"
SUPABASE_SERVICE_ROLE_KEY = "your_staging_supabase_service_role_key"
SUPABASE_JWKS_URL = "https://your-staging-project.supabase.co/auth/v1/.well-known/jwks.json"
SECRET_KEY = "your_staging_secret_key"
REDIS_URL = "rediss://.../1"
REDIS_KEY_PREFIX = "staging:"
CELERY_DEFAULT_QUEUE = "staging_default_queue"
TELEGRAM_BOT_TOKEN = "your_staging_telegram_bot_token"
WHATSAPP_VERIFY_TOKEN = "your_staging_whatsapp_verify_token"
```

---

## 🔒 UPA-1218: Staging Environment Isolation Protocol & Interim Rules

### 1. Staging Project Separation Blueprint
Staging and Production MUST NOT share database instances, JWT keys, user accounts, or Redis task queues.
- **Dedicated OCI Staging VM**: Dedicated `VM.Standard.E2.1.Micro` instance `universal-pro-ai-staging-instance` (AMD x86_64, Ubuntu 24.04.5 LTS, Public IP `129.225.86.241`, Private IP `10.0.2.242`, Subnet `staging-public-subnet` `10.0.2.0/24`, Security List `staging-security-list-universalpro-ai-vcn`) — **PROVISIONED, OS BOOTSTRAP, 2.0 GiB SWAP & DOCKER 29.8.1/COMPOSE v5.5.1 VERIFIED VIA SSH**. Repository checkout, Application deployment (Caddy / FastAPI), Supabase runtime connectivity, and Redis/Celery **NOT YET DEPLOYED / NOT YET VERIFIED / DEFERRED**.
- **Dedicated Supabase Project**: Separate Supabase project for staging environment (`https://mzpkdmaxsuhwezsooidu.supabase.co`).
- **SQL Migration Sequence (Owner-Executed Manual Steps)**:
  1. `01_schema.sql`: Core PostgreSQL tables (`users`, `profiles`, `extractions`, `affiliate_clicks`).
  2. `02_indexes.sql`: Performance lookup indexes (SHA-256 `url_hash`, `user_id`).
  3. `03_functions.sql`: Atomic RPC functions (`increment_user_extraction_count`).
  4. `04_rls_policies.sql`: Tenant Row-Level Security policies.
  5. `05_views.sql`: Analytics and public recipe views.
  *(Manual Steps: Owner creates staging project in Supabase UI $\rightarrow$ opens SQL Editor $\rightarrow$ runs scripts 01 through 05 in sequence $\rightarrow$ verifies schema).*
- **Per-Environment Redis & Queue Isolation (Finding & Proposal)**:
  - **Finding**: Currently, staging and production share `REDIS_URL` and default Celery task queue `celery` if unisolated, creating risks of staging workers pulling production tasks.
  - **Proposal**: 
    - Database Index: Production uses Redis DB 0 (`/0`), Staging uses Redis DB 1 (`/1`).
    - Key Prefix: Production `prod:`, Staging `staging:`.
    - Celery Queue: Production `prod_default_queue`, Staging `staging_default_queue`.
- **JWKS Endpoint Verification**:
  - Verify Staging JWKS via HTTP GET `{STAGING_SUPABASE_URL}/auth/v1/.well-known/jwks.json` returns 200 with valid ES256 key set.

### 2. Interim Rules (Enforced Until UPA-1218 is Complete)
- **Zero Agent Schema Mutations**: The agent NEVER applies a schema migration, table modification, or data deletion directly to database instances. SQL files may be drafted, but ONLY the owner applies them after taking a database backup. All migrations MUST be additive and backward compatible (e.g. `UPA-1215` `is_public` column nullable or defaulted `false`, zero destructive backfill).
- **Production Row Protection & Table Inventory**: Tests and QA execution on staging MUST NOT modify or delete existing production rows. For every feature change, list which tables are read or written:
  - `profiles`: READ (plan_tier, quota), WRITE (custom affiliate tags, daily count).
  - `extractions`: READ (SHA-256 cache hit), WRITE (new reel extractions).
  - `affiliate_clicks`: WRITE (monetization telemetry clicks).
- **Separate Credentials**: Independent `SECRET_KEY`, webhook secrets (`TELEGRAM_WEBHOOK_SECRET`, `WHATSAPP_VERIFY_TOKEN`, `RAZORPAY_WEBHOOK_SECRET`, `STRIPE_WEBHOOK_SECRET`), and Telegram bot token per environment.

