import { test, expect } from '@playwright/test';

test.describe('Operacion y workflow OPE-05', () => {
  test('OPE-05 - Auditoria completa se pausa antes de cambios de precio', async ({ page }) => {
    test.setTimeout(90_000);

    await page.goto('/');

    const threadId = page.getByTestId('thread-id');
    await expect(threadId).toBeVisible({ timeout: 15_000 });
    await expect(page.getByRole('tab', { name: '1 · Operacion' })).toBeVisible();
    await expect(page.getByText('NO_EXISTE', { exact: false }).first()).toBeVisible();

    const threadAnterior = (await threadId.innerText()).trim();
    await page.getByRole('button', { name: /Nuevo thread/i }).click();
    await expect.poll(async () => (await threadId.innerText()).trim(), {
      timeout: 15_000,
      message: 'El Thread ID debe cambiar al crear OPE-05',
    }).not.toBe(threadAnterior);

    const escenario = page.getByRole('combobox', { name: /Escenario/i });
    await escenario.click();
    await page.getByRole('option', { name: 'Auditoria completa (3 tools MCP)', exact: true }).click();
    await expect(escenario).toHaveAttribute('aria-label', /Auditoria completa \(3 tools MCP\)/i);
    const pregunta = page.getByRole('textbox', { name: 'Pregunta que entra a LangGraph' });
    await expect(pregunta).toHaveValue(
      'Necesito una auditoria completa del Yogur natural 1 litro de la Sala 12'
    );

    await page.getByRole('button', { name: /PAUSAR/i }).click();
    const textoVisible = async () => page.locator('body').innerText();
    await expect.poll(textoVisible, { timeout: 60_000 }).toMatch(/Este thread esta PAUSADO/i);
    await expect.poll(textoVisible, { timeout: 30_000 }).toMatch(/AUDITORIA_COMPLETA/i);
    await expect.poll(textoVisible, { timeout: 30_000 }).toMatch(/Workflow pausado antes de consultar_cambios_precio_mcp/i);
    await expect.poll(textoVisible, { timeout: 30_000 }).toMatch(/validar_entrada[\s\S]*clasificar_intencion[\s\S]*extraer_contexto[\s\S]*consultar_detalle_mcp/i);
    await expect.poll(textoVisible, { timeout: 30_000 }).toMatch(/consultar_cambios_precio_mcp/i);
    await expect.poll(textoVisible, { timeout: 30_000 }).toMatch(/consultar_acciones_comerciales_mcp[\s\S]*(no recorrido|pendiente|NO)/i);
    await expect(page.getByText('NEXT', { exact: true })).toBeVisible();
    await expect(page.getByRole('button', { name: /REANUDAR/i })).toBeEnabled();
    await expect(page.getByRole('button', { name: /EJECUTAR/i })).toBeDisabled();
  });
});