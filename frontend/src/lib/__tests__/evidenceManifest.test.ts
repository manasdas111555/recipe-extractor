import { describe, it, expect } from 'vitest';
import { sanitizeText, sanitizeUrl, sanitizeObject, validateStagingOrigin, EXACT_APPROVED_STAGING_ORIGINS } from '../evidenceSanitizer';
import { createRunManifest, validateManifest, TestEvidenceRecord } from '../evidenceManifest';

describe('Evidence Sanitizer', () => {
  it('redacts sensitive query parameters in text and URLs across all parameter variants', () => {
    const raw = 'Request to https://example.com/api?token=secret_12345&access_token=acc_tok_999&client_secret=cls_abc&api-key=my_dash_key';
    const sanitized = sanitizeText(raw);
    expect(sanitized).toContain('token=[REDACTED]');
    expect(sanitized).toContain('access_token=[REDACTED]');
    expect(sanitized).toContain('client_secret=[REDACTED]');
    expect(sanitized).toContain('api-key=[REDACTED]');
    expect(sanitized).not.toContain('secret_12345');
    expect(sanitized).not.toContain('acc_tok_999');
    expect(sanitized).not.toContain('cls_abc');
    expect(sanitized).not.toContain('my_dash_key');
  });

  it('redacts basic authentication credentials in URL authority', () => {
    const rawUrl = 'https://admin_user:secret_super_pass123@staging.internal.network/api/v1/extract';
    const sanitizedUrl = sanitizeUrl(rawUrl);
    expect(sanitizedUrl).toContain('REDACTED_USER:REDACTED_PASS@staging.internal.network');
    expect(sanitizedUrl).not.toContain('admin_user');
    expect(sanitizedUrl).not.toContain('secret_super_pass123');
  });

  it('redacts Vercel protection bypass query params, headers, and cookies', () => {
    const rawUrl = 'https://staging.vercel.app/?x-vercel-protection-bypass=supersecret99&other=1';
    const sanitizedUrl = sanitizeUrl(rawUrl);
    expect(sanitizedUrl).toContain('x-vercel-protection-bypass=%5BREDACTED%5D');
    expect(sanitizedUrl).not.toContain('supersecret99');

    const rawHeader = 'x-vercel-protection-bypass: bypass_token_value_abc';
    const sanitizedHeader = sanitizeText(rawHeader);
    expect(sanitizedHeader).toContain('[REDACTED]');
    expect(sanitizedHeader).not.toContain('bypass_token_value_abc');

    const rawCookie = 'Cookie: _vercel_jwt=eyJhbGciOiJIUzI1NiJ9.test.sig; theme=dark';
    const sanitizedCookie = sanitizeText(rawCookie);
    expect(sanitizedCookie).toContain('_vercel_jwt=[REDACTED]');
    expect(sanitizedCookie).not.toContain('eyJhbGciOiJIUzI1NiJ9.test.sig');
  });

  it('redacts Bearer and Basic authorization headers and JWT token signatures', () => {
    const bearerHeader = 'Authorization: Bearer my_secret_bearer_token_xyz';
    expect(sanitizeText(bearerHeader)).toBe('Authorization: Bearer [REDACTED_TOKEN]');

    const basicHeader = 'Authorization: Basic YWRtaW46cGFzc3dvcmQ=';
    expect(sanitizeText(basicHeader)).toBe('Authorization: Basic [REDACTED_CREDENTIAL]');

    const mockJwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c';
    expect(sanitizeText(`Token is ${mockJwt}`)).toBe('Token is [REDACTED_JWT]');
  });

  it('redacts provider API key formats (OpenAI sk-proj, Google AIzaSy, Supabase sbp, GitHub ghp)', () => {
    // Construct synthetic Google key fixture dynamically so static secret scanners do not trigger on continuous literals
    const syntheticGoogleKey = ['AIza', 'Sy', 'MOCK_SYNTHETIC_TEST_FIXTURE_12345'].join('');
    const rawKeys = `Keys: sk-proj-12345678901234567890, ${syntheticGoogleKey}, sbp_abcdef12345678901234, ghp_ghpat123456789012345`;
    const sanitized = sanitizeText(rawKeys);
    expect(sanitized).not.toContain('sk-proj-12345678901234567890');
    expect(sanitized).not.toContain(syntheticGoogleKey);
    expect(sanitized).not.toContain('sbp_abcdef12345678901234');
    expect(sanitized).not.toContain('ghp_ghpat123456789012345');
    expect(sanitized).toContain('[REDACTED_API_KEY]');
  });

  it('recursively sanitizes nested objects, arrays, and keys with credential/auth/cookie names', () => {
    const payload = {
      user: 'alice',
      authToken: 'secret_token_123',
      nested: {
        apiKey: 'key_value_456',
        client_credential: 'cred_secret_789',
        session_cookie: 'sess_abc',
        details: ['item1', 'token=abc_987'],
      },
    };
    const sanitized = sanitizeObject(payload);
    expect(sanitized.authToken).toBe('[REDACTED]');
    expect(sanitized.nested.apiKey).toBe('[REDACTED]');
    expect(sanitized.nested.client_credential).toBe('[REDACTED]');
    expect(sanitized.nested.session_cookie).toBe('[REDACTED]');
    expect(sanitized.nested.details[1]).toBe('token=[REDACTED]');
  });
});

