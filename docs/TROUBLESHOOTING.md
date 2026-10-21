# 🛠️ Universal Video Extractor — Troubleshooting & Issue Resolution Log

This document serves as our permanent log for all errors, bugs, and edge cases encountered during the development and deployment of the **Universal Reel & Shorts AI Extractor**. 

Whenever an issue occurs, we log it here in simple English along with the root cause, the exact code changes made, and how to verify the fix.

---

## 📋 Table of Issues

| Issue ID | Date | Category | Summary | Status |
| :--- | :--- | :--- | :--- | :--- |
| **ISSUE-001** | 2026-09-04 | Windows OS | `UnicodeEncodeError: 'charmap' codec can't encode character` | ✅ Resolved |
| **ISSUE-002** | 2026-09-04 | User Experience | Perceived slowness & frozen UI during long video uploads (18-25s) | ✅ Resolved |
| **ISSUE-003** | 2026-09-04 | AI Prompting | Reels classified as recipes instead of kitchen finds or tutorials | ✅ Resolved |
| **ISSUE-004** | 2026-09-05 | Product Extraction | No product buy links generated for kitchen gadgets shown in reels | ✅ Resolved |
| **ISSUE-005** | 2026-09-05 | Monetization | How to create working affiliate links for Flipkart and Meesho | ✅ Resolved |
| **ISSUE-006** | 2026-09-05 | Streamlit UI | HTML buttons rendered as raw code block text `<pre><code>` | ✅ Resolved |
| **ISSUE-007** | 2026-09-05 | Cloud Deployment | `ImportError: cannot import name 'get_video_from_url'` on Streamlit Cloud | ✅ Resolved |
| **ISSUE-008** | 2026-09-05 | Cloud Deployment | Custom subdomain error: "can't include the term 'staging'" on Streamlit Cloud | ✅ Resolved |
| **ISSUE-009** | 2026-09-07 | Cloud Uptime | Streamlit Cloud sleep timeout ("Zzzz This app has gone to sleep due to inactivity") | ✅ Resolved |
| **ISSUE-010** | 2026-09-08 | DNS & Domain | Hostinger domain `mpdtech.in` suspended due to NIXI registry KYC audit | ✅ Resolved |
| **ISSUE-011** | 2026-09-08 | Cloud Provisioning| Oracle Cloud image architecture incompatibility warning (`aarch64` vs `x86`) | ✅ Resolved |
| **ISSUE-012** | 2026-09-08 | Cloud Networking | Oracle Cloud public IPv4 toggle locked in VM wizard due to unattached Internet Gateway | ✅ Resolved |
| **ISSUE-013** | 2026-09-08 | Cloud Compute | Oracle Cloud Ampere A1 ARM host out-of-capacity error in availability domain AD-1 | ✅ Resolved |
| **ISSUE-014** | 2026-09-08 | Cloud Console | Oracle API rate limit ("Too many requests for the user") during instance creation | ✅ Resolved |
| **ISSUE-015** | 2026-09-08 | Security & SSH | Windows OpenSSH private key rejected: "bad permissions / key is too open" | ✅ Resolved |
| **ISSUE-016** | 2026-09-08 | Remote Operations | SSH connection reset silently drops to local PowerShell during `.env` creation | ✅ Resolved |
| **ISSUE-017** | 2026-09-08 | Docker Runtime | `NameError: name 'Any' is not defined` in `quota_service.py` on Python 3.11 | ✅ Resolved |
| **ISSUE-018** | 2026-09-08 | Frontend / AI | Next.js PWA reverted to recipe-only copy instead of multi-genre Universal AI | ✅ Resolved |
| **ISSUE-019** | 2026-09-08 | Docker & Worker | Celery worker failed with `No module named 'ai_router'` | ✅ Resolved |
| **ISSUE-020** | 2026-09-08 | Python 3.11 Runtime | `NameError: name 'Any' is not defined` in `gemini_processor.py:792` | ✅ Resolved |
| **ISSUE-021** | 2026-09-08 | Frontend / AI | Instagram Reel preview static fallback & missing structured details/notes in PWA UI | ✅ Resolved |
| **ISSUE-026** | 2026-09-15 | UI/UX & AI | Recipe Notes Lumping All Items into Steps 1..16 vs. 3-Section Format | ✅ Resolved |
| **ISSUE-027** | 2026-09-13 | Skills | Global Anthropic Agent Skills Installation (19 Production Skills) | ✅ Resolved |
| **ISSUE-028** | 2026-09-13 | UI/UX & Skills | Autonomous Playwright WebApp Visual & Functional E2E Audit (`webapp-testing` Skill) | ✅ Resolved |
| **ISSUE-029** | 2026-09-14 | Multi-LLM AI | Multi-LLM Council 3-Stage Consensus Engine (`karpathy/llm-council` Adaptation) | ✅ Resolved |
| **ISSUE-030** | 2026-09-14 | UI/UX & Design | Light Mode WCAG AA Contrast, 3D Feathered Radial Mask, and Streamlined Hero | ✅ Resolved |
| **ISSUE-031** | 2026-09-14 | Skills & Customizations | Global Agent Skills Installation from Downloads/Skill Files (Total 53 Skills) | ✅ Resolved |
| **ISSUE-032** | 2026-09-15 | UI/UX & Design | Minimalist UI Overhaul, Interior/Gaming Categories, Deprecated Model Pruning & E2E Validation | ✅ Resolved |
| **ISSUE-045** | 2026-09-20 | Security & Architecture | Security Hardening, Pure Function Refactoring, WCAG Accessibility, Admin Telemetry & Vault Rehydration | ✅ Resolved |
| **ISSUE-046** | 2026-09-20 | Security & Rule Enforcement | TRUSTED_PROXY Default, Egress Firewall Verification, IP Pinning SNI, Streamlit Admin Removal & Vault Rehydration Wiring | ✅ Resolved |
| **ISSUE-047** | 2026-09-26 | Security & Network | IP Pinning & PinnedHTTPSConnection Security Hardening (UPA-1205) | ✅ Resolved |
| **ISSUE-048** | 2026-09-26 | Security & DevOps | Container Egress Firewall Hardening & Rollback Automation (UPA-1206) | ✅ Resolved |
| **ISSUE-049** | 2026-09-26 | Security & DevOps | Docker Egress Firewall Broad RFC1918 172.16/12 RETURN Rule Bypass (UPA-1206) | ✅ Resolved |
| **ISSUE-050** | 2026-09-27 | Dependencies & Security | Python 3.11 Dependency Cleanup, Dev Partitioning & Pinned Lockfile (UPA-1207) | ✅ Resolved |
| **ISSUE-051** | 2026-10-18 | Governance & Tests | Governance Heading Assertion Brittleness in Sprint 14 Commerce Suite (UPA-1311) | ✅ Resolved |
| **ISSUE-052** | 2026-10-19 | Governance & CI/CD | Operational Workflow Streamlining & Mandatory Two-Tier Playwright Release Gates (UPA-1401) | ✅ Resolved on Dev |
| **ISSUE-053** | 2026-10-19 | Quality Assurance & E2E | Tier 1 Staging Smoke Submit CTA Assertion Failure & Environment Classification Audit (UPA-1401) | 🟡 Resolved on Dev / Staging Retest Pending |
| **ISSUE-054** | 2026-10-20 | Quality Assurance & E2E | E2E Evidence Overwrite Collision Risk During Multi-Run Live Staging Releases (UPA-1403) | ✅ Resolved on Dev |
| **ISSUE-055** | 2026-10-20 | Testing & CI/CD | Remote Single-Branch CI Checkout Branch-Resolution Test Failure (UPA-1404) | 🟡 Resolved on Dev / Remote CI Pending |
| **ISSUE-056** | 2026-10-20 | Quality Assurance & E2E | Tier 2 Live Staging Extraction Cache-Hit Bypass & Worker Stage Validation Gap (UPA-1405) | ✅ Resolved on Dev |
| **ISSUE-057** | 2026-10-21 | Database & Security | Supabase PostgREST Data API Grant-Readiness, Function Hardening & Migration Directory Parity (UPA-1406) | ✅ Resolved on Dev |
| **ISSUE-058** | 2026-10-21 | Database & DevOps | Supabase Free-Tier Project Dormancy Risk & Staging Keep-Alive Monitoring (UPA-1409) | ✅ Resolved on Dev |

---




## 🔍 Detailed Issue Logs

---

### 🚨 ISSUE-001: Windows Console Unicode / Emoji Crash
- **Date**: 2026-09-04
- **Affected Files**: `app.py`, `downloader.py`, `gemini_processor.py`, `cli.py`

#### 1. What Happened (Symptom):
When printing log messages to the Windows PowerShell terminal that contained emojis (`🍳`, `🛍️`) or Indian rupee symbols (`₹`), Python crashed with:
```text
UnicodeEncodeError: 'charmap' codec can't encode character '\u20b9' in position 14: character maps to <undefined>
```

#### 2. Root Cause:
On Windows, the standard console encoding defaults to legacy Windows-1252 (`charmap`), which cannot encode modern Unicode characters (like `₹` or emojis).

#### 3. Resolution (Code Changes):
We implemented two safeguards:
1. Reconfigured `sys.stdout` and `sys.stderr` to use UTF-8 at the very top of each Python file.
2. Created a safe printing helper `safe_print()` that falls back cleanly without crashing if an unsupported terminal is used.

```python
# Added to top of Python files
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def safe_print(msg: str):
    """Safely prints strings containing emojis or ₹ symbols."""
    try:
        print(msg)
    except Exception:
        try:
            print(str(msg).encode("ascii", errors="replace").decode("ascii"))
        except Exception:
            pass
```

---

### 🚨 ISSUE-002: Perceived Slowness & Frozen UI During AI Processing
- **Date**: 2026-09-04
- **Affected Files**: `app.py`, `ui_components.py`, `gemini_processor.py`

#### 1. What Happened (Symptom):
Downloading videos, uploading them to the Gemini File API, and waiting for model inference took 15 to 25 seconds. During this time, the default Streamlit spinner gave no feedback, making the app feel slow, frozen, or broken to users.

#### 2. Root Cause:
Video processing is inherently compute-heavy. Without fine-grained step-by-step progress feedback, users perceived the wait time as an application freeze.

#### 3. Resolution (Code Changes):
1. **Active Neural Scanner (`ui_components.py`)**: Built an animated scanner deck with animated neon sweep lines (`@keyframes scanner-sweep`) and pulsing status beacons.
2. **Live Fun Facts & Trivia Ticker**: Rotated interesting AI trivia and tips every 3 seconds to keep users engaged.
3. **Step-by-Step Progress Updates**: Connected a real-time `status_callback` showing each exact phase:
   - Ingesting HD video stream (e.g. `2.3s`)
   - Cloud upload and keyframe preparation (e.g. `8.7s`)
   - AI multimodal neural analysis (e.g. `8.1s`)
   - Formatting and WhatsApp export prep

---

### 🚨 ISSUE-003: Video Misclassification (Kitchen Finds Marked as Recipes)
- **Date**: 2026-09-04
- **Affected Files**: `gemini_processor.py`, `app.py`

#### 1. What Happened (Symptom):
When uploading reels featuring kitchen gadgets or coding tutorials, the AI forced them into recipe templates (e.g., trying to find "ingredients" and "cooking instructions" for a portable mini blender or a Python tutorial).

#### 2. Root Cause:
The Gemini system prompt was hardcoded strictly for recipes (`RECIPE`), and the response parser only looked for ingredients and preparation steps.

#### 3. Resolution (Code Changes):
1. **Universal Multi-Category Schema (`gemini_processor.py`)**:
   Expanded the system prompt with a mandatory classification header:
   ```text
   [CATEGORY]: RECIPE | KITCHEN_FINDS | PRODUCT_FINDS | TUTORIAL | EDUCATIONAL | WORKOUT | FINANCE_BUSINESS | BEAUTY_FASHION | LIFE_HACKS | GENERAL
   ```
2. **Dynamic Template Adaptation**:
   - For **KITCHEN_FINDS / PRODUCT_FINDS**: Outputs item list, price brackets, key utility, and search keywords.
   - For **TUTORIAL / EDUCATIONAL**: Outputs core concepts, step-by-step guides, and learning resources.
   - For **RECIPE**: Outputs ingredients, preparation time, and cooking steps.
3. **Dynamic UI Banners (`app.py`)**: Added an AI Domain Classification badge at the top of the output card displaying verified categories with custom emojis.

---

### 🚨 ISSUE-004: Missing Product Buy Links for Items Shown in Reels
- **Date**: 2026-09-05
- **Affected Files**: `gemini_processor.py`, `app.py`

#### 1. What Happened (Symptom):
When a reel showcased multiple gadgets, no shopping links were displayed on the card.

#### 2. Root Cause:
1. Gemini did not have a dedicated structured output block for shoppable items.
2. If the AI didn't use an exact bullet format, the regex parser failed to extract the product names.

#### 3. Resolution (Code Changes):
1. **Standardized Format**: Added `[PRODUCTS]:` syntax to prompt guidelines:
   ```text
   [PRODUCTS]:
   - PRODUCT: <Name> | PRICE: <Price or Under ₹X> | SEARCH: <Clean Search Keyword>
   ```
2. **Secondary Regex Fallback**: If the `[PRODUCTS]` block is omitted by the AI, the parser searches the body text for bolded items (e.g., `### 1. **Portable Blender**`) and auto-generates store search links.
3. **Conditionality**: The "Featured Products" section is now only displayed if actual products exist, keeping recipe and educational cards clean and distraction-free.

---

### 🚨 ISSUE-005: Affiliate Linking for Flipkart and Meesho
- **Date**: 2026-09-05
- **Affected Files**: `config.py`, `gemini_processor.py`, `app.py`, `.env`

#### 1. What Happened (Symptom):
The user wanted affiliate links for Flipkart and Meesho similar to Amazon (`AMAZON_AFFILIATE_TAG`), but:
- Flipkart's direct in-house affiliate program often pauses new public signups.
- Meesho does not provide a standard `&tag=` query parameter on `meesho.com`.

#### 2. Root Cause:
Indian e-commerce platforms operate on different affiliate standards:
- **Amazon**: Direct parameter (`&tag=yourtag-21`).
- **Flipkart & Meesho**: Typically monetized via affiliate aggregators (**EarnKaro** or **Cuelinks**), which hold enterprise agreements with Flipkart (up to 8% profit) and Meesho (up to 15% profit).

#### 3. Resolution (Code Changes):
1. **EarnKaro / Cuelinks URL Wrapping (`gemini_processor.py`)**:
   Created `build_product_store_links()` supporting:
   - Direct Amazon Associates tag.
   - EarnKaro redirect format: `https://ekaro.in/enlinks?r=<EARNKARO_ID>&url=<encoded_store_url>`.
   - Cuelinks redirect format: `https://linksredirect.com/?cid=<CUELINKS_ID>&url=<encoded_store_url>`.
   - Direct Flipkart tag (`&affid=`) and Meesho campaign tag (`&utm_campaign=`).
2. **Environment Variable Configuration**:
   Added `EARNKARO_ID` support across `config.py` and the Admin Vault (`?admin=1`). Setting `EARNKARO_ID=5608766` automatically monetizes Flipkart, Myntra, Meesho, Ajio, Nykaa, and Shopsy simultaneously.

---

### 🚨 ISSUE-006: Streamlit Rendered HTML Buttons as Raw Code Blocks
- **Date**: 2026-09-05
- **Affected Files**: `app.py`

#### 1. What Happened (Symptom):
In the browser, the search buttons inside the "Recommended YouTube Tutorials" section rendered as plain text inside a dark gray `<pre><code>` code block rather than interactive HTML buttons:
```html
<a href="https://www.google.com/search?q=..." target="_blank" style="...">🔍 Search Google</a>
```

