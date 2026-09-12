# Plan Playwright GRA: Grafo / arquitectura

## Application Overview

Plan exclusivamente observacional para GRA-01 a GRA-04 sobre la interfaz real de App Deteccion Prod en http://127.0.0.1:8501. No genera archivos de test ni modifica aplicación o tests. Cada caso es independiente, comienza con page.goto('/'), reubica elementos tras rerenders de Streamlit y usa localizadores accesibles estables; para la animación se recomienda expect.poll sobre texto de estado o bitácora, sin waitForTimeout ni sleeps.

## Test Scenarios

### 1. GRA - Grafo / arquitectura

**Seed:** `No aplica: el plan no genera tests`

#### 1.1. GRA-01 - Abrir grafo y arquitectura

**File:** `No se genera archivo de test`

**Steps:**
  1. Comenzar un caso independiente con page.goto('/'). Esperar la carga de la aplicación y localizar la pestaña por rol y nombre accesible '4 · Grafo / arquitectura'.
    - expect: La página muestra el título de la aplicación y la pestaña '4 · Grafo / arquitectura'.
  2. Activar la pestaña '4 · Grafo / arquitectura' usando getByRole('tab', { name: '4 · Grafo / arquitectura' }). Volver a localizar los elementos después del rerender de Streamlit.
    - expect: La pestaña queda seleccionada y existe el tabpanel '4 · Grafo / arquitectura'.
  3. Inspeccionar la sección visible sin usar refs del snapshot como localizadores finales.
    - expect: Es visible el heading 'Grafo generado por el codigo real'.
    - expect: Es visible un bloque de código con el grafo que contiene '__start__', 'validar_entrada', 'clasificar_intencion', 'extraer_contexto', 'consultar_detalle_mcp', 'consultar_cambios_precio_mcp', 'consultar_acciones_comerciales_mcp' y '__end__'.
    - expect: Es visible el heading 'Nodos recorridos por este thread'.
    - expect: En un thread nuevo se observa 'Sin ejecucion en este thread.'.
    - expect: Es visible el heading 'Arquitectura defendible' y su bloque de arquitectura con 'Guardrail', 'Clasificacion', 'LangGraph', 'MCP', 'SQLite', 'checkpoints / thread_id', 'traza' y 'evidencia'.

#### 1.2. GRA-02 - Ejecutar flujo BPMN animado

**File:** `No se genera archivo de test`

**Steps:**
  1. Comenzar un caso independiente con page.goto('/'). Activar la pestaña '4 · Grafo / arquitectura'. Tras el rerender, localizar el iframe del workflow BPMN y su contentFrame.
    - expect: El panel contiene el iframe del workflow BPMN y dentro de él existe el control combobox con las opciones 'Velocidad normal', 'Rápida' y 'Lenta para explicar'.
  2. Dentro del contentFrame, comprobar el estado inicial y pulsar el botón accesible '▶ Ejecutar flujo'.
    - expect: Antes del clic el estado visible es 'Listo para iniciar'.
    - expect: El botón '▶ Ejecutar flujo' existe y acepta el clic.
  3. Después del clic, volver a obtener el contentFrame y esperar el cambio dinámico con expect.poll, inspeccionando el texto del panel de estado o la bitácora, sin sleeps ni waitForTimeout.
    - expect: El estado deja de ser 'Listo para iniciar' y aparecen entradas de bitácora con etiquetas observables como 'start', 'detect' y posteriores estados de ejecución.
    - expect: La animación muestra avance visual en el workflow y la bitácora se actualiza de forma asíncrona.
  4. Esperar mediante expect.poll hasta que el estado del panel sea 'Workflow completado'.
    - expect: El estado visible es exactamente 'Workflow completado'.
    - expect: El texto asociado indica 'El caso terminó con trazabilidad completa y dashboard actualizado.'.
    - expect: La bitácora contiene, como mínimo, 'Workflow finalizado con trazabilidad completa' y 'Caso cerrado y dashboard actualizado'; en la ejecución observada también recorrió 'detect', 'validate', 'risk', 'price', 'decide', 'approve', 'execute' y 'review'.

#### 1.3. GRA-03 - Simular incidente

**File:** `No se genera archivo de test`

