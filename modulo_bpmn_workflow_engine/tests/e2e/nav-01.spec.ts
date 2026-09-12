// spec: specs/PLAN_01_NAVEGACION_SESION.md
// seed: tests/e2e/seed.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Navegacion y sesion', () => {
  test('NAV-01 - La apertura muestra el encabezado y la salud del sistema', async ({ page }) => {
    // 1. Iniciar en estado fresco y navegar a page.goto('/').
    await page.goto('/');

    // 2. Verificar que es visible un encabezado de nivel 1 cuyo nombre contiene 'App Deteccion Prod'.
    await expect(
      page.getByRole('heading', { name: /App Deteccion Prod/i, level: 1 })
    ).toBeVisible();

    // 3. Verificar que es visible el encabezado 'Salud del sistema'.
    await expect(
      page.getByRole('heading', { name: 'Salud del sistema', level: 3 })
    ).toBeVisible();
  });
});
