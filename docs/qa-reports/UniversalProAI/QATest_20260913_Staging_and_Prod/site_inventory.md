# 🗺️ Site Inventory & DOM Component Mapping

**Project**: Universal Pro AI (`recipe-extractor`)  
**Audit Timestamp**: 2026-09-13 09:15:00 UTC  
**Target Environments**:
- **Staging**: `https://universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app/?x-vercel-protection-bypass=[REDACTED_BYPASS_TOKEN]`
- **Production**: `https://universal-pro-ai.vercel.app/`

---

## 1. Header Navigation Component
- `brand-logo`: Clickable logo linking to homepage (`/`). SVG icon with `#10B981` Emerald gradient fill.
- `btn-intelligence-vault`: Top-right sliding drawer trigger (`Intelligence Vault`). Opens glassmorphic side drawer containing saved extractions.

## 2. Hero Section & Intelligence Extractor Hub
- `hero-title`: Primary `H1` visual anchor: *"Universal Reel & Shorts AI Intelligence Extractor"* (`bg-clip-text text-transparent bg-gradient-to-r`).
- `select-domain-hint`: Dropdown selector for content categories:
  - 🍳 *Cooking Recipe & Food* (`recipe`)
  - 🏋️ *Fitness & Workout Routine* (`workout`)
  - 💻 *Software Code & Tech Tutorial* (`tech_diy`)
  - 🛍️ *E-Commerce Product Review & Viral Finds* (`unboxing`)
  - ⚡ *Auto Detect* (`auto`)
- `input-video-url`: Main URL input box (`https://www.youtube.com/shorts/...` or `https://www.instagram.com/reel/...`).
- `btn-extract-intelligence`: Primary CTA button (`Extract Intelligence` + right arrow icon).
- `container-sample-chips`: 1-Click sample preset buttons:
  - `🍳 Steamed Egg Curry Reel` (`https://www.instagram.com/reel/DdGvPs9zhVu/`)
  - `💻 Quick Python Tips Short` (`https://www.youtube.com/shorts/KrFDs2M_FSE`)
  - `🛍️ Keyboard & Gadget Short` (`https://www.youtube.com/shorts/J---aiyznGQ`)
  - `⚡ Viral Meme Short` (`https://www.youtube.com/shorts/fC7oUOUEEi4`)
- `badge-telegram-hero`: Mobile callout badge linking to Telegram bot (`@UniversalProAIBot`).

## 3. Telemetry & Loading Component
- `container-progress-bar`: Dynamic progress bar (0–100%) with linear smooth transition.
- `text-loading-phase`: Real-time phase indicator (`Ready`, `Ingesting Video Stream...`, `Multimodal Neural Reasoning...`).
- `container-error-alert`: Translucent error container (`setError(null)` auto-clears on new extraction start).

## 4. Platform Superpowers (Feature Grid)
- `card-stream-parsing`: "Universal Stream Parsing" (Instagram, YouTube Shorts, TikTok auto-resolution).
- `card-neural-vision`: "Multimodal Neural Vision" (Simultaneous frame, visual text, and audio transcript analysis).
- `card-product-links`: "Shoppable Product Links" (Cookware, fitness gear, gadgets with 1-click buy tags).
- `card-whatsapp-sync`: "Instant WhatsApp Sync" (Direct 1-click delivery of clean formatted notes).

## 5. Footer Feature Pills Component
- `pill-turnaround`: `⚡ ~2.4s AI TURNAROUND`
- `pill-affiliate`: `🛍️ AMAZON AND FLIPKART LINK`
- `pill-whatsapp`: `📱 1-CLICK WHATSAPP SHARE`
