# 📋 Jira Agile Project Board — Universal Pro AI (UPA)

**Project Key**: `UPA`  
**Current Phase**: Phase 5 — SaaS Transformation & Scalability  
**Methodology**: Agile Scrum (6 Sprints × 2 Weeks)  
**Board Status**: 🟢 Active  
**Last Updated**: September 2026  

---

## 📊 Sprint Overview & Release Train

| Sprint | Goal / Theme | Story Points | Status | Target Timeline |
| :--- | :--- | :--- | :--- | :--- |
| **Sprint 1** | **Core Decoupling & Multi-Tenant Data Layer** (Supabase + FastAPI) | 26 pts | 🚀 **READY TO START** | Weeks 1–2 |
| **Sprint 2** | **Async Worker Pipeline & Scraper Resilience** (Celery + Redis + Proxies) | 34 pts | ⏳ Backlog | Weeks 3–4 |
| **Sprint 3** | **Zero-Friction Chat Ingestion Bot** (Telegram & WhatsApp Cloud API) | 29 pts | ⏳ Backlog | Weeks 5–6 |
| **Sprint 4** | **Next.js 15 PWA & Personal Vault** (Web Share Sheet + UI Dashboard) | 37 pts | ⏳ Backlog | Weeks 7–8 |
| **Sprint 5** | **Monetization, Quotas & Subscriptions** (Razorpay AutoPay + Stripe) | 26 pts | ⏳ Backlog | Weeks 9–10 |
| **Sprint 6** | **Creator Program & SEO Ingestion Engine** (Custom Tags + SSR Pages) | 21 pts | ⏳ Backlog | Weeks 11–12 |

---

## 📌 Sprint 1 Kanban Board (Current Sprint)

| 📝 To Do | 🔨 In Progress | 🧪 Testing / Review | ✅ Done |
| :--- | :--- | :--- | :--- |
| `UPA-101` Supabase Schema Migration<br>`UPA-102` RLS Security Policies<br>`UPA-103` URL Hash Cache Indexing<br>`UPA-104` FastAPI Directory Skeleton<br>`UPA-105` Supabase Auth & JWT Middleware<br>`UPA-106` `/v1/extract` Job Enqueue Endpoint<br>`UPA-107` `/status/{job_id}` Polling Endpoint | None | None | `UPA-001` Streamlit Prototype & Live Deployment<br>`UPA-002` Multi-Store Affiliate Links Engine<br>`UPA-003` 30-Test Automated Test Suite |

---

## 🎯 Epics Breakdown

```
[EPIC 1: Data Layer] ──> [EPIC 2: API Gateway] ──> [EPIC 3: Worker Queue]
                                                         │
                                                         ▼
[EPIC 6: Next.js PWA] <── [EPIC 5: Mobile Bots] <── [EPIC 4: Commerce Engine]
        │
        ▼
[EPIC 7: Monetization & Quotas]
```

* **EPIC-1 (`UPA-E1`)**: Multi-Tenant Data Layer & Database Architecture (Supabase / PostgreSQL)
* **EPIC-2 (`UPA-E2`)**: Decoupled Asynchronous API Gateway (FastAPI)
* **EPIC-3 (`UPA-E3`)**: High-Concurrency Async Media Worker & Extraction Pipeline (Celery + Redis)
* **EPIC-4 (`UPA-E4`)**: Contextual Multi-Store Commerce & Quick-Delivery Router
* **EPIC-5 (`UPA-E5`)**: Zero-Friction Mobile Chat Ingestion (Telegram & WhatsApp Cloud Webhooks)
* **EPIC-6 (`UPA-E6`)**: Modern Client Frontend & PWA (Next.js 15 App Router)
* **EPIC-7 (`UPA-E7`)**: Billing, Daily Quotas & Subscription Infrastructure (Razorpay + Stripe)

---

## 📝 User Stories Backlog

