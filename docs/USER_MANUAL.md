# 📘 Universal Pro AI — Comprehensive User Manual & Feature Guide

Welcome to the **Universal Pro AI** User Manual. This guide explains what features the app provides and how to use them step-by-step.

---

## 📋 Table of Contents

1. [Quick Start & Video Ingestion](#1-quick-start--video-ingestion)
2. [Extraction Card Output & Dual-Language Notes](#2-extraction-card-output--dual-language-notes)
3. [Interactive Hands-Free Cooking Mode](#3-interactive-hands-free-cooking-mode)
4. [Dynamic Recipe Servings Adjuster](#4-dynamic-recipe-servings-adjuster)
5. [10-Minute Quick Commerce & 1-Click Buying](#5-10-minute-quick-commerce--1-click-buying)
6. [Intelligence Vault & Local Library](#6-intelligence-vault--local-library)
7. [WhatsApp & Telegram Integration](#7-whatsapp--telegram-integration)

---

## 1. Quick Start & Video Ingestion

Universal Pro AI converts social media video links into structured recipe cards, workout routines, product reviews, and educational notes.

### How to Use:
1. **Copy Video URL**: Copy any public link from **YouTube Shorts**, **Instagram Reels**, **TikTok**, or **Facebook Reels**.
2. **Paste Link**: Paste the URL into the main search bar at the top of the app dashboard.
3. **Select Category (Optional)**: Leave on `Auto-Detect (Universal AI)` or pick a specific category:
   - 🍳 *Cooking Recipe & Food*
   - 🛍️ *Kitchen Finds & Home Gadgets*
   - 🏋️ *Fitness & Workout Routine*
   - 💻 *Tech Tutorial & Code Guide*
   - 📦 *Product Unboxing & Amazon Finds*
   - ✈️ *Travel Guide & Itinerary*
4. **Click "Extract Anything"**: The app processes your video link and displays your interactive result card.

---

## 2. Extraction Card Output & Dual-Language Notes

Once extracted, your result card provides the following interactive sections:

- **Docked Media Player**: Watch the source reel or video side-by-side with structured steps.
- **3-Section Recipe View**:
  - **Section I**: Equipment & Cookware Needed.
  - **Section II**: Ingredients with scaled quantities.
  - **Section III**: Step-by-Step Cooking Instructions.
- **Dual-Language Toggle**: Switch between English translation and native spoken language notes.
- **Interactive Travel Maps**: Open interactive directions for featured travel locations on Google Maps.
- **Domain Primary Action Hierarchy**: Render exactly 1 primary call-to-action tailored to the result domain (*"Shop ingredients"* for Recipes, *"Open in Google Maps"* for Travel, *"Buy"* for Products, *"Open resources"* for Tutorials).
- **Accessible Mobile Overflow Bottom Sheet**: On mobile viewports (<768px), secondary actions and utilities (Export Markdown, Export Text, Copy Link, Save to Vault) are cleanly grouped inside a WCAG 2.2 compliant bottom sheet modal (`role="dialog"`, `aria-modal="true"`, focus trapping, `Escape` key close).
- **Vault Re-hydration**: Opening saved items from local storage automatically re-hydrates missing store links via `/api/v1/library/rehydrate` so buy buttons and quick commerce links appear instantly without client-side affiliate tags.

---

## 3. Interactive Hands-Free Cooking Mode

Designed for active cooking in the kitchen without needing to touch mobile screens with messy hands.

### How to Use:
- **Launch Cooking Mode**: Click **"Start Cooking Mode"** on any recipe card or tap a shared cooking mode link from WhatsApp/Telegram.
- **Screen Wake Lock**: Automatically keeps mobile displays awake so your screen doesn't dim or turn off while cooking.
- **High-Contrast Text**: Large typography designed for reading from a distance across the kitchen counter.
- **Step Countdown Timers**: Timed step countdowns with 1-click controls (**Play**, **Pause**, **Reset**) and audio completion chimes.
- **Voice Command Control**: Turn on **Voice Mode** to navigate hands-free:
  - Say `"Next"` or `"Forward"` to advance to the next step.
  - Say `"Back"` or `"Previous"` to return to the previous step.
  - Say `"Start"` or `"Timer"` to start a step timer.
  - Say `"Pause"` or `"Stop"` to pause a timer.
- **Keyboard & Touch Navigation**: Press `→` / `Space` for next step, `←` for previous step, `Esc` to close, or swipe left/right on touchscreens.
- **Ingredients Slide Checklist**: Slide open the ingredients checklist to tick off items as you cook.

---

## 4. Dynamic Recipe Servings Adjuster

Adjust ingredient quantities for different portion sizes.

### How to Use:
- **Adjust Servings**: Click `+` or `-` to scale servings from **1 to 12 people**. Ingredient amounts recalculate automatically.
- **Clean Fraction Display**: Displays kitchen measurements in clean fractions (`½`, `¼`, `¾`, `⅓`, `⅔`).
- **Native Measurement Units**: Preserves traditional unit names and metrics (e.g. `1 katori (~150g)` scaled 2x → `2 katori (~300g)`).
- **Exclude Pantry Staples**: Check "Exclude Pantry Staples" to hide common household items (Salt, Water, Oil) from shopping lists.
- **Copy Ingredients**: Click **"Copy Notes"** to copy the formatted ingredient list to your clipboard.

---

## 5. 10-Minute Quick Commerce & 1-Click Buying

Order missing recipe ingredients or featured products in 1 click.

### How to Use:
- **10-Minute Grocery Delivery (Recipes & Food)**:
  - 🟡 **Blinkit**: Click Blinkit badges to open pre-filled ingredient cart searches for instant delivery.
  - ⚡ **Zepto**: Click Zepto badges for quick-commerce delivery.
  - 🛵 **Swiggy Instamart**: Click Swiggy Instamart badges for instant grocery shopping.
  - 📦 **BigBasket & JioMart**: Click BigBasket badges for bulk grocery ordering.
- **Online Shopping Marketplaces**:
  - 🛒 **Amazon India**: Click Amazon badges to purchase cookware, appliances, or ingredients.
  - ⚡ **Flipkart**: Click Flipkart badges to find kitchen equipment or tech gadgets.

---

## 6. Intelligence Vault & Local Library

Save and organize your extractions across all video categories.

### How to Use:
- **Multi-Category Vault**: Browse saved extractions for **Recipes**, **Travel Guides**, **Workouts**, **Product Finds**, and **Tutorials**.
- **Category Filters & Custom Actions**: Filter saved cards by category or click direct action buttons (*"Open Travel Guide ↗"*, *"Open Workout View ↗"*, *"Open Tutorial ↗"*).
- **Bookmark & Save**: Click **"Save to Vault"** on any card to store it in your browser library for offline access anytime.

---

## 7. WhatsApp & Telegram Integration

### How to Use:
- **WhatsApp Notes**: Click **"WhatsApp Notes"** on any card or enter a mobile phone number to receive formatted notes and shopping links on WhatsApp.
- **Telegram Bot (`@UniversalProAIBot`)**: Forward video links directly to our Telegram bot to receive structured markdown cards and tap **"Start Cooking Mode"** to launch the interactive viewer.
