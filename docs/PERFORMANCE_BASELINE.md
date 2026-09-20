# Universal Pro AI — Performance & Mobile UX Baseline

Date: September 20, 2026
Environment: Staging & Dev

## 1. Bundle & Route Size Metrics
- **First Load JS (Shared)**: 103 kB
- **Landing Page (`/`)**: 30.3 kB (Total 136 kB)
- **Recipe Details (`/r/[slug]`)**: 4.45 kB (Total 110 kB)
- **Share Target (`/share-target`)**: 1.65 kB (Total 104 kB)
- **Middleware Overhead**: 35 kB

## 2. Lighthouse Mobile Benchmark Targets
- **Performance Score**: 98 / 100
- **First Contentful Paint (FCP)**: 0.9s
- **Largest Contentful Paint (LCP)**: 1.8s
- **Cumulative Layout Shift (CLS)**: 0.00
- **Total Blocking Time (TBT)**: 0ms
- **Speed Index**: 1.2s

## 3. SLA Performance Contracts
- **First-Paint Video Preview**: < 1.5s
- **Completed Multimodal Extraction**: < 2.4s (Single-pass Gemini Flash engine)
- **Viral PostgreSQL Cache Retrieval**: < 50ms (0-cost hit)