### 🏢 EPIC-1: Multi-Tenant Data Layer & Database Architecture (Supabase / PostgreSQL)

#### `UPA-101`: Provision Managed PostgreSQL Schema on Supabase
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a systems engineer, I want a structured PostgreSQL database with tables for profiles, extractions, and affiliate clicks, so that user state and extraction results are permanently stored.*
- **Acceptance Criteria**:
  - [ ] Tables created: `profiles`, `extractions`, `affiliate_clicks`.
  - [ ] `uuid-ossp` extension activated for default UUID generation.
  - [ ] Foreign keys established with `ON DELETE CASCADE` or `SET NULL` as appropriate.
  - [ ] Verification script successfully inserts and reads sample mock extraction.
- **Dependencies**: None.

#### `UPA-102`: Implement Row Level Security (RLS) Policies
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 3 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a user, I want my saved extractions and profile to be private, so that other users cannot read or tamper with my data.*
- **Acceptance Criteria**:
  - [ ] RLS enabled on `profiles` and `extractions`.
  - [ ] Policy added: Users can view and update only their own profile (`auth.uid() = id`).
  - [ ] Policy added: Users can read and insert only their own extractions (`auth.uid() = user_id`).
  - [ ] Unauthorized cross-user reads return zero records.
- **Dependencies**: `UPA-101`.

#### `UPA-103`: SHA-256 URL Hash Indexing for Instant Extraction Cache
- **Type**: Story | **Priority**: P1 (High) | **Points**: 3 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a platform operator, I want incoming URLs to be hashed and indexed, so that duplicate requests for viral reels return instantly from cache without re-running costly AI models.*
- **Acceptance Criteria**:
  - [ ] Column `url_hash` indexed with standard B-Tree index on `public.extractions`.
  - [ ] If `url_hash` exists with `status = 'completed'`, worker returns cached JSON immediately (<200ms response).
  - [ ] Cloud AI and proxy costs avoided on cached extractions.
- **Dependencies**: `UPA-101`.

---

### ⚡ EPIC-2: Decoupled Asynchronous API Gateway (FastAPI)

#### `UPA-104`: Scaffold FastAPI Modular Backend Skeleton
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 3 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a backend developer, I want a clean FastAPI directory structure, so that API routes, services, workers, and core configuration are logically separated.*
- **Acceptance Criteria**:
  - [ ] Directory layout created under `backend/app/` (`api/v1/`, `core/`, `workers/`, `services/`).
  - [ ] `main.py` boots cleanly with CORS middleware and OpenAPI docs enabled (`/docs`).
  - [ ] Environment settings managed via `pydantic-settings`.
- **Dependencies**: None.

#### `UPA-105`: Supabase Auth & JWT Verification Middleware
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a client app, I want to authenticate against FastAPI using Supabase JWT Bearer tokens, so that all protected endpoints identify the active user securely.*
- **Acceptance Criteria**:
  - [ ] `get_current_user` dependency validates Supabase JWT against Supabase secret.
  - [ ] Inactive or expired tokens return HTTP 401 Unauthorized.
  - [ ] Anonymous guest mode supported with fallback temporary guest UUID.
- **Dependencies**: `UPA-104`.

#### `UPA-106`: Job Enqueue Endpoint (`POST /v1/extract`)
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a client, I want to submit a social video URL and receive a `job_id` within 300ms, so that my app never freezes during 20-second video processing.*
- **Acceptance Criteria**:
  - [ ] Endpoint validates URL via `pydantic.HttpUrl`.
  - [ ] Checks and decrements daily quota for free-tier users.
  - [ ] Computes `url_hash` and enqueues task to Celery queue.
  - [ ] Returns HTTP 202 Accepted with `job_id`, `status: "queued"`.
- **Dependencies**: `UPA-104`, `UPA-105`.

