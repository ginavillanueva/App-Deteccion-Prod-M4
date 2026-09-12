// spec: specs/PLAN_02_CONTEXTO_PRODUCTO.md
// seed: seed.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Contexto, producto, fuente y nota', () => {
  test('SRC-01 - Cambiar la fuente backend deja visible la seleccion antes de ejecutar', async ({ page }) => {
    // 1. Iniciar un caso independiente y verificar los radios de fuente.
    await page.goto('/');
    const demoValidado = page.getByRole('radio', { name: 'DEMO VALIDADO' });
    const contextoEmpresarial = page.getByRole('radio', { name: 'CONTEXTO EMPRESARIAL' });
    await expect(demoValidado).toBeChecked();

    // 2. Seleccionar CONTEXTO EMPRESARIAL.
    await contextoEmpresarial.dispatchEvent('click');
    await expect(contextoEmpresarial).toBeChecked();
    await expect(demoValidado).not.toBeChecked();

    // 3. Verificar el modo empresarial sin ejecutar el workflow.
    await expect(
      page.getByText('Modo empresarial:', { exact: false })
    ).toBeVisible();
  });
});