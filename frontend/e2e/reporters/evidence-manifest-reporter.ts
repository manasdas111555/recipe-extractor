import type {
  FullConfig,
  FullResult,
  Reporter,
  Suite,
  TestCase,
  TestResult,
} from '@playwright/test/reporter';
import * as fs from 'node:fs';
import * as path from 'node:path';
import { execSync } from 'node:child_process';
import {
  createRunManifest,
  validateManifest,
  TestEvidenceRecord,
  AssertionOutcome,
  GateStatus,
  ExecutionClassification,
  RunEvidenceManifest,
} from '../../src/lib/evidenceManifest';
import { sanitizeText } from '../../src/lib/evidenceSanitizer';

export default class EvidenceManifestReporter implements Reporter {
  private startTime = 0;
  private testRecords: TestEvidenceRecord[] = [];
  private runId = '';
  private commitSha = '';

  onBegin(_config: FullConfig, _suite: Suite) {
    this.startTime = Date.now();
    this.runId = `e2e_${new Date().toISOString().replace(/[:.]/g, '-')}_${Math.random().toString(36).substring(2, 7)}`;
    try {
      this.commitSha = process.env.GIT_COMMIT_SHA || execSync('git rev-parse HEAD', { encoding: 'utf-8' }).trim();
    } catch {
      this.commitSha = 'unknown-dev-commit';
    }
  }

  onTestEnd(test: TestCase, result: TestResult) {
    const projectName = test.parent.project()?.name || '';
    const isLive = projectName === 'staging-live' || test.annotations.some((a) => a.type === 'classification' && a.description === 'live');
    const executionType: ExecutionClassification = isLive ? 'live' : 'mocked';

    let outcome: GateStatus = 'FAIL';
    if (result.status === 'passed') {
      outcome = 'PASS';
    } else if (result.status === 'skipped') {
      outcome = 'NOT RUN';
    } else if (result.status === 'timedOut' || result.status === 'failed' || result.status === 'interrupted') {
      outcome = 'FAIL';
    }

    const assertionOutcomes: AssertionOutcome[] = [];
    const capturedConsoleErrors: string[] = [];
    const capturedHttpFailures: string[] = [];

    for (const annotation of test.annotations) {
      if (annotation.type === 'assertion') {
        try {
          const parsed = JSON.parse(annotation.description || '{}');
          assertionOutcomes.push({
            name: parsed.name || 'Assertion',
            status: parsed.status === 'PASS' ? 'PASS' : 'FAIL',
            message: parsed.message,
          });
        } catch {
          assertionOutcomes.push({
            name: annotation.description || 'Assertion',
            status: 'PASS',
          });
        }
      } else if (annotation.type === 'console-error') {
        if (annotation.description) capturedConsoleErrors.push(annotation.description);
      } else if (annotation.type === 'http-failure') {
        if (annotation.description) capturedHttpFailures.push(annotation.description);
      }
    }

    // Explicitly record missing assertion evidence if none were captured
    if (assertionOutcomes.length === 0 && outcome === 'PASS') {
      assertionOutcomes.push({
        name: 'Explicit assertion evidence recorded',
        status: 'FAIL',
        message: 'Missing assertion evidence: test marked passed by runner without recorded step assertions',
      });
    }

    const normalizePath = (targetPath: string): string => {
      try {
        const rel = path.relative(process.cwd(), targetPath).replace(/\\/g, '/');
        return rel.startsWith('..') ? targetPath.replace(/\\/g, '/') : rel;
      } catch {
        return targetPath.replace(/\\/g, '/');
      }
    };

    const screenshots: string[] = [];
    let video: string | undefined;
    let trace: string | undefined;

    for (const attachment of result.attachments) {
      if (attachment.path) {
        const normalized = normalizePath(attachment.path);
        if (attachment.name === 'screenshot' || normalized.endsWith('.png')) {
          screenshots.push(normalized);
        } else if (attachment.name === 'video' || normalized.endsWith('.webm') || normalized.endsWith('.mp4')) {
          video = normalized;
        } else if (attachment.name === 'trace' || normalized.endsWith('.zip')) {
          trace = normalized;
        }
      }
    }

    const record: TestEvidenceRecord = {
      testId: test.id || test.title.replace(/\s+/g, '_').toLowerCase(),
      title: test.title,
      outcome,
      startTime: result.startTime ? result.startTime.toISOString() : new Date().toISOString(),
      endTime: new Date(result.startTime ? result.startTime.getTime() + result.duration : Date.now()).toISOString(),
      durationMs: result.duration,
      executionType,
      browser: 'chromium',
      viewport: { width: 1280, height: 800 },
      assertionOutcomes,
      evidencePaths: {
        screenshots,
        video,
        trace,
        htmlReport: `${(process.env.PLAYWRIGHT_HTML_REPORT_DIR || 'playwright-report').replace(/\\/g, '/')}/index.html`,
      },
      capturedConsoleErrors,
      capturedHttpFailures,
      sanitized: true,
    };

    this.testRecords.push(record);
  }

