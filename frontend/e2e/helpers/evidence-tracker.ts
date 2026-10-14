import { Page, TestInfo } from '@playwright/test';
import * as fs from 'node:fs';
import * as path from 'node:path';
import { sanitizeText, sanitizeUrl } from '../../src/lib/evidenceSanitizer';

export class EvidenceTracker {
  private page: Page;
  private testInfo: TestInfo;
  private classification: 'mocked' | 'live';
  public consoleErrors: string[] = [];
  public httpFailures: string[] = [];

  constructor(page: Page, testInfo: TestInfo, classification: 'mocked' | 'live' = 'mocked') {
    this.page = page;
    this.testInfo = testInfo;
    this.classification = classification;

    // Register classification
    this.testInfo.annotations.push({
      type: 'classification',
      description: this.classification,
    });

    this.attachListeners();
  }

  private attachListeners() {
    this.page.on('console', (msg) => {
      if (msg.type() === 'error') {
        const sanitized = sanitizeText(msg.text());
        this.consoleErrors.push(sanitized);
        this.testInfo.annotations.push({
          type: 'console-error',
          description: sanitized,
        });
      }
    });

    this.page.on('response', (response) => {
      // Flag unhandled server errors (5xx)
      if (response.status() >= 500) {
        const sanitizedUrl = sanitizeUrl(response.url());
        const failureStr = `${response.status()} ${sanitizedUrl}`;
        this.httpFailures.push(failureStr);
        this.testInfo.annotations.push({
          type: 'http-failure',
          description: failureStr,
        });
      }
    });
  }

  /**
   * Explicitly record an assertion outcome into the evidence manifest.
   */
  recordAssertion(name: string, status: 'PASS' | 'FAIL', message?: string) {
    this.testInfo.annotations.push({
      type: 'assertion',
      description: JSON.stringify({
        name: sanitizeText(name),
        status,
        message: message ? sanitizeText(message) : undefined,
      }),
    });
  }

  /**
   * Capture a reviewable evidence screenshot of a key UI state and attach it to test results.
   */
  async captureStepScreenshot(stepName: string): Promise<string> {
    const screenshotDir = path.resolve(process.cwd(), 'test-results', 'screenshots');
    if (!fs.existsSync(screenshotDir)) {
      fs.mkdirSync(screenshotDir, { recursive: true });
    }

    const cleanStepName = stepName.toLowerCase().replace(/[^a-z0-9_-]/g, '_');
    const screenshotPath = path.join(screenshotDir, `${cleanStepName}_${Date.now()}.png`);

    await this.page.screenshot({
      path: screenshotPath,
      fullPage: true,
    });

    await this.testInfo.attach(cleanStepName, {
      path: screenshotPath,
      contentType: 'image/png',
    });

    return screenshotPath;
  }
}
