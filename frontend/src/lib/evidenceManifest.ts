/**
 * Universal Pro AI - E2E Evidence Manifest Engine
 * Structures machine-readable test execution evidence, assertion outcomes, and environment metadata.
 */

import * as fs from 'node:fs';
import * as path from 'node:path';
import { sanitizeObject, sanitizeText } from './evidenceSanitizer';

export type ExecutionClassification = 'mocked' | 'live';
export type GateStatus = 'PASS' | 'FAIL' | 'BLOCKED' | 'NOT RUN';

export interface AssertionOutcome {
  name: string;
  status: 'PASS' | 'FAIL';
  message?: string;
}

export interface EvidencePaths {
  screenshots: string[];
  video?: string;
  trace?: string;
  htmlReport?: string;
}

export interface TestEvidenceRecord {
  testId: string;
  title: string;
  outcome: GateStatus;
  startTime: string;
  endTime: string;
  durationMs: number;
  executionType: ExecutionClassification;
  browser: string;
  viewport: { width: number; height: number };
  assertionOutcomes: AssertionOutcome[];
  evidencePaths: EvidencePaths;
  capturedConsoleErrors: string[];
  capturedHttpFailures: string[];
  sanitized: boolean;
}

export interface RunEvidenceManifest {
  schemaVersion: number;
  runId: string;
  commitSha: string;
  environment: 'dev' | 'staging' | 'ci';
  startTime: string;
  endTime: string;
  totalDurationMs: number;
  overallStatus: GateStatus;
  executionClassification: ExecutionClassification;
  tests: TestEvidenceRecord[];
  evidenceDir: string;
  summary: {
    total: number;
    passed: number;
    failed: number;
    blocked: number;
    notRun: number;
  };
}

/**
 * Validates a RunEvidenceManifest against mandatory release gate schema and artifact integrity requirements.
 */
export function validateManifest(
  manifest: RunEvidenceManifest,
  options?: {
    checkPhysicalFiles?: boolean;
    basePath?: string;
    expectedCommitSha?: string;
    expectedClassification?: ExecutionClassification;
  }
): { isValid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (!manifest) {
    return { isValid: false, errors: ['Manifest is null or undefined'] };
  }
  if (!manifest.schemaVersion || manifest.schemaVersion < 1) {
    errors.push('Missing or invalid schemaVersion');
  }
  if (!manifest.runId) {
    errors.push('Missing runId');
  }
  if (!manifest.commitSha) {
    errors.push('Missing commitSha');
  }
  if (options?.expectedCommitSha) {
    if (!manifest.commitSha) {
      errors.push(`Missing commitSha in manifest (expected ${options.expectedCommitSha})`);
    } else if (manifest.commitSha !== options.expectedCommitSha) {
      errors.push(`Commit SHA mismatch: expected ${options.expectedCommitSha}, got ${manifest.commitSha}`);
    }
  }
  if (!['dev', 'staging', 'ci'].includes(manifest.environment)) {
    errors.push(`Invalid environment: ${manifest.environment}`);
  }
  if (!['mocked', 'live'].includes(manifest.executionClassification)) {
    errors.push(`Invalid executionClassification: ${manifest.executionClassification}`);
  }
  if (options?.expectedClassification) {
    if (!manifest.executionClassification) {
      errors.push(`Missing executionClassification in manifest (expected ${options.expectedClassification})`);
    } else if (manifest.executionClassification !== options.expectedClassification) {
      errors.push(
        `Execution classification mismatch: expected ${options.expectedClassification}, got ${manifest.executionClassification}`
      );
    }
  }
  if (!manifest.summary) {
    errors.push('Missing summary object');
  } else {
    if (manifest.overallStatus === 'PASS' && manifest.summary.passed === 0) {
      errors.push('Manifest overallStatus is PASS but passed test count is 0 (anti-false-green gate violation)');
    }
    if (manifest.overallStatus === 'PASS' && (manifest.summary.failed > 0 || manifest.summary.blocked > 0)) {
      errors.push('Manifest overallStatus is PASS but contains failed or blocked tests');
    }
    if (manifest.overallStatus === 'PASS' && manifest.summary.notRun > 0) {
      errors.push('Manifest overallStatus is PASS but contains NOT RUN tests (anti-false-green gate violation)');
    }
    if (manifest.executionClassification === 'live' && manifest.summary.passed === 0 && manifest.overallStatus === 'PASS') {
      errors.push('Live Staging release gate requires at least 1 passing live extraction test; cannot be marked PASS');
    }
  }

  if (!Array.isArray(manifest.tests)) {
    errors.push('tests must be an array');
  } else {
    manifest.tests.forEach((t, idx) => {
      if (!t.testId) errors.push(`Test at index ${idx} missing testId`);
      if (!t.title) errors.push(`Test at index ${idx} missing title`);
      if (!['PASS', 'FAIL', 'BLOCKED', 'NOT RUN'].includes(t.outcome)) {
        errors.push(`Test "${t.title}" has invalid outcome: ${t.outcome}`);
      }
      if (!['mocked', 'live'].includes(t.executionType)) {
        errors.push(`Test "${t.title}" has invalid executionType: ${t.executionType}`);
      }
      if (!t.evidencePaths || !Array.isArray(t.evidencePaths.screenshots)) {
        errors.push(`Test "${t.title}" missing screenshots array`);
      } else if (t.outcome === 'PASS') {
        // Enforce mandatory artifacts for passing tests
        if (t.evidencePaths.screenshots.length === 0) {
          errors.push(`Test "${t.title}" passed but generated 0 screenshots (mandatory screenshot evidence missing)`);
        }
        if (!t.evidencePaths.video) {
          errors.push(`Test "${t.title}" passed but missing mandatory video recording artifact`);
        }
        if (!t.evidencePaths.trace) {
          errors.push(`Test "${t.title}" passed but missing mandatory Playwright trace artifact`);
        }

        // Verify physical artifact existence on disk if requested
        if (options?.checkPhysicalFiles) {
          const rootDir = options.basePath || process.cwd();
          for (const s of t.evidencePaths.screenshots) {
            const absPath = path.resolve(rootDir, s);
            if (!fs.existsSync(absPath)) {
              errors.push(`Test "${t.title}" passed but referenced screenshot does not exist on disk: ${s}`);
            }
          }
          if (t.evidencePaths.video) {
            const absPath = path.resolve(rootDir, t.evidencePaths.video);
            if (!fs.existsSync(absPath)) {
              errors.push(`Test "${t.title}" passed but referenced video does not exist on disk: ${t.evidencePaths.video}`);
            }
          }
          if (t.evidencePaths.trace) {
            const absPath = path.resolve(rootDir, t.evidencePaths.trace);
            if (!fs.existsSync(absPath)) {
              errors.push(`Test "${t.title}" passed but referenced trace does not exist on disk: ${t.evidencePaths.trace}`);
            }
          }
        }

        // Enforce explicit step assertion evidence
        if (!t.assertionOutcomes || t.assertionOutcomes.length === 0) {
          errors.push(`Test "${t.title}" passed in runner but recorded 0 assertion outcomes (missing assertion evidence)`);
        } else if (t.assertionOutcomes.some((a) => a.status === 'FAIL')) {
          errors.push(`Test "${t.title}" marked as PASS but contains failing assertions in evidence record`);
        }
      }
    });
  }

  return { isValid: errors.length === 0, errors };
}

