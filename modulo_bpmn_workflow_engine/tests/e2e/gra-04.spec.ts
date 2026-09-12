import { test, expect } from '@playwright/test';

test.describe('GRA-04 - Reiniciar visualizacion', () => {
  test('restaura el estado inicial y limpia la bitacora', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('tab', { name: '4 · Grafo / arquitectura' }).click();
    const panel = page.getByRole('tabpanel', { name: '4 · Grafo / arquitectura' });
    await expect(panel.getByText('Grafo generado por el codigo real', { exact: true })).toBeVisible();

    const workflow = page.locator('iframe[title="st.iframe"]').contentFrame();
    await workflow.getByRole('button', { name: '⚠ Simular incidente' }).click();
    await expect.poll(
      async () => workflow.getByText('Workflow completado', { exact: true }).count(),
      { timeout: 30_000 },
    ).toBeGreaterThan(0);

    await workflow.getByRole('button', { name: '↺ Reiniciar' }).click();
    await expect.poll(
      async () => workflow.getByText('Listo para iniciar', { exact: true }).count(),
      { timeout: 7_500 },
    ).toBeGreaterThan(0);
    await expect(workflow.getByText('Presiona “Ejecutar flujo” para animar el proceso normal o “Simular incidente” para ver un retorno controlado.', { exact: true })).toBeVisible();
    await expect(workflow.getByRole('heading', { name: 'Bitácora de ejecución' })).toBeVisible();
    await expect(workflow.getByText('INCIDENTE', { exact: true })).toHaveCount(0);
    await expect(workflow.getByText('REWORK', { exact: true })).toHaveCount(0);
    await expect(workflow.getByRole('button', { name: '▶ Ejecutar flujo' })).toBeVisible();
  });
});
