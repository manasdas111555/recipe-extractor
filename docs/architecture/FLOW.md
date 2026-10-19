# 🧭 Universal Pro AI — Execution Flow Mapping & System Call Hierarchy

---

## 1. DOCUMENT CONTROL

* **Document Title**: Execution Flow Mapping & System Call Hierarchy
* **File Path**: `docs/architecture/FLOW.md`
* **Governing Rule**: AGENTS.md Rule 23 (*Execution Flow Mapping & System Call Hierarchy*)
* **Document Status**: Active / Reconciled Baseline `[VERIFIED IN CURRENT REPOSITORY]`
* **Initial Baseline Date**: October 16, 2026
* **Target Audience**: Core Engineers, System Architects, Quality Assurance, Automated Coding Agents

---

## 2. HIGH-LEVEL PIPELINE TOPOLOGY

```mermaid
flowchart TD
    Client["Client / PWA / Chat Bot"] -->|"1. Submit URL"| Gateway["FastAPI API Gateway (/api/v1/extract)"]
    Gateway -->|"2. Validate Scheme & SSRF"| Security["Security Validator (url_validator.py)"]
    Security -->|"3. Compute SHA-256 Hash"| CacheCheck{"Viral Cache Hit in Supabase?"}

    CacheCheck -->|"YES (Hit)"| InstantReturn["Instant HTTP 200 (0ms, 0 Token Cost, Stream Token Minted)"]
    InstantReturn --> Client

    CacheCheck -->|"NO (Miss)"| QuotaGate{"Daily Quota Available?"}
    QuotaGate -->|"Quota Exceeded"| HTTP429["Return HTTP 429 Too Many Requests"]
    QuotaGate -->|"Allowed"| DeductQuota["Deduct Quota & Create Job Record"]

    DeductQuota --> Dispatcher{"Redis / Celery Broker Reachable?"}
    Dispatcher -->|"YES (Production/Staging)"| CeleryQueue["Enqueue extract_video_task to Celery Redis Queue"]
    Dispatcher -->|"NO (Local Dev Fallback)"| InProcess["Enqueue run_extraction_worker_sync to BackgroundTasks"]

    CeleryQueue --> Worker["Worker Pipeline (tasks.py: execute_extraction_pipeline)"]
    InProcess --> Worker

    Worker --> Downloader["Managed Media Downloader (media_downloader.py)"]
    Downloader -->|"Enforce 360p / 90s Ceiling"| MediaDisk["/tmp/recipe_downloads/worker_...mp4"]

    MediaDisk --> AIRouter["Central AI Router (ai_router.py)"]
    AIRouter -->|"Primary Mode"| Gemini["Google Gemini Multimodal API (gemini_processor.py)"]
    AIRouter -->|"Opt-In / Fallback"| Council["3-Stage LLM Council (llm_council.py)"]
    AIRouter -->|"Secondary Vision"| Mistral["Mistral Vision Engine (mistral_processor.py)"]
    AIRouter -->|"Audio Dialogue"| Groq["Groq Whisper-v3 + Llama 3.3 (groq_processor.py)"]

    Gemini --> StructuredMeta["Structured JSON Domain Extraction"]
    Council --> StructuredMeta
    Mistral --> StructuredMeta
    Groq --> StructuredMeta

    StructuredMeta --> Affiliate["Affiliate & Quick-Commerce Engine (affiliate_engine.py)"]
    Affiliate -->|"Enrich Store Links"| FinalPayload["Final Content Payload + Timings"]

    FinalPayload --> DB["Atomic Supabase PostgreSQL Commit + Telemetry Logging"]
    DB --> Cleanup["Unskippable finally: Block (os.unlink temp media)"]
    Cleanup -->|"Job Status = Completed"| PollingClient["Client Polling (/api/v1/extract/status/{job_id})"]
```

---

## 3. CORE EXECUTION FLOWS

### 3.1 Video Extraction & Processing Pipeline

