# 🛡️ Agent Engineering Rules & Repository Constraints — Universal Pro AI

## 1. Test Suite Integrity & Regression Protection (Strict Owner Directive)
- **Zero Modification/Deletion of Existing Tests**: You must NEVER modify, edit, comment out, or delete any existing test cases or test files in the `tests/` directory.
- **Owner Approval Required**: Any change targeting an existing test case (including assertions, parameters, or test signatures) requires **explicit prior sign-off from the repository owner**.
- **Adding New Tests**: As features expand, you are encouraged to add *new* test cases by creating dedicated test files (e.g., `tests/test_sprintX_*.py`) or appending new, non-destructive test methods.
- **Regression Contract**: Existing tests serve as an immutable specification contract ensuring zero regressions against prior sprint deliverables.

## 2. Sprint Governance, 3-Layered Architecture & PO Production Gate
- **Strict 3-Layered Environment Isolation**:
  1. *Layer 1: Development (`Dev` branch)*: Local sandbox, unit tests (`pytest`), local Next.js builds. Never deploy directly to cloud from Dev.
  2. *Layer 2: Staging (`staging` branch)*: Vercel Preview deployments and Staging cloud containers. All feature additions, bug fixes, and manual verifications MUST deploy here first for PO review.
  3. *Layer 3: Production (`main` branch)*: `universal-pro-ai.vercel.app` and Production OCI containers.
- **Zero Direct-to-Production Rule (Strict Gate)**: Agents must NEVER push, merge, or fast-forward changes directly to `main` or deploy directly to production containers without **explicit, written prior sign-off from the repository owner / Product Owner**. Hotfixes and patches are subject to this exact same constraint.
- **Sign-Off Cadence**: At the end of every sprint or major feature milestone, prepare a comprehensive **Product Owner UI/UX Feature Showcase & Feedback Review** document. Wait for explicit PO approval before promoting from `staging` to `main`.
- **Step-by-Step Staging Promotion Rule**: Upon completing and verifying any step of the UX/Architectural Enhancement Roadmap (e.g., Step 1, Step 2, Step 3, Step 4), all implemented changes MUST immediately be pushed and promoted to the `staging` branch (Layer 2) for Vercel Preview & Staging validation before moving on to subsequent roadmap steps.
- **Vercel Staging Protection Bypass Protocol**: When running browser subagents, QA crawlers, or automated visual E2E tests against Vercel Preview/Staging deployments, agents MUST navigate via Option A URL query parameters (`?x-vercel-protection-bypass=<secret>&x-vercel-set-bypass-cookie=samesitenone`) to set the `_vercel_jwt` cookie on Vercel Edge for all downstream script, asset, and API fetch requests.

## 3. Monetization Invariants & Affiliate Parameter Protection (Revenue Shield)
- **Immutable Affiliate Identifiers**: The default monetization parameters (`tag=manasdas11155-21` for Amazon India and `r=5608766` for EarnKaro) are **immutable constants**. Under no circumstances should these be deleted, mocked, or altered in production paths.
- **Strict URL Encoding**: All search queries passed to e-commerce and quick-commerce partners (Amazon, Flipkart, Blinkit, Zepto, Instamart, JioMart) MUST use explicit URL encoding (`urllib.parse.quote_plus`). Agents must never generate raw unencoded query strings.
- **Domain-Affiliate Separation**: Affiliate logic must live exclusively within `backend/app/services/affiliate_engine.py`. Agents must never hardcode store links or affiliate tags inside AI prompt strings or UI presentation components.

## 4. Ingestion Guardrails & Cloud Cost Protection (Hard Ceilings)
- **Duration Cap (`MAX_VIDEO_DURATION = 90`)**: Agents must NEVER raise or remove the 90-second duration ceiling without explicit owner approval. Videos exceeding 90 seconds must fail immediately before media download.
- **Resolution Cap (360p Max)**: Media downloaders must strictly enforce `bestvideo[height<=360]+bestaudio/best[height<=360]`. Never configure `yt-dlp` to pull 720p, 1080p, or unconstrained streams.
- **Deterministic Disk Cleanup (`try...finally`)**: Any media download, frame slice, or temporary audio chunk created on disk MUST be deleted in an unskippable `finally:` block. Never leave orphaned `.mp4` or `.mp3` files in `/tmp` or local workspace directories.
- **Cache-First Bypass Guardrail**: The worker pipeline MUST query Supabase for an existing SHA-256 URL hash *before* initiating any proxy download or Gemini API call. Never trigger redundant AI inference on an already extracted URL.

