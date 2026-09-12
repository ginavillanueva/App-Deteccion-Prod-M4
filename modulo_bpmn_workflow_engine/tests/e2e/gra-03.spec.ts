import { test, expect } from '@playwright/test';

test.describe('GRA-03 - Simular incidente', () => {
  test('muestra incidente, rework y cierre controlado', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('tab', { name: '4 · Grafo / arquitectura' }).click();
    const panel = page.getByRole('tabpanel', { name: '4 · Grafo / arquitectura' });
    await expect(panel.getByText('Grafo generado por el codigo real', { exact: true })).toBeVisible();

    const workflow = page.locator('iframe[title="st.iframe"]').contentFrame();
    await expect(workflow.getByText('Listo para iniciar', { exact: true })).toBeVisible();
    await workflow.getByRole('button', { name: '⚠ Simular incidente' }).click();

    await expect.poll(
      async () => workflow.getByText('INCIDENTE', { exact: true }).count(),
      { timeout: 30_000 },
    ).toBeGreaterThan(0);
    await expect(workflow.getByText('Se detecta inconsistencia en ejecución o precio aplicado', { exact: true })).toBeVisible();
    await expect.poll(
      async () => workflow.getByText('REWORK', { exact: true }).count(),
      { timeout: 7_500 },
    ).toBeGreaterThan(0);
    await expect(workflow.getByText('Incidente abierto: el caso vuelve a ValidateEvidence', { exact: true })).toBeVisible();
    await expect.poll(
      async () => workflow.getByText('Workflow completado', { exact: true }).count(),
      { timeout: 30_000 },
    ).toBeGreaterThan(0);
    await expect(workflow.getByText('Supervisor revalida evidencia corregida', { exact: false })).toBeVisible();
    await expect(workflow.getByText('Mercaderista corrige y ejecuta nuevamente', { exact: false })).toBeVisible();
    await expect(workflow.getByText('Supervisor aprueba la corrección', { exact: false })).toBeVisible();
    await expect(workflow.getByText('Caso cerrado y dashboard actualizado', { exact: false })).toBeVisible();
    await expect(workflow.getByText('Workflow finalizado con trazabilidad completa', { exact: false })).toBeVisible();
  });
});
