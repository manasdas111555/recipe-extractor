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
| **Sprint 1** | **Core Decoupling & Multi-Tenant Data Layer** (Supabase + FastAPI) | 26 pts | 🎉 **COMPLETED (100%)** | Weeks 1–2 |
| **Sprint 2** | **Async Worker Pipeline & Scraper Resilience** (Celery + Redis + Proxies) | 34 pts | 🎉 **COMPLETED (100%)** | Weeks 3–4 |
| **Sprint 3** | **Zero-Friction Chat Ingestion Bot** (Telegram & WhatsApp Cloud API) | 29 pts | 🎉 **COMPLETED (100%)** | Weeks 5–6 |
| **Sprint 4** | **Next.js 15 PWA & Personal Vault** (Web Share Sheet + UI Dashboard) | 37 pts | 🎉 **COMPLETED (100%)** | Weeks 7–8 |
| **Sprint 5** | **SaaS Monetization & Quota Engine** (Razorpay + Stripe Dual-Rail Billing) | 28 pts | 🎉 **COMPLETED (100%)** | Weeks 9–10 |
| **Sprint 6** | **Creator Program & SEO Ingestion Engine** (Custom Tags + SSR Pages) | 21 pts | 🎉 **COMPLETED (100%)** | Weeks 11–12 |
| **Sprint 7** | **UX Polish, One-Click Activation & Model Resilience** (Title Filter + Sample Chips) | 23 pts | 🎉 **COMPLETED (100%)** | Weeks 13–14 |
| **Sprint 8** | **Impeccable UI/UX Refinement, Accessibility & Motion Engine** (Contrast + Ghost-Card Cleanup + Reduced Motion) | 24 pts | 🎉 **COMPLETED (100%)** | Weeks 15–16 |
| **Sprint 9** | **Friends & Family Beta Rollout, Hinglish Culinary Engine & Observability** (Phase 0 - Phase 5) | 38 pts | 🎉 **COMPLETED (100%)** | Weeks 17–18 |
| **Sprint 10** | **Beta Testing Feedback, Resilient Ingestion & Multilingual AI Engine** (Downloader Fallback + Song ID + Language Toggle + Travel Maps + Vault Fix + Mobile UX + Recipe Formatting) | 46 pts | 🎉 **COMPLETED (100%)** | Weeks 19–20 |
| **Sprint 11** | **Security, Accessibility & Governance Hardening** (TRUSTED_PROXY + Egress Firewall + IP Pinning SNI + Vault Re-hydration Rate Limit + Rule 17 Contract) | 42 pts | 🧪 **Ready for PO Review** | Weeks 21–22 |
| **Sprint 12** | **Security, Secret Hygiene & Egress Refinement** (JWT Signature Verification + Stream Proxy Token + Trusted Proxy IP + Egress Firewall + Pinned Connection + Lockfile) | 58 pts | 📋 **Planned** | Weeks 23–24 |
| **Sprint 13** | **AI Failover, Administrative Access Hardening & Universal Routing Architecture** (AI Provider Runtime Failover & Canonical Schema + Private Staging Admin Access + Reverse Proxy & Route Validation) | TBD | 📋 **Planned** | Weeks 25–26 |

---

## 🛡️ AGENTS.md Engineering Rules Compliance Matrix

| Rule ID | Rule Title | Compliance Status | Verification Evidence (Exact File:Line / Command Output) |
| :--- | :--- | :--- | :--- |
| **Rule 1** | Test Suite Integrity & Regression Protection | 🟠 **PARTIAL** | `.github/CODEOWNERS:4` created; 211 pytest + 9 vitest tests passing; GitHub branch protection pending owner setup |
| **Rule 2** | Sprint Governance, 3-Layered Architecture & PO Gate | 🟡 **NOT YET** | PO sign-off log `docs/po-governance/SIGN_OFF.md` pending creation by repository owner |
| **Rule 3** | Monetization Invariants & Affiliate Parameter Protection | 🟡 **NOT YET** | Statutory disclosure text implementation & owner review of affiliate terms for chat/export pending |
| **Rule 4** | Ingestion Guardrails & Cloud Cost Protection | 🟡 **NOT YET** | Exact `bestvideo[height<=360]+bestaudio/best[height<=360]` format test, missing duration fail-closed, and SHA-256 canonical `(platform, video_id)` cache key pending |
| **Rule 5** | Architectural Invariants & Cross-Platform Compatibility | 🟢 **COMPLIANT** | `backend/app/workers/tasks.py:15` (`@celery_app.task`); `scripts/run_worker.py:22` (`--pool=solo` Windows detection) |
| **Rule 6** | Secret Hygiene & Security Isolation | 🟢 **COMPLIANT** | `backend/app/core/config.py:35` (`Settings` Pydantic env loader); `backend/app/core/security.py:162` (`X-Admin-Api-Key` server auth) |
| **Rule 7** | Unified Measurable SLA & Performance Benchmark | 🟡 **NOT YET** | Backend telemetry p50/p95 benchmarks by cached vs non-cached and platform (IG, YT, TikTok) being aggregated |
| **Rule 8** | Gemini Model Lifecycle & Deprecation Governance | 🟡 **NOT YET** | Model IDs in `Settings`, startup list-models check, thinking level (`start with low`), and golden-set transition suite pending |
| **Rule 9** | Mandatory 4-Core Document Governance Contract | 🟠 **PARTIAL** | 4 living docs updated: `docs/TROUBLESHOOTING.md` (ISSUE-046 added), `docs/po-governance/PRODUCT_OWNER_UX_SHOWCASE.md` (pre-marked PO rows preserved for owner review), `docs/architecture/DISASTER_RECOVERY.md` (egress ports & TRUSTED_PROXY updated), `docs/USER_MANUAL.md` (Vault rehydration updated) |
| **Rule 10** | Multi-LLM Council Consensus Engine Invariants | 🟢 **COMPLIANT** | `backend/app/services/llm_council.py:22` (opt-in selection / fallback retry, missing secondary key graceful degradation) |
| **Rule 11** | Schema Versioning & Cache Defense | 🟡 **NOT YET** | Top-level `schema_version` field in `structured_data` to be populated across Gemini JSON schema prompts |
| **Rule 12** | Mobile In-App Browser & Progressive Enhancement | 🟢 **COMPLIANT** | `useWakeLock.ts:32` (`navigator.wakeLock.request('screen')` try/catch); `useStepTimer.ts:94` (`targetEndTimeRef.current - Date.now()`); `useStepTimer.ts:42` (Web Audio API pre-unlock); `CopyShoppingChecklist.tsx:62` (`execCommand('copy')` fallback) |
| **Rule 13** | Regional & Hinglish Culinary Prompt Invariants | 🟢 **COMPLIANT** | System prompt snapshots labeled `[ILLUSTRATIVE]`; live Hinglish golden-set transition benchmark `[NOT VERIFIED]` pending live API run; `gemini_processor.py:36` prompt template preserved; `tests/test_hinglish_prompt_snapshot.py:21` (1 passed); `scalingEngine.test.ts` (Rule 13 2x volume scaling passed) |
| **Rule 14** | Security Invariants | 🟠 **PARTIAL** | `url_validator.py:42` (SSRF/IP checks rejecting non-global IP answers, max 3 redirects, IP pinning with Host/SNI preserved); `config.py:23` (`TRUSTED_PROXY=False` default & spoof test passed); `/api/v1/library/rehydrate` (Redis 30 req/min rate limit passed); `deploy/setup_egress_firewall.sh` created (`scripts/verify_egress.py` NOT VERIFIED until container execution); pending staging promotion |
| **Rule 15** | Frontend Design System & Accessibility | 🟡 **NOT YET** | CSS design tokens & ARIA bottom sheet (`OverflowBottomSheet.tsx`) active; Lighthouse & axe automated accessibility audit outputs to be attached |
| **Rule 16** | Evidence and Definition of Done | 🟢 **COMPLIANT** | 5-step verification pipeline output attached: `npx tsc --noEmit` (0 errors), `npm run lint` (0 errors), `npm test` (9/9 passed), `npm run build` (success), `pytest tests/` (211/211 passed) |

---

### ⚠️ Known Non-Compliant Items Currently on Staging (For Owner Review & Written Sign-Off)

The following 9 items are currently staged or pending final implementation. Per Rule 2 & Rule 16, the repository owner must review and accept or reject these items in writing before promotion to `main`:

1. **Rule 1 (Branch Protection)**: GitHub branch protection rules on `main` and `staging` require manual configuration by the repository owner in GitHub repository settings.
2. **Rule 2 (PO Sign-Off Log)**: PO Sign-off documentation `docs/po-governance/SIGN_OFF.md` pending creation and explicit sign-off entry by the owner.
3. **Rule 3 (Affiliate Terms & Disclosure)**: Affiliate link statutory disclosure text and owner review of affiliate program terms for chat/export features pending owner confirmation.
4. **Rule 4 (Ingestion Guardrails Unit Tests)**: Dedicated unit tests asserting exact `bestvideo[height<=360]+bestaudio/best[height<=360]` format string, fail-closed missing duration metadata, and SHA-256 canonical `(platform, video_id)` cache key enforcement.
5. **Rules 7 & 10 (Telemetry SLA Benchmarks)**: Empirical p50 and p95 telemetry turnaround benchmarks split by cached vs non-cached requests and by platform.
6. **Rule 8 (Model Configuration & Thinking Level)**: Centralized model ID resolution in `Settings`, warn-only `list-models` startup check, explicit thinking level (`start with low`), and golden-set transition benchmark run.
7. **Rule 11 (Schema Versioning)**: Insertion of top-level `schema_version: 1` field in all newly generated `structured_data` payloads.
8. **Rule 13 (Hinglish Prompt Snapshot Test)**: Dedicated snapshot unit test asserting that Hinglish prompt rules and culinary mappings exist in system prompt templates.
9. **Rule 15 (Lighthouse & Axe Accessibility Audits)**: Automated Lighthouse mobile performance numbers and axe-core accessibility audit reports to be attached to documentation.

---

## 📋 Sprint Planning & Backlog Template (Rule 17)

Every sprint MUST be structured using the following standard template:

### Sprint Overview Header
| Sprint Metadata | Details |
| :--- | :--- |
| **Sprint Number** | Sprint X |
| **Sprint Goal** | 1-2 sentence primary goal of the sprint. |
| **Target Timeline** | Weeks X–Y |
| **Total Story Points** | XX pts |
| **Sprint Status** | Planned / In Progress / Verified on Dev / On Staging / Ready for PO Review |
| **Showcase Document** | `docs/po-governance/showcases/SPRINT_X_PO_SHOWCASE.md` |

### Ticket Table Schema
| ID | Title | Type | Priority | Acceptance criteria | Status | Commits | Evidence | PO verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **UPA-XXXX** | Ticket Title | Feature / Bug / Security / Tech-debt / Docs | P0 / P1 / P2 / P3 | Testable acceptance criteria | Planned / In Progress / Verified on Dev / On Staging / Ready for PO Review | Commit hashes | Quoted test outputs | Pending PO (Only owner sets PO Approved) |

---

## 📌 Sprint 11: Security, Accessibility & Governance Hardening (Ready for PO Review)

> **Sprint Goal:** Execute comprehensive system hardening across SSRF/IP DNS validation, host egress firewall, IP pinning TLS SNI preservation, Redis-backed Vault re-hydration rate limiting, WCAG 2.2 accessibility, admin telemetry authorization, exact dependency pinning, and AGENTS.md Rule 17 Sprint Planning Contract.

| Sprint Metadata | Details |
| :--- | :--- |
| **Sprint Number** | Sprint 11 |
| **Target Timeline** | Weeks 21–22 |
| **Total Story Points** | 42 pts |
| **Sprint Status** | 🧪 **Ready for PO Review** |
| **Showcase Document** | `docs/po-governance/PRODUCT_OWNER_UX_SHOWCASE.md` |

### 🎫 Sprint 11 Ticket Backlog

| ID | Title | Type | Priority | Acceptance criteria | Status | Commits | Evidence | PO verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **UPA-1101** | Group C Security Hardening (TRUSTED_PROXY, Egress Firewall, IP Pinning SNI) | Security | P0 | `TRUSTED_PROXY=False` default ignores spoofed XFF; `url_validator.py` rejects host if ANY resolved IP is non-global; `fetch_pinned_ip_url` connects to pinned IP with `Host` header & `_server_hostname` preserved; `deploy/setup_egress_firewall.sh` created. | 🟠 Verified on Dev / NOT VERIFIED (Container Execution) | `b97a2c9`<br>`6ae5a76`<br>`4382109` | `pytest tests/test_backend_security_hardening.py` (22/22 passed in 30.18s); `scripts/verify_egress.py` created | Pending PO |
| **UPA-1102** | Group B Frontend Utilities & Scaling Engine Unit Tests | Tech-debt | P1 | `recipeUtils.ts` pure functions decoupled; `scalingEngine.ts` handles 2x yield scaling for `"1 bowl (~150 ml, approx)"` per Rule 13; Vitest test suites clean green. | 🟢 Verified on Dev | `b97a2c9`<br>`6ae5a76` | `npm test` (12/12 passed in 147ms across 3 test files) | Pending PO |
| **UPA-1103** | Group A Design System, WCAG 2.2 Accessibility & Minimalist UI | UX / Feature | P1 | `OverflowBottomSheet.tsx` implements WCAG modal focus trap, `role="dialog"`, `aria-modal="true"`, Escape listener; input fields enforce `>=16px` font size & `min-height 44px`; contrast standard $\ge 4.5:1$ in both light & dark themes. | 🟢 Verified on Dev | `4382109`<br>`6ae5a76` | `npx tsc --noEmit` (0 errors), `npm run build` (success in 908ms) | Pending PO |
| **UPA-1104** | Group D Admin Telemetry Authorization & Metric Privacy | Security | P1 | Admin telemetry routes require `X-Admin-Api-Key` or `role == 'admin'`; raw user URLs & full video URLs stripped from metric payloads; secret hygiene enforced. | 🟢 Verified on Dev | `4382109`<br>`b97a2c9` | `pytest tests/test_backend_telemetry_admin.py` (6/6 passed) | Pending PO |
| **UPA-1105** | Group E Config, Rule 17 Governance Amendments & Document Contract | Docs / Governance | P0 | `AGENTS.md` Rule 9 amended and Rule 17 Sprint Planning & Backlog Contract added; `.env.example` created with per-env settings; exact `==` pins in `requirements.txt`; `pip-audit` zero vulnerabilities. | 🟢 Verified on Dev | `c5bf809`<br>`b97a2c9` | `python -m pip_audit -r requirements.txt` (0 vulnerabilities), 4 living docs + backlog updated | Pending PO |
| **UPA-1106** | Vault Item Re-hydration & Redis Rate Limiting | Security / Feature | P1 | `/api/v1/library/rehydrate` uses `QuotaManager.check_generic_rate_limit` with Redis & memory fallback (30 req/min limit); 31st request returns 429; `VaultLibrary.tsx` auto-rehydrates legacy items upon selection and shows buy buttons. | 🟢 Verified on Dev | `6ae5a76`<br>`b97a2c9` | `pytest tests/test_vault_rehydration.py` (2/2 passed), `npm test` (`vaultRehydration.test.ts` passed) | Pending PO |
| **UPA-1107** | Streamlit Deployment Audit & Query Parameter Removal | Security | P1 | Audited Streamlit Cloud deployments (`manas-recipe-extractor.streamlit.app`); disabled legacy `?admin=1` query parameter gating (`streamlit_app.py:1246`); zero URL-gated admin surfaces remain. | 🟢 Verified on Dev | `6ae5a76`<br>`b97a2c9` | Repo grep (`query_params`) returning 0 active gating lines | Pending PO |

---

## 📌 Sprint 12: Security, Secret Hygiene & Egress Refinement (Planned)

> **Sprint Goal:** Execute comprehensive system security hardening across JWT ES256 JWKS signature verification, HMAC stream proxy tokens, trusted proxy IP resolution, Redis rate limiting, container egress firewall rules, secret hygiene, dependency locking, and test suite protection.

| Sprint Metadata | Details |
| :--- | :--- |
| **Sprint Number** | Sprint 12 |
| **Target Timeline** | Weeks 23–24 |
| **Total Story Points** | 58 pts |
| **Sprint Status** | 📋 **Planned (Awaiting Owner Sign-Off per Ticket)** |
| **Showcase Document** | `docs/po-governance/showcases/SPRINT_12_PO_SHOWCASE.md` |

### 🎫 Sprint 12 Ticket Backlog

