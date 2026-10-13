import { test, expect } from '@playwright/test';

test.describe('Universal Pro AI - UI Smoke Suite', () => {
  test('renders homepage, accepts URL, and displays extracted recipe with mocked API', async ({ page }) => {
    const consoleErrors: string[] = [];
    const internalServerErrors: string[] = [];

    // Capture unhandled console errors
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    // Capture failed internal server requests (5xx)
    page.on('response', (response) => {
      if (response.status() >= 500) {
        internalServerErrors.push(`${response.status()} ${response.url()}`);
      }
    });

    // Deterministically mock /api/v1/extract (no live providers / no cloud API calls)
    await page.route('**/api/v1/extract', async (route) => {
      if (route.request().method() === 'POST') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            status: 'completed',
            data: {
              title: 'Smoked Butter Garlic Paneer',
              summary: 'Crispy paneer cubes tossed in aromatic garlic butter and smoky spices.',
              category: 'Recipe',
              ingredients: [
                { name: 'Paneer', quantity: '250', unit: 'g' },
                { name: 'Butter', quantity: '2', unit: 'tbsp' },
              ],
              instructions: [
                'Cut paneer into bite-sized cubes.',
                'Melt butter in a pan and sauté minced garlic until golden.',
              ],
            },
          }),
        });
      } else {
        await route.continue();
      }
    });

    // 1. Launch & Navigate
    await page.goto('/');

    // 2. Verify page title and main heading
    await expect(page).toHaveTitle(/Universal Pro AI/i);
    const mainHeading = page.locator('h1');
    await expect(mainHeading).toBeVisible();

    // 3. Locate inputs verified against real page.tsx DOM
    const urlInput = page.getByLabel('Video URL');
    await expect(urlInput).toBeVisible();

    const domainSelect = page.getByLabel('Content Domain Classifier');
    await expect(domainSelect).toBeVisible();

    const submitBtn = page.getByLabel('Get video intelligence');
    await expect(submitBtn).toBeVisible();

    // 4. Fill URL and trigger extraction
    await urlInput.fill('https://www.instagram.com/reel/C1234567890/');
    await expect(submitBtn).toBeEnabled();
    await submitBtn.click();

    // 5. Verify visible DOM output rendered from extraction
    const recipeTitle = page.getByRole('heading', { level: 2, name: /Smoked Butter Garlic Paneer/i });
    await expect(recipeTitle).toBeVisible({ timeout: 15_000 });

    const recipeSummary = page.getByText(/Crispy paneer cubes tossed in aromatic garlic butter/i);
    await expect(recipeSummary).toBeVisible();

    // 6. Fail on unexpected application console errors or 5xx responses
    expect(consoleErrors, `Unexpected browser console errors: ${consoleErrors.join(', ')}`).toEqual([]);
    expect(internalServerErrors, `Unexpected 5xx internal server errors: ${internalServerErrors.join(', ')}`).toEqual([]);
  });
});