/**
 * Creates and sanitizes a complete RunEvidenceManifest object.
 */
export function createRunManifest(params: {
  runId: string;
  commitSha: string;
  environment: 'dev' | 'staging' | 'ci';
  startTime: string;
  endTime: string;
  totalDurationMs: number;
  executionClassification: ExecutionClassification;
  tests: TestEvidenceRecord[];
  evidenceDir?: string;
}): RunEvidenceManifest {
  const tests = params.tests.map((t) => ({
    ...t,
    title: sanitizeText(t.title),
    assertionOutcomes: t.assertionOutcomes.map((a) => ({
      name: sanitizeText(a.name),
      status: a.status,
      message: a.message ? sanitizeText(a.message) : undefined,
    })),
    capturedConsoleErrors: t.capturedConsoleErrors.map((e) => sanitizeText(e)),
    capturedHttpFailures: t.capturedHttpFailures.map((h) => sanitizeText(h)),
    sanitized: true,
  }));

  const total = tests.length;
  const passed = tests.filter((t) => t.outcome === 'PASS').length;
  const failed = tests.filter((t) => t.outcome === 'FAIL').length;
  const blocked = tests.filter((t) => t.outcome === 'BLOCKED').length;
  const notRun = tests.filter((t) => t.outcome === 'NOT RUN').length;

  let overallStatus: GateStatus = 'PASS';
  if (failed > 0) {
    overallStatus = 'FAIL';
  } else if (blocked > 0) {
    overallStatus = 'BLOCKED';
  } else if (total === 0 || notRun === total || passed === 0) {
    overallStatus = 'NOT RUN';
  }

  const manifest: RunEvidenceManifest = {
    schemaVersion: 1,
    runId: params.runId,
    commitSha: params.commitSha,
    environment: params.environment,
    startTime: params.startTime,
    endTime: params.endTime,
    totalDurationMs: params.totalDurationMs,
    overallStatus,
    executionClassification: params.executionClassification,
    tests,
    evidenceDir: params.evidenceDir || 'test-results',
    summary: {
      total,
      passed,
      failed,
      blocked,
      notRun,
    },
  };

  return sanitizeObject(manifest);
}
