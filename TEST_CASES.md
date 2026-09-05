# 🧪 Universal Pro AI — QA & Test Case Specification

**Product**: Universal Reel & Shorts AI Extractor (Universal Pro AI)  
**Document Owner**: QA & Systems Engineering  
**Current Status**: Active Test Suite (45+ Automated Unit Tests Passing)  
**Last Updated**: September 2026  

---

## 📊 Test Suite Coverage Summary

| Category | Test Case IDs | Automated Coverage | Manual / Cloud Verification | Status |
| :--- | :--- | :--- | :--- | :--- |
| **1. Functional & Domain Extraction** | `TC-FUNC-01` to `05` | `tests/test_e2e.py`, `tests/test_api_gateway.py` | Verified on Live Streamlit Cloud | ✅ 100% Passed |
| **2. Ingestion & Boundary Limits** | `TC-ING-01` to `05` | `tests/test_qa_suite.py`, `tests/test_e2e.py` | Verified with yt-dlp & regex | ✅ 100% Passed |
| **3. Monetization & Affiliate Routing** | `TC-MON-01` to `04` | `tests/test_e2e.py`, `tests/test_qa_suite.py` | Amazon & EarnKaro tag validation | ✅ 100% Passed |
| **4. Distribution & Messaging** | `TC-DIST-01` to `04` | `tests/test_e2e.py`, `tests/test_qa_suite.py` | WhatsApp deep links & file exports | ✅ 100% Passed |
| **5. UI/UX & Performance** | `TC-PERF-01` to `03`, `TC-UI-01` | Browser subagents & CSS checks | Responsive mobile/desktop verified | ✅ 100% Passed |

---

## 📋 Comprehensive Test Matrix

### 1. Functional & Domain Extraction

| Test Case ID | Feature / Module | Preconditions | Test Steps & Input Data | Expected Result | Priority | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-FUNC-01** | Recipe Extraction (Happy Path) | App loaded; Auto-Detect domain. | 1. Paste valid 30s cooking Reel/Short.<br>2. Click "Extract Intelligence". | • Neural Scanner engages with phase indicators.<br>• Domain: `Recipes & Cooking`.<br>• Ingredients listed with quantities & preparation steps.<br>• Quick commerce & Amazon links generated. | High | ✅ Passed |
| **TC-FUNC-02** | Product/Gadget Intent Detection | App loaded; Auto-Detect domain. | 1. Paste link to a "Kitchen Gadget / Amazon Find" Reel.<br>2. Click "Extract Intelligence". | • Domain: `Kitchen Finds & Product Gadgets`.<br>• Items display estimated price range & core utility.<br>• Shoppable Catalog displays Amazon, Flipkart, Meesho, Myntra. | High | ✅ Passed |
| **TC-FUNC-03** | Tech & Code Tutorial Extraction | App loaded; Tech/DIY domain. | 1. Paste link to coding/dev Reel (Python, Docker, terminal tip).<br>2. Click "Extract Intelligence". | • Domain: `Tech & DIY Tutorials`.<br>• Code blocks render inside syntax-highlighted blocks.<br>• YouTube search and GitHub query links render. | Medium | ✅ Passed |
| **TC-FUNC-04** | Direct MP4 File Upload | App loaded; user has local MP4 (<90s, <50MB). | 1. Drag & drop `.mp4` into file uploader.<br>2. Click "Extract Intelligence". | • Upload completes successfully.<br>• Frames and audio bypass `yt-dlp` directly to AI router.<br>• Structured breakdown renders identically to URL flow. | High | ✅ Passed |
| **TC-FUNC-05** | Multimodal Fallback Router | Primary Gemini quota exhausted / 503 error. | 1. Submit valid Reel under simulated Gemini outage.<br>2. Observe server router logs. | • Multi-provider router seamlessly fails over to Mistral AI + Groq Whisper.<br>• User receives extraction without UI crash or raw traceback. | Critical | ✅ Passed |

---

### 2. Ingestion, Platform Scrapers & Boundary Limits

| Test Case ID | Scenario / Edge Case | Test Input | Expected Result | Priority | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-ING-01** | Duration Guardrail Limit | Video link exceeding 90s (e.g. 10-min YouTube video). | • Ingestion intercepts video duration.<br>• Processing halts with: *"Video is Xs long. Videos must be under 90 seconds."*<br>• Zero quota or heavy LLM compute consumed. | High | ✅ Passed |
| **TC-ING-02** | Private / Deleted Video Link | Link to private Instagram post or deleted TikTok. | • `yt-dlp` fails gracefully.<br>• UI displays: *"Unable to retrieve video. Ensure the post is public."*<br>• App does not crash with unhandled exception. | High | ✅ Passed |
| **TC-ING-03** | Invalid / Malformed URL | Non-URL text (`htp://insta.reel/123`, random strings). | • Regex catches invalid input.<br>• Highlights input: *"Please enter a valid social media video URL."* | Medium | ✅ Passed |
| **TC-ING-04** | Audio-Only Video (No Speech) | Cooking Reel featuring only music + text overlays. | • Visual inspection (Gemini 2.5 Flash OCR) parses text overlays & actions.<br>• Full recipe output constructed accurately despite empty audio. | High | ✅ Passed |
| **TC-ING-05** | Platform Rate Limit (HTTP 429) | Rapid sequential submissions. | • Fallback Playwright headless browser engages if `yt-dlp` encounters rate limits.<br>• Residential proxy rotation bypasses cloud IP limits. | Medium | ✅ Passed |

