# 🛡️ Agent Engineering Rules & Repository Constraints — Universal Pro AI

## 1. Test Suite Integrity & Regression Protection (Strict Owner Directive)
- **Zero Modification/Deletion of Existing Tests**: You must NEVER modify, edit, comment out, or delete any existing test cases or test files in the `tests/` directory.
- **Owner Approval Required**: Any change targeting an existing test case (including assertions, parameters, or test signatures) requires **explicit prior sign-off from the repository owner**.
- **Adding New Tests**: As features expand, you are encouraged to add *new* test cases by creating dedicated test files (e.g., `tests/test_sprintX_*.py`) or appending new, non-destructive test methods.
- **Regression Contract**: Existing tests serve as an immutable specification contract ensuring zero regressions against prior sprint deliverables.

## 2. Sprint Governance & PO Sign-Off Cadence
- At the end of every sprint, prepare a comprehensive **Product Owner UI/UX Feature Showcase & Feedback Review** document with screenshots, user flows, and a sign-off scorecard.
- Wait for the PO sign-off and address any P0 acceptance tweaks before officially kicking off the next sprint.

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
