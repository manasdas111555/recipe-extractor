import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock @playwright/test so importing smoke.staging.e2e does not throw outside Playwright runner
vi.mock('@playwright/test', () => {
  const fn: any = vi.fn();
  fn.describe = Object.assign(vi.fn(), { configure: vi.fn() });
  fn.skip = vi.fn();
  return {
    test: fn,
    expect: vi.fn(),
  };
});

import {
  resolveStagingApiOrigin,
  isMonitoredHttpErrorUrl,
  validateNavigationResponse,
} from '../../../e2e/specs/smoke.staging.e2e';

describe('GAP-03: Staging Smoke-Test HTTP Error Detection & Navigation Guard', () => {
  describe('resolveStagingApiOrigin', () => {
    it('defaults to documented OCI Staging VM IP when no argument or env var is present', () => {
      const originalEnv = process.env.STAGING_API_URL;
      delete process.env.STAGING_API_URL;
      try {
        const origin = resolveStagingApiOrigin();
        expect(origin).toBe('http://129.225.86.241');
      } finally {
        if (originalEnv) process.env.STAGING_API_URL = originalEnv;
      }
    });

    it('extracts origin from URL containing path segments (e.g. /health)', () => {
      const origin = resolveStagingApiOrigin('http://129.225.86.241/health');
      expect(origin).toBe('http://129.225.86.241');
    });

    it('extracts origin from custom HTTPS FQDN', () => {
      const origin = resolveStagingApiOrigin('https://staging-api.universal-pro-ai.com/api/v1');
      expect(origin).toBe('https://staging-api.universal-pro-ai.com');
    });

    it('strips trailing slashes from raw strings', () => {
      const origin = resolveStagingApiOrigin('http://129.225.86.241/');
      expect(origin).toBe('http://129.225.86.241');
    });
  });

  describe('isMonitoredHttpErrorUrl', () => {
    const stagingBase = 'https://universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app';
    const stagingApiOrigin = 'http://129.225.86.241';

    it('matches root-relative paths', () => {
      expect(isMonitoredHttpErrorUrl('/api/v1/health', stagingBase, stagingApiOrigin)).toBe(true);
      expect(isMonitoredHttpErrorUrl('/manifest.json', stagingBase, stagingApiOrigin)).toBe(true);
    });

    it('matches frontend Staging origin URLs', () => {
      expect(
        isMonitoredHttpErrorUrl(`${stagingBase}/api/v1/extract`, stagingBase, stagingApiOrigin)
      ).toBe(true);
      expect(
        isMonitoredHttpErrorUrl(`${stagingBase}/_next/static/chunks/main.js`, stagingBase, stagingApiOrigin)
      ).toBe(true);
    });

    it('matches backend OCI Staging API origin URLs (cross-origin backend)', () => {
      expect(
        isMonitoredHttpErrorUrl(`${stagingApiOrigin}/health`, stagingBase, stagingApiOrigin)
      ).toBe(true);
      expect(
        isMonitoredHttpErrorUrl(`${stagingApiOrigin}/api/v1/extract`, stagingBase, stagingApiOrigin)
      ).toBe(true);
    });

    it('rejects external/untracked third-party URLs', () => {
      expect(
        isMonitoredHttpErrorUrl('https://fonts.googleapis.com/css2', stagingBase, stagingApiOrigin)
      ).toBe(false);
      expect(
        isMonitoredHttpErrorUrl('https://analytics.google.com/collect', stagingBase, stagingApiOrigin)
      ).toBe(false);
      expect(
        isMonitoredHttpErrorUrl('https://unrelated-domain.com/failure', stagingBase, stagingApiOrigin)
      ).toBe(false);
    });

    it('rejects empty or null URLs safely', () => {
      expect(isMonitoredHttpErrorUrl('', stagingBase, stagingApiOrigin)).toBe(false);
      expect(isMonitoredHttpErrorUrl(null as any, stagingBase, stagingApiOrigin)).toBe(false);
    });
  });

  describe('validateNavigationResponse', () => {
    const targetUrl = 'https://universal-pro-ai-git-staging-manasprasannadas-projects.vercel.app';

    it('fails closed when page.goto returns null response', () => {
      const mockTracker = { recordAssertion: vi.fn() };
      expect(() => {
        validateNavigationResponse(null, targetUrl, mockTracker);
      }).toThrowError(/\[NAVIGATION FAILURE\] page\.goto\('.*'\) returned no HTTP response \(null\)\. Release gate fails closed\./);

      expect(mockTracker.recordAssertion).toHaveBeenCalledWith(
        'Core route / responds with HTTP 200 OK',
        'FAIL',
        expect.stringContaining('null response')
      );
    });

    it('fails closed when page.goto returns undefined response', () => {
      const mockTracker = { recordAssertion: vi.fn() };
      expect(() => {
        validateNavigationResponse(undefined, targetUrl, mockTracker);
      }).toThrowError(/\[NAVIGATION FAILURE\]/);

      expect(mockTracker.recordAssertion).toHaveBeenCalledWith(
        'Core route / responds with HTTP 200 OK',
        'FAIL',
        expect.anything()
      );
    });

    it('fails closed when application returns non-200 HTTP status (e.g. 500)', () => {
      const mockTracker = { recordAssertion: vi.fn() };
      const response500 = { status: () => 500 };

      expect(() => {
        validateNavigationResponse(response500, targetUrl, mockTracker);
      }).toThrowError(/\[NAVIGATION FAILURE\] Staging application returned non-200 HTTP status: 500/);

      expect(mockTracker.recordAssertion).toHaveBeenCalledWith(
        'Core route / responds with HTTP 200 OK',
        'FAIL',
        expect.stringContaining('500')
      );
    });

    it('fails closed when application returns 404 Not Found', () => {
      const mockTracker = { recordAssertion: vi.fn() };
      const response404 = { status: () => 404 };

      expect(() => {
        validateNavigationResponse(response404, targetUrl, mockTracker);
      }).toThrowError(/\[NAVIGATION FAILURE\] Staging application returned non-200 HTTP status: 404/);

      expect(mockTracker.recordAssertion).toHaveBeenCalledWith(
        'Core route / responds with HTTP 200 OK',
        'FAIL',
        expect.stringContaining('404')
      );
    });

    it('succeeds and records PASS assertion when application returns HTTP 200 OK', () => {
      const mockTracker = { recordAssertion: vi.fn() };
      const response200 = { status: () => 200 };

      const status = validateNavigationResponse(response200, targetUrl, mockTracker);
      expect(status).toBe(200);

      expect(mockTracker.recordAssertion).toHaveBeenCalledWith(
        'Core route / responds with HTTP 200 OK',
        'PASS'
      );
    });
  });
});
