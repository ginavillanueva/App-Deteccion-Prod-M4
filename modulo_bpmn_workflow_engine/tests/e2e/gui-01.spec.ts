import { test, expect } from '@playwright/test';

test.describe('GUI - Guion de defensa', () => {
  test('GUI-01 - Abrir guion de defensa', async ({ page }) => {
    // 1. Iniciar un caso independiente con page.goto('/'). Verificar el título y la pestaña real.
    await page.goto('/');
    await expect(page.getByRole('heading', { name: /App Deteccion Prod/i })).toBeVisible();
    await expect(page.getByRole('tab', { name: /5 · Guion defensa/ })).toBeVisible();

    // 2. Activar la pestaña y resolver nuevamente el contenido tras el rerender de Streamlit.
    await page.getByRole('tab', { name: /5 · Guion defensa/ }).click();
    const defenseTab = page.getByRole('tab', { name: /5 · Guion defensa/ });
    const defensePanel = page.getByRole('tabpanel', { name: /5 · Guion defensa/ });
    await expect(defenseTab).toHaveAttribute('aria-selected', 'true');
    await expect(defensePanel).toBeVisible();

    // 3. Verificar el heading y las instrucciones observables del guion express.
    await expect(
      defensePanel.getByRole('heading', {
        name: 'Guion express para demostrar que SI funciona',
        exact: true,
      })
    ).toBeVisible();
    await expect(defensePanel.locator('li')).toHaveCount(10);
    await expect(defensePanel.locator('li')).toContainText([
      'Selecciona una sala empresarial real y un producto del catalogo.',
      'Deja DEMO VALIDADO para garantizar resultados reproducibles.',
      'Con un thread NUEVO ejecuta VENCIMIENTO y muestra consultar_detalle_producto + fuente productos_vencimiento.',
      'Pulsa Nuevo thread, selecciona AUDITORIA_COMPLETA y pulsa PAUSAR.',
      "Muestra PAUSADO y NEXT=['consultar_cambios_precio_mcp'].",
      'Pulsa REANUDAR y muestra las 3 tools MCP y FINALIZADO.',
      'Pulsa Nuevo thread, selecciona SEGURIDAD y pulsa EJECUTAR.',
      'Muestra PROMPT_INJECTION, TOOLS=[] y solo validar_entrada.',
      'Abre Trazabilidad: checkpoint, historial, metadata de evidencia y thread_id.',
      'Abre Grafo: Mermaid generado desde el grafo_mcp real.',
    ]);

    // 4. Verificar las reglas operativas visibles expuestas por la sección.
    await expect(
      defensePanel.getByText(
        'Mensaje clave: la UI no decide el negocio. Solo captura contexto y evidencia; LangGraph gobierna el flujo, MCP consulta las tools, SQLite entrega datos y AsyncSqliteSaver conserva el estado.',
        { exact: true }
      )
    ).toBeVisible();
    await expect(
      defensePanel.getByText(
        'Cambio de precio = consulta informativa y trazabilidad. No es aprobacion de precio.',
        { exact: true }
      )
    ).toBeVisible();
  });
});
