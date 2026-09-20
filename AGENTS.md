# 🛡️ Agent Engineering Rules & Repository Constraints — Universal Pro AI

## 1. Test Suite Integrity & Regression Protection (Strict Owner Directive)
- **Zero Modification/Deletion of Existing Tests**: You must NEVER modify, edit, comment out, or delete any existing test cases or test files in the `tests/` directory or frontend test directories (`frontend/src/**/__tests__`).
- **Owner Approval Required**: Any change targeting an existing test case (including assertions, parameters, or test signatures) requires **explicit prior sign-off from the repository owner**.
- **Adding New Tests**: As features expand, you are encouraged to add *new* test cases by creating dedicated test files (e.g., `tests/test_sprintX_*.py`, `frontend/src/**/__tests__/*.test.ts`) or appending new, non-destructive test methods.
- **CODEOWNERS Protection**: Maintain CODEOWNERS entries for `tests/`, `AGENTS.md`, `backend/app/services/affiliate_engine.py`, `backend/app/services/url_validator.py`, and `backend/app/core/security.py`.
- **Regression Contract**: Existing tests serve as an immutable specification contract ensuring zero regressions against prior sprint deliverables.

## 2. Sprint Governance, 3-Layered Architecture & PO Production Gate
- **Strict 3-Layered Environment Isolation**:
  1. *Layer 1: Development (`Dev` branch)*: Local sandbox, unit tests (`pytest`), local Next.js builds. Never deploy directly to cloud from Dev.
  2. *Layer 2: Staging (`staging` branch)*: Vercel Preview deployments and Staging cloud containers. All feature additions, bug fixes, and manual verifications MUST deploy here first for PO review.
  3. *Layer 3: Production (`main` branch)*: `universal-pro-ai.vercel.app` and Production OCI containers.
- **Zero Direct-to-Production Rule (Strict Gate)**: Agents must NEVER push, merge, or fast-forward changes directly to `main` or deploy directly to production containers without **explicit, written prior sign-off from the repository owner / Product Owner**. Hotfixes and patches are subject to this exact same constraint.
- **Hotfix Fast Path**: Hotfixes must be owner-approved, deployed to staging, and smoke-tested first before any production promotion.
- **PO Sign-Off & Verdict Protection**: Agents MUST NEVER fill in PO verdicts, checkboxes, or sign-off lines in documentation or PRs (leave as "Pending PO"). Product Owner sign-off is recorded exclusively by the repository owner via PR approval or explicit entries in `docs/po-governance/SIGN_OFF.md` written by the owner.
- **Step-by-Step Staging Promotion Rule**: Upon completing and verifying any step of the UX/Architectural Enhancement Roadmap, all implemented changes MUST immediately be pushed and promoted to the `staging` branch (Layer 2) for Vercel Preview & Staging validation before moving on to subsequent roadmap steps.
- **Vercel Staging Protection Bypass Protocol**: When running browser subagents, QA crawlers, or automated visual E2E tests against Vercel Preview/Staging deployments, prefer sending the Vercel bypass secret as an HTTP header (`x-vercel-protection-bypass`). Never commit or log the secret. When using URL query parameters (`?x-vercel-protection-bypass=<secret>&x-vercel-set-bypass-cookie=samesitenone`), never output the raw secret in logs.

## 3. Monetization Invariants & Affiliate Parameter Protection (Revenue Shield)
- **Immutable Affiliate Identifiers**: The default monetization parameters (`tag=manasdas11155-21` for Amazon India and `r=5608766` for EarnKaro) are **immutable constants**. Under no circumstances should these be deleted, mocked, or altered in production paths.
- **Strict URL Encoding**: All search queries passed to e-commerce and quick-commerce partners (Amazon, Flipkart, Blinkit, Zepto, Instamart, JioMart) MUST use explicit URL encoding (`urllib.parse.quote_plus`). Agents must never generate raw unencoded query strings.
- **Domain-Affiliate Separation**: Affiliate logic must live exclusively within `backend/app/services/affiliate_engine.py`. Agents must never hardcode store links or affiliate tags inside AI prompt strings or UI presentation components.
- **Affiliate Disclosures & Channel Governance**: All affiliate links must be accompanied by the required statutory disclosure text. The owner must review affiliate program terms for links sent via chat messages (Telegram, WhatsApp) and `.txt` exports.
- **Creator Tag Vault Status**: The Creator Tag Vault feature remains hidden during initial launch.

