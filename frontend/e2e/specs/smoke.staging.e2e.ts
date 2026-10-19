import { test, expect } from '@playwright/test';
import { EvidenceTracker } from '../helpers/evidence-tracker';
import { validateStagingOrigin, sanitizeUrl } from '../../src/lib/evidenceSanitizer';

/**
 * Universal Pro AI - Live Staging Browser Smoke Test [LIVE]
 * ==========================================================
 * STRICT GOVERNANCE CONSTRAINTS:
 * 1. This suite is EXCLUSIVELY for execution against Layer 2 (Staging) after deployment.
 * 2. It must NEVER run in local Dev or without ALLOW_LIVE_STAGING_SMOKE=true.
 * 3. Non-destructive smoke verification: loads UI, verifies boot, controls, hero CTA, and single docked player.
 * 4. It does not perform media extraction or proxy downloads.
 */

/**
 * Resolves the authoritative backend API origin for Staging HTTP error monitoring.
 * Uses STAGING_API_URL if configured, falling back to documented OCI Staging VM (http://129.225.86.241).
 */
export function resolveStagingApiOrigin(stagingApiUrl?: string): string {
  const raw = stagingApiUrl || process.env.STAGING_API_URL || 'http://129.225.86.241';
  try {
    return new URL(raw).origin;
  } catch {
    return raw.replace(/\/$/, '');
  }
}

/**
 * Determines whether a response URL belongs to the monitored application scope:
 * 1. Relative paths (/...)
 * 2. Vercel Staging Frontend base URL
 * 3. OCI Staging Backend API origin
 */
export function isMonitoredHttpErrorUrl(
  url: string,
  stagingBaseUrl: string,
  stagingApiOrigin: string
): boolean {
  if (!url || typeof url !== 'string') return false;
  if (url.startsWith('/')) return true;
  if (stagingBaseUrl && url.startsWith(stagingBaseUrl)) return true;
  if (stagingApiOrigin && url.startsWith(stagingApiOrigin)) return true;
  return false;
}

/**
 * Validates the page.goto() navigation response, failing closed if response is null or non-200.
 */
export function validateNavigationResponse(
  response: { status(): number } | null | undefined,
  targetUrl: string,
  tracker?: { recordAssertion(name: string, status: 'PASS' | 'FAIL', message?: string): void }
): number {
  if (!response) {
    if (tracker) {
      tracker.recordAssertion('Core route / responds with HTTP 200 OK', 'FAIL', 'page.goto returned null response');
    }
    throw new Error(
      `[NAVIGATION FAILURE] page.goto('${targetUrl}') returned no HTTP response (null). Release gate fails closed.`
    );
  }

  const status = response.status();
  if (status !== 200) {
    if (tracker) {
      tracker.recordAssertion('Core route / responds with HTTP 200 OK', 'FAIL', `Returned HTTP ${status}`);
    }
    throw new Error(
      `[NAVIGATION FAILURE] Staging application returned non-200 HTTP status: ${status}`
    );
  }

  if (tracker) {
    tracker.recordAssertion('Core route / responds with HTTP 200 OK', 'PASS');
  }
  return status;
}