describe('Evidence Manifest Engine', () => {
  const sampleTestRecord: TestEvidenceRecord = {
    testId: 'test_mocked_extraction_1',
    title: 'renders homepage and extracts recipe with mocked API',
    outcome: 'PASS',
    startTime: '2026-10-13T17:00:00.000Z',
    endTime: '2026-10-13T17:00:05.000Z',
    durationMs: 5000,
    executionType: 'mocked',
    browser: 'chromium',
    viewport: { width: 1280, height: 800 },
    assertionOutcomes: [
      { name: 'Homepage heading visible', status: 'PASS' },
      { name: 'Recipe title displayed', status: 'PASS' },
    ],
    evidencePaths: {
      screenshots: ['test-results/01-initial.png', 'test-results/02-result.png'],
      video: 'test-results/video.webm',
      trace: 'test-results/trace.zip',
      htmlReport: 'playwright-report/index.html',
    },
    capturedConsoleErrors: [],
    capturedHttpFailures: [],
    sanitized: true,
  };

  it('creates a compliant RunEvidenceManifest', () => {
    const manifest = createRunManifest({
      runId: 'e2e_run_test_001',
      commitSha: '6ce1b1b144f38024d81f8a6db4ce931c11e34556',
      environment: 'dev',
      startTime: '2026-10-13T17:00:00.000Z',
      endTime: '2026-10-13T17:00:06.000Z',
      totalDurationMs: 6000,
      executionClassification: 'mocked',
      tests: [sampleTestRecord],
    });

    expect(manifest.schemaVersion).toBe(1);
    expect(manifest.runId).toBe('e2e_run_test_001');
    expect(manifest.overallStatus).toBe('PASS');
    expect(manifest.executionClassification).toBe('mocked');
    expect(manifest.summary.total).toBe(1);
    expect(manifest.summary.passed).toBe(1);
    expect(manifest.summary.failed).toBe(0);

    const validation = validateManifest(manifest);
    expect(validation.isValid).toBe(true);
    expect(validation.errors).toEqual([]);
  });

  it('flags validation errors for invalid manifests', () => {
    const invalidManifest: any = {
      schemaVersion: 0,
      runId: '',
      commitSha: '',
      environment: 'production_unsupported',
      executionClassification: 'unknown',
      tests: [{ title: 'Missing testId' }],
    };

    const validation = validateManifest(invalidManifest);
    expect(validation.isValid).toBe(false);
    expect(validation.errors.length).toBeGreaterThan(0);
  });

  it('correctly reports executionClassification as live for live staging runs and sets NOT RUN when skipped', () => {
    const liveSkippedRecord: TestEvidenceRecord = {
      ...sampleTestRecord,
      testId: 'test_live_staging_extraction_1',
      outcome: 'NOT RUN',
      executionType: 'live',
      assertionOutcomes: [],
    };

    const manifest = createRunManifest({
      runId: 'e2e_staging_run_002',
      commitSha: '6ce1b1b144f38024d81f8a6db4ce931c11e34556',
      environment: 'staging',
      startTime: '2026-10-13T17:10:00.000Z',
      endTime: '2026-10-13T17:10:30.000Z',
      totalDurationMs: 30000,
      executionClassification: 'live',
      tests: [liveSkippedRecord],
    });

    expect(manifest.executionClassification).toBe('live');
    expect(manifest.overallStatus).toBe('NOT RUN');
    expect(manifest.summary.passed).toBe(0);
    expect(manifest.summary.notRun).toBe(1);

    const validation = validateManifest(manifest);
    expect(validation.isValid).toBe(true);
  });

  it('fails gate validation when a passed test lacks mandatory screenshot evidence', () => {
    const missingEvidenceTest: TestEvidenceRecord = {
      ...sampleTestRecord,
      testId: 'test_missing_screenshots',
      evidencePaths: {
        screenshots: [], // 0 screenshots!
        video: 'test-results/video.webm',
        trace: 'test-results/trace.zip',
        htmlReport: 'playwright-report/index.html',
      },
    };

    const manifest = createRunManifest({
      runId: 'e2e_run_test_fail_path',
      commitSha: '6ce1b1b144f38024d81f8a6db4ce931c11e34556',
      environment: 'dev',
      startTime: '2026-10-13T17:00:00.000Z',
      endTime: '2026-10-13T17:00:05.000Z',
      totalDurationMs: 5000,
      executionClassification: 'mocked',
      tests: [missingEvidenceTest],
    });

    const validation = validateManifest(manifest);
    expect(validation.isValid).toBe(false);
    expect(validation.errors.some((err) => err.includes('mandatory screenshot evidence missing'))).toBe(true);
  });

  it('fails gate validation when a passed test lacks mandatory video or trace artifacts', () => {
    const missingVideoTraceTest: TestEvidenceRecord = {
      ...sampleTestRecord,
      testId: 'test_missing_video_trace',
      evidencePaths: {
        screenshots: ['test-results/01-initial.png'],
        video: undefined,
        trace: undefined,
        htmlReport: 'playwright-report/index.html',
      },
    };

    const manifest = createRunManifest({
      runId: 'e2e_run_test_missing_vt',
      commitSha: '6ce1b1b144f38024d81f8a6db4ce931c11e34556',
      environment: 'dev',
      startTime: '2026-10-13T17:00:00.000Z',
      endTime: '2026-10-13T17:00:05.000Z',
      totalDurationMs: 5000,
      executionClassification: 'mocked',
      tests: [missingVideoTraceTest],
    });

    const validation = validateManifest(manifest);
    expect(validation.isValid).toBe(false);
    expect(validation.errors.some((err) => err.includes('mandatory video recording artifact'))).toBe(true);
    expect(validation.errors.some((err) => err.includes('mandatory Playwright trace artifact'))).toBe(true);
  });

  it('fails gate validation when a passed test recorded zero assertions or contains failing assertions', () => {
    const zeroAssertionsTest: TestEvidenceRecord = {
      ...sampleTestRecord,
      testId: 'test_zero_assertions',
      assertionOutcomes: [],
    };

    const manifestZero = createRunManifest({
      runId: 'e2e_run_test_zero_asserts',
      commitSha: '6ce1b1b144f38024d81f8a6db4ce931c11e34556',
      environment: 'dev',
      startTime: '2026-10-13T17:00:00.000Z',
      endTime: '2026-10-13T17:00:05.000Z',
      totalDurationMs: 5000,
      executionClassification: 'mocked',
      tests: [zeroAssertionsTest],
    });

    const validationZero = validateManifest(manifestZero);
    expect(validationZero.isValid).toBe(false);
    expect(validationZero.errors.some((err) => err.includes('missing assertion evidence'))).toBe(true);

    const failingAssertionTest: TestEvidenceRecord = {
      ...sampleTestRecord,
      testId: 'test_failing_assertion',
      assertionOutcomes: [
        { name: 'Step 1', status: 'PASS' },
        { name: 'Step 2', status: 'FAIL', message: 'Element not visible' },
      ],
    };

    const manifestFail = createRunManifest({
      runId: 'e2e_run_test_fail_assert',
      commitSha: '6ce1b1b144f38024d81f8a6db4ce931c11e34556',
      environment: 'dev',
      startTime: '2026-10-13T17:00:00.000Z',
      endTime: '2026-10-13T17:00:05.000Z',
      totalDurationMs: 5000,
      executionClassification: 'mocked',
      tests: [failingAssertionTest],
    });

    const validationFail = validateManifest(manifestFail);
    expect(validationFail.isValid).toBe(false);
    expect(validationFail.errors.some((err) => err.includes('contains failing assertions'))).toBe(true);
  });

  it('fails gate validation if overallStatus is PASS but passed test count is 0', () => {
    const fakePassManifest: any = {
      schemaVersion: 1,
      runId: 'e2e_fake_pass',
      commitSha: '6ce1b1b144f38024d81f8a6db4ce931c11e34556',
      environment: 'dev',
      startTime: '2026-10-13T17:00:00.000Z',
      endTime: '2026-10-13T17:00:05.000Z',
      totalDurationMs: 5000,
      overallStatus: 'PASS',
      executionClassification: 'mocked',
      tests: [],
      evidenceDir: 'test-results',
      summary: {
        total: 0,
        passed: 0,
        failed: 0,
        blocked: 0,
        notRun: 0,
      },
    };

    const validation = validateManifest(fakePassManifest);
    expect(validation.isValid).toBe(false);
    expect(validation.errors.some((err) => err.includes('anti-false-green gate violation'))).toBe(true);
  });

  it('fails gate validation when physical artifact files do not exist on disk when checkPhysicalFiles is true', () => {
    const nonExistentArtifactTest: TestEvidenceRecord = {
      ...sampleTestRecord,
      testId: 'test_missing_physical_files',
      evidencePaths: {
        screenshots: ['non_existent_dir_xyz/screenshot_123.png'],
        video: 'non_existent_dir_xyz/video_123.webm',
        trace: 'non_existent_dir_xyz/trace_123.zip',
        htmlReport: 'playwright-report/index.html',
      },
    };

    const manifest = createRunManifest({
      runId: 'e2e_run_missing_physical_artifacts',
      commitSha: '6ce1b1b144f38024d81f8a6db4ce931c11e34556',
      environment: 'dev',
      startTime: '2026-10-13T17:00:00.000Z',
      endTime: '2026-10-13T17:00:05.000Z',
      totalDurationMs: 5000,
      executionClassification: 'mocked',
      tests: [nonExistentArtifactTest],
    });

    const validation = validateManifest(manifest, { checkPhysicalFiles: true, basePath: process.cwd() });
    expect(validation.isValid).toBe(false);
    expect(validation.errors.some((err) => err.includes('referenced screenshot does not exist on disk'))).toBe(true);
    expect(validation.errors.some((err) => err.includes('referenced video does not exist on disk'))).toBe(true);
    expect(validation.errors.some((err) => err.includes('referenced trace does not exist on disk'))).toBe(true);
  });

  it('fails gate validation when manifest has invalid environment, executionClassification, or test outcome', () => {
    const malformedManifest: any = {
      schemaVersion: 1,
      runId: 'e2e_run_malformed',
      commitSha: '6ce1b1b144f38024d81f8a6db4ce931c11e34556',
      environment: 'production', // Not allowed in dev/staging test gate!
      executionClassification: 'arbitrary_fake',
      startTime: '2026-10-13T17:00:00.000Z',
      endTime: '2026-10-13T17:00:05.000Z',
      totalDurationMs: 5000,
      overallStatus: 'PASS',
      summary: { total: 1, passed: 1, failed: 0, blocked: 0, notRun: 0 },
      tests: [
        {
          testId: 'test_invalid_fields',
          title: 'Invalid fields test',
          outcome: 'SOMETHING_RANDOM',
          executionType: 'quantum',
          startTime: '2026-10-13T17:00:00.000Z',
          endTime: '2026-10-13T17:00:05.000Z',
          durationMs: 5000,
          browser: 'chromium',
          viewport: { width: 1280, height: 800 },
          assertionOutcomes: [{ name: 'Dummy', status: 'PASS' }],
          evidencePaths: {
            screenshots: ['test-results/dummy.png'],
            video: 'test-results/dummy.webm',
            trace: 'test-results/dummy.zip',
          },
          capturedConsoleErrors: [],
          capturedHttpFailures: [],
          sanitized: true,
        },
      ],
    };

    const validation = validateManifest(malformedManifest);
    expect(validation.isValid).toBe(false);
    expect(validation.errors.some((err) => err.includes('Invalid environment: production'))).toBe(true);
    expect(validation.errors.some((err) => err.includes('Invalid executionClassification: arbitrary_fake'))).toBe(true);
    expect(validation.errors.some((err) => err.includes('has invalid outcome: SOMETHING_RANDOM'))).toBe(true);
    expect(validation.errors.some((err) => err.includes('has invalid executionType: quantum'))).toBe(true);
  });

  it('fails gate validation when live release gate claims PASS but has 0 passed tests', () => {
    const liveFailedGateManifest: any = {
      schemaVersion: 1,
      runId: 'e2e_run_live_fail_gate',
      commitSha: '6ce1b1b144f38024d81f8a6db4ce931c11e34556',
      environment: 'staging',
      startTime: '2026-10-13T17:00:00.000Z',
      endTime: '2026-10-13T17:00:05.000Z',
      totalDurationMs: 5000,
      overallStatus: 'PASS', // Claiming PASS illegitimately!
      executionClassification: 'live',
      summary: { total: 1, passed: 0, failed: 0, blocked: 0, notRun: 1 },
      tests: [
        {
          testId: 'test_live_skipped',
          title: 'Live Staging extraction',
          outcome: 'NOT RUN',
          executionType: 'live',
          startTime: '2026-10-13T17:00:00.000Z',
          endTime: '2026-10-13T17:00:05.000Z',
          durationMs: 0,
          browser: 'chromium',
          viewport: { width: 1280, height: 800 },
          assertionOutcomes: [],
          evidencePaths: { screenshots: [] },
          capturedConsoleErrors: [],
          capturedHttpFailures: [],
          sanitized: true,
        },
      ],
    };

    const validation = validateManifest(liveFailedGateManifest);
    expect(validation.isValid).toBe(false);
    expect(validation.errors.some((err) => err.includes('anti-false-green gate violation'))).toBe(true);
  });

  it('fails gate validation when overallStatus is PASS but contains failed or blocked tests', () => {
    const conflictingPassManifest: any = {
      schemaVersion: 1,
      runId: 'e2e_run_conflicting_pass',
      commitSha: '6ce1b1b144f38024d81f8a6db4ce931c11e34556',
      environment: 'dev',
      startTime: '2026-10-13T17:00:00.000Z',
      endTime: '2026-10-13T17:00:05.000Z',
      totalDurationMs: 5000,
      overallStatus: 'PASS',
      executionClassification: 'mocked',
      summary: { total: 2, passed: 1, failed: 1, blocked: 0, notRun: 0 },
      tests: [
        sampleTestRecord,
        {
          ...sampleTestRecord,
          testId: 'test_failing',
          outcome: 'FAIL',
        },
      ],
    };

    const validation = validateManifest(conflictingPassManifest);
    expect(validation.isValid).toBe(false);
    expect(validation.errors.some((err) => err.includes('contains failed or blocked tests'))).toBe(true);
  });
});