---

### 3. Monetization & Affiliate Link Validation

| Test Case ID | Test Target | Verification Steps | Acceptance Criteria | Priority | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-MON-01** | Amazon Associates Tagging | 1. Extract recipe containing "Olive Oil".<br>2. Inspect generated Amazon link. | • URL contains `tag=manasdas11155-21`.<br>• Search query `k=Olive+Oil` properly URL-encoded.<br>• Link opens in new tab (`target="_blank"`). | Critical | ✅ Passed |
| **TC-MON-02** | EarnKaro Link Aggregation | 1. Extract a gadget video.<br>2. Click Flipkart or Meesho button. | • URL routes through `https://earnkaro.com/deals?r=5608766&url=...`<br>• Decodes to target product search on merchant. | High | ✅ Passed |
| **TC-MON-03** | Quick Commerce 10-Min Delivery | 1. Inspect Quick Commerce shelf for "Butter". | • Blinkit: `https://blinkit.com/s/?q=Butter`<br>• Zepto: `https://www.zeptonow.com/search?q=Butter`<br>• Swiggy Instamart URL properly formatted. | High | ✅ Passed |
| **TC-MON-04** | Admin Vault Access | 1. Append `?admin=1` to base URL.<br>2. Open app without query parameter. | • With `?admin=1`: Admin credentials/vault sidebar unlocks for key configuration.<br>• Without parameter: Admin credentials remain completely hidden from consumers. | High | ✅ Passed |

---

### 4. Distribution, Messaging & Export Options

| Test Case ID | Feature | Execution Steps | Expected Result | Priority | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-DIST-01** | WhatsApp Deep Link | 1. Complete an extraction.<br>2. Click "Share via WhatsApp". | • Mobile: Launches WhatsApp app with formatted text pre-filled.<br>• Desktop: Opens `web.whatsapp.com`.<br>• Text contains domain badge, ingredients/steps, and source credit. | High | ✅ Passed |
| **TC-DIST-02** | Direct Messaging Dispatch | 1. Enter valid phone number in sidebar.<br>2. Trigger extraction with WhatsApp delivery toggled ON. | • Ingestion completes.<br>• Formatted message payload dispatches to phone number without requiring active tab. | Medium | ✅ Passed |
| **TC-DIST-03** | File Downloads (`.txt` & `.mp4`) | 1. Complete an extraction.<br>2. Click "Download .txt Notes".<br>3. Click "Download Clean Video". | • `.txt` file downloads immediately with human-readable formatting.<br>• Processed `.mp4` downloads directly from session cache without re-scraping. | Medium | ✅ Passed |
| **TC-DIST-04** | Native Mobile Share | 1. Open app in mobile Chrome / Safari.<br>2. Tap "Share to Apps". | • Native OS share sheet opens.<br>• Payload properly parsed by destination apps (Notes, Telegram, Slack). | Low | ✅ Passed |

---

### 5. UI/UX, Concurrency & Performance Benchmarks

| Test Case ID | Test Category | Target Threshold / Scenario | Expected Result | Priority | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-PERF-01** | Latency Benchmark | Ingest standard 30–45s Reel. | • Download phase: $\le 4.0\text{s}$<br>• AI Prep & Upload: $\le 9.0\text{s}$<br>• Multimodal Inference: $\le 10.0\text{s}$<br>• Total Turnaround: $\le 23.0\text{s}$ | High | ✅ Passed |
| **TC-PERF-02** | Real-Time Phase Animation | App in extraction state (0s to 20s). | • Neural Scanner Deck continuously animates.<br>• Ticker cycles status every 3–4s.<br>• UI remains responsive with no browser freeze. | Medium | ✅ Passed |
| **TC-UI-01** | Glassmorphism & Responsive Layout | Desktop (1920x1080), Tablet (768px), Mobile (390px). | • Dark luxury theme (`#0A0E1A`) renders cleanly with zero horizontal bleed.<br>• Store badges wrap cleanly into grid cards on mobile.<br>• Text contrast meets WCAG AA standards. | Medium | ✅ Passed |
| **TC-PERF-03** | Concurrency Load Check | 5 simultaneous users trigger extraction on Streamlit Cloud. | • Session states isolated per user.<br>• Zero variable leakage across sessions.<br>• Container memory remains within limits without rebooting. | Critical | ✅ Passed |