#### `UPA-107`: Task Polling & Progress Endpoint (`GET /v1/extract/status/{job_id}`)
- **Type**: Story | **Priority**: P1 (High) | **Points**: 2 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a client frontend, I want to poll job progress stages, so that I can show dynamic status indicators (downloading, AI scanning, complete) to the user.*
- **Acceptance Criteria**:
  - [ ] Queries Celery `AsyncResult` state (`PENDING`, `PROCESSING`, `SUCCESS`, `FAILURE`).
  - [ ] Returns current stage metadata (e.g. `downloading_media`, `multimodal_ai_inference`).
  - [ ] When completed, returns full structured JSON payload.
- **Dependencies**: `UPA-106`.

---

### ⚙️ EPIC-3: High-Concurrency Async Media Worker & Extraction Pipeline (Celery + Redis)

#### `UPA-201`: Configure Upstash Redis & Celery Worker Container
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a DevOps engineer, I want Celery configured with Upstash Redis, so that background workers can process jobs asynchronously across cloud instances.*
- **Acceptance Criteria**:
  - [ ] Celery app initialized with Redis broker and result backend.
  - [ ] Hard task execution timeout set to 180 seconds.
  - [ ] Worker processes tasks and tracks execution start state.
- **Dependencies**: `UPA-104`.

#### `UPA-202`: Worker Media Downloader with 360p Limit & Disk Cleanup
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a worker process, I want to download video streams using 360p resolution limits and auto-cleanup temporary files, so that server disk space is never exhausted.*
- **Acceptance Criteria**:
  - [ ] `yt-dlp` configured with `bestvideo[height<=360]+bestaudio/best[height<=360]`.
  - [ ] Maximum download size capped at 50 MB.
  - [ ] Downloaded file deleted in `finally:` block regardless of task success or failure.
- **Dependencies**: `UPA-201`.

#### `UPA-203`: Residential Proxy Rotation Middleware for `yt-dlp`
- **Type**: Story | **Priority**: P1 (High) | **Points**: 5 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a scraping worker, I want outbound downloads routed through rotating residential proxies, so that Instagram and TikTok never trigger HTTP 429 rate limit blocks.*
- **Acceptance Criteria**:
  - [ ] `RESIDENTIAL_PROXY_URL` injected into `ydl_opts['proxy']`.
  - [ ] Automatic retry logic if proxy drops connection.
  - [ ] Local fallback mode maintained for local development (`.env` toggle).
- **Dependencies**: `UPA-202`.

#### `UPA-204`: Port Multimodal AI Processor with Whisper/Keyframe Fallback
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 8 pts | **Status**: `[ ] TO DO`
- **User Story**: *As an extraction engine, I want to analyze videos via Gemini 2.5 Flash, and automatically fall back to Whisper audio transcription + Vision keyframes if direct video upload fails.*
- **Acceptance Criteria**:
  - [ ] Primary path: Direct Gemini 2.5 Flash video upload via Files API.
  - [ ] Fallback path: Keyframe extraction + Groq/Whisper transcription if video upload is unsupported.
  - [ ] Strict JSON schema enforced across all domains (`recipe`, `product_gadget`, `tech_diy`, `fitness_workout`, `travel_guide`).
- **Dependencies**: `UPA-202`.

#### `UPA-205`: Save Extraction Results to Supabase Database
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 3 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a worker, I want completed extraction JSON saved to Supabase, so that user libraries and public cache remain synchronized.*
- **Acceptance Criteria**:
  - [ ] Successful extraction updates row in `extractions` table (`status = 'completed'`).
  - [ ] User's `extractions_today` counter incremented via atomic RPC function.
  - [ ] Error messages captured and logged on task failure (`status = 'failed'`).
- **Dependencies**: `UPA-101`, `UPA-204`.

---

### 🛒 EPIC-4: Contextual Multi-Store Commerce & Quick-Delivery Router