## 4. Ingestion Guardrails & Cloud Cost Protection (Hard Ceilings)
- **Duration Cap (`MAX_VIDEO_DURATION = 90`)**: Agents must NEVER raise or remove the 90-second duration ceiling without explicit owner approval. Videos exceeding 90 seconds must fail immediately before media download. If duration metadata is missing, fail closed.
- **Resolution Cap (360p Max) & Format String**: Media downloaders must strictly enforce `bestvideo[height<=360]+bestaudio/best[height<=360]` (no bare `/best` fallback), with `max_filesize` set. A dedicated unit test MUST assert this exact format string. Resolution or duration cap changes are permitted only via owner-approved experiments with measured accuracy.
- **Deterministic Disk Cleanup (`try...finally`)**: Any media download, frame slice, or temporary audio chunk created on disk MUST be deleted in an unskippable `finally:` block. Never leave orphaned `.mp4` or `.mp3` files in `/tmp` or local workspace directories.
- **Canonical Cache-First Bypass Guardrail**: The worker pipeline MUST query Supabase for an existing cache record using the SHA-256 hash of canonical `(platform, video_id)` (not the raw URL) *before* initiating any proxy download or Gemini API call. Never trigger redundant AI inference on an already extracted URL.

## 5. Architectural Invariants & Cross-Platform Compatibility
- **Dual-Mode Dispatcher Preservation**: The backend must run in both:
  1. *Distributed Mode*: Celery + Upstash Redis (Production / Staging).
  2. *In-Memory Fallback Mode*: FastAPI `BackgroundTasks` (Local dev without Redis).
  Agents must NEVER remove the fallback dispatcher or assume Redis is always reachable.
- **Windows Worker Compatibility**: Any automation script running Celery workers (e.g., `scripts/run_worker.py`) must dynamically detect Windows OS and apply `--pool=solo` or `--pool=threads`. Never write Celery execution commands that depend on Unix `fork()`.
- **Stateless Web Layer**: Never store video blobs, session states, or extraction caches in memory inside the FastAPI app container. All state must live in Redis, Supabase, or ephemeral disk with immediate cleanup.

## 6. Secret Hygiene & Security Isolation
- **Zero Hardcoded Secrets**: Never commit, hardcode, or log API keys, proxy credentials, Supabase service roles, or webhook tokens in code or test fixtures. All secrets must resolve through `app.core.config.Settings` from environment variables.
- **Server-Side Admin Auth & Parameter Isolation**: Admin features require server-side authentication (`X-Admin-Api-Key` header or `role == 'admin'`). NEVER gate anything with a URL parameter such as `?admin=1`. Developer telemetry must remain isolated from standard user responses. Never expose raw infrastructure metrics or admin keys in client bundles.

## 7. Unified Measurable SLA & Single Video Player Contract
- **Unified Telemetry SLA Contract**: Extraction turnaround targets are strictly governed by p50 and p95 benchmarks tracked via backend telemetry, split by cached vs non-cached requests and by platform (Instagram, YouTube, TikTok). The repository owner sets the target benchmark numbers. UI components and documentation may cite ONLY empirically measured figures.
- **Single Docked Video Player**: Never duplicate HTML5 `<video>` player elements on the screen. The media preview player must remain single-docked to prevent duplicate audio tracks and mobile viewport collisions.
- **Council Mode Invariant**: The 3-Stage Multi-LLM Council Consensus Engine (Gemini + Groq Llama 3.3 + Mistral) must NEVER be configured as the default execution pipeline. It must strictly remain an explicit opt-in selection or an internal fallback retry mechanism.
- **Provider Key Isolation**: Council execution must degrade gracefully if secondary provider keys (`GROQ_API_KEY`, `MISTRAL_API_KEY`) are missing, falling back to single-provider execution without throwing 500 errors.

## 8. Gemini Model Lifecycle & Deprecation Governance
- **Centralized Model Configuration**: Model IDs live strictly in `app.core.config.Settings` as the single source of truth, never scattered across multiple backend files.
- **Startup Check**: Startup catalog validation (`list-models`) must be warn-only and never block application startup.
- **Primary Model Transition Protocol**: Switching the primary model requires running a golden-set test suite (Hinglish reels, text-overlay reels) with measured benchmark results attached.
- **Explicit Thinking Level & Cost Governance**: Set the thinking level explicitly (start with `low`) and log inference latency and token cost per request. Note that introductory API pricing may end at year-end; continuously review cost assumptions.
- **Catalog Alignment**: Continuously monitor Google Gemini's official model catalog (https://ai.google.dev/gemini-api/docs/models). As soon as any model endpoint is marked shutdown or deprecated by Google, agents must promptly prune it from `Settings` to prevent 404/410 latency spikes.

