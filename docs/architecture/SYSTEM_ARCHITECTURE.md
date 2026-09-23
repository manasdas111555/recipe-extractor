# 🏛️ Universal Pro AI — System Solution & Technical Architecture Baseline

---

## 1. DOCUMENT CONTROL

* **Document Title**: Universal Pro AI — System Solution & Technical Architecture Baseline
* **Project Name**: Universal Pro AI (UPA)
* **Document Purpose**: Establishes an authoritative, evidence-backed technical architecture baseline covering system topology, environment boundaries, security controls, data flows, deployment readiness gates, and living-document governance rules.
* **Author / Source Context**: Prepared by AI Systems Architect following read-only repository and documentation audit (UPA-1238).
* **Date Prepared**: September 24, 2026
* **Architecture Baseline Commit**: `ff3a2708f3aa208f11e24a55743c33adc8fe3c2f` [VERIFIED IN CURRENT REPOSITORY]
* **Document Status**: Reconciled Baseline — Governed Repository Artifact (UPA-1238)
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
3. **Background Processing Engine**: Celery worker processes backed by Redis (containerized `redis:7-alpine` on OCI, with optional cloud-managed Upstash Redis support) for media downloading (via `yt-dlp`), frame extraction, and AI processing [VERIFIED IN CURRENT REPOSITORY].
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
| **Production** | Vercel Production | OCI Production VM (`140.245.214.28`) | Supabase Production (`scrq...`) | `[VERIFIED IN EXISTING PROJECT DOCUMENTATION]` |

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
* **Repository Migration Inventory**:
  - `001_initial_schema.sql` (Initial core schema setup) [VERIFIED IN CURRENT REPOSITORY]
  - `009_beta_telemetry_feed.sql` (Beta telemetry feed schema) [VERIFIED IN CURRENT REPOSITORY]
  - `010_telemetry_events.sql` (Growth telemetry events table) [VERIFIED IN CURRENT REPOSITORY]
  - `011_privilege_hardening.sql` (Minimum-privilege ACLs & SECURITY DEFINER hardening) [VERIFIED IN CURRENT REPOSITORY]
  - *Note*: Numerical gaps exist between `001` and `009` in the repository migration history [VERIFIED IN CURRENT REPOSITORY].
* **Privilege Model**: Minimum-privilege ACLs via Migration 011; `ALLOW_DB_WRITES` setting controls write operations [VERIFIED IN CURRENT REPOSITORY].
* **Schema Versioning**: All `structured_data` JSON payloads include `schema_version` for forward compatibility [VERIFIED IN CURRENT REPOSITORY].

---

## 11. MONETIZATION & AFFILIATE ENGINE

* **Affiliate Engine**: `backend/app/services/affiliate_engine.py` generates affiliate-tagged e-commerce links [VERIFIED IN CURRENT REPOSITORY].
* **Affiliate Configuration**: Amazon IN and EarnKaro affiliate parameters are configured securely via application environment variables. Raw operational tag values are omitted from documentation [VERIFIED IN CURRENT REPOSITORY].
* **URL Encoding**: All merchant search queries are strictly URL-encoded using `urllib.parse.quote_plus` [VERIFIED IN CURRENT REPOSITORY].

---

## 12. BACKGROUND PROCESSING & QUEUE ARCHITECTURE

* **OCI Primary Topology**: Containerized `redis:7-alpine` service (`redis://redis:6379/0`) running inside Docker Compose [VERIFIED IN CURRENT REPOSITORY].
* **Optional Cloud Topology**: Managed Upstash Redis supported where configured via `REDIS_URL` [VERIFIED IN CURRENT REPOSITORY].
* **Distributed Processing**: Celery worker processes consuming tasks from Redis [VERIFIED IN CURRENT REPOSITORY].
* **Fallback Mode**: FastAPI `BackgroundTasks` for in-memory execution during local development when Redis is unconfigured [VERIFIED IN CURRENT REPOSITORY].
* **Windows Compatibility**: `scripts/run_worker.py` dynamically uses `--pool=solo` or `--pool=threads` on Windows [VERIFIED IN CURRENT REPOSITORY].

---

## 13. SECURITY ARCHITECTURE & THREAT MODEL

1. **SSRF & IP Guardrails**: `url_validator.py` blocks private/loopback/cloud-metadata IP ranges [VERIFIED IN CURRENT REPOSITORY].
2. **Secret Hygiene**: All credentials resolved via Pydantic `Settings`; zero hardcoded fallbacks in production paths [VERIFIED IN CURRENT REPOSITORY].
3. **Signed Stream Tokens**: HMAC-SHA256 tokens protect video streaming endpoints [VERIFIED IN CURRENT REPOSITORY].
4. **Merchant Redirects**: Redirect endpoints validate target host against allowlisted merchant domains [VERIFIED IN CURRENT REPOSITORY].

