// spec: specs/PLAN_02_CONTEXTO_PRODUCTO.md
// seed: seed.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Contexto, producto, fuente y nota', () => {
  test('PRD-01 - Seleccionar producto muestra producto y clasificacion asociada', async ({ page }) => {
    // 1. Iniciar un caso independiente y verificar Producto y Clasificacion.
    await page.goto('/');
    const producto = page.getByLabel('Producto empresarial / observado');
    await expect(producto).toBeVisible();
    await expect(page.getByText('Clasificacion', { exact: true })).toBeVisible();

    // 2. Seleccionar el producto real disponible.
    await producto.click();
    await page
      .getByRole('option', { name: '0000051433 — Prudential Comfort Total G 4x20' })
      .click();
    await expect(producto).toHaveAttribute('aria-label', /Selected 0000051433/);

    // 3. Verificar la clasificacion asociada visible.
    await expect(
      page.getByText('Absorbentes / ZAIMELLA / Incontinencia / Confort Total', { exact: true })
    ).toBeVisible();
  });
});