The primary extraction flow processes a user-supplied social video URL from ingestion to structured output.

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Client PWA
    participant API as FastAPI (extract.py)
    participant Sec as Validator (url_validator.py)
    participant DB as Supabase (PostgreSQL)
    participant Disp as Dispatcher (Dual-Mode)
    participant Work as Worker (tasks.py)
    participant DL as Downloader (yt-dlp)
    participant AI as Gemini Cloud (File API)
    participant Aff as Affiliate Engine (affiliate_engine.py)

    User->>API: POST /api/v1/extract { video_url, domain_hint, preferred_language }
    API->>API: Check anonymous rate limit (Redis sliding window)
    API->>Sec: validate_social_url(video_url)
    Sec->>Sec: Check HTTPS scheme & ALLOWED_DOMAINS
    Sec->>Sec: resolve_and_validate_hostname() [SSRF / IP pinning]
    Sec-->>API: Validated canonical URL
    API->>API: Compute SHA-256 url_hash
    API->>DB: get_cached_extraction(url_hash)

    alt Viral Cache Hit
        DB-->>API: Cached extraction record
        API->>Sec: generate_stream_token(cache_id, secret_key, target_url)
        API-->>User: HTTP 200 OK (is_cached: true, data: content_payload)
    else Cache Miss
        API->>API: check_and_consume_quota()
        API->>API: JobManager.create_job(job_id)
        API->>Disp: Dispatch task (Celery or BackgroundTasks)
        API-->>User: HTTP 202 Accepted (job_id, poll_url: /status/{job_id})

        Disp->>Work: execute_extraction_pipeline(job_id, video_url, ...)
        Work->>DL: managed_worker_download(video_url)
        DL->>DL: Probe duration (<= 90s) & 360p stream selector
        DL-->>Work: Yields temp path (/tmp/recipe_downloads/worker_...mp4)

        Work->>AI: Upload media to Gemini File API
        AI->>AI: Wait for ACTIVE state (1s poll)
        AI->>AI: Multimodal LLM reasoning (gemini-3.8-flash -> 3.7 -> 3.6 cascade)
        AI-->>Work: Raw text response & schema JSON
        Work->>AI: client.files.delete(uploaded_file)

        Work->>Aff: enrich_product_links(products) / quick-commerce cart links
        Aff-->>Work: Enriched payload
        Work->>DB: save_extraction(job_id, content_payload)
        Work->>DB: increment_daily_quota(user_id)
        Work->>DB: log_beta_telemetry()

        Work->>DL: Exit context manager -> finally: os.unlink(temp_file)
        Work->>Work: JobManager.update_job(job_id, status="completed", percent=100)

        User->>API: GET /api/v1/extract/status/{job_id}
        API-->>User: HTTP 200 OK (status: "completed", data: content_payload)
    end
```

#### Detailed Stage Breakdown:
1. **Request Intake & Schema Validation**:
   - `POST /api/v1/extract` receives `ExtractRequest` validated via Pydantic (`video_url`, `domain_hint`, `preferred_language`).
   - Anonymous tier IP sliding window: Rate limit enforced via Redis (`ANONYMOUS_RATE_LIMIT_PER_MINUTE = 3`).
2. **Security & SSRF Verification**:
   - `validate_social_url()` in `url_validator.py` checks protocol (`https://`), domain allowlist, executes DNS resolution with `socket.getaddrinfo`, and verifies `is_globally_routable_ip()`.
   - Maximum 3 redirect hops followed manually; each hop re-validates host and IP.
3. **Canonical Cache Lookup**:
   - Canonical URL string stripped of tracking parameters (`?igsh=...`, `?utm_source=...`).
   - SHA-256 hash computed. Supabase queried via PostgREST (`get_cached_extraction(url_hash)`).
   - If hit, signed HMAC stream token is minted, and payload is returned immediately with HTTP 200.
4. **Quota Gate & Enqueueing**:
   - On cache miss, `quota_manager.check_and_consume_quota()` decrements daily quota.
   - Job is registered in `JobManager` with UUID4 `job_id`.
   - HTTP 202 Accepted returned with `poll_url: /api/v1/extract/status/{job_id}`.
5. **Media Download (Ingestion Guardrails)**:
   - `managed_worker_download()` enters context manager.
   - `yt-dlp` fetches metadata. Duration verified $\le 90$s. Missing duration fails closed.
   - Format: `bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best[height<=360]`.
   - Stream saved to ephemeral path `/tmp/recipe_downloads/worker_<ts>_<id>.mp4`.
6. **Multimodal AI Reasoning**:
   - Video uploaded to Google Gemini File API (`client.files.upload()`).
   - Polled until state is `ACTIVE`.
   - Primary model cascade executed: `gemini-3.8-flash` $\rightarrow$ `gemini-3.7-flash` $\rightarrow$ `gemini-3.6-flash` $\rightarrow$ `gemini-3.5-flash`.
   - On HTTP 503/429/timeout, fast failover switches to the next model tier.
   - File deleted from Gemini Cloud via `client.files.delete()`.
   - `parse_extracted_content()` parses raw JSON into structured metadata (`title`, `category`, `summary`, `details`, `instructions`, `products`, `resources`).
