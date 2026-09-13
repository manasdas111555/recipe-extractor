# Site Crawl & DOM Inventory — Universal Pro AI (Staging)

> **Target URL:** `https://universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app/`  
> **Protection Protocol:** Vercel Edge Protection Bypass (`_vercel_jwt` Cookie Enabled)  
> **Environment:** Staging (Layer 2)  
> **Crawled At:** 2026-09-13T20:30:00+05:30  

---

## 🧭 Page Structure & Interactive Element Map

### 1. Top Navigation Bar (`<header>`)
| Element | Selector / Type | ARIA / Label | Action / Target |
| :--- | :--- | :--- | :--- |
| **Brand Logo** | `div > Zap` | "UNIVERSAL PRO AI" | Top Brand Anchor |
| **FAQ & Guide** | `button.btn-ghost` | `<HelpCircle /> FAQ & Guide` | Smooth scrolls to `#faq-section` |
| **Intelligence Vault** | `button.btn-ghost` | `<BookOpen /> Intelligence Vault` | Opens `VaultLibrary.tsx` slide-out drawer |

---

### 2. Main Hero Ingestion Section (`<main>`)
| Element | Selector / Type | Description / Input Type | Target Action |
| :--- | :--- | :--- | :--- |
| **Superpower Badge** | `.badge-pill.badge-emerald` | "Sub-3s Universal AI • Multi-Genre Multimodal Engine" | Informational Hero Badge |
| **Hero Heading** | `h1` | "Universal Reel & Shorts AI Intelligence Extractor" | Main H1 Title |
| **Content Domain** | `select` | Dropdown Options (Auto-Detect, Cooking Recipe, Kitchen Finds, Fitness, Tech, Unboxing, Life Hacks) | Domain hint parameter `domain_hint` |
| **Media URL Input** | `input[type="text"]` | Placeholder: `Paste Instagram Reel, TikTok, or YouTube Short link...` | Media URL state binding |
| **Extract Intelligence** | `button.btn-emerald` | Icon: `<Sparkles /> Extract Intelligence` | Triggers `/api/v1/extract` POST endpoint |
| **Sample Quick Chips** | `button.chip-tactile` | 4 Quick Try Chips: `🍳 Steamed Egg Curry Reel`, `💻 Quick Python Tips Short`, `🛍️ Keyboard & Gadget Short`, `⚡ Viral Meme Short` | Auto-populates URL input |
| **Telegram Banner** | `a` | `Prefer Mobile? Extract directly on Telegram: @UniversalProAIBot` | External link to Telegram Bot |

---

### 3. Platform Superpowers Deck (`.glass-card`)
| Card Title | Icon | Description Summary |
| :--- | :--- | :--- |
| **Universal Stream Parsing** | `<Video />` | Demuxing Instagram Reels, YouTube Shorts, and TikTok with high-res auto-resolution. |
| **Multimodal Neural Vision** | `<Cpu />` | Simultaneous analysis of video frames, on-screen text, and voiceover audio. |
| **Shoppable Product Links** | `<ShoppingBag />` | Identifies cookware, fitness gear, gadgets & ingredients with instant 1-click buy tags. |
| **Instant WhatsApp Sync** | `<MessageSquare />` | Direct delivery of clean, formatted intelligence notes straight to your phone. |

---

### 4. Interactive FAQ & User Guide Section (`#faq-section`)
| Component | Elements / Selectors | Features & Controls |
| :--- | :--- | :--- |
| **Header Badge** | `.badge-pill` | `<HelpCircle /> User Guide & Knowledge Base` |
| **4-Step Quick Start Grid** | 4 Step Cards | `01 Copy Video Link`, `02 Sub-3s AI Analysis`, `03 1-Click Buy & Store Search`, `04 Export to WhatsApp & Vault` |
| **Category Filter Pills** | 5 Button Pills | `All Questions`, `🚀 Getting Started`, `✨ Features & Shopping`, `📱 Platforms`, `🛠️ Troubleshooting` |
| **Live FAQ Search Input** | `input[type="text"]` | Placeholder: `Search FAQs...` (Filters questions in real-time) |
| **Accordion Items** | 7 Accordion Cards | Collapsible questions with `<ChevronDown />` / `<ChevronUp />` toggles |

---

### 5. Slide-Out Intelligence Vault Library Drawer (`<VaultLibrary />`)
| Element | Selector / Type | Functionality |
| :--- | :--- | :--- |
| **Drawer Header** | `h2` | "Personal Recipe Vault" with count badge |
| **Close Button** | `button` | Closes slide-out modal |
| **Vault Search Input** | `input[type="text"]` | Filters saved extractions in browser localStorage |
| **Empty State** | `div` | "Pantry Empty" illustration when 0 items saved |

---

### 6. Interactive Extracted Result Card (`ExtractionResult`)
| Component | Details / Sub-elements | Action Controls |
| :--- | :--- | :--- |
| **Video Player Dock** | Single-docked `<video>` / `<iframe>` | Play/Pause, Duration, Quality Badge |
| **Serving Adjuster** | `-` / `+` Counter Controls | Portion math scaling (1–12 servings) |
| **1-Click Commerce Links** | Badges for Amazon, Flipkart, Blinkit, Zepto, Swiggy Instamart, BigBasket | Opens store query with affiliate tag `manasdas11155-21` & EarnKaro `r=5608766` |
| **Export Action Deck** | Buttons: `Send via WhatsApp`, `Download .txt`, `Copy Notes` | Formats structured text payload |