#### 2. Root Cause:
Python-Markdown (used internally by Streamlit's `st.markdown`) follows CommonMark specification: **any line indented with 4 or more spaces is automatically treated as an indented code block (`<pre><code>`)**, even when `unsafe_allow_html=True` is set! Because our HTML string was indented inside an `if` block, Streamlit parsed it as source code.

#### 3. Resolution (Code Changes):
Wrapped all multi-line HTML strings with `textwrap.dedent(...).strip()` before passing to `st.markdown()`:

```python
# Before (Buggy):
st.markdown(f"""
    <div class="product-box-luxury">
        <a href="...">Button</a>
    </div>
""", unsafe_allow_html=True)

# After (Fixed):
import textwrap
html_content = f"""
<div class="product-box-luxury">
    <a href="...">Button</a>
</div>
"""
st.markdown(textwrap.dedent(html_content).strip(), unsafe_allow_html=True)
```

---

### 🚨 ISSUE-007: Streamlit Cloud `ImportError` on Deployment
- **Date**: 2026-09-05
- **Affected Files**: `app.py`, `downloader.py`

#### 1. What Happened (Symptom):
Immediately after merging `Dev` into `main`, the live Streamlit Cloud deployment (`https://manas-recipe-extractor.streamlit.app/`) crashed with:
```text
ImportError: This app has encountered an error. The original error message is redacted to prevent data leaks.
Traceback:
File "/mount/src/recipe-extractor/app.py", line 52, in <module>
    from downloader import get_video_from_url, detect_platform
```

#### 2. Root Cause:
1. **Stale In-Memory Module Cache**: Streamlit Cloud hot-reloads `app.py` when new Git commits are pushed, but Python retains already-imported modules in `sys.modules`. The running process still had the old `downloader.py` in memory (which only exported `get_recipe_video`, not the newly added `get_video_from_url` or `detect_platform`).
2. **Missing `sys.path` Priority**: On Linux cloud containers (`/mount/src/recipe-extractor/`), the script root was not explicitly placed first in `sys.path`.

#### 3. Resolution (Code Changes):
1. **Prioritized Root Directory in `sys.path`**:
   ```python
   ROOT_DIR = str(Path(__file__).parent.resolve())
   if ROOT_DIR not in sys.path:
       sys.path.insert(0, ROOT_DIR)
   ```
2. **Dynamic Safe Module Reloader (`_safe_load_module`)**:
   Created a helper in `app.py` that forces a fresh reload of all internal modules (`config`, `downloader`, `gemini_processor`, `ai_router`, `ui_components`, `whatsapp_service`) upon hot-reloads:
   ```python
   def _safe_load_module(module_name: str):
       try:
           mod = importlib.import_module(module_name)
           return importlib.reload(mod)
       except Exception:
           return importlib.import_module(module_name)
   ```
3. **Resilient Attribute Extraction**:
   Used `getattr()` with fallback defaults so missing functions never trigger fatal uncaught `ImportError` crashes:
   ```python
   downloader = _safe_load_module("downloader")
   get_video_from_url = getattr(downloader, "get_video_from_url", getattr(downloader, "get_recipe_video", None))
   detect_platform = getattr(downloader, "detect_platform", lambda url: "Instagram Reel" if "instagram" in url.lower() else "Web Video")
   ```

---

### 🚨 ISSUE-008: Streamlit Cloud Disallows "staging" in Subdomain
- **Date**: 2026-09-05
- **Affected Environment**: Streamlit Cloud Deployment Settings

#### 1. What Happened (Symptom):
When attempting to deploy the staging branch with the custom subdomain `universalpro-staging.streamlit.app`, Streamlit Cloud displayed a red validation error:
```text
Custom subdomains can't include the term 'staging'. Please provide an alternative subdomain.
```

#### 2. Root Cause:
Streamlit Community Cloud has a platform-level routing rule that reserves the keyword `"staging"` for internal Streamlit platform infrastructure and testing environments, blocking all user apps from using `"staging"` anywhere in custom subdomains.

#### 3. Resolution:
Use industry-standard alternative staging/testing environment prefixes that are accepted by Streamlit Cloud:
- **`universalpro-stage`** (Recommended) $\rightarrow$ `https://universalpro-stage.streamlit.app/`
- **`universalpro-test`** $\rightarrow$ `https://universalpro-test.streamlit.app/`
- **`universalpro-beta`** $\rightarrow$ `https://universalpro-beta.streamlit.app/`
- **`universalpro-preview`** $\rightarrow$ `https://universalpro-preview.streamlit.app/`

#### 4. Testing & Verification:
Entering `universalpro-stage` or `universalpro-beta` satisfies Streamlit's subdomain validation and enables the "Deploy" button.

---

### 🚨 ISSUE-009: Streamlit Community Cloud Sleep Timeout / Hibernation
- **Date**: 2026-09-07
- **Affected Environments**: `manas-recipe-extractor.streamlit.app`, `universalpro-stage.streamlit.app`

#### 1. What Happened (Symptom):
When accessing the live or staging web application after periods of zero traffic, visitors were greeted with an asleep screen:
```text
Zzzz This app has gone to sleep due to inactivity.
```
Clicking "Yes, get this app back up" took 45 to 90 seconds to reboot the container.

#### 2. Root Cause:
Streamlit Community Cloud is designed as a free tier that automatically hibernates inactive apps after prolonged periods of zero HTTP requests to conserve platform container resources.

#### 3. Resolution (Code Changes):
1. **Automated Health Pinger (`scripts/keep_alive.py`)**: Built an automated Python probe that issues periodic HTTP HEAD/GET requests with custom browser user-agent headers and exponential backoff.
2. **GitHub Actions Scheduled Keep-Alive Workflow (`.github/workflows/keep_alive.yml`)**: Configured a GitHub Actions cron trigger running every 6 hours (`0 */6 * * *`) that executes `keep_alive.py`, ensuring containers never enter dormancy.

---

### 🚨 ISSUE-010: Hostinger Domain `mpdtech.in` Suspended Due to NIXI KYC Audit
- **Date**: 2026-09-08
- **Affected Services**: Custom domain resolution on Hostinger

#### 1. What Happened (Symptom):
The domain `mpdtech.in` displayed a red `Suspended` badge with a lock icon in the Hostinger control panel despite active registration paid through February 2027.

#### 2. Root Cause:
The National Internet Exchange of India (NIXI), which governs the `.IN` top-level domain registry, initiated a mandatory registrant contact KYC compliance verification. Domains not verified via government ID within the regulatory window are placed in `ClientHold / Suspended` status.

#### 3. Resolution:
Decoupled SaaS production deployment from the suspended domain. Chose to route traffic directly through Oracle Cloud's permanent static public IP (`140.245.214.28`) and Vercel's global CDN (`*.vercel.app`), enabling instant production deployment without waiting days for NIXI ticket clearance.

---

### 🚨 ISSUE-011: Oracle Cloud OS Image Architecture Incompatibility (`aarch64` vs `x86`)
- **Date**: 2026-09-08
- **Affected Component**: Oracle Cloud Infrastructure Instance Creation Wizard

#### 1. What Happened (Symptom):
When selecting the Ubuntu OS image, Oracle displayed an amber warning banner:
```text
Warning: This image has no compatible image builds for the current shape. If you select this image, a compatible shape and image build will be selected.
```

#### 2. Root Cause:
The user selected `Canonical Ubuntu 24.04 Minimal aarch64`, which compiles specifically for 64-bit ARM processors, whereas the instance wizard had defaulted to an x86 AMD compute shape.

#### 3. Resolution:
Selected standard `Canonical Ubuntu 24.04` (x86_64 compatible), immediately clearing the architecture conflict.

---

### 🚨 ISSUE-012: Oracle Cloud Public IPv4 Toggle Locked in VM Wizard
- **Date**: 2026-09-08
- **Affected Component**: Oracle Virtual Cloud Network (VCN) Subnet Configuration

#### 1. What Happened (Symptom):
In the Compute Instance creation wizard, the toggle for *"Automatically assign public IPv4 address"* was disabled with warning:
```text
Warning: You must select a public subnet to assign a public IPv4 address.
```

#### 2. Root Cause:
Creating a VCN inline within the VM Instance creation screen fails to attach an Internet Gateway and route table entry (`0.0.0.0/0` $\rightarrow$ `IGW`) before the subnet is saved, causing Oracle to treat the new subnet as private.

#### 3. Resolution:
1. Opened **Networking** $\rightarrow$ **Virtual Cloud Networks** in a separate browser tab.
2. Executed **Start VCN Wizard** $\rightarrow$ **Create VCN with Internet Connectivity** (`universalpro-ai-vcn`).
3. Returned to the VM creation tab and selected `universalpro-ai-vcn` and its public subnet. The warning cleared instantly and the public IP toggle enabled automatically.

---

### 🚨 ISSUE-013: Oracle Cloud Ampere A1 Host Capacity Shortage (AD-1)
- **Date**: 2026-09-08
- **Affected Component**: Oracle Cloud Compute Shape Provisioning

#### 1. What Happened (Symptom):
Clicking Create Instance for shape `VM.Standard.A1.Flex` (4 core OCPU, 24 GB RAM) failed with:
```text
API Error: Out of capacity for shape VM.Standard.A1.Flex in availability domain AD-1. Create the instance in a different availability domain or try again later.
```

#### 2. Root Cause:
Physical 4-core Ampere ARM hardware hosts were fully allocated in the `ap-hyderabad-1` data center due to high regional demand for Always Free tier ARM compute.

#### 3. Resolution:
1. Switched shape to the high-availability AMD Always Free tier: **`VM.Standard.E2.1.Micro`** (1 OCPU, 1 GB RAM).
2. Provisioned a **2 GB Linux Virtual Swap File** (`/swapfile`) on the Ubuntu filesystem, expanding effective memory to 3 GB to comfortably run FastAPI, Celery workers, and Redis without memory exhaustion.

---

### 🚨 ISSUE-014: Oracle Console API Rate Limiter
- **Date**: 2026-09-08
- **Affected Component**: Oracle Cloud Web Console / OCI API

#### 1. What Happened (Symptom):
Clicking the Create button in rapid succession returned:
```text
API Error: Too many requests for the user
```

#### 2. Root Cause:
OCI enforces an anti-spam rate limit on instance creation API endpoints when requests fail repeatedly within a short time frame.

#### 3. Resolution:
Enforced a 60-second cooldown period before retrying. Once the rate limit window reset, the request succeeded immediately.

---

### 🚨 ISSUE-015: Windows OpenSSH Key File Rejected ("Key is Too Open")
- **Date**: 2026-09-08
- **Affected Component**: Windows PowerShell OpenSSH Client

#### 1. What Happened (Symptom):
Attempting to connect to the cloud server via `ssh -i ssh-key-2026-09-08.key ubuntu@140.245.214.28` failed with:
```text
WARNING: UNPROTECTED PRIVATE KEY FILE!
Permissions for 'ssh-key-2026-09-08.key' are too open.
It is required that your private key files are NOT accessible by others.
Load key "ssh-key-2026-09-08.key": bad permissions
ubuntu@140.245.214.28: Permission denied (publickey).
```

#### 2. Root Cause:
Windows NTFS file inheritance granted read permissions to user groups (`NT AUTHORITY\Authenticated Users`, `BUILTIN\Users`, `BUILTIN\Administrators`). OpenSSH strictly mandates that private keys be readable exclusively by the owner.

#### 3. Resolution:
Used the Windows `icacls` command-line utility to break inheritance and revoke all access except for the active user:
```powershell
icacls "ssh-key-2026-09-08.key" /inheritance:r
icacls "ssh-key-2026-09-08.key" /grant:r "$($env:USERNAME):(R)"
icacls "ssh-key-2026-09-08.key" /remove "NT AUTHORITY\Authenticated Users"
icacls "ssh-key-2026-09-08.key" /remove "BUILTIN\Users"
icacls "ssh-key-2026-09-08.key" /remove "BUILTIN\Administrators"
```
Re-running `ssh` authenticated and logged into the server immediately.

---

### 🚨 ISSUE-016: SSH Session Timeout / Disconnect Silently Resets Terminal to Local PowerShell
- **Date**: 2026-09-08
- **Affected Environment**: Windows Terminal / PowerShell SSH Session

#### 1. What Happened (Symptom):
While creating the server `.env` file, the SSH connection closed unexpectedly with:
```text
client_loop: send disconnect: Connection reset
PS D:\Personal Projects\New folder>
```
When the user pasted a multi-line bash command (`cat << 'EOF' > .env`), Windows PowerShell executed the text locally and threw syntax errors:
```powershell
Missing file specification after redirection operator.
The '<' operator is reserved for future use.
GEMINI_API_KEY=... : The term 'GEMINI_API_KEY=...' is not recognized as the name of a cmdlet...
```

#### 2. Root Cause:
The remote SSH socket experienced an idle timeout or connection reset from the network router. Because the terminal prompt changed from `ubuntu@universal-pro-ai-vnic:~$` back to `PS D:\...>`, the user unknowingly executed bash-specific commands inside native Windows PowerShell.

#### 3. Resolution:
1. Instead of manually pasting sensitive secrets in an interactive terminal session that might disconnect, we used **`scp`** directly from the local machine:
   ```powershell
   scp -i "D:\Personal Projects\New folder\ssh-key-2026-09-08.key" -o StrictHostKeyChecking=no "D:\Personal Projects\recipe-extractor\.env" ubuntu@140.245.214.28:~/recipe-extractor/.env
   ```
2. This transferred `.env` with atomic reliability in 2 seconds, with zero terminal copy-paste errors or clipboard leak.

---

### 🚨 ISSUE-017: Python 3.11 Runtime `NameError: name 'Any' is not defined` inside Docker
- **Date**: 2026-09-08
- **Affected Files**: `backend/app/services/quota_service.py`
- **Affected Components**: Docker Container (`universalpro-api`, `universalpro-worker`)

#### 1. What Happened (Symptom):
When launching the Docker container stack via `docker compose up -d --build`, `universalpro-api` crashed repeatedly on startup. Inspecting container logs (`docker compose logs api`) revealed:
```text
File "/app/backend/app/services/quota_service.py", line 135, in QuotaManager
    ) -> Dict[str, Any]:
NameError: name 'Any' is not defined
```

#### 2. Root Cause:
In `backend/app/services/quota_service.py`, the import statement was:
```python
from typing import Tuple, Dict, Optional
```
`Any` was missing from the import list. Under modern development environments (like Python 3.14 on Windows), deferred evaluation of type hints may mask this error at import time. However, in the production Docker image running Python 3.11, class definition methods evaluate type annotations at import time, triggering an immediate fatal `NameError`.

#### 3. Resolution (Code Changes):
Added `Any` to the typing imports in `backend/app/services/quota_service.py`:
```python
# Before
from typing import Tuple, Dict, Optional

# After
from typing import Tuple, Dict, Optional, Any
```

#### 4. Testing & Verification:
Rebuilt and restarted the containers on the Oracle Cloud server:
```bash
git pull origin main
docker compose up -d --build api worker
```
Both `universalpro-api` and `universalpro-worker` started cleanly. 
Health check confirmed HTTP 200 with all integrations verified:
```json
{"status":"healthy","service":"Universal Pro AI - API Gateway","version":"1.0.0","integrations":{"supabase":true,"gemini":true,"groq":true,"mistral":true}}
```

---

### 🚨 ISSUE-018: Next.js PWA Reverted to Recipe-Only Copy instead of Multi-Genre Universal Extractor
- **Date**: 2026-09-08
- **Affected Files**: `frontend/src/app/page.tsx`, `backend/app/api/v1/extract.py`

#### 1. What Happened (Symptom):
After successfully deploying the Next.js 15 PWA frontend on Vercel, the user noticed that the interface had reverted to recipe-specific branding (*"Turn Any Cooking Video into a Structured Recipe & Pantry Cart"*, *"Extract Recipe"*, *"Recipe Vault"*, and recipe-only sample chips), whereas the Streamlit application had already evolved into the full **Universal Reel & Shorts AI Extractor** (handling recipes, workout routines, tech tutorials, unboxings, and product finds).

#### 2. Root Cause:
During initial Next.js scaffolding in Sprint 6, static placeholder copy and labels were copied from early Sprint 1 recipe mockups. Meanwhile, the backend AI models (`gemini_processor.py`, `ai_router.py`, `app.py`) already supported full multi-domain auto-detection and prompt routing (`Auto-Detect (Universal AI)`, `🍳 Cooking`, `🏋️ Fitness`, `💻 Tech Tutorials`, `🛍️ Kitchen & Home Gadgets`, `📦 Product Unboxing`, `💡 Life Hacks`). The Next.js frontend UI had not yet been updated to expose the Content Domain selector and multi-category layout. Furthermore, the FastAPI backend endpoint `ExtractRequest` strictly expected `video_url`, while frontend payloads sometimes sent `url`.

#### 3. Resolution (Code Changes):
1. **Frontend Multi-Genre Upgrade (`frontend/src/app/page.tsx`)**:
   - Replaced hero title with **Universal Reel & Shorts AI Extractor** and multi-genre subtitle.
   - Added interactive **🎯 Content Domain selector** above the input bar with 7 options (`Auto-Detect`, `Cooking & Recipes`, `Fitness & Workouts`, `Tech Tutorials & Coding`, `Kitchen Finds & Gadgets`, `Product Unboxing`, `Life Hacks`).
   - Added multi-genre sample buttons (`🍳 Butter Chicken Reel`, `🏋️ 6 Core Exercises Workout`, `💻 Quick Python Tips`, `🛍️ Viral Kitchen Slicer Find`).
   - Renamed buttons to **"Extract Intelligence ➔"** and **"Intelligence Vault"**.
   - Added **Platform Superpowers showcase** (Universal Stream Parsing, Multimodal Neural Vision, Shoppable Product Links, Instant WhatsApp Dispatch) and bottom telemetry badges.
   - Enhanced dynamic result rendering to support Workout Routines, Step-by-Step Tutorials, Code Procedures, and Shoppable Products with 1-click Amazon/Flipkart buy tags.
2. **Backend Payload Resiliency (`backend/app/api/v1/extract.py`)**:
   - Added Pydantic `@model_validator(mode="before")` on `ExtractRequest` to transparently map `url` to `video_url`.

#### 4. Testing & Verification:
- Ran complete test suite (149 tests): 100% passed in 40s with zero regressions.
- Next.js production build (`npm run build`): compiled cleanly in 1.3s with zero TypeScript/lint errors.
- Pushed commits to `Dev`, `staging`, and `main` branches. Vercel automatically redeployed the updated multi-genre PWA.

---

### 🚨 ISSUE-019: Celery Background Worker Failed with `No module named 'ai_router'`
- **Date**: 2026-09-08
- **Affected Files**: `backend/app/workers/tasks.py`, `backend/app/workers/celery_app.py`, `Dockerfile`, `docker-compose.yml`

#### 1. What Happened (Symptom):
When submitting an Instagram Reel link on the live Vercel frontend (`https://universal-pro-ai.vercel.app`), the extraction failed during background processing and surfaced an error banner:
```text
No module named 'ai_router'
```

#### 2. Root Cause:
The Celery background worker process (`universalpro-worker`) and BackgroundTasks execution environment run inside the Docker container `/app`. When `tasks.py` imported `from ai_router import route_video_intelligence`, Python looked in the worker subpackage directories rather than the project root directory. `PYTHONPATH=/app` was missing from the Docker container environment, and `tasks.py` / `celery_app.py` did not explicitly prepend the repository root directory to Python's `sys.path`.

#### 3. Resolution (Code Changes):
1. **Explicit Root Directory Prepending (`sys.path`)**:
   Added repository root resolution to `backend/app/workers/tasks.py` and `backend/app/workers/celery_app.py`:
   ```python
   import sys
   from pathlib import Path

   ROOT_DIR = str(Path(__file__).resolve().parent.parent.parent.parent)
   if ROOT_DIR not in sys.path:
       sys.path.insert(0, ROOT_DIR)
   ```
2. **Container `PYTHONPATH` Guarantee**:
   - Added `ENV PYTHONPATH=/app` to `Dockerfile`.
   - Added `PYTHONPATH=/app` to the `environment:` section of both `api` and `worker` services in `docker-compose.yml`.

#### 4. Testing & Verification:
- Executed full test suite (149 tests): 100% passed in 38.7s with zero regressions.
- Pulled latest commit on the Oracle Cloud production server and restarted the worker container.
- Ran live extraction verification.

---

### 🚨 ISSUE-020: `NameError: name 'Any' is not defined` in `gemini_processor.py:792` on Python 3.11
- **Date**: 2026-09-08
- **Affected Files**: `gemini_processor.py`, `backend/app/core/supabase_client.py`

#### 1. What Happened (Symptom):
During live extraction of an Instagram Reel on the production Oracle Cloud server, the background Celery task failed with:
```text
File "/app/gemini_processor.py", line 792, in <module>
    def format_downloadable_txt(meta: Dict[str, Any]) -> str:
NameError: name 'Any' is not defined
```

#### 2. Root Cause:
`gemini_processor.py` line 7 imported `from typing import Tuple, List, Dict`. When `format_downloadable_txt` used `Dict[str, Any]`, Python 3.11 evaluated the type annotation at module load time and failed with an uncaught `NameError`. In Python 3.14 (local development), type annotations were evaluated lazily, masking this error in local runs. Additionally, `tasks.py` called `supabase.save_extraction` and `supabase.increment_daily_quota`, which were named `insert_extraction` and `increment_user_quota` in `supabase_client.py`.

#### 3. Resolution (Code Changes):
1. **Added `Any` and `Optional` to `gemini_processor.py`**:
   ```python
   # Before
   from typing import Tuple, List, Dict
   
   # After
   from typing import Tuple, List, Dict, Any, Optional
   ```
2. **Added method aliases in `supabase_client.py`**:
   ```python
   def save_extraction(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
       return self.insert_extraction(payload)

   def increment_daily_quota(self, user_id: str) -> bool:
       return self.increment_user_quota(user_id)
   ```
3. **Hot-reloaded production server**:
   Hot-copied updated files via SCP and Docker CP directly into `universalpro-worker` and `universalpro-api`, then restarted the containers.

#### 4. Testing & Verification:
Submitted the exact same Instagram Reel (`https://www.instagram.com/reel/DcrYHLVyThI/`) to the live API endpoint.
- Download succeeded in 0.6s at 12.10 MiB/s.
- Gemini 3.8 Flash analyzed the video frames and audio cleanly.
- Extracted: *"Three Essential Desk Setup Upgrades"* (Product Unboxing & Finds category) with 3 full product profiles (BenQ ScreenBar, Anker Nano, KUXIU Stand), monetized Amazon (`tag=manasdas11155-21`) & Flipkart affiliate tags, and 10-minute quick commerce links.
- Verified progress transitioned to `completed` (100%) and saved in Supabase.

---

### 🚨 ISSUE-021: Instagram Reel Preview Static Fallback & Missing Structured Details/Notes in PWA UI
- **Date**: 2026-09-08
- **Affected Files**: `backend/app/workers/tasks.py`, `frontend/src/app/page.tsx`

#### 1. What Happened (Symptom):
When users extracted an Instagram Reel or YouTube Short on the Next.js PWA (`universal-pro-ai.vercel.app`):
1. **Video Preview Failed**: The Single-Docked Media Player displayed an empty black box with a play icon and "Source Stream Ingested", with no active video or embed playing.
2. **Notes Generation Blank / Generic Fallback**: The intelligence section for gadgets and reviews showed a generic placeholder: *"Method & Procedure: Follow the video clip for exact step-by-step guidance"* instead of the rich, multi-point technical specifications and review notes extracted by Gemini (e.g. 4K 144Hz / 1080p 288Hz dual mode, color accuracy, brightness, ergonomic stand, pricing).

#### 2. Root Cause:
1. **Media Player URL Gaps**:
   - `backend/app/workers/tasks.py` unlinks media files from disk upon completion to satisfy `AGENTS.md` Rule 4 (zero disk leaks). Consequently, it did not set `media_url` in `content_payload`.
   - `frontend/src/app/page.tsx` strictly required `result.media_url` and did not support native social iframe embeds for Instagram Reels (`/reel/{id}/embed/`) or YouTube Shorts (`/embed/{id}`).
2. **Missing `details` in Worker Payload & Strict Recipe Fallback**:
   - `gemini_processor.py` returned `meta["details"]` containing the complete structured specifications, but `tasks.py` omitted `"details"` from `content_payload`.
   - `frontend/src/app/page.tsx` only checked `result.instructions` and `result.details`. When both were empty, it fell back to "Method & Procedure: Follow the video clip for exact step-by-step guidance."

#### 3. Resolution (Code Changes):
1. **Added `details`, `instructions`, and `media_url` to `tasks.py`**:
   ```python
   details_text = meta.get("details", "") or ""
   parsed_instructions = []
   if details_text:
       for line in details_text.splitlines():
           line_clean = line.strip()
           if not line_clean or line_clean.startswith(('#', '=')):
               continue
           if line_clean.startswith(("- ", "* ", "• ")) or re.match(r'^\d+\.\s+', line_clean):
               clean_item = re.sub(r'^[-*•\d\.]+\s*', '', line_clean).strip()
               if clean_item:
                   parsed_instructions.append(clean_item)
           elif line_clean.startswith("**") and ":" in line_clean:
               parsed_instructions.append(line_clean)

   content_payload = {
       "title": meta.get("title", "Extracted Content"),
       "category": meta.get("category", "RECIPE"),
       "category_name": meta.get("category_name", "Content"),
       "summary": meta.get("summary", ""),
       "details": details_text,
       "instructions": parsed_instructions if parsed_instructions else meta.get("instructions", []),
       "full_text": recipe_text,
       "txt_filepath": txt_filepath,
       "products": enriched_products,
       "resources": enriched_resources,
       "timings": meta.get("timings", {}),
       "source_url": video_url,
       "media_url": video_url,
       "url_hash": url_hash
   }
   ```
2. **Added Multi-Platform Media Resolver in `frontend/src/app/page.tsx`**:
   - Supports native Instagram Reel embeds (`https://www.instagram.com/reel/{id}/embed/`).
   - Supports YouTube Shorts embed (`https://www.youtube-nocookie.com/embed/{id}`).
   - Supports direct HTML5 `<video>` for raw files.
   - Adds 1-click external link: *"▶ Open Reel in Instagram App ↗"*.
3. **Upgraded Right Column to Rich Specifications & Notes**:
   - Dynamically titles the section by domain (e.g. *"Key Features, Specifications & Review Notes"* for products/gadgets, *"Workout Routine & Form Steps"* for fitness, *"Step-by-Step Tutorial Guide"* for tech).
   - Added regex fallback `getResolvedDetails()` to retrieve notes from `full_text` for existing database cache records.
   - Parses bold labels (`**Display Size & Panel:**`) into cyan-highlighted structured cards.
   - Added 1-click *"📋 Copy Notes"* action button.

#### 4. Testing & Verification:
- Built frontend production bundle: compiled 100% cleanly in 1054ms.
- Executed full test suite: 150/150 tests passed with 0 failures.

---

### 🚨 ISSUE-022: Vercel Preview Staging Protection `401 Unauthorized` & Client Loading Lock
- **Date**: 2026-09-13
- **Affected Components**: Vercel Preview Deployments, QA E2E Crawlers, `AGENTS.md`
- **Environment**: Layer 2 Staging (`staging` branch on Vercel)

#### 1. What Happened (Symptom):
When launching browser QA agents or visual testing crawlers against the Vercel Preview URL with `?x-vercel-protection-bypass=<secret>`, the initial page HTML loaded, but the UI froze indefinitely on the loading screen: `"Loading Universal Pro AI..."`. Subsequent client-side JS chunk fetches and API calls returned `401 Unauthorized`.

#### 2. Root Cause:
Passing `?x-vercel-protection-bypass=<secret>` only bypasses Vercel Edge protection for the single initial document request. Subsequent client-side `fetch` calls, dynamic JS chunks, or media assets lack the query parameter and are blocked by Vercel Edge unless an explicit session cookie is set.

#### 3. Resolution (Code & Architecture Rules):
1. **Cookie Flag Integration**: Added `x-vercel-set-bypass-cookie=samesitenone` to all QA browser subagent tasks and E2E test navigation URLs:
   ```text
   https://universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app/?x-vercel-protection-bypass=<secret>&x-vercel-set-bypass-cookie=samesitenone
   ```
2. **Repository Governance Rule**: Codified the protocol in [`AGENTS.md`](file:///d:/Personal%20Projects/recipe-extractor/AGENTS.md#L17) and [`.agents/rules/vercel_staging_protection.md`](file:///d:/Personal%20Projects/recipe-extractor/.agents/rules/vercel_staging_protection.md).

#### 4. Testing & Verification:
- Verified on live Vercel Preview URL with `browser_subagent`: 100% of JS chunks and API calls loaded cleanly; React mounted and executed full extraction flows without errors.

---

### 🚨 ISSUE-023: YouTube Shorts Cloud IP Bot Block (`403 Forbidden` / `GVS PO Token required`)
- **Date**: 2026-09-13
- **Affected Files**: `backend/app/workers/media_downloader.py`, `downloader.py`
- **Environment**: Cloud Serverless Environments (Vercel Lambda & OCI Containers)

#### 1. What Happened (Symptom):
When attempting to extract YouTube Shorts URLs (such as `https://www.youtube.com/shorts/J---aiyznGQ`) from cloud datacenter IPs, `yt-dlp` failed with bot detection errors:
`Media download failed: Download failed: ERROR: [youtube] J---aiyznGQ: Sign in to confirm you're not a bot...`

#### 2. Root Cause:
Two underlying factors caused the failure:
1. **Regex Rigid Length Cap (`[\w-]{11}`)**: The fallback regex `r"(?:shorts/|v=|be/)([\w-]{11})"` strictly enforced 11 characters. Shorts URLs containing triple hyphens or non-standard lengths failed regex matching (`re.search` returned `None`), causing `download_youtube_fallback` to exit prematurely.
2. **Sequential Client Retry Delay**: `yt-dlp` wasted 15–20 seconds cycling through 4 player client combinations (`android`, `ios`, `tv`, `web`) that all failed with bot challenges before ever reaching the fallback logic.

#### 3. Resolution (Code Changes):
1. **Flexible Regex & Query String Cleaner**:
   Updated regex to `r"(?:shorts/|shorts|v=|be/|watch\?v=)(?:/)?([A-Za-z0-9_-]{6,15})"` and added string cleaning `match.group(1).split("?")[0].split("&")[0]` across [`backend/app/workers/media_downloader.py`](file:///d:/Personal%20Projects/recipe-extractor/backend/app/workers/media_downloader.py) and [`downloader.py`](file:///d:/Personal%20Projects/recipe-extractor/downloader.py).
2. **Instant Bot Intercept**:
   Added an immediate error pattern scanner `if any(k in err_str for k in ["bot", "sign in", "po token", "403", "confirm"])` inside the `yt-dlp` exception loop to execute `download_youtube_fallback()` on the very first bot challenge without delay.
3. **5-Tier Quality Cascade**:
   Cascades `[oembed_thumb, maxresdefault.jpg, sddefault.jpg, hqdefault.jpg, mqdefault.jpg, default.jpg]` to guarantee high-resolution stream thumbnail retrieval for Gemini Multimodal Vision API inference.

#### 4. Testing & Verification:
- Ran Python verification script on all sample YouTube Shorts: `J---aiyznGQ` (Keyboard Cat), `KrFDs2M_FSE` (Python Tips), `fC7oUOUEEi4` (Stick Bug) all returned HTTP 200 with complete oEmbed metadata and thumbnail images.
- Unit test suite: `150/150 passed` (0 failures).

---

### 🚨 ISSUE-024: Global Skill Installation & Luxury Next.js Design Architecture Integration
- **Date**: 2026-09-13
- **Affected Files**: `frontend/src/app/globals.css`, `frontend/src/app/page.tsx`, `frontend/src/components/ParticleBackground.tsx`, `C:\Users\admin\.gemini\config\skills\`
- **Environment**: Global Agent System & Next.js 15 Client

#### 1. What Happened (Symptom):
1. User requested installing 14 downloaded skills from `C:\Users\admin\Downloads\Skill Files` globally across the AI agent workspace.
2. The web application's typography and background aesthetics were perceived as generic / AI-generated without modern interactive micro-animations or custom visual brand tokens.

#### 2. Root Cause:
1. Skills residing only in `Downloads` were not automatically discovered by Antigravity AI; global skills must be located in `C:\Users\admin\.gemini\config\skills\<skill_name>\SKILL.md`.
2. Standard browser defaults (`Inter` or sans-serif fallbacks) lacks visual personality compared to luxury Awwwards-style web applications.
3. Adding interactive HTML5 canvas animation without clean-up handlers causes memory leaks or high DPI blurry rendering on Retina displays.

#### 3. Resolution (Code & Architecture Changes):
1. **Global Skill Installer (`scratch/install_skills.py`)**:
   Wrote an automated installer script that parsed YAML frontmatter across all 14 downloaded skills and installed them into `C:\Users\admin\.gemini\config\skills\`:
   `find-skills`, `frontend-design`, `high-end-visual-design`, `loop-me`, `handoff`, `prototype`, `research`, `shadcn`, `tailwind-design-system`, `theme-factory`, `to-issues`, `to-prd`, `triage`, `wayfinder`.
2. **Typography System Upgrade (`globals.css`)**:
   Imported Google Fonts:
   - `Plus Jakarta Sans`: Primary display headers and titles.
   - `Space Grotesk`: Domain category badges and status pills.
   - `JetBrains Mono`: Execution latency telemetry and code blocks.
3. **Interactive Particle Canvas (`ParticleBackground.tsx`)**:
   Created a lightweight canvas component using `requestAnimationFrame`, mouse radial tracking, distance-based line opacity calculations, and `window.devicePixelRatio` scaling.
4. **Visual Layer Composition (`page.tsx`)**:
   Combined dynamic canvas constellation layer (`<ParticleBackground />`) with ambient aurora backgrounds (`hero_neural_bg.jpg`) and 3D glass crystal artwork (`hero_glass_artwork.jpg`).

#### 4. Testing & Verification:
- Next.js production build: compiled 100% cleanly in 1211ms.
- E2E visual verification on Vercel Preview Staging.
- Unit test suite: `150/150 passed` (0 failures).

---

### 🚨 ISSUE-025: Default Light Mode & Interactive Sun/Moon Dark Mode Toggle
- **Date**: 2026-09-13
- **Affected Files**: `frontend/src/app/globals.css`, `frontend/src/app/page.tsx`, `frontend/src/components/ParticleBackground.tsx`, `frontend/src/components/FaqSection.tsx`
- **Environment**: Client UI & Browser Theme Engine

#### 1. What Happened (Symptom):
User requested defaulting the website theme to Light Mode while providing a prominent, interactive Sun/Moon button in the sticky top navigation bar to toggle Dark Cyber-Obsidian Mode.

#### 2. Root Cause:
1. CSS variables in `:root` were hardcoded to dark obsidian colors (`#040711`), offering no light mode styling or variables.
2. Canvas background (`ParticleBackground.tsx`) used fixed bright cyan/emerald particles that washed out on white background backdrops without theme color scaling.

#### 3. Resolution (Code Changes):
1. **CSS Dual-Theme Tokens (`globals.css`)**:
   - `:root`: Light mode base (`#F8FAFC`), white frosted glass (`rgba(255,255,255,0.88)`), slate-900 typography (`#0F172A`).
   - `html.dark, body.dark`: Obsidian base (`#040711`), dark glass (`rgba(14,20,36,0.75)`), white typography (`#F8FAFC`).
2. **Interactive Header Toggle (`page.tsx`)**:
   - Integrated `<Sun />` / `<Moon />` icon button in sticky header bar.
   - Synchronizes `localStorage.getItem('theme')` (defaulting to `'light'`) and toggles `.dark` class on `document.documentElement`.
3. **Theme-Aware Canvas (`ParticleBackground.tsx`)**:
   - Accepts `theme` prop (`'light' | 'dark'`) to switch particle dot hues and line translucency dynamically.

#### 4. Testing & Verification:
- Next.js production build: compiled 100% cleanly in 1362ms.
- Full unit test suite: `150/150 passed` (0 failures).

---

### 🚨 ISSUE-026: World-Class Ceramic Light & Obsidian Dark Dual Theme Architecture
- **Date**: 2026-09-13
- **Affected Files**: `frontend/src/app/globals.css`, `frontend/src/app/page.tsx`, `frontend/src/components/FaqSection.tsx`, `frontend/src/components/ParticleBackground.tsx`
- **Environment**: Agency-Grade Visual UI System

#### 1. What Happened (Symptom):
Initial Light Mode implementation was perceived as basic, lacking depth, card contrast, or world-class design polish across both Light and Dark modes.

#### 2. Root Cause:
1. Glass card panels (`.awwwards-card`, `.shimmer-card`) hardcoded dark background opacities and static shadows.
2. Light mode lacked ceramic frosted glass tokens, elevation shadows (`box-shadow`), accent top borders (`.accent-border-t`), or theme-aware texture blend modes (`multiply` vs `screen`).

#### 3. Resolution (Code Changes):
1. **Ceramic Light & Obsidian Dark System (`globals.css`)**:
   - Light Mode: Porcelain ceramic background (`#F8FAFC` to `#F1F5F9`), frosted white glass (`rgba(255,255,255,0.82)`), deep slate-900 typography (`#0F172A`), multi-tone gradient titles (`linear-gradient(135deg, #059669 0%, #10B981 50%, #0284C7 100%)`).
   - Dark Mode: Obsidian cyber-glass (`rgba(14,20,36,0.78)`), snow typography (`#F8FAFC`), neon cyan/emerald badges.
2. **Texture Blend Modes**:
   - `html:not(.dark) .bg-hero-texture`, `.bg-glass-artwork`: `mix-blend-mode: multiply`, `opacity: 0.12`.
3. **Component Adaptability**:
   - Domain selectors, telemetry badges, sample chips, and FAQ cards consume CSS variables (`var(--bg-surface)`, `var(--shadow-card)`, `var(--text-primary)`).

#### 4. Testing & Verification:
- Next.js production build: compiled 100% cleanly in 1440ms.
- Full unit test suite: `150/150 passed` (0 failures).

---

### 🚨 ISSUE-027: Anthropic Global Agent Skills Repository Synchronization (`github.com/anthropics/skills`)
- **Date**: 2026-09-13
- **Affected Location**: `C:\Users\admin\.gemini\config\skills\`
- **Environment**: Global Agent System & Multi-Project Capabilities

#### 1. What Happened (Symptom):
User requested the installation of all official Anthropic agent skills from `https://github.com/anthropics/skills` at the global level for cross-project utility.

#### 2. Root Cause:
Anthropic skills repo contains 19 production-grade agent skills (`academy-guide`, `algorithmic-art`, `brand-guidelines`, `canvas-design`, `claude-api`, `discernment-nudge`, `doc-coauthoring`, `docx`, `frontend-design`, `internal-comms`, `mcp-builder`, `pdf`, `pptx`, `skill-creator`, `slack-gif-creator`, `theme-factory`, `web-artifacts-builder`, `webapp-testing`, `xlsx`) requiring global registration in `C:\Users\admin\.gemini\config\skills\`.

#### 3. Resolution (Code & File Changes):
1. **Cloned Repository**: Cloned `https://github.com/anthropics/skills.git` to temporary workspace scratch folder (`scratch/anthropics_skills`).
2. **Global Sync Script**: Executed `install_anthropics_skills.py` to copy all 19 skills with their complete subfolder hierarchies (references, scripts, templates, assets) into `C:\Users\admin\.gemini\config\skills\<skill_name>\`.
3. **Verification**: Total global skills count reached 45 verified, active agent skills.

#### 4. Testing & Verification:
- Full automated test suite: `150/150 passed` (0 failures).
- All 19 skills verified present with valid `SKILL.md` entries.

---

### 🚨 ISSUE-028: Autonomous Playwright WebApp Visual & Functional E2E Audit (`webapp-testing` Skill)
- **Date**: 2026-09-13
- **Affected Target**: Staging Preview (`universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app`)
- **Environment**: Automated Playwright Headless Audit

#### 1. What Happened (Symptom):
Executed full automated Playwright webapp visual inspection & functional testing using the newly installed `webapp-testing` agent skill.

#### 2. Root Cause & Verification Findings:
1. **Light & Dark Mode Synchronization**: Theme toggle (`Dark Mode` / `Light Mode` header trigger) accurately mutates `document.documentElement.classList` to toggle `.dark`, persisting state and adjusting CSS surface tokens.
2. **Interactive Form Input & Domain Hints**: Form inputs successfully receive URLs, render platform badge ("YouTube Short"), and accept domain selection.
3. **FAQ Accordion & Knowledge Base**: Smooth accordion expansion validated without layout shifts or text overlaps.
4. **Mobile Responsiveness (375x812 Viewport)**: Verified clean single-column layout stack, sticky header compact spacing, and readable font sizing.

#### 3. Visual Artifact Proof:
- Initial Light Mode: [`webapp_test_initial_light_mode.png`](file:///C:/Users/admin/.gemini/antigravity-ide/brain/4d9e6a2e-1965-400e-81ff-bdf8142c51fa/webapp_test_initial_light_mode.png)
- Obsidian Dark Mode: [`webapp_test_dark_mode.png`](file:///C:/Users/admin/.gemini/antigravity-ide/brain/4d9e6a2e-1965-400e-81ff-bdf8142c51fa/webapp_test_dark_mode.png)
- FAQ Accordion Interaction: [`webapp_test_faq_interaction.png`](file:///C:/Users/admin/.gemini/antigravity-ide/brain/4d9e6a2e-1965-400e-81ff-bdf8142c51fa/webapp_test_faq_interaction.png)
- Mobile Responsive Viewport: [`webapp_test_mobile_viewport.png`](file:///C:/Users/admin/.gemini/antigravity-ide/brain/4d9e6a2e-1965-400e-81ff-bdf8142c51fa/webapp_test_mobile_viewport.png)

#### 4. Testing & Verification:
- 0 Console Errors, 0 Uncaught Exceptions.
- Automated pytest suite: `150/150 passed` (0 failures).

---

### 🚨 ISSUE-029: Multi-LLM Council 3-Stage Consensus Engine (`karpathy/llm-council` Adaptation)
- **Date**: 2026-09-14
- **Affected Subsystem**: `ai_router.py`, `backend/app/services/llm_council.py`, `app.py`
- **Environment**: Dev & Staging

#### 1. What Happened (Symptom):
Need for maximum extraction accuracy, peer audit cross-verification, and missing-ingredient detection on complex cooking reels and audio transcripts without sacrificing sub-3s fast execution defaults.

#### 2. Root Cause & Solution:
Integrated Andrey Karpathy's 3-Stage LLM Council Consensus framework into Universal Pro AI:
- **Stage 1 (Parallel First Opinions)**: Dispatches video/audio concurrently to Gemini 3.8 Flash, Groq (Whisper + Llama 3.3 70B), and Mistral AI using `ThreadPoolExecutor`.
- **Stage 2 (Anonymized Peer Audit)**: Masks provider identities into `Model Alpha`, `Model Beta`, `Model Gamma` and runs peer-audit verification to highlight missing ingredients or measurement discrepancies.
- **Stage 3 (Chairman JSON Synthesis)**: Chairman model consolidates verified findings into a single unified `RecipeSchema` output dictionary.

#### 3. Code Changes:
- Created [`backend/app/services/llm_council.py`](file:///d:/Personal%20Projects/recipe-extractor/backend/app/services/llm_council.py)
- Updated [`ai_router.py`](file:///d:/Personal%20Projects/recipe-extractor/ai_router.py)
- Updated [`backend/app/workers/tasks.py`](file:///d:/Personal%20Projects/recipe-extractor/backend/app/workers/tasks.py)
- Updated [`app.py`](file:///d:/Personal%20Projects/recipe-extractor/app.py)
- Added dedicated test suite [`tests/test_sprint8_llm_council.py`](file:///d:/Personal%20Projects/recipe-extractor/tests/test_sprint8_llm_council.py)

#### 4. Testing & Verification:
- Full automated test suite: `155/155 passed` (0 failures).

---

### 🚨 ISSUE-030: Light Mode Contrast Deficits & Hero Artwork Bounding Edges (P0/P1 PO Review Directive)
- **Date**: 2026-09-14
- **Affected Files**: `frontend/src/app/globals.css`, `frontend/src/app/page.tsx`, `frontend/src/components/FaqSection.tsx`, `app.py`
- **Environment**: Dev & Staging

#### 1. What Happened (Symptom):
Product Owner visual inspection revealed three P0/P1 visual flaws in Light Mode:
1. Floating 3D crystal artwork (`hero_glass_artwork.jpg`) rendered with a square dark bounding box breaking hero symmetry.
2. Light mode headline and subheadings suffered from low WCAG AA contrast ratio (< 3:1).
3. Hero input card was cluttered by a full-width top domain selector bar pushing the URL input downward.

#### 2. Root Cause & Resolution:
1. **Feathered Radial Mask for 3D Artwork**: Added CSS `mask-image: radial-gradient(circle at center, rgba(0,0,0,1) 20%, rgba(0,0,0,0) 75%)` and `mix-blend-mode: multiply` in light mode to blend artwork seamlessly.
2. **Light Mode WCAG AA Contrast**:
   - Set Light Mode headline color to `#0F172A` Slate-900 with emerald-cyan gradient on `"Intelligence Extractor"`.
   - Darkened body/description text to `#334155` Slate-700.
   - Darkened FAQ step numbers `01-04` to high-contrast colors (`#059669`, `#0284C7`, `#D97706`, `#C026D3`).
   - Filled active category filter pill with solid `#10B981` emerald background and white bold text.
3. **Hero Input Card Streamlining**:
   - Merged domain classifier as a compact inline select chip (`⚡ Auto-Detect ▾`) inside the URL input bar.
   - Repositioned micro-badges (`~2.4s AI SLA`, `Amazon & Flipkart Links`, `1-Click WhatsApp Export`) directly under the hero headline description as a clean trust proof bar.

#### 3. Testing & Verification:
- Full automated test suite: `155/155 passed` (0 failures).

---

### 🚨 ISSUE-031: Global Agent Skills Audit & Installation from Downloads Folder
- **Date**: 2026-09-14
- **Affected Location**: `C:\Users\admin\Downloads\Skill Files` -> `C:\Users\admin\.gemini\config\skills\`
- **Environment**: Global Agent System & Customizations

#### 1. What Happened (Symptom):
User downloaded 22 skill `.md` files to `C:\Users\admin\Downloads\Skill Files\` and requested an audit and global installation of all usable missing skills.

#### 2. Root Cause & Verification Findings:
Audited all 22 downloaded skill files against existing installed skills in `C:\Users\admin\.gemini\config\skills\`. Identified 7 brand new missing skills (`design-taste-frontend`, `figma-generate-design`, `figma-use`, `impeccable`, `minimalist-ui`, `mobile-android-design`, `redesign-existing-projects`).

#### 3. Resolution (Files Installed):
Created global skill directories and installed `SKILL.md` for all 7 missing skills:
1. `design-taste-frontend`
2. `figma-generate-design`
3. `figma-use`
4. `impeccable`
5. `minimalist-ui`
6. `mobile-android-design`
7. `redesign-existing-projects`

#### 4. Testing & Verification:
- Total active global skills count reached **53 verified agent skills**.
- All 53 skills verified with valid `SKILL.md` frontmatter.

---

### 🚨 ISSUE-032: Impeccable UI/UX Contrast Ratio, Dual-Theme Artwork, Ghost-Card Removal & Motion Engine
- **Date**: 2026-09-14
- **Affected Files**: `frontend/src/app/globals.css`, `frontend/src/app/page.tsx`, `frontend/public/hero_glass_artwork_light.jpg`, `ui-ux-audits/2026-09-14-impeccable-ui-ux-audit.md`, `SPRINT_8_PO_SHOWCASE.md`
- **Environment**: Dev & Staging

#### 1. What Happened (Symptom):
UI/UX audit using the newly installed `impeccable` skill revealed a dark gray smudgy rectangular blur artifact in Light Mode caused by reusing the dark-background 3D glass artwork (`hero_glass_artwork.jpg`) with `mix-blend-mode: multiply`. Additionally, minor contrast ratio deficits existed on dark mode subtext (`#64748B`) and light mode emerald badges (`#059669`), along with a "ghost-card" visual tell on `.glass-panel` (pairing 1px translucent border with heavy blur shadow `≥16px`), unbalanced multi-line header breaks, and missing accessibility reduced-motion fallbacks.

#### 2. Root Cause & Solution:
1. **Dual-Theme Background Artwork & Smudge Removal**:
   - Identified that dark texture images (`hero_ambient_glow.jpg`, `hero_neural_bg.jpg`, `hero_glass_artwork.jpg`) were causing gray clouds and dark smudges over the Light Mode hero section.
   - Updated [`globals.css`](file:///d:/Personal%20Projects/recipe-extractor/frontend/src/app/globals.css) to suppress dark texture images in Light Mode (`display: none !important`) and substituted a pure CSS radiant emerald-cyan aura (`radial-gradient(circle at 50% -10%, rgba(16, 185, 129, 0.14) 0%, rgba(6, 182, 212, 0.07) 45%, transparent 75%)`), achieving a 100% smudge-free Ceramic Light interface.
2. **WCAG 2.1 AA Contrast Ratio**:
   - Updated dark mode `--text-muted` from `#64748B` to `#94A3B8` (>7.2:1 contrast ratio).
   - Updated light mode `.badge-emerald` text from `#059669` to `#047857` (>5.1:1 contrast ratio).
3. **Ghost-Card Removal & Surface Separation**:
   - Decoupled heavy shadow blur (`0 20px 40px -15px ...`) from `.glass-panel` and replaced with a clean elevation shadow (`0 4px 16px rgba(...)`).
   - Removed inline heavy shadow override on hero URL input card in `page.tsx`.
4. **Typography Line Balancing**:
   - Added global `h1, h2, h3 { text-wrap: balance; }` and `p { text-wrap: pretty; }`.
5. **Accessibility Motion Engine**:
   - Added `@media (prefers-reduced-motion: reduce)` block disabling animations, transform shifts, and parallax for users requesting reduced motion.
6. **Audit Persistence & Sprint Showcase Documents**:
   - Created dedicated `ui-ux-audits/` repository folder and saved the full audit report into [`ui-ux-audits/2026-09-14-impeccable-ui-ux-audit.md`](file:///d:/Personal%20Projects/recipe-extractor/ui-ux-audits/2026-09-14-impeccable-ui-ux-audit.md).
   - Created [`SPRINT_8_PO_SHOWCASE.md`](file:///d:/Personal%20Projects/recipe-extractor/SPRINT_8_PO_SHOWCASE.md) following repository governance standards.

#### 3. Testing & Verification:
- Automated test suite: `156/156 passed` (0 failures).
- Pre-promotion gate verified clean build and promoted `Dev -> staging`.

---

### 🚨 ISSUE-033: Friends & Family Beta Rollout, Hinglish Regional Prompt & Telemetry Engine
- **Date**: 2026-09-14
- **Affected Files**: `backend/app/services/quota_service.py`, `database/009_beta_telemetry_feed.sql`, `backend/app/services/telemetry_service.py`, `whatsapp_service.py`, `gemini_processor.py`, `scripts/run_telegram_bot.py`, `frontend/src/components/CopyShoppingChecklist.tsx`, `frontend/src/app/page.tsx`, `tests/test_sprint9_beta_telemetry.py`
- **Environment**: Dev & Staging

#### 1. What Happened (Symptom):
Preparing for the 5-phase 48-hour Friends & Family Beta rollout required relaxing extraction limits to prevent HTTP 429 paywalls during co-testing, provisioning a passive telemetry table, setting up real-time Telegram admin alerts for failures or negative feedback, tuning Gemini 3.8 Flash for Indian regional Hinglish metrics (*katori*, *chamach*, *Ghee*, *Kasuri Methi*), adding inline Telegram feedback buttons, and providing a Safari-resilient clipboard component.

#### 2. Root Cause & Resolution:
1. **Beta Quota Overrides**: Updated `GUEST_DAILY_LIMIT = 20` and `FREE_AUTH_DAILY_LIMIT = 30` in `backend/app/services/quota_service.py`.
2. **Supabase Telemetry Migration**: Created `database/009_beta_telemetry_feed.sql` defining `beta_telemetry_feed` table, index, and RLS policies.
3. **Telegram Admin Alerts**: Created `backend/app/services/telemetry_service.py` dispatching instant Markdown alerts to developer private chat on failures (`🚨 FAILURE` / `⚠️ NEGATIVE FEEDBACK`).
4. **WhatsApp Outbound Formatter**: Implemented `format_whatsapp_recipe` in `whatsapp_service.py` returning compact ingredient lists, top 4 prep steps, and 10-minute Blinkit/Zepto delivery links.
5. **Hinglish Prompt Tuning**: Embedded `REGIONAL_EXTRACTION_SYSTEM_PROMPT` into `gemini_processor.py` for colloquial metric conversions.
6. **Telegram Inline Feedback Keyboards**: Added `get_feedback_keyboard` and `get_detail_failure_keyboard` to `scripts/run_telegram_bot.py`.
7. **Safari & WebView Clipboard Component**: Built `frontend/src/components/CopyShoppingChecklist.tsx` featuring `navigator.clipboard` with an automatic `execCommand('copy')` fallback textarea.
8. **Dual-Bot Hero Callouts**: Added Telegram and WhatsApp mobile chat pill links below hero sample chips in `frontend/src/app/page.tsx`.

#### 3. Testing & Verification:
- Created dedicated test suite `tests/test_sprint9_beta_telemetry.py` (157 tests total).
- All 157 automated unit & integration tests passed with 0 failures.

---

### 🚨 ISSUE-023: Instagram Reel Empty Media Response & Video Format Errors
- **Date**: 2026-09-15
- **Affected Files**: `downloader.py`, `backend/app/workers/media_downloader.py`

#### 1. What Happened (Symptom):
During beta testing, downloading certain Instagram reels threw raw `yt-dlp` tracebacks: `ERROR: [Instagram] DR92ta_EkO2: Instagram sent an empty media response. Check if this post is accessible in your browser without being logged-in...` or `ERROR: [Instagram] DdRYstgJwgl: No video formats found!`.

#### 2. Root Cause:
Instagram regularly applies rate limits or requires browser user agent impersonation when retrieving reels from cloud datacenter IP ranges. `yt-dlp` format extraction failed when raw video streams were blocked, throwing unhandled exceptions.

#### 3. Resolution (Code Changes):
1. **Instagram oEmbed Snapshot Downloader (`download_instagram_fallback`)**: Added fallback keyframe snapshot retriever in `downloader.py` using official Instagram oEmbed metadata (`/oembed/`) and direct media endpoints (`/media/?size=l`).
2. **Error Message Sanitization (`sanitize_download_error`)**: Stripped raw `yt-dlp` stack traces and replaced them with user-friendly actionable status messages.

#### 4. Testing & Verification:
Verified with unit tests in `tests/test_sprint10_beta_feedback.py` (`test_downloader_error_sanitization` & `test_instagram_fallback_regex`).

---

### 🚨 ISSUE-024: Intelligence Vault Not Persisting Saved Extractions or Missing Save Action Button
- **Date**: 2026-09-15
- **Affected Files**: `frontend/src/app/page.tsx`, `frontend/src/components/VaultLibrary.tsx`

#### 1. What Happened (Symptom):
Beta users reported that completed extractions were not showing up in the Intelligence Vault, nor was there a clear option on result cards to save recipes to the Vault.

#### 2. Root Cause:
`handleExtract` in `page.tsx` saved extracted payloads only in ephemeral component state (`setResult`) without writing to `localStorage` or triggering Vault persistence. Additionally, result cards lacked a `[ 💾 Save to Vault ]` bookmark button.

#### 3. Resolution (Code Changes):
1. **Auto-Save on Completion**: Added `localStorage.setItem('upa_vault_items', ...)` auto-save execution inside `handleExtract` in `page.tsx`.
2. **Result Header Action Button**: Added `[ 💾 Save to Vault ]` / `[ ✅ Saved in Vault ]` button to extraction result card headers with `toggleSaveToVault` handler.
3. **Hybrid Storage Sync**: Updated `VaultLibrary.tsx` to merge items from `localStorage` (`upa_vault_items`) and backend `/api/v1/library`, ensuring offline and online reliability.

#### 4. Testing & Verification:
Verified with unit tests in `tests/test_sprint10_beta_feedback.py` (`test_vault_auto_save_payload_schema`).

---

### 🚨 ISSUE-025: Search Bar Button Cut Off on Mobile & FAQ Page Clutter
- **Date**: 2026-09-15
- **Affected Files**: `frontend/src/app/page.tsx`, `frontend/src/app/globals.css`, `frontend/src/components/FaqSection.tsx`

#### 1. What Happened (Symptom):
1. On mobile viewports (<640px), the "Extract Intelligence ->" button was cut off horizontally due to a non-responsive inline flex container without flex-wrap.
2. The homepage rendered a large static FAQ section by default, causing vertical scroll clutter.

#### 2. Root Cause & Resolution:
1. **Responsive Mobile CSS (`globals.css`)**: Added `.main-search-input-container` with `@media (max-width: 640px)` rule forcing vertical column stacking, full 100% width, 16px font-size to prevent iOS Safari auto-zoom, and 48px touch targets.
2. **Header FAQ Modal (`page.tsx` & `FaqSection.tsx`)**: Completely removed `<FaqSection />` from the default home page flow. Added `isFaqModalOpen` state. Clicking top navigation "FAQ & Guide" button opens `<FaqSection />` in a clean modal overlay drawer.

#### 3. Testing & Verification:
Tested with Playwright / Chrome DevTools mobile viewports (<640px) and verified zero horizontal overflow.

---

### 🚨 ISSUE-032: Minimalist UI Overhaul, Interior/Gaming Categories, Deprecated Model Pruning & E2E Validation
- **Date**: 2026-09-15
- **Affected Files**: `frontend/src/app/page.tsx`, `gemini_processor.py`, `frontend/src/app/api/v1/webhooks/whatsapp/route.ts`, `frontend/src/app/api/v1/webhooks/telegram/route.ts`

#### 1. What Happened (Symptom):
1. PO Feedback annotated screenshot highlighted non-minimal UI clutter: top SLA badge, upper telemetry badges, non-functional chat bot callout bar, Platform Superpowers section, and bottom telemetry badges.
2. App needed auto-detection and prompt guidance for Interior Design (`INTERIOR_DESIGN` / 🏠) and Gaming Settings (`GAMING` / 🎮) categories.
3. Fallback Gemini candidate list contained deprecated 404 endpoints (`gemini-3.1-pro`, `gemini-3-flash`, `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-2.5-flash-lite`), causing ~20s latency spikes on congested requests.

#### 2. Root Cause & Resolution:
1. **Ultra-Minimalist UI Overhaul (`page.tsx`)**: Removed top SLA badge, upper/lower telemetry pills, bot callout bar, and Platform Superpowers grid. Streamlined hero subtitle to single line: `"Instant AI extraction for recipes, travel, gadgets, interior, gaming & shorts."`
2. **Category System Expansion (`gemini_processor.py` & `page.tsx`)**:
   - Added `INTERIOR_DESIGN` (🏠) and `GAMING` (🎮) to `CATEGORY_EMOJIS`, `CATEGORY_NAMES`, `DOMAIN_OPTIONS`, `getSectionTitle`, auto-detect prompts, and category parsers.
3. **Deprecated Model Pruning (`gemini_processor.py`, webhook routes)**:
   - Enforced **AGENTS.md Rule 8** by pruning non-existent 404 endpoints from `preferred_candidates` array in `gemini_processor.py`.
   - Updated WhatsApp and Telegram webhook routes to use `gemini-3.8-flash`.

#### 3. Testing & Verification:
- **Unit Tests**: Full suite passed 100% green (**168 / 168 tests passed**).
- **E2E Video Test**: Verified 6 user-provided video links across Cooking, Travel (9 Google Maps links parsed!), Interior, Gaming Settings, and Gadget Shorts.

---

### 🚨 ISSUE-033: Dynamic Travel Itinerary Day-by-Day Activity & Google Maps Link Formatting
- **Date**: 2026-09-15
- **Affected Files**: `gemini_processor.py`, `frontend/src/app/page.tsx`, `tests/test_sprint10_travel_formatting.py`

#### 1. What Happened (Symptom):
Product Owner annotated screenshot requested a dedicated, dynamic Travel Itinerary format breaking down travel reels by Days (`Day 1:`, `Day 2:`) and Activities (`Activity 1:`, `Activity 2:`) with 1-click Google Maps location links for every place.

#### 2. Root Cause & Resolution:
1. **Gemini Processor (`gemini_processor.py`)**: Updated `TRAVEL_GUIDE` category prompt to enforce `Day N:` -> `- Activity M: <Description> | LOCATION: <Place> | SEARCH: <Query>` output structure. Enhanced `parse_extracted_content` to build structured `travel_itinerary` JSON array with `day` and `activities` objects. Updated `format_downloadable_txt` to format day-by-day activities and Google Maps links.
2. **Frontend UI & Text Export (`page.tsx`)**:
   - Added `travel_itinerary` to `ExtractionResult` interface.
   - Built `parseTravelItinerary` helper function for robust day and activity parsing.
   - Updated `generateStructuredText` to format WhatsApp and downloadable `.txt` files with `Activity 1:`, `Activity 2:` and Google Maps search URLs.
   - Built dedicated Travel Itinerary UI card component rendering styled day cards (`📍 Day 1`), activity badges (`Activity 1`), descriptions, and 1-click `📍 Open in Google Maps` buttons.
3. **Unit Testing (`tests/test_sprint10_travel_formatting.py`)**: Created dedicated test suite validating travel itinerary day extraction, activity parsing, location search query construction, and `.txt` formatting (**169 / 169 tests passed**).

#### 3. Testing & Verification:
- Next.js local build (`npm run build`): Passed cleanly (**0 errors**).
- Pytest unit test suite: **169 / 169 PASSED**.

| **ISSUE-034** | 2026-09-15 | Monetization | Enforce Owner Immutable Affiliate Tag Shield & Removal of Creator Tag Overrides | ✅ Resolved |
| **ISSUE-035** | 2026-09-18 | Architecture & Null-Safety | SAFE-1101: TypeScript Schema Null-Safety & Historical Cache Protection | ✅ Resolved |
| **ISSUE-036** | 2026-09-18 | Core UX Infrastructure | SAFE-1102: Screen Wake-Lock Defensive Hook & Auto-Reacquire | ✅ Resolved |
| **ISSUE-037** | 2026-09-18 | Core Utility Engine | SAFE-1103: Mobile Timer Delta Math & Web Audio Pre-Unlock | ✅ Resolved |
| **ISSUE-038** | 2026-09-18 | State Architecture | SAFE-1104: Centralized Recipe & Pantry Context Store | ✅ Resolved |
| **ISSUE-039** | 2026-09-18 | Parsing Algorithm | SAFE-1105: Deterministic Regex Duration Tokenizer Sandbox | ✅ Resolved |

---

### 🚨 ISSUE-039: `SAFE-1105`: Deterministic Regex Duration Tokenizer Sandbox
- **Date**: 2026-09-18
- **Affected Files**: `frontend/src/utils/durationParser.ts`, `tests/test_sprint11_safety.py`

#### 1. What Happened (Symptom):
Converting instruction time strings (e.g. `"simmer for 15-20 mins"`, `"bake for 1 hr 30 min"`) into countdown timers previously relied on secondary LLM API round-trips, introducing 1.5s+ latency and additional inference costs.

#### 2. Root Cause & Resolution:
1. **Regex Tokenizer (`frontend/src/utils/durationParser.ts`)**: Built `parseInstructionDurations` tokenizer scanning single values, hyphenated/word ranges (taking upper/max bound), and compound durations (`"1 hr 30 mins"`) into structured seconds intervals in 0ms without network calls.

#### 3. Testing & Verification:
- Pytest test suite (`tests/test_sprint11_safety.py`): **176 / 176 PASSED**.

---

### 🚨 ISSUE-038: `SAFE-1104`: Centralized Recipe & Pantry Context Store
- **Date**: 2026-09-18
- **Affected Files**: `frontend/src/context/RecipeContext.tsx`, `tests/test_sprint11_safety.py`

#### 1. What Happened (Symptom):
Serving size scaling, ingredient checking, and pantry exclusions were managed independently in disconnected UI components, leading to desynchronization between clipboard exports, UI displays, and e-commerce affiliate cart parameters.

#### 2. Root Cause & Resolution:
1. **Context Store (`frontend/src/context/RecipeContext.tsx`)**: Created `RecipeProvider` and `useRecipeContext` hook managing `servingsMultiplier` ($1 \le n \le 12$), `checkedIngredientIds: Set<string>`, and `excludedPantryIds: Set<string>`.
2. **Pantry Exclusion Selector**: Implemented `getFilteredIngredients()` selector and `excludeDefaultPantryBasics()` helper to instantly filter staple ingredients across all views.

#### 3. Testing & Verification:
- Pytest test suite (`tests/test_sprint11_safety.py`): **175 / 175 PASSED**.

---

### 🚨 ISSUE-037: `SAFE-1103`: Mobile Timer Delta Math & Web Audio Pre-Unlock
- **Date**: 2026-09-18
- **Affected Files**: `frontend/src/hooks/useStepTimer.ts`, `tests/test_sprint11_safety.py`

#### 1. What Happened (Symptom):
Standard `setInterval` counter decrements suffered severe timer drift when mobile browser tabs were throttled in the background. Furthermore, mobile browsers blocked completion chimes played programmatically without prior gesture pre-unlock.

#### 2. Root Cause & Resolution:
1. **Delta Math (`frontend/src/hooks/useStepTimer.ts`)**: Built `useStepTimer` hook using target epoch timestamp deltas (`targetEndTime - Date.now()`), instantly recalculating accurate remaining time upon tab focus restoration.
2. **Audio & Haptics Pre-Unlock**: Added `unlockAudio` callback pre-unlocking a silent 1ms Web Audio `AudioContext` buffer on user gestures, enabling A5 (880Hz) sine tone completion chimes and `navigator.vibrate([200, 100, 200])`.

#### 3. Testing & Verification:
- Pytest test suite (`tests/test_sprint11_safety.py`): **174 / 174 PASSED**.

---

### 🚨 ISSUE-036: `SAFE-1102`: Screen Wake-Lock Defensive Hook & Auto-Reacquire
- **Date**: 2026-09-18
- **Affected Files**: `frontend/src/hooks/useWakeLock.ts`, `tests/test_sprint11_safety.py`

#### 1. What Happened (Symptom):
In mobile webviews, in-app browsers, or iOS WKWebView, calling `navigator.wakeLock.request('screen')` directly threw uncaught `NotAllowedError` exceptions or lost the wake lock sentinel permanently when users switched apps or tab visibility changed.

#### 2. Root Cause & Resolution:
1. **Defensive Hook (`frontend/src/hooks/useWakeLock.ts`)**: Built `useWakeLock` hook with safe feature detection (`'wakeLock' in navigator`), `try...catch` wrapper for `NotAllowedError`, and an unmount release sentinel cleanup.
2. **Auto-Reacquire Listener**: Added a `visibilitychange` event listener that automatically re-acquires the screen lock when `document.visibilityState === 'visible'`.

#### 3. Testing & Verification:
- Pytest test suite (`tests/test_sprint11_safety.py`): **173 / 173 PASSED**.

### 🚨 ISSUE-035: `SAFE-1101`: TypeScript Schema Null-Safety & Historical Cache Protection
- **Date**: 2026-09-18
- **Affected Files**: `frontend/src/types/recipe.ts`, `frontend/src/app/page.tsx`, `tests/test_sprint11_safety.py`

#### 1. What Happened (Symptom):
Historical extractions cached in Supabase prior to Sprint 11 did not contain the new `nutrition` property. Reading properties from undefined objects caused potential runtime `TypeError: Cannot read properties of undefined` crashes in Next.js client views.

#### 2. Root Cause & Resolution:
1. **Centralized Types (`frontend/src/types/recipe.ts`)**: Created `NutritionInfo` interface with strictly optional metrics (`calories?`, `protein_g?`, `carbs_g?`, `fat_g?`, `is_estimated?`). Updated `ExtractionResult` and `RecipeSchema` to make `nutrition?: NutritionInfo` optional.
2. **Page Imports (`frontend/src/app/page.tsx`)**: Replaced inline interface definitions with centralized imports from `../types/recipe`.

#### 3. Testing & Verification:
- Pytest test suite (`tests/test_sprint11_safety.py`): **172 / 172 PASSED**.

### 🚨 ISSUE-038: `SAFE-1106`: Omnichannel Cooking Deep-Link Routing
- **Date**: 2026-09-18
- **Affected Files**: `backend/app/services/whatsapp_service.py`, `backend/app/services/telegram_bot.py`, `scripts/run_telegram_bot.py`, `frontend/src/app/page.tsx`, `tests/test_sprint11_safety.py`

#### 1. What Happened (Symptom):
Outbound WhatsApp message templates and Telegram bot inline keyboards lacked deep-link routing parameter `?mode=cook`. Users opening outbound links landed at the top hero section of the web application instead of being auto-focused on step-by-step cooking instructions.

#### 2. Root Cause & Resolution:
1. **WhatsApp & Telegram Outbound Formatting (`whatsapp_service.py`, `telegram_bot.py`, `run_telegram_bot.py`)**: Added `?mode=cook` query parameter to outbound web application URLs and added `🧑‍🍳 Start Cooking Mode` inline keyboard button.
2. **Next.js Deep-Link Listener (`frontend/src/app/page.tsx`)**: Added `id="cooking-mode-section"` to Section III instructions container and updated `searchParams` listener hook to auto-scroll into view when `mode === 'cook'`.

#### 3. Testing & Verification:
- Pytest test suite (`tests/test_sprint11_safety.py`): **177 / 177 PASSED**.

### 🚨 ISSUE-039: Sprint 12: Fullscreen Interactive Hands-Free Cooking Mode
- **Date**: 2026-09-18
- **Affected Files**: `frontend/src/components/CookingModeDrawer.tsx`, `frontend/src/app/page.tsx`, `tests/test_sprint12_cooking.py`

#### 1. What Happened (Symptom):
Cooking instructions were presented as a flat static list, forcing users to manually interact with their mobile screens while cooking (leading to dirty screen touches, display timeouts, and loss of current step location).

#### 2. Root Cause & Resolution:
1. **Cooking Mode Component (`frontend/src/components/CookingModeDrawer.tsx`)**: Created fullscreen glassmorphic drawer UI featuring high-contrast step text, step progress track, and slide-over ingredients checklist.
2. **Wake Lock & Timer Integration**: Automatically activates `useWakeLock` hook to keep screen awake during cooking, and embeds interactive `useStepTimer` cards for detected duration phrases.
3. **Voice Navigation & Touch Gestures**: Integrated Web Speech API fallback for hands-free voice commands ("next", "back", "timer", "stop") and touch swipe gesture navigation.

#### 3. Testing & Verification:
- Pytest test suite (`tests/test_sprint12_cooking.py`): **184 / 184 PASSED**.

### 🚨 ISSUE-040: Sprint 13: Dynamic Smart Recipe Scaling Engine
- **Date**: 2026-09-18
- **Affected Files**: `frontend/src/utils/scalingEngine.ts`, `frontend/src/components/ServingAdjuster.tsx`, `tests/test_sprint13_scaling.py`

#### 1. What Happened (Symptom):
Adjusting recipe yield servings previously performed naive string splitting without handling complex fractions (`1 1/2`, `3/4`), ranges (`2-3`), or regional parenthetical unit notes (`1 katori (~150g)`), violating AGENTS.md Rule 13.

#### 2. Root Cause & Resolution:
1. **Scaling Engine Utility (`frontend/src/utils/scalingEngine.ts`)**: Created standalone scaling engine providing `parseQuantity`, `formatQuantity`, and `scaleIngredientItem`.
2. **Rule 13 Native Term Protection**: Implemented parenthetical metric scaling (e.g. `1 katori (~150g)` scaled 2x $\rightarrow$ `2 katori (~300g)`) while preserving regional spice terms.
3. **Pantry Exclusion & Context Store (`ServingAdjuster.tsx`)**: Bound `RecipeContext` for `servingsMultiplier` and `excludedPantryIds` filtering.

#### 3. Testing & Verification:
- Pytest test suite (`tests/test_sprint13_scaling.py`): **187 / 187 PASSED**.

### 🚨 ISSUE-041: Sprint 14: Automated Grocery Cart Integration & Quick Commerce Deep Links
- **Date**: 2026-09-18
- **Affected Files**: `backend/app/services/affiliate_engine.py`, `frontend/src/components/ServingAdjuster.tsx`, `tests/test_sprint14_commerce.py`

#### 1. What Happened (Symptom):
Outbound quick-commerce links for Blinkit, Zepto, Swiggy Instamart, and JioMart required strict URL encoding validation and domain-level category suppression to prevent irrelevant store links from appearing on non-food extractions.

#### 2. Root Cause & Resolution:
1. **Affiliate Engine Quick Commerce (`backend/app/services/affiliate_engine.py`)**: Added `generate_blinkit_url`, `generate_zepto_url`, `generate_instamart_url`, and `generate_jiomart_url` with strict `urllib.parse.quote_plus` encoding.
2. **Monetization & Shield Invariants**: Asserted immutable owner tags `tag=manasdas11155-21` and `r=5608766` across all generated product search links (AGENTS.md Rule 3).
3. **Category-Conditional Filtering**: Suppressed Blinkit/Zepto on fashion/tutorial domains and suppressed Myntra/Meesho on culinary recipe extractions.

#### 3. Testing & Verification:
- Pytest test suite (`tests/test_sprint14_commerce.py`): **191 / 191 PASSED**.

### 🚨 ISSUE-042: Telemetry Noise — Repeated Outbound Telegram Admin Alert Spam During Unit Tests
- **Date**: 2026-09-19
- **Affected Files**: `backend/app/services/telemetry_service.py`, `tests/test_sprint9_beta_telemetry.py`, `docs/TROUBLESHOOTING.md`

#### 1. What Happened (Symptom):
Developer Telegram admin chat received repeated stream of `🚨 FAILURE` (URL: `https://instagram.com/reel/123`, Detail: `Test error detail`) and `⚠️ NEGATIVE FEEDBACK` (`🧪 Verification Test Alert`) notifications without active production failures.

#### 2. Root Cause:
`send_admin_telemetry_alert` in `telemetry_service.py` was directly invoked by `test_sprint9_beta_telemetry.py` during unit test runs (`pytest` and `verify_promotion.py`). When `TELEGRAM_BOT_TOKEN` and `ADMIN_TELEGRAM_CHAT_ID` were loaded from `.env`, every test run made live outbound HTTP POST requests to `https://api.telegram.org/bot<token>/sendMessage`.

#### 3. Resolution (Code Changes):
Added an environment test guard in `backend/app/services/telemetry_service.py` to suppress real HTTP calls during test execution:
```python
# Defensive Guard: Suppress live Telegram HTTP calls during unit test runs
import sys
is_testing = (
    os.getenv("TESTING") == "true"
    or "pytest" in sys.modules
    or "unittest" in sys.modules
    or any("pytest" in arg or "unittest" in arg for arg in sys.argv)
)
if is_testing:
    logger.info(f"[Telemetry Test Guard] Suppressed live Telegram admin alert in test mode for {event_type}")
    return True
```

#### 4. Testing & Verification:
- Unit test suite run (`pytest`): **192 / 192 PASSED** with 0 outbound Telegram API alerts.

### 🚨 ISSUE-043: Travel Video Misclassification as TUTORIAL & Universal Intelligence Vault Multi-Genre Support
- **Date**: 2026-09-20
- **Affected Files**: `backend/app/services/gemini_processor.py`, `frontend/src/components/VaultLibrary.tsx`, `docs/TROUBLESHOOTING.md`

#### 1. What Happened (Symptom):
A travel Reel titled *"3-Day Varkala Travel Itinerary Guide"* was classified as `TUTORIAL` instead of `TRAVEL_GUIDE` when saved into the vault. Additionally, the Vault drawer presented hardcoded recipe-specific labels (`Personal Recipe Vault`, `0 ingredients indexed`, `Open in Chef View`) regardless of extracted video genre.

#### 2. Root Cause:
1. **Fallback Category Priority**: In `gemini_processor.py`, fallback category detection matched the keyword `"GUIDE"` under `TUTORIAL` before evaluating `"ITINERARY"` or `"TRAVEL"`. In header sample matching, `TUTORIAL` / `EDUCATIONAL` keyword checks triggered prior to checking domain titles.
2. **Hardcoded Vault Labels**: `VaultLibrary.tsx` hardcoded recipe metadata strings without domain-specific rendering logic for Travel, Fitness, Products, or Tutorials.

#### 3. Resolution (Code Changes):
1. **Category Priority & Title Guardrails (`backend/app/services/gemini_processor.py`)**: Reordered header fallback categories to evaluate `TRAVEL_GUIDE` and `WORKOUT` keywords before generic `TUTORIAL` fallbacks. Added title-based safety checks for travel (`"ITINERARY"`, `"TRAVEL GUIDE"`, `"PLACES TO VISIT"`) and fitness keywords.
2. **Universal Intelligence Vault UI (`frontend/src/components/VaultLibrary.tsx`)**: Renamed drawer header to `📖 Universal Intelligence Vault`, updated multi-genre placeholder/empty state, added dynamic domain badge generator (`getCategoryBadge`), dynamic metadata counter string (`metaText`), and domain-specific action buttons (`"Open Travel Guide ↗"`, `"Open Workout View ↗"`, `"Open Tutorial ↗"`, `"Open Product View ↗"`, `"Open Recipe ↗"`).

#### 4. Testing & Verification:
- Backend Unit Test Suite (`pytest tests/`): **191 / 191 PASSED**.
- Browser E2E Staging Verification: Verified live on Staging preview deployment.

### 🚨 ISSUE-044: FAQ Modal & Full User Manual View Isolation Cleanup
- **Date**: 2026-09-20
- **Affected Files**: `frontend/src/app/page.tsx`, `frontend/src/components/FaqSection.tsx`, `docs/TROUBLESHOOTING.md`

#### 1. What Happened (Symptom):
The top navbar contained a redundant standalone `"User Manual"` button, and inside the FAQ modal drawer, the 4-step Quick Start cards and search bar category pills overlapped when switching to the Full User Manual view.

#### 2. Root Cause:
1. `page.tsx` rendered duplicate buttons for `FAQ & Guide` and `User Manual` in the navbar.
2. `FaqSection.tsx` rendered 4-step Quick Start cards and search bar category pills outside the `activeCategory !== 'user_manual'` conditional wrapper.

#### 3. Resolution (Code Changes):
1. **Navbar Cleanup (`page.tsx`)**: Removed the separate `User Manual` button from top navigation bar.
2. **Strict View Isolation (`FaqSection.tsx`)**: Wrapped 4-step Quick Start cards, FAQ category pills, and search bar inside `activeCategory !== 'user_manual'` branch. Removed `user_manual` pill from the search bar row.

#### 4. Testing & Verification:
- Next.js build (`npm run build`): **100% SUCCESSFUL**.
- Browser E2E Staging Verification: Verified live on Staging preview deployment.

### 🚨 ISSUE-045: Comprehensive Hardening (Groups C -> B -> A -> D -> E)
- **Date**: 2026-09-20
- **Affected Files**: `backend/app/services/url_validator.py`, `backend/app/core/security.py`, `backend/app/api/v1/telemetry.py`, `backend/app/api/v1/library.py`, `frontend/src/lib/recipeUtils.ts`, `frontend/src/components/OverflowBottomSheet.tsx`, `frontend/src/app/page.tsx`

#### 1. What Happened (Symptom):
Need to execute multi-domain system hardening across SSRF/IP redirect validation, stream proxy security, pure function refactoring, WCAG 2.2 accessibility, explicit admin telemetry authorization, and vault re-hydration without client-side affiliate tags.

#### 2. Root Cause:
1. **SSRF & IP Validation**: URLs required re-validation after redirects (max 3 hops) with `ipaddress.is_global` check on all DNS resolved addresses.
2. **Stream Proxy & Token**: IG video preview required short-lived signed HMAC tokens instead of unauthenticated `?url=` queries.
3. **Frontend Refactoring**: Pure functions in `recipeUtils.ts` with explicit parameters (`resolveMediaPreview`, `generateStructuredText`, `parseIngredients`) decoupled logic from closure state.
4. **WCAG Accessibility & Telemetry**: Bottom sheet required ARIA attributes (`role="dialog"`, `aria-modal="true"`, focus trap, Escape key handler), input fields required `>=16px` font size and `min-height 44px`, and telemetry endpoints required `ADMIN_API_KEY` authentication without storing raw URLs in metrics.
5. **Vault Re-hydration**: Saved vault items without server-built affiliate links needed re-hydration via `/api/v1/library/rehydrate` so buy buttons appear without hardcoded client-side tags.

#### 3. Resolution (Code Changes):
- `url_validator.py`: Added `validate_url_and_follow_redirects` with max 3 hops, `resolve_and_validate_hostname` with `ipaddress.is_global`, HMAC stream token generation/verification, and `validate_merchant_redirect_url`.
- `recipeUtils.ts`: Extracted pure functions with explicit state parameters and unit test coverage (`recipeUtils.test.ts`).
- `OverflowBottomSheet.tsx`: Implemented WCAG-compliant bottom sheet modal with focus trap and keyboard listeners.
- `security.py` & `telemetry.py`: Added `require_admin_user` checking `X-Admin-Api-Key` or `role == 'admin'`, and stripped raw URLs from telemetry event payloads.
- `library.py` & `test_vault_rehydration.py`: Implemented `/api/v1/library/rehydrate` endpoint and added dedicated test suite.

#### 4. Testing & Verification:
- Next.js Build (`npm run build`): **SUCCESSFUL (0 errors)**.
- Vitest Suite (`npm test`): **9 / 9 PASSED**.
- Backend Pytest Suite (`pytest tests/`): **211 / 211 PASSED**.

### 🚨 ISSUE-046: Security Rule Enforcement & Infrastructure Isolation
- **Date**: 2026-09-20
- **Affected Files**: `backend/app/core/config.py`, `backend/app/core/security.py`, `backend/app/services/streamlit_app.py`, `backend/app/api/v1/library.py`, `frontend/src/components/VaultLibrary.tsx`, `scripts/verify_egress.py`, `tests/test_backend_security_hardening.py`, `tests/test_hinglish_prompt_snapshot.py`

#### 1. What Happened (Symptom):
1. `TRUSTED_PROXY` defaulted to `True` or trusted unvalidated proxy headers by default.
2. Container egress firewall verification needed real automated tests blocking 169.254.169.254 and private IPs.
3. IP pinning needed tests asserting Host header and TLS SNI/server_hostname preservation.
4. Vault item rehydration required sliding window rate limiting (30 req/min) and UI wiring in `VaultLibrary.tsx`.
5. Streamlit app contained legacy `?admin=1` URL parameter gating.
6. Hinglish prompt snapshot test was required for Rule 13 compliance.

#### 2. Root Cause:
1. Proxy settings must default to untrusted (`TRUSTED_PROXY=False`) unless explicitly enabled per environment.
2. IP pinning overrides destination socket IP; HTTP client MUST preserve the original Host header and TLS SNI server hostname.
3. Legacy Vault items needed automatic re-hydration upon selection to receive fresh stream tokens without triggering re-extraction.
4. Streamlit app line 833 evaluated `admin=1` query string without server-side authentication.

#### 3. Resolution (Code Changes):
- `config.py`: Set `TRUSTED_PROXY: bool = False`. Documented environment values in `.env.example` and `DISASTER_RECOVERY.md`.
- `scripts/verify_egress.py`: Created automated python & bash egress verification script asserting metadata/private IP connection drops and public HTTPS success.
- `test_backend_security_hardening.py`: Added `test_ip_pinning_uses_first_public_ip_and_no_reresolve` and `test_ip_pinning_preserves_host_header_and_tls_sni`.
- `library.py` & `VaultLibrary.tsx`: Added rate limiter to `/api/v1/library/rehydrate` and wired auto-rehydration into `onSelectRecipe`.
- `streamlit_app.py`: Hardcoded `is_admin = False` permanently disabling URL parameter gating.
- `test_hinglish_prompt_snapshot.py`: Added snapshot test asserting Hinglish culinary prompt mappings in `REGIONAL_EXTRACTION_SYSTEM_PROMPT`.

#### 4. Testing & Verification:
- Egress Script (`python scripts/verify_egress.py`): **ALL EGRESS FIREWALL CHECKS PASSED [OK]**.
- Frontend Vitest (`npm test`): **9 / 9 PASSED**.
- Backend Pytest (`pytest tests/`): **216 / 216 PASSED**.

### 🚨 ISSUE-047: IP Pinning & PinnedHTTPSConnection Security Hardening (UPA-1205)
- **Date**: 2026-09-26
- **Affected Files**: `backend/app/services/url_validator.py`, `tests/test_pinned_https.py`

#### 1. What Happened (Symptom):
Outbound HTTP/HTTPS connections needed protection against DNS rebinding and Time-of-Check-Time-of-Use (TOCTOU) race conditions where DNS resolution changes between validation and connection time. Additionally, DNS lookups could block the asyncio event loop, and redirect validation needed single-resolution fail-closed enforcement.

#### 2. Root Cause:
1. Standard `http.client.HTTPSConnection` sets TLS SNI `server_hostname` to the socket destination host (the numeric IP when connecting to a pinned address), causing TLS handshake/cert validation failures unless explicitly overridden.
2. Synchronous DNS calls (`socket.getaddrinfo`) block the main event loop if executed on async routes.
3. Redirect probes needed to connect directly to the pre-validated pinned IP without issuing secondary unbounded DNS queries.

#### 3. Resolution (Code Changes):
- `backend/app/services/url_validator.py`:
  - Created `PinnedHTTPSConnection(http.client.HTTPSConnection)` subclass binding `self.target_host` to `server_hostname` for TLS SNI and certificate verification while connecting socket to `pinned_ip`.
  - Added fail-closed `connect()` guard verifying `ip.is_global` before establishing the TCP socket.
  - Implemented `async_resolve_and_validate_hostname` and `async_validate_url_and_follow_redirects` using a dedicated `ThreadPoolExecutor` off the event loop.
  - Hardened `validate_url_and_follow_redirects` to use single DNS resolution per hop and direct pinned IP probing.
- `tests/test_pinned_https.py`:
  - Added comprehensive test suite with `trustme` CA certificate generation, loopback TLS handshakes, SNI verification, cert mismatch rejection, and async helper validation.

#### 4. Testing & Verification:
- Unit Test Suite (`pytest tests/test_pinned_https.py -v`): **13 / 13 PASSED [MEASURED]**.
- Security Suite (`pytest tests/test_backend_security_hardening.py tests/test_ssrf_entrypoint.py tests/test_pinned_https.py -v`): **36 / 36 PASSED [MEASURED]**.
- Full Pytest Regression (`pytest tests/ -q`): **249 PASSED, 3 DESELECTED in 22.24s [MEASURED]**.
- Frontend Vitest (`npm test`): **12 / 12 PASSED [MEASURED]**.
- TypeScript Check (`npx tsc --noEmit`): **0 ERRORS [MEASURED]**.

### 🚨 ISSUE-048: Container Egress Firewall Hardening & Rollback Automation (UPA-1206)
- **Date**: 2026-09-26
- **Affected Files**: `deploy/setup_egress_firewall.sh`, `deploy/rollback_egress_firewall.sh`, `scripts/verify_egress.py`

#### 1. What Happened (Symptom):
Docker containers running API and Celery workers required strict host-level egress network filtering to prevent container breakouts or SSRF pivoting to internal cloud instance metadata (169.254.169.254) and RFC 1918 private subnets, while guaranteeing that intra-compose communications (API <-> Redis <-> Caddy) and inbound connections remained undisturbed.

#### 2. Root Cause:
1. Bare `-d <private range> -j REJECT` rules without source filtering can inadvertently impact other host-level routing.
2. Compose-to-compose traffic (e.g. `172.28.0.0/16` or `172.16.0.0/12`) requires an explicit `RETURN` rule before RFC 1918 reject rules.
3. IPv6 egress was unconfigured in `ip6tables`.
4. An emergency single-command rollback script was required for operator safety.

#### 3. Resolution (Code Changes):
- `deploy/setup_egress_firewall.sh`:
  - Enforced `-s <compose subnet>` source binding on all outbound filtering rules.
  - Inserted compose-to-compose `RETURN` rule before private range blocks.
  - Added IPv6 filtering with `ip6tables` (`fc00::/7`, `fe80::/10`, `::1/128`).
  - Added idempotency (flush on start) and reboot persistence via `netfilter-persistent` / `/etc/iptables`.
- `deploy/rollback_egress_firewall.sh`:
  - Created automated rollback script flushing `DOCKER-USER` chain and resetting policy to `RETURN`.
- `scripts/verify_egress.py`:
  - Verified local and container egress verification suite.

#### 4. Testing & Verification:
- Egress Script (`python scripts/verify_egress.py`): **ALL CONTAINER EGRESS FIREWALL CHECKS PASSED [OK] [MEASURED]**.
- Full Pytest Regression (`pytest tests/ -q`): **249 PASSED, 3 DESELECTED in 22.34s [MEASURED]**.
- Status: **Resolved on Dev**.

---

### 🚨 ISSUE-049: Docker Egress Firewall Broad RFC1918 172.16/12 RETURN Rule Bypass (UPA-1206)
- **Date**: 2026-09-26
- **Affected Files**: `deploy/setup_egress_firewall.sh`, `scripts/verify_egress.py`, `docs/po-governance/JIRA_BACKLOG.md`

#### 1. What Happened (Symptom):
During isolated Linux test-host verification, the `DOCKER-USER` chain contained:
```text
-A DOCKER-USER -s 172.28.0.0/16 -d 172.28.0.0/16 -j RETURN
-A DOCKER-USER -s 172.16.0.0/12 -d 172.16.0.0/12 -j RETURN
...
-A DOCKER-USER -s 172.28.0.0/16 -d 172.16.0.0/12 -j REJECT
```
Because the Compose subnet (`172.28.0.0/16`) is a subset of the RFC 1918 `172.16.0.0/12` block, any packet directed to another private IP in `172.16.0.0/12` matched the broad `172.16.0.0/12 -> 172.16.0.0/12 RETURN` rule early, terminating chain traversal before reaching the intended `-d 172.16.0.0/12 -j REJECT` rule at line 15.

#### 2. Root Cause:
`deploy/setup_egress_firewall.sh` defined `DOCKER_BRIDGE_RANGE="172.16.0.0/12"` and added an intra-bridge exception rule `iptables -A DOCKER-USER -s 172.16.0.0/12 -d 172.16.0.0/12 -j RETURN`. This allowed broad egress from the Compose subnet to arbitrary private subnets in the `172.16.0.0/12` space.

#### 3. Resolution (Code Changes):
1. **Removed Broad RETURN Rule**: Removed `DOCKER_BRIDGE_RANGE="172.16.0.0/12"` from `deploy/setup_egress_firewall.sh`. Allowed compose-to-compose communication strictly for the explicitly configured `COMPOSE_SUBNET` (`-s "${COMPOSE_SUBNET}" -d "${COMPOSE_SUBNET}" -j RETURN`).
2. **Strengthened Verification**: Updated `scripts/verify_egress.py` with explicit test cases for non-compose `172.16.0.0/12` endpoints (`172.16.0.1` and `172.31.255.1`), verifying they are connection refused / rejected.

#### 4. Testing & Verification:
- **Container Execution**: Executed `scripts/verify_egress.py` inside a container on `universalpro-test-net` (`172.28.0.0/16`) on an isolated DinD Linux host:
  - `http://169.254.169.254/latest/meta-data/` -> **BLOCKED AS EXPECTED (Connection refused)** [MEASURED]
  - `http://10.0.0.1/` -> **BLOCKED AS EXPECTED (Connection refused)** [MEASURED]
  - `http://192.168.1.1/` -> **BLOCKED AS EXPECTED (Connection refused)** [MEASURED]
  - `http://172.16.0.1/` -> **BLOCKED AS EXPECTED (Connection refused)** [MEASURED]
  - `http://172.31.255.1/` -> **BLOCKED AS EXPECTED (Connection refused)** [MEASURED]
  - `https://www.instagram.com/` -> **SUCCESS (HTTP 200)** [MEASURED]
  - `http://service-peer:8000/` (intra-compose container-to-container) -> **SUCCESS (HTTP 200)** [MEASURED]
  - DNS resolution -> **RESOLVED (57.144.40.34)** [MEASURED]
- **Idempotency**: Executed `setup_egress_firewall.sh` twice; verified 0 duplicate rules in `iptables -S DOCKER-USER` and `ip6tables -S DOCKER-USER`.
- **Rollback**: Executed `rollback_egress_firewall.sh`; verified clean `-A DOCKER-USER -j RETURN` on IPv4 and IPv6.
- **Pytest**: `pytest tests/ -q` -> **249 PASSED, 3 DESELECTED in 22.28s [MEASURED]**.
- **Classification**: **VERIFIED — CONTAINER EXECUTION**.

---

### 🚨 ISSUE-050: Python 3.11 Runtime Dependency Cleanup, Dev Partitioning & Pinned Lockfile (UPA-1207)
- **Date**: 2026-09-27
- **Affected Files**: `requirements.txt`, `requirements-dev.txt`, `requirements.lock`, `backend/requirements.txt`, `backend/app/services/llm_council.py`, `backend/app/workers/tasks.py`

#### 1. What Happened (Symptom):
During repository dependency auditing and Docker containerization:
1. `requirements.txt` contained dead dependencies (`pypdf`) from earlier prototype iterations and lacked explicit `uvicorn[standard]` for FastAPI container startup.
2. Developer and test tools (`pytest`, `pytest-asyncio`, `pytest-socket`, `pip-audit`, `trustme`, `fakeredis`) were mixed or unpartitioned.
3. In Python 3.11, `backend/app/services/llm_council.py` triggered a `SyntaxError: f-string expression part cannot include a backslash` when joining strings inside an f-string expression.
4. `backend/app/workers/tasks.py` had an import resolution conflict where direct submodule imports bypassed top-level mock patch targets in `tests/test_sprint6_content_payload.py`.

#### 2. Root Cause:
1. Manifest drift across sprints without strict dev vs. runtime dependency partitioning.
2. Python 3.11 syntax constraint on f-string inner backslashes (prior to Python 3.12 grammar improvements).
3. Ambiguity between top-level `import ai_router` vs nested package import in Celery worker context.

#### 3. Resolution (Code Changes):
1. **Manifest Cleaning & Dev Partitioning**:
   - `requirements.txt`: Removed dead `pypdf`, added explicit `uvicorn[standard]>=0.34.0`, synced `backend/requirements.txt`.
   - `requirements-dev.txt`: Added `pytest>=7.0.0`, `pytest-asyncio>=0.23.0`, `pytest-socket>=0.8.1`, `pip-audit>=2.7.0`, `trustme>=1.1.0`, `fakeredis>=2.20.0`, `pip-tools>=7.4.0`.
2. **Python 3.11 Syntax Fix**:
   - `backend/app/services/llm_council.py`: Extracted `formatted_anon_outputs = "---".join(...)` before the f-string interpolation.
3. **Import Robustness**:
   - `backend/app/workers/tasks.py` & services: Added defensive `try/except ImportError` fallbacks ensuring both top-level and package-level module resolution without breaking existing test mock targets.
4. **Deterministic Lockfile Generation**:
   - Generated pinned `requirements.lock` using `pip-compile` inside an isolated Docker `python:3.11-slim` container.

#### 4. Testing & Verification:
- **Clean Venv Python 3.11 Container**: Built clean environment in Docker container; imported all backend modules (`ALL RUNTIME IMPORTS SUCCESSFUL IN CONTAINER [OK]`) [MEASURED].
- **Deterministic Lockfile**: Re-ran resolution; verified 1:1 exact byte match (186 lines pinned) [MEASURED].
- **Security Audit**:
  - `pip-audit -r requirements.txt` -> **0 known vulnerabilities found [OK] [MEASURED]**.
  - `pip-audit -r requirements.lock` -> **0 known vulnerabilities found [OK] [MEASURED]**.
- **Docker Build & Boot**:
  - Built `universal-pro-ai:upa-1207` from Dockerfile [MEASURED].
  - Booted container with `docker run -d -p 8000:8000 --name upa1207-test universal-pro-ai:upa-1207` [MEASURED].
  - `curl http://localhost:8000/health` -> **HTTP 200 `{"status":"healthy",...}` [MEASURED]**.
- **Full Pytest Suite**: `pytest tests/ -q` -> **249 passed, 3 deselected in 22.33s [MEASURED]**.
- **Status**: **Resolved on Dev**.

---

### 🚨 ISSUE-051: Governance Heading Assertion Brittleness in Sprint 14 Commerce Suite (UPA-1311)
- **Date**: 2026-10-18
- **Affected Files**: `tests/test_sprint14_commerce.py`

#### 1. What Happened (Symptom):
During pre-promotion test suite execution and CI validation under Rule 16, `tests/test_sprint14_commerce.py::TestSprint14CommerceIntegration::test_four_core_document_governance_contract_and_user_manual` failed with:
`AssertionError: 'Mandatory 4-Core Document Governance Contract' not found in AGENTS.md`
The test failure blocked clean promotional gates without requiring an owner-approved Rule 16 exception.

#### 2. Root Cause:
Under UPA-1308 (commit `010a56cff15b5c9398a90b499aff59c11f74d8fd`), Section 9 of `AGENTS.md` was expanded from 4 documents to 6 living architecture documents and retitled to `## 9. Mandatory Document Governance Contract & Living Architecture Files` when adding `docs/architecture/DECISIONS.md` and `docs/architecture/FLOW.md`. The test in `test_sprint14_commerce.py` asserted the exact legacy substring `"Mandatory 4-Core Document Governance Contract"`, causing a brittle failure despite the underlying contract being fully satisfied.

#### 3. Resolution (Code Changes):
1. **Line-Anchored Section 9 Extraction & Resilient Assertion**:
   - Replaced exact heading assertion with line-anchored level-two heading extraction (`re.search(r"(?m)^##\s+9\..*$", ...)` up to the next level-two heading `re.search(r"(?m)^##\s+", ...)` without hardcoding Section 10).
   - Asserted that Section 9 and its terminating level-two heading exist with clear failure diagnostics.
   - Iterated over all six required living document paths (`docs/TROUBLESHOOTING.md`, `docs/po-governance/PRODUCT_OWNER_UX_SHOWCASE.md`, `docs/architecture/DISASTER_RECOVERY.md`, `docs/USER_MANUAL.md`, `docs/architecture/DECISIONS.md`, and `docs/architecture/FLOW.md`) and asserted their presence within Section 9.
   - Added explicit diagnostic messages identifying the exact missing document path upon assertion failure.
2. **Method Renaming**:
   - Renamed test method from `test_four_core_document_governance_contract_and_user_manual` to `test_mandatory_document_governance_contract_and_user_manual`.
3. **Preservation of Surrounding Invariants**:
   - Preserved `manual_file.exists()`, manual content checks, and FAQ modal assertions.

#### 4. Testing & Verification:
- **Focused Unit Test**: `pytest tests/test_sprint14_commerce.py -v` -> **5 passed in 0.22s [MEASURED]**.
- **Full Backend Pytest Suite**: `pytest tests/` -> **349 passed, 3 deselected, 12 warnings in 48.20s [MEASURED]**.
- **Frontend Type Check**: `npx tsc --noEmit` -> **0 errors [MEASURED]**.
- **Frontend Lint**: `npm run lint` -> **0 errors (7 warnings) [MEASURED]**.
- **Frontend Unit Tests**: `npm test` -> **40 passed in 2.27s [MEASURED]**.
- **Frontend Production Build**: `npm run build` -> **Compiled in 913ms, 8/8 routes generated [MEASURED]**.
- **Status**: **Resolved on Dev (Commits `e74c77d`, `e223af9`); Promoted to Staging via PR #6 (`48a426c`); Staging verification accepted by Product Owner in SIGN_OFF.md [MEASURED]**.

---

### 🚨 ISSUE-052: Operational Workflow Streamlining & Mandatory Two-Tier Playwright Release Gates (UPA-1401)
- **Date**: 2026-10-19
- **Affected Files**: `AGENTS.md`, `frontend/e2e/specs/smoke.staging.e2e.ts`, `frontend/playwright.config.ts`, `frontend/package.json`, `scripts/ci_check.py`, `scripts/promote.py`, `scripts/verify_promotion.py`, `docs/architecture/DISASTER_RECOVERY.md`, `docs/architecture/DECISIONS.md`, `docs/architecture/FLOW.md`

#### 1. What Happened (Symptom):
1. The release lifecycle had expanded into approximately 13 loosely structured operational phases, causing boundary ambiguity between development, staging promotion, live environment verification, and production release.
2. In the test suite, mocked Playwright E2E tests (`npm run test:e2e:mocked` targeting `http://localhost:3000`) were not strictly separated in policy from live deployed-environment release gates, risking false confidence where passing mocked CI checks might be mistaken for live Staging verification.
3. Staging deployments lacked a mandatory, lightweight live browser smoke test that executes after every Staging deployment before Product Owner acceptance, while un-mocked live extraction E2E suites needed clear conditional triggering without creating dirty database rows.
4. Proposed Staging API endpoints (such as `staging-api.universal-pro-ai.com/health`) were cited in documentation without authoritative DNS/TLS verification, and production rollback procedures relied on unconditional git reverts.

#### 2. Root Cause:
1. Operational phases lacked strict consolidation into well-defined, sequential release lifecycle phases with explicit failure-stop boundaries.
2. Playwright configuration did not isolate staging smoke specifications from mocked UI test runs, causing potential test pollution or unintended live environment requests during offline developer runs.
3. The Staging API domain is currently reachable via Oracle Cloud Infrastructure Staging VM IP `129.225.86.241` over Caddy reverse proxy; custom FQDN DNS/TLS was deferred, so documentation required reconciliation with configured ground truth.
4. An automatic `git revert` on `origin/main` without concurrency checks or target validation could overwrite concurrent commits or bypass required Product Owner authorization gates.

#### 3. Resolution (Code Changes):
1. **Six-Phase Release Lifecycle Workflow (`AGENTS.md` Rule 2)**:
   - Consolidated release operations into six sequential phases:
     - Phase 1: Intake & Governed Planning (backlog registration, risk assessment, surgical rollback plan, owner checkpoint gate).
     - Phase 2: Dev Implementation & Local Verification (sandbox implementation, focused regressions, mocked Playwright `test:e2e:mocked`).
     - Phase 3: Living Document Sync & Definitive Verification (sync all six living architecture documents, Rule 21.6 assessment, definitive full Rule 16 pipeline on final synchronized tree, Dev/PO boundary stop).
     - Phase 4: Governed Staging Promotion (promotion branch, PR to `staging`, remote GitHub Actions CI, owner approval, merge).
     - Phase 5: Live Staging Deployment Verification & Release Gates (deploy frontend & backend, verify deployed versions, execute Tier 1 live Staging smoke gate, conditionally execute Tier 2 un-mocked live extraction gate under `ALLOW_DB_WRITES=false`, record commit-bound evidence, stop for PO sign-off).
     - Phase 6: Governed Production Release & Closeout (separate prior owner authorization, deploy to Production Vercel and OCI VM `140.245.214.28`, post-deployment live smoke verification, bounded rollback handling on failure, owner closeout in `SIGN_OFF.md` and `JIRA_BACKLOG.md`).
2. **Two-Tier Live Staging Release Gate Policy (`AGENTS.md` Rule 2 & Rule 16)**:
   - **Tier 1 (Universal Live Staging Smoke Gate)**: Mandatory after every Staging deployment before Staging acceptance (`smoke.staging.e2e.ts`). Verifies UI boot, hero CTA interactivity, single docked video player contract, and design system tokens.
   - **Tier 2 (Conditional Live Extraction E2E Gate)**: Mandatory whenever changes affect media extraction, request routing, background-worker behavior, or AI inference (`staging.live.e2e.ts`). Operates safely under `ALLOW_DB_WRITES=false` via ephemeral Redis/memory `JobManager` results with zero dirty PostgreSQL rows.
   - Formulated four-state gate semantics: `PASS`, `FAIL`, `BLOCKED`, `NOT RUN`.
3. **Frontend Playwright Configuration & Smoke Spec**:
   - Created [`frontend/e2e/specs/smoke.staging.e2e.ts`](file:///d:/Personal%20Projects/recipe-extractor/frontend/e2e/specs/smoke.staging.e2e.ts) with origin validation, Vercel bypass protocol, core route `/` 200 OK assertion, design system tokens inspection (`--bg-base`, `--accent-emerald`, `--text-primary`), mobile (375x812) and desktop (1280x800) responsive layouts without horizontal overflow, input font-size >= 16px (Rule 15), interactive controls (sample chips, theme toggle, submit CTA), single docked player assertion, HTTP 4xx/5xx tracking, and safety environment guard (`ALLOW_LIVE_STAGING_SMOKE`).
   - Updated [`frontend/playwright.config.ts`](file:///d:/Personal%20Projects/recipe-extractor/frontend/playwright.config.ts) to define `staging-smoke` project targeting authoritative Vercel Staging preview origin (`https://universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app`) and ignore live/staging specs in `mocked-ui`.
   - Updated [`frontend/package.json`](file:///d:/Personal%20Projects/recipe-extractor/frontend/package.json) with `"test:e2e:staging:smoke": "playwright test --project=staging-smoke"`.
4. **CI & Promotion Tooling Enhancement**:
   - Updated [`scripts/ci_check.py`](file:///d:/Personal%20Projects/recipe-extractor/scripts/ci_check.py) to run the full Rule 16 5-step pipeline (`npx tsc --noEmit`, `npm run lint`, `npm test`, `npm run build`, `pytest tests/`) sequentially with UTF-8 Windows console output.
   - Enhanced [`scripts/verify_promotion.py`](file:///d:/Personal%20Projects/recipe-extractor/scripts/verify_promotion.py) with `--deployed [staging|prod]` mode verifying actual frontend and backend health endpoints, and added `verify_evidence_manifest` enforcing `manifest.commitSha === expectedCommitSha` and anti-false-green gate validation.
   - **P0 Evidence Classification Enforcement**: Enforced that `executionClassification` must be `"live"` for Staging and Production release gates; `"mocked"` evidence is accepted strictly on Dev. Missing, invalid, or mismatched classification fails closed with exit code 1. Mocked evidence cannot satisfy Staging or Production release gates.
   - **GAP-01 Promotion Entry Point Preflight & Source-Aware Mapping**: Enhanced [`scripts/promote.py`](file:///d:/Personal%20Projects/recipe-extractor/scripts/promote.py) to execute source-aware preflight evidence verification (`verify_evidence_manifest`):
     - Dev → Staging preflight: verifies source `Dev` manifest using `--env dev` with expected Dev SHA, accepting Dev-appropriate classification (`mocked` or `live`).
     - Staging release acceptance: requires live Staging evidence bound to the deployed Staging revision (`executionClassification: "live"`).
     - Staging → Production preflight: verifies source `staging` manifest using `--env staging` with expected Staging SHA, strictly enforcing `executionClassification: "live"` (`mocked` evidence strictly rejected for Staging/Production gates).
   - **GAP-02 Verifier Output Label & Verdict Hygiene**: Renamed `Manifest Overall Status` to `Payload Self-Reported Status` in [`scripts/verify_promotion.py`](file:///d:/Personal%20Projects/recipe-extractor/scripts/verify_promotion.py) so raw payload text is not presented as verified gate truth. Emits explicit evaluated final verdicts (`REJECTED (FAILED CLOSED)` / `PASSED`), ensuring an overall gate pass is never implied when manifest validation fails closed.
   - Enhanced [`frontend/src/lib/evidenceManifest.ts`](file:///d:/Personal%20Projects/recipe-extractor/frontend/src/lib/evidenceManifest.ts) with `options.expectedCommitSha` validation and anti-false-green `notRun > 0` validation. Added 4 unit tests in [`frontend/src/lib/__tests__/evidenceManifest.test.ts`](file:///d:/Personal%20Projects/recipe-extractor/frontend/src/lib/__tests__/evidenceManifest.test.ts).
   - Created dedicated manifest verification pytest suite in [`tests/test_verify_promotion_manifest.py`](file:///d:/Personal%20Projects/recipe-extractor/tests/test_verify_promotion_manifest.py) containing 28 tests covering SHA checks, classification rules, source-aware promote preflight, and output label/verdict assertions.
5. **Hardened Staging Smoke Error Detection (GAP-03)**:
   - In [`frontend/e2e/specs/smoke.staging.e2e.ts`](file:///d:/Personal%20Projects/recipe-extractor/frontend/e2e/specs/smoke.staging.e2e.ts), expanded HTTP 4xx/5xx error monitoring to include both Vercel frontend origin and configured backend API origin (`STAGING_API_URL` or fallback `http://129.225.86.241`). Cross-origin backend failures are tracked and asserted against.
   - Added fail-closed navigation validation helper `validateNavigationResponse` asserting non-null navigation response and `response.ok()`, preventing silent false greens if page loading fails.
   - Added 14 unit tests in [`frontend/src/lib/__tests__/stagingSmoke.test.ts`](file:///d:/Personal%20Projects/recipe-extractor/frontend/src/lib/__tests__/stagingSmoke.test.ts) covering API origin resolution, monitored URL pattern matching, and navigation response validation.
   - *Operational Status Note*: The hardened smoke checks have not yet been executed against live Staging (they remain offline in Dev, guarded by `ALLOW_LIVE_STAGING_SMOKE=true`).
6. **Governed, Bounded Production Rollback**:
   - Replaced blind git revert with bounded rollback protocol in `docs/architecture/DISASTER_RECOVERY.md`: capture failed SHA and smoke evidence, alert owner, halt progression, identify previous known-good releases on Vercel and OCI VM, and stop for operator intervention if automated rollback is not explicitly approved.
7. **Ticket-Scoped Promotion Branch Support & Fail-Closed Remote Lookup (`scripts/promote.py`)**:
   - Mandated validated `--ticket <ticket>` CLI argument when promoting to Staging (`--to staging`), normalizing tickets (`validate_ticket_format`) to `promotion/<ticket>-staging` (e.g. `promotion/upa-1401-staging`). Rejects malformed or empty tickets with `ValueError`.
   - Added collision detection (`check_branch_exists`) checking both local refs (`git show-ref`) and remote refs (`git ls-remote`). Replaced destructive `git checkout -B` with safe `git checkout -b`, halting safely before branch creation or push if a branch already exists.
   - **Remote-Lookup Fail-Closed Handling**: Distinguishes clean nonexistent branches (`returncode == 0` and empty stdout) from remote failures (`returncode != 0`). Any non-zero exit code (network error, auth failure, git error) raises `RuntimeError` and halts promotion with exit code 1 before preflight and branch creation, never misclassifying remote failure as branch absence.
   - Expanded manifest verification pytest suite in `tests/test_verify_promotion_manifest.py` from 28 to 50 passing unit tests.
8. **Documentation Plan Reconciliation**:
   - Recorded ADR-008 in `docs/architecture/DECISIONS.md` and updated ADR Index table (reconciled sequential ADR-008 vs preliminary reference ADR-014).
   - Added Section 8 (Governance Reference) and Section 9 (Developer & QA Guide) to `docs/USER_MANUAL.md` and updated Table of Contents (reconciled Section 9 vs preliminary reference Section 19).
   - Updated `docs/po-governance/JIRA_BACKLOG.md` with explicit Rule 21.6 Documentation Impact Assessment across all six living architecture documents.

#### 4. Testing & Verification:
- **Focused Unit Test Suite**: `pytest tests/test_sprint14_commerce.py tests/test_port_shielding_and_docs.py -v` -> **12 passed in 0.40s [MEASURED]**.
- **Evidence Manifest Pytest Suite**: `pytest tests/test_verify_promotion_manifest.py -v` -> **50 passed in 0.64s [MEASURED]**.
- **TypeScript Compilation**: `npx tsc --noEmit` -> **0 errors [MEASURED]**.
- **Frontend Vitest Suite**: `npm test` -> **62 passed in 1.93s [MEASURED]** (including 29 evidence manifest tests and 14 staging smoke unit tests).
- **Frontend Lint**: `npm run lint` -> **0 errors (7 pre-existing warnings) [MEASURED]**.
- **Mocked Playwright E2E Suite**: `npm run test:e2e:mocked` -> **7 passed in 22.3s, Overall Gate Status: PASS [MEASURED]**.
- **Staging Smoke Execution Status**: `smoke.staging.e2e.ts` skipped locally (1 skipped, 0 live network calls; not yet executed against live Staging) [MEASURED].
- **Preservation Verification**: `frontend/e2e/specs/staging.live.e2e.ts`, `.agents/skills/gravitas/`, and `skills-lock.json` strictly preserved without modification.
- **Status**: **Resolved on Dev; Ready for Product Owner Phase 3 review**.

---

### 🚨 ISSUE-053: Tier 1 Staging Smoke Submit CTA Assertion Failure & Environment Classification Audit (UPA-1401)
- **Date**: 2026-10-19
- **Affected Files**: `frontend/e2e/specs/smoke.staging.e2e.ts`, `frontend/e2e/reporters/evidence-manifest-reporter.ts`, `scripts/verify_promotion.py`

#### 1. What Happened (Symptom):
Following the governed promotion of UPA-1401 via PR #7 to `staging` (merge commit `85fa6e7b7366711ab9c3f9b2a3271ecae86d99d7`), remote GitHub Actions CI passed (run `39300030918`) and Vercel deployed Staging successfully (deployment `#7181210296`). However, when executing the mandatory Tier 1 live Staging browser smoke test (`npm run test:e2e:staging:smoke`), the test failed with exit code 1:
```text
Error: expect(locator).toBeEnabled() failed
Locator: getByLabel('Get video intelligence')
Expected: enabled
Received: disabled
Timeout: 10000ms
```
Additionally, the generated evidence manifest recorded `executionClassification: "live"` and `commitSha: "85fa6e7b7366711ab9c3f9b2a3271ecae86d99d7"`, but defaulted to `environment: "dev"`. The verification command also incorrectly used `--env dev`.

#### 2. Root Cause:
1. **Assertion Contract Mismatch**: In `frontend/src/app/page.tsx:1038`, the application intentionally disables the submit button whenever the URL input is empty: `disabled={isLoading || !url}`. The initial smoke test asserted `await expect(submitBtn).toBeEnabled();` on initial page load before any input was supplied, which failed against valid application behavior.
2. **Environment Defaulting**: In `frontend/e2e/reporters/evidence-manifest-reporter.ts`, `environment` resolves from `process.env.TEST_ENV || process.env.APP_ENV || 'dev'`. Because neither `TEST_ENV` nor `APP_ENV` was set during invocation, the reporter defaulted to `'dev'` despite targeting the live Staging preview URL.

#### 3. Resolution (Code Changes):
1. **Test-Only Assertion Correction on Dev (`frontend/e2e/specs/smoke.staging.e2e.ts`)**:
   Committed locally on Dev (commit `0c107ca681b1e5dda8d61f5b58f8e33ffb224e67`):
   ```typescript
   const submitBtn = page.getByLabel('Get video intelligence');
   await expect(submitBtn).toBeVisible();
   // Application enforces disabled={isLoading || !url}; verify initial disabled state on empty input
   await expect(submitBtn).toBeDisabled();

   // Verify input interaction enables the submit CTA without initiating extraction
   await urlInput.fill('https://www.instagram.com/reel/C1234567890/');
   await expect(submitBtn).toBeEnabled();
   await urlInput.clear();
   ```
2. **Environment Classification Requirement**:
   Documented operational requirement: live Staging smoke executions must supply `$env:TEST_ENV = "staging"` and bind to the active deployed commit SHA (`$env:GIT_COMMIT_SHA = "<deployed-staging-sha>"`), and manifest verification must use `--env staging`.

#### 4. Testing & Verification:
- **TypeScript Static Check**: `npx tsc --noEmit` -> **0 errors [MEASURED]**.
- **Frontend Vitest Suite**: `npm test` -> **62 passed in 2.17s [MEASURED]**.
- **Mocked Playwright Suite**: `npm run test:e2e:mocked` -> **7 passed in 20.1s, Overall Gate Status: PASS [MEASURED]** (includes empty URL submission guard test).
- **Backend Manifest Pytest**: `pytest tests/test_verify_promotion_manifest.py` -> **50 passed in 0.77s [MEASURED]**.
- **Working Tree Preservation**: Zero changes to application validation logic (`page.tsx`), and main working tree files strictly preserved.
- **Status**: **Resolved on Dev (commit `0c107ca`); live Staging release gate remains FAIL pending subsequent fix promotion and live retest**.

---

### 🚨 ISSUE-054: E2E Evidence Overwrite Collision Risk During Multi-Run Live Staging Releases (UPA-1403)

#### 1. What Happened (Symptom):
During Phase 5 live Staging smoke testing and subsequent re-test attempts, executing Playwright runs posed an immediate risk of clobbering historical evidence manifests (`frontend/test-results/evidence-manifest.json` and `frontend/e2e-evidence/evidence-manifest.json`) and screenshots. If an operator ran a live smoke test, the hardcoded reporter paths unconditionally overwrote prior test results via `fs.writeFileSync`, preventing multi-run auditability and violating the owner's non-destructive evidence retention directive.

#### 2. Root Cause:
1. **Hardcoded Reporter Output Paths**: In `frontend/e2e/reporters/evidence-manifest-reporter.ts:172-183`, output directories were hardcoded to `process.cwd()/test-results` and `process.cwd()/e2e-evidence` without respecting custom output directory environment variables.
2. **Hardcoded Screenshot Destination**: In `frontend/e2e/helpers/evidence-tracker.ts:71`, `captureStepScreenshot` hardcoded `path.resolve(process.cwd(), 'test-results', 'screenshots')`.
3. **Hardcoded Playwright Configuration**: In `frontend/playwright.config.ts`, `outputFolder` for HTML reports was hardcoded to `'playwright-report'`, and `outputDir` was omitted (defaulting to `'test-results'`).

#### 3. Resolution (Code Changes):
1. **Dynamic Reporter Output Directories (`frontend/e2e/reporters/evidence-manifest-reporter.ts`)**:
   Updated the reporter to support `EVIDENCE_OUTPUT_DIR`, `DISABLE_SECONDARY_MANIFEST_WRITE`, `E2E_SECONDARY_EVIDENCE_DIR`, `EVIDENCE_MANIFEST_FILENAME`, and `PLAYWRIGHT_HTML_REPORT_DIR`. When `EVIDENCE_OUTPUT_DIR` is set, secondary writes to `e2e-evidence/` are suppressed unless explicitly requested, preserving historical records.
2. **Dynamic Screenshot Resolution (`frontend/e2e/helpers/evidence-tracker.ts`)**:
   Updated `captureStepScreenshot` to resolve destination directory against `process.env.EVIDENCE_OUTPUT_DIR || 'test-results'`.
3. **Configurable Playwright Output (`frontend/playwright.config.ts`)**:
   Configured `outputDir: process.env.EVIDENCE_OUTPUT_DIR || 'test-results'` and HTML reporter `outputFolder: process.env.PLAYWRIGHT_HTML_REPORT_DIR || 'playwright-report'`.
4. **Promotion Verifier Integration (`scripts/verify_promotion.py`)**:
   Updated `verify_evidence_manifest` to auto-detect `EVIDENCE_MANIFEST_PATH` and `EVIDENCE_OUTPUT_DIR`, with full backward compatibility fallback.
5. **Regression Unit Test Suites**:
   Created `frontend/src/lib/__tests__/evidenceIsolation.test.ts` (8 Vitest tests) and `tests/test_evidence_isolation.py` (6 pytest tests) without touching existing test files (Rule 1).

#### 4. Testing & Verification:
- **TypeScript Static Check**: `npx tsc --noEmit` -> **0 errors [MEASURED]**.
- **Frontend Vitest Suite**: `npm test` -> **70 passed in 2.17s [MEASURED]** (includes 8 isolation unit tests).
- **ESLint**: `npm run lint` -> **0 errors [MEASURED]**.
- **Next.js Production Build**: `npm run build` -> **Compiled successfully [MEASURED]**.
- **Backend Pytest Suite**: `pytest tests/` -> **405 passed in 49.61s [MEASURED]** (includes 6 isolation unit tests).
- **Status**: **Resolved on Dev (UPA-1403)**.

---

### 🚨 ISSUE-055: Remote Single-Branch CI Checkout Branch-Resolution Test Failure (UPA-1404)
- **Date**: 2026-10-20
- **Affected Files**: `tests/test_verify_promotion_manifest.py`
- **Related Tickets**: `UPA-1404`

#### 1. What Happened (Symptom):
During GitHub Actions CI execution for Dev commit `40df9f1f1a252df4010e97f2420d0f13e8ce5756` (workflow run `39403691187`), the backend pytest suite failed with 404 passed, 1 failed, 3 deselected:
```text
FAILED tests/test_verify_promotion_manifest.py::test_resolve_source_sha_resolves_branches - RuntimeError: Failed to resolve commit SHA for promotion source 'staging': fatal: ambiguous argument 'staging': unknown revision or path not in the working tree.
```
While local developer sandboxes with multiple local branch refs checked out had passed, the clean GitHub Actions environment (`actions/checkout` on `Dev`) performs a single-branch checkout where local branch `staging` does not exist, causing `git rev-parse staging` to fail closed with exit code 128.

#### 2. Root Cause:
`tests/test_verify_promotion_manifest.py::test_resolve_source_sha_resolves_branches` invoked `resolve_source_sha("staging")` without mocking `subprocess.run`. In `scripts/promote.py`, `resolve_source_sha` calls `git rev-parse <source>`. In automated CI runners where only the target branch (`Dev`) is checked out into the runner workspace, `git rev-parse staging` fails with `fatal: ambiguous argument 'staging'`, raising an unhandled `RuntimeError`.

#### 3. Resolution (Code Changes):
In `tests/test_verify_promotion_manifest.py`:
1. **Isolated Branch Resolution Test**:
   Updated `test_resolve_source_sha_resolves_branches(monkeypatch)` to mock `subprocess.run` via pytest's `monkeypatch` fixture. When `git rev-parse` is invoked for `"Dev"` or `"staging"`, it returns deterministic 40-character SHA mock responses (`mock_dev_sha` and `mock_staging_sha`) and asserts that the expected git commands were dispatched, decoupling the unit test from the external repository branch topology.
2. **Deterministic Failure Handling Test**:
   Added `test_resolve_source_sha_failure_raises_runtime_error(monkeypatch)` to explicitly verify the fail-closed error path: when `git rev-parse` returns a non-zero exit code (e.g. exit code 128 for an unknown branch), `resolve_source_sha` correctly raises `RuntimeError` containing the underlying stderr message.
3. **Preserved Production Code**:
   Preserved `scripts/promote.py` and `.github/workflows/ci.yml` untouched, maintaining the production branch resolver contract.

#### 4. Testing & Verification:
- **Focused Unit Tests**: `pytest tests/test_verify_promotion_manifest.py -v` -> **51 passed in 0.71s [MEASURED]**.
- **Backend Pytest Suite**: `pytest tests/` -> **406 passed, 3 deselected, 12 warnings in 49.54s [MEASURED]**.
- **Frontend Vitest Suite**: `npm test` -> **70/70 passed in 2.22s [MEASURED]**.
- **TypeScript Static Check**: `npx tsc --noEmit` -> **0 errors [MEASURED]**.
- **ESLint**: `npm run lint` -> **0 errors [MEASURED]**.
- **Next.js Production Build**: `npm run build` -> **Compiled successfully [MEASURED]**.
- **Full CI Pipeline**: `python scripts/ci_check.py` -> **Exit code 0 [MEASURED]**.
- **Syntax & Whitespace Check**: `git diff --check` -> **Exit code 0 [MEASURED]**.
- **Status**: **Resolved locally on Dev; Remote CI verification pending publication**.

---

### 🚨 ISSUE-056: Tier 2 Live Staging Extraction Cache-Hit Bypass & Worker Stage Validation Gap (UPA-1405)
- **Date**: 2026-10-20
- **Affected Files**: `frontend/e2e/specs/staging.live.e2e.ts`
- **Related Tickets**: `UPA-1405`

#### 1. What Happened (Symptom):
During live Staging release gate evaluation (`frontend/e2e/specs/staging.live.e2e.ts`), if the submitted target URL was already present in the database or Redis extraction cache (`is_cached: true`), the API immediately returned an HTTP 200 payload without queueing an asynchronous worker task. As a result, the live release gate evaluated to a false-green `PASS` without ever exercising `media_downloader.py`, the `yt-dlp` format selectors, or the Celery worker processing pipeline. Furthermore, status response polling did not correlate candidate events to the submitted `job_id`, accepted a terminal `completed` status without verifying intermediate stages, and un-sanitized diagnostic URLs risked logging query parameters or credentials.

#### 2. Root Cause:
`staging.live.e2e.ts` only checked for terminal HTTP 200 completion without asserting `is_cached: false` on the initial extraction POST. Because viral reels may be processed multiple times across different tests, a viral cache hit completely bypassed the downloader and background worker. Additionally, the response listener did not match candidate status events to the target `job_id`, meaning events from concurrent background tasks could satisfy the test, and terminal `completed` status was accepted even if no intermediate downloader or inference stage was observed.

#### 3. Resolution (Code Changes):
In `frontend/e2e/specs/staging.live.e2e.ts`:
1. **Cache-Miss Guard**:
   Enforced that the initial extraction POST must return HTTP 202 Accepted with `is_cached: false`, failing closed with an explicit `[UPA-1305 VALIDATION BLOCKED]` error if served from cache.
   ```typescript
   if (initialStatus === 200 || initialJson.is_cached === true) {
     throw new Error(
       `[UPA-1305 VALIDATION BLOCKED] Target URL "${sanitizedDisplayTargetUrl}" was served from viral cache (HTTP ${initialStatus}, is_cached: ${initialJson.is_cached}). ` +
       'A cached extraction bypasses media_downloader.py and cannot validate the UPA-1305 downloader fix. ' +
       'Please supply an uncached, permitted Instagram or TikTok URL via STAGING_TEST_URL.'
     );
   }
   ```
2. **Strict `job_id` Event Correlation**:
   Tracked candidate status polling responses strictly matching the path segment `/api/v1/extract/status/{job_id}` for `targetJobId`. Raised fail-closed errors on status response parse errors or conflicting body `job_id` values.
3. **Worker Stage Evidence Requirement**:
   Required that intermediate stages `downloading_media` or `multimodal_ai_inference` are observed during status polling. Explicitly excluded terminal `completed` status alone as proof of worker execution.
   ```typescript
   const hasWorkerStageEvidence =
     observedStages.has('downloading_media') ||
     observedStages.has('multimodal_ai_inference');
   expect(
     hasWorkerStageEvidence,
     `Real worker processing stage must be observed during background extraction polling for job "${targetJobId}" (expected "downloading_media" or "multimodal_ai_inference"). Observed stages: [${observedStageList.join(', ')}]`
   ).toBe(true);
   ```
4. **Diagnostic Sanitization & Bounded Teardown**:
   Sanitized URLs and error messages with `sanitizeUrl` and `sanitizeText`. Wrapped polling in a bounded 90s timeout with deterministic listener cleanup in an unskippable `finally:` block.

#### 4. Testing & Verification:
- **TypeScript Static Check**: `npx tsc --noEmit` -> **0 errors [MEASURED]**.
- **ESLint**: `npm run lint` -> **0 errors [MEASURED]**.
- **Frontend Vitest Suite**: `npm test` -> **70/70 passed in 2.35s [MEASURED]**.
- **Mocked Playwright E2E Suite**: `npm run test:e2e:mocked` -> **7/7 passed in 17.3s [MEASURED]**.
- **Next.js Production Build**: `npm run build` -> **Compiled successfully [MEASURED]**.
- **Backend Pytest Suite**: `pytest tests/` -> **406 passed, 3 deselected, 12 warnings in 48.53s [MEASURED]**.
- **Full CI Pipeline**: `python scripts/ci_check.py` -> **Exit code 0 [MEASURED]**.
- **Syntax & Whitespace Check**: `git diff --check` -> **Exit code 0 [MEASURED]**.
- **Status**: **Resolved locally on Dev; Live un-mocked staging extraction and remote CI pending next push**.

---

### 🚨 ISSUE-057: Supabase Data API Automatic Grant Deprecation & Migration Directory Parity Gap (UPA-1406)
- **Date**: 2026-10-21
- **Affected Files**: `backend/database/001_initial_schema.sql`, `backend/database/009_beta_telemetry_feed.sql`, `backend/database/010_telemetry_events.sql`, `backend/database/README.md`, `database/*.sql`, `tests/test_database_grants.py`, `tests/test_database_schema.py`, `scripts/ci_check.py`

#### 1. What Happened (Symptom):
Under an upcoming Supabase platform update taking effect on October 30, 2026, newly created tables in the `public` schema will no longer automatically receive default privileges (`GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated, service_role`). In fresh provisioning or disaster recovery rebuilds, PostgREST HTTP queries targeting `profiles`, `extractions`, `affiliate_clicks`, `beta_telemetry_feed`, or `telemetry_events` would fail with HTTP 404 (table hidden from API schema) or HTTP 42501 (`insufficient_privilege`). Additionally, migration directory drift existed between `backend/database/` and root `database/`, with root missing migrations `010`, `011`, and `012`.

#### 2. Root Cause:
1. `001_initial_schema.sql` relied on PostgreSQL default privileges and omitted explicit table-level grants for `service_role` and `anon`/`authenticated`.
2. `009_beta_telemetry_feed.sql` lacked explicit grants, leaving worker telemetry inserts vulnerable to permission denial.
3. `010_telemetry_events.sql` used an un-hardened `GRANT ALL ON public.telemetry_events TO service_role`, granting unnecessary privileges (`DROP`, `ALTER`, `DELETE`).
4. Root `database/` had not been maintained in sync with `backend/database/`, lacking migrations `010`, `011`, and `012`.
5. Rebuilding the database schema was not formally distinguished from data recovery, and Supabase Free-tier limits (2 project slots occupied by Production and Staging) were not documented in DR runbooks.

#### 3. Resolution (Code Changes):
1. **Explicit Least-Privilege Table Grants**:
   - In `001_initial_schema.sql`:
     ```sql
     GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;
     GRANT SELECT, UPDATE ON public.profiles TO service_role;
     GRANT SELECT, INSERT, DELETE ON public.extractions TO service_role;
     GRANT SELECT ON public.extractions TO anon, authenticated;
     GRANT SELECT, INSERT ON public.affiliate_clicks TO service_role;
     ```
   - In `009_beta_telemetry_feed.sql`:
     ```sql
     GRANT INSERT ON public.beta_telemetry_feed TO service_role;
     REVOKE ALL ON public.beta_telemetry_feed FROM anon, authenticated, PUBLIC;
     ```
   - In `010_telemetry_events.sql`:
     ```sql
     GRANT SELECT, INSERT ON public.telemetry_events TO service_role;
     REVOKE ALL ON public.telemetry_events FROM anon, authenticated, PUBLIC;
     ```
2. **Function Search-Path & Execution Hardening**:
   - Added explicit `SET search_path = public` to `increment_user_extraction_count`, `reset_daily_extraction_quotas`, and `handle_new_user`.
   - Narrowed execute revocations to reviewed functions (`REVOKE EXECUTE ... FROM PUBLIC; GRANT EXECUTE ... TO service_role`) to protect PostgreSQL built-ins (`uuid-ossp`, `pgcrypto`).
3. **Directory Parity**:
   - Mirrored all migrations and README from `backend/database/` to root `database/` with 100% byte parity.
4. **Automated Static CI Protection**:
   - Added `tests/test_database_grants.py` asserting table grants, directory parity, search-path protections, execute restrictions, and RLS across all 5 tables.
   - Added Step 5 to `scripts/ci_check.py` executing `test_database_grants.py`.

#### 4. Testing & Verification:
- **Focused Database Grant Suite**: `pytest tests/test_database_grants.py -v` -> **9/9 passed in 0.23s [MEASURED]**.
- **Database Schema Suite**: `pytest tests/test_database_schema.py -v` -> **7/7 passed in 0.22s [MEASURED]**.
- **Backend Pytest Suite**: `pytest tests/` -> **415 passed, 3 deselected in 48.91s [MEASURED]**.
- **Full CI Pipeline**: `python scripts/ci_check.py` -> **Exit code 0 [MEASURED]**.
- **Whitespace & Parity Check**: `git diff --check` -> **Exit code 0 [MEASURED]**.
- **Status**: **Resolved locally on Dev; Cloud databases remained 100% untouched**.

---

### 🚨 ISSUE-058: Supabase Free-Tier Project Dormancy Risk & Staging Keep-Alive Monitoring (UPA-1409)
- **Date**: 2026-10-21
- **Affected Files**: `scripts/staging_supabase_keep_alive.py`, `.github/workflows/staging_supabase_keep_alive.yml`, `tests/test_staging_supabase_keep_alive.py`

#### 1. What Happened (Symptom):
Under Supabase Free-Tier platform policies, projects that receive no database or PostgREST API traffic for 7 consecutive days are automatically placed into project dormancy ("paused" state). When dormant, all incoming API requests fail with HTTP 503 (`Project is paused`), rendering Staging Vercel previews, authentication, and E2E extraction gates completely inoperable until manually unpaused via the Supabase cloud dashboard.

Inspection of the repository's existing keep-alive implementation revealed that legacy `scripts/keep_alive.py` and `.github/workflows/keep_alive.yml` only executed HTTP `GET` requests against decommissioned Streamlit Community Cloud frontend URLs (`https://manas-recipe-extractor.streamlit.app/`, `https://universalpro-stage.streamlit.app/`) and did not touch Supabase or issue database queries. Consequently, existing keep-alive automation provided zero dormancy prevention for Supabase PostgreSQL.

#### 2. Root Cause:
Supabase dormancy detection tracks genuine PostgreSQL / PostgREST Data API transactions, not frontend pings or container `/health` probes. Low-frequency environments like Staging (which are exercised primarily during sprint release cycles) are exposed to dormancy whenever development sprints pause or testing is inactive for over a week.

#### 3. Resolution (Code Changes):
1. **Dedicated Staging Keep-Alive Probe Script (`scripts/staging_supabase_keep_alive.py`)**:
   - Implemented a lightweight, read-only PostgREST probe targeting `GET /rest/v1/extractions?select=id&limit=1` against `public.extractions`.
   - Reused existing table privileges: `anon` role was granted explicit `SELECT` on `public.extractions` in migration `011_privilege_hardening.sql`, enabling probes via `SUPABASE_STAGING_ANON_KEY` without requiring privileged `service_role` tokens.
   - Enforced strict hostname validation locked exclusively to `https://mzpkdmaxsuhwezsooidu.supabase.co`. Production URLs, localhost, and unexpected hostnames are rejected fail-closed before any HTTP request is issued.
   - Implemented finite 15-second request timeouts and safe structured logging that guarantees zero emission of API keys, bearer tokens, or database row contents in logs or results.
   - Treats both populated rows (`[{"id": "..."}]`) and empty results (`[]`) as successful database transactions, returning exit code 0 on success and 1 on error.
2. **Dedicated Staging GitHub Actions Workflow (`.github/workflows/staging_supabase_keep_alive.yml`)**:
   - Configured scheduled cron execution 3 times daily (`17 0,8,16 * * *`) and on-demand `workflow_dispatch`.
   - Granted least privilege (`permissions: contents: read`) with a 5-minute bounded job timeout.
   - Injected strictly Staging-scoped secrets: `SUPABASE_STAGING_URL` and `SUPABASE_STAGING_ANON_KEY`, preventing cross-environment credential leakage.
   - Preserved legacy Production keep-alive files 100% untouched.
3. **Operational Unpause Runbook (If Project Pauses)**:
   - If a Staging project enters dormancy before keep-alive is active:
     1. Operator navigates to `https://supabase.com/dashboard/project/mzpkdmaxsuhwezsooidu`.
     2. Clicks **"Restore project" / "Unpause project"**.
     3. Awaits project provisioning (~2-3 minutes).
     4. Runs the manual keep-alive probe via `gh workflow run staging_supabase_keep_alive.yml` or manual curl to verify HTTP 200 OK.
   - *Note on Free-Tier Guarantees*: The keep-alive probe generates ordinary database activity to reduce dormancy risk, but does not guarantee against platform-level pauses or serve as a backup/disaster-recovery mechanism.

#### 4. Testing & Verification:
- **Unit Test Suite**: `pytest tests/test_staging_supabase_keep_alive.py -v` -> **22/22 passed in 0.32s [MEASURED]**.
- **Full Backend Regression Suite**: `pytest tests/` -> **Clean pass**.
- **Full CI Pipeline**: `python scripts/ci_check.py` -> **Clean pass**.
- **Whitespace & Diff Check**: `git diff --check` -> **Exit code 0 [MEASURED]**.
- **Status**: **Resolved locally on Dev; Staging secret provisioning and live workflow execution pending owner authorization**.

---

## 📌 Standard Protocol for Logging Future Issues

Whenever a new bug or unexpected behavior occurs:
1. **Add an entry to the Table of Issues** with an incremented ID (`ISSUE-018`, etc.).
2. **Document the 4 Core Sections**:
   - **What Happened (Symptom)**
   - **Root Cause**
   - **Resolution (Exact Code Snippets)**
   - **Testing & Verification**
3. Keep language simple, concise, and accessible to any developer joining the project.