7. **Monetization & Quick-Commerce Enrichment**:
   - `affiliate_engine.enrich_product_links()` injects Amazon Associates (`tag=manasdas11155-21`), EarnKaro (`r=5608766`), and 10-minute quick-commerce search links (Blinkit, Zepto, Instamart, JioMart).
8. **Persistence & Cleanup**:
   - Structured payload committed to Supabase `extractions` table.
   - Telemetry logged (`log_beta_telemetry`).
   - Context manager exits: `finally:` block unlinks `/tmp/recipe_downloads/worker_...mp4`.
   - `JobManager` status updated to `completed` (100%).

---

### 3.2 Dual-Mode Dispatcher Flow

Ensures zero dependency friction in local development while maintaining horizontally scalable distributed queues in production.

```mermaid
flowchart TD
    Submit["enqueue_extraction() receives request"] --> ReachableCheck{"is_celery_broker_reachable()?"}

    ReachableCheck -->|"Ping Successful (Redis Alive)"| TryCelery["Try: extract_video_task.apply_async(...)"]
    TryCelery -->|"Enqueued Successfully"| CeleryWorker["Celery Worker Cluster (Layer 2 / Layer 3)"]
    TryCelery -->|"Connection / Serialization Error"| FallbackLog["Log Warning & Fallback"]
    FallbackLog --> BackgroundTasksPath["background_tasks.add_task(run_extraction_worker_sync, ...)"]

    ReachableCheck -->|"Redis Offline / Unconfigured"| BackgroundTasksPath

    subgraph CeleryExecution["Celery Worker Pipeline"]
        CeleryWorker --> PlatformDetect{"OS Platform Check (sys.platform)"}
        PlatformDetect -->|"win32 (Windows Dev)"| WinPool["Execute with --pool=solo (No fork errors)"]
        PlatformDetect -->|"linux (Docker / OCI)"| LinuxPool["Execute with --concurrency=4 (Prefork)"]
        WinPool --> Exec1["execute_extraction_pipeline()"]
        LinuxPool --> Exec1
    end

    subgraph BackgroundTasksExecution["In-Memory Fallback Pipeline"]
        BackgroundTasksPath --> InProcessThread["FastAPI Background Threadpool"]
        InProcessThread --> Exec2["execute_extraction_pipeline()"]
    end

    Exec1 --> StateUpdate["State Tracked in Redis & JobManager"]
    Exec2 --> StateUpdate2["State Tracked in JobManager In-Memory State"]
```

#### Dispatcher Invariants:
* **Broker Probing**: `is_celery_broker_reachable()` performs a non-blocking TCP socket check against `REDIS_URL` with a 1-second timeout.
* **Windows Multi-Processing Guard**: When running `scripts/run_worker.py` on Windows, `--pool=solo` is forced. Celery pre-fork (`fork()`) is strictly reserved for Linux container runtimes.
* **Stateless Web Layer**: Neither path retains media files or extraction state in web process memory. Completed state is written to Supabase and polled via `job_id`.

---

### 3.3 Security & Video Stream Proxy Flow

The `/stream-video` endpoint allows in-page HTML5 video playback without exposing raw upstream URLs or triggering CORS/media player collisions.

```mermaid
sequenceDiagram
    autonumber
    actor Player as HTML5 Video Player (Browser)
    participant Proxy as /api/v1/extract/stream-video
    participant Quota as Rate Limiter (quota_service.py)
    participant Sec as URL Validator (url_validator.py)
    participant Cache as Ephemeral Cache (/tmp/universalpro_media_cache)
    participant DL as Worker Downloader (media_downloader.py)

    Player->>Proxy: GET /stream-video?id={id}&token={exp.sig} (Range: bytes=0-)
    Proxy->>Proxy: Validate parameter presence (reject raw ?url=)
    Proxy->>Quota: check_generic_rate_limit("stream:{client_ip}", limit=60/min)
    Quota-->>Proxy: Allowed (under rate limit)

    Proxy->>Proxy: Parse token format (<exp>.<sig>)
    Proxy->>Proxy: Verify exp >= int(time.time())
    Proxy->>Proxy: Resolve target_url from JobManager or Supabase record
    Proxy->>Sec: verify_stream_token(id, token, secret_key, target_url)
    Sec-->>Proxy: Cryptographic Signature Valid (HMAC-SHA256)
    Proxy->>Sec: validate_social_url(target_url)
    Sec-->>Proxy: Target Host & IP Valid

    Proxy->>Cache: cleanup_ephemeral_media_cache(max_age=1800s)
    Proxy->>DL: asyncio.to_thread(_download_stream_video_sync, target_url, Cache)
    DL-->>Proxy: Returns video file path (/tmp/universalpro_media_cache/...)

    Proxy->>Proxy: Validate file size <= 50MB (Rule 4 cap)
    Proxy->>Player: HTTP 206 Partial Content (Content-Range, video/mp4 stream)

    Note over Player,Proxy: Single docked player invariant (Rule 7): Only ONE player instance active
```

