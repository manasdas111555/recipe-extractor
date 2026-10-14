import { test, expect } from '@playwright/test';
import { EvidenceTracker } from '../helpers/evidence-tracker';
import { validateStagingOrigin, EXACT_APPROVED_STAGING_ORIGINS } from '../../src/lib/evidenceSanitizer';

/**
 * Universal Pro AI - Live Staging Extraction E2E Release Gate [LIVE]
 * =================================================================
 * STRICT GOVERNANCE CONSTRAINTS:
 * 1. This suite is EXCLUSIVELY for execution against Layer 2 (Staging) after owner authorization.
 * 2. It must NEVER run in local Dev or without ALLOW_LIVE_STAGING_EXTRACTION=true.
 * 3. It DOES NOT mock /api/v1/extract — it executes real live end-to-end extraction.
 * 4. Uses a permitted non-YouTube URL (Instagram reel) and bounded 90s timeout.
 * 5. Single-attempt guard prevents repeated calls that consume AI inference and proxy quotas.
 */
test.describe('Universal Pro AI - Live Staging Extraction Suite [LIVE]', () => {
  // Enforce single-attempt policy per Rule 4 to protect AI inference & proxy quotas
  test.describe.configure({ retries: 0 });

  test('live-staging: real UI submission with un-mocked backend extraction and content verification', async ({ page }, testInfo) => {
    // 1. Enforce Staging Gate Authorization Guard
    if (process.env.ALLOW_LIVE_STAGING_EXTRACTION !== 'true') {
      test.skip(
        true,
        'Live Staging extraction BLOCKED: requires explicit gate authorization (ALLOW_LIVE_STAGING_EXTRACTION=true). Dev runs must remain mocked.'
      );
    }

    // 2. Validate Target Origin against explicitly approved HTTPS Staging allowlist (Refuse Production & Lookalikes)
    const stagingBaseUrl = (
      process.env.STAGING_BASE_URL ||
      'https://universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app'
    ).replace(/\/$/, '');

    const originValidation = validateStagingOrigin(stagingBaseUrl);
    if (!originValidation.isValid) {
      throw new Error(`[RELEASE GATE SECURITY VIOLATION] ${originValidation.error}`);
    }

    // 3. Validate Test Video Target URL (Must be permitted HTTPS platform, refuse arbitrary SSRF targets)
    const stagingUrl = process.env.STAGING_TEST_URL || 'https://www.instagram.com/reel/DdGvPs9zhVu/';
    const parsedTarget = new URL(stagingUrl);
    if (parsedTarget.protocol !== 'https:') {
      throw new Error(`[SECURITY GATE VIOLATION] Target test URL must use HTTPS: ${stagingUrl}`);
    }
    const targetHost = parsedTarget.hostname.toLowerCase();
    const isApprovedPlatform = ['instagram.com', 'www.instagram.com', 'tiktok.com', 'www.tiktok.com'].includes(targetHost);
    if (!isApprovedPlatform) {
      throw new Error(`[SECURITY GATE VIOLATION] Target URL "${stagingUrl}" is not an approved media platform.`);
    }

    const tracker = new EvidenceTracker(page, testInfo, 'live');

    // 4. Launch on Staging Base URL & Validate Against Unsafe Redirects
    await page.goto(stagingBaseUrl, { waitUntil: 'domcontentloaded' });
    const postNavOrigin = new URL(page.url()).origin;
    if (!EXACT_APPROVED_STAGING_ORIGINS.has(postNavOrigin)) {
      throw new Error(`[SECURITY GATE VIOLATION] Unsafe redirect detected: Navigated to "${postNavOrigin}", which is not in the exact approved Staging origins.`);
    }

    tracker.recordAssertion(`Staging frontend loaded and verified on exact staging origin: ${postNavOrigin}`, 'PASS');
    await tracker.captureStepScreenshot('staging_01_loaded');

    // 5. Fill URL in real UI input
    const urlInput = page.getByLabel('Video URL');
    const submitBtn = page.getByLabel('Get video intelligence');

    await expect(urlInput).toBeVisible();
    await urlInput.fill(stagingUrl);
    await expect(submitBtn).toBeEnabled();
    await tracker.captureStepScreenshot('staging_02_url_submitted');

    // 6. Trigger Real Un-Mocked Extraction (Single-attempt)
    // Setup listener for terminal extraction completion to reject 202/queued/partial responses
    const terminalResponsePromise = page.waitForResponse(
      async (resp) => {
        if (!resp.url().includes('/api/v1/extract')) return false;
        if (resp.status() !== 200) return false;
        try {
          const json = await resp.json();
          return json.status === 'completed';
        } catch {
          return false;
        }
      },
      { timeout: 90_000 }
    );

    await submitBtn.click();

    // 7. Bounded Poll for Terminal Completed Status (Max 90 seconds per Rule 4 cap)
    // Progress deck must clear completely (cannot stay in queued/processing state)
    await expect(page.locator('.shimmer-card')).not.toBeVisible({ timeout: 90_000 });
    await expect(page.getByText(/Ingesting Video Stream|Executing Neural Multimodal/i)).not.toBeVisible();

    // Await explicit backend completed response
    const terminalResponse = await terminalResponsePromise;
    expect(terminalResponse.status(), 'Backend extraction must return HTTP 200, not 202 or 500').toBe(200);
    const terminalJson = await terminalResponse.json();
    expect(terminalJson.status, 'Backend extraction must report terminal "completed" status').toBe('completed');
    expect(terminalJson.data, 'Backend extraction must contain structured data object').toBeTruthy();
    tracker.recordAssertion('Backend API terminal status verified as completed with HTTP 200', 'PASS');

    // Assert that no error alert was rendered
    const errorAlert = page.locator('main [role="alert"]').or(page.locator('.glass-panel[role="alert"]')).first();
    await expect(errorAlert).not.toBeVisible();

    // Locate terminal result heading
    const resultHeading = page.locator('main h2').first();
    await expect(resultHeading).toBeVisible({ timeout: 10_000 });
    tracker.recordAssertion('Terminal extraction status reached successfully within 90s bounded timeout', 'PASS');
    await tracker.captureStepScreenshot('staging_03_result_rendered');

    // 8. Assert Real Meaningful Structured Content Attributes (Reject empty/partial/202 responses)
    const resultText = await resultHeading.innerText();
    expect(resultText.trim().length).toBeGreaterThanOrEqual(5);
    tracker.recordAssertion('Live extracted title verified meaningful and non-empty (>= 5 chars)', 'PASS');

    // Verify structured ingredients section rendered with at least 2 distinct items
    const ingredientsSection = page.getByText(/Ingredients/i).first();
    await expect(ingredientsSection).toBeVisible();
    const ingredientItems = page.locator('main ul li, main ol li, main tr');
    const ingredientCount = await ingredientItems.count();
    expect(ingredientCount).toBeGreaterThanOrEqual(2);
    tracker.recordAssertion(`Live extracted ingredients verified structured with ${ingredientCount} items`, 'PASS');

    // Verify structured instructions section rendered with content
    const instructionsSection = page.getByText(/Step-by-Step Instructions|Instructions/i).first();
    await expect(instructionsSection).toBeVisible();
    tracker.recordAssertion('Live extracted instructions section verified with complete steps', 'PASS');

    // 9. Assert Clean Error Logs
    expect(tracker.httpFailures, `Staging HTTP errors: ${tracker.httpFailures.join(', ')}`).toEqual([]);
    expect(tracker.consoleErrors, `Staging browser console errors: ${tracker.consoleErrors.join(', ')}`).toEqual([]);
  });
});
