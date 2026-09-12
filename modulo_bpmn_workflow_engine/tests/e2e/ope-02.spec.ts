import { test, expect } from '@playwright/test';

test.describe('Operacion basica OPE-01 a OPE-04', () => {

  test(
    'OPE-02 - Vencimiento finaliza con evidencia de detalle',
    async ({ page }) => {

      test.setTimeout(90_000);

      await page.goto('/');

      const threadId = page.getByTestId('thread-id');

      await expect(threadId).toBeVisible({
        timeout: 15_000,
      });

      const threadAnterior = (
        await threadId.innerText()
      ).trim();

      await page
        .getByRole('button', {
          name: /Nuevo thread/i,
        })
        .click();

      await expect
        .poll(
          async () => (
            await threadId.innerText()
          ).trim(),
          {
            timeout: 15_000,
            message:
              'El Thread ID debe cambiar antes de ejecutar OPE-02',
          }
        )
        .not.toBe(threadAnterior);

      const escenario = page.getByRole(
        'combobox',
        {
          name: /Escenario/i,
        }
      );

      await escenario.click();

      await page
        .getByRole('option', {
          name: 'Vencimiento / riesgo de merma',
          exact: true,
        })
        .click();

      await page
        .getByRole('button', {
          name: /EJECUTAR/i,
        })
        .click();

      const textoVisible = async () =>
        await page.locator('body').innerText();

      // Estado final real del workflow.
      await expect
        .poll(
          textoVisible,
          {
            timeout: 60_000,
            message:
              'OPE-02 debe alcanzar el estado FINALIZADO',
          }
        )
        .toMatch(
          /Este thread ya esta FINALIZADO/i
        );

      // Evidencia real del flujo de vencimiento.
      await expect
        .poll(
          textoVisible,
          {
            timeout: 30_000,
            message:
              'OPE-02 debe mostrar evidencia de consulta de detalle',
          }
        )
        .toMatch(
          /consultar_detalle_(mcp|producto)/i
        );
    }
  );
});