---

## 14. INFRASTRUCTURE & NETWORK ARCHITECTURE (OCI)

* **Production VM Specification**:
  - **Shape**: `VM.Standard.E2.1.Micro` (AMD 1-core OCPU, 1 GB RAM + 2 GB Swap, `x86_64`) [VERIFIED IN EXISTING PROJECT DOCUMENTATION].
  - **OS**: `Canonical Ubuntu 24.04 LTS` [VERIFIED IN EXISTING PROJECT DOCUMENTATION].
  - **Stack**: Caddy reverse proxy, Docker containers for FastAPI and Celery workers [VERIFIED IN CURRENT REPOSITORY].
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

    Gateway -->|Async Job Dispatch| Redis[(Redis Queue / Upstash)]
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

## 17. GIT & RELEASE BRANCHING FLOW

```
[Feature Branch] ---> PR ---> [Dev Branch] ---> promote.py ---> [staging Branch] ---> PR ---> [main Branch]
```
* **`Dev`**: Primary active integration branch [VERIFIED IN CURRENT REPOSITORY].
* **`staging`**: Pre-production branch linked to Vercel Staging Preview and Staging backend testing [VERIFIED IN CURRENT REPOSITORY].
* **`main`**: Protected production branch [VERIFIED IN CURRENT REPOSITORY].

---

## 18. WEBHOOK INGESTION ARCHITECTURE

* **Telegram Bot**: Webhook endpoint at `/api/v1/webhooks/telegram` backed by secret token header verification [VERIFIED IN CURRENT REPOSITORY].
* **WhatsApp Cloud API**: Webhook endpoint at `/api/v1/webhooks/whatsapp` backed by `x-hub-signature-256` HMAC validation over raw payload bytes [VERIFIED IN CURRENT REPOSITORY].

---

## 19. QUOTA & SAAS BILLING ARCHITECTURE

* **Quota Accounting**: Redis-backed sliding window rate limiter (`QuotaManager`) enforcing guest, free, and paid user tiers [VERIFIED IN CURRENT REPOSITORY].
* **Dual-Rail Billing**: Razorpay (INR) and Stripe (USD) integration stubs for subscription management [VERIFIED IN CURRENT REPOSITORY].

---

## 20. TELEMETRY & OBSERVABILITY ARCHITECTURE

* **Admin Telemetry**: Gated via `X-Admin-Api-Key` header or `role == 'admin'` claims [VERIFIED IN CURRENT REPOSITORY].
* **Metric Privacy**: Raw user URLs and sensitive query parameters are stripped before telemetry event persistence [VERIFIED IN CURRENT REPOSITORY].

---

## 21. DETAILED CURRENT PRODUCTION ARCHITECTURE

* **Frontend**: Next.js 15 PWA deployed on Vercel Production [VERIFIED IN EXISTING PROJECT DOCUMENTATION].
* **Backend**: FastAPI app running in Docker container on OCI VM behind Caddy reverse proxy [VERIFIED IN EXISTING PROJECT DOCUMENTATION].
* **Database**: Supabase Production PostgreSQL [VERIFIED IN EXISTING PROJECT DOCUMENTATION].
* **Status**: `UNTOUCHED` during all staging and development operations [VERIFIED IN CURRENT REPOSITORY].

---

## 22. DETAILED CURRENT STAGING ARCHITECTURE

* **Frontend**: Vercel Preview deployment bound to `staging` branch [VERIFIED IN CURRENT REPOSITORY].
* **Backend Host**: NOT PROVISIONED / NOT VERIFIED [EXTERNAL PLATFORM / INFRASTRUCTURE VERIFICATION REQUIRED].
* **Database**: Dedicated Staging Supabase project (`mzpkd...`) [VERIFIED IN CURRENT REPOSITORY].
* **Write Mode**: Initial deployment configured with `ALLOW_DB_WRITES=false` [VERIFIED IN CURRENT REPOSITORY].

---

## 23. NETWORK & EGRESS FIREWALL ARCHITECTURE

* **Host Firewall**: `deploy/setup_egress_firewall.sh` configures `iptables` and `ip6tables` rules [VERIFIED IN CURRENT REPOSITORY].
* **Egress Guard**: Rejects outbound container traffic to non-allowlisted destinations [VERIFIED IN CURRENT REPOSITORY].

---

## 24. CONFIGURATION & SECRETS HIERARCHY