## 9. Mandatory 4-Core Document Governance Contract & Measured Metrics
- **Living Documentation Requirement**: Whenever any feature, bug fix, architectural change, or roadmap step is built or modified, agents MUST update and maintain the following 4 core living documents without exception:
  1. **`docs/TROUBLESHOOTING.md`**: Log every encountered error/bug, root cause, exact code resolution diffs, and verification steps.
  2. **`docs/po-governance/PRODUCT_OWNER_UX_SHOWCASE.md`**: Maintain product strategy, user impact, architecture diagrams, UI visual showcases, and PO review sign-off checklists.
  3. **`docs/architecture/DISASTER_RECOVERY.md`**: Maintain system architecture inventory, active endpoints, cloud failure modes, emergency failovers, and step-by-step DR runbooks.
  4. **`docs/USER_MANUAL.md`**: Maintain end-to-end user manual and feature guide explaining how to use all features.
- **Automated & Measured Metrics**: Metrics (test counts, latency, throughput) must be generated directly from CI outputs or telemetry data, never typed manually by agents. Every numerical figure in documentation must be explicitly labeled as **[MEASURED]** or **[ESTIMATED]**.
- **Verification Rule**: No feature implementation or bug fix is considered complete until all 4 living documents reflect the updated state of the codebase.

## 10. Schema Backward Compatibility, Schema Versioning & Cache Defense
- **Zero Breaking Assumptions on `structured_data`**: The Supabase `extractions` table contains historical records from earlier sprints that lack newer schema keys.
- **Schema Versioning (`schema_version`)**: All newly generated `structured_data` payloads MUST include a top-level `schema_version` field (e.g., `schema_version: 1`) to enable seamless future re-hydration, cache invalidation, and data migrations.
- **Mandatory Optional Types & Null Guards**: All newly introduced JSON fields must be defined as optional (`field?: Type`) in TypeScript interfaces. Frontend components must strictly use optional chaining (`data.nutrition?.calories`) and default fallbacks.
- **Single-Inference Extraction Schema**: New domain properties must be incorporated directly into the primary Gemini JSON schema prompt. Agents must NEVER trigger secondary round-trip LLM calls to fetch supplementary metadata for an already extracted video.

## 11. Mobile In-App Browser & Web API Progressive Enhancement
- **Strict Feature Detection**: Advanced browser APIs (`navigator.wakeLock`, `AudioContext`, `navigator.clipboard`, `navigator.vibrate`) are heavily restricted or unsupported inside mobile in-app webviews (Instagram WKWebView, WhatsApp browser, Telegram webview).
- **Mandatory Defensive Wrappers**:
  - `wakeLock.request('screen')` must always be wrapped in a defensive try/catch block, catching `NotAllowedError` silently without breaking UI state.
  - Timers must calculate remaining duration using target epoch timestamp deltas (`targetTime - Date.now()`), never raw `setInterval` decrements which freeze under mobile OS background tab throttling.
  - Audio chimes must initialize and pre-unlock on an explicit user gesture tick before playing programmatically.
  - Clipboard operations must implement an `execCommand('copy')` textarea fallback for legacy webviews.

## 12. Regional & Hinglish Culinary Prompt Invariants
- **Prompt Preservation**: System prompts in `backend/app/services/gemini_processor.py` contain tuned culinary rules for South Asian and Hinglish terminology. Agents must NEVER delete, overwrite, or simplify these rules during prompt refactoring.
- **Mandatory Linguistic Mappings & Approximate Conversions**:
  - Spoken metrics must always translate to standardized units labeled as approximate while preserving native terms in parentheses: e.g., *1 katori* $\rightarrow$ *1 bowl (~150g, approx)* (do NOT label a katori as "1 cup"), *1 chamach* $\rightarrow$ *1 tbsp (approx)*, *chutki bhar* $\rightarrow$ *pinch*.
  - Native ingredient names must be preserved in parentheses: e.g., *Cumin seeds (Jeera)*, *Asafoetida (Hing)*, *Dried Fenugreek (Kasuri Methi)*.
  - Quick-commerce link builders must prioritize the colloquial Indian spice name to ensure accurate search indexing on Blinkit and Zepto.