#### `UPA-301`: Affiliate Link Generator Engine
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a business owner, I want every extracted item converted into monetized Amazon and EarnKaro links, so that the platform earns affiliate revenue.*
- **Acceptance Criteria**:
  - [ ] Amazon links formatted with tag `manasdas11155-21`.
  - [ ] Flipkart and Meesho links wrapped through EarnKaro redirect with ID `5608766`.
  - [ ] Pro and Creator tier users can override default tags with their own custom affiliate credentials.
- **Dependencies**: `UPA-101`.

#### `UPA-302`: 10-Minute Quick-Commerce Cart Deep Search
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 3 pts | **Status**: `[ ] TO DO`
- **User Story**: *As an Indian user extracting a recipe, I want 1-click search buttons for Blinkit, Zepto, and Swiggy Instamart, so that I can order missing ingredients in 10 minutes.*
- **Acceptance Criteria**:
  - [ ] Deep search URLs generated for Blinkit, Zepto, and Instamart with URL-encoded item names.
  - [ ] Unit tested against special characters, spices, and brand names.
- **Dependencies**: None.

#### `UPA-303`: Click-Through Analytics Logging
- **Type**: Story | **Priority**: P1 (High) | **Points**: 3 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a business analyst, I want outbound merchant clicks recorded in `affiliate_clicks`, so that I can track conversion rate and EPC (Earnings Per Click).*
- **Acceptance Criteria**:
  - [ ] `/v1/redirect/{click_id}` redirects to merchant while inserting event into `affiliate_clicks`.
  - [ ] Captures `merchant`, `target_url`, `user_id`, and `extraction_id`.
- **Dependencies**: `UPA-101`, `UPA-301`.

---

### 💬 EPIC-5: Zero-Friction Mobile Chat Ingestion (Telegram & WhatsApp)

#### `UPA-401`: Telegram Ingestion Bot MVP (Instant Launch)
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a mobile user, I want to forward a reel to a Telegram bot and get my recipe notes within 15 seconds, so that I don't have to open a browser.*
- **Acceptance Criteria**:
  - [ ] Telegram Bot initialized using `python-telegram-bot` or FastAPI webhook.
  - [ ] Listens for Instagram, TikTok, and YouTube URLs.
  - [ ] Dispatches extraction job to Celery worker.
  - [ ] Sends back structured message with interactive inline buttons (`🛒 Buy Ingredients`, `📝 View Steps`).
- **Dependencies**: `UPA-106`, `UPA-204`.

#### `UPA-402`: WhatsApp Cloud API Webhook Integration
- **Type**: Story | **Priority**: P1 (High) | **Points**: 8 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a mainstream user, I want to share reels directly to a WhatsApp business contact, so that I get structured summaries natively in my chat.*
- **Acceptance Criteria**:
  - [ ] Webhook verification handshake implemented (`hub.mode`, `hub.verify_token`).
  - [ ] Incoming messages acknowledged with HTTP 200 within 2 seconds.
  - [ ] Background worker sends reply payload via Meta Graph API v19.0.
- **Dependencies**: `UPA-106`, `UPA-204`.

---

### 🌐 EPIC-6: Modern Client Frontend & PWA (Next.js 15)

#### `UPA-501`: Next.js 15 App Router Project Skeleton & Theme
- **Type**: Story | **Priority**: P1 (High) | **Points**: 5 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a user, I want a blazing fast, dark-mode luxury web app, so that the extraction interface feels premium and state-of-the-art.*
- **Acceptance Criteria**:
  - [ ] Next.js 15 initialized with TypeScript, Tailwind CSS, and Lucide icons.
  - [ ] Consistent dark theme matching current Universal Pro AI palette (`#0A0E1A`, `#FF416C`).
  - [ ] Responsive layout on mobile and desktop viewports.
- **Dependencies**: None.