#### Stream Proxy Security Controls:
1. **Query Hygiene**: Client-supplied `?url=` parameters are strictly rejected (`HTTP 400`). Only server-side resolved URLs bound to the signed token are streamed.
2. **Token Structure**: Token consists of `<expiration_timestamp>.<hmac_signature>`. Expired tokens fail before cryptographic verification.
3. **Payload Binding**: The HMAC-SHA256 signature binds the extraction `id`, `expiration`, and server-resolved `media_url` using `SECRET_KEY`.
4. **Range Requests**: Supports HTTP Range headers (`bytes=0-`) to enable scrubbing and instant playback on iOS Safari and mobile Chrome.
5. **Ephemeral Cache TTL**: Media files in `/tmp/universalpro_media_cache/` are purged after 30 minutes via `cleanup_ephemeral_media_cache()`.

---

### 3.4 Storage & Ephemeral Media Cleanup Lifecycle

Enforces zero media retention and strict compliance with AGENTS.md Rules 4 and 5.

```mermaid
stateDiagram-v2
    [*] --> Idle: Worker waiting for job
    Idle --> Ingestion: Video URL dispatched

    state Ingestion {
        [*] --> DownloadMedia: managed_worker_download()
        DownloadMedia --> ValidateCaps: Check duration <= 90s, format <= 360p
        ValidateCaps --> WriteTemp: Write to /tmp/recipe_downloads/worker_<ts>_<id>.mp4
    }

    state AIReasoning {
        WriteTemp --> UploadGemini: client.files.upload()
        UploadGemini --> Inference: models.generate_content()
        Inference --> DeleteGeminiCloud: client.files.delete()
        DeleteGeminiCloud --> ParseJSON: parse_extracted_content()
    }

    state Cleanup {
        ParseJSON --> FinallyBlock: Enter unskippable finally: block
        FinallyBlock --> CheckDisk: os.path.exists(/tmp/recipe_downloads/worker_...mp4)
        CheckDisk --> UnlinkFile: os.unlink(temp_file)
        UnlinkFile --> VerifyClean: File removed from container disk
    }

    Cleanup --> PersistDB: Commit structured JSON to Supabase
    PersistDB --> [*]: Disk usage = 0 bytes, DB = permanent record
```

#### Cleanup Invariants:
1. **Unskippable `finally:` Guarantee**: All media downloads inside `managed_worker_download` execute within a Python context manager. Regardless of whether inference succeeds, throws an exception, or encounters a timeout, the file path is unlinked.
2. **Intermediate Artifacts**:
   - Keyframe images (`frames_<stem>/frame_*.jpg`) generated for Mistral Vision must be unlinked in a `finally:` block.
   - Audio tracks (`.mp3`) extracted for Groq Whisper must be unlinked immediately after transcription completes.
3. **Container Immutability**: No media files are ever moved or written to `/app/backend/app/services/downloads/` or any directory inside the application source tree. All temporary processing happens under `/tmp/`.

---

### 3.5 Web Share Target & Chat Ingestion Flow

Universal Pro AI supports one-tap video ingestion from native mobile apps (Instagram, TikTok, YouTube) and chat platforms.

```mermaid
flowchart LR
    subgraph MobileClients["Mobile Ingestion Sources"]
        Instagram["Instagram App Share Sheet"]
        YouTube["YouTube App Share Sheet"]
        TikTok["TikTok App Share Sheet"]
    end

    subgraph WebhookClients["Chat Platforms"]
        Telegram["Telegram Bot (@UniversalReelBot)"]
        WhatsApp["WhatsApp Cloud API Webhook"]
    end

    MobileClients -->|Web Share Target API| ShareTarget["/share-target (Next.js PWA)"]
    ShareTarget -->|Redirect with ?url=| WebPWA["Frontend PWA Home (/)"]
    WebPWA -->|POST /api/v1/extract| APIGateway["FastAPI Gateway"]

    Telegram -->|Webhook / Long Polling| TeleService["telegram_bot.py"]
    WhatsApp -->|POST /webhook/whatsapp| WAWebhook["whatsapp_service.py"]

    WAWebhook -->|Verify HMAC-SHA256 Signature| WAEgress["Validate & Parse Text"]
    TeleService --> APIGateway
    WAEgress --> APIGateway
```

