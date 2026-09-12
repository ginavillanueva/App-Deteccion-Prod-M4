import { test, expect } from '@playwright/test';

test.describe('GRA-01 - Abrir grafo y arquitectura', () => {
  test('muestra el grafo generado y la arquitectura defendible', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: /App Deteccion Prod/i })).toBeVisible();
    await page.getByRole('tab', { name: '4 · Grafo / arquitectura' }).click();

    const panel = page.getByRole('tabpanel', { name: '4 · Grafo / arquitectura' });
    await expect(panel).toBeVisible();
    await expect(panel.getByRole('heading', { name: 'Grafo generado por el codigo real' })).toBeVisible();
    const graph = panel.locator('code').filter({ hasText: '__start__' });
    for (const node of [
      '__start__', 'validar_entrada', 'clasificar_intencion', 'extraer_contexto',
      'consultar_detalle_mcp', 'consultar_cambios_precio_mcp',
      'consultar_acciones_comerciales_mcp', '__end__',
    ]) {
      await expect(graph).toContainText(node);
    }
    await expect(panel.getByRole('heading', { name: 'Nodos recorridos por este thread' })).toBeVisible();
    await expect(panel.getByText('Sin ejecucion en este thread.', { exact: true })).toBeVisible();
    await expect(panel.getByRole('heading', { name: 'Arquitectura defendible' })).toBeVisible();
    const architecture = panel.locator('code').filter({ hasText: 'Guardrail' });
    for (const component of [
      'Guardrail', 'Clasificacion', 'LangGraph', 'MCP', 'SQLite',
      'checkpoints / thread_id', 'traza', 'evidencia',
    ]) {
      await expect(architecture).toContainText(component);
    }
  });
});
