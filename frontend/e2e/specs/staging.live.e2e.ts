import { test, expect, Response } from '@playwright/test';
import { EvidenceTracker } from '../helpers/evidence-tracker';
import { validateStagingOrigin, EXACT_APPROVED_STAGING_ORIGINS, sanitizeUrl, sanitizeText } from '../../src/lib/evidenceSanitizer';

/**
 * Universal Pro AI - Live Staging Extraction E2E Release Gate [LIVE]
 * =================================================================
 * STRICT GOVERNANCE CONSTRAINTS:
 * 1. This suite is EXCLUSIVELY for execution against Layer 2 (Staging) after owner authorization.
 * 2. It must NEVER run in local Dev or without ALLOW_LIVE_STAGING_EXTRACTION=true.
 * 3. It DOES NOT mock /api/v1/extract — it executes real live end-to-end extraction.
 * 4. Uses a permitted non-YouTube URL (Instagram reel) and bounded 90s timeout.
 * 5. Single-attempt guard prevents repeated calls that consume AI inference and proxy quotas.
 * 6. Strictly enforces cache-miss execution (HTTP 202 queued -> background worker -> HTTP 200 completed).
 *    Viral cache hits (HTTP 200 is_cached: true) are rejected to guarantee UPA-1305 downloader path execution.
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
    // Sanitize target URL for diagnostics and error messages (stripping query parameters and credentials)
    const sanitizedDisplayTargetUrl = sanitizeUrl(parsedTarget.origin + parsedTarget.pathname);

    if (parsedTarget.protocol !== 'https:') {
      throw new Error(`[SECURITY GATE VIOLATION] Target test URL must use HTTPS: ${sanitizedDisplayTargetUrl}`);
    }
    const targetHost = parsedTarget.hostname.toLowerCase();
    const isApprovedPlatform = ['instagram.com', 'www.instagram.com', 'tiktok.com', 'www.tiktok.com'].includes(targetHost);
    if (!isApprovedPlatform) {
      throw new Error(`[SECURITY GATE VIOLATION] Target URL "${sanitizedDisplayTargetUrl}" is not an approved media platform.`);
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
    let targetJobId: string | null = null;
    interface CandidateStatusRecord {
      response: Response;
      url: string;
      urlJobId?: string;
      parsedJobId?: string;
      status?: string;
      stage?: string;
      json?: any;
      parseError?: string;
    }

    const candidateEvidencePromises: Promise<CandidateStatusRecord>[] = [];
    let terminalRecordResolver: ((record: CandidateStatusRecord) => void) | null = null;
    let terminalRecordRejecter: ((err: Error) => void) | null = null;
    let terminalRecordSettled = false;

    const terminalRecordPromise = new Promise<CandidateStatusRecord>((resolve, reject) => {
      terminalRecordResolver = (record: CandidateStatusRecord) => {
        if (!terminalRecordSettled) {
          terminalRecordSettled = true;
          resolve(record);
        }
      };
      terminalRecordRejecter = (err: Error) => {
        if (!terminalRecordSettled) {
          terminalRecordSettled = true;
          reject(err);
        }
      };
    });

    const checkCandidateForTerminal = (record: CandidateStatusRecord) => {
      if (terminalRecordSettled || !targetJobId) return;

      // Only evaluate responses for the exact target job URL path segment
      if (record.urlJobId !== targetJobId) {
        return;
      }

      // If a response has the exact target-job status URL but JSON parsing failed,
      // reject the pending terminal wait immediately with a sanitized [STAGE CAPTURE ERROR]
      if (record.parseError) {
        const sanitizedUrl = sanitizeUrl(record.url);
        const sanitizedError = sanitizeText(record.parseError);
        terminalRecordRejecter?.(
          new Error(
            `[STAGE CAPTURE ERROR] Failed to parse status response JSON for job "${targetJobId}" (${sanitizedUrl}): ${sanitizedError}`
          )
        );
        return;
      }

      // If a JSON job_id is supplied, reject conflict with URL/target job ID
      if (record.parsedJobId && record.parsedJobId !== targetJobId) {
        const sanitizedUrl = sanitizeUrl(record.url);
        terminalRecordRejecter?.(
          new Error(
            `[JOB ID MISMATCH] Status response JSON job_id "${record.parsedJobId}" conflicts with URL job_id "${record.urlJobId}" and target job_id "${targetJobId}" (${sanitizedUrl}).`
          )
        );
        return;
      }

      // When parsing succeeded and response indicates terminal completion:
      if (
        record.response.status() === 200 &&
        record.parsedJobId === targetJobId &&
        record.status === 'completed'
      ) {
        terminalRecordResolver?.(record);
      }
    };

    // Setup listener to intercept and validate the initial extraction submission
    const initialPostResponsePromise = page.waitForResponse(
      (resp) => resp.url().includes('/api/v1/extract') && resp.request().method() === 'POST',
      { timeout: 30_000 }
    );

    // Collect candidate status response records without mutating evidence before targetJobId is known
    const onResponseHandler = (resp: Response) => {
      const url = resp.url();
      if (resp.status() !== 200 || !url.includes('/api/v1/extract/status/')) {
        return;
      }
      const match = url.match(/\/api\/v1\/extract\/status\/([^?#/]+)/);
      const urlJobId = match ? match[1] : undefined;

      const parsePromise = (async (): Promise<CandidateStatusRecord> => {
        try {
          const json = await resp.json();
          const record: CandidateStatusRecord = {
            response: resp,
            url,
            urlJobId,
            parsedJobId: json && typeof json.job_id === 'string' ? json.job_id : undefined,
            status: json && typeof json.status === 'string' ? json.status : undefined,
            stage: json && typeof json.stage === 'string' ? json.stage : undefined,
            json,
          };
          checkCandidateForTerminal(record);
          return record;
        } catch (err: any) {
          const record: CandidateStatusRecord = {
            response: resp,
            url,
            urlJobId,
            parseError: err?.message || String(err),
          };
          checkCandidateForTerminal(record);
          return record;
        }
      })();
      candidateEvidencePromises.push(parsePromise);
    };
    page.on('response', onResponseHandler);

    const extractionStartTime = Date.now();
    await submitBtn.click();

    // Validate Initial Extraction POST: must be an uncached background job (HTTP 202 Accepted)
    const initialPostResponse = await initialPostResponsePromise;
    const initialStatus = initialPostResponse.status();
    const initialJson = await initialPostResponse.json().catch(() => ({}));

    // Explicitly reject viral cache hits (HTTP 200 or is_cached: true):
    // UPA-1305 downloader fix can ONLY be proven via an uncached worker extraction pipeline.
    if (initialStatus === 200 || initialJson.is_cached === true) {
      throw new Error(
        `[UPA-1305 VALIDATION BLOCKED] Target URL "${sanitizedDisplayTargetUrl}" was served from viral cache (HTTP ${initialStatus}, is_cached: ${initialJson.is_cached}). ` +
        'A cached extraction bypasses media_downloader.py and cannot validate the UPA-1305 downloader fix. ' +
        'Please supply an uncached, permitted Instagram or TikTok URL via STAGING_TEST_URL.'
      );
    }

    expect(
      initialStatus,
      `Initial extraction POST must return HTTP 202 Accepted for an uncached background extraction, got HTTP ${initialStatus}`
    ).toBe(202);
    expect(
      initialJson.is_cached,
      'Initial extraction response must have is_cached: false to exercise worker downloader'
    ).toBe(false);
    expect(
      initialJson.status,
      'Initial extraction response status must be "queued"'
    ).toBe('queued');
    expect(
      initialJson.job_id,
      'Initial extraction response must include a valid job_id'
    ).toBeTruthy();
    expect(
      initialJson.poll_url,
      'Initial extraction response must include a poll_url'
    ).toBeTruthy();

    targetJobId = String(initialJson.job_id);
    expect(
      initialJson.poll_url,
      `Initial poll_url must target the enqueued job_id: ${targetJobId}`
    ).toContain(targetJobId);

    tracker.recordAssertion(`Initial extraction verified as uncached background job (HTTP 202, is_cached: false, job_id: ${targetJobId})`, 'PASS');

    // Retroactively check any candidate records that arrived before targetJobId was established
    for (const promise of candidateEvidencePromises) {
      promise.then((record) => {
        checkCandidateForTerminal(record);
      }).catch(() => {});
    }

    // 7. Bounded Poll for Terminal Completed Status (Max 90 seconds per Rule 4 cap)
    const extractionDeadline = extractionStartTime + 90_000;
    const remainingTimeoutMs = Math.max(1000, extractionDeadline - Date.now());

    let timeoutTimer: NodeJS.Timeout | null = null;
    const terminalTimeoutPromise = new Promise<never>((_, reject) => {
      timeoutTimer = setTimeout(() => {
        terminalRecordSettled = true;
        reject(
          new Error(
            `[TIMEOUT] Timed out waiting for terminal "completed" status response for target job "${targetJobId || 'unknown'}" within 90s bounded timeout.`
          )
        );
      }, remainingTimeoutMs);
    });

    // Await explicit backend completed response from status polling with race-safe selection
    let terminalRecord: CandidateStatusRecord;
    try {
      terminalRecord = await Promise.race([
        terminalRecordPromise,
        terminalTimeoutPromise,
      ]);
    } finally {
      if (timeoutTimer) {
        clearTimeout(timeoutTimer);
      }
      page.off('response', onResponseHandler);
    }

    // Progress deck must clear completely (cannot stay in queued/processing state)
    await expect(page.locator('.shimmer-card')).not.toBeVisible({ timeout: 90_000 });
    await expect(page.getByText(/Ingesting Video Stream|Executing Neural Multimodal/i)).not.toBeVisible();

    // Await all candidate status parsing promises to guarantee complete asynchronous capture
    const candidateEvidenceList = await Promise.all(candidateEvidencePromises);

    const terminalResponse = terminalRecord.response;
    expect(terminalResponse.status(), 'Terminal extraction status must return HTTP 200').toBe(200);
    const terminalJson = terminalRecord.json;
    expect(terminalJson.status, 'Backend extraction must report terminal "completed" status').toBe('completed');
    expect(terminalJson.job_id, 'Terminal extraction response must match target job_id').toBe(targetJobId);
    expect(terminalJson.data, 'Backend extraction must contain structured data object').toBeTruthy();
    expect(typeof terminalJson.data.title, 'Terminal structured payload must contain title').toBe('string');
    expect(terminalJson.data.title.trim().length, 'Terminal structured payload title must be meaningful (>= 5 chars)').toBeGreaterThanOrEqual(5);
    expect(
      Array.isArray(terminalJson.data.instructions) && terminalJson.data.instructions.length > 0,
      'Terminal structured payload must contain non-empty instructions array'
    ).toBe(true);
    tracker.recordAssertion('Backend API terminal status verified as completed with HTTP 200 and structured content', 'PASS');

    // Filter candidate evidence strictly associated with targetJobId
    const observedStages = new Set<string>();
    for (const item of candidateEvidenceList) {
      // 1. Require exact target job ID in the status URL path segment
      if (item.urlJobId !== targetJobId) {
        // A body ID alone must not qualify as evidence when the URL path cannot be validated
        if (item.parsedJobId === targetJobId) {
          const sanitizedUrl = sanitizeUrl(item.url);
          throw new Error(
            `[JOB ID MISMATCH] Status response JSON job_id "${item.parsedJobId}" conflicts with status URL path "${sanitizedUrl}".`
          );
        }
        // Disregard status events from unrelated background requests
        continue;
      }

      // 2. Exact URL match established: if parsing failed for target job, fail explicitly
      if (item.parseError) {
        const sanitizedUrl = sanitizeUrl(item.url);
        const sanitizedError = sanitizeText(item.parseError);
        throw new Error(
          `[STAGE CAPTURE ERROR] Failed to parse status response JSON for job "${targetJobId}" (${sanitizedUrl}): ${sanitizedError}`
        );
      }

      // 3. If a JSON job_id is supplied, require it to agree with both the URL job ID and the target ID
      if (item.parsedJobId && item.parsedJobId !== targetJobId) {
        const sanitizedUrl = sanitizeUrl(item.url);
        throw new Error(
          `[JOB ID MISMATCH] Status response JSON job_id "${item.parsedJobId}" conflicts with URL job_id "${item.urlJobId}" and target job_id "${targetJobId}" (${sanitizedUrl}).`
        );
      }

      if (item.stage) {
        observedStages.add(item.stage);
      }
    }

    // Verify downloader-related execution: real worker processing stages must have been observed for targetJobId
    // Note: terminalJson.stage === 'completed' is strictly excluded as a substitute.
    const observedStageList = Array.from(observedStages);
    const hasWorkerStageEvidence =
      observedStages.has('downloading_media') ||
      observedStages.has('multimodal_ai_inference');
    expect(
      hasWorkerStageEvidence,
      `Real worker processing stage must be observed during background extraction polling for job "${targetJobId}" (expected "downloading_media" or "multimodal_ai_inference"). Observed stages: [${observedStageList.join(', ')}]`
    ).toBe(true);
    tracker.recordAssertion(
      `Worker background execution observed with processing stages for job ${targetJobId}: [${observedStageList.join(', ')}]`,
      'PASS'
    );

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