- **Snapshot Test Requirement**: A dedicated snapshot unit test MUST assert that Hinglish prompt rules and culinary mappings exist in system prompt templates.

## 13. Security Invariants
- **Strict URL Validation Order**: Every user-supplied or remote-derived URL MUST pass through `backend/app/services/url_validator.py` (enforcing HTTPS only, domain allowlist, SSRF/IP checks, redirect re-validation after every hop up to max 3) BEFORE cache lookup, media download, or remote fetch. Execution order MUST be: `validate` $\rightarrow$ `cache lookup` $\rightarrow$ `download` $\rightarrow$ `inference`. No entry point (Telegram/WhatsApp bots, webhooks, `/share-target`, worker tasks) may bypass this order.
- **Signed Stream Proxy Tokens**: `/stream-video` accepts ONLY signed, short-lived HMAC tokens minted at payload serialization time. Stream tokens must NEVER be saved in Supabase cache or stored in the Vault.
- **Fail-Closed Secrets & Signature Verification**: Webhook and admin secrets must fail closed if unset, using `hmac.compare_digest` for comparison. WhatsApp webhook signatures MUST be verified over the raw request payload body before parsing JSON.
- **Environment Secret Enforcement**: Define development behavior explicitly (`APP_ENV=development`). Staging and Production environments MUST refuse to start if a required secret is missing, logging only the environment variable NAME.
- **Server-Side Admin Authentication**: Admin features require server-side authentication (`X-Admin-Api-Key` header or `role == 'admin'`). NEVER gate anything with a URL query parameter such as `?admin=1`. Never ship admin keys or service roles in client bundles.
- **Allowlisted Merchant Redirects**: E-commerce and quick-commerce redirect endpoints (`/api/v1/affiliate/redirect`) MUST allow only allowlisted HTTPS merchant hosts and reject all external or open-redirect URLs.
- **Log Privacy & Secret Hygiene**: Never log secrets, API keys, tokens, phone numbers, or full user URLs in application logs or telemetry.
- **Dependency Audit Compliance**: Dependency changes must be declared in `requirements.txt` / `package.json` and lockfiles (`package-lock.json`), followed immediately by running `pip-audit` (against requirements) and `npm audit`.

## 14. Frontend Design System and Accessibility
- **Design System Tokens & Contrast**: No hardcoded colors in UI components; all styling must use CSS design tokens from `globals.css` supporting both Light and Dark themes. Text contrast MUST achieve WCAG AA Compliance ($\ge 4.5:1$). Verify visual contrast in both themes at 375px (mobile) and 1280px (desktop) viewports.
- **Input & Touch Accessibility**: All input fields must enforce `font-size >= 16px` (prevents iOS Safari auto-zoom), touch targets must meet `min-height: 44px` / `min-width: 44px`, visible or `sr-only` `<label>` elements must exist on all controls, and `:focus-visible` outlines must be clearly styled for keyboard navigation.
- **Modal & Sheet Focus Management**: All modals, drawers, and bottom sheets must implement `role="dialog"`, `aria-modal="true"`, focus trapping, `Escape` key dismissal, and focus restoration to the triggering element upon closing.
- **Motion & Visual Performance**: Parallax effects and particle canvas backgrounds are forbidden. `backdrop-filter` is permitted ONLY on the sticky header. The `@media (prefers-reduced-motion: reduce)` block must cover every remaining animation and transition in the application.
- **Action Hierarchy**: Render exactly ONE primary action per result domain (Recipe: *"Shop ingredients"*, Travel: *"Open in Google Maps"*, Product: *"Buy"*, Tutorial: *"Open resources"*). All secondary and utility actions must be contained within the overflow bottom sheet / menu.

## 15. Evidence and Definition of Done
- **Empirical Evidence Requirement**: Every "verified", "passing", or "score" claim in pull requests, commits, and documentation MUST include exact command execution output or measured values. Unmeasured scores or speculative benchmarks in docs are forbidden.
- **Complete Verification Pipeline**: Every code change requires executing `npx tsc --noEmit`, `npm run lint`, `npm test`, `npm run build`, and `pytest tests/`, with all checks clean green and output attached. Any known test failure BLOCKS promotion to `staging` unless the repository owner explicitly accepts it in writing.
- **Governance Contract**: Agents must NEVER modify `AGENTS.md` without explicit, prior approval from the repository owner.