## 5. Architectural Invariants & Cross-Platform Compatibility
- **Dual-Mode Dispatcher Preservation**: The backend must run in both:
  1. *Distributed Mode*: Celery + Upstash Redis (Production / Staging).
  2. *In-Memory Fallback Mode*: FastAPI `BackgroundTasks` (Local dev without Redis).
  Agents must NEVER remove the fallback dispatcher or assume Redis is always reachable.
- **Windows Worker Compatibility**: Any automation script running Celery workers (e.g., `scripts/run_worker.py`) must dynamically detect Windows OS and apply `--pool=solo` or `--pool=threads`. Never write Celery execution commands that depend on Unix `fork()`.
- **Stateless Web Layer**: Never store video blobs, session states, or extraction caches in memory inside the FastAPI app container. All state must live in Redis, Supabase, or ephemeral disk with immediate cleanup.

## 6. Secret Hygiene & Security Isolation
- **Zero Hardcoded Secrets**: Never commit, hardcode, or log API keys, proxy credentials, Supabase service roles, or webhook tokens in code or test fixtures. All secrets must resolve through `app.core.config.Settings` from environment variables.
- **Admin Parameter Isolation**: The Admin Vault (`?admin=1`) and developer latency telemetry cards must remain isolated from standard user responses. Never expose raw infrastructure metrics (cloud prep time, proxy latency, token counts) on public consumer endpoints.

## 7. UI/UX Performance Contract
- **Sub-3s Turnaround Contract**: Any changes to the ingestion or inference pipeline must preserve our core benchmark (<1.5s first-paint video preview, <3s completed structured extraction).
- **Single Docked Video Player**: Never duplicate HTML5 `<video>` player elements on the screen. The media preview player must remain single-docked to prevent duplicate audio tracks and mobile viewport collisions.

## 8. Gemini Model Lifecycle & Deprecation Governance
- **Catalog Alignment**: Continuously monitor Google Gemini's official model catalog (https://ai.google.dev/gemini-api/docs/models).
- **Proactive Pruning of Deprecated Endpoints**: As soon as any model endpoint is marked shutdown or deprecated by Google (e.g., `gemini-2.0-flash`, `gemini-2.0-flash-lite`), agents must promptly prune it from `preferred_candidates` across `gemini_processor.py`, `ai_router.py`, and `app.py` to prevent wasted retry cycles and 404/410 latency spikes.
- **Flagship Alignment**: The primary dispatch model should always point to Google's latest stable production Flash model (currently `gemini-3.8-flash`), followed by high-reliability fallbacks (`gemini-3.7-flash`, `gemini-3.5-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`), before external provider failover.

## 9. Mandatory 3-Core Document Governance Contract (Immutable Rule)
- **Living Documentation Requirement**: Whenever any feature, bug fix, architectural change, or roadmap step is built or modified, agents MUST update and maintain the following 3 core living documents without exception:
  1. **`docs/TROUBLESHOOTING.md`**: Log every encountered error/bug, root cause, exact code resolution diffs, and verification steps.
  2. **`docs/po-governance/PRODUCT_OWNER_UX_SHOWCASE.md`** (and sprint showcases under `docs/po-governance/showcases/SPRINT_X_PO_SHOWCASE.md`): Maintain product strategy, user impact, architecture diagrams, UI visual showcases, and PO review sign-off checklists.
  3. **`docs/architecture/DISASTER_RECOVERY.md`**: Maintain system architecture inventory, active endpoints, cloud failure modes, emergency failovers, and step-by-step DR runbooks.
