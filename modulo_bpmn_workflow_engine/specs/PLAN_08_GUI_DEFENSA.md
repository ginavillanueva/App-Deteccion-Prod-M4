# Plan Playwright GUI: Guion de defensa

## Application Overview

Plan exclusivamente observacional para GUI-01 sobre la interfaz real de App Deteccion Prod en http://127.0.0.1:8501. No genera tests, no llama al generator, no modifica la aplicación ni tests existentes. El caso es independiente, comienza con page.goto('/'), usa localizadores semánticos accesibles y assertions web-first. El click de la pestaña provoca un rerender de Streamlit; los elementos deben volver a resolverse después del rerender. No usar refs dinámicas del snapshot, waitForTimeout ni sleeps.

## Test Scenarios

### 1. GUI - Guion de defensa

**Seed:** `No aplica: el plan no genera tests`

#### 1.1. GUI-01 - Abrir guion de defensa

**File:** `No se genera archivo de test`

**Steps:**
  1. Iniciar un caso independiente con page.goto('/'). Esperar la carga normal de la aplicación y localizar la pestaña por su rol y nombre accesible '5 · Guion defensa'.
    - expect: La página muestra el título accesible 'App Deteccion Prod' y la pestaña '5 · Guion defensa'.
    - expect: No se requieren datos de negocio, ejecución de workflow, thread específico ni tokens para este caso.
  2. Activar la pestaña con getByRole('tab', { name: '5 · Guion defensa' }). No conservar refs del snapshot y volver a resolver los elementos después del rerender de Streamlit.
    - expect: La pestaña queda seleccionada.
    - expect: Existe un tabpanel accesible con nombre '5 · Guion defensa'.
    - expect: El contenido del tabpanel se actualiza tras el rerender sin depender de una espera temporal fija.
  3. Dentro del tabpanel, localizar el heading exacto 'Guion express para demostrar que SI funciona' y verificar el contenido de la lista del guion.
    - expect: El heading 'Guion express para demostrar que SI funciona' está visible.
    - expect: La lista muestra la instrucción observable 'Selecciona una sala empresarial real' y la indicación de seleccionar un producto del catálogo.
    - expect: La lista muestra la instrucción observable 'DEMO VALIDADO' para resultados reproducibles.
    - expect: La lista muestra instrucciones visibles sobre 'Nuevo thread', 'AUDITORIA_COMPLETA' y 'PAUSAR'.
    - expect: La lista muestra instrucciones visibles sobre 'REANUDAR', 'SEGURIDAD' y 'EJECUTAR'.
    - expect: La lista muestra la instrucción visible para abrir 'Trazabilidad' y la instrucción visible para abrir 'Grafo'.
  4. Verificar las reglas operativas expuestas en los dos mensajes de la sección, usando texto observable y sin inferir contenido adicional.
    - expect: Es visible el mensaje 'La UI no decide el negocio. Solo captura contexto y evidencia; LangGraph gobierna el flujo, MCP consulta las tools, SQLite entrega datos y AsyncSqliteSaver conserva el estado.'.
    - expect: Es visible la regla 'Cambio de precio = consulta informativa y trazabilidad. No es aprobacion de precio.'.
    - expect: El resultado final corresponde a GUI-01: el guion express y las reglas operativas están visibles.

## Ficha de cobertura GUI-01

- **ID:** GUI-01
- **Objetivo:** Confirmar que una persona puede abrir la pestaña real `5 · Guion defensa` y observar el guion express junto con las reglas operativas expuestas por la aplicación.
- **Precondiciones:** Aplicación accesible en `http://127.0.0.1:8501`; caso independiente iniciado con `page.goto('/')`; no requiere seleccionar contexto, producto, ejecutar workflow ni usar un thread concreto.
- **Resultado observable:** La pestaña queda seleccionada, existe el tabpanel `5 · Guion defensa`, y son visibles el heading `Guion express para demostrar que SI funciona`, las instrucciones del guion y los dos mensajes de reglas operativas.
- **Localizadores:** `getByRole('tab', { name: '5 · Guion defensa' })`; `getByRole('tabpanel', { name: '5 · Guion defensa' })`; `getByRole('heading', { name: 'Guion express para demostrar que SI funciona', exact: true })`; `getByText()` o `getByRole('listitem')` filtrados por los textos observados; mensajes completos mediante `getByText()` con coincidencia estable. No usar refs dinámicas del snapshot.
- **Assertions:** Assertions web-first como `toBeVisible()`, `toHaveAttribute('aria-selected', 'true')`, `toContainText()` y `toHaveText()` cuando corresponda. Resolver nuevamente los localizadores después del rerender de Streamlit; no usar `waitForTimeout`, sleeps ni tiempos fijos.
- **Riesgos/fragilidades:** El click de una pestaña de Streamlit reconstruye el contenido y puede invalidar referencias previamente obtenidas. Los textos incluyen emojis, mayúsculas y acentos que podrían cambiar; mantener las assertions limitadas al contenido observado. El panel no expone un control adicional para abrir el guion.
- **data-testid:** No indispensable; la pestaña, el tabpanel, el heading, la lista y los mensajes tienen localizadores semánticos reales.
- **Automatizable:** Sí.
- **Cambios de aplicación requeridos:** No.
- **Tokens:** tokens no expuestos por la interfaz.