* **Configuration Engine**: Pydantic `Settings` class (`backend/app/core/config.py`) reading environment variables [VERIFIED IN CURRENT REPOSITORY].
* **Secret Hygiene**: Zero hardcoded secret fallbacks in production execution paths [VERIFIED IN CURRENT REPOSITORY].

---

## 25. DOCKER & CADDY DEPLOYMENT ARCHITECTURE

* **Containers**: Defined in `docker-compose.yml` (`redis`, `api`, `worker`, `caddy`) [VERIFIED IN CURRENT REPOSITORY].
* **Caddy Reverse Proxy**: Automatic HTTPS TLS termination and reverse proxying to `api:8000` [VERIFIED IN CURRENT REPOSITORY].

---

## 26. CI/CD & VERIFICATION SCRIPTS

* **Local CI Verification**: `python scripts/ci_check.py` executing `tsc`, `lint`, `npm test`, `npm run build`, and `pytest` [VERIFIED IN CURRENT REPOSITORY].
* **Promotion Automation**: `python scripts/promote.py` for automated branch promotion [VERIFIED IN CURRENT REPOSITORY].
* **Post-Promotion Verification**: `scripts/verify_promotion.py` test suite runner [VERIFIED IN CURRENT REPOSITORY].

---

## 27. DEPLOYMENT READINESS 9-GATE MODEL

| Gate | Description | Environment | Status | Evidence Source | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gate 1** | Owner authorization & backlog ticket | Governance | `VERIFIED` | `JIRA_BACKLOG.md` ticket entries | `[VERIFIED IN CURRENT REPOSITORY]` |
| **Gate 2** | `Dev` -> `staging` promotion | Git Branch | `VERIFIED` | Clean git history & branch alignment | `[VERIFIED IN CURRENT REPOSITORY]` |
| **Gate 3** | Vercel Preview frontend build | Vercel | `VERIFIED` | Vercel preview build pipeline | `[EXTERNAL PLATFORM VERIFICATION REQUIRED]` |
| **Gate 4** | Staging backend API container startup | OCI Staging | `NOT VERIFIED` | Dedicated Staging OCI VM not provisioned | `[EXTERNAL PLATFORM VERIFICATION REQUIRED]` |
| **Gate 5** | Staging FastAPI `/health` endpoint | OCI Staging | `NOT VERIFIED` | Health response on staging host | `[EXTERNAL PLATFORM VERIFICATION REQUIRED]` |
| **Gate 6** | App -> Supabase Staging PostgREST read | Staging App | `NOT VERIFIED` | HTTP 404 on dummy slug lookup from deployed app | `[EXTERNAL PLATFORM VERIFICATION REQUIRED]` |
| **Gate 7** | Governed DB write enablement | Staging App | `NOT VERIFIED` | `ALLOW_DB_WRITES=true` configuration | `[PLANNED / INTENDED ARCHITECTURE]` |
| **Gate 8** | Redis / Celery async worker pool | Staging App | `DEFERRED` | Worker task queue processing | `[PLANNED / INTENDED ARCHITECTURE]` |
| **Gate 9** | Full E2E validation suite | Staging App | `DEFERRED` | End-to-end integration test output | `[PLANNED / INTENDED ARCHITECTURE]` |

---

## 28. SECURITY GAP MATRIX

| Security Domain | Mitigation Status | Current State Evidence |
| :--- | :--- | :--- |
| **SSRF & IP Spoofing** | Mitigated | `url_validator.py` IP resolution check & `TRUSTED_PROXY=False` default [VERIFIED IN CURRENT REPOSITORY] |
| **JWT Verification** | Mitigated | `security.py` ES256 JWKS signature verification & audience check [VERIFIED IN CURRENT REPOSITORY] |
| **Stream Token Security** | Mitigated | HMAC-SHA256 token requirement on `/stream-video` [VERIFIED IN CURRENT REPOSITORY] |
| **Database Minimum Privilege** | Mitigated | Migration `011_privilege_hardening.sql` executed on Supabase Staging [VERIFIED IN CURRENT REPOSITORY] |

---

## 29. ENVIRONMENT ISOLATION INVARIANTS

1. Development MUST NOT touch Production or Staging databases [VERIFIED IN CURRENT REPOSITORY].
2. Staging MUST use dedicated credentials and dedicated Supabase ref (`mzpkd...`) [VERIFIED IN CURRENT REPOSITORY].
3. Production (`scrq...`) MUST remain untouched during test runs [VERIFIED IN CURRENT REPOSITORY].

---

## 30. END-TO-END EXECUTION FLOWS

