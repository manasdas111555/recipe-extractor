# 🏛️ Universal Pro AI — System Solution & Technical Architecture Baseline

---

## 1. DOCUMENT CONTROL

* **Document Title**: Universal Pro AI — System Solution & Technical Architecture Baseline
* **Project Name**: Universal Pro AI (UPA)
* **Document Purpose**: Establishes an authoritative, evidence-backed technical architecture baseline covering system topology, environment boundaries, security controls, data flows, deployment readiness gates, and living-document governance rules.
* **Author / Source Context**: Prepared by AI Systems Architect following read-only repository and documentation discovery.
* **Date Prepared**: September 23, 2026
* **Architecture Baseline Commit**: `9fa2fa8a8d04e6bbbf4b488021d8dfd725588a51` [VERIFIED IN CURRENT REPOSITORY]
* **Document Status**: Adopted Baseline — Governed Repository Artifact (UPA-1237)
* **Verification Philosophy**: Every technical statement in this document is explicitly categorized using a strict 5-tier evidence model:
  1. `[VERIFIED IN CURRENT REPOSITORY]`: Supported directly by inspected source code or configuration files.
  2. `[VERIFIED IN EXISTING PROJECT DOCUMENTATION]`: Supported by project documentation/runbooks but not verified at live runtime.
  3. `[EXTERNAL PLATFORM / INFRASTRUCTURE VERIFICATION REQUIRED]`: Depends on external cloud infrastructure or live runtime state.
  4. `[PLANNED / INTENDED ARCHITECTURE]`: Target architecture designed but not yet operationalized.
  5. `[UNKNOWN / REQUIRES OWNER CONFIRMATION]`: Insufficient or conflicting evidence.

> [!IMPORTANT]
> **Living Document Rule**: Architecture and operational documentation are living project artifacts. They must remain synchronized with actual governed implementation. (See Section 35).

---

## 2. EXECUTIVE SUMMARY

Universal Pro AI is an asynchronous multimodal media ingestion, extraction, and contextual commerce system designed to transform short-form social video feeds (Instagram Reels, YouTube Shorts, TikTok) into structured, actionable utility payloads (recipes, product guides, travel directions, tech tutorials) [VERIFIED IN CURRENT REPOSITORY].

### System Component Overview
1. **Frontend PWA Layer**: Next.js 15 App Router Progressive Web App hosted on Vercel [VERIFIED IN CURRENT REPOSITORY].
2. **API Gateway Layer**: FastAPI application providing REST API endpoints, JWT token verification, guest quota accounting, and PostgREST client wrappers [VERIFIED IN CURRENT REPOSITORY].
3. **Background Processing Engine**: Celery worker processes backed by Redis for media downloading (via `yt-dlp`), frame extraction, and AI processing [VERIFIED IN CURRENT REPOSITORY].
4. **AI Processing Engine**: Primary Google Gemini Flash multimodal LLM calls with optional multi-LLM consensus fallbacks (Groq Llama 3.3 / Mistral) [VERIFIED IN CURRENT REPOSITORY].
5. **Database & Storage Layer**: PostgreSQL hosted on Supabase with Row Level Security (RLS), custom RPC functions, minimum-privilege grants (Migration 011), and PostgREST querying [VERIFIED IN CURRENT REPOSITORY].

---

## 3. EVIDENCE CLASSIFICATION SYSTEM & GOVERNANCE MODEL

To prevent false claims and enforce rigorous engineering standards, all claims in this document obey the 5-level evidence model:

* `[VERIFIED IN CURRENT REPOSITORY]`: Direct code/config verification.
* `[VERIFIED IN EXISTING PROJECT DOCUMENTATION]`: Documented in `ENVIRONMENTS.md`, `ORACLE_CLOUD_DEPLOYMENT.md`, `DISASTER_RECOVERY.md`, or `JIRA_BACKLOG.md`.
* `[EXTERNAL PLATFORM / INFRASTRUCTURE VERIFICATION REQUIRED]`: Requires cloud console inspection, live curl/TLS check, or deployment validation.
* `[PLANNED / INTENDED ARCHITECTURE]`: Future roadmap items.
* `[UNKNOWN / REQUIRES OWNER CONFIRMATION]`: Items requiring explicit owner sign-off.