#### Ingestion Security Invariants:
* **Web Share Target**: Receives `POST /share-target` from mobile OS share sheets and parses URL query params before client-side submission.
* **WhatsApp Signature Verification**: The WhatsApp webhook handler validates `X-Hub-Signature-256` over the **raw request payload body** using `hmac.compare_digest` *before* parsing JSON, preventing request tampering.

---

### 3.6 Six-Phase Release Lifecycle & Mandatory Two-Tier Playwright Gate Sequence

All repository changes follow six distinct operational phases with mandatory automated release gates and Product Owner checkpoints:

```mermaid
flowchart TD
    subgraph Phase1["Phase 1: Intake & Governed Planning"]
        P1A["Backlog Intake (JIRA_BACKLOG.md)"] --> P1B["Risk Assessment & Rollback Map"]
        P1B --> P1C{"Touches Protected Areas?"}
        P1C -->|Yes| P1D["Owner Checkpoint Gate (STOP)"]
        P1C -->|No| P2A
        P1D -->|Approved| P2A
    end

    subgraph Phase2["Phase 2: Dev Implementation & Local Verification"]
        P2A["Sandbox Implementation on Dev"] --> P2B["Focused Regressions (pytest / vitest)"]
        P2B --> P2C["Deterministic Mocked Playwright (test:e2e:mocked)"]
    end

    subgraph Phase3["Phase 3: Living Document Sync & Definitive Verification"]
        P2C --> P3A["Synchronize All 6 Living Documents (Rule 9/21)"]
        P3A --> P3B["Documentation Impact Assessment & ADR/FLOW Updates"]
        P3B --> P3C["Inspect Final Tree Diff"]
        P3C --> P3D["Definitive Rule 16 Pipeline (ci_check.py: tsc, lint, vitest, build, pytest)"]
        P3D --> P3E["Governed Commit ([UPA-####] ...)"]
        P3E --> P3F["Dev / PO Review Boundary Gate (STOP)"]
    end

    subgraph Phase4["Phase 4: Governed Staging Promotion"]
        P3F -->|PO Authorized| P4Pre{"Source Preflight Check (Dev Manifest @ commit SHA)"}
        P4Pre -->|FAIL / Mismatch / Unverified| P4Block["Fail-Closed Promotion Blocker (STOP)"]
        P4Pre -->|PASS (Dev evidence valid for SHA)| P4A["Prepare Promotion Branch (promotion/...)"]
        P4A --> P4B["Submit PR to staging & Validate Remote CI (ci.yml)"]
        P4B --> P4C["Owner PR Sign-Off & Merge into origin/staging"]
    end

    subgraph Phase5["Phase 5: Live Staging Deployment Verification & Release Gates"]
        P4C --> P5A["Deploy Frontend (Vercel) & Backend (OCI VM 129.225.86.241)"]
        P5A --> P5B["Verify Deployed Versions & Endpoints (verify_promotion.py --deployed)"]
        P5B --> P5C["Tier 1 Mandatory Live Staging Smoke Gate (smoke.staging.e2e.ts)"]
        P5C --> P5D{"Extraction / Worker Changed?"}
        P5D -->|Yes| P5E["Tier 2 Conditional Live Extraction Gate (ALLOW_DB_WRITES=false)"]
        P5D -->|No| P5F["Record Commit-Bound Evidence Manifest"]
        P5E --> P5F
        P5F --> P5G["Owner Staging Sign-Off in SIGN_OFF.md (STOP)"]
    end

    subgraph Phase6["Phase 6: Governed Production Release & Closeout"]
        P5G -->|Explicit Written Authorization| P6Pre{"Source Preflight Check (Staging Live Manifest @ commit SHA)"}
        P6Pre -->|FAIL / Mocked Evidence / Mismatch| P6Block["Fail-Closed Promotion Blocker (STOP)"]
        P6Pre -->|PASS (Live Staging evidence bound to SHA)| P6A["Deploy to Production (universal-pro-ai.vercel.app & OCI 140.245.214.28)"]
        P6A --> P6B["Post-Deployment Non-Destructive Live Smoke Check"]
        P6B --> P6C{"Production Smoke PASS?"}
        P6C -->|FAIL| P6D["Halt Progression, Alert Owner, Execute Bounded Rollback (Runbook 25)"]
        P6C -->|PASS| P6E["Owner Final Closeout (SIGN_OFF.md & JIRA_BACKLOG.md Released)"]
    end
```