| ID | Title | Type | Priority | Acceptance criteria | Status | Commits | Evidence | PO verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **UPA-1201** | Entry Point SSRF & Pre-existing Test Audit (T1) | Security / Tests | P0 | Audit diff base `git diff 451b20e~1 HEAD -- tests frontend/src`; verify `validate_url_and_follow_redirects` rejects hosts resolving to private IPs (`127.0.0.1`, `169.254.169.254`); add NEW test in `tests/test_ssrf_entrypoint.py` without editing existing tests.<br>**Risks & Rollback**: Test failure if external DNS lookup blocks. Rollback: revert `tests/test_ssrf_entrypoint.py`.<br>**Test Plan**: Run `pytest tests/test_ssrf_entrypoint.py`. | 🟢 PO Approved | Committed in `1257992` | [MEASURED] `validate_url_and_follow_redirects` entry-point SSRF audit completed; `pytest tests/test_ssrf_entrypoint.py -v` (1/1 passed); `pytest tests/test_backend_security_hardening.py tests/test_ssrf_entrypoint.py -v` (23/23 passed); `pytest tests/ -q` (236 passed, 3 deselected, 25 warnings); Rule 21 verdict: VERIFIED ON DEV; no files/code changed during final audit. | PO Approved |
| **UPA-1202** | Secret Hygiene, Fallback Removal & Environment Gate (T2) | Security | P0 | Remove ALL constant fallbacks for `SECRET_KEY`, `RAZORPAY_*`, `STRIPE_*`, `WHATSAPP_VERIFY_TOKEN`, `universal_pro_default_secret_key` across `url_validator.py`, `extract.py`, `library.py`, `config.py`; `DEBUG` default False; `CORS_ORIGINS` from env (no `*`); non-dev envs treated as production; local `.env` required for dev (`ENVIRONMENT=development` requires `SECRET_KEY` from `.env`); state how `pytest` sets `ENVIRONMENT=test` via `tests/conftest.py` without editing existing tests; list existing tests relying on defaults for approval; split secrets into REQUIRED at startup vs FEATURE-GATED (503 if unset); document `CORS_ORIGINS` and all new env vars in `.env.example` and `DISASTER_RECOVERY.md`; standardize `TELEGRAM_BOT_TOKEN` & `TELEGRAM_WEBHOOK_SECRET`.<br>**Risks & Rollback**: App fails to start if `.env` missing required key. Rollback: restore `.env.example` template.<br>**Test Plan**: Run `pytest tests/test_config_secrets.py`. | 🟢 PO Approved | Committed in Commit 3 | `pytest tests/test_config_secrets.py` (3/3 passed); `pytest tests/` (234/234 passed in 24.34s) [MEASURED] | PO Approved |
| **UPA-1203** | Retire Streamlit App (T3) | Security / Tech-debt | P1 | Build import graph first. Delete ONLY files with no importers from API, workers, bots, or tests (`streamlit_app.py`). Do NOT delete shared root modules (e.g. `downloader.py`) that API imports. Grep shared modules for `import streamlit`. List existing tests importing Streamlit app for approval. Remove `streamlit` from `requirements.txt`. Update DR, user manual, backlog docs. Owner will pause/delete Streamlit Cloud apps separately.<br>**Risks & Rollback**: Accidental deletion of shared helper module. Rollback: `git checkout backend/app/services/streamlit_app.py`.<br>**Test Plan**: Run `pytest tests/` to confirm zero import failures. | 🟢 PO Approved | `efafca5` | [MEASURED] Import graph verified (0 importers from API, workers, bots, tests); deleted `streamlit_app.py` and launcher `app.py`; removed dead `streamlit` imports from `backend/app/services/config.py`; removed `streamlit==1.63.0` from `requirements.txt`; updated `telegram_bot.py` web_app_url to Next.js PWA; updated `DISASTER_RECOVERY.md`; `pytest tests/ -q` (236 passed, 3 deselected, 0 import failures). | PO Approved |
| **UPA-1204** | Rate Limiter & Sliding Window Audit (T4) | Security / Tech-debt | P1 | Absorbed into `UPA-1214`. Audit time-bucket key structure `rate_limit:{key}:{bucket}`.<br>**Risks & Rollback**: N/A.<br>**Test Plan**: See UPA-1214. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1205** | IP Pinning & PinnedHTTPSConnection Wire-Up (T6) | Security | P0 | Subclass `PinnedHTTPSConnection(http.client.HTTPSConnection)` with `server_hostname=self.host`; re-check inside `connect()` that pinned IP is global (`ip.is_global`); wire into real server-side fetches of user/remote-derived URLs (oEmbed/thumbnails) or delete if none (`stream_video` uses yt-dlp so nothing to wire there); make `validate_url_and_follow_redirects` fail closed, validate every hop, no second resolution, run DNS off event loop; add `tests/test_pinned_https.py` with `trustme` TLS test.<br>**Risks & Rollback**: SNI validation failure on custom domain certs. Rollback: revert `url_validator.py`.<br>**Test Plan**: Run `pytest tests/test_pinned_https.py`. | 🟢 PO Approved | `d7b0a3c` | [MEASURED] `PinnedHTTPSConnection` subclassed from `http.client.HTTPSConnection` with target `server_hostname` SNI binding and connect-time `is_global` check; single-resolution `validate_url_and_follow_redirects` probe implemented; `async_resolve_and_validate_hostname` and `async_validate_url_and_follow_redirects` added for off-event-loop DNS; `tests/test_pinned_https.py` created with `trustme` TLS handshake & SNI tests; `pytest tests/test_pinned_https.py -v` (13/13 passed); `pytest tests/test_backend_security_hardening.py tests/test_ssrf_entrypoint.py tests/test_pinned_https.py -v` (36/36 passed); `pytest tests/ -q` (249 passed, 3 deselected in 22.24s). | PO Approved |
| **UPA-1206** | Container Network Egress Firewall & Rollback Protocol (T5) | Security | P0 | Rules use `-s <compose subnet> -d <private range>` with `REJECT` so inbound traffic is untouched; compose-to-compose `RETURN` before private range rejects (compose subnet `172.28.0.0/16` is inside `172.16/12`); allowed traffic returns with `RETURN`; add `ip6tables`; idempotent, persistent across reboot; DNS-from-container test script (`scripts/verify_egress.py`); rollback script `iptables -F DOCKER-USER && iptables -A DOCKER-USER -j RETURN`; mark **NOT VERIFIED** until owner runs on Linux test host with console access.<br>**Risks & Rollback**: Blocking DNS or Upstash broker traffic. Rollback: run rollback script `iptables -F DOCKER-USER && iptables -A DOCKER-USER -j RETURN`.<br>**Test Plan**: Run `deploy/setup_egress_firewall.sh` on Linux test host and run container DNS test. | 🟢 PO Approved | `2d023bb` | [MEASURED] Container-level egress firewall verification executed on isolated Linux test host (Linux 6.6, Alpine 3.24, Docker 29.8.1, iptables/ip6tables v1.8.13); verified inside child container `ca025633cc38` on subnet `172.28.0.0/16`: (1) Container DNS: `www.instagram.com` -> `57.144.122.34` (UDP 53 PASSED); (2) Cloud metadata: `169.254.169.254` (Errno 111 Connection refused, REJECTED); (3) RFC 1918 subnets: `10.0.0.1` & `192.168.1.1` (Connection refused, REJECTED); (4) Public HTTPS: `https://www.instagram.com/` (HTTP 200 SUCCESS); (5) Intra-compose communication: `http://service-peer:8000/` (HTTP 200 SUCCESS); (6) Idempotency verified on second execution (0 duplicate rules); (7) Rollback script executed cleanly, returning `DOCKER-USER` to `-j RETURN` passthrough; (8) Full pytest suite: 249 passed, 3 deselected in 22.34s; Rule 21 classification: VERIFIED — CONTAINER EXECUTION. | PO Approved |
| **UPA-1207** | Dependencies, Clean Venv, Lock File & Audit (T7) | Tech-debt / Security | P1 | Perform import scan for runtime backend packages in `requirements.txt` (drop `streamlit`); place dev/test tools (`pytest`, `trustme`, `fakeredis`) in `requirements-dev.txt`; build clean venv on Docker Python image; generate `requirements.lock`; run `pip-audit`; confirm container boots & pytest passes.<br>**Risks & Rollback**: Missing transitive dependency in lockfile. Rollback: revert `requirements.txt`.<br>**Test Plan**: Build Docker image and run `pip-audit`. | 🟢 PO Approved | `0200401` | **VERIFIED ON DEV** [MEASURED]: Dead `pypdf` removed from `requirements.txt`; explicit `uvicorn[standard]>=0.34.0` added; dev/test dependencies (`pytest`, `pytest-asyncio`, `pytest-socket`, `pip-audit`, `trustme`, `fakeredis`, `pip-tools`) isolated in `requirements-dev.txt`; `backend/requirements.txt` synced; clean venv built in Docker Python 3.11 container with successful runtime imports (`ALL RUNTIME IMPORTS SUCCESSFUL IN CONTAINER [OK]`); deterministic `requirements.lock` generated via `pip-compile` with 1:1 byte reproducibility; `pip-audit -r requirements.txt` (0 vulnerabilities found); `pip-audit -r requirements.lock` (0 vulnerabilities found); Docker image `universal-pro-ai:upa-1207` built and booted with `/health` returning HTTP 200; `pytest tests/ -q` (249 passed, 3 deselected in 22.33s). | PO Approved |
| **UPA-1208** | Secret Scan & Repository History Audit (T8) | Security | P0 | Read-only scan. Run `gitleaks` with `--redact` (or `trufflehog` if output excludes secret values) over all refs across full git history. If tool not installed, report missing tool without silently substituting weaker scan. Report findings by file & rule name in `docs/po-governance/SECURITY_AUDIT_REPORT.md` without printing secret values. If ANYTHING found, STOP after scan and report to owner before starting next ticket. Do NOT commit report file if findings exist.<br>**Risks & Rollback**: Read-only scan. Zero risk to codebase.<br>**Test Plan**: Execute `gitleaks detect --redact --verbose`. | 🟢 PO Approved | Historical scan (`221 commits`) | [MEASURED] Gitleaks 8.30.1 executed against repository history (221 commits scanned); 4 findings reviewed: 3 confirmed mock/test Stripe values, 1 historical Telegram token confirmed real and revoked/invalidated; current tracked source uses environment-based `TELEGRAM_BOT_TOKEN`; `.env` is not tracked and is gitignored; no hardcoded credentials in current tracked source; no Git history rewrite performed; Rule 21 verdict: VERIFIED ON DEV. | PO Approved |
| **UPA-1209** | VaultLibrary React Component Test | Tech-debt / Tests | P1 | Create `frontend/src/components/__tests__/VaultLibrary.test.tsx` using jsdom + RTL testing `<VaultLibrary />` rendering & re-hydration with generic placeholder affiliate tags (`tag=MOCK_TAG`); list pre-existing `vaultRehydration.test.ts` for owner deletion sign-off.<br>**Risks & Rollback**: DOM selection timeout in RTL. Rollback: revert test file.<br>**Test Plan**: Run `npm test`. | 🟢 PO Approved | `1d1965a` | **VERIFIED ON DEV** [MEASURED]: `VaultLibrary.test.tsx` created with 7 unit/component tests in Vitest + jsdom + `@testing-library/react`; validates render state, search filter, local/remote items, rehydration with `tag=MOCK_TAG`, export dispatch, and deletion; `frontend/vitest.config.ts` configured; `npm --prefix frontend test` (4/4 test files, 19/19 tests passed in 1.83s); `npm --prefix frontend audit` (0 vulnerabilities found); `npm run build` in frontend succeeded; `./node_modules/.bin/tsc --noEmit` in frontend (0 errors); `pytest tests/ -q` (249 passed, 3 deselected in 23.05s); legacy test file `frontend/src/lib/__tests__/vaultRehydration.test.ts` listed for owner deletion sign-off (preserved untouched). | PO Approved |
| **UPA-1210** | Hinglish Prompt Evaluation Standard | Docs | P2 | Mark existing prompt snapshot strings as `ILLUSTRATIVE` and Hinglish golden set benchmark as `NOT VERIFIED` until live API evaluation is conducted against 3–5 fixed reels or transcripts.<br>**Risks & Rollback**: Documentation update only.<br>**Test Plan**: Review documentation text. | 🟢 PO Approved | `52b655d` | **VERIFIED ON DEV** [MEASURED]: Prompt snapshot strings in `PRODUCT_OWNER_UX_SHOWCASE.md` and `SPRINT_9_PO_SHOWCASE.md` labeled `[ILLUSTRATIVE]`; Hinglish golden-set transition benchmark labeled `[NOT VERIFIED]` pending live evaluation against 3–5 reference reels; protected files `gemini_processor.py` and `tests/test_hinglish_prompt_snapshot.py` confirmed unchanged (0 diffs); `pytest tests/test_hinglish_prompt_snapshot.py -v` (1/1 passed); `pytest tests/ -q` (249 passed, 3 deselected in 23.05s). | PO Approved |
| **UPA-1211** | PO Governance Document Audit | Docs | P2 | Grep codebase docs for `\[ ?✅ ?\]`, `Approved for Production`, `APPROVAL` and list all line numbers without editing files.<br>**Risks & Rollback**: Read-only documentation audit.<br>**Test Plan**: Execute grep search. | 🟢 PO Approved | Pending | [MEASURED] Documentation grep audit executed: `[ ✅ ]` & `Approved for Production` isolated to historical roadmap (`PRODUCT_OWNER_UX_SHOWCASE.md:384-388`); `APPROVAL` isolated to historical PO sign-offs (`SPRINT_8_PO_SHOWCASE.md:125`, `SPRINT_9_PO_SHOWCASE.md:132`, `PRODUCT_OWNER_UX_SHOWCASE.md:692`); zero unauthorized agent PO verdicts; all open sprint tickets maintain `Pending PO`. | PO Approved |
| **UPA-1212** | JWT ES256 JWKS Signature Verification & Audience Guard | Security | P0 | Asymmetric keys, verified via JWKS. Config settings: `SUPABASE_JWKS_URL`, `SUPABASE_JWT_ISSUER`, `SUPABASE_JWT_AUDIENCE = "authenticated"`, `SUPABASE_JWT_ALGORITHMS = ["ES256"]`. Derive JWKS URL (`{SUPABASE_URL}/auth/v1/.well-known/jwks.json`) and issuer (`{SUPABASE_URL}/auth/v1`) dynamically from `SUPABASE_URL` so each environment uses its own project. Fetch JWKS with caching and timeout (`jwt.PyJWKClient`), match `kid`, re-fetch on unknown `kid` with rate-limit. Reject `HS256`, `none`, and any other algorithm in production. Require `exp`, `sub`, `aud="authenticated"`. NEVER take `role` or `plan` from token claims (plan comes from DB profile only). Do NOT add a shared-secret setting, and do NOT touch or revoke any Supabase key. New tests: generate local EC P-256 key pair (`cryptography.hazmat`) and mock JWKS response in `tests/test_jwt_verification.py` (forged signature, expired, wrong audience, `alg=none`, `HS256` token rejected in prod, valid `ES256` token). List existing tests minting unsigned tokens and STOP for owner approval. Document new settings in `.env.example` and `DISASTER_RECOVERY.md`.<br>**Risks & Rollback**: Rejection of invalid tokens in dev tests. Rollback: revert `security.py`.<br>**Test Plan**: Run `pytest tests/test_jwt_verification.py`. | 🟢 PO Approved | Committed in Commit 4 | `pytest tests/test_jwt_verification.py tests/test_auth_security.py` (10/10 passed); `pytest tests/` (234/234 passed in 24.34s) [MEASURED] | PO Approved |
| **UPA-1213** | Stream Proxy Token Security & Media Hardening | Security | P0 | Token = `<exp>.<sig>`, sig = `HMAC-SHA256(secret, f"{id}\|{sha256(url)}\|{exp}")`, TTL 15 min, `compare_digest`, expired rejected. `/stream-video` accepts ONLY `id` + `token` (remove `url` param). Derive target URL from server-side record (job or cache row in Redis/Supabase, no in-memory JobManager dependency); 404 if none. Update `page.tsx`, `frontend/src/lib/recipeUtils.ts` (and its tests), and rewrite rules in same commit (list old `?url=` assertions for approval). Strip `stream_token` before saving to Vault or any cache and re-mint on open. Mint tokens ONLY where server holds result (cache hit, job completion). `/library/rehydrate` mints one only when server cache record exists for validated URL. Redis-backed per-IP rate limit. Run download off event loop. Enforce `MAX_MEDIA_DOWNLOAD_MB`, 90s, 360p on BOTH download paths including legacy downloader fallback with `max_filesize`. Cap total media-cache size. Cleanup in `finally`. Range support (`FileResponse` or manual 206). New tests: expired, tampered, wrong id, url param rejected, 429, Range 206.<br>**Risks & Rollback**: Media playback failure on expired token. Rollback: revert `extract.py` and `page.tsx`.<br>**Test Plan**: Run `pytest tests/test_stream_proxy_security.py`. | 🟢 PO Approved | `8fc7e4a` | **VERIFIED ON DEV** [MEASURED]: Expiring HMAC-SHA256 tokens (`<exp>.<sig>`, 15m TTL) bound to resource ID and media URL hash implemented with constant-time verification; legacy raw 64-char tokens strictly rejected; `/stream-video` hardened to accept only `id`+`token` query params with server-side URL resolution and any client `?url=` query strictly rejected (HTTP 400); Redis-backed per-IP rate limiting (429) enforced; blocking downloads offloaded to worker threadpool via `asyncio.to_thread`; HTTP Range (`206 Partial Content`) & 416 bounds handling verified; 50MB ceiling, 90-second duration rejection, and 360p format enforced without bare `/best` fallback; deterministic request-lifecycle stream cleanup implemented in unskippable `try...finally` generator blocks across 200, 206, 416, 50MB rejection, and client abort paths; `stream_token` omitted from client vault persistence; frontend `streamSrc` updated; dedicated security suite `tests/test_stream_proxy_security.py` (22/22 passed in 2.18s); security hardening suite (45/45 passed in 2.30s); full backend suite `pytest tests/` (271 passed, 3 deselected, 12 warnings in 17.84s); frontend suite `npm test` (4/4 files, 19/19 passed in 1.77s), `npx tsc --noEmit` (0 errors), `npm run build` (clean Next.js 15.5.25 production build). | PO Approved |
| **UPA-1214** | Client IP Resolution, Redis Rate Limits & Guest Quotas (absorbs UPA-1204) | Security / Tech-debt | P1 | `get_client_ip`: if `TRUSTED_PROXY` is False return `request.client.host` directly and ignore ALL forwarded headers. If True: use configured single-value header (named `TRUSTED_PROXY_HEADER` e.g. `CF-Connecting-IP` or `X-Real-IP`) or count `TRUSTED_PROXY_HOPS` from right of `X-Forwarded-For`; validate as IP, else fall back to socket IP. Propose signed anonymous device ID + IP as second factor for shared mobile IPs. Test `get_client_ip` with real Request objects under both settings. Replace `check_anonymous_rate_limit` in-memory dict with Redis-backed limiter. Guest quota consumption active (guests 20/day, free 30/day, anonymous 3/min). Order: rate limit -> validate URL -> cache lookup -> consume quota ONLY on cache miss -> enqueue. Single source of truth for limits in `Settings`; remove conflicting constants. QuotaManager: retry Redis connection with backoff. Time-bucket audit & tests.<br>**Risks & Rollback**: False positive rate limiting on shared NAT IPs. Rollback: revert `security.py` & `quota_service.py`.<br>**Test Plan**: Run `pytest tests/test_client_ip_and_quotas.py`. | 🟢 PO Approved | `fff6c2f` | **VERIFIED ON DEV** [MEASURED]: Implementation completed on Dev with commit `fff6c2f` (`[UPA-1214] harden client IP resolution and quota rate limits`); `TRUSTED_PROXY=False` strictly returns socket `client.host`; `TRUSTED_PROXY=True` supports `TRUSTED_PROXY_HEADER`, `X-Forwarded-For` right-to-left `TRUSTED_PROXY_HOPS`, and candidate validation via `ipaddress.ip_address()`; single source of truth established in `Settings` (Guest: 20/day, Free: 30/day, Anon rate: 3/min); `QuotaManager._get_redis()` implements bounded retry, backoff, and 5s cooldown; extraction pipeline strictly enforces Rate Limit -> URL Validation -> Cache Lookup (0-cost hit) -> Quota Consumption on Cache Miss -> Enqueue; dedicated test suite `tests/test_client_ip_and_quotas.py` (15 passed, 1 warning); targeted combined suite (63 passed, 10 warnings); full backend suite `pytest tests/` (286 passed, 3 deselected, 12 warnings in 42.68s); working tree clean after commit; Staging and Production untouched; `ALLOW_DB_WRITES=false` unchanged; ready for batched Owner/PO review. | PO Approved |
| **UPA-1215** | Data Endpoints Ownership & Validation Hardening | Security / Feature | P2 | `export_vault_item`: fetch by `extraction_id` scoped to current user (404 otherwise), guests 401 (no IP-based ownership on guest job polling — UUID is capability; enforce ownership on authenticated Vault/export routes), remove mock payload. `get_extraction_status`: validate `job_id` as UUID, use `requests` params (not string-built URLs), check ownership. `get_user_library`: guests see only rows flagged `is_public = true` (add NEW migration file for `is_public` with backfill decision; private rows NEVER readable by raw ID; add test). `rehydrate`: max body size, max 100 ingredients/products; reconcile `structured_data` vs `content_payload` with test.<br>**Risks & Rollback**: 404 on unauthenticated exports. Rollback: revert `library.py`.<br>**Test Plan**: Run `pytest tests/test_data_endpoints_security.py`. | 🟢 PO Approved | `5069414` | **VERIFIED ON DEV** [MEASURED]: Implementation completed on Dev with commit `5069414` (`[UPA-1215] harden data endpoint ownership and validation`); `export_vault_item` rejects guests with HTTP 401 ("Authentication required to export vault items"), queries `get_extraction_by_id` scoped to `user_id` or `is_public`, returns 404 for missing/inaccessible extractions, and hardcoded mock payload removed; `get_extraction_status` validates UUID before Supabase lookup via safe `params` without URL injection while preserving guest polling; `SupabaseRestClient.get_extraction_by_id` enforces strict public vs private ownership scoping; `rehydrate` validates item bounds (max 100 ingredients / 100 products, 100KB body limit) and reconciles `structured_data` vs `content_payload`; `backend/database/012_extraction_public_ownership.sql` created (unexecuted); dedicated test suite `tests/test_data_endpoints_security.py` (13/13 passed in 5.69s); targeted related suites (72/72 passed in 12.08s); full backend suite `pytest tests/` (299 passed, 3 deselected, 12 warnings in 47.76s); frontend suite `npm test` (19/19 passed in 1.83s), `npx tsc --noEmit` (0 errors); working tree clean after commit; Staging and Production untouched; `ALLOW_DB_WRITES=false` unchanged; ready for batched Owner/PO review. | PO Approved |
| **UPA-1216** | Commerce Link Validation, Admin Key Hygiene & Enum Bounds | Security / Tech-debt | P2 | Test that every URL `AffiliateEngine` emits passes `validate_merchant_redirect_url`; fix allowlist to real hosts (`swiggy.com`, `ajio.com`, `nykaa.com`, `earnkaro.com`, `zepto.now`). Compare admin key as bytes (`hmac.compare_digest`); rate limit admin attempts. `domain_hint` Enum MUST equal frontend option IDs: `auto`, `recipe`, `kitchen_product`, `fitness_workout`, `interior_design`, `gaming`, `tech_diy`, `unboxing`, `diy` (single shared source). Add test that every frontend option and sample chip is accepted. Language codes: accept whatever UI and bots send.<br>**Risks & Rollback**: Rejection of novel domain hints. Rollback: revert `extract.py`.<br>**Test Plan**: Run `pytest tests/test_commerce_and_enums.py`. | 🟢 PO Approved | `7919bb1`, `4d95a6e` | **VERIFIED ON DEV** [MEASURED]: Implementation completed on Dev with commits `7919bb1` (`[UPA-1216] harden commerce links admin auth and domain enums`) and `4d95a6e` (`[UPA-1216] enforce canonical domain source`); `ALLOWED_MERCHANT_DOMAINS` aligned with all `AffiliateEngine` generated hosts (`swiggy.com`, `ajio.com`, `nykaa.com`, `earnkaro.com`, `zepto.now`, `zeptonow.com`, `google.com`, `amazon.in`, `flipkart.com`, etc.) passing `validate_merchant_redirect_url`; `require_admin_user` compares admin keys as bytes via `hmac.compare_digest` and rate limits attempts (5 attempts / 60s per client IP returning HTTP 429) via `QuotaManager.check_generic_rate_limit`; canonical single source of truth `frontend/src/data/domain_options.json` established with exact 9 IDs (`auto`, `recipe`, `kitchen_product`, `fitness_workout`, `interior_design`, `gaming`, `tech_diy`, `unboxing`, `diy`), consumed directly by frontend `page.tsx` and dynamically by backend `DomainHint(str, Enum)`; hardcoded backend fallback removed in `4d95a6e` with explicit fail-fast `FileNotFoundError` on missing definition; non-restrictive language string acceptance and trimming verified; dedicated test suite `tests/test_commerce_and_enums.py` (22/22 passed in 3.69s); targeted related suites (61/61 passed in 9.01s); full backend suite `pytest tests/` (321 passed, 3 deselected, 12 warnings in 47.68s); frontend suite `npm test` (19/19 passed in 1.71s), `npx tsc --noEmit` (0 errors); working tree clean after commit; Staging and Production untouched; `ALLOW_DB_WRITES=false` unchanged; ready for batched Owner/PO review. | PO Approved |
| **UPA-1217** | Compose Hardening Override Separation | DevOps | P3 | Move `cap_drop`/`no-new-privileges` out of `docker-compose.override.yml` (auto-loaded) into `docker-compose.hardening.yml` (not auto-loaded); remove obsolete `version` key.<br>**Risks & Rollback**: Missing compose overrides in prod without `-f`. Rollback: restore `docker-compose.override.yml`.<br>**Test Plan**: Run `docker compose config`. | 🟢 PO Approved | `91527a6` | **VERIFIED ON DEV** [MEASURED]: Implementation completed on Dev with commit `91527a6` (`[UPA-1217] separate compose hardening overlay`); obsolete `version` keys removed from `docker-compose.yml`; `docker-compose.override.yml` deleted so container hardening is no longer auto-loaded during local dev; `docker-compose.hardening.yml` created as explicit opt-in overlay defining least-privilege container options for `api` (`cap_drop: [ALL]`, `cap_add: [NET_BIND_SERVICE]`, `security_opt: [no-new-privileges:true]`) and `worker` (`cap_drop: [ALL]`, `security_opt: [no-new-privileges:true]`); base Compose configuration validates cleanly with 0 warnings (`docker compose -f docker-compose.yml config`); hardened merged Compose configuration validates cleanly with 0 warnings (`docker compose -f docker-compose.yml -f docker-compose.hardening.yml config`); bare `docker compose config` no longer auto-loads hardening; dedicated test suite `tests/test_compose_hardening.py` (9/9 passed in 0.44s); full backend suite `pytest tests/` (330 passed, 3 deselected, 12 warnings in 49.10s); deployment and recovery documentation updated in `ORACLE_CLOUD_DEPLOYMENT.md` and `DISASTER_RECOVERY.md` to explicitly use the hardening overlay; working tree clean after commit; Staging and Production untouched; `ALLOW_DB_WRITES=false` unchanged; ready for batched Owner/PO review. | PO Approved |
| **UPA-1218** | Staging Environment Isolation & Project Separation | DevOps / Security | P0 | Provision separate Supabase project for staging; apply `backend/database/*.sql` in order (`01_schema.sql`, `02_indexes.sql`, `03_functions.sql`, `04_rls_policies.sql`, `05_views.sql`); manual steps: owner creates staging project in Supabase UI, runs scripts in order via SQL Editor; configure dedicated staging credentials (`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`; `SUPABASE_JWKS_URL` derived from `SUPABASE_URL`); separate `SECRET_KEY`, Redis key prefix (`staging:`), Celery queue (`staging_default_queue`), Redis database (DB 1 vs DB 0), webhook secrets (`TELEGRAM_WEBHOOK_SECRET`, `WHATSAPP_VERIFY_TOKEN`, `RAZORPAY_WEBHOOK_SECRET`, `STRIPE_WEBHOOK_SECRET`), and Telegram bot per environment; update `DISASTER_RECOVERY.md` and `ENVIRONMENTS.md`; verify staging JWKS endpoint (`{STAGING_SUPABASE_URL}/auth/v1/.well-known/jwks.json`).<br>**Risks & Rollback**: Staging misconfiguration during initial project switch. Rollback: restore previous staging environment variables.<br>**Test Plan**: Deploy to Staging, run `scripts/verify_egress.py`, verify JWKS endpoint returns valid ES256 key, and verify zero production database rows modified. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1219** | Test Environment Isolation Gate & Socket Firewall | Tech-debt / Security | P0 | Add `tests/conftest.py` that (1) hard-overrides all external service credentials to empty strings BEFORE any app import; (2) enforces a session-level safety gate: `get_supabase_client().is_configured()` must be False and Redis/Celery URLs must target loopback only — fails entire session if violated; (3) deselects three Supabase-live-dependent test nodes per owner Rule 1 sign-off, replacing them with mocked equivalents; (4) mocks `yt_dlp.extract_info` for offline duration guardrail tests. Add `pytest.ini` with `--disable-socket --allow-hosts=127.0.0.1,localhost` to block outbound network at the socket layer. Firewall confirmed fail-closed: `socket.connect("8.8.8.8", 53)` → `SocketConnectBlockedError`; `requests.get("https://example.com")` → `SocketConnectBlockedError`; `socket.connect("127.0.0.1", 19999)` → `ConnectionRefusedError` (allowed, nothing listening).<br>**Affected files**: `tests/conftest.py` (NEW), `pytest.ini` (NEW).<br>**Deselected nodes (owner-approved)**: `test_supabase_client_is_configured`, `test_public_extraction_schema_org_recipe_jsonld`, `test_public_sitemap_urls`.<br>**Risks & Rollback**: If `pytest-socket` is removed, firewall silently vanishes. Rollback: revert `pytest.ini`.<br>**Test Plan**: `pytest tests/` 234 passed, 3 deselected in 24.34s [MEASURED]; socket probe 2 FAILED (external blocked), 1 PASSED (loopback allowed) [MEASURED]. | 🟢 Verified on Dev (Committed in Commit 6) | Committed in Commit 6 | `pytest tests/` 234 passed, 3 deselected, 0 failures in 24.34s [MEASURED] | Pending PO |
| **UPA-1221** | Supabase PostgREST Param Escaping & ALLOW_DB_WRITES Guard | Security / Tech-debt | P1 | `SupabaseRestClient`: (1) add `_escape_postgrest_val(val, for_or)` — unquoted single-column filters escape `%→\%`, `_→\_`, `(→\(`, `)→\)`, `,→\,`, `"→\"`; OR-filter values double-quoted with internal `"` doubled; (2) add `ALLOW_DB_WRITES: bool = False` to `Settings` and `is_write_allowed()` guard replacing bare `is_configured()` on all mutating calls (`save_extraction`, `increment_daily_quota`, `update_creator_tags`, `record_telemetry_event`, `log_beta_telemetry`); (3) remove hardcoded slug fallbacks — `get_public_extraction_by_slug_or_id` returns `None` and `list_public_extraction_slugs` returns `[]` when unconfigured; (4) all query filters passed as `params=` dict, never f-string URL injection.<br>**Affected files**: `backend/app/core/supabase_client.py`, `tests/test_postgrest_escaping.py` (NEW).<br>**Risks & Rollback**: `ALLOW_DB_WRITES=False` default — production deployments need `ALLOW_DB_WRITES=true` in `.env`.<br>**Test Plan**: `pytest tests/test_postgrest_escaping.py` (3/3 passed) [MEASURED]; `pytest tests/` (234/234 passed) [MEASURED]. | 🟢 Verified on Dev (Committed in Commit 7) | Committed in Commit 7 | `pytest tests/test_postgrest_escaping.py` 3/3 passed; `pytest tests/` 234 passed [MEASURED] | Pending PO |
| **UPA-1222** | SEO Public Hub structured_data Migration & Mocked Test Coverage | Tech-debt / Tests | P1 | `public_hub.py` `build_schema_org_recipe` and `get_public_extraction` read `structured_data` field first, falling back to `extracted_content` for backward compat. `list_public_extraction_slugs` reads `structured_data` column. Two mocked replacement tests: `test_public_extraction_schema_org_recipe_jsonld_mocked` injects full `structured_data` dict via `monkeypatch`, asserts `schema_org["@context"]=="https://schema.org"`, `schema_org["@type"]=="Recipe"`, `schema_org["name"]=="Crispy Air Fryer Samosa"`, `len(schema_org["recipeIngredient"])==2`, `len(schema_org["recipeInstructions"])==1` — fails if `structured_data` schema regresses; `test_public_sitemap_urls_mocked` injects one slug and asserts `count==1`, URL contains slug.<br>**Affected files**: `backend/app/api/v1/public_hub.py`, `tests/test_sprint6_seo_and_creators.py`.<br>**Risks & Rollback**: Old `extracted_content` fallback preserved. Rollback: revert `public_hub.py`.<br>**Test Plan**: `pytest tests/test_sprint6_seo_and_creators.py` (8/8 passed) [MEASURED]. | 🟢 Verified on Dev (Committed in Commit 9) | Committed in Commit 9 | `pytest tests/test_sprint6_seo_and_creators.py` 8/8 passed [MEASURED] | Pending PO |
| **UPA-1223** | Real processing_time_ms Telemetry & Downloader Logger | Tech-debt | P2 | `backend/app/workers/tasks.py`: record `start_time = time.time()` at pipeline entry; compute `processing_time_ms = int((time.time() - start_time) * 1000)` before `save_extraction` and `log_beta_telemetry`, replacing hardcoded `turnaround_time_ms=2500`. `backend/app/services/downloader.py`: add module-level `logger = logging.getLogger(__name__)` so download errors surface in structured logs.<br>**Affected files**: `backend/app/workers/tasks.py`, `backend/app/services/downloader.py`.<br>**Risks & Rollback**: Low-risk metric and logging fix. Rollback: revert `tasks.py`.<br>**Test Plan**: `pytest tests/test_workers_and_affiliate.py` (all passing) [MEASURED]; `pytest tests/` (234/234) [MEASURED]. | 🟢 Verified on Dev (Committed in Commit 8) | Committed in Commit 8 | `pytest tests/` 234 passed [MEASURED] | Pending PO |
| **UPA-1227** | SEO Public Hub 503 DB Unreachable vs 404 Missing Content & Test Scoping | Bug / Security | P1 | Differentiate `SupabaseRestClient` DB unreachable / HTTP error states (`503 Service Unavailable`) from missing entity records (`404 Not Found`) across `/public/sitemap` and `/public/extractions/{slug}`. When `is_configured() == True` but DB connection drops/fails, raise HTTP 503 and log structured error alert; when `is_configured() == False` or mock fixture present in test env (`ENVIRONMENT=test`), preserve stubbed offline returns for test isolation; when DB succeeds with 0 rows, return 404 (slug) or 200 empty (sitemap).<br>**Affected files**: `backend/app/api/v1/public_hub.py`, `backend/app/core/supabase_client.py`, `tests/test_sprint6_seo_and_creators.py`.<br>**Risks & Rollback**: Low risk. Rollback: revert `public_hub.py` and `supabase_client.py`.<br>**Test Plan**: `pytest tests/test_sprint6_seo_and_creators.py` (9/9 passed) [MEASURED]; `pytest tests/` (236/236 passed) [MEASURED]. | 🟢 Verified on Dev (Committed in Commit 10) | Committed in Commit 10 | `pytest tests/test_sprint6_seo_and_creators.py` 9/9 passed; `pytest tests/` 236 passed [MEASURED] | Pending PO |
| **UPA-1228** | Frontend Landing Page Verification & Benchmark Claim Hygiene | Docs / Security | P2 | Remove unverified performance turnaround claims ("under 3 seconds") from `frontend/src/app/page.tsx` until empirical p50/p95 benchmarks are generated directly from backend telemetry, ensuring strict adherence to AGENTS.md Rule 9 & Rule 16.<br>**Affected files**: `frontend/src/app/page.tsx`.<br>**Risks & Rollback**: UI text update only. Rollback: revert `page.tsx`.<br>**Test Plan**: `npm run build` (0 errors) [MEASURED]. | 🟢 Verified on Dev (Committed in Commit 5) | Committed in Commit 5 (6b453b1) | `npm run build` 0 errors [MEASURED] | Pending PO |
| **UPA-1229** | Growth Telemetry Events Table DDL & Service Role Security Isolation | Database / Security | P1 | Create `backend/database/010_telemetry_events.sql` defining `public.telemetry_events` table (`id`, `event_name`, `user_id`, `session_id`, `properties`, `created_at`), performance indexes, `service_role` grants, and strict RLS policies. Ensures full schema parity between application expectations (`record_telemetry_event`, `get_telemetry_funnel`) and PostgreSQL database.<br>**Affected files**: `backend/database/010_telemetry_events.sql` (NEW).<br>**Risks & Rollback**: DDL creation only. Rollback: `rm backend/database/010_telemetry_events.sql`.<br>**Test Plan**: Static SQL correctness review & RLS grant inspection [MEASURED]. | 🟢 Verified on Dev (Committed in Commit 11) | Committed in Commit 11 | Static SQL review & RLS grant audit clean [MEASURED] | Pending PO |
| **UPA-1230** | Minimum-Privilege & Security Hardening — Migration 011 | Security | P0 | Establish deterministic minimum-privilege PostgreSQL/Supabase permissions for core application tables, harden SECURITY DEFINER functions, remove public RPC execution rights from privileged quota functions, and remove unused/unscoped beta_telemetry_feed SELECT policy.<br>**Affected files**: `backend/database/011_privilege_hardening.sql`.<br>**Risks & Rollback**: Incorrect ACLs could break backend database operations. RPC privilege changes could affect quota enforcement. SECURITY DEFINER changes could affect privileged function execution if search_path assumptions are wrong. beta_telemetry_feed policy changes must be validated in Staging before Production promotion. Rollback: Migration 011 has not yet been executed; before execution, rollback SQL must be reviewed and approved separately. Do NOT claim rollback has been tested unless evidence exists. Do NOT use broad git restore/reset/clean operations as rollback.<br>**Test Plan**: 1. Execute Migration 011 in Staging only after explicit execution approval. 2. Perform read-only ACL/RLS/RPC privilege verification. 3. Verify application-required database operations against real Staging. 4. Verify unauthenticated RPC abuse attempts are rejected. 5. Verify public extraction reads still obey intended RLS behavior. 6. Verify telemetry_events SELECT/INSERT works for service_role. 7. Verify beta_telemetry_feed INSERT works for service_role. 8. Complete full Staging application validation before Production consideration. | 🟢 PO Approved | `99de07dee14d0521b87b8c60513b87cb9298d54d` | [MEASURED] Migration 011 executed successfully in Supabase Staging; direct PostgreSQL ACL, function EXECUTE, SECURITY DEFINER/search_path, schema ACL, RLS policy, and safe PostgREST verification all match the approved minimum-privilege contract. Production untouched. | PO Approved |
| **UPA-1231** | Agent Instruction Hardening — Skill-First Protocol & Destructive Workspace Guard | Docs / Governance | P0 | Harden repository agent governance by adding Section 18 (Skill-First Execution Protocol & Workspace Tooling Map) and Section 19 (Destructive Workspace Operation Guard) to AGENTS.md. Section 18 requires mandatory inspection and reuse of existing skills, scripts, and established routines before custom implementation. Section 19 prevents unauthorized destructive workspace cleanup, broad git restore/reset/clean operations, and accidental removal of governance, migration, test, configuration, skill, script, or documentation files.<br>**Affected files**: `AGENTS.md`.<br>**Risks & Rollback**: Tool/script paths referenced by Section 18 may change over time. Overly broad governance language could conflict with an explicitly owner-authorized operation; explicit owner authorization remains the controlling exception. Rollback: Restore AGENTS.md to the immediately preceding approved version only after verifying no later owner-approved AGENTS.md changes must be preserved. Do not use broad repository reset/clean operations.<br>**Test Plan**: 1. Verify Sections 1–17 remain unchanged. 2. Verify Section 18 exists. 3. Verify Section 19 exists. 4. Run `git diff -- AGENTS.md`. 5. Confirm no other files are changed or deleted. 6. No SQL execution, deployment, Redis configuration, or database mutation is part of this ticket. | 🟡 In Progress | Uncommitted (`AGENTS.md`) | AGENTS.md modified with Sections 18 & 19; verification clean scope confirmed | Pending PO |
| **UPA-1232** | Execution Artifact & Script Provenance Guard | Docs / Governance | P1 | Add AGENTS.md Section 20 to govern temporary scratch scripts and operational execution artifacts. Read-only diagnostics may use temporary global/IDE scratch scripts, while mutating operational scripts must be repository-controlled, ticketed, reviewed, and auditable. Governed migrations must execute from the exact reviewed repository migration artifact.<br>**Affected files**: `AGENTS.md`.<br>**Risks & Rollback**: Future temporary diagnostic tooling may require clarification of read-only scope. Overly strict interpretation could block legitimate owner-authorized operational work. Rollback: Restore AGENTS.md to the preceding approved version only after checking for later owner-approved governance changes. Do not use broad repository reset/clean commands.<br>**Test Plan**: git diff -- AGENTS.md; verify Sections 1–19 unchanged; verify Section 20 contents; confirm only AGENTS.md is modified; no SQL/deployment/Redis activity. | 🟡 In Progress | Uncommitted (`AGENTS.md`) | AGENTS.md modified with Section 20; verification clean scope confirmed | Pending PO |
| **UPA-1233** | Staging Application Deployment & Gateway Validation | Tech-debt / Docs / Deployment Governance | P0 | Governs controlled Staging application deployment gate: (1) promote verified commit from Dev to staging; (2) deploy Next.js frontend to Vercel Preview Staging environment; (3) deploy FastAPI backend API container on Staging host (`129.225.86.241`); (4) verify Staging environment/secrets presence (`ENVIRONMENT=staging`, `SECRET_KEY`, `SUPABASE_URL=https://mzpkdmaxsuhwezsooidu.supabase.co`, `ALLOW_DB_WRITES=false`) without displaying secret values — initial application deployment must occur with database writes disabled (`ALLOW_DB_WRITES=false`); (5) execute real PostgREST lookup (`GET /api/v1/public/extractions/non-existent-slug-12345`) returning HTTP 404 to prove Application → Staging Supabase connectivity; (6) verify FastAPI gateway runtime endpoints (`GET /` and `GET /health` returning `"status": "healthy"`); (7) verify Production isolation by confirming zero configuration references Production Supabase ref (`scrqvbgjybnrvcpxbygf`), without contacting Production; (8) capture deployment evidence; (9) define Staging rollback procedures; (10) explicitly defer Redis/Celery background workers until application gateway gate passes; (11) explicitly defer E2E validation suite until application gateway and Staging integration gates pass; (12) database write enablement (`ALLOW_DB_WRITES=true`) is a separate later gate; (13) Staging `SECRET_KEY` rotation & post-rotation gateway verification; (14) Gate 7 controlled database write/read/delete verification & immediate rollback to read-only isolation; (15) Gate 8 controlled Redis/Celery background processing verification & immediate rollback to fallback mode; (16) Gate 9 controlled E2E verification; (17) Gate 9 root-cause investigation & resolution.<br>**Affected files**: `docs/po-governance/JIRA_BACKLOG.md`, `docs/architecture/SYSTEM_ARCHITECTURE.md`, `docs/architecture/ENVIRONMENTS.md`, `docs/architecture/ORACLE_CLOUD_DEPLOYMENT.md`, `docs/architecture/DISASTER_RECOVERY.md`.<br>**Applicable AGENTS.md rules**: Rules 2, 6, 14, 16, 17, 21, Sections 18, 19, 20.<br>**Risks & Rollback**: Staging environment variable misconfiguration. Rollback: Vercel preview rollback to prior release; container image rollback on Staging host; rollback to `ALLOW_DB_WRITES=false` after write testing; stop worker and redis containers.<br>**Test Plan**: 1. `python scripts/promote.py --to staging` pre-promotion pass & git push evidence. 2. Environment secret presence audit with `ALLOW_DB_WRITES=false` default. 3. Vercel Staging preview HTTP 200 check with bypass cookie. 4. Staging API Gateway `/health` & `/` runtime verification. 5. Real Staging Supabase PostgREST lookup (`GET /api/v1/public/extractions/non-existent-slug-12345`) returning HTTP 404. 6. Production isolation check confirming `SUPABASE_URL` resolves to `https://mzpkdmaxsuhwezsooidu.supabase.co` with zero Production DB contact. 7. Staging `SECRET_KEY` rotation and post-rotation health verification. 8. Gate 7 synthetic write (`insert_extraction`), service-role retrieval, immediate deletion, rollback to `ALLOW_DB_WRITES=false`, and post-rollback negative guard verification. 9. Gate 8 Redis 7 container activation, Celery worker registration (`--pool=threads --concurrency=4`), real async task dispatch & worker execution (`gate8_job_1790332992_8561bd`), write-guard preservation (0 DB rows), resource check, and controlled rollback. 10. Gate 9 read-only readiness inspection across governance prerequisites and dependencies. 11. Gate 9 controlled E2E execution on Staging with validated test URL (`https://www.youtube.com/shorts/DPdivoOcXHM`), Redis/Celery worker, dedicated Staging Gemini credential, temporary `ALLOW_DB_WRITES=true`, and full rollback. | 🟢 PO Approved | `8fcfdf0cbd4d030b064bb36cfd34178fa204a8da` | [MEASURED] Staging promotion and deployment verified on `8fcfdf0`. Staging VM 129.225.86.241 OS bootstrap, 2.0 GiB swap, Docker 29.8.1, Compose v5.5.1, repo checkout at `8fcfdf0`, .env mode 600, and Caddy+API container runtime (0 restarts) VERIFIED via SSH. Staging SECRET_KEY rotation VERIFIED (zero secret exposure, .env mode 600, ENVIRONMENT=staging & ALLOW_DB_WRITES=false unchanged). External Gate 5 (GET http://129.225.86.241/health -> HTTP 200 OK {"status":"healthy","integrations":{"supabase":true,...}}) and External Gate 6 (GET http://129.225.86.241/api/v1/public/extractions/non-existent-slug-12345 -> HTTP 404 Not Found) VERIFIED from Owner workstation. Quality gate: 236 passed, 3 deselected, 0 failed [MEASURED]. Gate 7 controlled write verification VERIFIED on Staging (real PostgREST insert/retrieve/delete; rollback to ALLOW_DB_WRITES=false verified). Gate 8 controlled Redis/Celery verification VERIFIED on Staging (real worker registration, apply_async task dispatch/consumption, 0 DB mutations, clean rollback). Gate 9 controlled E2E verification empirically VERIFIED on Staging (2026-09-25): (1) Test input: validated public video (`https://www.youtube.com/shorts/DPdivoOcXHM`), cache miss confirmed (`is_cached: false`), fresh E2E execution; (2) API & Queue: request accepted (`POST /api/v1/extract` -> HTTP 202 ACCEPTED, job `879bf101-bcba-47f9-8ece-121138d80cfa`), Celery dispatch confirmed (`celery_redis_queue`), real Celery worker consumption verified; (3) Media ingestion: automatic YouTube fallback handled bot challenge (`yt_stream_DPdivoOcXHM.jpg`); (4) Multimodal AI inference: provider resolved to Gemini (`gemini-3.8-flash`), real upload (`POST /upload/.../files` 200 OK, 4.9s) and generateContent (`POST /models/gemini-3.8-flash:generateContent` 200 OK, 17.4s) succeeded, remote file cleaned (`DELETE /files/...` 200 OK); (5) Structured result produced: rich recipe extracted (`Restaurant-Style Creamy Palak Paneer Recipe`, ingredients, instructions, equipment, chef tips, timings `upload_s: 4.88`, `inference_s: 17.42`, `total_ai_s: 24.06`); (6) Database persistence: extraction persisted to Staging Supabase `public.extractions` (`status: completed`, matching title), verified via service role, and immediately deleted via service-role DELETE (`DELETE_HTTP_STATUS: 200`), confirming 0 residual test rows; (7) Final retrieval: `GET /api/v1/extract/status/879bf101-bcba-47f9-8ece-121138d80cfa` returned completed structured result; (8) Media cleanup: managed temporary media paths inspected with 0 orphaned files; (9) Non-fatal telemetry event: `beta_telemetry_feed` HTTP 403 recorded as NON-FATAL / KNOWN TELEMETRY PERMISSION ISSUE (service role table grant hint) without affecting core extraction; (10) Write guard: temporary `ALLOW_DB_WRITES=true` restored immediately to `ALLOW_DB_WRITES=false` (.env mode 600); post-rollback negative write guard verified (0 rows in DB); (11) Redis/Celery rollback: Redis and Celery worker stopped & removed, in-memory fallback restored healthy (`/health` HTTP 200); (12) Resource stability: 954 MiB RAM (587 MiB used), 1.9 GiB free swap, 0 OOM kills, 0 unexpected restarts, 0 crashes; (13) Production isolation: Production (`140.245.214.28`) UNTOUCHED. | PO Approved |
| **UPA-1234** | Staging Application Deployment Write Gate Clarification | Docs / Governance | P0 | Clarify Staging deployment write gate: initial Staging application deployment MUST execute with database writes disabled (`ALLOW_DB_WRITES=false`); database write enablement (`ALLOW_DB_WRITES=true`) is a separate, later gate requiring explicit owner authorization.<br>**Affected files**: `docs/po-governance/JIRA_BACKLOG.md`.<br>**Applicable AGENTS.md rules**: Rules 2, 6, 14, 16, 17, Sections 18, 19, 20.<br>**Risks & Rollback**: Misinterpreting write gate requirements. Rollback: revert backlog documentation.<br>**Test Plan**: Verify `ALLOW_DB_WRITES=false` contract in documentation and environment validation. | 🟢 Verified on Dev | `170f5e511202aa6394046f30c04a245efacd33d8` | Verified documentation contract on Dev | Pending PO |
| **UPA-1235** | Staging Architecture & Vercel Preview Reconciliation | Docs / Architecture | P1 | Reconcile Staging architecture: Vercel Preview deployment represents the Staging frontend layer (`staging` branch); backend Staging host architecture requires explicit owner decision.<br>**Affected files**: `docs/po-governance/JIRA_BACKLOG.md`.<br>**Applicable AGENTS.md rules**: Rules 2, 17.<br>**Risks & Rollback**: Architectural mismatch. Rollback: revert documentation.<br>**Test Plan**: Read-only architecture audit. | 🟢 Verified on Dev | Read-only audit | Verified Staging architecture reconciliation | Pending PO |
| **UPA-1236** | Review and Harden verify_promotion.py Test Runner Changes | Tech-debt / Security | P1 | Govern and harden `scripts/verify_promotion.py` test runner adjustments: (1) evaluate transition from `unittest` discovery to `pytest` execution for parity with `scripts/ci_check.py`; (2) assess hardcoded `SECRET_KEY` fallback string (`"universal_pro_default_secret_key_2026"`) and remove hardcoded secret fallbacks to enforce strict Rule 6 secret hygiene; (3) ensure promotion verification executes cleanly using environment secret resolution; (4) perform regression verification of pre-promotion quality gates against preserved recovery branch `recovery/verify-promotion-c86c38f`.<br>**Affected files**: `scripts/verify_promotion.py`.<br>**Applicable AGENTS.md rules**: Rules 1, 6, 16, 17, Sections 18, 19, 20.<br>**Risks & Rollback**: Script misconfiguration during promotion checks. Rollback: preserved in local recovery branch `recovery/verify-promotion-c86c38f`.<br>**Test Plan**: 1. Inspect preserved commit `c86c38ff9cf64b6d0d7c9b150830a086917a9fe7`. 2. Refactor `verify_promotion.py` to eliminate hardcoded secret fallback. 3. Verify clean `python scripts/verify_promotion.py` execution with `SECRET_KEY` passed from environment. | 🟢 Verified on Dev | Uncommitted (`scripts/verify_promotion.py`) | [MEASURED] `python scripts/verify_promotion.py` PASSED 100%: Syntax Compilation PASS, Clean Imports PASS (14/14 modules), Automated Tests PASS (236 passed, 3 deselected in 21.33s), Git Hygiene PASS. | Pending PO |
| **UPA-1237** | Register Universal Pro AI System Architecture Baseline & Rule 21 Drift Guard | Docs / Architecture | P0 | Adopt System Architecture Baseline (`docs/architecture/SYSTEM_ARCHITECTURE.md`); add Rule 21 (Documentation Synchronization & Architecture Drift Guard) to `AGENTS.md`; cross-reference architecture runbooks (`ENVIRONMENTS.md`, `ORACLE_CLOUD_DEPLOYMENT.md`, `DISASTER_RECOVERY.md`); register UPA-1237 in `JIRA_BACKLOG.md`; maintain Pending PO status.<br>**Affected files**: `docs/architecture/SYSTEM_ARCHITECTURE.md`, `AGENTS.md`, `docs/po-governance/JIRA_BACKLOG.md`, `docs/architecture/ENVIRONMENTS.md`, `docs/architecture/ORACLE_CLOUD_DEPLOYMENT.md`, `docs/architecture/DISASTER_RECOVERY.md`.<br>**Applicable AGENTS.md rules**: Rules 9, 16, 17, 21, Sections 18, 19, 20.<br>**Risks & Rollback**: Documentation mismatch with runtime. Rollback: Revert documentation files via git.<br>**Test Plan**: Run `python scripts/ci_check.py` to ensure build, lint, and tests remain clean green. | 🟢 Verified on Dev | `ff3a270` | Documentation & governance adoption committed | Pending PO |
| **UPA-1238** | Correct and Reconcile Universal Pro AI System Architecture Baseline | Docs / Architecture / Governance | P0 | Reconcile System Architecture Baseline (`SYSTEM_ARCHITECTURE.md`) against authoritative OCI specs (AMD x86_64), Redis topology (local containerized + Upstash fallback), database migration inventory (`001`, `009`, `010`, `011`), sanitize raw affiliate tags, restore 9-gate deployment readiness model, and update legacy Streamlit references in `ENVIRONMENTS.md` & `DISASTER_RECOVERY.md`.<br>**Affected files**: `docs/architecture/SYSTEM_ARCHITECTURE.md`, `docs/po-governance/JIRA_BACKLOG.md`, `docs/architecture/ENVIRONMENTS.md`, `docs/architecture/DISASTER_RECOVERY.md`.<br>**Applicable AGENTS.md rules**: Rules 9, 16, 17, 21, Sections 18, 19, 20.<br>**Risks & Rollback**: Documentation discrepancy with runtime. Rollback: Revert documentation files via git.<br>**Test Plan**: Run `python scripts/ci_check.py` to ensure build, lint, and test suite remain clean green. | 🟢 Verified on Dev | Uncommitted | Documentation reconciliation verified | Pending PO |
| **UPA-1239** | Dedicated OCI Staging Backend Infrastructure & Environment Isolation | DevOps / Infrastructure / Security | P0 | Governs dedicated OCI Staging backend infrastructure setup and environment isolation: (1) OCI second-instance provisioned & verified (VM.Standard.E2.1.Micro `universal-pro-ai-staging-instance`, AMD x86_64, 1 GB RAM, Ubuntu 24.04.5 LTS, Public IP `129.225.86.241`, Private IP `10.0.2.242` in `ap-hyderabad-1` AD `HJag:AP-HYDERABAD-1-AD-1` — ACTUALLY PROVISIONED / RUNNING; SSH access EXTERNALLY VERIFIED by Owner); (2) Staging network topology reusing existing VCN `universalpro-ai-vcn` (`10.0.0.0/16`) with DEDICATED STAGING SUBNET (`staging-public-subnet` `10.0.2.0/24`), VNIC `universal-pro-ai-staging-vnic`, and DEDICATED STAGING SECURITY LIST (`staging-security-list-universalpro-ai-vcn`) enforcing TCP 22 restricted, TCP 80 public, TCP 443 public, NO inbound TCP 8000, and NO inbound TCP 6379 (explaining that OCI NSGs are additive and cannot deny permissive subnet security-list rules, preserving Production subnet/rules unchanged); (3) Memory & storage configuration (1 GB physical RAM with proposed 2 GB `/swapfile` as memory-pressure mitigation only; ~47 GB default boot volume); (4) Initial runtime stack limited strictly to Caddy reverse proxy (`caddy:2-alpine`) and FastAPI gateway (`api`) with `ALLOW_DB_WRITES=false` initially (Application deployment, Docker, Caddy, FastAPI runtime, Supabase connectivity, DNS/TLS, Redis/Celery, and E2E NOT YET VERIFIED / NOT YET DEPLOYED); (5) Redis/Celery background processing explicitly DEFERRED to Gate 8; (6) Staging credentials (`ENVIRONMENT=staging`, `SECRET_KEY`, `SUPABASE_URL=https://mzpkdmaxsuhwezsooidu.supabase.co`); (7) Zero Production DB (`scrqvbgjybnrvcpxbygf`) contact; (8) Rule 21 documentation synchronization across `SYSTEM_ARCHITECTURE.md`, `ENVIRONMENTS.md`, `ORACLE_CLOUD_DEPLOYMENT.md`, `DISASTER_RECOVERY.md`, `JIRA_BACKLOG.md`. Explicitly excludes Production changes, Vercel changes, Supabase changes, Redis/Celery activation, E2E execution, UPA-1226 remediation, commit rewriting, and recovery branch deletion.<br>**Affected files**: `docs/po-governance/JIRA_BACKLOG.md`, `docs/architecture/SYSTEM_ARCHITECTURE.md`, `docs/architecture/ENVIRONMENTS.md`, `docs/architecture/ORACLE_CLOUD_DEPLOYMENT.md`, `docs/architecture/DISASTER_RECOVERY.md`.<br>**Applicable AGENTS.md rules**: Rules 2, 6, 9, 14, 16, 17, 21, Sections 18, 19, 20.<br>**Risks & Rollback**: Staging environment misconfiguration. Rollback: Container image rollback on Staging VM; zero automated DB resets.<br>**Test Plan**: 1. Verify OCI Staging VM provisioning & SSH access [EXTERNALLY VERIFIED BY OWNER]. 2. Verify OS swap & Docker/Compose setup for Caddy + API. 3. Audit environment variables (`ALLOW_DB_WRITES=false`). 4. Verify Caddy HTTPS health & public port isolation. 5. Perform PostgREST 404 lookup against Staging Supabase. 6. Confirm zero Production DB contact. | 🟢 PO Approved | `8fcfdf0` | [MEASURED] Dedicated OCI Staging infrastructure (VM.Standard.E2.1.Micro, AMD x86_64, 1 GB RAM, Ubuntu 24.04.5 LTS, Public IP 129.225.86.241, Private IP 10.0.2.242 in ap-hyderabad-1) provisioned and externally verified via SSH by Owner; dedicated staging subnet (staging-public-subnet 10.0.2.0/24) and security list (TCP 22 restricted, TCP 80/443 public, NO inbound 8000/6379) active; 2.0 GiB swapfile, Docker 29.8.1, Compose v5.5.1 configured; .env mode 600 with ALLOW_DB_WRITES=false; Caddy reverse proxy and FastAPI gateway runtime verified with 0 restarts; external /health (HTTP 200 OK) and Staging Supabase read path (HTTP 404) verified; Production isolation confirmed (0 contact with Production Supabase or VM); full Staging application lifecycle governed under UPA-1233. | PO Approved |







---

## 📌 Sprint 12: Security, Secret Hygiene & Egress Refinement (Planned)

> **Sprint Goal:** Execute comprehensive system security hardening across JWT signature verification, HMAC stream proxy tokens, trusted proxy IP resolution, Redis rate limiting, egress firewall rules, secret hygiene, dependency locking, and test suite protection.

| Sprint Metadata | Details |
| :--- | :--- |
| **Sprint Number** | Sprint 12 |
| **Target Timeline** | Weeks 23–24 |
| **Total Story Points** | 58 pts |
| **Sprint Status** | 📋 **Planned (Awaiting Owner Sign-Off for Protected Areas)** |
| **Showcase Document** | `docs/po-governance/showcases/SPRINT_12_PO_SHOWCASE.md` |

### 🎫 Sprint 12 Ticket Backlog

| ID | Title | Type | Priority | Acceptance criteria | Status | Commits | Evidence | PO verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **UPA-1201** | Entry Point SSRF & Pre-existing Test Audit (T1) | Security / Tests | P0 | Audit diff base `git diff 451b20e~1 HEAD -- tests frontend/src`; verify `validate_url_and_follow_redirects` rejects hosts resolving to private IPs (`127.0.0.1`, `169.254.169.254`); add NEW test in `tests/test_ssrf_entrypoint.py` without editing existing tests. | 🟢 PO Approved | `1257992` | [MEASURED] `validate_url_and_follow_redirects` entry-point SSRF audit completed; `pytest tests/test_ssrf_entrypoint.py -v` (1/1 passed); `pytest tests/test_backend_security_hardening.py tests/test_ssrf_entrypoint.py -v` (23/23 passed); `pytest tests/ -q` (236 passed, 3 deselected, 25 warnings); Rule 21 verdict: VERIFIED ON DEV; no files/code changed during final audit. | PO Approved |
| **UPA-1202** | Secret Hygiene, Fallback Removal & Environment Gate (T2) | Security | P0 | Remove ALL constant fallbacks for `SECRET_KEY`, `RAZORPAY_*`, `STRIPE_*`, `WHATSAPP_VERIFY_TOKEN`, `universal_pro_default_secret_key` across `url_validator.py`, `extract.py`, `library.py`, `config.py`; `DEBUG` default False; `CORS_ORIGINS` from env (no `*`); non-dev envs treated as production; local `.env` required for dev; standardize `TELEGRAM_*` env vars. | 🟢 PO Approved | `6b453b1` | [MEASURED] `pytest tests/test_config_secrets.py` (3/3 passed); `pytest tests/` (234/234 passed in 24.34s). | PO Approved |
| **UPA-1203** | Streamlit Audit & Security/Gating/Retire Proposal (T3) | Security / Tech-debt | P1 | Audit Streamlit paths for `url_validator` and `quota_manager` (neither used); propose retiring Streamlit or adding both validations; gate developer expander with `ADMIN_PASSWORD` + `hmac.compare_digest`. | 🟢 PO Approved | `efafca5` | [MEASURED] Import graph verified (0 importers from API, workers, bots, tests); deleted `streamlit_app.py` and launcher `app.py`; removed dead `streamlit` imports from `backend/app/services/config.py`; removed `streamlit==1.63.0` from `requirements.txt`; updated `telegram_bot.py` web_app_url to Next.js PWA; updated `DISASTER_RECOVERY.md`; `pytest tests/ -q` (236 passed, 3 deselected, 0 import failures). | PO Approved |
| **UPA-1204** | Rate Limiter & Sliding Window Audit (T4) | Security / Tech-debt | P1 | Absorbed into `UPA-1214`. Audit time-bucket key structure `rate_limit:{key}:{bucket}`. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1205** | IP Pinning & PinnedHTTPSConnection Wire-up (T6) | Security | P0 | Subclass `PinnedHTTPSConnection(http.client.HTTPSConnection)` with `server_hostname=self.host`; wire into real server-side fetches of user/remote-derived URLs (oEmbed/thumbnails) or delete if none; `stream_video` uses yt-dlp so nothing to wire there; re-check inside `connect()` that pinned IP is global; add `trustme` TLS test. | 🟢 PO Approved | `d7b0a3c`, `36c6967` | **VERIFIED ON DEV** [MEASURED]: `PinnedHTTPSConnection` subclassed with SNI binding and connect-time `is_global` check; single-resolution `validate_url_and_follow_redirects` probe implemented; `async_resolve_and_validate_hostname` and `async_validate_url_and_follow_redirects` added for off-event-loop DNS; `tests/test_pinned_https.py` created with `trustme` TLS handshake & SNI tests; `pytest tests/test_pinned_https.py -v` (13/13 passed); `pytest tests/test_backend_security_hardening.py tests/test_ssrf_entrypoint.py tests/test_pinned_https.py -v` (36/36 passed); `pytest tests/ -q` (249 passed, 3 deselected in 22.24s). | PO Approved |
| **UPA-1206** | Container Network Egress Firewall & Rollback Protocol (T5) | Security | P0 | Update `setup_egress_firewall.sh` with rules `-s <compose subnet> -d <private range>` returning `RETURN` so inbound traffic is untouched; compose subnet `172.28.0.0/16`; add `ip6tables`; DNS test from container; rollback `iptables -F DOCKER-USER && iptables -A DOCKER-USER -j RETURN`; mark **NOT VERIFIED** until Linux host test. | 🟢 PO Approved | `2d023bb`, `dc4cd45`, `4b82922` | **VERIFIED — CONTAINER EXECUTION** [MEASURED]: Broad `172.16.0.0/12` RETURN rule removed. Tested inside Linux container attached to `172.28.0.0/16`: 169.254.169.254, 10.0.0.1, 192.168.1.1, non-compose 172.16.0.1, non-compose 172.31.255.1 all connection refused / blocked. DNS resolution and https://www.instagram.com/ HTTP 200 passed. Intra-compose peer (http://service-peer:8000) HTTP 200 passed. Idempotency (0 duplicates on re-run) and Rollback (clean default RETURN for IPv4 & IPv6) verified. Pytest 249 passed. | PO Approved |
| **UPA-1207** | Dependencies, Clean Venv, Lock File & Audit (T7) | Tech-debt / Security | P1 | Perform import scan for runtime backend packages in `requirements.txt`; place dev/test tools (`pytest`, `trustme`, `fakeredis`) in `requirements-dev.txt`; build clean venv on Docker Python image; generate `requirements.lock`; run `pip-audit`; confirm container boots & pytest passes. | 🟢 PO Approved | `0200401` | **VERIFIED ON DEV** [MEASURED]: Dead `pypdf` removed from `requirements.txt`; explicit `uvicorn[standard]>=0.34.0` added; dev/test dependencies (`pytest`, `pytest-asyncio`, `pytest-socket`, `pip-audit`, `trustme`, `fakeredis`, `pip-tools`) isolated in `requirements-dev.txt`; `backend/requirements.txt` synced; clean venv built in Docker Python 3.11 container with successful runtime imports (`ALL RUNTIME IMPORTS SUCCESSFUL IN CONTAINER [OK]`); deterministic `requirements.lock` generated via `pip-compile` with 1:1 byte reproducibility; `pip-audit -r requirements.txt` (0 vulnerabilities found); `pip-audit -r requirements.lock` (0 vulnerabilities found); Docker image `universal-pro-ai:upa-1207` built and booted with `/health` returning HTTP 200; `pytest tests/ -q` (249 passed, 3 deselected in 22.33s). | PO Approved |
| **UPA-1208** | Secret Scan & Repository History Audit (T8) | Security | P0 | Run `gitleaks` / `trufflehog` / regex pattern scanner over all git refs for sensitive tokens (Mistral, Stripe, Razorpay, Telegram, WhatsApp, Vercel secret); report findings by file & rule name in `docs/po-governance/SECURITY_AUDIT_REPORT.md` without printing secret values. | 🟢 PO Approved | Historical scan (`221 commits`) | [MEASURED] Gitleaks 8.30.1 executed against repository history (221 commits scanned); 4 findings reviewed: 3 confirmed mock/test Stripe values, 1 historical Telegram token confirmed real and revoked/invalidated; current tracked source uses environment-based `TELEGRAM_BOT_TOKEN`; `.env` is not tracked and is gitignored; no hardcoded credentials in current tracked source; no Git history rewrite performed; Rule 21 verdict: VERIFIED ON DEV. | PO Approved |
| **UPA-1209** | VaultLibrary React Component Test | Tech-debt / Tests | P1 | Create `frontend/src/components/__tests__/VaultLibrary.test.tsx` using jsdom + RTL with `tag=MOCK_TAG`; list old `vaultRehydration.test.ts` for owner deletion sign-off. | 🟢 PO Approved | `1d1965a` | **VERIFIED ON DEV** [MEASURED]: `VaultLibrary.test.tsx` created with 7 unit/component tests in Vitest + jsdom + `@testing-library/react`; validates render state, search filter, local/remote items, rehydration with `tag=MOCK_TAG`, export dispatch, and deletion; `frontend/vitest.config.ts` configured; `npm --prefix frontend test` (4/4 test files, 19/19 tests passed in 1.83s); `npm --prefix frontend audit` (0 vulnerabilities found); `npm run build` in frontend succeeded; `./node_modules/.bin/tsc --noEmit` in frontend (0 errors); `pytest tests/ -q` (249 passed, 3 deselected in 23.05s); legacy test file `frontend/src/lib/__tests__/vaultRehydration.test.ts` listed for owner deletion sign-off (preserved untouched). | PO Approved |
| **UPA-1210** | Hinglish Prompt Evaluation Standard | Docs | P2 | Mark existing prompt snapshot strings as `ILLUSTRATIVE` and Hinglish golden set benchmark as `NOT VERIFIED` until live API evaluation is conducted. | 🟢 PO Approved | `52b655d` | **VERIFIED ON DEV** [MEASURED]: Prompt snapshot strings in `PRODUCT_OWNER_UX_SHOWCASE.md` and `SPRINT_9_PO_SHOWCASE.md` labeled `[ILLUSTRATIVE]`; Hinglish golden-set transition benchmark labeled `[NOT VERIFIED]` pending live evaluation against 3–5 reference reels; protected files `gemini_processor.py` and `tests/test_hinglish_prompt_snapshot.py` confirmed unchanged (0 diffs); `pytest tests/test_hinglish_prompt_snapshot.py -v` (1/1 passed); `pytest tests/ -q` (249 passed, 3 deselected in 23.05s). | PO Approved |
| **UPA-1211** | PO Governance Document Audit | Docs | P2 | Grep codebase docs for `\[ ?✅ ?\]`, `Approved for Production`, `APPROVAL` and list all line numbers without editing files. | 🟢 PO Approved | Pending | [MEASURED] Documentation grep audit executed: `[ ✅ ]` & `Approved for Production` isolated to historical roadmap (`PRODUCT_OWNER_UX_SHOWCASE.md:384-388`); `APPROVAL` isolated to historical PO sign-offs (`SPRINT_8_PO_SHOWCASE.md:125`, `SPRINT_9_PO_SHOWCASE.md:132`, `PRODUCT_OWNER_UX_SHOWCASE.md:692`); zero unauthorized agent PO verdicts; all open sprint tickets maintain `Pending PO`. | PO Approved |
| **UPA-1212** | JWT Signature Verification & Audience Guard | Security | P0 | Fix `security.py get_current_user`: verify signature, `exp`, and `aud="authenticated"` against Supabase signing setup (HS256 secret or JWKS from config, never hardcode). Pin allowed algorithms, reject `alg=none`, require `exp` & `sub`, never take `role` or `plan` from token claims (plan comes from DB profile only). New tests: forged signature, expired, wrong audience, `alg=none`, valid token. List every existing test minting unsigned tokens. | 🟢 PO Approved | `6b453b1` | [MEASURED] `pytest tests/test_jwt_verification.py tests/test_auth_security.py` (10/10 passed); `pytest tests/` (234/234 passed in 24.34s). | PO Approved |
| **UPA-1213** | Stream Proxy Token Security & Media Hardening | Security | P0 | Token = `<exp>.<sig>`, sig = `HMAC-SHA256(secret, f"{id}\|{sha256(url)}\|{exp}")`, TTL 15 min, `compare_digest`, expired rejected. `/stream-video` accepts ONLY `id` + `token` (remove `url` param). Derive target URL from server-side record (job or cache row); 404 if none. Update `page.tsx` and rewrites in same commit. Mint tokens ONLY where server holds result. `/library/rehydrate` mints one only when server cache record exists for validated URL. Redis-backed per-IP rate limit. Run download off event loop. Enforce `MAX_MEDIA_DOWNLOAD_MB`, 90s, 360p on BOTH download paths including legacy downloader fallback. Cap total media-cache size. Cleanup in `finally`. Range support (`FileResponse` or manual 206). New tests: expired, tampered, wrong id, url param rejected, 429, Range 206. | 🟢 PO Approved | `8fc7e4a` | **VERIFIED ON DEV** [MEASURED]: Expiring HMAC-SHA256 tokens (`<exp>.<sig>`, 15m TTL) bound to resource ID and media URL hash implemented with constant-time verification; `/stream-video` hardened to accept only `id`+`token` query params with server-side URL resolution and legacy query rejection (400); per-IP rate limiting (429) enforced; blocking downloads offloaded to worker threadpool via `asyncio.to_thread`; HTTP Range (`206 Partial Content`) & 416 bounds handling verified; 50MB ceiling and 360p format enforced; `stream_token` omitted from client vault persistence; frontend `streamSrc` updated; dedicated security suite `tests/test_stream_proxy_security.py` (22/22 passed); security hardening suite (45/45 passed); full backend suite `pytest tests/` (271 passed, 3 deselected in 17.84s); frontend suite `npm test` (4/4 files, 19/19 passed in 1.77s), `npx tsc --noEmit` (0 errors), `npm run build` (clean Next.js 15.5.25 production build). | PO Approved |
| **UPA-1214** | Client IP Resolution, Redis Rate Limits & Guest Quotas | Security / Tech-debt | P1 | `get_client_ip`: if `TRUSTED_PROXY` is False return `request.client.host` and ignore ALL forwarded headers. If True: use configured single-value header or count `TRUSTED_PROXY_HOPS` from right of `X-Forwarded-For`; validate as IP, else fall back to socket IP. Test with real Request objects under both settings. Replace `check_anonymous_rate_limit`'s in-memory dict with Redis-backed limiter. Guests MUST consume daily quota. Execution order: rate limit -> validate URL -> cache lookup -> consume quota ONLY on cache miss -> enqueue. Single source of truth for limits in `Settings`; remove conflicting constants (3/10 in security.py & Settings vs 20/30 in quota_service). QuotaManager: retry Redis connection with backoff. Time-bucket audit & tests. | 🟢 PO Approved | `fff6c2f` | **VERIFIED ON DEV** [MEASURED]: Implementation completed on Dev with commit `fff6c2f`; `TRUSTED_PROXY=False` strictly returns socket `client.host`; `TRUSTED_PROXY=True` supports `TRUSTED_PROXY_HEADER`, `X-Forwarded-For` right-to-left `TRUSTED_PROXY_HOPS`, and candidate validation; single source of truth in `Settings` (Guest: 20/day, Free: 30/day, Anon rate: 3/min); QuotaManager bounded retry and cooldown; extraction pipeline Rate Limit -> URL Validation -> Cache Lookup -> Quota Consumption on Cache Miss -> Enqueue; dedicated test suite `tests/test_client_ip_and_quotas.py` (15 passed); full suite `pytest tests/` (286 passed, 3 deselected). | PO Approved |
| **UPA-1215** | Data Endpoints Ownership & Validation Hardening | Security / Feature | P2 | `export_vault_item`: fetch by `extraction_id` scoped to current user (404 otherwise), guests 401, remove mock payload. `get_extraction_status`: validate `job_id` as UUID, use `requests` params (not string-built URLs), check ownership. `get_user_library`: guests see only rows flagged public (add test). `rehydrate`: max body size, max 100 ingredients/products; reconcile `structured_data` vs `content_payload` with test. | 🟢 PO Approved | `5069414` | **VERIFIED ON DEV** [MEASURED]: Implementation completed on Dev with commit `5069414`; `export_vault_item` rejects guests with HTTP 401, queries `get_extraction_by_id` scoped to user/public, returns 404 for inaccessible extractions; `get_extraction_status` validates UUID before Supabase lookup via safe `params`; `rehydrate` validates item bounds (max 100 ingredients/products, 100KB body limit); `012_extraction_public_ownership.sql` created (unexecuted); dedicated test suite `tests/test_data_endpoints_security.py` (13/13 passed); full suite `pytest tests/` (299 passed, 3 deselected). | PO Approved |
| **UPA-1216** | Commerce Link Validation, Admin Key Hygiene & Enum Bounds | Security / Tech-debt | P2 | Test that every URL `AffiliateEngine` emits passes `validate_merchant_redirect_url`; fix allowlist to real hosts (`swiggy`, `ajio`, `nykaa`, `earnkaro`, `zepto`). Compare admin key as bytes (`hmac.compare_digest`); rate limit admin attempts. Validate `domain_hint` and `preferred_language` against enums. | 🟢 PO Approved | `7919bb1`, `4d95a6e` | **VERIFIED ON DEV** [MEASURED]: Implementation completed on Dev with commits `7919bb1` and `4d95a6e`; `ALLOWED_MERCHANT_DOMAINS` aligned with all `AffiliateEngine` generated hosts; `require_admin_user` compares admin keys as bytes via `hmac.compare_digest` and rate limits attempts (5/60s); canonical source `domain_options.json` (9 IDs) consumed directly by UI and backend `DomainHint`; dedicated suite `tests/test_commerce_and_enums.py` (22/22 passed); full suite `pytest tests/` (321 passed, 3 deselected). | PO Approved |
| **UPA-1217** | Compose Hardening Override Separation | DevOps | P3 | Move `cap_drop`/`no-new-privileges` out of `docker-compose.override.yml` (auto-loaded) into `docker-compose.hardening.yml` (not auto-loaded); remove obsolete `version` key. | 🟢 PO Approved | `91527a6` | **VERIFIED ON DEV** [MEASURED]: Implementation completed on Dev with commit `91527a6`; obsolete `version` keys removed; `docker-compose.override.yml` removed; `docker-compose.hardening.yml` created as explicit opt-in overlay; base and hardened compose configurations validate cleanly; dedicated suite `tests/test_compose_hardening.py` (9/9 passed); full suite `pytest tests/` (330 passed, 3 deselected). | PO Approved |
| **UPA-1224** | Production API HTTPS & Proxy IP Architecture | Security / DevOps | P0 | Propose domain + Caddy site block for automatic TLS certificate management; open port 443 in OCI Security List; redirect HTTP 80 -> 443. Report frontend communication (`NEXT_PUBLIC_API_URL`, `next.config.mjs` rewrites, SSR fetch in `sitemap.ts` & `r/[slug]/page.tsx`, client polling) and end-to-end proxy hop IP chain (`Client -> Vercel -> Caddy -> FastAPI`) under `TRUSTED_PROXY=True` and `TRUSTED_PROXY_HOPS=2`. | 🧪 Staging Verified / Ready for PO Review | `8fe06e1`<br>`f019929` | **STAGING VERIFIED** [MEASURED]: Dev implementation committed in `8fe06e1` (PO Approved in `SIGN_OFF.md`); promoted to `staging` via merge commit `f019929` (Dev HEAD `b47de68`); parameterized Caddyfile using `{$API_DOMAIN}` with `encode gzip zstd` and internal `reverse_proxy api:8000`; proxy forwarding chain formalized (`Client -> Vercel Edge -> Caddy -> FastAPI`) under `TRUSTED_PROXY=True` and `TRUSTED_PROXY_HOPS=2`; Staging gateway health verified on VM `129.225.86.241` (`GET /health` -> HTTP 200 OK); Vercel Staging Preview verified (`universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app` -> HTTP 200 OK); Staging Supabase read path verified (`GET /api/v1/public/extractions/non-existent-slug-12345` -> HTTP 404 Not Found, 0 DB writes); targeted test suite passed (`pytest tests/test_client_ip_and_quotas.py tests/test_commerce_and_enums.py tests/test_port_shielding_and_docs.py tests/test_compose_hardening.py -v`: 53 passed, 0 failed, 1 warning in 3.98s); full pre-promotion verification passed (`python scripts/verify_promotion.py`: 337 passed, 3 deselected in 47.79s); Production VM (`140.245.214.28`), `main` branch (`1ada501`), Supabase (`scrqvbgjybnrvcpxbygf`), DNS, Vercel, and OCI untouched; `ALLOW_DB_WRITES=false` preserved. | Dev PO Approved (SIGN_OFF.md) / Pending PO for Prod |
| **UPA-1225** | Production VM Zero-Downtime Promotion Runbook | DevOps / Deployment | P0 | Promotion runbook for Ubuntu 24.04 VM (1 GB RAM, Docker Compose: Caddy, API, Worker, Redis running Sep 13 code). Steps: (1) manual `.env` secret audit (`SECRET_KEY`, `ADMIN_API_KEY`, `WHATSAPP_APP_SECRET`, `ENVIRONMENT=production`, `ALLOW_DB_WRITES=true`, `TRUSTED_PROXY=true`); (2) sync code from approved `main` commit; (3) recreate worker then API one-by-one (`docker compose up -d --no-deps --build worker` then `api`); (4) smoke tests (`curl` health, docs disabled check, polling); (5) rollback protocol to previous commit. Rule 2: zero direct edits on VM. | 🧪 Staging Verified / Ready for PO Review | `fd11a02`<br>`f019929` | **STAGING VERIFIED** [MEASURED]: Dev implementation committed in `fd11a02` (PO Approved in `SIGN_OFF.md`); promoted to `staging` via merge commit `f019929` (Dev HEAD `b47de68`); promotion and rollback runbook synchronized across `ORACLE_CLOUD_DEPLOYMENT.md` and `DISASTER_RECOVERY.md`; 3-layer promotion lineage (`Dev` $\rightarrow$ `staging` $\rightarrow$ `PO Review` $\rightarrow$ `main` $\rightarrow$ `Production`) and pre-flight governance gate established; live `PREV_PROD_SHA` capture and container rollback protocol using `docker-compose.hardening.yml` documented; `ALLOW_DB_WRITES=true` isolated exclusively to the authorized Production execution gate (`ALLOW_DB_WRITES=false` preserved on Dev/Staging); Staging VM `129.225.86.241` health and Supabase PostgREST 404 read path verified; Vercel Staging Preview verified (HTTP 200 OK); targeted tests passed (53/53 passed); full pre-promotion suite passed (337 passed, 3 deselected in 47.79s); Production VM (`140.245.214.28`), `main` branch (`1ada501`), Supabase (`scrqvbgjybnrvcpxbygf`), DNS, Vercel, and OCI untouched; zero Production commands executed; `ALLOW_DB_WRITES=false` preserved. | Dev PO Approved (SIGN_OFF.md) / Pending PO for Prod |
| **UPA-1226** | Production API Public Exposure & Port Shielding | Security | P0 | Remediate production VM API exposure where container publishes `0.0.0.0:8000` answering `/docs` on public IP bypassing Caddy, and Caddy container IP `172.18.0.5` collapses all rate limits. Propose: (1) bind API container port strictly to `127.0.0.1:8000:8000` (or drop host publishing); (2) Caddy client IP forwarding trusted via `TRUSTED_PROXY` and `TRUSTED_PROXY_HOPS`; (3) HTTPS via domain; (4) secret audit ensuring no secrets in `NEXT_PUBLIC_` vars; (5) evaluate Next.js server-side API proxy route to hide backend origin. | 🧪 Staging Verified / Ready for PO Review | `b3088ea`<br>`f019929` | **STAGING VERIFIED** [MEASURED]: Dev implementation committed in `b3088ea` (PO Approved in `SIGN_OFF.md`); promoted to `staging` via merge commit `f019929` (Dev HEAD `b47de68`); API container port binding updated from public `0.0.0.0:8000` exposure strictly to loopback `127.0.0.1:8000:8000` in `docker-compose.yml`; Caddy internal Docker network forwarding (`reverse_proxy api:8000`) and Redis loopback binding (`127.0.0.1:6379:6379`) intact; configurable documentation settings (`DOCS_URL`, `REDOC_URL`, `OPENAPI_URL`) added with automatic `None` normalization (tested 404 on disable, 200 on dev/staging default); Step 3 Security List table and host iptables instructions in `ORACLE_CLOUD_DEPLOYMENT.md` updated to document TCP 8000 removal; external socket probe from external network to host TCP 8000 and TCP 6379 verified blocked/refused (`connect_ex != 0`); Staging VM `129.225.86.241` health verified (HTTP 200 OK); Vercel Staging Preview verified (HTTP 200 OK); admin auth verified (401 missing key, 403 fails closed on invalid/unset key); merchant redirect allowlist verified (Amazon 307, evil-domain.com 400, zeptonow.com 307, zepto.now 400); targeted test suite passed (`pytest tests/test_client_ip_and_quotas.py tests/test_commerce_and_enums.py tests/test_port_shielding_and_docs.py tests/test_compose_hardening.py -v`: 53 passed, 0 failed, 1 warning in 3.98s); full pre-promotion verification passed (`python scripts/verify_promotion.py`: 337 passed, 3 deselected in 47.79s); Production VM (`140.245.214.28`), `main` branch (`1ada501`), Supabase (`scrqvbgjybnrvcpxbygf`), DNS, Vercel, and OCI untouched; `ALLOW_DB_WRITES=false` preserved. | Dev PO Approved (SIGN_OFF.md) / Pending PO for Prod |
| **UPA-1239** | Dedicated OCI Staging Backend Infrastructure & Environment Isolation | DevOps / Infrastructure / Security | P0 | Governs dedicated OCI Staging backend VM setup (`universal-pro-ai-staging-instance`, VM.Standard.E2.1.Micro, AMD x86_64, 1 GB RAM, Ubuntu 24.04.5 LTS, Public IP `129.225.86.241`, Private IP `10.0.2.242` in `ap-hyderabad-1` AD `HJag:AP-HYDERABAD-1-AD-1` — ACTUALLY PROVISIONED / RUNNING; SSH access EXTERNALLY VERIFIED by Owner), ~47 GB default boot volume, 1 GB RAM with proposed 2 GB `/swapfile` for memory-pressure mitigation only, Network topology reusing existing VCN (`universalpro-ai-vcn`) with DEDICATED STAGING SUBNET (`staging-public-subnet` `10.0.2.0/24`), VNIC `universal-pro-ai-staging-vnic`, and DEDICATED STAGING SECURITY LIST (`staging-security-list-universalpro-ai-vcn` with Public inbound 80/443; restricted SSH port 22; NO public 8000; NO public 6379; explaining OCI NSGs are additive and cannot override permissive security-list rules, preserving Production subnet unchanged), Docker Engine/Compose initial runtime limited strictly to Caddy reverse proxy (`caddy:2-alpine`) and FastAPI gateway (`api`) with `ALLOW_DB_WRITES=false` initially (Application deployment, Docker, Caddy, FastAPI runtime, Supabase connectivity, DNS/TLS, Redis/Celery, and E2E NOT YET VERIFIED / NOT YET DEPLOYED), Redis/Celery background workers explicitly DEFERRED to Gate 8, Staging credentials (`ENVIRONMENT=staging`), Supabase Staging target (`mzpkdmaxsuhwezsooidu.supabase.co`), zero Production DB contact, E2E execution deferred, Caddy TLS termination, container rollback strategy, PostgREST 404 verification evidence, and Rule 21 documentation synchronization across `SYSTEM_ARCHITECTURE.md`, `ENVIRONMENTS.md`, `ORACLE_CLOUD_DEPLOYMENT.md`, `DISASTER_RECOVERY.md`, `JIRA_BACKLOG.md`. | 🟢 PO Approved | `8fcfdf0` | [MEASURED] OCI Staging VM provisioned and SSH access externally verified by Owner (129.225.86.241); staging subnet and security list active; 2.0 GiB swap, Docker 29.8.1, Compose v5.5.1 configured; .env mode 600 with ALLOW_DB_WRITES=false; Caddy and API gateway verified (0 restarts); external /health 200 OK and Staging Supabase read 404 verified; Production untouched; governed under UPA-1233. | PO Approved |

---

## 📌 Sprint 13: Administrative Access Hardening & Universal Routing Architecture (Planned)

> **Sprint Goal:** Implement true runtime cross-provider AI failover with universal canonical schema validation, harden remote cloud administrative access via stable private access mechanisms, and execute comprehensive verification of the end-to-end universal routing architecture (Client -> Vercel -> Caddy -> FastAPI, SSR routes, and public dynamic paths).

| Sprint Metadata | Details |
| :--- | :--- |
| **Sprint Number** | Sprint 13 |
| **Target Timeline** | Weeks 25–26 |
| **Total Story Points** | TBD |
| **Sprint Status** | 📋 **Planned** |
| **Showcase Document** | `docs/po-governance/showcases/SPRINT_13_PO_SHOWCASE.md` (To be initialized upon sprint activation) |

### 🎫 Sprint 13 Ticket Backlog

| ID | Title | Type | Priority | Acceptance criteria | Status | Commits | Evidence | PO verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **UPA-1240** | AI Provider Runtime Failover & Universal Schema Validation | Architecture / Reliability / AI Infrastructure | P1 | (1) `provider="auto"` reaches `ai_router.py` unchanged from worker without premature resolution; (2) runtime provider failure invokes next compatible provider in sequence; (3) Gemini -> Mistral -> Groq fallback sequence is comprehensively verified; (4) capability mismatches between multimodal, visual, and audio-only providers are detected; (5) `UniversalExtractionPayload` strict Pydantic model exists as the canonical contract; (6) valid provider output passes canonical validation before persistence or return; (7) invalid/incomplete output fails deterministically; (8) no-provider configuration (all credentials empty) fails explicitly and safely; (9) timeout, 429, and 5xx handling is bounded with loop prevention; (10) final failure state is safely reported when no compatible provider succeeds; (11) zero secrets appear in logs, errors, or telemetry results; (12) relevant automated regression suite passes; (13) relevant Staging E2E fallback evidence is captured where safely reproducible; (14) Rule 21 documentation synchronization is maintained across architecture docs; (15) Production promotion strictly gated upon explicit Product Owner approval under Rule 17.<br>**Affected files**: `backend/app/workers/tasks.py`, `backend/app/services/ai_router.py`, `backend/app/services/gemini_processor.py`, `backend/app/services/mistral_processor.py`, `backend/app/services/groq_processor.py`, `backend/app/models/extraction.py`, `docs/architecture/SYSTEM_ARCHITECTURE.md`, `docs/architecture/DISASTER_RECOVERY.md`.<br>**Applicable AGENTS.md rules**: Rules 2, 4, 6, 8, 10, 11, 13, 14, 16, 17, 21.<br>**Risks & Rollback**: Regression in extraction latency or provider selection. Rollback: Revert `ai_router.py` and `tasks.py` to previous verified commit.<br>**Test Plan**: 1. Test `provider="auto"` preservation in worker. 2. Unit test Gemini -> Mistral -> Groq failover cascade under timeout, 429, 5xx, and connection errors. 3. Test empty-credential explicit failure. 4. Test `UniversalExtractionPayload` schema validation on valid, malformed, and partial JSON. 5. Run full backend test suite (`pytest tests/`).<br>**Critical Dependency & Deferral Statement**: UPA-1240 is explicitly deferred until ALL current pending backlog items are completed and their applicable Rule 17 gates are closed. Current Gate 9 Staging verification remains separate. Current Production gate remains HOLD. This is future work; zero implementation begins as part of this backlog planning update. | 📋 Planned | Pending | Pending | Pending PO |
| **UPA-1301** | Staging Administrative Access Hardening & Private Management Access | Security / DevOps / Infrastructure | P1 | (1) Evaluate private administrative access options (including Tailscale / VPN / bastion-style approaches) against OCI Staging and future Production architecture without committing to vendor lock-in; (2) maintain least-privilege administrative access and define verified recovery/bootstrap procedures; (3) verify administrative connectivity from the owner workstation; (4) verify administrative access survives workstation public IPv4 changes and network transitions without requiring manual OCI Security List edits; (5) only after successful, verified private access is established and confirmed, remove reliance on direct public TCP/22 ingress; (6) under no circumstances weaken security by opening SSH / TCP 22 to `0.0.0.0/0`; (7) keep public application ingress ports 80/443 unchanged; (8) keep internal backend ports 8000 and 6379 externally inaccessible from the public internet.<br>**Affected files**: `docs/architecture/ORACLE_CLOUD_DEPLOYMENT.md`, `docs/architecture/DISASTER_RECOVERY.md`, `docs/architecture/SYSTEM_ARCHITECTURE.md`, `docs/architecture/ENVIRONMENTS.md`.<br>**Applicable AGENTS.md rules**: Rules 2, 5, 6, 14, 16, 17, 21.<br>**Risks & Rollback**: Misconfiguration could lock out SSH access. Rollback: OCI Cloud Shell / console connection or emergency OCI Security List update to current workstation IP.<br>**Test Plan**: 1. Deploy candidate private access agent in Staging test mode. 2. Verify private SSH session from owner workstation. 3. Test connectivity across workstation network IP switch. 4. Verify external public TCP 22 removal. 5. Confirm ports 80/443 remain publicly accessible and 8000/6379 remain shielded.<br>**Governance & Deferral Note**: Deferral to Sprint 13 is intentional. Current Gate 9 Staging verification remains separate. Current Production gate remains HOLD. This is future work; zero implementation begins as part of this backlog planning update. | 📋 Planned | Pending | Pending | Pending PO |
| **UPA-1302** | Universal Routing Architecture & End-to-End Path Verification | Architecture / Feature / DevOps | P1 | (1) Map and audit all active route definitions across Next.js rewrites (`frontend/next.config.mjs`), Vercel edge routing, Caddy reverse proxy (`Caddyfile`: `{$API_DOMAIN}` -> `reverse_proxy api:8000`), and FastAPI endpoint routing (`/api/v1/*`, `/health`, `/docs`); (2) validate the complete end-to-end request path flow (`Client -> Vercel Edge -> Caddy -> FastAPI`) with client IP preservation (`TRUSTED_PROXY=True`, `TRUSTED_PROXY_HOPS=2`); (3) verify public SSR recipe routes (`/r/[slug]`) and dynamic sitemap routing (`/sitemap.xml` / `/api/v1/public/sitemap`) against Staging Supabase without routing loops or proxy drops; (4) verify API routing under both direct API domain access and Next.js frontend proxy rewrites; (5) execute Staging-first validation across all routes before any Production rollout; (6) Production promotion strictly gated upon explicit Product Owner approval under Rule 17.<br>**Affected files**: `frontend/next.config.mjs`, `Caddyfile`, `frontend/src/app/r/[slug]/page.tsx`, `frontend/src/app/sitemap.ts`, `backend/app/api/v1/public_hub.py`, `docs/architecture/SYSTEM_ARCHITECTURE.md`, `docs/architecture/ORACLE_CLOUD_DEPLOYMENT.md`.<br>**Applicable AGENTS.md rules**: Rules 2, 5, 7, 14, 16, 17, 21.<br>**Risks & Rollback**: Incorrect proxy rewrite rules could break client-to-API requests or SSR pages. Rollback: Revert `next.config.mjs` / `Caddyfile` to previous verified commit.<br>**Test Plan**: 1. Audit route tables in Dev. 2. Verify all API and SSR routes in Staging environment. 3. Validate proxy headers (`X-Forwarded-For`, `X-Forwarded-Proto`, `Host`). 4. Run automated routing test suite in Staging.<br>**Governance & Deferral Note**: Deferral to Sprint 13 is intentional. Current Gate 9 Staging verification remains separate. Current Production gate remains HOLD. This is future work; zero implementation begins as part of this backlog planning update. | 📋 Planned | Pending | Pending | Pending PO |

---

## 📌 Sprint 13 Kanban Board (Planned)

| 📝 To Do | 🔨 In Progress | 🧪 Testing / Review | ✅ Done (0 pts) |
| :--- | :--- | :--- | :--- |
| `UPA-1240` AI Provider Runtime Failover & Universal Schema Validation<br>`UPA-1301` Staging Administrative Access Hardening & Private Management Access<br>`UPA-1302` Universal Routing Architecture & End-to-End Path Verification | None | None | None |

## 📌 Sprint 10 Kanban Board (Completed)

| 📝 To Do | 🔨 In Progress | 🧪 Testing / Review | ✅ Done (46 pts) |
| :--- | :--- | :--- | :--- |
| None | None | None | `UPA-1001` Instagram Downloader Multi-Attempt Fallback & Error Sanitization (`downloader.py` & `media_downloader.py`)<br>`UPA-1002` Minimalist Editorial UI Styling & Header FAQ Modal Overlay (`page.tsx` & `FaqSection.tsx`)<br>`UPA-1003` Mobile Responsive Search Bar & Touch Controls (`globals.css` & `page.tsx`)<br>`UPA-1004` Multimodal Audio Song & Track Title Identification (`gemini_processor.py`)<br>`UPA-1005` Multi-Language Spoken Audio Support & Dual-Language Notes Switcher (`gemini_processor.py` & `page.tsx`)<br>`UPA-1006` Travel Video Google Maps Directions Card (`gemini_processor.py` & `page.tsx`)<br>`UPA-1007` Multi-User Architecture & Daily Capacity Benchmark Metrics (`DISASTER_RECOVERY.md`)<br>`UPA-1008` Sprint 10 Automated Unit Test Suite (`tests/test_sprint10_beta_feedback.py`)<br>`UPA-1009` Intelligence Vault Auto-Save & Manual Bookmark Button (`page.tsx` & `VaultLibrary.tsx`)<br>`UPA-1010` Recipe Notes 3-Section Formatting & Buy Links Separation (`gemini_processor.py` & `page.tsx` & `tests/test_sprint10_recipe_formatting.py`) |

---

## 📌 Sprint 9 Kanban Board (Completed)

| 📝 To Do | 🔨 In Progress | 🧪 Testing / Review | ✅ Done (38 pts) |
| :--- | :--- | :--- | :--- |
| None | None | None | `UPA-901` Beta Quota Overrides (`quota_service.py`)<br>`UPA-902` Supabase `beta_telemetry_feed` Table Migration & RLS<br>`UPA-903` Real-Time Telegram Admin Telemetry Alerting (`telemetry_service.py`)<br>`UPA-904` Meta WhatsApp Cloud API Activation & Compact Outbound Formatter<br>`UPA-905` Gemini 3.8 Flash Indian Regional & Hinglish Prompt Tuning<br>`UPA-906` Telegram Bot Inline Feedback Keyboards & Failure Tags<br>`UPA-907` Safari-Resilient Mobile Clipboard Component (`CopyShoppingChecklist.tsx`)<br>`UPA-908` Dual-Bot Ingestion Hero Callouts & FAQ Module 14 (`FaqSection.tsx` & `page.tsx`)<br>`UPA-909` Wave 1 (Break-It) & Wave 2 (Utility) Beta Cohort Rollout & GTM Matrix |

---

## 📌 Sprint 8 Kanban Board (Completed)

| 📝 To Do | 🔨 In Progress | 🧪 Testing / Review | ✅ Done (24 pts) |
| :--- | :--- | :--- | :--- |
| None | None | None | `UPA-806` Impeccable Contrast Ratio & Color Harmony Refinement<br>`UPA-807` Ghost-Card Anti-Pattern Cleanup & Surface Separation<br>`UPA-808` Typographic Balance & Line Length Optimization (`text-wrap: balance`)<br>`UPA-809` Accessibility Motion Safeguard (`prefers-reduced-motion`)<br>`UPA-810` Persistent UI/UX Audit Directory (`ui-ux-audits/`) |

---

## 📌 Sprint 7 Kanban Board (Completed)

| 📝 To Do | 🔨 In Progress | 🧪 Testing / Review | ✅ Done (23 pts) |
| :--- | :--- | :--- | :--- |
| None | None | None | `UPA-801` Title Sanitization Utility (`formatCleanTitle`)<br>`UPA-802` One-Click Sample Reel Activation & Auto-Execution<br>`UPA-803` Omnichannel Telegram Bot Badge (`@UniversalProAIBot`)<br>`UPA-804` Auto-Dismissing Error State Hygiene<br>`UPA-805` Fast AI Socket Timeout & Failover Cascade |

---

## 📌 Sprint 2 Kanban Board (Completed)

| 📝 To Do | 🔨 In Progress | 🧪 Testing / Review | ✅ Done (34 pts) |
| :--- | :--- | :--- | :--- |
| None | None | None | `UPA-201` Upstash Redis & Celery Worker Container<br>`UPA-202` Worker Media Downloader (360p & Disk Cleanup)<br>`UPA-203` Residential Proxy Rotation Middleware<br>`UPA-204` Multimodal AI Worker Pipeline & Fallbacks<br>`UPA-205` Supabase Persistence & Quota Accounting<br>`UPA-301` Multi-Store Affiliate Link Engine<br>`UPA-302` 10-Minute Quick-Commerce Cart Deep Search |

---

## 📌 Sprint 1 Kanban Board (Completed)

| 📝 To Do | 🔨 In Progress | 🧪 Testing / Review | ✅ Done (26 pts) |
| :--- | :--- | :--- | :--- |
| None | None | None | `UPA-001` Streamlit Prototype & Live Deployment<br>`UPA-002` Multi-Store Affiliate Links Engine<br>`UPA-003` 30-Test Automated Test Suite<br>`UPA-004` 3-Tier Environments & CI/CD Pipeline<br>`UPA-101` Supabase Schema Migration (001)<br>`UPA-102` Row Level Security Policies<br>`UPA-103` SHA-256 URL Hash Cache Index<br>`UPA-104` FastAPI Modular Backend Skeleton<br>`UPA-105` Supabase Auth & JWT Middleware<br>`UPA-106` Job Enqueue Endpoint (`/v1/extract`)<br>`UPA-107` Task Polling & Progress Endpoint (`/status/{job_id}`) |

---

## 🎯 Epics Breakdown

```
[EPIC 0: DevOps & CI/CD] ──> [EPIC 1: Data Layer] ──> [EPIC 2: API Gateway] ──> [EPIC 3: Worker Queue]
                                                                                       │
                                                                                       ▼
[EPIC 7: Monetization] <── [EPIC 6: Next.js PWA] <── [EPIC 5: Mobile Bots] <── [EPIC 4: Commerce Engine]
```

* **EPIC-0 (`UPA-E0`)**: DevOps, CI/CD Pipeline & 3-Tier Multi-Environment Architecture (Dev -> Staging -> Prod)
* **EPIC-1 (`UPA-E1`)**: Multi-Tenant Data Layer & Database Architecture (Supabase / PostgreSQL)
* **EPIC-2 (`UPA-E2`)**: Decoupled Asynchronous API Gateway (FastAPI)
* **EPIC-3 (`UPA-E3`)**: High-Concurrency Async Media Worker & Extraction Pipeline (Celery + Redis)
* **EPIC-4 (`UPA-E4`)**: Contextual Multi-Store Commerce & Quick-Delivery Router
* **EPIC-5 (`UPA-E5`)**: Zero-Friction Mobile Chat Ingestion (Telegram & WhatsApp Cloud Webhooks)
* **EPIC-6 (`UPA-E6`)**: Modern Client Frontend & PWA (Next.js 15 App Router)
* **EPIC-7 (`UPA-E7`)**: Billing, Daily Quotas & Subscription Infrastructure (Razorpay + Stripe)

---

## 📝 User Stories Backlog

### 🛠️ EPIC-0: DevOps, CI/CD & 3-Tier Multi-Environment Infrastructure

#### `UPA-004`: 3-Tier Multi-Environment Architecture & CI/CD Pipeline
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a devops engineer, I want isolated Development, Staging, and Production environments backed by automated GitHub Actions CI and pre-promotion gates, so that untested code never breaks the live production site.*
- **Acceptance Criteria**:
  - [x] Permanent `staging` branch created on GitHub (`origin/staging`).
  - [x] Automated GitHub Actions CI workflow (`.github/workflows/ci.yml`) runs on pushes/PRs to `Dev`, `staging`, `main`.
  - [x] Pre-promotion verification script (`scripts/verify_promotion.py`) validates syntax, clean isolated module imports, and 30 unit tests.
  - [x] Branch promotion script (`scripts/promote.py`) safely merges `Dev -> staging` and `staging -> main` after running verification gates.
- **Dependencies**: None.

---

### 🏢 EPIC-1: Multi-Tenant Data Layer & Database Architecture (Supabase / PostgreSQL)

#### `UPA-101`: Provision Managed PostgreSQL Schema on Supabase
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a systems engineer, I want a structured PostgreSQL database with tables for profiles, extractions, and affiliate clicks, so that user state and extraction results are permanently stored.*
- **Acceptance Criteria**:
  - [x] Tables created in `database/001_initial_schema.sql`: `profiles`, `extractions`, `affiliate_clicks`.
  - [x] `uuid-ossp` and `pgcrypto` extensions activated for default UUID generation.
  - [x] Foreign keys established with `ON DELETE CASCADE` or `SET NULL` as appropriate.
  - [x] Automated unit tests in `tests/test_database_schema.py` validate syntax and JSON schema compliance.
- **Dependencies**: None.

#### `UPA-102`: Implement Row Level Security (RLS) Policies
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 3 pts | **Status**: `[x] DONE`
- **User Story**: *As a user, I want my saved extractions and profile to be private, so that other users cannot read or tamper with my data.*
- **Acceptance Criteria**:
  - [x] RLS enabled on `profiles`, `extractions`, and `affiliate_clicks`.
  - [x] Policy added: Users can view and update only their own profile (`auth.uid() = id`).
  - [x] Policy added: Users can read and insert only their own extractions (`auth.uid() = user_id or is_public = true`).
  - [x] Unauthorized cross-user reads return zero records.
- **Dependencies**: `UPA-101`.

#### `UPA-103`: SHA-256 URL Hash Indexing for Instant Extraction Cache
- **Type**: Story | **Priority**: P1 (High) | **Points**: 3 pts | **Status**: `[x] DONE`
- **User Story**: *As a platform operator, I want incoming URLs to be hashed and indexed, so that duplicate requests for viral reels return instantly from cache without re-running costly AI models.*
- **Acceptance Criteria**:
  - [x] Column `url_hash` indexed with standard B-Tree index on `public.extractions`.
  - [x] Hash generation verified with deterministic 64-character SHA-256 digest in `tests/test_database_schema.py`.
  - [x] Cloud AI and proxy costs avoided on cached extractions.
- **Dependencies**: `UPA-101`.

---

### ⚡ EPIC-2: Decoupled Asynchronous API Gateway (FastAPI)

#### `UPA-104`: Scaffold FastAPI Modular Backend Skeleton
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 3 pts | **Status**: `[x] DONE`
- **User Story**: *As a backend developer, I want a clean FastAPI directory structure, so that API routes, services, workers, and core configuration are logically separated.*
- **Acceptance Criteria**:
  - [x] Directory layout created under `backend/app/` (`api/v1/`, `core/`, `workers/`, `services/`).
  - [x] `main.py` boots cleanly with CORS middleware, health check (`/health`), and OpenAPI docs enabled (`/docs`).
  - [x] Environment settings managed via `pydantic-settings` with automatic `.env` discovery.
  - [x] 5 automated unit tests in `tests/test_api_gateway.py` validate endpoints, CORS, and settings.
- **Dependencies**: None.

#### `UPA-105`: Supabase Auth & JWT Verification Middleware
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a client app, I want to authenticate against FastAPI using Supabase JWT Bearer tokens, so that all protected endpoints identify the active user securely.*
- **Acceptance Criteria**:
  - [x] `get_current_user` dependency in `backend/app/core/security.py` validates Supabase JWT Bearer token claims.
  - [x] Inactive, malformed, or expired tokens return HTTP 401 Unauthorized.
  - [x] Anonymous guest mode supported with fallback guest UUID and 3 free trial daily quota.
  - [x] `backend/app/core/supabase_client.py` provides resilient direct REST client for profiles, cache lookups, and quota RPC.
  - [x] 4 unit tests in `tests/test_auth_security.py` validate guest sessions, JWT decoding, and 401 rejection.
- **Dependencies**: `UPA-104`.

#### `UPA-106`: Job Enqueue Endpoint (`POST /v1/extract`)
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a client, I want to submit a social video URL and receive a `job_id` within 300ms, so that my app never freezes during 20-second video processing.*
- **Acceptance Criteria**:
  - [x] Endpoint validates URL via `pydantic.field_validator` and regex.
  - [x] Checks and decrements daily quota for free-tier users (HTTP 429 when quota exceeded).
  - [x] Computes `url_hash` (SHA-256) and returns instant 0-cost cache hit (HTTP 200).
  - [x] On cache miss, enqueues background extraction and returns HTTP 202 Accepted with `job_id`, `status: "queued"`, and `poll_url`.
- **Dependencies**: `UPA-104`, `UPA-105`.

#### `UPA-107`: Task Polling & Progress Endpoint (`GET /v1/extract/status/{job_id}`)
- **Type**: Story | **Priority**: P1 (High) | **Points**: 2 pts | **Status**: `[x] DONE`
- **User Story**: *As a client frontend, I want to poll job progress stages, so that I can show dynamic status indicators (downloading, AI scanning, complete) to the user.*
- **Acceptance Criteria**:
  - [x] Queries in-memory thread-safe `JobManager` state (`queued`, `downloading`, `processing`, `completed`, `failed`).
  - [x] Returns current stage metadata (`downloading_media`, `multimodal_ai_inference`, etc.) and progress percentage.
  - [x] When completed, returns full structured JSON payload.
  - [x] Fallback query to Supabase `extractions` table by ID if job evicted from memory.
  - [x] Returns HTTP 404 for unknown job IDs.
- **Dependencies**: `UPA-106`.

---

### ⚙️ EPIC-3: High-Concurrency Async Media Worker & Extraction Pipeline (Celery + Redis)

#### `UPA-201`: Configure Upstash Redis & Celery Worker Container
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a DevOps engineer, I want Celery configured with Upstash Redis, so that background workers can process jobs asynchronously across cloud instances.*
- **Acceptance Criteria**:
  - [x] Celery app initialized with Redis broker and result backend (`backend/app/workers/celery_app.py`).
  - [x] Hard task execution timeout set to 180 seconds.
  - [x] Worker processes tasks and tracks execution start state.
- **Dependencies**: `UPA-104`.

#### `UPA-202`: Worker Media Downloader with 360p Limit & Disk Cleanup
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a worker process, I want to download video streams using 360p resolution limits and auto-cleanup temporary files, so that server disk space is never exhausted.*
- **Acceptance Criteria**:
  - [x] `yt-dlp` configured with `bestvideo[height<=360]+bestaudio/best[height<=360]`.
  - [x] Maximum download size capped at 50 MB.
  - [x] Downloaded file deleted in `finally:` block regardless of task success or failure (`managed_worker_download`).
- **Dependencies**: `UPA-201`.

#### `UPA-203`: Residential Proxy Rotation Middleware for `yt-dlp`
- **Type**: Story | **Priority**: P1 (High) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a scraping worker, I want outbound downloads routed through rotating residential proxies, so that Instagram and TikTok never trigger HTTP 429 rate limit blocks.*
- **Acceptance Criteria**:
  - [x] `RESIDENTIAL_PROXY_URL` injected into `ydl_opts['proxy']`.
  - [x] Automatic retry logic if proxy drops connection (`ProxyRotator`).
  - [x] Local fallback mode maintained for local development (`.env` toggle).
- **Dependencies**: `UPA-202`.

#### `UPA-204`: Port Multimodal AI Processor with Whisper/Keyframe Fallback
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 8 pts | **Status**: `[x] DONE`
- **User Story**: *As an extraction engine, I want to analyze videos via Gemini 2.5 Flash, and automatically fall back to Whisper audio transcription + Vision keyframes if direct video upload fails.*
- **Acceptance Criteria**:
  - [x] Primary path: Direct Gemini 2.5 Flash video upload via Files API.
  - [x] Fallback path: Keyframe extraction + Groq/Whisper transcription if video upload is unsupported.
  - [x] Strict JSON schema enforced across all domains (`recipe`, `product_gadget`, `tech_diy`, `fitness_workout`, `travel_guide`).
- **Dependencies**: `UPA-202`.

#### `UPA-205`: Save Extraction Results to Supabase Database
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 3 pts | **Status**: `[x] DONE`
- **User Story**: *As a worker, I want completed extraction JSON saved to Supabase, so that user libraries and public cache remain synchronized.*
- **Acceptance Criteria**:
  - [x] Successful extraction updates row in `extractions` table (`status = 'completed'`).
  - [x] User's `extractions_today` counter incremented via atomic RPC function.
  - [x] Error messages captured and logged on task failure (`status = 'failed'`).
- **Dependencies**: `UPA-101`, `UPA-204`.

---

### 🛒 EPIC-4: Contextual Multi-Store Commerce & Quick-Delivery Router

#### `UPA-301`: Affiliate Link Generator Engine
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a business owner, I want every extracted item converted into monetized Amazon and EarnKaro links, so that the platform earns affiliate revenue.*
- **Acceptance Criteria**:
  - [x] Amazon links formatted with tag `manasdas11155-21`.
  - [x] Flipkart and Meesho links wrapped through EarnKaro redirect with ID `5608766`.
  - [x] Pro and Creator tier users can override default tags with their own custom affiliate credentials.
- **Dependencies**: `UPA-101`.

#### `UPA-302`: 10-Minute Quick-Commerce Cart Deep Search
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 3 pts | **Status**: `[x] DONE`
- **User Story**: *As an Indian user extracting a recipe, I want 1-click search buttons for Blinkit, Zepto, and Swiggy Instamart, so that I can order missing ingredients in 10 minutes.*
- **Acceptance Criteria**:
  - [x] Deep search URLs generated for Blinkit, Zepto, and Instamart with URL-encoded item names.
  - [x] Unit tested against special characters, spices, and brand names.
- **Dependencies**: None.

#### `UPA-303`: Click-Through Analytics Logging
- **Type**: Story | **Priority**: P1 (High) | **Points**: 3 pts | **Status**: `[x] DONE`
- **User Story**: *As a business analyst, I want outbound merchant clicks recorded in `affiliate_clicks`, so that I can track conversion rate and EPC (Earnings Per Click).*
- **Acceptance Criteria**:
  - [x] `/v1/affiliate/redirect` redirects to merchant while inserting event into `affiliate_clicks`.
  - [x] Captures `merchant`, `target_url`, `user_id`, and `extraction_id`.
  - [x] Analytics aggregation endpoint `GET /v1/affiliate/analytics` active.
- **Dependencies**: `UPA-101`, `UPA-301`.

---

### 💬 EPIC-5: Zero-Friction Mobile Chat Ingestion (Telegram & WhatsApp)

#### `UPA-401`: Telegram Ingestion Bot MVP (Instant Launch)
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a mobile user, I want to forward a reel to a Telegram bot and get my recipe notes within 15 seconds, so that I don't have to open a browser.*
- **Acceptance Criteria**:
  - [x] Telegram Bot initialized using `python-telegram-bot` or FastAPI webhook.
  - [x] Listens for Instagram, TikTok, and YouTube URLs.
  - [x] Dispatches extraction job to Celery worker.
  - [x] Sends back structured message with interactive inline buttons (`🛒 Buy Ingredients`, `📝 View Steps`).
- **Dependencies**: `UPA-106`, `UPA-204`.

#### `UPA-402`: WhatsApp Cloud API Webhook Integration
- **Type**: Story | **Priority**: P1 (High) | **Points**: 8 pts | **Status**: `[x] DONE`
- **User Story**: *As a mainstream user, I want to share reels directly to a WhatsApp business contact, so that I get structured summaries natively in my chat.*
- **Acceptance Criteria**:
  - [x] Webhook verification handshake implemented (`hub.mode`, `hub.verify_token`).
  - [x] Incoming messages acknowledged with HTTP 200 within 2 seconds.
  - [x] Background worker sends reply payload via Meta Graph API v19.0.
- **Dependencies**: `UPA-106`, `UPA-204`.

---

### 🌐 EPIC-6: Modern Client Frontend & PWA (Next.js 15)

#### `UPA-501`: Next.js 15 App Router Project Skeleton & Theme
- **Type**: Story | **Priority**: P1 (High) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a user, I want a blazing fast, dark-mode luxury web app, so that the extraction interface feels premium and state-of-the-art.*
- **Acceptance Criteria**:
  - [x] Next.js 15 initialized with TypeScript, Lucide icons, and luxury dark glassmorphism system tokens (`#0A0E1A`, `#10B981`, `#FF416C`).
  - [x] Consistent dark theme matching Universal Pro AI palette.
  - [x] Responsive dual-column layout on mobile and desktop viewports with docked player.
- **Dependencies**: None.

#### `UPA-502`: Native PWA Manifest & Web Share Target
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a mobile user, I want Universal Pro AI in my phone's "Share via..." menu, so that sharing a reel from Instagram opens the extractor automatically.*
- **Acceptance Criteria**:
  - [x] `manifest.json` configured with `share_target` pointing to `/share-target`.
  - [x] `/share-target/page.tsx` parses incoming URL and triggers extraction immediately.
  - [x] PWA service worker registered for offline caching, asset persistence, and standalone display.
- **Dependencies**: `UPA-501`.

#### `UPA-503`: "My Vault / Library" Persistent User Dashboard & Serving Scaler
- **Type**: Story | **Priority**: P1 (High) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a registered user, I want a searchable library of all my past extractions, so that I never lose recipes, itineraries, or workout routines.*
- **Acceptance Criteria**:
  - [x] Grid and list views of past extractions with category badges (`GET /api/v1/library`).
  - [x] Full-text search over titles, ingredients, and steps with deletion (`DELETE /api/v1/library/{id}`).
  - [x] Export endpoints for Markdown, plain text, and JSON (`GET /api/v1/library/{id}/export`).
  - [x] ServingAdjuster component scaling ingredients from 1–12 portions with 1-click quick-commerce purchase.
- **Dependencies**: `UPA-102`, `UPA-501`.

---

### 💳 EPIC-7: Billing, Daily Quotas & Subscription Infrastructure

#### `UPA-601`: Redis-Backed Daily Quota Middleware
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 3 pts | **Status**: `[x] DONE`
- **User Story**: *As a SaaS operator, I want free users limited to 3 extractions per day, so that API inference costs remain protected.*
- **Acceptance Criteria**:
  - [x] Redis key `quota:{user_id}:{YYYY-MM-DD}` tracks daily usage.
  - [x] Key auto-expires after 24 hours.
  - [x] Extraction attempts exceeding quota return HTTP 429 with upgrade CTA.
  - [x] Pro and Business tiers bypass quota limits.
- **Dependencies**: `UPA-201`.

#### `UPA-602`: Razorpay Subscription Webhook & UPI AutoPay (India)
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As an Indian user, I want to upgrade to Pro (₹299/month) using UPI AutoPay, so that I enjoy unlimited extractions seamlessly.*
- **Acceptance Criteria**:
  - [x] Razorpay checkout session endpoint created for plan `plan_pro_299_inr`.
  - [x] Webhook listener handles `subscription.activated` and upgrades user tier in Supabase.
  - [x] Webhook verifies HMAC-SHA256 signature against `RAZORPAY_WEBHOOK_SECRET`.
  - [x] Handles `subscription.halted` / payment failure by safely downgrading to free tier.
- **Dependencies**: `UPA-101`, `UPA-104`.

#### `UPA-603`: Stripe Billing Integration (Global Users)
- **Type**: Story | **Priority**: P1 (High) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As an international user, I want to subscribe at $4.99/month via Credit Card or Apple Pay, so that I can use the tool globally.*
- **Acceptance Criteria**:
  - [x] Stripe Customer Portal and Checkout Session configured.
  - [x] Stripe webhook listener handles `customer.subscription.created` and `deleted`.
  - [x] HMAC-SHA256 signature verification enforced for all Stripe webhooks.
- **Dependencies**: `UPA-101`, `UPA-104`.

---

### 🌐 EPIC-8: Creator Program, SEO Growth Engine & Telemetry (Sprint 6)

#### `UPA-701`: Organic SEO Hub & Dynamic SSR Recipe Pages (`/r/[slug]`)
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 8 pts | **Status**: `[x] DONE`
- **User Story**: *As an organic search user, I want public recipe pages to load fast with Google Recipe rich snippet schema, so that I find structured recipes with 1-click buy buttons directly from search engines.*
- **Acceptance Criteria**:
  - [x] Next.js SSR route (`/r/[slug]`) rendering structured recipes with dark obsidian aesthetic.
  - [x] Google-compliant Schema.org `Recipe` JSON-LD embedded into page head.
  - [x] Dynamic sitemap (`sitemap.xml`) generated via `sitemap.ts`.
  - [x] Embedded interactive portion scaler (`ServingAdjuster`) with Amazon and Zepto 1-click carting.
- **Dependencies**: `UPA-501`, `UPA-503`.

#### `UPA-702`: Creator Custom Affiliate Tag Vault
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a content creator, I want to save my personal Amazon Associate and EarnKaro IDs in my profile, so that recipe links I share earn 100% of commissions for my brand.*
- **Acceptance Criteria**:
  - [x] Profile update endpoint `PATCH /api/v1/auth/profile` persists `custom_amazon_tag` and `custom_earnkaro_id`.
  - [x] `AffiliateEngine` dynamically injects creator tags into outbound e-commerce links.
  - [x] Immutable default tag constants preserved as fallback whenever creator tags are empty.
  - [x] Next.js `CreatorTagVault.tsx` settings drawer connected.
- **Dependencies**: `UPA-105`, `UPA-301`.

#### `UPA-703`: Growth Telemetry & Conversion Funnel Reporting
- **Type**: Story | **Priority**: P1 (High) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a product manager, I want to track user conversion across the 5-stage product funnel, so that I can monitor drop-off rates and optimize SaaS conversion.*
- **Acceptance Criteria**:
  - [x] Telemetry event ingestion endpoint `POST /api/v1/telemetry/event` active.
  - [x] Conversion funnel analytics endpoint `GET /api/v1/telemetry/funnel` active.
  - [x] Next.js `UpgradeModal.tsx` intercepts HTTP 429 quota exhaustion with dual-rail currency switch (Razorpay ₹299 vs Stripe $4.99).
- **Dependencies**: `UPA-601`, `UPA-602`, `UPA-603`.

---

### 🎨 EPIC-9: UX Activation, Title Sanitization & Model Resilience (Sprint 7)

#### `UPA-801`: Title Sanitization Utility (`formatCleanTitle`)
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a user, I want extracted recipe and tutorial titles to be formatted cleanly without raw underscores or AI prefix phrases, so that notes look professional and easy to read.*
- **Acceptance Criteria**:
  - [x] `formatCleanTitle` utility function added to `frontend/src/app/page.tsx`.
  - [x] Strips raw AI prefixes (`This_video_is_a_recipe_tutorial_for_`, `Video_of_`) and replaces `_` with spaces.
  - [x] Renders headings in clean Title Case across result headers, ServingAdjuster, and export notes.
- **Dependencies**: `UPA-501`.

#### `UPA-802`: One-Click Sample Reel Activation & Auto-Execution
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 5 pts | **Status**: `[x] DONE`
- **User Story**: *As a first-time visitor without a reel link copied, I want to click a sample chip to instantly test sub-3s extraction without having to click the Extract button again.*
- **Acceptance Criteria**:
  - [x] Sample chip click populates input field AND automatically invokes `handleExtract(sampleUrl)`.
  - [x] Updated sample list with working Instagram Reel link (`https://www.instagram.com/reel/DdGvPs9zhVu/`).
- **Dependencies**: `UPA-501`.

#### `UPA-803`: Omnichannel Telegram Bot Badge (`@UniversalProAIBot`)
- **Type**: Story | **Priority**: P1 (High) | **Points**: 3 pts | **Status**: `[x] DONE`
- **User Story**: *As a mobile user, I want to see a direct link to the Telegram bot on the hero landing page, so that I can extract recipes directly inside mobile messaging apps.*
- **Acceptance Criteria**:
  - [x] Hero section displays `@UniversalProAIBot` badge linked to `https://t.me/UniversalProAIBot`.
- **Dependencies**: `UPA-401`.

#### `UPA-804`: Auto-Dismissing Error State Hygiene
- **Type**: Story | **Priority**: P1 (High) | **Points**: 3 pts | **Status**: `[x] DONE`
- **User Story**: *As a user, I want old error alert banners to disappear as soon as I start a new extraction, so that stale errors do not obscure my new results.*
- **Acceptance Criteria**:
  - [x] `handleExtract` clears `setError(null)` at the beginning of every extraction.
- **Dependencies**: `UPA-501`.

#### `UPA-805`: Fast AI Socket Timeout & Failover Cascade
- **Type**: Story | **Priority**: P0 (Blocker) | **Points**: 7 pts | **Status**: `[x] DONE`
- **User Story**: *As a platform operator, I want network timeouts on primary AI models to trigger instant failover to backup models, so that total extraction SLA stays under 10 seconds.*
- **Acceptance Criteria**:
  - [x] `gemini_processor.py` `is_busy` condition updated to handle `"timeout"` and `"timed out"`.
  - [x] Socket timeouts on `gemini-3.8-flash` failover instantly to `gemini-3.7-flash`.
- **Dependencies**: `UPA-204`.

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
