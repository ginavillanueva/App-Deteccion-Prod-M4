import { test, expect } from '@playwright/test';

test.describe('Trazabilidad', () => {
  test('TRZ-02 - abrir Trazabilidad despues de ejecutar', async ({ page }) => {
    await page.goto('/');

    await expect(page.getByRole('heading', { name: /App Deteccion Prod/i })).toBeVisible();
    await expect(page.getByRole('heading', { name: '🎛 Control' })).toBeVisible();
    await expect(page.getByTestId('thread-id')).toBeVisible();
    await expect(page.getByRole('alert').filter({ hasText: 'NO_EXISTE' }).first()).toBeVisible();

    await expect(page.getByRole('combobox', { name: /Departamento/ })).toHaveAttribute('aria-label', /Selected 1 - La Paz/);
    await expect(page.getByRole('combobox', { name: /Cadena/ })).toHaveAttribute('aria-label', /Selected Andys/);
    await expect(page.getByRole('combobox', { name: /Sala/ })).toHaveAttribute('aria-label', /Selected 101797 — ANDYS SAN MIGUEL/);
    await expect(page.getByRole('combobox', { name: /Producto empresarial/ })).toHaveAttribute('aria-label', /Selected 0000051432 — Prudential Comfort Total M 4x20/);
    await expect(page.getByRole('combobox', { name: /Escenario/ })).toHaveAttribute('aria-label', /Selected Vencimiento \/ riesgo de merma/);
    await expect(page.getByRole('radio', { name: 'DEMO VALIDADO' })).toBeChecked();

    const threadId = await page.getByTestId('thread-id').textContent();
    await expect(page.getByText('▶ EJECUTAR', { exact: true })).toBeVisible();
    await page.getByText('▶ EJECUTAR', { exact: true }).click();
    await expect.poll(async () => (await page.getByRole('alert').allTextContents()).join(' ')).toMatch(/PAUSADO|FINALIZADO/);

    const pausedStatus = page.getByRole('alert').filter({ hasText: 'PAUSADO' }).first();
    if (await pausedStatus.isVisible()) {
      await page.getByRole('button').filter({ hasText: 'REANUDAR' }).click();
    }

    await expect.poll(async () => (await page.getByRole('alert').allTextContents()).join(' ')).toMatch(/FINALIZADO/);
    await expect(page.getByTestId('thread-id')).toHaveText(threadId!);

    await page.getByRole('tab', { name: '3 · Trazabilidad' }).click();
    const tracePanel = page.getByRole('tabpanel', { name: '3 · Trazabilidad' });
    await expect(tracePanel).toBeVisible();
    await expect(tracePanel.getByRole('heading', { name: 'Trazabilidad tecnica completa' })).toBeVisible();
    await expect(tracePanel).toContainText(`Thread: ${threadId}`);
    await expect(tracePanel).toContainText('FINALIZADO');
    await expect(tracePanel.getByRole('heading', { name: 'Checkpoint actual' })).toBeVisible();
    await expect(tracePanel).toContainText('"values"');
    await expect(tracePanel).toContainText('"next"');
    await expect(tracePanel).toContainText('"metadata"');
    await expect(tracePanel.getByRole('heading', { name: 'Estado LangGraph' })).toBeVisible();
    await expect(tracePanel).toContainText('"pregunta"');
    await expect(tracePanel).toContainText('"thread_id"');
    await expect(tracePanel).toContainText('"intencion"');
    await expect(tracePanel).toContainText('"producto"');
    await expect(tracePanel).toContainText('"tienda"');
    await expect(tracePanel).toContainText('"fuentes"');
    await expect(tracePanel).toContainText('"tools_usadas"');
    await expect(tracePanel).toContainText('"observaciones"');
    await expect(tracePanel).toContainText('"bloqueado"');
    await expect(tracePanel).toContainText('"problema"');
    await expect(tracePanel).toContainText('"traza"');
    await expect(tracePanel).toContainText('productos_vencimiento');
    await expect(tracePanel).toContainText('consultar_detalle_producto');
    await expect(tracePanel.getByRole('heading', { name: 'Historial de checkpoints' })).toBeVisible();
    await expect(tracePanel.getByRole('button', { name: /Checkpoint \d+ · NEXT=/ }).first()).toBeVisible();
    await expect(tracePanel.getByRole('button', { name: /NEXT=/ }).first()).toBeVisible();
    await expect(tracePanel.getByRole('heading', { name: 'Evidencia y contexto empresarial' })).toBeVisible();
    await expect(tracePanel.getByText('Aun no hay metadata guardada para este thread.', { exact: true })).toBeVisible();
  });
});