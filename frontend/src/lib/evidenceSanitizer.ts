/**
 * Universal Pro AI - Evidence Data Sanitizer
 * Redacts secrets, tokens, API keys, passwords, and sensitive headers from E2E test artifacts.
 *
 * BINARY ARTIFACT POLICY:
 * Video recordings (.webm/.mp4) and Playwright trace archives (trace.zip) are binary formats
 * that cannot be text-sanitized reliably in post-processing.
 * Safe Handling Policy:
 * 1. Test specifications must NEVER input real secrets, passwords, or live tokens in UI interactions.
 * 2. Binary artifacts are strictly ignored from Git tracking (.gitignore) to prevent accidental commit.
 * 3. Only the machine-readable manifest (evidence-manifest.json), console logs, and text annotations
 *    are audited for promotion gates, and they are aggressively sanitized via this engine.
 */

const SECRET_PARAM_REGEX = /((?:[?&]|\b)(?:token|secret|key|api_key|api-key|password|passwd|x-vercel-protection-bypass|bypass_token|access_token|refresh_token|auth|client_secret)=)([^&\s]+)/gi;
const BASIC_AUTH_REGEX = /((?:Authorization|Proxy-Authorization):\s*Basic\s+)[^\s\r\n]+/gi;
const BEARER_AUTH_REGEX = /((?:Authorization|Proxy-Authorization):\s*Bearer\s+|Bearer\s+)[A-Za-z0-9_.-]+/gi;
const JWT_TOKEN_REGEX = /eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+/g;
const VERCEL_BYPASS_HEADER_REGEX = /(x-vercel-protection-bypass[\s:=]+)[A-Za-z0-9_-]+/gi;
const VERCEL_JWT_COOKIE_REGEX = /(_vercel_jwt[\s:=]+)[A-Za-z0-9_.-]+/gi;
const GENERIC_API_KEY_REGEX = /(sk-proj-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{20,}|sbp_[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AIzaSy[A-Za-z0-9_-]{33})/g;

/**
 * Sanitize a string by replacing credentials and tokens with redaction tags.
 */
export function sanitizeText(input: string): string {
  if (!input || typeof input !== 'string') return input;
  return input
    .replace(SECRET_PARAM_REGEX, '$1[REDACTED]')
    .replace(BASIC_AUTH_REGEX, '$1[REDACTED_CREDENTIAL]')
    .replace(BEARER_AUTH_REGEX, '$1[REDACTED_TOKEN]')
    .replace(JWT_TOKEN_REGEX, '[REDACTED_JWT]')
    .replace(VERCEL_BYPASS_HEADER_REGEX, '$1[REDACTED]')
    .replace(VERCEL_JWT_COOKIE_REGEX, '$1[REDACTED]')
    .replace(GENERIC_API_KEY_REGEX, '[REDACTED_API_KEY]');
}

/**
 * Sanitize a URL to strip basic auth and query parameters containing sensitive tokens.
 */
export function sanitizeUrl(rawUrl: string): string {
  if (!rawUrl || typeof rawUrl !== 'string') return rawUrl;
  try {
    const parsed = new URL(rawUrl, 'http://localhost');

    // Redact basic auth username/password in URL authority
    if (parsed.username || parsed.password) {
      parsed.username = 'REDACTED_USER';
      parsed.password = 'REDACTED_PASS';
    }

    const sensitiveKeys = [
      'token', 'secret', 'key', 'api_key', 'api-key', 'password', 'passwd',
      'x-vercel-protection-bypass', 'bypass_token', 'access_token', 'refresh_token',
      'auth', 'client_secret',
    ];

    for (const key of sensitiveKeys) {
      if (parsed.searchParams.has(key)) {
        parsed.searchParams.set(key, '[REDACTED]');
      }
    }

    // Return relative or full URL based on input
    if (rawUrl.startsWith('http://') || rawUrl.startsWith('https://')) {
      return parsed.toString();
    }
    return parsed.pathname + parsed.search + parsed.hash;
  } catch {
    return sanitizeText(rawUrl);
  }
}

/**
 * Recursively sanitize objects, arrays, and nested string values.
 */
export function sanitizeObject<T>(value: T): T {
  if (value === null || value === undefined) return value;
  if (typeof value === 'string') {
    return sanitizeText(value) as unknown as T;
  }
  if (Array.isArray(value)) {
    return value.map((item) => sanitizeObject(item)) as unknown as T;
  }
  if (typeof value === 'object') {
    const result: Record<string, any> = {};
    for (const [k, v] of Object.entries(value)) {
      const lowerKey = k.toLowerCase();
      if (
        lowerKey.includes('secret') ||
        lowerKey.includes('token') ||
        lowerKey.includes('password') ||
        lowerKey.includes('passwd') ||
        lowerKey.includes('authorization') ||
        lowerKey.includes('bypass') ||
        lowerKey.includes('key') ||
        lowerKey.includes('credential') ||
        lowerKey.includes('cookie') ||
        lowerKey.includes('auth')
      ) {
        result[k] = '[REDACTED]';
      } else {
        result[k] = sanitizeObject(v);
      }
    }
    return result as T;
  }
  return value;
}

/**
 * Authoritative Layer 2 Staging Origin Allowlist
 * Derived directly from repository governance documentation (STAGING_GATE_9_E2E_VERIFICATION.md,
 * PO_FINAL_PRODUCTION_GATE_DIRECTIVE.md, JIRA_BACKLOG.md, and TROUBLESHOOTING.md).
 */
export const EXACT_APPROVED_STAGING_ORIGINS = new Set([
  'https://universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app',
]);

/**
 * Validates whether a target URL is an exact approved Layer 2 Staging origin,
 * explicitly refusing Production, lookalikes, insecure HTTP, and unapproved previews.
 */
export function validateStagingOrigin(rawUrl: string): { isValid: boolean; error?: string } {
  try {
    const parsed = new URL(rawUrl);
    if (parsed.protocol !== 'https:') {
      return { isValid: false, error: `Staging origin must use HTTPS: "${rawUrl}"` };
    }
    const host = parsed.hostname.toLowerCase();
    if (
      host === 'universal-pro-ai.vercel.app' ||
      host === 'universal-pro.ai' ||
      host.endsWith('.universal-pro.ai')
    ) {
      return {
        isValid: false,
        error: `Target origin "${host}" is PRODUCTION. Rule 2 strictly forbids live testing against Layer 3 Production.`,
      };
    }
    if (!EXACT_APPROVED_STAGING_ORIGINS.has(parsed.origin)) {
      return {
        isValid: false,
        error: `Target origin "${parsed.origin}" is not an exact approved Layer 2 Staging host.`,
      };
    }
    return { isValid: true };
  } catch (e: any) {
    return { isValid: false, error: `Malformed URL: ${e?.message || rawUrl}` };
  }
}
