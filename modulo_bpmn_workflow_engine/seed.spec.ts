import { test, expect } from '@playwright/test';

test.describe('App Detección Prod - entorno base', () => {
  test('seed', async ({ page }) => {
    await page.goto('/');

    await expect(
      page.getByRole('heading', {
        name: 'App Deteccion Prod',
      })
    ).toBeVisible();
  });
});