test.describe('Universal Pro AI - Live Staging Browser Smoke Suite [LIVE]', () => {
  test.describe.configure({ retries: 0 });

  test('live-staging-smoke: renders live staging application, verifies boot, controls, and layout', async ({ page }, testInfo) => {
    // 1. Enforce Staging Gate Authorization Guard
    if (process.env.ALLOW_LIVE_STAGING_SMOKE !== 'true') {
      test.skip(
        true,
        'Live Staging smoke test BLOCKED: requires gate authorization (ALLOW_LIVE_STAGING_SMOKE=true). Dev runs must remain mocked.'
      );
    }

    // 2. Validate Target Origin against explicitly approved HTTPS Staging allowlist
    const stagingBaseUrl = (
      process.env.STAGING_BASE_URL ||
      'https://universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app'
    ).replace(/\/$/, '');

    const originValidation = validateStagingOrigin(stagingBaseUrl);
    if (!originValidation.isValid) {
      throw new Error(`[RELEASE GATE SECURITY VIOLATION] ${originValidation.error}`);
    }

    const stagingApiOrigin = resolveStagingApiOrigin(process.env.STAGING_API_URL);
    const tracker = new EvidenceTracker(page, testInfo, 'live');

    // Track application HTTP 4xx/5xx responses (both frontend origin and configured backend API origin)
    const httpErrors: string[] = [];
    page.on('response', (res) => {
      if (res.status() >= 400) {
        const u = res.url();
        if (isMonitoredHttpErrorUrl(u, stagingBaseUrl, stagingApiOrigin)) {
          httpErrors.push(`${res.status()} ${sanitizeUrl(u)}`);
        }
      }
    });

    // 3. Construct URL with Vercel protection bypass if configured
    const bypassSecret = process.env.VERCEL_PROTECTION_BYPASS || '';
    let targetNavUrl = stagingBaseUrl;
    if (bypassSecret) {
      const urlObj = new URL(stagingBaseUrl);
      urlObj.searchParams.set('x-vercel-protection-bypass', bypassSecret);
      urlObj.searchParams.set('x-vercel-set-bypass-cookie', 'samesitenone');
      targetNavUrl = urlObj.toString();
    }

    // 4. Launch on Staging Base URL & Validate Against Unsafe Redirects
    const response = await page.goto(targetNavUrl, { waitUntil: 'domcontentloaded' });

    // Validate against null or non-200 response (fails closed immediately per GAP-03)
    validateNavigationResponse(response, targetNavUrl, tracker);
    expect(response!.status(), `Staging application returned non-200 HTTP status: ${response?.status()}`).toBe(200);

    const postNavOrigin = new URL(page.url()).origin;
    const postNavValidation = validateStagingOrigin(postNavOrigin);
    if (!postNavValidation.isValid) {
      throw new Error(`[POST-NAV REDIRECT VIOLATION] Redirected to unapproved origin: ${postNavOrigin}`);
    }

    await tracker.captureStepScreenshot('smoke_staging_01_homepage_loaded');

    // 5. Verify page title, main heading, and frontend bootstrap
    await expect(page).toHaveTitle(/Universal Pro AI/i);
    const mainHeading = page.locator('h1');
    await expect(mainHeading).toBeVisible();
    tracker.recordAssertion('Frontend bootstrap: title and heading visible', 'PASS');

    // 6. Verify Design System Tokens
    const designTokens = await page.evaluate(() => {
      const styles = getComputedStyle(document.documentElement);
      return {
        bgBase: styles.getPropertyValue('--bg-base').trim(),
        accentEmerald: styles.getPropertyValue('--accent-emerald').trim(),
        textPrimary: styles.getPropertyValue('--text-primary').trim(),
      };
    });
    expect(designTokens.bgBase, 'Design token --bg-base must be defined').toBeTruthy();
    expect(designTokens.accentEmerald, 'Design token --accent-emerald must be defined').toBeTruthy();
    expect(designTokens.textPrimary, 'Design token --text-primary must be defined').toBeTruthy();
    tracker.recordAssertion('Design system CSS tokens verified (--bg-base, --accent-emerald, --text-primary)', 'PASS');

    // 7. Locate and verify interactive input and controls
    const urlInput = page.getByLabel('Video URL');
    await expect(urlInput).toBeVisible();
    await expect(urlInput).toBeEnabled();

    const domainSelect = page.getByLabel('Content Domain Classifier');
    await expect(domainSelect).toBeVisible();

    const submitBtn = page.getByLabel('Get video intelligence');
    await expect(submitBtn).toBeVisible();
    // Application enforces disabled={isLoading || !url}; verify initial disabled state on empty input
    await expect(submitBtn).toBeDisabled();

    // Verify input interaction enables the submit CTA without initiating extraction
    await urlInput.fill('https://www.instagram.com/reel/C1234567890/');
    await expect(submitBtn).toBeEnabled();
    await urlInput.clear();

    const sampleChips = page.locator('.chip-tactile');
    const sampleCount = await sampleChips.count();
    expect(sampleCount, 'Expected at least 1 sample chip rendered').toBeGreaterThan(0);

    const themeToggle = page.locator('button[aria-label*="Mode" i]');
    await expect(themeToggle).toBeVisible();
    tracker.recordAssertion('Interactive controls verified (input, classifier, submit CTA, sample chips, theme toggle)', 'PASS');

    // 8. Verify Desktop and Mobile Layouts
    // Desktop layout (1280px)
    const desktopScrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    expect(desktopScrollWidth, 'Desktop horizontal overflow detected').toBeLessThanOrEqual(1280);
    tracker.recordAssertion('Desktop layout verified (1280px viewport without overflow)', 'PASS');

    // Mobile layout (375x812)
    await page.setViewportSize({ width: 375, height: 812 });
    const mobileScrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    expect(mobileScrollWidth, 'Mobile horizontal overflow detected').toBeLessThanOrEqual(375);

    // Rule 15: font-size >= 16px on input to prevent iOS auto-zoom
    const inputFontSize = await urlInput.evaluate((el) => window.getComputedStyle(el).fontSize);
    expect(parseFloat(inputFontSize), 'Rule 15 violation: input font-size must be >= 16px').toBeGreaterThanOrEqual(16);

    await tracker.captureStepScreenshot('smoke_staging_02_mobile_layout');
    tracker.recordAssertion('Mobile layout verified (375px viewport without overflow, font-size >= 16px)', 'PASS');

    // Restore desktop viewport
    await page.setViewportSize({ width: 1280, height: 800 });

    // 9. Verify single docked video player contract (never duplicate HTML5 <video> elements)
    const videoElements = page.locator('video');
    const videoCount = await videoElements.count();
    expect(videoCount, 'Contract violation: More than 1 HTML5 video element detected').toBeLessThanOrEqual(1);
    tracker.recordAssertion('Single docked video player contract verified (count <= 1)', 'PASS');

    // 10. Capture completed state screenshot
    await tracker.captureStepScreenshot('smoke_staging_03_verified');
    tracker.recordAssertion('Live Staging browser smoke verification completed', 'PASS');

    // 11. Fail on unexpected application console errors or 4xx/5xx responses
    expect(tracker.consoleErrors, `Unexpected browser console errors: ${tracker.consoleErrors.join(', ')}`).toEqual([]);
    expect(tracker.httpFailures, `Unexpected 5xx internal server errors: ${tracker.httpFailures.join(', ')}`).toEqual([]);
    expect(httpErrors, `Unexpected HTTP 4xx/5xx responses: ${httpErrors.join(', ')}`).toEqual([]);
  });
});
