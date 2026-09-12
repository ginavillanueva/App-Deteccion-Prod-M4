import { test, expect } from '@playwright/test';

test.describe('GRA-02 - Ejecutar flujo BPMN animado', () => {
  test('muestra avance y finalizacion del flujo', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('tab', { name: '4 · Grafo / arquitectura' }).click();
    const panel = page.getByRole('tabpanel', { name: '4 · Grafo / arquitectura' });
    await expect(panel.getByText('Grafo generado por el codigo real', { exact: true })).toBeVisible();

    const workflow = page.locator('iframe[title="st.iframe"]').contentFrame();
    await expect(workflow.getByRole('combobox')).toBeVisible();
    await expect(workflow.getByText('Listo para iniciar', { exact: true })).toBeVisible();
    await workflow.getByRole('button', { name: '▶ Ejecutar flujo' }).click();

    await expect.poll(
      async () => workflow.getByText('Listo para iniciar', { exact: true }).count(),
      { timeout: 7_500 },
    ).toBe(0);
    await expect.poll(
      async () => workflow.getByText('Workflow completado', { exact: true }).count(),
      { timeout: 30_000 },
    ).toBeGreaterThan(0);
    await expect(workflow.getByText('El caso terminó con trazabilidad completa y dashboard actualizado.', { exact: true })).toBeVisible();
    await expect(workflow.getByText('Workflow finalizado con trazabilidad completa', { exact: false })).toBeVisible();
    await expect(workflow.getByText('Caso cerrado y dashboard actualizado', { exact: false })).toBeVisible();
  });
});