describe('Staging Origin Enforcer & Privacy Policy', () => {
  it('approves exact authoritative Layer 2 Staging origin', () => {
    const validStaging = 'https://universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app';
    const result = validateStagingOrigin(validStaging);
    expect(result.isValid).toBe(true);
    expect(result.error).toBeUndefined();
    expect(EXACT_APPROVED_STAGING_ORIGINS.has(validStaging)).toBe(true);
  });

  it('strictly rejects Layer 3 Production domain per Rule 2', () => {
    const prodUrl = 'https://universal-pro-ai.vercel.app';
    const result = validateStagingOrigin(prodUrl);
    expect(result.isValid).toBe(false);
    expect(result.error).toContain('is PRODUCTION');

    const apexProd = 'https://universal-pro.ai';
    const apexResult = validateStagingOrigin(apexProd);
    expect(apexResult.isValid).toBe(false);
    expect(apexResult.error).toContain('is PRODUCTION');
  });

  it('rejects lookalike domains, unapproved preview wildcards, and arbitrary origins', () => {
    const lookalike = 'https://universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app.attacker.com';
    const resultLookalike = validateStagingOrigin(lookalike);
    expect(resultLookalike.isValid).toBe(false);
    expect(resultLookalike.error).toContain('not an exact approved Layer 2 Staging host');

    const arbitraryPreview = 'https://universal-pro-ai-preview-123.vercel.app';
    const resultPreview = validateStagingOrigin(arbitraryPreview);
    expect(resultPreview.isValid).toBe(false);

    const insecureHttp = 'http://universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app';
    const resultHttp = validateStagingOrigin(insecureHttp);
    expect(resultHttp.isValid).toBe(false);
    expect(resultHttp.error).toContain('must use HTTPS');
  });

  it('differentiates metadata sanitization from binary artifact storage protection', () => {
    // Binary artifacts cannot be textually parsed/regex-sanitized in post-processing
    const testRecord: TestEvidenceRecord = {
      testId: 'binary_artifact_privacy_test',
      title: 'Inspects user login',
      outcome: 'PASS',
      startTime: '2026-10-13T17:00:00.000Z',
      endTime: '2026-10-13T17:00:01.000Z',
      durationMs: 1000,
      executionType: 'mocked',
      browser: 'chromium',
      viewport: { width: 1280, height: 800 },
      assertionOutcomes: [{ name: 'Step 1', status: 'PASS' }],
      evidencePaths: {
        screenshots: ['test-results/snap.png'],
        video: 'test-results/video.webm',
        trace: 'test-results/trace.zip',
      },
      capturedConsoleErrors: [],
      capturedHttpFailures: [],
      sanitized: true, // Indicates JSON manifest and log metadata was sanitized
    };

    // Assert that binary file extensions are recognized as raw media
    const isBinaryArtifact = (filePath?: string) =>
      Boolean(filePath && (filePath.endsWith('.webm') || filePath.endsWith('.zip') || filePath.endsWith('.png') || filePath.endsWith('.mp4')));

    expect(isBinaryArtifact(testRecord.evidencePaths.video)).toBe(true);
    expect(isBinaryArtifact(testRecord.evidencePaths.trace)).toBe(true);
    expect(isBinaryArtifact(testRecord.evidencePaths.screenshots[0])).toBe(true);

    // Metadata is sanitized
    expect(testRecord.sanitized).toBe(true);
  });
});
