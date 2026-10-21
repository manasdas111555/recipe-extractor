# 🏛️ Universal Pro AI — Architectural Decision Records (ADRs)

---

## 1. DOCUMENT CONTROL

* **Document Title**: Architectural Decision Records (ADRs) & Baseline Log
* **File Path**: `docs/architecture/DECISIONS.md`
* **Governing Rule**: AGENTS.md Rule 22 (*Architectural Decision Tracking & Baseline Log*)
* **Document Status**: Active / Reconciled Baseline `[VERIFIED IN CURRENT REPOSITORY]`
* **Initial Baseline Date**: October 16, 2026
* **Target Audience**: Core Engineers, System Architects, Product Owners, Automated Coding Agents

---

## 2. ADR INDEX

| ADR ID | Title | Primary AGENTS.md Rule | Status | Initial Sprint |
| :--- | :--- | :--- | :--- | :--- |
| **[ADR-001](#adr-001-strict-url-validation-order--egress-security)** | Strict URL Validation Order & Egress Security | Rule 14 | **Accepted / Active** | Sprint 1 / Hardened Sprint 12 |
| **[ADR-002](#adr-002-dual-mode-background-task-dispatcher)** | Dual-Mode Background Task Dispatcher (Celery + Redis vs. In-Memory) | Rule 5 | **Accepted / Active** | Sprint 2 |
| **[ADR-003](#adr-003-ingestion-caps--canonical-hash-caching)** | Ingestion Caps (90s, 360p) & Canonical Hash Caching | Rule 4 | **Accepted / Active** | Sprint 2 / Hardened Sprint 11 |
| **[ADR-004](#adr-004-centralized-gemini-configuration--multi-llm-council-fallback)** | Centralized Gemini Configuration & Multi-LLM Council Consensus | Rules 8, 10 | **Accepted / Active** | Sprint 8 / Reconciled Sprint 12 |
| **[ADR-005](#adr-005-domain-affiliate-engine-isolation--immutable-partner-identifiers)** | Domain-Affiliate Engine Isolation & Immutable Partner Identifiers | Rule 3 | **Accepted / Active** | Sprint 3 |
| **[ADR-006](#adr-006-3-layer-environment-architecture--production-sign-off-gates)** | 3-Layer Environment Architecture & Production Sign-Off Gates | Rule 2 | **Accepted / Active** | Sprint 11 / Reconciled Sprint 12 |
| **[ADR-007](#adr-007-resilient-document-governance-assertion--section-scoping-protocol)** | Resilient Document Governance Assertion & Section-Scoping Protocol | Rules 1, 9, 16 | **Accepted / Active** | Sprint 13 (UPA-1311) |
| **[ADR-008](#adr-008-six-phase-release-lifecycle--mandatory-two-tier-playwright-release-gates)** | Six-Phase Release Lifecycle & Mandatory Two-Tier Playwright Release Gates | Rules 2, 16, 21 | **Proposed / Implemented on Dev** | Sprint 14 (UPA-1401) |
| **[ADR-009](#adr-009-supabase-data-api-least-privilege-grants-canonical-migration-source--replay-parity)** | Supabase Data API Least-Privilege Grants, Canonical Migration Source & Replay Parity | Rules 2, 4, 14, 16, 21 | **Proposed / Implemented on Dev** | Sprint 14 (UPA-1406) |

---

## ADR-001: Strict URL Validation Order & Egress Security

* **Status**: Accepted / Active `[VERIFIED IN CURRENT REPOSITORY]`
* **Date / Sprint**: Sprint 1 (Initial) / Sprint 12 (Hardened Egress Validation)
* **Governing Rules**: AGENTS.md Rule 14 (*Security Invariants*)

### Context & Problem Statement
Universal Pro AI ingests user-supplied video URLs from major social platforms (Instagram, YouTube, TikTok) and fetches media streams into cloud containers for AI inference. Without strict pre-download validation, the service is vulnerable to:
1. Server-Side Request Forgery (SSRF) targeting internal cloud metadata services (e.g., `169.254.169.254` on OCI/AWS).
2. DNS Rebinding attacks where an allowed hostname resolves to a loopback or private network IP.
3. Open Redirect vulnerability chains where an allowed domain redirects to a forbidden internal or malicious IP.
4. Denial of Service (DoS) from unparseable or malicious schemes (`file://`, `gopher://`, `http://`).

### Options Considered
1. **Option A: Delegate validation entirely to `yt-dlp`**:
   - *Pros*: Minimal custom code.
   - *Cons*: `yt-dlp` does not perform DNS pinning, does not block cloud metadata IPs by default, and allows redirect hops across domains, creating high-severity SSRF vulnerabilities.
2. **Option B: Web Application Firewall (WAF) / Reverse-Proxy URL Inspection**:
   - *Pros*: Edge-layer blocking.
   - *Cons*: WAF inspection cannot detect dynamic DNS rebinding or post-redirect IP hops executed by backend client sockets.
3. **Option C (Selected): Pre-Ingestion Custom URL Validator with DNS Pinning & Redirect Hop Re-Validation**:
   - *Pros*: Strict HTTPS enforcement, strict domain allowlist, socket DNS pre-resolution with global routability check (`ip.is_global`), unwrapping of IPv4-mapped IPv6, and re-validation across up to 3 redirect hops before any socket connection or cache query.

### Decision & Rationale
We implemented `backend/app/services/url_validator.py` as an immutable security boundary. Every entry point (FastAPI route, Celery task, Telegram bot, WhatsApp webhook, `/share-target`) must execute validation in the exact sequence:
$$\text{validate} \longrightarrow \text{cache lookup} \longrightarrow \text{download} \longrightarrow \text{inference}$$

* **HTTPS Enforcement**: Only `https://` is permitted; plaintext `http://` is unconditionally rejected.
* **Allowlist Enforcement**: Hostnames must match `ALLOWED_DOMAINS` (`instagram.com`, `youtube.com`, `youtu.be`, `tiktok.com`, `facebook.com`, `fb.watch`) or `ALLOWED_MERCHANT_DOMAINS`. Raw IPs are rejected.
* **SSRF Defense**: `resolve_and_validate_hostname()` uses `socket.getaddrinfo` to check that all resolved IPs are globally routable. Any private, loopback, link-local, multicast, or cloud-metadata address halts processing immediately.
* **Redirect Guardrail**: HTTP redirects are followed manually up to a maximum of 3 hops; every hop re-runs the full domain, scheme, and IP validation chain.

### Accepted Trade-Offs
* DNS resolution incurs an additional ~20–50ms latency before processing begins.
* Niche URL shorteners that redirect to Instagram/YouTube are blocked unless explicitly added to the allowlist.

---

## ADR-002: Dual-Mode Background Task Dispatcher

* **Status**: Accepted / Active `[VERIFIED IN CURRENT REPOSITORY]`
* **Date / Sprint**: Sprint 2 (Dual-Mode Architecture)
* **Governing Rules**: AGENTS.md Rule 5 (*Architectural Invariants & Dual-Mode Dispatcher*)

### Context & Problem Statement
Multimodal video extraction and AI reasoning take between 4 to 25 seconds per request. Running this synchronously in HTTP request threads would exhaust FastAPI worker connections and cause gateway timeouts (HTTP 504) on client browsers and mobile webviews.

However, requiring a live Redis broker and Celery worker cluster for local development or lightweight testing creates substantial friction for developers on Windows or restricted environments where Docker/Redis is not running.

### Options Considered
1. **Option A: Strict Celery + Redis Dependency**:
   - *Pros*: Unified production-grade distributed task queue.
   - *Cons*: Local development fails without Redis running; Windows developers face fork crashes (`multiprocessing.context.ForkProcess`).
2. **Option B: Pure FastAPI `BackgroundTasks`**:
   - *Pros*: Zero external dependencies; in-memory thread execution.
   - *Cons*: Unbounded concurrency under high traffic; task state lost if the API process restarts; does not scale horizontally across multiple container instances.
3. **Option C (Selected): Dual-Mode Dispatcher with Automatic Broker Probing & Windows Guard**:
   - *Pros*: Distributed Celery + Redis queue is used in Staging and Production; FastAPI `BackgroundTasks` automatically activates as a seamless fallback if Redis is unreachable. Windows Celery execution is protected via `--pool=solo`.

### Decision & Rationale
Implemented `backend/app/api/v1/extract.py:enqueue_extraction` with dynamic broker reachability detection (`is_celery_broker_reachable()`):
1. **Production / Staging**: Tasks are dispatched asynchronously via `extract_video_task.apply_async(...)` to Celery backed by Redis (`redis:7-alpine` on OCI or Upstash Redis).
2. **Local Fallback**: If Redis is unreachable, the task is enqueued to `background_tasks.add_task(run_extraction_worker_sync, ...)`.
3. **Windows Worker Guard**: In `scripts/run_worker.py`, the system detects `sys.platform == "win32"` and forces `--pool=solo` (or `--pool=threads`) to eliminate POSIX `fork()` crashes.

### Accepted Trade-Offs
* `BackgroundTasks` fallback does not persist across container crashes.
* Progress tracking must support dual backends: Redis keys when Celery is active, and an in-memory thread-safe `JobManager` singleton when running in fallback mode.

---

## ADR-003: Ingestion Caps & Canonical Hash Caching

* **Status**: Accepted / Active `[VERIFIED IN CURRENT REPOSITORY]`
* **Date / Sprint**: Sprint 2 (Caps) / Sprint 11 (Canonical Hash Hardening)
* **Governing Rules**: AGENTS.md Rule 4 (*Ingestion Guardrails & Cloud Cost Protection*)

### Context & Problem Statement
Unrestricted video downloads risk severe cloud cost exhaustion, disk exhaustion, and abusive compute spikes:
1. Long videos (>90 seconds) consume excessive Gemini API token quotas and memory during multimodal reasoning.
2. High-resolution downloads (1080p, 4K) overwhelm container disk bandwidth without improving AI multimodal recipe/tutorial extraction accuracy.
3. Viral social media videos extracted repeatedly by multiple users waste proxy bandwidth and trigger redundant Gemini API billing.

### Options Considered
1. **Option A: Full-Resolution Downloads with Dynamic Duration**:
   - *Pros*: Pristine media quality.
   - *Cons*: Heavy bandwidth consumption (50–200MB per video), slow upload to Gemini Cloud, high risk of disk exhaustion.
2. **Option B: Raw URL String Caching**:
   - *Pros*: Simple string matching in database.
   - *Cons*: Tracking query parameters (`?igsh=...`, `?utm_source=...`) produce cache misses for identical videos.
3. **Option C (Selected): Hard Ingestion Ceilings (90s / 360p / 50MB) + SHA-256 Canonical Hash Caching**:
   - *Pros*: Deterministic bandwidth limits, fast inference upload, 0-cost instant cache hits for viral reels.

### Decision & Rationale
We locked the following invariants in `backend/app/core/config.py`, `backend/app/workers/media_downloader.py`, and `downloader.py`:
1. **Duration Cap (`MAX_VIDEO_DURATION = 90`)**: `yt-dlp` extracts metadata first. If duration exceeds 90 seconds, the download fails closed immediately before fetching media chunks.
2. **Resolution Cap (360p Max)**: Media format string is strictly enforced:
   ```text
   bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best[height<=360]
   ```
3. **Filesize Ceiling**: Strict 50MB ceiling enforced via `max_filesize` in `yt-dlp` options.
4. **Canonical Hash Caching**: URLs are stripped of query parameters and converted to canonical platform representations. A SHA-256 hash is computed and queried against Supabase `extractions.url_hash` *before* initiating any proxy download or AI call. Cache hits return HTTP 200 in ~0ms without burning daily user quota.

### Accepted Trade-Offs
* Videos longer than 90 seconds (e.g., full YouTube cooking episodes) are rejected; users must use short-form content.
* 360p video streams have reduced visual fidelity for human viewing, but provide optimal optical character recognition (OCR) and multimodal feature extraction for Gemini Flash.

---

## ADR-004: Centralized Gemini Configuration & Multi-LLM Council Consensus Fallback

* **Status**: Accepted / Active `[VERIFIED IN CURRENT REPOSITORY]`
* **Date / Sprint**: Sprint 8 (Council Mode) / Sprint 12 (Model Lifecycle Governance)
* **Governing Rules**: AGENTS.md Rule 8 (*Gemini Model Lifecycle*) & Rule 10 (*Multi-LLM Council Consensus*)

### Context & Problem Statement
AI models undergo frequent deprecation, rate-limiting (HTTP 429/503), and latency variability:
1. Hardcoded model names scattered across code cause silent failures when Google deprecates endpoints.
2. Multimodal extraction must withstand sudden capacity shortages on specific model tiers without degrading user experience.
3. High-stakes culinary, tutorial, and technical instructions require cross-model verification when requested by pro users.

### Options Considered
1. **Option A: Static Single Model (e.g., hardcoded `gemini-1.5-flash`)**:
   - *Pros*: Simple invocation.
   - *Cons*: Vulnerable to single-point model outages and Google deprecation schedules.
2. **Option B: Multi-LLM Council as Default Execution**:
   - *Pros*: Maximum consensus and cross-verification across 3 LLM providers (Gemini, Groq Llama, Mistral).
   - *Cons*: High latency (15–30s) and multi-provider token costs; completely impractical as the default path for high-throughput mobile users.
3. **Option C (Selected): Centralized Model Settings + Fast Cascade Failover + Opt-In Council Mode**:
   - *Pros*: `Settings` serves as single source of truth. Single-model execution cascaded across Google's active flash family with sub-second failover. Multi-LLM Council is strictly opt-in or fallback.

### Decision & Rationale
1. **Centralized Model Registry**: Model identifiers live strictly in `backend/app/core/config.py:Settings`.
2. **Cascaded Fast Failover in `gemini_processor.py`**:
   The primary execution cascade tries:
   $$\text{gemini-3.8-flash} \longrightarrow \text{gemini-3.7-flash} \longrightarrow \text{gemini-3.6-flash} \longrightarrow \text{gemini-3.5-flash} \longrightarrow \text{gemini-3.5-flash-lite}$$
   On HTTP 503, 429, or timeout, the engine immediately switches to the next model tier without stalling.
3. **Provider Key Isolation & Graceful Degradation**:
   Secondary providers (Mistral, Groq) execute only if their keys are configured. Missing secondary keys degrade gracefully to single-model execution without throwing HTTP 500 errors.
4. **Council Invariant (Rule 10)**: The 3-Stage Multi-LLM Council Consensus Engine is never default; it is strictly opt-in or an explicit retry strategy.

### Accepted Trade-Offs
* Maintaining failover logic across multiple Gemini model generations requires continuous monitoring of Google's official API deprecation notices.

---

## ADR-005: Domain-Affiliate Engine Isolation & Immutable Partner Identifiers

* **Status**: Accepted / Active `[VERIFIED IN CURRENT REPOSITORY]`
* **Date / Sprint**: Sprint 3 (Affiliate Engine)
* **Governing Rules**: AGENTS.md Rule 3 (*Monetization Invariants & Revenue Shield*)

### Context & Problem Statement
The application generates revenue through e-commerce and quick-commerce affiliate links (Amazon Associates, EarnKaro, Blinkit, Zepto, Instamart). If affiliate logic is scattered across UI components or AI prompt templates:
1. AI hallucination can corrupt store links, invent fake tracking tags, or alter monetization parameters.
2. Irrelevant merchants (e.g., fast fashion links on a butter chicken recipe, or grocery links on a coding tutorial) damage conversion and user trust.
3. Modifying store parameters could break revenue tracking.

### Options Considered
1. **Option A: Prompt-Driven Affiliate Link Insertion**:
   - *Pros*: The LLM generates product links directly in the extracted markdown text.
   - *Cons*: High hallucination rate, broken query URLs, corrupted affiliate tags, security risk of arbitrary unencoded URLs.
2. **Option B: Frontend Client-Side Link Decoration**:
   - *Pros*: Client appends tags before rendering `<a>` tags.
   - *Cons*: Exposed to ad-blockers; easy client-side tampering; inconsistent across export formats (.txt, WhatsApp deep links, Telegram bot).
3. **Option C (Selected): Isolated Backend Affiliate Engine with Immutable Constants**:
   - *Pros*: Strict domain separation. Monetization logic lives exclusively in `backend/app/services/affiliate_engine.py`. URL encoding and category rules are deterministic.

### Decision & Rationale
1. **Immutable Constants**:
   - Amazon Associates Tag: `tag=manasdas11155-21`
   - EarnKaro Tracking ID: `r=5608766`
2. **Domain-Specific Storefront Routing**:
   - `RECIPE` $\longrightarrow$ 10-Minute Quick Commerce (Blinkit, Zepto, Swiggy Instamart, JioMart) + Amazon Grocery.
   - `BEAUTY_FASHION` $\longrightarrow$ Flipkart, Myntra, AJIO, Nykaa via EarnKaro.
   - `TUTORIAL` / `TECH` $\longrightarrow$ Official documentation and YouTube tutorials; e-commerce storefronts are suppressed.
3. **Strict URL Encoding**: All search queries passed to merchants use `urllib.parse.quote_plus()`.
4. **Domain-Affiliate Separation**: UI components and AI prompt strings NEVER contain hardcoded store links or affiliate tags.

### Accepted Trade-Offs
* Quick-commerce deep links use search queries (`/search?q=...`) rather than exact SKU product IDs because real-time grocery SKU availability varies by PIN code.

---

## ADR-006: 3-Layer Environment Architecture & Production Sign-Off Gates

* **Status**: Accepted / Active `[VERIFIED IN CURRENT REPOSITORY]`
* **Date / Sprint**: Sprint 11 / Reconciled Sprint 12
* **Governing Rules**: AGENTS.md Rule 2 (*Sprint Governance & PO Production Gate*)

### Context & Problem Statement
Direct pushes and ad-hoc hotfixes to production risk live downtime, database corruption, and broken user sessions. In a governed AI pair-programming environment, agents must have strict guardrails preventing unauthorized deployments or speculative code promotions.

### Options Considered
1. **Option A: Traditional 2-Tier (Dev $\rightarrow$ Main)**:
   - *Pros*: Rapid deployment cycle.
   - *Cons*: Local development changes deploy directly to production without live staging verification, risking broken mobile viewports and production outages.
2. **Option B (Selected): Strict 3-Layer Environment Isolation with PO Production Gate**:
   - *Pros*: Complete isolation between local developer sandbox (Layer 1), live Vercel Preview / Staging OCI VM (Layer 2), and live production containers (Layer 3). Zero direct-to-production pushes permitted.

### Decision & Rationale
1. **Layer 1: Development (`Dev` branch)**:
   - Local sandbox, unit tests (`pytest`), local Next.js builds. Direct deployment to cloud is forbidden.
2. **Layer 2: Staging (`staging` branch)**:
   - Vercel Preview deployments and Staging cloud containers (`129.225.86.241`, Staging Supabase DB `mzpkd...`). All feature additions, bug fixes, and manual verifications deploy here first.
3. **Layer 3: Production (`main` branch)**:
   - `universal-pro-ai.vercel.app` and Production OCI VM (`140.245.214.28`, Production Supabase DB `scrq...`).
4. **PO Gate**: Agents must NEVER push or merge to `main` without explicit, written prior approval from the repository owner.
5. **Step-by-Step Staging Promotion**: Changes must be promoted to `staging` and verified on Staging before any production promotion is considered.

### Accepted Trade-Offs
* Promotion requires a multi-step git merge and verification cycle (`scripts/promote.py`, `scripts/ci_check.py`).
* Staging environment requires maintaining isolated configuration, secrets, and database hosts.

---

## ADR-007: Resilient Document Governance Assertion & Section-Scoping Protocol

* **Status**: Accepted / Verified on Staging (PR #6 @ `48a426c`) `[VERIFIED IN CURRENT REPOSITORY]`
* **Date / Sprint**: Sprint 13 (UPA-1311)
* **Governing Rules**: AGENTS.md Rule 1 (*Test Suite Integrity*), Rule 9 (*Living Documentation Contract*), Rule 16 (*Evidence & Verification*)

### Context & Problem Statement
Section 9 of `AGENTS.md` mandates continuous maintenance of the project's living architecture documents. Historical tests in `tests/test_sprint14_commerce.py` asserted an exact substring match on the section's heading title: `"Mandatory 4-Core Document Governance Contract"`.

When UPA-1308 added `docs/architecture/DECISIONS.md` and `docs/architecture/FLOW.md` (expanding the contract from 4 to 6 documents) and retitled Section 9 to `## 9. Mandatory Document Governance Contract & Living Architecture Files`, the exact title assertion broke. This produced a brittle test failure on subsequent test runs even though all document governance requirements were strictly fulfilled.

### Options Considered
1. **Option A: Revert Section 9 heading in `AGENTS.md`**:
   - *Pros*: Makes the legacy assertion pass without touching test files.
   - *Cons*: Violates the living architecture reality where 6 documents are actively maintained; mislabels the section as "4-Core".
2. **Option B (Selected): Section-Scoped Path Validation & Method Renaming**:
   - *Pros*: Dynamically locates Section 9 via line-anchored heading (`(?m)^##\s+9\..*$`) and extracts until the next level-two heading (`(?m)^##\s+`) without hardcoding Section 10. Asserts that each of the six required document paths (`docs/TROUBLESHOOTING.md`, `docs/po-governance/PRODUCT_OWNER_UX_SHOWCASE.md`, `docs/architecture/DISASTER_RECOVERY.md`, `docs/USER_MANUAL.md`, `docs/architecture/DECISIONS.md`, `docs/architecture/FLOW.md`) is explicitly present in the section. Renames test method to `test_mandatory_document_governance_contract_and_user_manual`.
   - *Cons*: Requires an authorized test contract update under Rule 1 with explicit Product Owner sign-off.

### Decision & Rationale
We adopted Option B under explicit Product Owner approval. Rather than asserting a volatile markdown heading string or assuming Section 10 is the only possible terminator, the test uses line-anchored regex to extract Section 9 up to the subsequent level-two heading and validates the contractual substance by asserting the presence of all six canonical document paths inside the extracted section. If any document is removed or misspelled, the test fails with an informative error message naming the missing file.

### Accepted Trade-Offs
* Requires `AGENTS.md` section numbering for Section 9 (`## 9.`) to be maintained, but does not constrain subsequent section numbering.

---

## ADR-008: Six-Phase Release Lifecycle & Mandatory Two-Tier Playwright Release Gates

* **Status**: Proposed / Implemented on Dev `[VERIFIED IN CURRENT REPOSITORY]`
* **Date / Sprint**: Sprint 14 (UPA-1401)
* **Governing Rules**: AGENTS.md Rule 2 (*Sprint Governance & Release Lifecycle*), Rule 16 (*Verification & Definition of Done*), Rule 21 (*Living Documentation Contract*)
* **Sequential Numbering Reconciliation**: Formally designated as ADR-008 (sequentially following ADR-007) to maintain contiguous baseline numbering; resolves preliminary planning references to ADR-014.

### Context & Problem Statement
Operational release activities had expanded into approximately 13 loosely structured operational phases across development, promotion, and deployment. This created ambiguity in three critical areas:
1. **Mocked vs Live Verification**: Local Playwright tests (`npm run test:e2e:mocked` against `http://localhost:3000`) were not formally segregated in policy from live deployed environment verification, risking false confidence where passing offline mock tests could be mistaken for live Staging acceptance.
2. **Staging Release Gate Absence**: Staging deployments lacked a mandatory, lightweight live browser smoke gate executing after *every* deployment before Product Owner acceptance, while un-mocked extraction tests risked mutating the database or failing due to external rate limits.
3. **Rollback & Health Discrepancies**: Staging documentation cited speculative custom domain FQDNs (`staging-api.universal-pro-ai.com`) rather than authoritative OCI VM IPs, and production rollback procedures relied on unconditional `git revert` commands that could create concurrency hazards.

### Options Considered
1. **Option A: Retain 13-Phase Ad-Hoc Process & Offline CI Only**:
   - *Pros*: Minimal tooling changes.
   - *Cons*: High operational friction, unclear stage boundaries, risk of deploying broken staging UIs to production without live validation.
2. **Option B (Selected): Consolidated Six-Phase Release Lifecycle with Two-Tier Live Playwright Release Gates**:
   - *Pros*:
     - Consolidates operations into six sequential, well-defined phases: Phase 1 (Intake & Governed Planning), Phase 2 (Dev Implementation & Local Verification), Phase 3 (Living Document Sync & Definitive Verification), Phase 4 (Governed Staging Promotion), Phase 5 (Live Staging Deployment Verification & Release Gates), Phase 6 (Governed Production Release & Closeout).
     - Establishes a Two-Tier Staging Release Gate: Tier 1 (Universal Live Staging Smoke Gate: `smoke.staging.e2e.ts`) running after every deployment, and Tier 2 (Conditional Live Extraction E2E: `staging.live.e2e.ts`) triggered only on extraction/routing/worker changes and protected by `ALLOW_DB_WRITES=false`.
     - Reconciles authoritative endpoints (`https://universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app` and `http://129.225.86.241/health`).
     - Replaces blind git reverts with a governed, bounded Production rollback protocol requiring failed SHA capture, owner alert, known-good version target identification, and operator intervention safeguards.
   - *Cons*: Requires developers and automated agents to strictly follow Phase 3 documentation synchronization before running the definitive Rule 16 pipeline.

### Decision & Rationale
We adopted Option B. By codifying the Six-Phase Release Lifecycle in `AGENTS.md` Rule 2 and separating mocked sandbox testing (`test:e2e:mocked`) from deployed environment gates (`test:e2e:staging:smoke`), the project ensures:
1. No release is accepted on Staging without empirical browser evidence of UI bootstrap, single docked player invariants, and CTA interactivity.
2. Un-mocked live extractions never write dirty rows to production or staging databases.
3. Documentation synchronization is completed and verified against the definitive 5-step Rule 16 pipeline *before* PR submission or promotion.
4. Production rollback is bounded and safe against concurrency issues.
5. **Commit-Bound Evidence & Source-Aware Preflight**: `scripts/promote.py` enforces source-aware preflight manifest verification (`verify_evidence_manifest`): Dev → Staging preflight verifies source `Dev` manifest using `--env dev` with expected Dev SHA, accepting Dev-appropriate classification (`mocked` or `live`). Staging release acceptance strictly requires live Staging evidence (`executionClassification: "live"`). Staging → Production preflight verifies source `staging` manifest using `--env staging` with expected Staging SHA, strictly enforcing `executionClassification: "live"`. Mocked evidence cannot satisfy Staging or Production release gates.
6. **Verifier Output Label & Verdict Hygiene**: `scripts/verify_promotion.py` displays raw manifest status as `Payload Self-Reported Status` and emits explicit evaluated final gate verdicts (`REJECTED (FAILED CLOSED)` / `PASSED`), ensuring false greens are impossible when validation fails closed.
7. **Hardened Staging Smoke Error Tracking & Assertion Contract**: `smoke.staging.e2e.ts` tracks failed HTTP responses across both frontend preview and backend API origins (`STAGING_API_URL` or fallback `http://129.225.86.241`), and validates navigation response (`validateNavigationResponse`) fail-closed. Initial live execution against Staging merge commit `85fa6e7b7366711ab9c3f9b2a3271ecae86d99d7` failed because it expected the Submit CTA to be enabled while the URL input was empty. Application validation intentionally enforces `disabled={isLoading || !url}`. The assertion contract was corrected on Dev (`0c107ca681b1e5dda8d61f5b58f8e33ffb224e67`) to verify the disabled state on empty input, verify enabled state when a fixture URL is supplied, and clear the input without submitting an extraction request. Live Staging release gate remains `FAIL` pending promotion of the fix and live retest.
8. **Environment Classification Hygiene**: Staging smoke executions must supply `TEST_ENV=staging` so that `evidence-manifest-reporter.ts` records `environment: "staging"` and `scripts/verify_promotion.py --verify-manifest --env staging` evaluates evidence consistently without defaulting to `dev`.
9. **Ticket-Scoped Promotion Branch Support & Fail-Closed Remote Lookup**: `scripts/promote.py` enforces validated `--ticket` parameters (`^[a-z]+-\d+$`, e.g., `upa-1401`) for Staging promotion, mapping to canonical branches `promotion/<ticket>-staging` (e.g., `promotion/upa-1401-staging`). Safe branch checkout (`git checkout -b`) verifies both local (`git show-ref --verify`) and remote (`git ls-remote --heads origin`) existence before branching. Remote queries fail closed: empty stdout with exit code 0 indicates absence, whereas any nonzero exit code (network, auth, or remote failure) halts execution immediately with an explicit Rule 2 error to prevent unintended branch collisions or corrupt promotion states.
10. **E2E Evidence Artifact Isolation & Non-Destructive Multi-Run Framework (UPA-1403)**: To enable repeated live Staging smoke gate executions without risk of clobbering historical evidence manifests or screenshots, `frontend/e2e/reporters/evidence-manifest-reporter.ts`, `frontend/e2e/helpers/evidence-tracker.ts`, and `frontend/playwright.config.ts` support dynamic isolation via `process.env.EVIDENCE_OUTPUT_DIR`, `process.env.DISABLE_SECONDARY_MANIFEST_WRITE`, `process.env.E2E_SECONDARY_EVIDENCE_DIR`, `process.env.EVIDENCE_MANIFEST_FILENAME`, and `process.env.PLAYWRIGHT_HTML_REPORT_DIR`. When `EVIDENCE_OUTPUT_DIR` is set to an isolated directory, all Playwright traces, videos, step screenshots, and `evidence-manifest.json` are encapsulated within that directory, and secondary mirroring into `e2e-evidence/` is suppressed to preserve historical evidence intact. `scripts/verify_promotion.py` dynamically auto-detects `EVIDENCE_OUTPUT_DIR` or `EVIDENCE_MANIFEST_PATH` with full fallback compatibility to default paths.
11. **Tier 2 Live Staging E2E Cache-Miss & Worker Stage Hardening (UPA-1405)**: To ensure that un-mocked Tier 2 live staging extraction tests (`staging.live.e2e.ts`) genuinely exercise the full asynchronous downloader and worker pipeline under `ALLOW_DB_WRITES=false`, the test asserts an initial HTTP 202 response and explicitly fails closed if an initial HTTP 200 or `is_cached === true` response occurs (indicating a viral cache hit that bypassed the media downloader, throwing `[UPA-1305 VALIDATION BLOCKED]`). Furthermore, the test correlates status polling to the exact submitted `targetJobId` and requires observing intermediate worker progress stages (`downloading_media` or `multimodal_ai_inference`) during extraction, strictly rejecting runs where only terminal `completed` status was observed without visible worker execution. In-flight URL parameters and credentials in test traces and failure summaries are sanitized via `sanitizeUrl` and `sanitizeText` to prevent accidental credential leakage in test reports and CI logs.


### Accepted Trade-Offs
* Running Tier 1 live Staging smoke tests requires Vercel edge protection bypass tokens and network access to Vercel preview URLs.
* Local development remains strictly offline/mocked; live gates are evaluated exclusively against deployed Staging and Production layers.
* Mocked test evidence cannot satisfy Staging or Production promotion gates; promotion automation fails closed if only mocked evidence or mismatched SHAs are provided.
* Staging promotion branches require explicit ticket identifiers, rejecting generic branch names to prevent collisions across concurrent sprint workflows.

---

## ADR-009: Supabase Data API Least-Privilege Grants, Canonical Migration Source & Replay Parity

* **Status**: Proposed / Implemented on Dev `[VERIFIED IN DEV SANDBOX]`
* **Date / Sprint**: Sprint 14 (UPA-1406)
* **Governing Rules**: AGENTS.md Rules 2 (*Sprint Governance & Gate Integrity*), 4 (*Ingestion Guardrails & Cache*), 14 (*Security Invariants*), 16 (*Verification Before Completion*), 21 (*Living Document Synchronization*), 22 (*Architectural Decision Records*)

### Context & Problem Statement
On October 30, 2026, Supabase will deprecate the legacy PostgreSQL behavior that automatically executed `GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated, service_role` for newly created tables.

Universal Pro AI interacts with PostgreSQL exclusively through the PostgREST HTTP Data API; there are zero direct PostgreSQL wire/TCP connections in application runtime. PostgREST role visibility is strictly dictated by PostgreSQL table-level grants.

Prior to UPA-1406:
1. `001_initial_schema.sql` relied on default privileges and lacked explicit table-level grants for `profiles`, `extractions`, and `affiliate_clicks`.
2. `009_beta_telemetry_feed.sql` lacked explicit grants, leaving `beta_telemetry_feed` vulnerable to post-October 30 API invisibility.
3. `010_telemetry_events.sql` used an un-hardened `GRANT ALL ON public.telemetry_events TO service_role`, granting unnecessary privileges (`DROP`, `ALTER`, `DELETE`).
4. Migration directory drift existed between `backend/database/` (active source) and root `database/` (which lacked migrations `010`, `011`, and `012`).
5. In fresh provisioning or disaster recovery scenarios, replaying historical migrations would produce tables inaccessible to PostgREST, throwing HTTP 404 or HTTP 42501 (`insufficient_privilege`) errors.
6. A clear architectural distinction was required between schema rebuild readiness (recreating schema/grants via migrations) and independent data recovery (restoring data rows from external backups), while adhering to Supabase's two-project Free-tier constraint.

### Options Considered
1. **Option A: Retain Implicit Grants & Rely on Dashboard Manual Permissions**:
   - *Pros*: Zero migration edits.
   - *Cons*: Highly error-prone; breaks automated disaster recovery and fresh environment setups; causes immediate HTTP 42501 failures on any newly created Supabase project after October 30, 2026.
2. **Option B: Broad Blanket Grants (`GRANT ALL ON ALL TABLES IN SCHEMA public ...`)**:
   - *Pros*: Quick fix.
   - *Cons*: Violates least-privilege principles; grants excessive permissions (e.g. `DROP`, `TRUNCATE`) to application roles; risks exposing internal telemetry tables to public client writes.
3. **Option C (Selected): Explicit Least-Privilege Grants per Table, Function Search-Path Protection, Directory Parity & Automated CI Guards**:
   - *Pros*:
     - Grants explicitly and only the operations each application access path requires.
     - Protects function execution and search paths (`search_path = public`).
     - Reconciles canonical `backend/database/` and mirrored `database/` to 100% byte parity.
     - Enforces full migration replay chain (`001 -> 009 -> 010 -> 011 -> 012`).
     - Adds automated pytest suite (`tests/test_database_grants.py`) and static CI check (`scripts/ci_check.py`).
     - Documents disaster recovery protocols within the two-project Free-tier boundary.
   - *Cons*: Requires updating and maintaining mirror parity across both migration directories for all future database changes.

### Decision & Rationale
We implemented Option C:
1. **Explicit Table-Level Least-Privilege Grants**:
   - `public.profiles`: `GRANT SELECT, UPDATE ON public.profiles TO service_role` (application reads and updates quotas/tags; no public client access).
   - `public.extractions`: `GRANT SELECT, INSERT, DELETE ON public.extractions TO service_role` (worker writes, cache reads, and cleanup); `GRANT SELECT ON public.extractions TO anon, authenticated` (read-only client extraction viewer).
   - `public.affiliate_clicks`: `GRANT SELECT, INSERT ON public.affiliate_clicks TO service_role` (telemetry logging; no public client access).
   - `public.beta_telemetry_feed`: `GRANT INSERT ON public.beta_telemetry_feed TO service_role` (worker telemetry ingest; client access revoked).
   - `public.telemetry_events`: `GRANT SELECT, INSERT ON public.telemetry_events TO service_role` (hardened from `GRANT ALL`; client access revoked).
2. **Schema Usage & Function Hardening**:
   - `GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role`.
   - Explicit `SET search_path = public` on reviewed functions (`increment_user_extraction_count`, `reset_daily_extraction_quotas`, `handle_new_user`).
   - Function execution revocations strictly narrowed to reviewed functions (`REVOKE EXECUTE ... FROM PUBLIC; GRANT EXECUTE ... TO service_role`), preventing unintended disruption of PostgreSQL built-ins (`uuid-ossp`, `pgcrypto`).
3. **Canonical Migration Directory & Parity**:
   - `backend/database/` is designated as the canonical source of truth.
   - Root `database/` is maintained as an exact 1-to-1 mirror.
   - The replay sequence is formalized: `001_initial_schema.sql` $\rightarrow$ `009_beta_telemetry_feed.sql` $\rightarrow$ `010_telemetry_events.sql` $\rightarrow$ `011_privilege_hardening.sql` $\rightarrow$ `012_extraction_public_ownership.sql`.
4. **Disaster Recovery & Capacity Alignment**:
   - Schema rebuild readiness (DDL + explicit grants) is distinguished from independent data recovery (encrypted logical `pg_dump` backups and Supabase Storage backups).
   - Free-tier 2-project limit (Production & Staging) is accounted for; no third project or Staging backup tables are permitted.
5. **Automated Static CI Protection**:
   - Dedicated test suite `tests/test_database_grants.py` asserts table grants, directory parity, search-path protections, execute restrictions, and RLS across all tables.
   - Step 5 in `scripts/ci_check.py` validates database grants as an unskippable gate before PR or promotion.

### Accepted Trade-Offs
* Any future table introduced in `public` must declare explicit table-level grants for `service_role` and optionally `anon`/`authenticated`, or `tests/test_database_grants.py` will fail closed.
* All future migration additions must be mirrored across both `backend/database/` and `database/` to satisfy directory parity checks.

---

## ADR-010: Supabase Staging Free-Tier Inactivity Keep-Alive, Database Activity Probing & Credential Isolation

* **Status**: Proposed / Implemented on Dev `[VERIFIED IN DEV SANDBOX]`
* **Date / Sprint**: Sprint 14 (UPA-1409)
* **Governing Rules**: AGENTS.md Rules 2 (*Sprint Governance & Gate Integrity*), 4 (*Ingestion Guardrails & Cloud Cost Protection*), 6 (*Secret Hygiene & Security Isolation*), 9 (*Mandatory Document Governance*), 14 (*Security Invariants*), 16 (*Verification Before Completion*), 21 (*Living Document Synchronization*), 22 (*Architectural Decision Records*)

### Context & Problem Statement
Under Supabase platform architecture, projects on the Free tier are automatically paused after 7 consecutive days of zero database activity. Once paused, incoming PostgREST API and PostgreSQL requests fail with HTTP 503 Service Unavailable (`"Project is paused"`).

Universal Pro AI operates within explicit infrastructure boundaries:
1. **Two-Project Free-Tier Limit**: The organization uses its two Free-tier project slots for **Production** (`scrqvbgjybnrvcpxbygf`) and **Staging** (`mzpkdmaxsuhwezsooidu`).
2. **Staging Inactivity Exposure**: Between release cycles or active testing sprints, Staging traffic can remain idle for over 7 days, causing Supabase to pause the database. This breaks automated Staging smoke tests (`smoke.staging.e2e.ts`), Vercel Preview validations, and developer testing.
3. **Legacy Keep-Alive Limitations**: The existing keep-alive setup (`scripts/keep_alive.py` and `.github/workflows/keep_alive.yml`) was originally designed for retired Streamlit frontend apps and pinged the OCI FastAPI backend `/health` endpoint. It issued zero database queries or PostgREST calls and provided zero mitigation against Supabase Free-tier database pausing.
4. **Production Protection Invariant**: The repository owner strictly directed that the existing Production keep-alive implementation must remain 100% untouched to avoid any risk of regression to Production health monitoring.

### Options Considered
1. **Option A: Modify Existing `scripts/keep_alive.py` to Probe Staging Database**:
   - *Pros*: Single script for all keep-alive tasks.
   - *Cons*: Violates the strict owner constraint that Production keep-alive must remain untouched; conflates Production frontend/backend monitoring with Staging database probing; creates shared blast radius where a Staging secret misconfiguration could break Production alerting.
2. **Option B: External Third-Party Cron / Webhook Service (e.g. UptimeRobot, cron-job.org)**:
   - *Pros*: Offloads scheduling from GitHub Actions.
   - *Cons*: Introduces unnecessary external third-party dependencies; requires provisioning and managing external accounts; stores Staging credentials on third-party servers; increases attack surface and maintenance overhead.
3. **Option C (Selected): Dedicated, Isolated Staging Keep-Alive Script & GitHub Actions Workflow with Strict Hostname Locking & Least-Privilege `anon` Probing**:
   - *Pros*:
     - **Complete Isolation**: Existing Production files (`scripts/keep_alive.py`, `.github/workflows/keep_alive.yml`) remain 100% byte-for-byte untouched.
     - **Strict Target Locking**: Fails closed before issuing any network request unless the URL strictly matches `https://mzpkdmaxsuhwezsooidu.supabase.co`. Accidental substitution of Production URLs is physically prevented.
     - **Credential Isolation**: Uses dedicated `SUPABASE_STAGING_URL` and `SUPABASE_STAGING_ANON_KEY` secrets with zero fallback to Production.
     - **Least-Privilege Role**: Uses the `anon` key to query `public.extractions` (`GET /rest/v1/extractions?select=id&limit=1`), utilizing the explicit `GRANT SELECT` established in `011_privilege_hardening.sql`. Never requires `service_role` privileges.
     - **Zero Secret/Data Logging**: Structured logging emits only environment, status, duration, and HTTP code; never logs keys, bearer tokens, or response rows.
     - **Deterministic Error Handling**: Empty array responses (`[]`) are accepted as successful database activity; timeouts, network errors, and non-200 HTTP codes cause non-zero exit codes.
     - **Full Automated Unit Suite**: 22 unit tests verify URL validation, header injection, secret masking, and failure handling using mocked HTTP responses.
   - *Cons*: Requires separate repository secrets (`SUPABASE_STAGING_URL` and `SUPABASE_STAGING_ANON_KEY`) to be provisioned in GitHub Actions repository settings.

### Decision & Rationale
We implemented Option C:
1. **Dedicated Script**: `scripts/staging_supabase_keep_alive.py` implementing URL parsing, hostname locking (`mzpkdmaxsuhwezsooidu.supabase.co`), key validation ($\ge 20$ chars), PostgREST query execution (`GET /rest/v1/extractions?select=id&limit=1`, 15s timeout), and structured secret-free logging.
2. **Dedicated Workflow**: `.github/workflows/staging_supabase_keep_alive.yml` running on UTC cron `17 0,8,16 * * *` (3 times daily) and `workflow_dispatch`, with bounded 5-minute timeout and minimal `contents: read` permissions.
3. **Isolated Test Suite**: `tests/test_staging_supabase_keep_alive.py` with 22 comprehensive mocked unit tests verifying all edge cases and asserting that Production keep-alive files remain untouched.
4. **Architectural & Disaster Recovery Distinction**:
   - Documented in `DISASTER_RECOVERY.md` Runbook 27 that keep-alive activity probing is an operational dormancy risk mitigation, **NOT** a disaster recovery or backup tool.
   - Probing reduces pause risk by generating ordinary API/database traffic, but does not guarantee that Supabase will never pause a Free-tier project under its platform policies.
   - True disaster recovery requires canonical migration replay (`Runbook 26 Step 3`) and independent encrypted logical backups (`Runbook 26 Step 4`).
   - Documented step-by-step unpause runbook in `DISASTER_RECOVERY.md`.
5. **Scheduled Workflow Platform Invariant**:
   - Documented that GitHub Actions scheduled workflows (`schedule` trigger) only run from the repository's **default branch**. Adding the workflow on `Dev` or `staging` enables manual `workflow_dispatch` testing, but background automation takes effect post-promotion to default branch.

### Accepted Trade-Offs
* The workflow requires two repository secrets (`SUPABASE_STAGING_URL` and `SUPABASE_STAGING_ANON_KEY`) to be provisioned before live runs can succeed; without them, the job fails closed safely.
* Scheduled runs will not execute automatically on `Dev` or `staging` branches prior to merge into the default branch per GitHub Actions platform rules.
* Probing generates legitimate PostgREST traffic to reset the inactivity timer, but cannot prevent platform-level pauses or maintenance outages executed by Supabase.
