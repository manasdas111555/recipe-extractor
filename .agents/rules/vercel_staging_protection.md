# 🛡️ Vercel Staging Environment Protection Bypass Rule

Whenever accessing, testing, or running QA crawlers/subagents against the Vercel Staging environment (Layer 2 Vercel Preview deployments), you MUST ALWAYS include both the protection bypass token AND the bypass cookie setter parameter:

```text
?x-vercel-protection-bypass=<secret>&x-vercel-set-bypass-cookie=samesitenone
```

## Key Requirements:
1. **Initial URL Navigation**: Append `?x-vercel-protection-bypass=<secret>&x-vercel-set-bypass-cookie=samesitenone` to the initial staging URL.
2. **Cookie Setting**: The `x-vercel-set-bypass-cookie=samesitenone` flag instructs Vercel Edge to set the `_vercel_jwt` cookie in the browser session.
3. **Downstream Assets & APIs**: Setting the cookie guarantees that all subsequent client-side `fetch` calls, Next.js dynamic script chunks, CSS assets, and API routes load past the protection wall without getting stuck on "Loading Universal Pro AI..." or returning 401 Unauthorized errors.