---

## 4. MULTI-ENVIRONMENT ARCHITECTURE & DEPLOYMENT TOPOLOGY

The system follows a strict 3-layered environment isolation model:

```
[Layer 1: Development]    --->    [Layer 2: Staging]          --->    [Layer 3: Production]
- Local Sandbox / Git         - Vercel Preview (Frontend)         - Vercel Production
- In-memory / Local Redis     - Dedicated OCI VM (Pending)        - Production OCI VM
- Local Supabase / Dev DB     - Staging Supabase DB               - Production Supabase DB
- Branch: Dev                 - Branch: staging                   - Branch: main
```

### Environment Status Table
| Environment | Frontend Host | Backend Host | Database Host | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Development** | Localhost (3000) | Localhost (8000) | Local / Supabase Dev | `[VERIFIED IN CURRENT REPOSITORY]` |
| **Staging** | Vercel Preview | Dedicated OCI VM (Pending) | Supabase Staging (`mzpkd...`) | `[EXTERNAL PLATFORM / INFRASTRUCTURE VERIFICATION REQUIRED]` |
| **Production** | Vercel Production | OCI Production VM | Supabase Production (`scrq...`) | `[VERIFIED IN EXISTING PROJECT DOCUMENTATION]` |

---

## 5. SOURCE-OF-TRUTH DOCUMENTATION MAP

| Architectural Domain | Primary Source-of-Truth Document |
| :--- | :--- |
| **System Solution & Technical Baseline** | `docs/architecture/SYSTEM_ARCHITECTURE.md` |
| **Environment Topology & Deployment Rules** | `docs/architecture/ENVIRONMENTS.md` |
| **Oracle Cloud Infrastructure (OCI) Runbook** | `docs/architecture/ORACLE_CLOUD_DEPLOYMENT.md` |
| **Disaster Recovery & Operational Runbooks** | `docs/architecture/DISASTER_RECOVERY.md` |
| **Agent Governance & Rules** | `AGENTS.md` |
| **Database Migrations & Schema** | `backend/database/` + migration artifacts |
| **Sprint Backlog & PO Sign-offs** | `docs/po-governance/JIRA_BACKLOG.md` |

---

## 6. FRONTEND PWA ARCHITECTURE (NEXT.JS 15)

* **Framework**: Next.js 15 App Router (`frontend/src/app`) [VERIFIED IN CURRENT REPOSITORY].
* **Styling & Tokens**: Vanilla CSS / Tailwind with design tokens in `globals.css` supporting light & dark themes [VERIFIED IN CURRENT REPOSITORY].
* **State & Hooks**: Custom React hooks (`useStepTimer`, `useWakeLock`, `useRecipeStore`) with mobile in-app browser polyfills/wrappers [VERIFIED IN CURRENT REPOSITORY].
* **PWA Capability**: Web Share Target receiver (`/share-target`) for one-tap ingestion from Instagram/TikTok/YouTube mobile apps [VERIFIED IN CURRENT REPOSITORY].

---

## 7. BACKEND API GATEWAY ARCHITECTURE (FASTAPI)

* **Framework**: FastAPI (`backend/app/main.py`) [VERIFIED IN CURRENT REPOSITORY].
* **Routing Structure**: `/api/v1/extract`, `/api/v1/library`, `/api/v1/affiliate`, `/api/v1/public` [VERIFIED IN CURRENT REPOSITORY].
* **Security & Auth**: JWT verification, `X-Admin-Api-Key` for admin telemetry routes, IP-based / token-based rate limiting [VERIFIED IN CURRENT REPOSITORY].
* **Fallback Execution**: In-memory `BackgroundTasks` fallback when Celery/Redis is unreachable in local dev [VERIFIED IN CURRENT REPOSITORY].

