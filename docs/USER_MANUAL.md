# 📘 Universal Pro AI — Comprehensive User Manual & Feature Guide

Welcome to the **Universal Pro AI** User Manual. This living guide explains how to use all end-to-end features of the application, including AI video extraction, interactive hands-free cooking mode, dynamic recipe yield scaling, 10-minute quick commerce delivery, and omnichannel chatbot integration.

---

## 📋 Table of Contents

1. [Quick Start & Video Ingestion](#1-quick-start--video-ingestion)
2. [Multimodal Intelligence Output & Dual-Language Notes](#2-multimodal-intelligence-output--dual-language-notes)
3. [Interactive Hands-Free Cooking Mode](#3-interactive-hands-free-cooking-mode)
4. [Dynamic Smart Recipe Scaling Engine](#4-dynamic-smart-recipe-scaling-engine)
5. [10-Minute Quick Commerce & 1-Click Buying](#5-10-minute-quick-commerce--1-click-buying)
6. [Intelligence Vault & Local Library](#6-intelligence-vault--local-library)
7. [Omnichannel WhatsApp & Telegram Integration](#7-omnichannel-whatsapp--telegram-integration)

---

## 1. Quick Start & Video Ingestion

Universal Pro AI extracts structured recipes, workout routines, product reviews, and educational notes from short-form videos in under 2.4 seconds.

### Steps to Extract:
1. **Copy Video URL**: Copy any public link from **YouTube Shorts**, **Instagram Reels**, **TikTok**, or **Facebook Reels**.
2. **Paste & Ingest**: Paste the URL into the main input bar at the top of the dashboard.
3. **Select Domain (Optional)**: Leave on `Auto-Detect (Universal AI)` or select a specific domain:
   - 🍳 *Cooking Recipe & Food*
   - 🛍️ *Kitchen Finds & Home Gadgets*
   - 🏋️ *Fitness & Workout Routine*
   - 💻 *Tech Tutorial & Code Guide*
   - 📦 *Product Unboxing & Amazon Finds*
   - ✈️ *Travel Guide & Itinerary*
4. **Click "Extract Intelligence"**: The system processes video frames and audio transcripts to render structured output.

---

## 2. Multimodal Intelligence Output & Dual-Language Notes

Once processed, the extraction deck displays:

- **Single-Docked Media Player**: Watch the source reel or video directly alongside structured steps.
- **3-Section Recipe Hierarchy**:
  - **Section I**: Equipment Needed (e.g. `a. Non-stick skillet`, `b. Chef knife`).
  - **Section II**: Ingredients with exact quantities.
  - **Section III**: Chronological Step-by-Step Instructions.
- **Dual-Language Toggle**: Switch between English translation and native reel spoken language (e.g. Hindi, Hinglish, Tamil, Spanish).
- **Travel Maps Integration**: Interactive Google Maps directions for featured travel locations.

---

## 3. Interactive Hands-Free Cooking Mode

Designed for active cooking in the kitchen without touching mobile screens with messy hands.

### Key Capabilities:
- **Deep-Link Auto Launch**: Open any link with `?mode=cook` (from WhatsApp or Telegram) to launch cooking mode immediately.
- **Screen Wake Lock**: Automatically prevents mobile displays from dimming or going to sleep (`useWakeLock`).
- **High-Contrast Text**: Large, legible step text designed for reading from a distance.
- **Inline Audio Step Timers**: Automatic duration detection with 1-click timer controls (`Play`, `Pause`, `Reset`) and Web Audio completion chimes.
- **Voice Command Navigation**: Toggle **Voice Mode** to navigate hands-free:
  - Say `"Next"` or `"Forward"` $\rightarrow$ Advances to next step.
  - Say `"Back"` or `"Previous"` $\rightarrow$ Returns to previous step.
  - Say `"Start"` or `"Timer"` $\rightarrow$ Starts step countdown timer.
  - Say `"Pause"` or `"Stop"` $\rightarrow$ Pauses timer.
- **Keyboard & Swipe Gestures**: Press `→` / `Space` for next step, `←` for previous step, `Esc` to close, or swipe left/right on touchscreens.
- **Slide-over Ingredients Checklist**: Slide open the ingredients panel to tick off items in real-time.

---

## 4. Dynamic Smart Recipe Scaling Engine

Scale ingredient quantities dynamically for 1 to 12 servings.

### Key Capabilities:
- **Yield Servings Adjuster**: Click `+` or `-` to scale servings from **1 to 12 people** with instant automatic quantity recalculation.
- **Smart Fraction Formatting**: Displays exact kitchen measurements as clean unicode fractions (`½`, `¼`, `¾`, `⅓`, `⅔`).
- **Native Term Protection (Rule 13)**: Preserves native ingredient names and parenthetical metrics (e.g. `1 katori (~150g)` scaled 2x $\rightarrow$ `2 katori (~300g)`).
- **Pantry Staples Exclusion**: Click to exclude common pantry items (Salt, Water, Oil) from scaled shopping lists.
- **1-Click Copy**: Copy formatted scaled ingredient lists directly to your clipboard.

---

## 5. 10-Minute Quick Commerce & 1-Click Buying

Instantly purchase missing ingredients or featured cookware.

### E-Commerce & Quick Commerce Partners:
- **10-Minute Delivery (Recipes & Food)**:
  - 🟡 **Blinkit**: Direct search cart links for instant 10-minute grocery delivery.
  - ⚡ **Zepto**: Instant grocery delivery search deep links.
  - 🛵 **Swiggy Instamart**: Quick grocery cart integration.
  - 📦 **JioMart & BigBasket**: Bulk grocery shopping links.
- **E-Commerce & Marketplaces**:
  - 🛒 **Amazon India**: Cookware, appliances, and ingredients.
  - ⚡ **Flipkart**: Kitchen equipment and tech gadgets.
  - 👗 **Myntra, Meesho, AJIO, Nykaa**: Suppressed for food recipes; active for fashion & beauty extractions.

---

## 6. Intelligence Vault & Local Library

- **Auto-Save**: Extracted recipes are saved locally in your browser's **Intelligence Vault** (`upa_vault_items`).
- **Offline Access**: View past extractions, copy notes, or adjust servings even without an active internet connection.
- **Bookmark Toggle**: Click **"Save to Vault"** on any extraction card to bookmark or remove items.

---

## 7. Omnichannel WhatsApp & Telegram Integration

### WhatsApp Dispatch:
- Click **"WhatsApp Notes"** or enter a mobile phone number to receive clean, formatted WhatsApp notes containing summary, top ingredients, step summary, and quick delivery links.

### Telegram Bot (`@UniversalProAIBot`):
- Forward any reel or shorts link to the Telegram bot to receive instant structured markdown notes.
- Click **"🧑‍🍳 Start Cooking Mode"** inline button to open the web app directly in cooking mode.
