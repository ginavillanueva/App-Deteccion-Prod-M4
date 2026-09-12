// spec: specs/PLAN_02_CONTEXTO_PRODUCTO.md
// seed: seed.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Contexto, producto, fuente y nota', () => {
  test('CTX-01 - Seleccionar Departamento, Cadena y Sala refleja la sala empresarial', async ({ page }) => {
    // 1. Iniciar un caso independiente y verificar los selectores de contexto.
    await page.goto('/');
    const departamento = page.getByLabel('Departamento');
    const cadena = page.getByLabel('Cadena');
    const sala = page.getByLabel('Sala');
    await expect(departamento).toBeVisible();
    await expect(cadena).toBeVisible();
    await expect(sala).toBeVisible();

    // 2. Seleccionar el departamento real disponible.
    await departamento.click();
    await page.getByRole('option', { name: '2 - Santa Cruz' }).click();
    await expect(departamento).toHaveAttribute('aria-label', /Selected 2 - Santa Cruz\. Departamento/);

    // 3. Seleccionar la cadena y comprobar que Sala sigue disponible.
    await cadena.click();
    await page.getByRole('option', { name: 'Brands' }).click();
    await expect(cadena).toHaveAttribute('aria-label', /Selected Brands\. Cadena/);
    await expect(sala).toBeVisible();

    // 4. Seleccionar la sala empresarial aprobada.
    await sala.click();
    await page
      .getByRole('option', { name: '200089 — BRANDS SOCIEDAD DE RESPONSABILIDAD LIMITADA' })
      .click();
    await expect(sala).toHaveAttribute('aria-label', /Selected 200089/);

    // 5. Verificar el resultado empresarial visible.
    await expect(
      page.getByText(
        'Sala empresarial: BRANDS SOCIEDAD DE RESPONSABILIDAD LIMITADA · COD 200089 · Cadena Brands · DPTO 2 - Santa Cruz',
        { exact: false }
      )
    ).toBeVisible();
  });
});