- **Canonical Folder Hierarchy**:
  - `docs/architecture/`: Infrastructure, cloud deployment specs (`ENVIRONMENTS.md`, `ORACLE_CLOUD_DEPLOYMENT.md`, `ROADMAP_AND_STRATEGY.md`).
  - `docs/po-governance/`: Product directives, backlogs (`JIRA_BACKLOG.md`), test specs (`TEST_CASES.md`), and sprint showcases (`showcases/`).
  - `docs/qa-reports/` & `docs/ui-ux-audits/`: Automated E2E QA reports and visual inspection logs.
  - `backend/database/`: Supabase SQL schemas and migration scripts.
- **Verification Rule**: No feature implementation or bug fix is considered complete until all 3 living documents reflect the updated state of the codebase.

## 10. Multi-LLM Council Consensus & Latency SLA Guardrail
- **Single-Pass Sub-3s Default**: The default extraction pipeline for all web, Telegram, WhatsApp, and API requests MUST remain the fast, single-pass `gemini-3.8-flash` engine to satisfy our core turnaround SLA (<2.4s).
- **Council Mode Invariant**: The 3-Stage Multi-LLM Council Consensus Engine (Gemini + Groq Llama 3.3 + Mistral) must NEVER be configured as the default execution pipeline. It must strictly remain an explicit opt-in selection or an internal fallback retry mechanism.
- **Provider Key Isolation**: Council execution must degrade gracefully if secondary provider keys (`GROQ_API_KEY`, `MISTRAL_API_KEY`) are missing, falling back to single-provider execution without throwing 500 errors.

## 11. Schema Backward Compatibility & Historical Cache Defense
- **Zero Breaking Assumptions on `structured_data`**: The Supabase `extractions` table contains historical records from earlier sprints that lack newer schema keys (e.g., `nutrition_per_serving`, `equipment_needed`, `google_maps_locations`, `audio_song`).
- **Mandatory Optional Types & Null Guards**: All newly introduced JSON fields must be defined as optional (`field?: Type`) in TypeScript interfaces. Frontend components must strictly use optional chaining (`data.nutrition?.calories`) and default fallbacks. Agents must never assume a database record contains newly invented schema fields.
- **Single-Inference Extraction Schema**: New domain properties (such as nutritional macros) must be incorporated directly into the primary Gemini JSON schema prompt. Agents must NEVER trigger secondary round-trip LLM calls to fetch supplementary metadata for an already extracted video.

## 12. Mobile In-App Browser & Web API Progressive Enhancement
- **Strict Feature Detection**: Advanced browser APIs (`navigator.wakeLock`, `AudioContext`, `navigator.clipboard`, `navigator.vibrate`) are heavily restricted or unsupported inside mobile in-app webviews (Instagram WKWebView, WhatsApp browser, Telegram webview).
- **Mandatory Defensive Wrappers**:
  - `wakeLock.request('screen')` must always be wrapped in a defensive try/catch block, catching `NotAllowedError` silently without breaking UI state.
  - Timers must calculate remaining duration using target epoch timestamp deltas (`targetTime - Date.now()`), never raw `setInterval` decrements which freeze under mobile OS background tab throttling.
  - Audio chimes must initialize and pre-unlock on an explicit user gesture tick before playing programmatically.
  - Clipboard operations must implement an `execCommand('copy')` textarea fallback for legacy webviews.

## 13. Regional & Hinglish Culinary Prompt Invariants
- **Prompt Preservation**: System prompts in `backend/app/services/gemini_processor.py` and `multimodal.py` contain tuned culinary rules for South Asian and Hinglish terminology. Agents must NEVER delete, overwrite, or simplify these rules during prompt refactoring.
- **Mandatory Linguistic Mappings**:
  - Spoken metrics must always translate to standardized units while preserving native terms in parentheses: *1 katori* $\rightarrow$ *1 cup (~150g)*, *1 chamach* $\rightarrow$ *1 tbsp*, *chutki bhar* $\rightarrow$ *pinch*.
  - Native ingredient names must be preserved in parentheses: e.g., *Cumin seeds (Jeera)*, *Asafoetida (Hing)*, *Dried Fenugreek (Kasuri Methi)*.
  - Quick-commerce link builders must prioritize the colloquial Indian spice name to ensure accurate search indexing on Blinkit and Zepto.
