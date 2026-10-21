# 📘 Universal Pro AI — Comprehensive User Manual & Feature Guide

Welcome to the **Universal Pro AI** User Manual. This guide explains what features the app provides and how to use them step-by-step.

---

## 📋 Table of Contents

1. [Quick Start & Video Ingestion](#1-quick-start--video-ingestion)
2. [Extraction Card Output & Dual-Language Notes](#2-extraction-card-output--dual-language-notes)
3. [Interactive Hands-Free Cooking Mode](#3-interactive-hands-free-cooking-mode)
4. [Dynamic Recipe Servings Adjuster](#4-dynamic-recipe-servings-adjuster)
5. [10-Minute Quick Commerce & 1-Click Buying](#5-10-minute-quick-commerce--1-click-buying)
6. [Intelligence Vault & Local Library](#6-intelligence-vault--local-library)
7. [WhatsApp & Telegram Integration](#7-whatsapp--telegram-integration)
8. [Governance & Documentation Reference](#8-governance--documentation-reference)
9. [Developer & QA Guide: Release Verification & Testing Framework](#9-developer--qa-guide-release-verification--testing-framework)

---

## 1. Quick Start & Video Ingestion

Universal Pro AI converts social media video links into structured recipe cards, workout routines, product reviews, and educational notes.

### How to Use:
1. **Copy Video URL**: Copy any public link from **YouTube Shorts**, **Instagram Reels**, **TikTok**, or **Facebook Reels**.
2. **Paste Link**: Paste the URL into the main search bar at the top of the app dashboard.
3. **Select Category (Optional)**: Leave on `Auto-Detect (Universal AI)` or pick a specific category:
   - 🍳 *Cooking Recipe & Food*
   - 🛍️ *Kitchen Finds & Home Gadgets*
   - 🏋️ *Fitness & Workout Routine*
   - 💻 *Tech Tutorial & Code Guide*
   - 📦 *Product Unboxing & Amazon Finds*
   - ✈️ *Travel Guide & Itinerary*
4. **Click "Extract Anything"**: The app processes your video link and displays your interactive result card.

---

## 2. Extraction Card Output & Dual-Language Notes

Once extracted, your result card provides the following interactive sections:

- **Docked Media Player**: Watch the source reel or video side-by-side with structured steps.
- **3-Section Recipe View**:
  - **Section I**: Equipment & Cookware Needed.
  - **Section II**: Ingredients with scaled quantities.
  - **Section III**: Step-by-Step Cooking Instructions.
- **Dual-Language Toggle**: Switch between English translation and native spoken language notes.
- **Interactive Travel Maps**: Open interactive directions for featured travel locations on Google Maps.
- **Domain Primary Action Hierarchy**: Render exactly 1 primary call-to-action tailored to the result domain (*"Shop ingredients"* for Recipes, *"Open in Google Maps"* for Travel, *"Buy"* for Products, *"Open resources"* for Tutorials).
- **Accessible Mobile Overflow Bottom Sheet**: On mobile viewports (<768px), secondary actions and utilities (Export Markdown, Export Text, Copy Link, Save to Vault) are cleanly grouped inside a WCAG 2.2 compliant bottom sheet modal (`role="dialog"`, `aria-modal="true"`, focus trapping, `Escape` key close).
- **Vault Re-hydration**: Opening saved items from local storage automatically re-hydrates missing store links via `/api/v1/library/rehydrate` so buy buttons and quick commerce links appear instantly without client-side affiliate tags.

---

## 3. Interactive Hands-Free Cooking Mode

Designed for active cooking in the kitchen without needing to touch mobile screens with messy hands.

### How to Use:
- **Launch Cooking Mode**: Click **"Start Cooking Mode"** on any recipe card or tap a shared cooking mode link from WhatsApp/Telegram.
- **Screen Wake Lock**: Automatically keeps mobile displays awake so your screen doesn't dim or turn off while cooking.
- **High-Contrast Text**: Large typography designed for reading from a distance across the kitchen counter.
- **Step Countdown Timers**: Timed step countdowns with 1-click controls (**Play**, **Pause**, **Reset**) and audio completion chimes.
- **Voice Command Control**: Turn on **Voice Mode** to navigate hands-free:
  - Say `"Next"` or `"Forward"` to advance to the next step.
  - Say `"Back"` or `"Previous"` to return to the previous step.
  - Say `"Start"` or `"Timer"` to start a step timer.
  - Say `"Pause"` or `"Stop"` to pause a timer.
- **Keyboard & Touch Navigation**: Press `→` / `Space` for next step, `←` for previous step, `Esc` to close, or swipe left/right on touchscreens.
- **Ingredients Slide Checklist**: Slide open the ingredients checklist to tick off items as you cook.

---

## 4. Dynamic Recipe Servings Adjuster

Adjust ingredient quantities for different portion sizes.

### How to Use:
- **Adjust Servings**: Click `+` or `-` to scale servings from **1 to 12 people**. Ingredient amounts recalculate automatically.
- **Clean Fraction Display**: Displays kitchen measurements in clean fractions (`½`, `¼`, `¾`, `⅓`, `⅔`).
- **Native Measurement Units**: Preserves traditional unit names and metrics (e.g. `1 katori (~150g)` scaled 2x → `2 katori (~300g)`).
- **Exclude Pantry Staples**: Check "Exclude Pantry Staples" to hide common household items (Salt, Water, Oil) from shopping lists.
- **Copy Ingredients**: Click **"Copy Notes"** to copy the formatted ingredient list to your clipboard.

---

## 5. 10-Minute Quick Commerce & 1-Click Buying

Order missing recipe ingredients or featured products in 1 click.

### How to Use:
- **10-Minute Grocery Delivery (Recipes & Food)**:
  - 🟡 **Blinkit**: Click Blinkit badges to open pre-filled ingredient cart searches for instant delivery.
  - ⚡ **Zepto**: Click Zepto badges for quick-commerce delivery.
  - 🛵 **Swiggy Instamart**: Click Swiggy Instamart badges for instant grocery shopping.
  - 📦 **BigBasket & JioMart**: Click BigBasket badges for bulk grocery ordering.
- **Online Shopping Marketplaces**:
  - 🛒 **Amazon India**: Click Amazon badges to purchase cookware, appliances, or ingredients.
  - ⚡ **Flipkart**: Click Flipkart badges to find kitchen equipment or tech gadgets.

---

## 6. Intelligence Vault & Local Library

Save and organize your extractions across all video categories.

### How to Use:
- **Multi-Category Vault**: Browse saved extractions for **Recipes**, **Travel Guides**, **Workouts**, **Product Finds**, and **Tutorials**.
- **Category Filters & Custom Actions**: Filter saved cards by category or click direct action buttons (*"Open Travel Guide ↗"*, *"Open Workout View ↗"*, *"Open Tutorial ↗"*).
- **Bookmark & Save**: Click **"Save to Vault"** on any card to store it in your browser library for offline access anytime.

---

## 7. WhatsApp & Telegram Integration

### How to Use:
- **WhatsApp Notes**: Click **"WhatsApp Notes"** on any card or enter a mobile phone number to receive formatted notes and shopping links on WhatsApp.
- **Telegram Bot (`@UniversalProAIBot`)**: Forward video links directly to our Telegram bot to receive structured markdown cards and tap **"Start Cooking Mode"** to launch the interactive viewer.

---

## 8. Governance & Documentation Reference

Universal Pro AI maintains continuous synchronization across its six mandatory living architecture documents as enforced by AGENTS.md Section 9:
- `docs/TROUBLESHOOTING.md` — Bug logs, root cause analysis, and resolution verification.
- `docs/po-governance/PRODUCT_OWNER_UX_SHOWCASE.md` — Feature showcases, UX improvements, and sign-off criteria.
- `docs/architecture/DISASTER_RECOVERY.md` — System architecture, capacity metrics, and disaster runbooks.
- `docs/USER_MANUAL.md` — End-to-end user guide and feature workflows.
- `docs/architecture/DECISIONS.md` — Architectural Decision Records (ADRs).
- `docs/architecture/FLOW.md` — Execution flow diagrams and subsystem call hierarchy.

---

## 9. Developer & QA Guide: Release Verification & Testing Framework

*(Sequential Numbering Reconciliation: Formally designated as Section 9 to align with the actual 9-section structure of USER_MANUAL.md; resolves preliminary planning references to Section 19).*

Universal Pro AI implements a strict multi-tier testing framework separating offline sandbox verification from live deployment release gates:

### 1. Local Developer Sandbox (`Dev` Branch)
- **Unit & Component Tests**:
  - Frontend Vitest: `npm test` (executes component and utility unit tests).
  - Backend Pytest: `pytest tests/` (executes all unit, security, and integration test suites).
  - Database Grant Suite: `pytest tests/test_database_grants.py` (verifies table grants, directory parity, RLS, and search paths).
- **Deterministic Mocked Playwright Suite**:
  - `npm run test:e2e:mocked` (runs Playwright against `http://localhost:3000` with network mocks; never contacts external servers or triggers AI inference).
- **Definitive Rule 16 Verification Pipeline**:
  - `python scripts/ci_check.py` (executes the complete 6-step pipeline: `tsc`, `lint`, `vitest`, `build`, `test_database_grants`, `pytest`).

### 1b. Database Schema Migrations & Grant-Readiness Verification (UPA-1406)
- **Canonical Source & Directory Parity**: `backend/database/` is the canonical source of truth for all database migrations. Root `database/` is maintained as a verified 1-to-1 byte mirror.
- **Migration Replay Chain**:
  - `001_initial_schema.sql` $\rightarrow$ `009_beta_telemetry_feed.sql` $\rightarrow$ `010_telemetry_events.sql` $\rightarrow$ `011_privilege_hardening.sql` $\rightarrow$ `012_extraction_public_ownership.sql`.
- **Explicit Least-Privilege Grants**:
  - The Supabase PostgREST Data API requires explicit table-level grants following Supabase's October 30, 2026 automatic grant deprecation.
  - Tables `profiles`, `extractions`, `affiliate_clicks`, `beta_telemetry_feed`, and `telemetry_events` declare explicit grants tailored strictly to application access paths (`service_role` for backend ops, `anon`/`authenticated` for public extraction reads). Client write access is revoked on all internal tables.
- **Automated Verification**:
  - `pytest tests/test_database_grants.py` validates directory parity, explicit table grants, rejection of wildcard grants, function search-path protections, and RLS.
- **Fresh Provisioning vs Existing Database Updates**:
  - *Fresh database*: Apply migrations sequentially from `001` through `012`.
  - *Existing deployed database*: Apply only subsequent unapplied migrations (e.g. `011` and `012`), as `011` idempotently hardens table grants and function search paths on pre-existing tables.

### 1c. Supabase Staging Free-Tier Inactivity Keep-Alive Operations (UPA-1409)
- **Operational Purpose**: Under Supabase platform rules, Free-tier projects are paused after 7 consecutive days of zero database activity. The Staging keep-alive workflow issues periodic, lightweight read-only queries to generate database activity and mitigate inactivity pause risk on Staging project `Universal Pro AI — Staging` (`mzpkdmaxsuhwezsooidu`).
- **Architectural Distinction — Activity Probing vs Disaster Recovery**:
  - Keep-alive activity probing is an operational availability safeguard, **NOT** a backup or disaster recovery mechanism.
  - Probing generates ordinary API/database activity to reduce inactivity pausing risk, but does not guarantee that Supabase will never pause the project under its platform policies.
  - In the event of schema corruption or data loss, refer to canonical migration replay (`docs/architecture/DISASTER_RECOVERY.md` Runbook 26 Step 3) and independent logical backups (`pg_dump`).
  - If the Staging database becomes paused, follow the unpause runbook in `docs/architecture/DISASTER_RECOVERY.md` Runbook 27.
- **Dedicated Staging Probe Script**:
  - `python scripts/staging_supabase_keep_alive.py`
  - Enforces strict target locking to `mzpkdmaxsuhwezsooidu.supabase.co` (fails closed on unexpected hostname or Production URL).
  - Queries `GET /rest/v1/extractions?select=id&limit=1` via PostgREST using the least-privilege `anon` key.
  - Enforces 15-second request timeout; accepts both rows and empty array `[]` as successful database activity; fails closed on HTTP errors.
  - Structured logging emits execution timestamp, environment (`staging`), HTTP status, and duration without ever logging secrets, bearer tokens, or database row contents.
- **Dedicated GitHub Actions Workflow**:
  - File: `.github/workflows/staging_supabase_keep_alive.yml`
  - Schedule: 3 times daily at UTC cron `17 0,8,16 * * *` plus `workflow_dispatch` for manual execution.
  - Permissions: Minimal `contents: read`; bounded 5-minute job timeout.
  - Required Secrets: `SUPABASE_STAGING_URL` and `SUPABASE_STAGING_ANON_KEY`. Must be provisioned in GitHub repository secrets before the workflow can succeed.
- **Platform Invariant on Scheduled Workflows**:
  - Scheduled GitHub Actions workflows (`schedule` trigger) only run automatically from the repository's **default branch** (`main`).
  - The workflow on `Dev` or `staging` branches can be verified manually via `workflow_dispatch` once secrets are provisioned, but automated 8-hour background probing takes effect post-promotion to the default branch.

### 2. Live Staging Release Gates (`staging` Branch)
- **Commit-Bound Manifest & Source-Aware Promotion Preflight**:
  - **Dev → Staging Preflight**: `python scripts/promote.py --to staging --ticket <ticket>` executes preflight verification (`verify_evidence_manifest`) on the source `Dev` evidence manifest using `--env dev`, checking `manifest.commitSha === expectedDevSha` and accepting Dev-appropriate classification (`mocked` or `live`).
  - **Ticket-Scoped Promotion Branches**: Staging promotion strictly mandates a validated ticket identifier via `--ticket <ticket>` (e.g. `python scripts/promote.py --to staging --ticket upa-1401`). Prepares and pushes isolated ticket-scoped branch `promotion/<ticket>-staging` (e.g. `promotion/upa-1401-staging`). Malformed ticket formats are rejected with `ValueError`.
  - **Collision Detection & Fail-Closed Remote Lookup**: Probes both local refs (`git show-ref`) and remote refs (`git ls-remote`). Replaces destructive branch resets with safe `git checkout -b`, halting safely before branch creation or push if a branch already exists. Non-zero `git ls-remote` exit codes (network, authentication, or remote-access errors) raise `RuntimeError` and immediately fail closed, never misclassifying remote lookup failures as proof of branch absence.
  - **Staging Release Acceptance**: Generating release acceptance evidence on Staging requires deploying to Staging and executing the live Staging smoke/E2E suite, producing an `evidence-manifest.json` bound to the deployed Staging revision with `executionClassification: "live"`.
  - **Staging → Production Preflight**: `python scripts/promote.py --to main` executes preflight verification on the source `staging` evidence manifest using `--env staging`, checking `manifest.commitSha === expectedStagingSha` and strictly enforcing `executionClassification: "live"`. Mocked evidence is permitted strictly on Dev and cannot satisfy Staging or Production release gates.
- **Tier 1 — Universal Live Staging Smoke Gate**:
  - `npm run test:e2e:staging:smoke` (mandatory after *every* Staging deployment before Product Owner acceptance).
  - Targets `https://universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app` with `ALLOW_LIVE_STAGING_SMOKE=true` and edge bypass cookies.
  - Monitors HTTP 4xx/5xx errors targeting both frontend origin and backend API origin (`STAGING_API_URL` or fallback `http://129.225.86.241`).
  - Asserts fail-closed navigation response using `validateNavigationResponse`.
  - *Operational Status Note*: Executed on live Staging commit `85fa6e7b7366711ab9c3f9b2a3271ecae86d99d7`; evaluated to `FAIL` because the initial test expected `submitBtn` enabled with an empty input (`disabled={isLoading || !url}` is intentional). Corrected on Dev (`0c107ca`) to test disabled on empty input and enabled when fixture input is supplied without submitting. Live Staging runs require `$env:TEST_ENV = "staging"` so evidence is not mislabeled as `dev`. Staging release gate remains `FAIL` pending fix promotion and live retest.
- **Tier 2 — Conditional Live Extraction E2E Gate**:
  - `npx playwright test --project=staging-live` (mandatory when changes touch media extraction, request routing, or background workers).
  - Runs with `ALLOW_DB_WRITES=false` ensuring zero dirty rows in PostgreSQL.
  - **Cache-Miss & Worker Stage Hardening (`UPA-1405`)**: Strictly rejects viral cache hits (initial HTTP 200 or `is_cached: true` fails closed with `[UPA-1305 VALIDATION BLOCKED]`) to guarantee that media downloader and ingestion stages are genuinely exercised; requires observing intermediate worker progress stages (`downloading_media` or `multimodal_ai_inference`) specifically correlated to the submitted `targetJobId` (terminal `completed` status alone is strictly excluded); sanitizes in-flight URLs in failure diagnostics to prevent secret leakage in logs; test target URL can be configured via `STAGING_TEST_URL`.
- **Evidence Artifact Isolation Framework (`UPA-1403`)**:
  - To prevent clobbering historical evidence manifests or test screenshots during repeated Staging or Dev test runs, pass `EVIDENCE_OUTPUT_DIR=test-results/staging-smoke-<timestamp>` and `DISABLE_SECONDARY_MANIFEST_WRITE=true`.
  - All Playwright attachments, traces, step screenshots, and `evidence-manifest.json` are isolated to that specified directory without mutating `frontend/e2e-evidence/`.
  - Manifest verification via `python scripts/verify_promotion.py --verify-manifest --env staging --expected-sha <sha>` automatically detects `EVIDENCE_OUTPUT_DIR` or `EVIDENCE_MANIFEST_PATH`.
- **Deployed Health Audit**:
  - `python scripts/verify_promotion.py --deployed staging` (verifies deployed Vercel frontend and OCI backend `http://129.225.86.241/health`).

### 3. Production Release & Smoke Gate (`main` Branch)
- Strictly requires prior separate written Product Owner authorization in `docs/po-governance/SIGN_OFF.md`.
- Requires mandatory post-deployment non-destructive live smoke verification against `https://universal-pro-ai.vercel.app`.
- If smoke testing fails, follow bounded rollback procedures in `docs/architecture/DISASTER_RECOVERY.md` (Runbook 25).