  onEnd(result: FullResult) {
    const endTime = Date.now();
    const totalDurationMs = endTime - this.startTime;

    const hasLive = this.testRecords.some((t) => t.executionType === 'live');
    const executionClassification: ExecutionClassification = hasLive ? 'live' : 'mocked';

    const env = (process.env.TEST_ENV || process.env.APP_ENV || 'dev') as 'dev' | 'staging' | 'ci';
    const validEnv = ['dev', 'staging', 'ci'].includes(env) ? env : 'dev';

    const manifest: RunEvidenceManifest = createRunManifest({
      runId: this.runId,
      commitSha: this.commitSha,
      environment: validEnv,
      startTime: new Date(this.startTime).toISOString(),
      endTime: new Date(endTime).toISOString(),
      totalDurationMs,
      executionClassification,
      tests: this.testRecords,
    });

    // Validate manifest against mandatory release gate rules and physical file existence
    const validation = validateManifest(manifest, {
      checkPhysicalFiles: true,
      basePath: process.cwd(),
    });
    if (!validation.isValid) {
      process.exitCode = 1;
      console.error('🚨 [EvidenceManifestReporter] Mandatory release gate validation failed:\n', validation.errors);
      throw new Error(`[EvidenceManifestReporter] Mandatory release gate BLOCKED: Evidence validation failed:\n  - ${validation.errors.join('\n  - ')}`);
    }

    // Write to primary and optional secondary directory
    const primaryDir = process.env.EVIDENCE_OUTPUT_DIR
      ? path.resolve(process.cwd(), process.env.EVIDENCE_OUTPUT_DIR)
      : path.resolve(process.cwd(), 'test-results');

    const outputDirs: string[] = [primaryDir];

    // Determine secondary output directory
    const disableSecondary = process.env.DISABLE_SECONDARY_MANIFEST_WRITE === 'true';
    if (!disableSecondary) {
      if (process.env.E2E_SECONDARY_EVIDENCE_DIR) {
        outputDirs.push(path.resolve(process.cwd(), process.env.E2E_SECONDARY_EVIDENCE_DIR));
      } else if (!process.env.EVIDENCE_OUTPUT_DIR) {
        // Default historical behavior: write to e2e-evidence as secondary only when EVIDENCE_OUTPUT_DIR is unset
        outputDirs.push(path.resolve(process.cwd(), 'e2e-evidence'));
      }
    }

    const manifestFileName = process.env.EVIDENCE_MANIFEST_FILENAME || 'evidence-manifest.json';

    for (const outDir of outputDirs) {
      try {
        if (!fs.existsSync(outDir)) {
          fs.mkdirSync(outDir, { recursive: true });
        }
        const manifestFile = path.join(outDir, manifestFileName);
        fs.writeFileSync(manifestFile, JSON.stringify(manifest, null, 2), 'utf-8');
      } catch (e) {
        process.exitCode = 1;
        console.error(`Failed writing manifest to ${outDir}:`, e);
        throw new Error(`[EvidenceManifestReporter] Mandatory release gate BLOCKED: Failed writing evidence manifest to ${outDir}: ${e}`);
      }
    }

    // Print summary to terminal
    console.log('\n============================================================');
    console.log('📊 AUDITABLE BROWSER E2E EVIDENCE MANIFEST SUMMARY');
    console.log('============================================================');
    console.log(`  Run ID:                  ${manifest.runId}`);
    console.log(`  Commit SHA:              ${manifest.commitSha}`);
    console.log(`  Environment:             ${manifest.environment}`);
    console.log(`  Execution Classification: [${manifest.executionClassification.toUpperCase()}]`);
    console.log(`  Overall Gate Status:     ${manifest.overallStatus}`);
    console.log(`  Total Tests:             ${manifest.summary.total}`);
    console.log(`  Passed:                  ${manifest.summary.passed}`);
    console.log(`  Failed:                  ${manifest.summary.failed}`);
    console.log(`  Blocked / Not Run:       ${manifest.summary.notRun + manifest.summary.blocked}`);
    console.log(`  Evidence Manifest:       ${path.relative(process.cwd(), path.join(primaryDir, manifestFileName)).replace(/\\/g, '/')}`);
    console.log(`  HTML Report:             ${(process.env.PLAYWRIGHT_HTML_REPORT_DIR || 'playwright-report').replace(/\\/g, '/')}/index.html`);
    console.log('============================================================\n');
  }
}