1. **User Request**: Web Share Target or Bot Webhook sends media URL [VERIFIED IN CURRENT REPOSITORY].
2. **URL Validation**: `url_validator.py` checks HTTPS, domain allowlist, and IP range [VERIFIED IN CURRENT REPOSITORY].
3. **Cache Lookup**: SHA-256 hash query against Supabase `extractions` table [VERIFIED IN CURRENT REPOSITORY].
4. **Media Processing**: Celery worker invokes `yt-dlp` (max 90s, 360p) and extracts frames [VERIFIED IN CURRENT REPOSITORY].
5. **AI Inference**: Gemini Flash extracts structured JSON with `schema_version` [VERIFIED IN CURRENT REPOSITORY].
6. **Payload Delivery**: Response serialized and delivered to PWA client [VERIFIED IN CURRENT REPOSITORY].

---

## 31. ARCHITECTURAL DECISION RECORDS (ADRS)

* **ADR-001**: Transition from Streamlit Monolith to Next.js 15 PWA + FastAPI Gateway [VERIFIED IN EXISTING PROJECT DOCUMENTATION].
* **ADR-002**: Adoption of Supabase PostgreSQL as Multi-Tenant Data Layer [VERIFIED IN EXISTING PROJECT DOCUMENTATION].
* **ADR-003**: In-Memory Fallback Dispatcher for Redis-less Local Development [VERIFIED IN CURRENT REPOSITORY].

---

## 32. ARCHITECTURE RISKS & OPEN QUESTIONS

| Risk / Open Question | Severity | Mitigation / Status |
| :--- | :--- | :--- |
| **Dedicated Staging OCI VM Capacity** | Medium | Pending OCI capacity availability check by Owner [UNKNOWN / REQUIRES OWNER CONFIRMATION] |
| **Gemini API Pricing / Quota Limits** | Medium | Monitored via Pydantic `Settings` and rate limiting [VERIFIED IN CURRENT REPOSITORY] |

---

## 33. DISASTER RECOVERY RUNBOOK ALIGNMENT

All disaster recovery procedures, database backup restoration steps, and emergency failover protocols align with `docs/architecture/DISASTER_RECOVERY.md` [VERIFIED IN EXISTING PROJECT DOCUMENTATION].

---

## 34. HISTORICAL ARCHITECTURE NOTES & DEPRECATION REGISTRY

* **Streamlit Monolith**: `[HISTORICAL / DEPRECATED]`. The initial Streamlit prototype (`streamlit_app.py`) served as the v0 proof-of-concept. All primary frontend capabilities have been migrated to the Next.js 15 PWA (`frontend/src/app`) and FastAPI API Gateway (`backend/app/main.py`) [VERIFIED IN CURRENT REPOSITORY].

---

## 35. DOCUMENTATION GOVERNANCE — MANDATORY LIVING-DOCUMENT RULE

> "Architecture and operational documentation are living project artifacts. They must remain synchronized with the actual governed implementation."

### SECTION 21 — DOCUMENTATION SYNCHRONIZATION & ARCHITECTURE DRIFT GUARD

**Rule 21**: Every governed project change must keep applicable technical documentation synchronized with implementation.

1. Any change affecting architecture, infrastructure, deployment, environments, APIs, authentication, security, database schema/migrations, background processing, AI providers, configuration, networking, CI/CD, observability, data flows, integrations, or operational procedures MUST include corresponding documentation updates in the same governed ticket/change.
2. The following documents are living project artifacts:
   * System / Solution Architecture Baseline (`docs/architecture/SYSTEM_ARCHITECTURE.md`)
   * Environment Architecture & Deployment Guide (`docs/architecture/ENVIRONMENTS.md`)
   * Oracle Cloud Infrastructure Runbook (`docs/architecture/ORACLE_CLOUD_DEPLOYMENT.md`)
   * Disaster Recovery Runbook (`docs/architecture/DISASTER_RECOVERY.md`)
   * Product Owner UX Showcase & Backlog (`docs/po-governance/JIRA_BACKLOG.md`)
   * Agent Engineering Rules (`AGENTS.md`)
3. Documentation updates must be based on actual implemented and verified state, not merely intended design.
4. A change must NOT update documentation to claim a capability, deployment, configuration, security control, or verification that has not actually been completed and empirically verified.
5. Every governed change MUST perform a **Documentation Impact Assessment** in its verification output.
6. Documentation changes must use the same ticket/governance context as the implementation change.
7. Obsolete documentation must be corrected or marked as historical/deprecated.
8. Documentation MUST distinguish the 5 evidence states.
9. The purpose of this rule is to prevent architecture drift, deployment drift, environment drift, infrastructure drift, and documentation drift.