---

## 8. INGESTION, DOWNLOAD & MEDIA PIPELINE

1. **Validation**: Strict URL validation via `backend/app/services/url_validator.py` (HTTPS only, domain allowlist, max 3 redirects, SSRF/IP checks) [VERIFIED IN CURRENT REPOSITORY].
2. **Download Guardrails**: `yt-dlp` capped at 90s max duration and 360p resolution (`bestvideo[height<=360]+bestaudio/best[height<=360]`) [VERIFIED IN CURRENT REPOSITORY].
3. **Temp File Lifecycle**: All temporary files cleaned up in unskippable `finally:` blocks [VERIFIED IN CURRENT REPOSITORY].
4. **Proxy Stream Token**: `/api/v1/extract/stream-video` requires HMAC-signed, short-lived tokens; raw video URLs are never stored in cache [VERIFIED IN CURRENT REPOSITORY].

---

## 9. AI PROCESSING & MULTI-LLM CONSENSUS ENGINE

* **Primary Engine**: Google Gemini Multimodal API (`gemini-1.5-flash` / `gemini-2.0-flash` configured in `Settings`) [VERIFIED IN CURRENT REPOSITORY].
* **Hinglish & Culinary Prompts**: Tuned system prompts preserving native culinary terminology (e.g., *1 katori -> 1 bowl (~150 ml, approx)*, *Jeera*, *Hing*) [VERIFIED IN CURRENT REPOSITORY].
* **Consensus Engine (Opt-In)**: 3-stage consensus pipeline via `llm_council.py` incorporating Groq Llama 3.3 and Mistral APIs as fallbacks [VERIFIED IN CURRENT REPOSITORY].

---

## 10. DATABASE & STORAGE ARCHITECTURE (SUPABASE / POSTGRESQL)

* **Provider**: Supabase PostgreSQL with PostgREST API [VERIFIED IN CURRENT REPOSITORY].
* **Migrations**: Executed sequentially (`01_schema.sql` ... `011_privilege_hardening.sql`) [VERIFIED IN CURRENT REPOSITORY].
* **Privilege Model**: Minimum-privilege ACLs via Migration 011; `ALLOW_DB_WRITES` setting controls write operations [VERIFIED IN CURRENT REPOSITORY].
* **Schema Versioning**: All `structured_data` JSON payloads include `schema_version` for forward compatibility [VERIFIED IN CURRENT REPOSITORY].

---

## 11. MONETIZATION & AFFILIATE ENGINE

* **Affiliate Engine**: `backend/app/services/affiliate_engine.py` generates affiliate-tagged e-commerce links [VERIFIED IN CURRENT REPOSITORY].
* **Immutable Identifiers**: Default tags (`manasdas11155-21` for Amazon IN, `r=5608766` for EarnKaro) are protected constants [VERIFIED IN CURRENT REPOSITORY].
* **URL Encoding**: All merchant search queries are strictly URL-encoded using `urllib.parse.quote_plus` [VERIFIED IN CURRENT REPOSITORY].

---

## 12. BACKGROUND PROCESSING & QUEUE ARCHITECTURE

* **Distributed Mode**: Celery + Upstash Redis for asynchronous task execution [VERIFIED IN CURRENT REPOSITORY].
* **Fallback Mode**: FastAPI `BackgroundTasks` for in-memory execution during local development [VERIFIED IN CURRENT REPOSITORY].
* **Windows Compatibility**: `scripts/run_worker.py` dynamically uses `--pool=solo` or `--pool=threads` on Windows [VERIFIED IN CURRENT REPOSITORY].

---

## 13. SECURITY ARCHITECTURE & THREAT MODEL

