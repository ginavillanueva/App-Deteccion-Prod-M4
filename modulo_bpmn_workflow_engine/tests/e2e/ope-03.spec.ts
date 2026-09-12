import { test, expect } from '@playwright/test';

test.describe('Operacion basica OPE-01 a OPE-04', () => {

  test(
    'OPE-03 - Cambio de precio es consulta informativa trazable',
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
              'El Thread ID debe cambiar antes de ejecutar OPE-03',
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
          name: 'Cambio de precio (informativo, sin aprobacion)',
          exact: true,
        })
        .click();

      // Streamlit hace rerender despu?s de cambiar el escenario.
      // No ejecutar hasta que la selecci?n real quede reflejada.
      await expect(escenario).toHaveAttribute(
        'aria-label',
        /Cambio de precio \(informativo, sin aprobacion\)/i,
        {
          timeout: 20_000,
        }
      );

      const ejecutar = page.getByRole('button', {
        name: /EJECUTAR/i,
      });

      // Esperar a que el rerun de Streamlit deje el control ejecutable.
      await expect(ejecutar).toBeEnabled({
        timeout: 20_000,
      });

      await ejecutar.click();

      const textoVisible = async () =>
        await page.locator('body').innerText();

      // Estado final real.
      await expect
        .poll(
          textoVisible,
          {
            timeout: 60_000,
            message:
              'OPE-03 debe alcanzar el estado FINALIZADO',
          }
        )
        .toMatch(
          /Este thread ya esta FINALIZADO/i
        );

      // Evidencia de consulta de cambios de precio.
      await expect
        .poll(
          textoVisible,
          {
            timeout: 30_000,
            message:
              'OPE-03 debe mostrar evidencia de consulta de cambio de precio',
          }
        )
        .toMatch(
          /consultar_cambios_precio(_mcp)?|cambios_precio/i
        );
    }
  );
});
