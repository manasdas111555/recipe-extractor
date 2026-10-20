import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import * as path from 'node:path';
import * as fs from 'node:fs';
import * as os from 'node:os';
import { createRunManifest, validateManifest, TestEvidenceRecord } from '../evidenceManifest';

describe('E2E Evidence Artifact Isolation & Non-Destructive Framework (UPA-1403)', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    process.env = { ...originalEnv };
  });

  afterEach(() => {
    process.env = originalEnv;
  });

  it('preserves historical e2e-evidence by omitting secondary write when EVIDENCE_OUTPUT_DIR is set', () => {
    // When EVIDENCE_OUTPUT_DIR is set without explicit E2E_SECONDARY_EVIDENCE_DIR,
    // the secondary output directory MUST NOT be written to.
    process.env.EVIDENCE_OUTPUT_DIR = 'test-results/isolated-staging-smoke';
    delete process.env.E2E_SECONDARY_EVIDENCE_DIR;
    delete process.env.DISABLE_SECONDARY_MANIFEST_WRITE;

    const primaryDir = process.env.EVIDENCE_OUTPUT_DIR
      ? path.resolve(process.cwd(), process.env.EVIDENCE_OUTPUT_DIR)
      : path.resolve(process.cwd(), 'test-results');

    const outputDirs: string[] = [primaryDir];
    const disableSecondary = process.env.DISABLE_SECONDARY_MANIFEST_WRITE === 'true';

    if (!disableSecondary) {
      if (process.env.E2E_SECONDARY_EVIDENCE_DIR) {
        outputDirs.push(path.resolve(process.cwd(), process.env.E2E_SECONDARY_EVIDENCE_DIR));
      } else if (!process.env.EVIDENCE_OUTPUT_DIR) {
        outputDirs.push(path.resolve(process.cwd(), 'e2e-evidence'));
      }
    }

    expect(outputDirs).toHaveLength(1);
    expect(outputDirs[0]).toBe(path.resolve(process.cwd(), 'test-results/isolated-staging-smoke'));
    expect(outputDirs).not.toContain(path.resolve(process.cwd(), 'e2e-evidence'));
  });

  it('defaults to dual write (test-results and e2e-evidence) when no isolation env vars are set', () => {
    delete process.env.EVIDENCE_OUTPUT_DIR;
    delete process.env.E2E_SECONDARY_EVIDENCE_DIR;
    delete process.env.DISABLE_SECONDARY_MANIFEST_WRITE;

    const primaryDir = process.env.EVIDENCE_OUTPUT_DIR
      ? path.resolve(process.cwd(), process.env.EVIDENCE_OUTPUT_DIR)
      : path.resolve(process.cwd(), 'test-results');

    const outputDirs: string[] = [primaryDir];
    const disableSecondary = process.env.DISABLE_SECONDARY_MANIFEST_WRITE === 'true';

    if (!disableSecondary) {
      if (process.env.E2E_SECONDARY_EVIDENCE_DIR) {
        outputDirs.push(path.resolve(process.cwd(), process.env.E2E_SECONDARY_EVIDENCE_DIR));
      } else if (!process.env.EVIDENCE_OUTPUT_DIR) {
        outputDirs.push(path.resolve(process.cwd(), 'e2e-evidence'));
      }
    }

    expect(outputDirs).toHaveLength(2);
    expect(outputDirs[0]).toBe(path.resolve(process.cwd(), 'test-results'));
    expect(outputDirs[1]).toBe(path.resolve(process.cwd(), 'e2e-evidence'));
  });

  it('suppresses secondary write completely when DISABLE_SECONDARY_MANIFEST_WRITE is true', () => {
    delete process.env.EVIDENCE_OUTPUT_DIR;
    process.env.DISABLE_SECONDARY_MANIFEST_WRITE = 'true';

    const primaryDir = process.env.EVIDENCE_OUTPUT_DIR
      ? path.resolve(process.cwd(), process.env.EVIDENCE_OUTPUT_DIR)
      : path.resolve(process.cwd(), 'test-results');

    const outputDirs: string[] = [primaryDir];
    const disableSecondary = process.env.DISABLE_SECONDARY_MANIFEST_WRITE === 'true';

    if (!disableSecondary) {
      if (process.env.E2E_SECONDARY_EVIDENCE_DIR) {
        outputDirs.push(path.resolve(process.cwd(), process.env.E2E_SECONDARY_EVIDENCE_DIR));
      } else if (!process.env.EVIDENCE_OUTPUT_DIR) {
        outputDirs.push(path.resolve(process.cwd(), 'e2e-evidence'));
      }
    }

    expect(outputDirs).toHaveLength(1);
    expect(outputDirs[0]).toBe(path.resolve(process.cwd(), 'test-results'));
  });

  it('allows explicit secondary directory targeting via E2E_SECONDARY_EVIDENCE_DIR', () => {
    process.env.EVIDENCE_OUTPUT_DIR = 'test-results/run-101';
    process.env.E2E_SECONDARY_EVIDENCE_DIR = 'test-results/backup-101';

    const primaryDir = process.env.EVIDENCE_OUTPUT_DIR
      ? path.resolve(process.cwd(), process.env.EVIDENCE_OUTPUT_DIR)
      : path.resolve(process.cwd(), 'test-results');

    const outputDirs: string[] = [primaryDir];
    const disableSecondary = process.env.DISABLE_SECONDARY_MANIFEST_WRITE === 'true';

    if (!disableSecondary) {
      if (process.env.E2E_SECONDARY_EVIDENCE_DIR) {
        outputDirs.push(path.resolve(process.cwd(), process.env.E2E_SECONDARY_EVIDENCE_DIR));
      } else if (!process.env.EVIDENCE_OUTPUT_DIR) {
        outputDirs.push(path.resolve(process.cwd(), 'e2e-evidence'));
      }
    }

    expect(outputDirs).toHaveLength(2);
    expect(outputDirs[0]).toBe(path.resolve(process.cwd(), 'test-results/run-101'));
    expect(outputDirs[1]).toBe(path.resolve(process.cwd(), 'test-results/backup-101'));
  });

  it('supports custom manifest filename via EVIDENCE_MANIFEST_FILENAME', () => {
    process.env.EVIDENCE_MANIFEST_FILENAME = 'staging-smoke-manifest.json';
    const manifestFileName = process.env.EVIDENCE_MANIFEST_FILENAME || 'evidence-manifest.json';
    expect(manifestFileName).toBe('staging-smoke-manifest.json');
  });

  it('calculates screenshot destination directory from EVIDENCE_OUTPUT_DIR', () => {
    process.env.EVIDENCE_OUTPUT_DIR = 'custom-e2e-artifacts';
    const baseOutputDir = process.env.EVIDENCE_OUTPUT_DIR || 'test-results';
    const screenshotDir = path.resolve(process.cwd(), baseOutputDir, 'screenshots');
    expect(screenshotDir).toBe(path.resolve(process.cwd(), 'custom-e2e-artifacts', 'screenshots'));
  });

  it('formats htmlReport path dynamically with PLAYWRIGHT_HTML_REPORT_DIR', () => {
    process.env.PLAYWRIGHT_HTML_REPORT_DIR = 'custom-playwright-report';
    const htmlReport = `${(process.env.PLAYWRIGHT_HTML_REPORT_DIR || 'playwright-report').replace(/\\/g, '/')}/index.html`;
    expect(htmlReport).toBe('custom-playwright-report/index.html');
  });

  it('successfully validates manifest with physical files in an isolated custom directory', () => {
    // Create an ephemeral test directory inside OS temp
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'upa-evidence-test-'));
    try {
      const screenshotsDir = path.join(tmpDir, 'screenshots');
      fs.mkdirSync(screenshotsDir, { recursive: true });

      const screenshotFile = path.join(screenshotsDir, 'step1.png');
      const videoFile = path.join(tmpDir, 'video.webm');
      const traceFile = path.join(tmpDir, 'trace.zip');

      fs.writeFileSync(screenshotFile, 'fake_png_data');
      fs.writeFileSync(videoFile, 'fake_video_data');
      fs.writeFileSync(traceFile, 'fake_trace_data');

      // Relative paths from tmpDir
      const record: TestEvidenceRecord = {
        testId: 'smoke_staging_hero',
        title: 'Smoke Staging Hero Test',
        outcome: 'PASS',
        startTime: '2026-10-20T12:00:00.000Z',
        endTime: '2026-10-20T12:00:05.000Z',
        durationMs: 5000,
        executionType: 'live',
        browser: 'chromium',
        viewport: { width: 1280, height: 800 },
        assertionOutcomes: [
          { name: 'Initial CTA Disabled Check', status: 'PASS' },
          { name: 'Fixture URL Input Verification', status: 'PASS' },
        ],
        evidencePaths: {
          screenshots: ['screenshots/step1.png'],
          video: 'video.webm',
          trace: 'trace.zip',
          htmlReport: 'custom-report/index.html',
        },
        capturedConsoleErrors: [],
        capturedHttpFailures: [],
        sanitized: true,
      };

      const manifest = createRunManifest({
        runId: 'e2e_isolated_staging_run_01',
        commitSha: '332d766439d01832439303c417f0666c9356acc8',
        environment: 'staging',
        startTime: '2026-10-20T12:00:00.000Z',
        endTime: '2026-10-20T12:00:05.000Z',
        totalDurationMs: 5000,
        executionClassification: 'live',
        tests: [record],
      });

      const validation = validateManifest(manifest, {
        checkPhysicalFiles: true,
        basePath: tmpDir,
      });

      expect(validation.isValid).toBe(true);
      expect(validation.errors).toEqual([]);
    } finally {
      // Deterministic cleanup
      fs.rmSync(tmpDir, { recursive: true, force: true });
    }
  });
});
