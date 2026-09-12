// spec: specs/PLAN_01_NAVEGACION_SESION.md
// seed: tests/e2e/seed.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Navegacion y sesion', () => {
  test('THR-01 - Nuevo thread cambia el Thread ID activo', async ({ page }) => {
    // 1. Iniciar en estado fresco y navegar a page.goto('/').
    await page.goto('/');

    const threadId = page.getByTestId('thread-id');

    // 2. Localizar el valor visible de Thread ID, guardarlo y verificar que no esta vacio.
    await expect(threadId).toBeVisible();
    await expect(threadId).not.toHaveText('');
    const threadIdAnterior = (await threadId.textContent())?.trim() ?? '';
    expect(threadIdAnterior).not.toBe('');

    // 3. Pulsar el boton 'Nuevo thread' por nombre accesible.
    await page.getByRole('button', { name: /Nuevo thread/i }).click();

    // 4. Esperar mediante assertion web-first a que el Thread ID cambie.
    await expect
      .poll(async () => (await threadId.textContent())?.trim() ?? '')
      .not.toBe(threadIdAnterior);

    // 5. Verificar que el nuevo valor no esta vacio y es distinto del anterior.
    const threadIdNuevo = (await threadId.textContent())?.trim() ?? '';
    expect(threadIdNuevo).not.toBe('');
    expect(threadIdNuevo).not.toBe(threadIdAnterior);
  });
});
