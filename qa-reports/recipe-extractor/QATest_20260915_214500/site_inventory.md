# 🗺️ Site Inventory & Component Map — Universal Pro AI

**Target Domain**: `https://universal-pro-ai.vercel.app` (Universal Reel & Shorts AI Extractor)  
**Test Date**: September 15, 2026  
**Environment**: Production & Staging (Vercel Edge Network)  

---

## 1. Page Routes & Structural Components

| Route / Component | Selector / Element ID | Purpose | Interactivity |
| :--- | :--- | :--- | :--- |
| **Header Bar** | `<header>` | Sticky top navbar | Logo, Theme Toggle (`Dark Mode` / `Light Mode`), FAQ Button, Vault Button |
| **Hero Title** | `<h1>` | Main headline | Static typography ("Universal Reel & Shorts AI Intelligence Extractor") |
| **Hero Subtitle** | `<p>` | Concise tagline | Static typography ("Instant AI extraction for recipes, travel, gadgets, interior, gaming & shorts.") |
| **Search Container** | `.main-search-input-container` | Main extraction input | Full-width responsive input field with inline domain hint & submit button |
| **URL Input Field** | `<input type="text">` | Video link entry | Value binding (`url`), `onKeyDown` Enter trigger, placeholder text |
| **Domain Selector** | `<select>` | Domain classification hint | 9 options (`Auto-Detect`, `Recipe`, `Kitchen Finds`, `Fitness`, `Interior`, `Gaming`, `Tech`, `Unboxing`, `Life Hacks`) |
| **Submit Button** | `<button class="btn-emerald">` | Trigger extraction | Disables when loading or URL empty; displays spinner & "Extract Intelligence" |
| **Sample Chips** | `.chip-tactile` buttons | Quick test links | 4 sample URLs across Cooking, Tech, Unboxing, and Viral Meme |
| **Progress Track** | `.shimmer-card` | Live status bar | Displays phase (`loadingPhase`), percentage bar (`loadingProgress`), and subtext |
| **Result Dashboard** | `div` (Grid) | Extraction output | 2-column layout: Single-docked media player (left), Structured Intelligence card (right) |
| **Media Player** | `<video>` / `<iframe>` | Video stream preview | Single-docked HTML5 video / Instagram / YouTube Shorts embed preview |
| **3-Section Recipe Card**| Section containers | Recipe formatting | Section I (Equipment), Section II (Ingredients + Qty), Section III (Instructions) |
| **Google Maps Card** | Card container | Travel locations | Displays locations with 1-click Google Maps search URLs |
| **Buy Links Shelf** | Shoppable buttons | Commercial links | Amazon, Flipkart, Blinkit, Swiggy Instamart, Zepto |
| **Action Bar** | Card header buttons | Result operations | `[ 🌐 Dual Language ]`, `[ 💬 WhatsApp Share ]`, `[ 📥 Download .txt ]`, `[ 💾 Save to Vault ]` |
| **FAQ Modal Drawer** | `<FaqSection />` | User Guide & FAQ | Slide-out overlay drawer triggered by header `[ FAQ & Guide ]` button |
| **Vault Drawer** | `<VaultLibrary />` | Saved intelligence | Slide-out library list triggered by header `[ Intelligence Vault ]` button |

---

## 2. Interactive Selector Map

```json
{
  "theme_toggle": "button[title*='Switch to']",
  "faq_guide_btn": "button:has-text('FAQ & Guide')",
  "vault_btn": "button:has-text('Intelligence Vault')",
  "url_input": "input[placeholder*='Paste Instagram Reel']",
  "domain_select": "select[title='Content Domain Classifier']",
  "extract_btn": "button:has-text('Extract Intelligence')",
  "sample_chips": "button:has-text('Try samples:') ~ button",
  "save_vault_btn": "button:has-text('Save to Vault')",
  "download_txt_btn": "button:has-text('Download')",
  "whatsapp_share_btn": "button:has-text('WhatsApp')"
}
```