**Steps:**
  1. Comenzar un caso independiente con page.goto('/'). Activar la pestaña '4 · Grafo / arquitectura'. Tras el rerender, localizar el iframe BPMN y acceder a su contentFrame.
    - expect: El iframe contiene el botón accesible '⚠ Simular incidente'.
  2. Comprobar que el estado inicial del iframe es 'Listo para iniciar' y pulsar '⚠ Simular incidente'.
    - expect: El estado inicial es 'Listo para iniciar'.
    - expect: La acción se acepta sin requerir datos adicionales ni controles fuera del iframe.
  3. Volver a obtener el contentFrame después del clic y usar expect.poll para observar la bitácora dinámica.
    - expect: Aparecen entradas OK para 'start', 'detect', 'validate', 'risk', 'price' y 'approve'/'decide' según avance observado.
    - expect: La bitácora muestra una entrada con etiqueta 'INCIDENTE' y texto 'Se detecta inconsistencia en ejecución o precio aplicado'.
    - expect: La bitácora muestra una entrada con etiqueta 'REWORK' y texto 'Incidente abierto: el caso vuelve a ValidateEvidence'.
  4. Esperar por estado dinámico hasta la conclusión de la simulación.
    - expect: Se observa 'Supervisor revalida evidencia corregida', seguido de 'Mercaderista corrige y ejecuta nuevamente', 'Supervisor aprueba la corrección', 'Caso cerrado y dashboard actualizado' y 'Workflow finalizado con trazabilidad completa'.
    - expect: El estado final es 'Workflow completado'.
    - expect: La bitácora conserva visiblemente el incidente y el retorno controlado a ValidateEvidence, además del cierre final.

#### 1.4. GRA-04 - Reiniciar visualización

**File:** `No se genera archivo de test`

