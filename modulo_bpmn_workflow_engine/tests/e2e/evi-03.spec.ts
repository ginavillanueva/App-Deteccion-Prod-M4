import { test, expect } from '@playwright/test';
import path from 'node:path';

const cameraFixture = path.join(__dirname, 'fixtures', 'evi-03-camera.y4m');

test.use({
  permissions: ['camera'],
  launchOptions: {
    args: [
      '--use-fake-device-for-media-stream',
      '--use-fake-ui-for-media-stream',
      `--use-file-for-fake-video-capture=${cameraFixture}`,
    ],
  },
});

test.describe('Evidencia multimodal', () => {
  test('EVI-03 - Activar camara y verificar captura disponible', async ({ page }) => {
    await page.goto('/');

    // 1. Activar la camara desde la pestaña de evidencia multimodal.
    await page.getByRole('tab', { name: '· Evidencia multimodal' }).click();
    const cameraToggle = page.getByRole('checkbox', { name: 'Activar camara' });
    await page.getByText('Activar camara', { exact: true }).click();
    await expect(cameraToggle).toBeChecked();

    // 2-3. Verificar y usar el control real de captura.
    await expect(page.getByText('Tomar foto del producto', { exact: true })).toBeVisible();
    const takePhoto = page.getByRole('button', { name: 'Take Photo' });
    await expect(takePhoto).toBeEnabled();
    await takePhoto.click();
    await expect(page.getByText('Evidencia visual capturada', { exact: true })).toBeVisible();
  });
});