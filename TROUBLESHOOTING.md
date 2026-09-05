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

## 📌 Standard Protocol for Logging Future Issues

Whenever a new bug or unexpected behavior occurs:
1. **Add an entry to the Table of Issues** with an incremented ID (`ISSUE-008`, `ISSUE-009`, etc.).
2. **Document the 4 Core Sections**:
   - **What Happened (Symptom)**
   - **Root Cause**
   - **Resolution (Exact Code Snippets)**
   - **Testing & Verification**
3. Keep language simple, concise, and accessible to any developer joining the project.
