# 📋 QA & UX Test Strategy Matrix — Universal Pro AI

**Test Run Identifier**: `QATest_20260915_214500`  
**Scope**: 6 Quality Dimensions + Multimodal End-to-End Test Suite  

---

## Quality Dimensions & Test Plan

| Dimension | Test Focus & Scenario | Verification Method | Status |
| :--- | :--- | :--- | :--- |
| **1. Happy Paths** | Extract valid Instagram Reels & YouTube Shorts across 6 genres (Cooking, Travel, Interior, Game Settings, Gadgets) | Multimodal AI Execution + DOM Result Verification | ✅ PASS |
| **2. Form Validation** | Submit empty URL, whitespace-only URL, or invalid domain string | Verify error message alert rendered (`Please paste a valid video URL...`) | ✅ PASS |
| **3. Edge Cases** | Rapid multi-clicking extract button, theme toggling during loading, modal dismissal via backdrop | Verify button disabled state, smooth theme transition, zero unhandled errors | ✅ PASS |
| **4. Responsive Viewports** | Audit viewports (`375x812` Mobile, `768x1024` Tablet, `1440x900` Desktop, `1920x1080` Ultrawide) | Verify stacked form inputs on mobile, zero horizontal scrollbar | ✅ PASS |
| **5. Error Handling** | API rate limit / quota exceeded (HTTP 429) & congested Gemini API failovers | Verify `UpgradeModal.tsx` trigger, automatic model fallback without user crash | ✅ PASS |
| **6. Accessibility & UX** | Minimalist UI audit, light/dark mode contrast, button touch targets (min 48px), visual hierarchy | Verify minimal layout (zero top SLA clutter, zero non-functional bot bar) | ✅ PASS |

---

## 6-Genre Multimodal Test Plan Matrix

| Test ID | Expected Category | Test Input URL | Required Extracted Artifacts |
| :--- | :--- | :--- | :--- |
| **E2E-01** | Cooking / Recipe | `https://www.instagram.com/reel/DaNI2wxx91z/...` | 3-Section formatting (Equipment, Ingredients + Qty, Instructions), recipe title, taste summary |
| **E2E-02** | Travel | `https://www.instagram.com/reel/DcJKd5uB_WB/...` | `TRAVEL_GUIDE` category, 1-click Google Maps links for itinerary spots |
| **E2E-03** | Interior Design | `https://www.instagram.com/reel/DYmrRU3i13d/...` | `INTERIOR_DESIGN` / 🏠 category, switchboard zones & electrical planning principles |
| **E2E-04** | Game Settings | `https://www.instagram.com/reel/DZ4A-YkOqe0/...` | `GAMING` / 🎮 category, AMD color temperature/saturation settings for Valorant |
| **E2E-05** | Gadget Short 1 | `https://youtube.com/shorts/30KMGj70mZM...` | `PRODUCT_FINDS` category, 3 gadgets under Rs. 50 with pros & cons |
| **E2E-06** | Gadget Short 2 | `https://youtube.com/shorts/IQtfcjqruy4...` | `PRODUCT_FINDS` category, Stream ingestion & model resilience fallback |
