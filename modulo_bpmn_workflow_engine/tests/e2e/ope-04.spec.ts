import { test, expect } from '@playwright/test';

test.describe('Operacion basica OPE-01 a OPE-04', () => {

  test(
    'OPE-04 - Accion comercial consulta registros sin ejecucion autonoma',
    async ({ page }) => {

      // Es un limite maximo, NO una espera fija.
      test.setTimeout(90_000);

      // 1. Cargar aplicación.
      await page.goto('/');

      // 2. Confirmar Thread ID actual.
      const threadId = page.getByTestId('thread-id');

      await expect(threadId).toBeVisible({
        timeout: 15_000,
      });

      const threadAnterior = (
        await threadId.innerText()
      ).trim();

      // 3. Crear un thread realmente nuevo.
      await page
        .getByRole('button', {
          name: /Nuevo thread/i,
        })
        .click();

      // No usamos sleep.
      // Esperamos hasta que el ID cambie realmente.
      await expect
        .poll(
          async () => {
            return (
              await threadId.innerText()
            ).trim();
          },
          {
            timeout: 15_000,
            message:
              'El Thread ID debe cambiar al crear un nuevo thread',
          }
        )
        .not.toBe(threadAnterior);

      // 4. Seleccionar Acción comercial registrada.
      const escenario = page.getByRole(
        'combobox',
        {
          name: /Escenario/i,
        }
      );

      await escenario.click();

      await page
        .getByRole('option', {
          name: 'Accion comercial registrada',
          exact: true,
        })
        .click();

      // Comprobar que Streamlit reflejó realmente la selección.
      await expect(escenario).toHaveAttribute(
        'aria-label',
        /Accion comercial registrada/i,
        {
          timeout: 15_000,
        }
      );

      // 5. Ejecutar workflow.
      await page
        .getByRole('button', {
          name: /EJECUTAR/i,
        })
        .click();

      /*
       * IMPORTANTE:
       * No buscamos page.getByText('FINALIZADO').first()
       * porque Streamlit puede conservar nodos ocultos durante rerenders.
       *
       * innerText() devuelve el texto renderizado/observable y se
       * vuelve a consultar en cada poll.
       */
      const textoVisible = async () => {
        return await page.locator('body').innerText();
      };

      // 6. Esperar estado final REAL.
      await expect
        .poll(
          textoVisible,
          {
            timeout: 60_000,
            message:
              'El workflow debe llegar al estado FINALIZADO',
          }
        )
        .toMatch(
          /Este thread ya esta FINALIZADO/i
        );

      // 7. Verificar evidencia estructurada de consulta comercial.
      // Regla de negocio:
      // consulta registros, NO ejecuta acciones autónomamente.
      await expect
        .poll(
          textoVisible,
          {
            timeout: 30_000,
            message:
              'Debe existir evidencia estructurada de consulta comercial',
          }
        )
        .toMatch(
          /consultar_acciones_comerciales_mcp|CONSULTA_DE_REGISTRO_SIN_EJECUCION_AUTONOMA/i
        );
    }
  );
});
