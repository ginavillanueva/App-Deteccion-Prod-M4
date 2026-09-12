import { test, expect } from '@playwright/test';

test.describe('Trazabilidad', () => {
  test('TRZ-01 - abrir Trazabilidad en thread nuevo', async ({ page }) => {
    await page.goto('/');

    await expect(page.getByRole('heading', { name: /App Deteccion Prod/i })).toBeVisible();
    await expect(page.getByRole('heading', { name: '🎛 Control' })).toBeVisible();
    await expect(page.getByTestId('thread-id')).toBeVisible();
    await expect(page.getByRole('alert').filter({ hasText: 'NO_EXISTE' }).first()).toBeVisible();

    const initialThreadId = await page.getByTestId('thread-id').textContent();
    await page.getByRole('button', { name: /Nuevo thread/i }).click();
    await expect.poll(async () => page.getByTestId('thread-id').textContent()).not.toBe(initialThreadId);
    await expect(page.getByTestId('thread-id')).toBeVisible();
    await expect(page.getByRole('alert').filter({ hasText: 'NO_EXISTE' }).first()).toBeVisible();

    await page.getByRole('tab', { name: '3 · Trazabilidad' }).click();
    const tracePanel = page.getByRole('tabpanel', { name: '3 · Trazabilidad' });
    await expect(tracePanel).toBeVisible();
    await expect(tracePanel.getByRole('heading', { name: 'Trazabilidad tecnica completa' })).toBeVisible();

    const threadId = await page.getByTestId('thread-id').textContent();
    await expect(tracePanel).toContainText(`Thread: ${threadId}`);
    await expect(tracePanel).toContainText('Estado:');
    await expect(tracePanel).toContainText('NO_EXISTE');
    await expect(tracePanel.getByText('Checkpoint actual')).toBeVisible();
    await expect(tracePanel.getByText('Estado LangGraph')).toBeVisible();
    await expect(tracePanel.getByText('{}').first()).toBeVisible();
    await expect(tracePanel.getByRole('heading', { name: 'Historial de checkpoints' })).toBeVisible();
    await expect(tracePanel.getByText('No hay historial cargado.', { exact: true })).toBeVisible();
    await expect(tracePanel.getByRole('heading', { name: 'Evidencia y contexto empresarial' })).toBeVisible();
    await expect(tracePanel.getByText('Aun no hay metadata guardada para este thread.', { exact: true })).toBeVisible();
  });
});