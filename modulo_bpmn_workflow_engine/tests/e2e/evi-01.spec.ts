import { test, expect } from '@playwright/test';
import path from 'node:path';

test.describe('Evidencia multimodal', () => {
  test('EVI-01 - Subir audio y confirmar transcripcion', async ({ page }) => {
    await page.goto('/');

    // 1. Abrir la pestaña de evidencia multimodal.
    await page.getByRole('tab', { name: '· Evidencia multimodal' }).click();
    await expect(page.getByRole('tabpanel', { name: '2 · Evidencia multimodal' })).toBeVisible();
    await expect(page.getByRole('heading', { name: '🎤 Audio' })).toBeVisible();
    await expect(page.getByText(/WAV\/MP3\/M4A\/OGG/)).toBeVisible();

    // 2-3. Subir el fixture WAV y comprobar que aparece en el uploader.
    const audioUploader = page.getByRole('button', { name: 'Subir evidencia de audio' });
    const audioChooser = page.waitForEvent('filechooser');
    await audioUploader.click();
    await (await audioChooser).setFiles(path.join(__dirname, 'fixtures', 'evi-01-silence.wav'));
    await expect(page.getByText('evi-01-silence.wav', { exact: true })).toBeVisible();

    // 4. Confirmar la transcripcion manual observable.
    const transcription = page.getByRole('textbox', { name: 'Transcripcion confirmada' });
    await transcription.fill('Audio de evidencia de prueba.');
    await expect(transcription).toHaveValue('Audio de evidencia de prueba.');
  });
});