1. **SSRF & IP Guardrails**: `url_validator.py` blocks private/loopback/cloud-metadata IP ranges [VERIFIED IN CURRENT REPOSITORY].
2. **Secret Hygiene**: All credentials resolved via Pydantic `Settings`; zero hardcoded fallbacks in production paths [VERIFIED IN CURRENT REPOSITORY].
3. **Signed Stream Tokens**: HMAC-SHA256 tokens protect video streaming endpoints [VERIFIED IN CURRENT REPOSITORY].
4. **Merchant Redirects**: Redirect endpoints validate target host against allowlisted merchant domains [VERIFIED IN CURRENT REPOSITORY].

---

## 14. INFRASTRUCTURE & NETWORK ARCHITECTURE (OCI)

* **Production VM**: Oracle Cloud Infrastructure Ampere A1 (ARM64) instance running Caddy reverse proxy, Docker containers for API and Celery workers [VERIFIED IN EXISTING PROJECT DOCUMENTATION].
* **Staging VM**: Dedicated Staging VM (Pending OCI provisioning) [PLANNED / INTENDED ARCHITECTURE].
* **Egress Firewall**: `deploy/setup_egress_firewall.sh` sets `iptables`/`ip6tables` rules restricting outbound container traffic [VERIFIED IN CURRENT REPOSITORY].

---

## 15. DISASTER RECOVERY & SYSTEM RESILIENCE

* **Backup & Restore**: Supabase automated database backups; docker-compose configuration for fast container restart [VERIFIED IN EXISTING PROJECT DOCUMENTATION].
* **Runbook Reference**: Detailed disaster recovery steps documented in `docs/architecture/DISASTER_RECOVERY.md` [VERIFIED IN EXISTING PROJECT DOCUMENTATION].

---

## 16. CONSOLIDATED MERMAID ARCHITECTURE DIAGRAM

```mermaid
graph TD
    User([User Mobile / Desktop]) -->|HTTPS / PWA| Vercel[Vercel Frontend - Next.js 15]
    User -->|Telegram / WhatsApp| Bots[Bot Webhooks]

    Vercel -->|REST API Requests| Gateway[FastAPI API Gateway]
    Bots -->|Webhook Events| Gateway

    Gateway -->|Auth / JWT| SupabaseAuth[Supabase Auth]
    Gateway -->|Read/Write Data| SupabaseDB[(Supabase PostgreSQL)]

    Gateway -->|Async Job Dispatch| Redis[(Upstash Redis Queue)]
    Gateway -.->|Fallback In-Memory| LocalWorker[Local Background Tasks]

    Redis --> CeleryWorker[Celery Background Workers]
    CeleryWorker -->|Media Download (yt-dlp)| WebMedia[Social Platforms]
    CeleryWorker -->|AI Ingestion| Gemini[Google Gemini API]
    CeleryWorker -.->|Consensus Fallback| LLMCouncil[Groq / Mistral APIs]
    CeleryWorker -->|Save Extraction| SupabaseDB

    Gateway -->|Affiliate Links| AffiliateEngine[Affiliate Engine]
    AffiliateEngine -->|Redirects| ECommerce[Amazon / Flipkart / Blinkit / Zepto]
```

---

## 17. DOCUMENTATION GOVERNANCE — RULE 21

### Rule 21: Documentation Synchronization & Architecture Drift Guard
1. Every governed project change must keep applicable technical documentation synchronized with the implementation.
2. Any architecture, infrastructure, deployment, environment, API, security, database, background-processing, AI, configuration, networking, CI/CD, observability, or data-flow change MUST assess documentation impact.
3. Affected living documents must be updated in the same governed ticket/change.
4. Documentation must describe actual implemented and empirically verified state.
5. Documentation must never falsely claim deployment, capability, configuration, security, or verification.
6. Every governed change must produce an explicit **Documentation Impact Assessment**.
7. Obsolete documentation must be corrected or marked historical/deprecated.
8. Documentation must distinguish the 5 evidence states.
9. Primary goal: Prevent architecture, deployment, environment, infrastructure, and documentation drift.
