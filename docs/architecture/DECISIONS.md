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