---

## 4. SUBSYSTEM CALL HIERARCHY & DEPENDENCY MAP

| Entry Point / Route | Primary Module | Downstream Calls & Libraries | System of Record | Fallback Path |
| :--- | :--- | :--- | :--- | :--- |
| `POST /api/v1/extract` | `api/v1/extract.py` | `url_validator.py`, `supabase_client.py`, `quota_service.py` | Supabase `extractions` | `BackgroundTasks` if Redis down |
| `GET /api/v1/extract/status/{id}` | `api/v1/extract.py` | `job_manager.py`, `supabase_client.py` | In-memory `JobManager` / Supabase | Fallback to Supabase cache query |
| `GET /api/v1/extract/stream-video` | `api/v1/extract.py` | `url_validator.py`, `media_downloader.py`, `quota_service.py` | Ephemeral disk `/tmp/universalpro_media_cache` | Legacy `get_video_from_url` fallback |
| `POST /api/v1/library/{id}/export` | `api/v1/library.py` | `supabase_client.py`, `security.py` | Supabase `extractions` | In-memory `PlainTextResponse` |
| Worker Extraction Task | `workers/tasks.py` | `media_downloader.py`, `ai_router.py`, `affiliate_engine.py`, `supabase_client.py` | Supabase `extractions` | Cascade failover across Gemini Flash models |
| Gemini Multimodal Processor | `services/gemini_processor.py` | `google-genai` SDK (`client.files`, `client.models`) | In-memory metadata | Failover: 3.8 $\rightarrow$ 3.7 $\rightarrow$ 3.6 $\rightarrow$ 3.5 |
| Multi-LLM Council Consensus | `services/llm_council.py` | `gemini_processor.py`, `mistral_processor.py`, `groq_processor.py` | In-memory report | Degrades to single provider if keys missing |
| Affiliate Link Enrichment | `services/affiliate_engine.py` | `urllib.parse.quote_plus` | Immutable constants | Dynamic store link suppression by category |
| Telegram Bot Listener | `services/telegram_bot.py` | `url_validator.py`, `extract.py`, `requests` | Telegram Bot API | Error message dispatch to chat |
| WhatsApp Cloud Webhook | `services/whatsapp_service.py` | `url_validator.py`, `hmac`, `requests` | Meta Graph API | Fail-closed signature verification |
| Governance Contract Verification | `tests/test_sprint14_commerce.py` | `AGENTS.md` (line-anchored Section 9 slice), `docs/USER_MANUAL.md`, `FaqSection.tsx` | `AGENTS.md` | Explicit missing-path diagnostics |
| Mocked E2E Release Verification | `frontend/e2e/specs/app.spec.ts` | Playwright mock route fixtures, `http://localhost:3000` | In-memory Next.js test server | Fail build on regression |
| Tier 1 Live Staging Smoke Gate | `frontend/e2e/specs/smoke.staging.e2e.ts` | Vercel Staging preview origin, Vercel edge bypass cookie, backend origin (`STAGING_API_URL` / `http://129.225.86.241`), `validateNavigationResponse` | Vercel Edge Staging | Block Staging acceptance on failure (offline unit-tested; not yet run against live Staging) |
| Tier 2 Conditional Extraction E2E | `frontend/e2e/specs/staging.live.e2e.ts` | Media downloader, OCI Staging VM (`129.225.86.241`), `ALLOW_DB_WRITES=false` | Ephemeral Redis/memory JobManager | Block Staging sign-off on failure |
| Promotion Manifest Verification | `scripts/promote.py` & `scripts/verify_promotion.py` | `verify_evidence_manifest`, `validateEvidenceManifest`, commit SHA check | Commit-bound `evidence-manifest.json` | Rejects mocked evidence for staging/prod; blocks promotion on missing/mismatched SHA |
| Definitive Rule 16 CI Pipeline | `scripts/ci_check.py` | `npx tsc`, `npm run lint`, `npm test`, `npm run build`, `pytest tests/` | Immutable Rule 16 Contract | Zero-defect promotion blocker |