#### `UPA-502`: Native PWA Manifest & Web Share Target
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a mobile user, I want Universal Pro AI in my phone's "Share via..." menu, so that sharing a reel from Instagram opens the extractor automatically.*
- **Acceptance Criteria**:
  - [ ] `manifest.json` configured with `share_target` pointing to `/share-target`.
  - [ ] `/share-target/page.tsx` parses incoming URL and triggers extraction immediately.
  - [ ] PWA installable on iOS (Safari Add to Home Screen) and Android (Chrome Install).
- **Dependencies**: `UPA-501`.

#### `UPA-503`: "My Vault / Library" Persistent User Dashboard
- **Type**: Story | **Priority**: P1 (High) | **Points**: 5 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a registered user, I want a searchable library of all my past extractions, so that I never lose recipes, itineraries, or workout routines.*
- **Acceptance Criteria**:
  - [ ] Grid and list views of past extractions with category badges.
  - [ ] Full-text search over titles, ingredients, and steps.
  - [ ] Export buttons for Notion, Markdown, and Plain Text.
- **Dependencies**: `UPA-102`, `UPA-501`.

---

### 💳 EPIC-7: Billing, Daily Quotas & Subscription Infrastructure

#### `UPA-601`: Redis-Backed Daily Quota Middleware
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 3 pts | **Status**: `[ ] TO DO`
- **User Story**: *As a SaaS operator, I want free users limited to 3 extractions per day, so that API inference costs remain protected.*
- **Acceptance Criteria**:
  - [ ] Redis key `quota:{user_id}:{YYYY-MM-DD}` tracks daily usage.
  - [ ] Key auto-expires after 24 hours.
  - [ ] 4th extraction attempt by free user returns HTTP 429 with upgrade CTA.
  - [ ] Pro and Business tiers bypass quota limits.
- **Dependencies**: `UPA-201`.

#### `UPA-602`: Razorpay Subscription Webhook & UPI AutoPay (India)
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[ ] TO DO`
- **User Story**: *As an Indian user, I want to upgrade to Pro (₹299/month) using UPI AutoPay, so that I enjoy unlimited extractions seamlessly.*
- **Acceptance Criteria**:
  - [ ] Razorpay checkout modal created for plan `plan_pro_299_inr`.
  - [ ] Webhook listener handles `subscription.activated` and upgrades user tier in Supabase.
  - [ ] Webhook verifies HMAC-SHA256 signature against `RAZORPAY_WEBHOOK_SECRET`.
  - [ ] Handles `subscription.halted` / payment failure by safely downgrading to free tier.
- **Dependencies**: `UPA-101`, `UPA-104`.

#### `UPA-603`: Stripe Billing Integration (Global Users)
- **Type**: Story | **Priority**: P1 (High) | **Points**: 5 pts | **Status**: `[ ] TO DO`
- **User Story**: *As an international user, I want to subscribe at $4.99/month via Credit Card or Apple Pay, so that I can use the tool globally.*
- **Acceptance Criteria**:
  - [ ] Stripe Customer Portal and Checkout Session configured.
  - [ ] Stripe webhook listener handles `customer.subscription.created` and `deleted`.
- **Dependencies**: `UPA-101`, `UPA-104`.

---

## 📈 Issue Status Legend
- `[ ] TO DO`: In backlog, not started.
- `[/] IN PROGRESS`: Actively under development on `Dev` branch.
- `[T] TESTING`: Code written, automated unit tests and manual verification running.
- `[x] DONE`: Verified, committed, and merged.

---

## 🛠️ Definition of Done (DoD) Checklist
For any user story to transition to **`[x] DONE`**:
1. Code written following PEP 8 / TypeScript conventions.
2. Unit tests implemented and passing with 100% assertion coverage.
3. Relevant error scenarios documented in [TROUBLESHOOTING.md](file:///d:/Personal%20Projects/recipe-extractor/TROUBLESHOOTING.md) if encountered.
4. Git commit tagged with issue key (e.g. `feat(api): add /v1/extract endpoint [UPA-106]`).
5. Live or staging verification completed.
