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
| **Rule 13** | Regional & Hinglish Culinary Prompt Invariants | 🟢 **COMPLIANT** | `gemini_processor.py:36` (`1 katori -> 1 bowl (~150 ml, approx)`), `AGENTS.md:87` updated, `tests/test_hinglish_prompt_snapshot.py:21` (1 passed), `scalingEngine.test.ts` (Rule 13 2x volume scaling passed) |
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
| **UPA-1201** | Entry Point SSRF & Pre-existing Test Audit (T1) | Security / Tests | P0 | Audit diff base `git diff 451b20e~1 HEAD -- tests frontend/src`; verify `validate_url_and_follow_redirects` rejects hosts resolving to private IPs (`127.0.0.1`, `169.254.169.254`); add NEW test in `tests/test_ssrf_entrypoint.py` without editing existing tests.<br>**Risks & Rollback**: Test failure if external DNS lookup blocks. Rollback: revert `tests/test_ssrf_entrypoint.py`.<br>**Test Plan**: Run `pytest tests/test_ssrf_entrypoint.py`. | 🟢 APPROVED NOW (Step 3) | Pending | Pending | Pending PO |
| **UPA-1202** | Secret Hygiene, Fallback Removal & Environment Gate (T2) | Security | P0 | Remove ALL constant fallbacks for `SECRET_KEY`, `RAZORPAY_*`, `STRIPE_*`, `WHATSAPP_VERIFY_TOKEN`, `universal_pro_default_secret_key` across `url_validator.py`, `extract.py`, `library.py`, `config.py`; `DEBUG` default False; `CORS_ORIGINS` from env (no `*`); non-dev envs treated as production; local `.env` required for dev (`ENVIRONMENT=development` requires `SECRET_KEY` from `.env`); state how `pytest` sets `ENVIRONMENT=test` via `tests/conftest.py` without editing existing tests; list existing tests relying on defaults for approval; split secrets into REQUIRED at startup vs FEATURE-GATED (503 if unset); document `CORS_ORIGINS` and all new env vars in `.env.example` and `DISASTER_RECOVERY.md`; standardize `TELEGRAM_BOT_TOKEN` & `TELEGRAM_WEBHOOK_SECRET`.<br>**Risks & Rollback**: App fails to start if `.env` missing required key. Rollback: restore `.env.example` template.<br>**Test Plan**: Run `pytest tests/test_config_secrets.py`. | 🟢 Verified on Dev (Step 5) | Committed in Commit 3 | `pytest tests/test_config_secrets.py` (3/3 passed); `pytest tests/` (234/234 passed in 24.34s) [MEASURED] | Pending PO |
| **UPA-1203** | Retire Streamlit App (T3) | Security / Tech-debt | P1 | Build import graph first. Delete ONLY files with no importers from API, workers, bots, or tests (`streamlit_app.py`). Do NOT delete shared root modules (e.g. `downloader.py`) that API imports. Grep shared modules for `import streamlit`. List existing tests importing Streamlit app for approval. Remove `streamlit` from `requirements.txt`. Update DR, user manual, backlog docs. Owner will pause/delete Streamlit Cloud apps separately.<br>**Risks & Rollback**: Accidental deletion of shared helper module. Rollback: `git checkout backend/app/services/streamlit_app.py`.<br>**Test Plan**: Run `pytest tests/` to confirm zero import failures. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1204** | Rate Limiter & Sliding Window Audit (T4) | Security / Tech-debt | P1 | Absorbed into `UPA-1214`. Audit time-bucket key structure `rate_limit:{key}:{bucket}`.<br>**Risks & Rollback**: N/A.<br>**Test Plan**: See UPA-1214. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1205** | IP Pinning & PinnedHTTPSConnection Wire-Up (T6) | Security | P0 | Subclass `PinnedHTTPSConnection(http.client.HTTPSConnection)` with `server_hostname=self.host`; re-check inside `connect()` that pinned IP is global (`ip.is_global`); wire into real server-side fetches of user/remote-derived URLs (oEmbed/thumbnails) or delete if none (`stream_video` uses yt-dlp so nothing to wire there); make `validate_url_and_follow_redirects` fail closed, validate every hop, no second resolution, run DNS off event loop; add `tests/test_pinned_https.py` with `trustme` TLS test.<br>**Risks & Rollback**: SNI validation failure on custom domain certs. Rollback: revert `url_validator.py`.<br>**Test Plan**: Run `pytest tests/test_pinned_https.py`. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1206** | Container Network Egress Firewall & Rollback Protocol (T5) | Security | P0 | Rules use `-s <compose subnet> -d <private range>` with `REJECT` so inbound traffic is untouched; compose-to-compose `RETURN` before private range rejects (compose subnet `172.28.0.0/16` is inside `172.16/12`); allowed traffic returns with `RETURN`; add `ip6tables`; idempotent, persistent across reboot; DNS-from-container test script (`scripts/verify_egress.py`); rollback script `iptables -F DOCKER-USER && iptables -A DOCKER-USER -j RETURN`; mark **NOT VERIFIED** until owner runs on Linux test host with console access.<br>**Risks & Rollback**: Blocking DNS or Upstash broker traffic. Rollback: run rollback script `iptables -F DOCKER-USER && iptables -A DOCKER-USER -j RETURN`.<br>**Test Plan**: Run `deploy/setup_egress_firewall.sh` on Linux test host and run container DNS test. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1207** | Dependencies, Clean Venv, Lock File & Audit (T7) | Tech-debt / Security | P1 | Perform import scan for runtime backend packages in `requirements.txt` (drop `streamlit`); place dev/test tools (`pytest`, `trustme`, `fakeredis`) in `requirements-dev.txt`; build clean venv on Docker Python image; generate `requirements.lock`; run `pip-audit`; confirm container boots & pytest passes.<br>**Risks & Rollback**: Missing transitive dependency in lockfile. Rollback: revert `requirements.txt`.<br>**Test Plan**: Build Docker image and run `pip-audit`. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1208** | Secret Scan & Repository History Audit (T8) | Security | P0 | Read-only scan. Run `gitleaks` with `--redact` (or `trufflehog` if output excludes secret values) over all refs across full git history. If tool not installed, report missing tool without silently substituting weaker scan. Report findings by file & rule name in `docs/po-governance/SECURITY_AUDIT_REPORT.md` without printing secret values. If ANYTHING found, STOP after scan and report to owner before starting next ticket. Do NOT commit report file if findings exist.<br>**Risks & Rollback**: Read-only scan. Zero risk to codebase.<br>**Test Plan**: Execute `gitleaks detect --redact --verbose`. | 🟢 APPROVED NOW (Step 1) | Pending | Pending | Pending PO |
| **UPA-1209** | VaultLibrary React Component Test | Tech-debt / Tests | P1 | Create `frontend/src/components/__tests__/VaultLibrary.test.tsx` using jsdom + RTL testing `<VaultLibrary />` rendering & re-hydration with generic placeholder affiliate tags (`tag=MOCK_TAG`); list pre-existing `vaultRehydration.test.ts` for owner deletion sign-off.<br>**Risks & Rollback**: DOM selection timeout in RTL. Rollback: revert test file.<br>**Test Plan**: Run `npm test`. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1210** | Hinglish Prompt Evaluation Standard | Docs | P2 | Mark existing prompt snapshot strings as `ILLUSTRATIVE` and Hinglish golden set benchmark as `NOT VERIFIED` until live API evaluation is conducted against 3–5 fixed reels or transcripts.<br>**Risks & Rollback**: Documentation update only.<br>**Test Plan**: Review documentation text. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1211** | PO Governance Document Audit | Docs | P2 | Grep codebase docs for `\[ ?✅ ?\]`, `Approved for Production`, `APPROVAL` and list all line numbers without editing files.<br>**Risks & Rollback**: Read-only documentation audit.<br>**Test Plan**: Execute grep search. | 🟢 APPROVED NOW (Step 2) | Pending | Pending | Pending PO |
| **UPA-1212** | JWT ES256 JWKS Signature Verification & Audience Guard | Security | P0 | Asymmetric keys, verified via JWKS. Config settings: `SUPABASE_JWKS_URL`, `SUPABASE_JWT_ISSUER`, `SUPABASE_JWT_AUDIENCE = "authenticated"`, `SUPABASE_JWT_ALGORITHMS = ["ES256"]`. Derive JWKS URL (`{SUPABASE_URL}/auth/v1/.well-known/jwks.json`) and issuer (`{SUPABASE_URL}/auth/v1`) dynamically from `SUPABASE_URL` so each environment uses its own project. Fetch JWKS with caching and timeout (`jwt.PyJWKClient`), match `kid`, re-fetch on unknown `kid` with rate-limit. Reject `HS256`, `none`, and any other algorithm in production. Require `exp`, `sub`, `aud="authenticated"`. NEVER take `role` or `plan` from token claims (plan comes from DB profile only). Do NOT add a shared-secret setting, and do NOT touch or revoke any Supabase key. New tests: generate local EC P-256 key pair (`cryptography.hazmat`) and mock JWKS response in `tests/test_jwt_verification.py` (forged signature, expired, wrong audience, `alg=none`, `HS256` token rejected in prod, valid `ES256` token). List existing tests minting unsigned tokens and STOP for owner approval. Document new settings in `.env.example` and `DISASTER_RECOVERY.md`.<br>**Risks & Rollback**: Rejection of invalid tokens in dev tests. Rollback: revert `security.py`.<br>**Test Plan**: Run `pytest tests/test_jwt_verification.py`. | 🟢 Verified on Dev (Step 4) | Committed in Commit 4 | `pytest tests/test_jwt_verification.py tests/test_auth_security.py` (10/10 passed); `pytest tests/` (234/234 passed in 24.34s) [MEASURED] | Pending PO |
| **UPA-1213** | Stream Proxy Token Security & Media Hardening | Security | P0 | Token = `<exp>.<sig>`, sig = `HMAC-SHA256(secret, f"{id}\|{sha256(url)}\|{exp}")`, TTL 15 min, `compare_digest`, expired rejected. `/stream-video` accepts ONLY `id` + `token` (remove `url` param). Derive target URL from server-side record (job or cache row in Redis/Supabase, no in-memory JobManager dependency); 404 if none. Update `page.tsx`, `frontend/src/lib/recipeUtils.ts` (and its tests), and rewrite rules in same commit (list old `?url=` assertions for approval). Strip `stream_token` before saving to Vault or any cache and re-mint on open. Mint tokens ONLY where server holds result (cache hit, job completion). `/library/rehydrate` mints one only when server cache record exists for validated URL. Redis-backed per-IP rate limit. Run download off event loop. Enforce `MAX_MEDIA_DOWNLOAD_MB`, 90s, 360p on BOTH download paths including legacy downloader fallback with `max_filesize`. Cap total media-cache size. Cleanup in `finally`. Range support (`FileResponse` or manual 206). New tests: expired, tampered, wrong id, url param rejected, 429, Range 206.<br>**Risks & Rollback**: Media playback failure on expired token. Rollback: revert `extract.py` and `page.tsx`.<br>**Test Plan**: Run `pytest tests/test_stream_proxy_security.py`. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1214** | Client IP Resolution, Redis Rate Limits & Guest Quotas (absorbs UPA-1204) | Security / Tech-debt | P1 | `get_client_ip`: if `TRUSTED_PROXY` is False return `request.client.host` directly and ignore ALL forwarded headers. If True: use configured single-value header (named `TRUSTED_PROXY_HEADER` e.g. `CF-Connecting-IP` or `X-Real-IP`) or count `TRUSTED_PROXY_HOPS` from right of `X-Forwarded-For`; validate as IP, else fall back to socket IP. Propose signed anonymous device ID + IP as second factor for shared mobile IPs. Test `get_client_ip` with real Request objects under both settings. Replace `check_anonymous_rate_limit` in-memory dict with Redis-backed limiter. Guest quota consumption active (guests 20/day, free 30/day, anonymous 3/min). Order: rate limit -> validate URL -> cache lookup -> consume quota ONLY on cache miss -> enqueue. Single source of truth for limits in `Settings`; remove conflicting constants. QuotaManager: retry Redis connection with backoff. Time-bucket audit & tests.<br>**Risks & Rollback**: False positive rate limiting on shared NAT IPs. Rollback: revert `security.py` & `quota_service.py`.<br>**Test Plan**: Run `pytest tests/test_client_ip_and_quotas.py`. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1215** | Data Endpoints Ownership & Validation Hardening | Security / Feature | P2 | `export_vault_item`: fetch by `extraction_id` scoped to current user (404 otherwise), guests 401 (no IP-based ownership on guest job polling — UUID is capability; enforce ownership on authenticated Vault/export routes), remove mock payload. `get_extraction_status`: validate `job_id` as UUID, use `requests` params (not string-built URLs), check ownership. `get_user_library`: guests see only rows flagged `is_public = true` (add NEW migration file for `is_public` with backfill decision; private rows NEVER readable by raw ID; add test). `rehydrate`: max body size, max 100 ingredients/products; reconcile `structured_data` vs `content_payload` with test.<br>**Risks & Rollback**: 404 on unauthenticated exports. Rollback: revert `library.py`.<br>**Test Plan**: Run `pytest tests/test_data_endpoints_security.py`. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1216** | Commerce Link Validation, Admin Key Hygiene & Enum Bounds | Security / Tech-debt | P2 | Test that every URL `AffiliateEngine` emits passes `validate_merchant_redirect_url`; fix allowlist to real hosts (`swiggy.com`, `ajio.com`, `nykaa.com`, `earnkaro.com`, `zepto.now`). Compare admin key as bytes (`hmac.compare_digest`); rate limit admin attempts. `domain_hint` Enum MUST equal frontend option IDs: `auto`, `recipe`, `kitchen_product`, `fitness_workout`, `interior_design`, `gaming`, `tech_diy`, `unboxing`, `diy` (single shared source). Add test that every frontend option and sample chip is accepted. Language codes: accept whatever UI and bots send.<br>**Risks & Rollback**: Rejection of novel domain hints. Rollback: revert `extract.py`.<br>**Test Plan**: Run `pytest tests/test_commerce_and_enums.py`. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1217** | Compose Hardening Override Separation (UNTESTED) | DevOps | P3 | Move `cap_drop`/`no-new-privileges` out of `docker-compose.override.yml` (auto-loaded) into `docker-compose.hardening.yml` (not auto-loaded); remove obsolete `version` key.<br>**Risks & Rollback**: Missing compose overrides in prod without `-f`. Rollback: restore `docker-compose.override.yml`.<br>**Test Plan**: Run `docker compose config`. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1218** | Staging Environment Isolation & Project Separation | DevOps / Security | P0 | Provision separate Supabase project for staging; apply `backend/database/*.sql` in order (`01_schema.sql`, `02_indexes.sql`, `03_functions.sql`, `04_rls_policies.sql`, `05_views.sql`); manual steps: owner creates staging project in Supabase UI, runs scripts in order via SQL Editor; configure dedicated staging credentials (`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`; `SUPABASE_JWKS_URL` derived from `SUPABASE_URL`); separate `SECRET_KEY`, Redis key prefix (`staging:`), Celery queue (`staging_default_queue`), Redis database (DB 1 vs DB 0), webhook secrets (`TELEGRAM_WEBHOOK_SECRET`, `WHATSAPP_VERIFY_TOKEN`, `RAZORPAY_WEBHOOK_SECRET`, `STRIPE_WEBHOOK_SECRET`), and Telegram bot per environment; update `DISASTER_RECOVERY.md` and `ENVIRONMENTS.md`; verify staging JWKS endpoint (`{STAGING_SUPABASE_URL}/auth/v1/.well-known/jwks.json`).<br>**Risks & Rollback**: Staging misconfiguration during initial project switch. Rollback: restore previous staging environment variables.<br>**Test Plan**: Deploy to Staging, run `scripts/verify_egress.py`, verify JWKS endpoint returns valid ES256 key, and verify zero production database rows modified. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1219** | Test Environment Isolation Gate & Socket Firewall | Tech-debt / Security | P0 | Add `tests/conftest.py` that (1) hard-overrides all external service credentials to empty strings BEFORE any app import; (2) enforces a session-level safety gate: `get_supabase_client().is_configured()` must be False and Redis/Celery URLs must target loopback only — fails entire session if violated; (3) deselects three Supabase-live-dependent test nodes per owner Rule 1 sign-off, replacing them with mocked equivalents; (4) mocks `yt_dlp.extract_info` for offline duration guardrail tests. Add `pytest.ini` with `--disable-socket --allow-hosts=127.0.0.1,localhost` to block outbound network at the socket layer. Firewall confirmed fail-closed: `socket.connect("8.8.8.8", 53)` → `SocketConnectBlockedError`; `requests.get("https://example.com")` → `SocketConnectBlockedError`; `socket.connect("127.0.0.1", 19999)` → `ConnectionRefusedError` (allowed, nothing listening).<br>**Affected files**: `tests/conftest.py` (NEW), `pytest.ini` (NEW).<br>**Deselected nodes (owner-approved)**: `test_supabase_client_is_configured`, `test_public_extraction_schema_org_recipe_jsonld`, `test_public_sitemap_urls`.<br>**Risks & Rollback**: If `pytest-socket` is removed, firewall silently vanishes. Rollback: revert `pytest.ini`.<br>**Test Plan**: `pytest tests/` 234 passed, 3 deselected in 24.34s [MEASURED]; socket probe 2 FAILED (external blocked), 1 PASSED (loopback allowed) [MEASURED]. | 🟢 Verified on Dev (Committed in Commit 6) | Committed in Commit 6 | `pytest tests/` 234 passed, 3 deselected, 0 failures in 24.34s [MEASURED] | Pending PO |
| **UPA-1221** | Supabase PostgREST Param Escaping & ALLOW_DB_WRITES Guard | Security / Tech-debt | P1 | `SupabaseRestClient`: (1) add `_escape_postgrest_val(val, for_or)` — unquoted single-column filters escape `%→\%`, `_→\_`, `(→\(`, `)→\)`, `,→\,`, `"→\"`; OR-filter values double-quoted with internal `"` doubled; (2) add `ALLOW_DB_WRITES: bool = False` to `Settings` and `is_write_allowed()` guard replacing bare `is_configured()` on all mutating calls (`save_extraction`, `increment_daily_quota`, `update_creator_tags`, `record_telemetry_event`, `log_beta_telemetry`); (3) remove hardcoded slug fallbacks — `get_public_extraction_by_slug_or_id` returns `None` and `list_public_extraction_slugs` returns `[]` when unconfigured; (4) all query filters passed as `params=` dict, never f-string URL injection.<br>**Affected files**: `backend/app/core/supabase_client.py`, `tests/test_postgrest_escaping.py` (NEW).<br>**Risks & Rollback**: `ALLOW_DB_WRITES=False` default — production deployments need `ALLOW_DB_WRITES=true` in `.env`.<br>**Test Plan**: `pytest tests/test_postgrest_escaping.py` (3/3 passed) [MEASURED]; `pytest tests/` (234/234 passed) [MEASURED]. | 🟢 Verified on Dev (Committed in Commit 7) | Committed in Commit 7 | `pytest tests/test_postgrest_escaping.py` 3/3 passed; `pytest tests/` 234 passed [MEASURED] | Pending PO |
| **UPA-1222** | SEO Public Hub structured_data Migration & Mocked Test Coverage | Tech-debt / Tests | P1 | `public_hub.py` `build_schema_org_recipe` and `get_public_extraction` read `structured_data` field first, falling back to `extracted_content` for backward compat. `list_public_extraction_slugs` reads `structured_data` column. Two mocked replacement tests: `test_public_extraction_schema_org_recipe_jsonld_mocked` injects full `structured_data` dict via `monkeypatch`, asserts `schema_org["@context"]=="https://schema.org"`, `schema_org["@type"]=="Recipe"`, `schema_org["name"]=="Crispy Air Fryer Samosa"`, `len(schema_org["recipeIngredient"])==2`, `len(schema_org["recipeInstructions"])==1` — fails if `structured_data` schema regresses; `test_public_sitemap_urls_mocked` injects one slug and asserts `count==1`, URL contains slug.<br>**Affected files**: `backend/app/api/v1/public_hub.py`, `tests/test_sprint6_seo_and_creators.py`.<br>**Risks & Rollback**: Old `extracted_content` fallback preserved. Rollback: revert `public_hub.py`.<br>**Test Plan**: `pytest tests/test_sprint6_seo_and_creators.py` (8/8 passed) [MEASURED]. | 🟢 Verified on Dev (Committed in Commit 9) | Committed in Commit 9 | `pytest tests/test_sprint6_seo_and_creators.py` 8/8 passed [MEASURED] | Pending PO |
| **UPA-1223** | Real processing_time_ms Telemetry & Downloader Logger | Tech-debt | P2 | `backend/app/workers/tasks.py`: record `start_time = time.time()` at pipeline entry; compute `processing_time_ms = int((time.time() - start_time) * 1000)` before `save_extraction` and `log_beta_telemetry`, replacing hardcoded `turnaround_time_ms=2500`. `backend/app/services/downloader.py`: add module-level `logger = logging.getLogger(__name__)` so download errors surface in structured logs.<br>**Affected files**: `backend/app/workers/tasks.py`, `backend/app/services/downloader.py`.<br>**Risks & Rollback**: Low-risk metric and logging fix. Rollback: revert `tasks.py`.<br>**Test Plan**: `pytest tests/test_workers_and_affiliate.py` (all passing) [MEASURED]; `pytest tests/` (234/234) [MEASURED]. | 🟢 Verified on Dev (Committed in Commit 8) | Committed in Commit 8 | `pytest tests/` 234 passed [MEASURED] | Pending PO |
| **UPA-1227** | SEO Public Hub 503 DB Unreachable vs 404 Missing Content & Test Scoping | Bug / Security | P1 | Differentiate `SupabaseRestClient` DB unreachable / HTTP error states (`503 Service Unavailable`) from missing entity records (`404 Not Found`) across `/public/sitemap` and `/public/extractions/{slug}`. When `is_configured() == True` but DB connection drops/fails, raise HTTP 503 and log structured error alert; when `is_configured() == False` or mock fixture present in test env (`ENVIRONMENT=test`), preserve stubbed offline returns for test isolation; when DB succeeds with 0 rows, return 404 (slug) or 200 empty (sitemap).<br>**Affected files**: `backend/app/api/v1/public_hub.py`, `backend/app/core/supabase_client.py`, `tests/test_sprint6_seo_and_creators.py`.<br>**Risks & Rollback**: Low risk. Rollback: revert `public_hub.py` and `supabase_client.py`.<br>**Test Plan**: `pytest tests/test_sprint6_seo_and_creators.py` (9/9 passed) [MEASURED]; `pytest tests/` (236/236 passed) [MEASURED]. | 🟢 Verified on Dev (Committed in Commit 10) | Committed in Commit 10 | `pytest tests/test_sprint6_seo_and_creators.py` 9/9 passed; `pytest tests/` 236 passed [MEASURED] | Pending PO |
| **UPA-1228** | Frontend Landing Page Verification & Benchmark Claim Hygiene | Docs / Security | P2 | Remove unverified performance turnaround claims ("under 3 seconds") from `frontend/src/app/page.tsx` until empirical p50/p95 benchmarks are generated directly from backend telemetry, ensuring strict adherence to AGENTS.md Rule 9 & Rule 16.<br>**Affected files**: `frontend/src/app/page.tsx`.<br>**Risks & Rollback**: UI text update only. Rollback: revert `page.tsx`.<br>**Test Plan**: `npm run build` (0 errors) [MEASURED]. | 🟢 Verified on Dev (Committed in Commit 5) | Committed in Commit 5 (6b453b1) | `npm run build` 0 errors [MEASURED] | Pending PO |
| **UPA-1229** | Growth Telemetry Events Table DDL & Service Role Security Isolation | Database / Security | P1 | Create `backend/database/010_telemetry_events.sql` defining `public.telemetry_events` table (`id`, `event_name`, `user_id`, `session_id`, `properties`, `created_at`), performance indexes, `service_role` grants, and strict RLS policies. Ensures full schema parity between application expectations (`record_telemetry_event`, `get_telemetry_funnel`) and PostgreSQL database.<br>**Affected files**: `backend/database/010_telemetry_events.sql` (NEW).<br>**Risks & Rollback**: DDL creation only. Rollback: `rm backend/database/010_telemetry_events.sql`.<br>**Test Plan**: Static SQL correctness review & RLS grant inspection [MEASURED]. | 🟢 Verified on Dev (Committed in Commit 11) | Committed in Commit 11 | Static SQL review & RLS grant audit clean [MEASURED] | Pending PO |
| **UPA-1230** | Minimum-Privilege & Security Hardening — Migration 011 | Security | P0 | Establish deterministic minimum-privilege PostgreSQL/Supabase permissions for core application tables, harden SECURITY DEFINER functions, remove public RPC execution rights from privileged quota functions, and remove unused/unscoped beta_telemetry_feed SELECT policy.<br>**Affected files**: `backend/database/011_privilege_hardening.sql`.<br>**Risks & Rollback**: Incorrect ACLs could break backend database operations. RPC privilege changes could affect quota enforcement. SECURITY DEFINER changes could affect privileged function execution if search_path assumptions are wrong. beta_telemetry_feed policy changes must be validated in Staging before Production promotion. Rollback: Migration 011 has not yet been executed; before execution, rollback SQL must be reviewed and approved separately. Do NOT claim rollback has been tested unless evidence exists. Do NOT use broad git restore/reset/clean operations as rollback.<br>**Test Plan**: 1. Execute Migration 011 in Staging only after explicit execution approval. 2. Perform read-only ACL/RLS/RPC privilege verification. 3. Verify application-required database operations against real Staging. 4. Verify unauthenticated RPC abuse attempts are rejected. 5. Verify public extraction reads still obey intended RLS behavior. 6. Verify telemetry_events SELECT/INSERT works for service_role. 7. Verify beta_telemetry_feed INSERT works for service_role. 8. Complete full Staging application validation before Production consideration. | 🟢 Verified on Staging | `99de07dee14d0521b87b8c60513b87cb9298d54d` | [MEASURED] Migration 011 executed successfully in Supabase Staging; direct PostgreSQL ACL, function EXECUTE, SECURITY DEFINER/search_path, schema ACL, RLS policy, and safe PostgREST verification all match the approved minimum-privilege contract. Production untouched. | Pending PO |
| **UPA-1231** | Agent Instruction Hardening — Skill-First Protocol & Destructive Workspace Guard | Docs / Governance | P0 | Harden repository agent governance by adding Section 18 (Skill-First Execution Protocol & Workspace Tooling Map) and Section 19 (Destructive Workspace Operation Guard) to AGENTS.md. Section 18 requires mandatory inspection and reuse of existing skills, scripts, and established routines before custom implementation. Section 19 prevents unauthorized destructive workspace cleanup, broad git restore/reset/clean operations, and accidental removal of governance, migration, test, configuration, skill, script, or documentation files.<br>**Affected files**: `AGENTS.md`.<br>**Risks & Rollback**: Tool/script paths referenced by Section 18 may change over time. Overly broad governance language could conflict with an explicitly owner-authorized operation; explicit owner authorization remains the controlling exception. Rollback: Restore AGENTS.md to the immediately preceding approved version only after verifying no later owner-approved AGENTS.md changes must be preserved. Do not use broad repository reset/clean operations.<br>**Test Plan**: 1. Verify Sections 1–17 remain unchanged. 2. Verify Section 18 exists. 3. Verify Section 19 exists. 4. Run `git diff -- AGENTS.md`. 5. Confirm no other files are changed or deleted. 6. No SQL execution, deployment, Redis configuration, or database mutation is part of this ticket. | 🟡 In Progress | Uncommitted (`AGENTS.md`) | AGENTS.md modified with Sections 18 & 19; verification clean scope confirmed | Pending PO |
| **UPA-1232** | Execution Artifact & Script Provenance Guard | Docs / Governance | P1 | Add AGENTS.md Section 20 to govern temporary scratch scripts and operational execution artifacts. Read-only diagnostics may use temporary global/IDE scratch scripts, while mutating operational scripts must be repository-controlled, ticketed, reviewed, and auditable. Governed migrations must execute from the exact reviewed repository migration artifact.<br>**Affected files**: `AGENTS.md`.<br>**Risks & Rollback**: Future temporary diagnostic tooling may require clarification of read-only scope. Overly strict interpretation could block legitimate owner-authorized operational work. Rollback: Restore AGENTS.md to the preceding approved version only after checking for later owner-approved governance changes. Do not use broad repository reset/clean commands.<br>**Test Plan**: git diff -- AGENTS.md; verify Sections 1–19 unchanged; verify Section 20 contents; confirm only AGENTS.md is modified; no SQL/deployment/Redis activity. | 🟡 In Progress | Uncommitted (`AGENTS.md`) | AGENTS.md modified with Section 20; verification clean scope confirmed | Pending PO |
| **UPA-1233** | Staging Application Deployment & Gateway Validation | Tech-debt / Docs / Deployment Governance | P0 | Governs controlled Staging application deployment gate: (1) promote verified commit `78b335e75d254864a2ee0a0b8730a4379adfd895` from Dev to staging; (2) deploy Next.js frontend to Vercel Preview Staging environment; (3) deploy FastAPI backend API container on Staging host; (4) verify Staging environment/secrets presence (`ENVIRONMENT=staging`, `SECRET_KEY`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `TRUSTED_PROXY=true`, `ALLOW_DB_WRITES=false`) without displaying secret values — initial application deployment must occur with database writes disabled (`ALLOW_DB_WRITES=false`); (5) execute real PostgREST lookup (`GET /api/v1/public/extractions/non-existent-slug-12345`) returning HTTP 404 to prove Application → Staging Supabase connectivity and confirm `SUPABASE_URL` resolves to `https://mzpkdmaxsuhwezsooidu.supabase.co`; (6) verify FastAPI gateway runtime endpoints (`GET /` and `GET /health` returning `"status": "healthy"`); (7) verify Production isolation by confirming zero configuration references Production Supabase ref (`scrqvbgjybnrvcpxbygf`), without contacting Production; (8) capture deployment evidence (promoted commit hash, `scripts/verify_promotion.py` pass, Vercel staging URL, container ID, runtime health response); (9) define Staging rollback procedures (Vercel preview rollback, container image rollback, zero automated DB reset); (10) explicitly defer Redis/Celery background workers until application gateway gate passes; (11) explicitly defer E2E validation suite until application gateway and Staging integration gates pass; (12) database write enablement (`ALLOW_DB_WRITES=true`) is a separate later gate and may only be enabled during an explicitly governed write-validation step after read-only gateway and Staging Supabase connectivity gates pass, without using Production access.<br>**Affected files**: `docs/po-governance/JIRA_BACKLOG.md` (ticket registration).<br>**Applicable AGENTS.md rules**: Rules 2, 6, 14, 16, 17, Sections 18, 19, 20.<br>**Risks & Rollback**: Staging environment variable misconfiguration or Vercel protection wall block. Rollback: Vercel preview rollback to prior release; container image rollback on Staging host. No automated database reset/clean operations permitted.<br>**Test Plan**: 1. `python scripts/promote.py --to staging` pre-promotion pass & git push evidence. 2. Environment secret presence audit with `ALLOW_DB_WRITES=false` default (hashes/booleans only). 3. Vercel Staging preview HTTP 200 check with bypass cookie. 4. Staging API Gateway `/health` & `/` runtime verification. 5. Real Staging Supabase PostgREST lookup (`GET /api/v1/public/extractions/non-existent-slug-12345`) returning HTTP 404. 6. Production isolation check confirming `SUPABASE_URL` resolves to `https://mzpkdmaxsuhwezsooidu.supabase.co` with zero Production DB contact. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1234** | Staging Application Deployment Write Gate Clarification | Docs / Governance | P0 | Clarify Staging deployment write gate: initial Staging application deployment MUST execute with database writes disabled (`ALLOW_DB_WRITES=false`); database write enablement (`ALLOW_DB_WRITES=true`) is a separate, later gate requiring explicit owner authorization.<br>**Affected files**: `docs/po-governance/JIRA_BACKLOG.md`.<br>**Applicable AGENTS.md rules**: Rules 2, 6, 14, 16, 17, Sections 18, 19, 20.<br>**Risks & Rollback**: Misinterpreting write gate requirements. Rollback: revert backlog documentation.<br>**Test Plan**: Verify `ALLOW_DB_WRITES=false` contract in documentation and environment validation. | 🟢 Verified on Dev | `170f5e511202aa6394046f30c04a245efacd33d8` | Verified documentation contract on Dev | Pending PO |
| **UPA-1235** | Staging Architecture & Vercel Preview Reconciliation | Docs / Architecture | P1 | Reconcile Staging architecture: Vercel Preview deployment represents the Staging frontend layer (`staging` branch); backend Staging host architecture requires explicit owner decision.<br>**Affected files**: `docs/po-governance/JIRA_BACKLOG.md`.<br>**Applicable AGENTS.md rules**: Rules 2, 17.<br>**Risks & Rollback**: Architectural mismatch. Rollback: revert documentation.<br>**Test Plan**: Read-only architecture audit. | 🟢 Verified on Dev | Read-only audit | Verified Staging architecture reconciliation | Pending PO |
| **UPA-1236** | Review and Harden verify_promotion.py Test Runner Changes | Tech-debt / Security | P1 | Govern and harden `scripts/verify_promotion.py` test runner adjustments: (1) evaluate transition from `unittest` discovery to `pytest` execution for parity with `scripts/ci_check.py`; (2) assess hardcoded `SECRET_KEY` fallback string (`"universal_pro_default_secret_key_2026"`) and remove hardcoded secret fallbacks to enforce strict Rule 6 secret hygiene; (3) ensure promotion verification executes cleanly using environment secret resolution; (4) perform regression verification of pre-promotion quality gates against preserved recovery branch `recovery/verify-promotion-c86c38f`.<br>**Affected files**: `scripts/verify_promotion.py`.<br>**Applicable AGENTS.md rules**: Rules 1, 6, 16, 17, Sections 18, 19, 20.<br>**Risks & Rollback**: Script misconfiguration during promotion checks. Rollback: preserved in local recovery branch `recovery/verify-promotion-c86c38f`.<br>**Test Plan**: 1. Inspect preserved commit `c86c38ff9cf64b6d0d7c9b150830a086917a9fe7`. 2. Refactor `verify_promotion.py` to eliminate hardcoded secret fallback. 3. Verify clean `python scripts/verify_promotion.py` execution with `SECRET_KEY` passed from environment. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1237** | Register Universal Pro AI System Architecture Baseline & Rule 21 Drift Guard | Docs / Architecture | P0 | Adopt System Architecture Baseline (`docs/architecture/SYSTEM_ARCHITECTURE.md`); add Rule 21 (Documentation Synchronization & Architecture Drift Guard) to `AGENTS.md`; cross-reference architecture runbooks (`ENVIRONMENTS.md`, `ORACLE_CLOUD_DEPLOYMENT.md`, `DISASTER_RECOVERY.md`); register UPA-1237 in `JIRA_BACKLOG.md`; maintain Pending PO status.<br>**Affected files**: `docs/architecture/SYSTEM_ARCHITECTURE.md`, `AGENTS.md`, `docs/po-governance/JIRA_BACKLOG.md`, `docs/architecture/ENVIRONMENTS.md`, `docs/architecture/ORACLE_CLOUD_DEPLOYMENT.md`, `docs/architecture/DISASTER_RECOVERY.md`.<br>**Applicable AGENTS.md rules**: Rules 9, 16, 17, 21, Sections 18, 19, 20.<br>**Risks & Rollback**: Documentation mismatch with runtime. Rollback: Revert documentation files via git.<br>**Test Plan**: Run `python scripts/ci_check.py` to ensure build, lint, and tests remain clean green. | 🟢 Verified on Dev | Uncommitted | Documentation & governance adoption verified | Pending PO |







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
| **UPA-1201** | Entry Point SSRF & Pre-existing Test Audit (T1) | Security / Tests | P0 | Audit diff base `git diff 451b20e~1 HEAD -- tests frontend/src`; verify `validate_url_and_follow_redirects` rejects hosts resolving to private IPs (`127.0.0.1`, `169.254.169.254`); add NEW test in `tests/test_ssrf_entrypoint.py` without editing existing tests. | 📋 Planned | Pending | Pending | Pending PO |
| **UPA-1202** | Secret Hygiene, Fallback Removal & Environment Gate (T2) | Security | P0 | Remove ALL constant fallbacks for `SECRET_KEY`, `RAZORPAY_*`, `STRIPE_*`, `WHATSAPP_VERIFY_TOKEN`, `universal_pro_default_secret_key` across `url_validator.py`, `extract.py`, `library.py`, `config.py`; `DEBUG` default False; `CORS_ORIGINS` from env (no `*`); non-dev envs treated as production; local `.env` required for dev; standardize `TELEGRAM_*` env vars. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1203** | Streamlit Audit & Security/Gating/Retire Proposal (T3) | Security / Tech-debt | P1 | Audit Streamlit paths for `url_validator` and `quota_manager` (neither used); propose retiring Streamlit or adding both validations; gate developer expander with `ADMIN_PASSWORD` + `hmac.compare_digest`. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1204** | Rate Limiter & Sliding Window Audit (T4) | Security / Tech-debt | P1 | Absorbed into `UPA-1214`. Audit time-bucket key structure `rate_limit:{key}:{bucket}`. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1205** | IP Pinning & PinnedHTTPSConnection Wire-up (T6) | Security | P0 | Subclass `PinnedHTTPSConnection(http.client.HTTPSConnection)` with `server_hostname=self.host`; wire into real server-side fetches of user/remote-derived URLs (oEmbed/thumbnails) or delete if none; `stream_video` uses yt-dlp so nothing to wire there; re-check inside `connect()` that pinned IP is global; add `trustme` TLS test. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1206** | Container Network Egress Firewall & Rollback Protocol (T5) | Security | P0 | Update `setup_egress_firewall.sh` with rules `-s <compose subnet> -d <private range>` returning `RETURN` so inbound traffic is untouched; compose subnet `172.28.0.0/16`; add `ip6tables`; DNS test from container; rollback `iptables -F DOCKER-USER && iptables -A DOCKER-USER -j RETURN`; mark **NOT VERIFIED** until Linux host test. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1207** | Dependencies, Clean Venv, Lock File & Audit (T7) | Tech-debt / Security | P1 | Perform import scan for runtime backend packages in `requirements.txt`; place dev/test tools (`pytest`, `trustme`, `fakeredis`) in `requirements-dev.txt`; build clean venv on Docker Python image; generate `requirements.lock`; run `pip-audit`; confirm container boots & pytest passes. | 📋 Planned | Pending | Pending | Pending PO |
| **UPA-1208** | Secret Scan & Repository History Audit (T8) | Security | P0 | Run `gitleaks` / `trufflehog` / regex pattern scanner over all git refs for sensitive tokens (Mistral, Stripe, Razorpay, Telegram, WhatsApp, Vercel secret); report findings by file & rule name in `docs/po-governance/SECURITY_AUDIT_REPORT.md` without printing secret values. | 📋 Planned | Pending | Pending | Pending PO |
| **UPA-1209** | VaultLibrary React Component Test | Tech-debt / Tests | P1 | Create `frontend/src/components/__tests__/VaultLibrary.test.tsx` using jsdom + RTL with `tag=MOCK_TAG`; list old `vaultRehydration.test.ts` for owner deletion sign-off. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1210** | Hinglish Prompt Evaluation Standard | Docs | P2 | Mark existing prompt snapshot strings as `ILLUSTRATIVE` and Hinglish golden set benchmark as `NOT VERIFIED` until live API evaluation is conducted. | 📋 Planned | Pending | Pending | Pending PO |
| **UPA-1211** | PO Governance Document Audit | Docs | P2 | Grep codebase docs for `\[ ?✅ ?\]`, `Approved for Production`, `APPROVAL` and list all line numbers without editing files. | 📋 Planned | Pending | Pending | Pending PO |
| **UPA-1212** | JWT Signature Verification & Audience Guard | Security | P0 | Fix `security.py get_current_user`: verify signature, `exp`, and `aud="authenticated"` against Supabase signing setup (HS256 secret or JWKS from config, never hardcode). Pin allowed algorithms, reject `alg=none`, require `exp` & `sub`, never take `role` or `plan` from token claims (plan comes from DB profile only). New tests: forged signature, expired, wrong audience, `alg=none`, valid token. List every existing test minting unsigned tokens. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1213** | Stream Proxy Token Security & Media Hardening | Security | P0 | Token = `<exp>.<sig>`, sig = `HMAC-SHA256(secret, f"{id}\|{sha256(url)}\|{exp}")`, TTL 15 min, `compare_digest`, expired rejected. `/stream-video` accepts ONLY `id` + `token` (remove `url` param). Derive target URL from server-side record (job or cache row); 404 if none. Update `page.tsx` and rewrites in same commit. Mint tokens ONLY where server holds result. `/library/rehydrate` mints one only when server cache record exists for validated URL. Redis-backed per-IP rate limit. Run download off event loop. Enforce `MAX_MEDIA_DOWNLOAD_MB`, 90s, 360p on BOTH download paths including legacy downloader fallback. Cap total media-cache size. Cleanup in `finally`. Range support (`FileResponse` or manual 206). New tests: expired, tampered, wrong id, url param rejected, 429, Range 206. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1214** | Client IP Resolution, Redis Rate Limits & Guest Quotas | Security / Tech-debt | P1 | `get_client_ip`: if `TRUSTED_PROXY` is False return `request.client.host` and ignore ALL forwarded headers. If True: use configured single-value header or count `TRUSTED_PROXY_HOPS` from right of `X-Forwarded-For`; validate as IP, else fall back to socket IP. Test with real Request objects under both settings. Replace `check_anonymous_rate_limit`'s in-memory dict with Redis-backed limiter. Guests MUST consume daily quota. Execution order: rate limit -> validate URL -> cache lookup -> consume quota ONLY on cache miss -> enqueue. Single source of truth for limits in `Settings`; remove conflicting constants (3/10 in security.py & Settings vs 20/30 in quota_service). QuotaManager: retry Redis connection with backoff. Time-bucket audit & tests. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1215** | Data Endpoints Ownership & Validation Hardening | Security / Feature | P2 | `export_vault_item`: fetch by `extraction_id` scoped to current user (404 otherwise), guests 401, remove mock payload. `get_extraction_status`: validate `job_id` as UUID, use `requests` params (not string-built URLs), check ownership. `get_user_library`: guests see only rows flagged public (add test). `rehydrate`: max body size, max 100 ingredients/products; reconcile `structured_data` vs `content_payload` with test. | 📋 Planned | Pending | Pending | Pending PO |
| **UPA-1216** | Commerce Link Validation, Admin Key Hygiene & Enum Bounds | Security / Tech-debt | P2 | Test that every URL `AffiliateEngine` emits passes `validate_merchant_redirect_url`; fix allowlist to real hosts (`swiggy`, `ajio`, `nykaa`, `earnkaro`, `zepto`). Compare admin key as bytes (`hmac.compare_digest`); rate limit admin attempts. Validate `domain_hint` and `preferred_language` against enums. | 📋 Planned | Pending | Pending | Pending PO |
| **UPA-1217** | Compose Hardening Override Separation | DevOps | P3 | Move `cap_drop`/`no-new-privileges` out of `docker-compose.override.yml` (auto-loaded) into `docker-compose.hardening.yml` (not auto-loaded); remove obsolete `version` key. | 📋 Planned | Pending | Pending | Pending PO |
| **UPA-1224** | Production API HTTPS & Proxy IP Architecture | Security / DevOps | P0 | Propose domain + Caddy site block for automatic TLS certificate management; open port 443 in OCI Security List; redirect HTTP 80 -> 443. Report frontend communication (`NEXT_PUBLIC_API_URL`, `next.config.mjs` rewrites, SSR fetch in `sitemap.ts` & `r/[slug]/page.tsx`, client polling) and end-to-end proxy hop IP chain (`Client -> Vercel -> Caddy -> FastAPI`) under `TRUSTED_PROXY=True` and `TRUSTED_PROXY_HOPS=2`. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1225** | Production VM Zero-Downtime Promotion Runbook | DevOps / Deployment | P0 | Promotion runbook for Ubuntu 24.04 VM (1 GB RAM, Docker Compose: Caddy, API, Worker, Redis running Sep 13 code). Steps: (1) manual `.env` secret audit (`SECRET_KEY`, `ADMIN_API_KEY`, `WHATSAPP_APP_SECRET`, `ENVIRONMENT=production`, `ALLOW_DB_WRITES=true`, `TRUSTED_PROXY=true`); (2) sync code from approved `main` commit; (3) recreate worker then API one-by-one (`docker compose up -d --no-deps --build worker` then `api`); (4) smoke tests (`curl` health, docs disabled check, polling); (5) rollback protocol to previous commit. Rule 2: zero direct edits on VM. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |
| **UPA-1226** | Production API Public Exposure & Port Shielding | Security | P0 | Remediate production VM API exposure where container publishes `0.0.0.0:8000` answering `/docs` on public IP bypassing Caddy, and Caddy container IP `172.18.0.5` collapses all rate limits. Propose: (1) bind API container port strictly to `127.0.0.1:8000:8000` (or drop host publishing); (2) Caddy client IP forwarding trusted via `TRUSTED_PROXY` and `TRUSTED_PROXY_HOPS`; (3) HTTPS via domain; (4) secret audit ensuring no secrets in `NEXT_PUBLIC_` vars; (5) evaluate Next.js server-side API proxy route to hide backend origin. | 🔒 Pending Owner Approval | Pending | Pending | Pending PO |

---

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
