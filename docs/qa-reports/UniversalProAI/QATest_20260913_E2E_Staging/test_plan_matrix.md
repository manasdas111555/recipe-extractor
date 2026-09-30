# Comprehensive QA & UX Test Strategy Matrix (Staging)

> **Target Application:** Universal Pro AI (Vercel Staging Deployment)  
> **Test Suite Run:** `QATest_20260913_E2E_Staging`  
> **Coverage:** 6 Quality Dimensions across Desktop & Mobile Viewports  

---

## 🎯 Quality Dimension Test Matrix

| # | Dimension | Test Focus & Scenario | Target Element / Route | Expected Outcome | Status |
|---|---|---|---|---|:---:|
| **1** | **Happy Paths** | Hero Landing & Navigation | Top Nav / Hero | Glassmorphism UI renders cleanly, header buttons active | ✅ PASS |
| **2** | **Happy Paths** | Smooth-Scroll Navigation | `FAQ & Guide` Button | Page smooth-scrolls down to `#faq-section` container | ✅ PASS |
| **3** | **Happy Paths** | Interactive FAQ Filter Pills | Category Pills | FAQ items filter dynamically based on selected category | ✅ PASS |
| **4** | **Happy Paths** | Real-Time FAQ Keyword Search | FAQ Search Input | Typing "Blinkit" or "WhatsApp" isolates matching questions | ✅ PASS |
| **5** | **Happy Paths** | Accordion Expand / Collapse | FAQ Accordion Card | Clicking accordion toggles answer visibility & chevron icon | ✅ PASS |
| **6** | **Form Validation** | Empty Form Submission | Primary Search Box | Error banner appears stating "Please paste a valid video URL" | ✅ PASS |
| **7** | **Form Validation** | Quick Try Sample Selection | Sample Chip Buttons | Input field auto-fills with sample URL | ✅ PASS |
| **8** | **Edge Cases** | Multimodal Domain Hint Override | Category Dropdown | Domain hint parameter `domain_hint` correctly passed to backend | ✅ PASS |
| **9** | **Live End-to-End** | Full Recipe Extraction Pipeline | `Extract Intelligence` | Real-time progress bar advances to 100%, renders result card | ✅ PASS |
| **10** | **Live End-to-End** | Single-Docked Media Preview | Video Player | Single player docked without duplicate audio streams | ✅ PASS |
| **11** | **Live End-to-End** | 1-Click Buy & Quick-Commerce | E-Commerce Badges | Links contain Amazon `tag=manasdas11155-21` & EarnKaro `r=5608766` | ✅ PASS |
| **12** | **Live End-to-End** | WhatsApp Export Formatter | WhatsApp Button | Generates structured markdown text with store deep links | ✅ PASS |
| **13** | **Live End-to-End** | Intelligence Vault Drawer | Vault Header Button | Slide-out drawer opens, search input & empty state render | ✅ PASS |
| **14** | **Responsive UX** | Mobile Viewport (`375x812`) | Full Page Layout | Zero horizontal overflow, tap targets >44px, text legible | ✅ PASS |
| **15** | **Security & Auth** | Vercel Edge Bypass Cookie | HTTP Request Headers | `_vercel_jwt` cookie set via query params, bypasses edge lock | ✅ PASS |
