import { test, expect } from '@playwright/test';

test.describe('Operacion basica OPE-01 a OPE-04', () => {
  test('OPE-01 - Thread nuevo sin ejecutar queda en NO_EXISTE', async ({ page }) => {
    // 1. Cargar la aplicacion.
    await page.goto('/');

    // 2. Crear un thread nuevo sin ejecutar el workflow.
    await page.getByRole('button', { name: /Nuevo thread/i }).click();

    // 3. Comprobar el estado observable NO_EXISTE.
    await expect(page.getByRole('alert').filter({ hasText: 'NO_EXISTE' }).first()).toBeVisible();
    await expect(page.getByText('NO_EXISTE', { exact: false }).first()).toBeVisible();
  });
});