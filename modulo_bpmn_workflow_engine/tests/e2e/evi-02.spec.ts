import { test, expect } from '@playwright/test';
import path from 'node:path';

test.describe('Evidencia multimodal', () => {
  test('EVI-02 - Subir imagen y confirmar descripcion', async ({ page }) => {
    await page.goto('/');

    // 1. Abrir la pestaña de evidencia y localizar el flujo de imagen.
    await page.getByRole('tab', { name: '· Evidencia multimodal' }).click();
    await expect(page.getByRole('tabpanel', { name: '2 · Evidencia multimodal' })).toBeVisible();
    await expect(page.getByRole('heading', { name: '📷 Foto' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'O subir imagen' })).toBeVisible();

    // 2-3. Subir el fixture PNG y comprobar que aparece en el uploader.
    const imageUploader = page.getByRole('button', { name: 'O subir imagen' });
    const imageChooser = page.waitForEvent('filechooser');
    await imageUploader.click();
    await (await imageChooser).setFiles(path.join(__dirname, 'fixtures', 'evi-02-product.png'));
    await expect(page.getByText('evi-02-product.png', { exact: true })).toBeVisible();

    // 4. Confirmar la descripcion manual observable.
    const description = page.getByRole('textbox', { name: 'Lectura/descripcion confirmada' });
    await description.fill('Producto de evidencia, presentacion 1 unidad y fecha visible.');
    await expect(description).toHaveValue('Producto de evidencia, presentacion 1 unidad y fecha visible.');
  });
});