**Steps:**
  1. Comenzar un caso independiente con page.goto('/'). Activar '4 · Grafo / arquitectura', localizar el iframe BPMN y pulsar '⚠ Simular incidente' para producir un estado no inicial; esperar con expect.poll hasta que la bitácora muestre 'Workflow completado'.
    - expect: El caso independiente llega a un estado ejecutado con bitácora visible, lo que permite comprobar el efecto del reinicio.
  2. Volver a obtener el contentFrame y pulsar el botón accesible '↺ Reiniciar'.
    - expect: El control '↺ Reiniciar' existe y el clic se procesa.
  3. Tras el rerender del iframe, volver a localizar el panel de estado y la bitácora.
    - expect: El estado vuelve exactamente a 'Listo para iniciar'.
    - expect: El texto de ayuda vuelve a 'Presiona “Ejecutar flujo” para animar el proceso normal o “Simular incidente” para ver un retorno controlado.'.
    - expect: La bitácora vuelve a mostrar únicamente el encabezado 'Bitácora de ejecución' y 'Trazabilidad visual', sin entradas previas de ejecución, incidente o rework.
    - expect: La visualización de las cajas BPMN queda en su estado inicial y el botón '▶ Ejecutar flujo' vuelve a estar disponible.

  ## Fichas de cobertura

  ### GRA-01

  - **Objetivo:** Confirmar que la pestaña abre el grafo generado desde código real y la sección de arquitectura.
  - **Precondiciones:** Aplicación accesible; cada ejecución comienza con `page.goto('/')`; thread nuevo para observar `Sin ejecucion en este thread.`.
  - **Resultado observable:** Tabpanel activo, bloque de grafo textual, nombres de nodos, sección de nodos recorridos y `Arquitectura defendible` visibles.
  - **Localizadores:** `getByRole('tab', { name: '4 · Grafo / arquitectura' })`; `getByRole('tabpanel', { name: '4 · Grafo / arquitectura' })`; headings por nombre; `getByText` o `locator('code')` filtrado por contenido estable. No usar refs de snapshots.
  - **Assertions:** `expect(...).toBeVisible()` para headings y textos; `toContainText()` para los nombres del grafo; re-resolver locators después del rerender de Streamlit.
  - **Datos necesarios:** Ninguno.
  - **Riesgos/fragilidades:** El grafo se expone como bloque `code` con Mermaid textual, no como SVG con roles de nodos; emojis y marcas pueden variar; el DOM puede rerenderizarse.
  - **data-testid:** No indispensable.

  ### GRA-02

  - **Objetivo:** Confirmar que el botón real inicia la animación BPMN, muestra avance y termina en estado completado.
  - **Precondiciones:** `page.goto('/')`; pestaña abierta; iframe cargado; estado inicial `Listo para iniciar`; velocidad por defecto observada `Velocidad normal`.
  - **Resultado observable:** Bitácora y estado avanzan desde `Listo para iniciar` hasta `Workflow completado`, con cierre y trazabilidad.
  - **Localizadores:** `locator('iframe[title="st.iframe"]').contentFrame()`; dentro del frame `getByRole('button', { name: '▶ Ejecutar flujo' })`, `getByRole('combobox')`, `getByRole('heading', { name: 'Bitácora de ejecución' })` y textos de estado. Re-obtener el frame tras rerenders.
  - **Assertions:** `expect(...).toBeVisible()` y `toHaveText()`; `expect.poll` sobre el texto del panel de estado o bitácora para estados asíncronos; no timestamps ni esperas temporizadas.
  - **Datos necesarios:** Ninguno.
  - **Riesgos/fragilidades:** Animación asíncrona y iframe reconstruible; duración dependiente de velocidad y entorno; clases visuales de cajas no son localizadores accesibles estables.
  - **data-testid:** No indispensable.

  ### GRA-03

  - **Objetivo:** Confirmar que la simulación abre un incidente, marca rework/retorno y completa la corrección.
  - **Precondiciones:** `page.goto('/')`; pestaña abierta; iframe cargado; estado inicial `Listo para iniciar`; no requiere datos de negocio.
  - **Resultado observable:** Bitácora con `INCIDENTE` en `execute`, `REWORK` hacia `ValidateEvidence`, revalidación/corrección y `Workflow completado`.
  - **Localizadores:** Dentro de `locator('iframe[title="st.iframe"]').contentFrame()`: botón `getByRole('button', { name: '⚠ Simular incidente' })`, textos `Listo para iniciar`, `INCIDENTE`, `REWORK`, `Workflow completado` y heading `Bitácora de ejecución`.
  - **Assertions:** `expect.poll` para aparición de incidente, rework y finalización; re-resolver el contentFrame después del rerender; no asertar timestamps ni milisegundos fijos.
  - **Datos necesarios:** Ninguno.
  - **Riesgos/fragilidades:** El snapshot puede capturar estados intermedios distintos; los mensajes de bitácora son la evidencia observable; el iframe cambia de referencias al reconstruirse.
  - **data-testid:** No indispensable.

  ### GRA-04

  - **Objetivo:** Confirmar que `Reiniciar` restaura el estado inicial y limpia la trazabilidad visual acumulada.
  - **Precondiciones:** `page.goto('/')`; pestaña abierta; ejecutar primero `⚠ Simular incidente` y esperar por `Workflow completado` para producir un estado no inicial.
  - **Resultado observable:** Estado exacto `Listo para iniciar`, ayuda inicial, bitácora sin entradas y cajas BPMN en estado inicial.
  - **Localizadores:** Dentro del iframe: botones `⚠ Simular incidente`, `↺ Reiniciar`, `▶ Ejecutar flujo`; textos `Workflow completado`, `Listo para iniciar`; heading `Bitácora de ejecución`; ayuda inicial estable. No usar refs de snapshots.
  - **Assertions:** `expect.poll` para el estado previo y para el estado posterior; `toHaveText('Listo para iniciar')`; ausencia de mensajes anteriores con `not.toBeVisible()` o conteo de entradas solo si el DOM estable lo permite; re-obtener el frame tras rerender.
  - **Datos necesarios:** Ninguno; la simulación de incidente prepara el estado no inicial.
  - **Riesgos/fragilidades:** No pulsar durante la animación; la bitácora puede conservar contenedores vacíos, por lo que se verifica ausencia de textos y no una estructura DOM inventada; el iframe se rerenderiza.
  - **data-testid:** No indispensable.

  ## Recomendación de automatización

  - GRA-01 automatizable: **Sí**.
  - GRA-02 automatizable: **Sí**, con `expect.poll` y re-resolución del iframe.
  - GRA-03 automatizable: **Sí**, con `expect.poll` para `INCIDENTE`, `REWORK` y el estado final.
  - GRA-04 automatizable: **Sí**, esperando finalización antes de reiniciar.
  - Total: **4 casos automatizables**.
  - Fragilidades principales: rerenders de Streamlit, iframe BPMN reconstruible, tiempos de animación variables, timestamps dinámicos y grafo expuesto como texto Mermaid.
  - Cambios de aplicación requeridos: **No**.
  - Tokens: **tokens no expuestos por la interfaz**.
