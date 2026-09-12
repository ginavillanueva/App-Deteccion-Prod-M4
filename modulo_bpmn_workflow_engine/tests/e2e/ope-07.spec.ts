import { test, expect } from '@playwright/test';

test.describe('Operacion y workflow OPE-07', () => {
  test('OPE-07 - Recuperar conserva el estado persistido sin reejecutar MCP', async ({ page }) => {
    test.setTimeout(120_000);

    await page.goto('/');

    const threadId = page.getByTestId('thread-id');
    await expect(threadId).toBeVisible({ timeout: 15_000 });
    const threadAnterior = (await threadId.innerText()).trim();
    await page.getByRole('button', { name: /Nuevo thread/i }).click();
    await expect.poll(async () => (await threadId.innerText()).trim(), {
      timeout: 15_000,
      message: 'El Thread ID debe cambiar al crear OPE-07',
    }).not.toBe(threadAnterior);

    const escenario = page.getByRole('combobox', { name: /Escenario/i });
    await escenario.click();
    await page.getByRole('option', { name: 'Auditoria completa (3 tools MCP)', exact: true }).click();
    await expect(escenario).toHaveAttribute('aria-label', /Auditoria completa \(3 tools MCP\)/i);
    await expect(page.getByRole('textbox', { name: 'Pregunta que entra a LangGraph' })).toHaveValue(
      'Necesito una auditoria completa del Yogur natural 1 litro de la Sala 12'
    );

    await page.getByRole('button', { name: /PAUSAR/i }).click();
    const textoVisible = async () => page.locator('body').innerText();
    await expect.poll(textoVisible, { timeout: 60_000 }).toMatch(/Este thread esta PAUSADO/i);
    await page.getByRole('button', { name: /REANUDAR/i }).click();
    await expect.poll(textoVisible, { timeout: 60_000 }).toMatch(/Workflow reanudado desde SQLite\/checkpoint/i);
    await expect.poll(textoVisible, { timeout: 60_000 }).toMatch(/Este thread ya esta FINALIZADO/i);
    const threadFinalizado = (await threadId.innerText()).trim();

    await page.getByRole('button', { name: /RECUPERAR/i }).click();
    await expect.poll(textoVisible, { timeout: 30_000 }).toMatch(/Estado recuperado desde checkpoints sin reejecutar MCP/i);
    await expect.poll(textoVisible, { timeout: 30_000 }).toMatch(/Este thread ya esta FINALIZADO/i);
    await expect.poll(textoVisible, { timeout: 30_000 }).toMatch(/AUDITORIA_COMPLETA/i);
    await expect(page.getByText('Flujo real de la ejecucion', { exact: true })).toBeVisible();
    await expect(page.getByText('Resultados / observaciones MCP', { exact: true })).toBeVisible();
    await expect(page.getByText('NEXT', { exact: true })).toBeVisible();
    await expect.poll(async () => (await threadId.innerText()).trim(), {
      timeout: 15_000,
      message: 'RECUPERAR debe conservar el Thread ID de OPE-07',
    }).toBe(threadFinalizado);
  });
});