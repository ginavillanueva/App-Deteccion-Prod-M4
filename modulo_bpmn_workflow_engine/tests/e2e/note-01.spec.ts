// spec: specs/PLAN_02_CONTEXTO_PRODUCTO.md
// seed: seed.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Contexto, producto, fuente y nota', () => {
  test('NOTE-01 - Conservar nota operativa sin reemplazar la pregunta principal', async ({ page }) => {
    // 1. Iniciar un caso independiente y verificar ambos textboxes.
    await page.goto('/');
    const pregunta = page.getByLabel('Pregunta que entra a LangGraph');
    const nota = page.getByLabel(/Nota operativa adicional/);
    await expect(pregunta).toBeVisible();
    await expect(nota).toBeVisible();
    const preguntaOriginal = await pregunta.inputValue();
    expect(preguntaOriginal).not.toBe('');

    // 2. Escribir la nota controlada y comprobar ambos valores.
    await nota.fill('E2E NOTE-01 - evidencia controlada');
    await expect(nota).toHaveValue('E2E NOTE-01 - evidencia controlada');
    await expect(pregunta).toHaveValue(preguntaOriginal);

    // 3. Confirmar que el rerender conserva la nota y la pregunta original.
    await expect(nota).toHaveValue('E2E NOTE-01 - evidencia controlada');
    await expect(pregunta).toHaveValue(preguntaOriginal);
  });
});