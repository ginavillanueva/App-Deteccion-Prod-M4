# PLAN 02 - Contexto, producto, fuente y nota

## Application Overview

Plan Playwright para App Deteccion Prod (http://127.0.0.1:8501/) limitado exclusivamente a CTX-01, PRD-01, SRC-01 y NOTE-01. Los cuatro casos parten de una navegacion independiente a '/', verifican solo estado observable previo a la ejecucion y no pulsan EJECUTAR, PAUSAR, REANUDAR ni RECUPERAR. La exploracion real encontro controles accesibles: combobox Departamento, Cadena, Sala y Producto; radiogroup Fuente de consulta MCP con DEMO VALIDADO y CONTEXTO EMPRESARIAL; textbox Pregunta que entra a LangGraph; y textbox Nota operativa adicional (queda en evidencia, no altera automaticamente la pregunta). La interfaz no expone tokens de entrada ni salida.

## Test Scenarios

### 1. Contexto, producto, fuente y nota - seleccion y estado previo

**Seed:** `seed.spec.ts`

#### 1.1. CTX-01 - Seleccionar Departamento, Cadena y Sala refleja la sala empresarial

**File:** `tests/planner/ctx-01.spec.ts`

**Steps:**
  1. Precondicion: iniciar un caso independiente con `await page.goto('/')`; esperar de forma semantica a que el combobox `Departamento` sea visible y no ejecutar el workflow.
    - expect: La pagina muestra los selectores accesibles de Departamento, Cadena y Sala.
  2. Usar el selector accesible por rol y etiqueta visible `Departamento` para elegir `2 - Santa Cruz`.
    - expect: El valor elegido de Departamento queda visible.
    - expect: Los controles dependientes Cadena y Sala se actualizan sin error.
  3. Usar el selector accesible por rol y etiqueta visible `Cadena` para elegir `Brands`.
    - expect: El valor elegido de Cadena queda visible.
    - expect: El selector Sala refleja una sala correspondiente a la combinacion seleccionada.
  4. Usar el selector accesible por rol y etiqueta visible `Sala` para elegir la opcion disponible `200089 — BRANDS SOCIEDAD DE RESPONSABILIDAD LIMITADA` (o localizarla por el texto exacto que exponga la interfaz para esa opcion).
    - expect: El valor elegido de Sala queda visible.
  5. Localizar el texto visible asociado al resultado `Sala empresarial:`.
    - expect: La pantalla muestra `Sala empresarial: BRANDS SOCIEDAD DE RESPONSABILIDAD LIMITADA · COD 200089 · Cadena Brands · DPTO 2 - Santa Cruz`.
    - expect: El resultado observable corresponde a la seleccion real y no depende de un ref dinamico del snapshot.

  **Auditoria:**
  - ID del caso Planner: CTX-01
  - Flujo del inventario cubierto: CTX-01
  - Precondicion: `await page.goto('/')`; interfaz operativa cargada; workflow sin ejecutar.
  - Pasos de la persona: seleccionar Departamento `2 - Santa Cruz`, Cadena `Brands` y la Sala empresarial disponible `200089`.
  - Resultado observable esperado: el texto visible de `Sala empresarial:` refleja `BRANDS SOCIEDAD DE RESPONSABILIDAD LIMITADA`, codigo `200089`, Cadena `Brands` y DPTO `2 - Santa Cruz`.
  - Localizadores recomendados: `getByRole('combobox', { name: /Departamento/ })`, `getByRole('combobox', { name: /Cadena/ })`, `getByRole('combobox', { name: /Sala/ })`, `getByRole('option', { name: /Brands|200089/ })`, `getByText('Sala empresarial:', { exact: false })`.
  - Datos propios necesarios: Departamento `2 - Santa Cruz`; Cadena `Brands`; Sala `200089 — BRANDS SOCIEDAD DE RESPONSABILIDAD LIMITADA`.
  - Riesgos o fragilidad: Streamlit regenera nombres accesibles con el valor seleccionado y los refs del snapshot son dinamicos; seleccionar Departamento o Cadena actualiza controles dependientes y puede cambiar sus valores.
  - Requiere un data-testid nuevo: No para el alcance actual; recomendar `data-testid="sala-empresarial-result"` si el texto compuesto deja de ser estable.
  - Dependencia de otro caso: No.

#### 1.2. PRD-01 - Seleccionar producto muestra producto y clasificacion asociada

**File:** `tests/planner/prd-01.spec.ts`

**Steps:**
  1. Precondicion: iniciar un caso independiente con `await page.goto('/')`; esperar semanticamente al combobox etiquetado `Producto empresarial / observado`; no ejecutar el workflow.
    - expect: El selector de Producto y el texto `Clasificacion` son visibles.
  2. Usar el selector accesible por rol y etiqueta `Producto empresarial / observado` para elegir `0000051433 — Prudential Comfort Total G 4x20`.
    - expect: El valor visible del selector contiene `0000051433 — Prudential Comfort Total G 4x20`.
  3. Localizar el valor visible presentado junto a la etiqueta `Clasificacion`.
    - expect: La clasificacion asociada permanece visible: `Absorbentes / ZAIMELLA / Incontinencia / Confort Total`.
    - expect: El caso comprueba simultaneamente el producto seleccionado y la clasificacion, sin inferir la redaccion de un LLM.

  **Auditoria:**
  - ID del caso Planner: PRD-01
  - Flujo del inventario cubierto: PRD-01
  - Precondicion: `await page.goto('/')`; interfaz operativa cargada; workflow sin ejecutar.
  - Pasos de la persona: seleccionar `0000051433 — Prudential Comfort Total G 4x20` en Producto.
  - Resultado observable esperado: el producto seleccionado y `Absorbentes / ZAIMELLA / Incontinencia / Confort Total` quedan visibles.
  - Localizadores recomendados: `getByRole('combobox', { name: /Producto empresarial \/ observado/ })`, `getByRole('option', { name: /0000051433/ })`, `getByText('Clasificacion', { exact: true })` y el texto de clasificacion dentro del bloque de Producto.
  - Datos propios necesarios: producto `0000051433 — Prudential Comfort Total G 4x20`; clasificacion observable `Absorbentes / ZAIMELLA / Incontinencia / Confort Total`.
  - Riesgos o fragilidad: el nombre accesible del combobox incluye el valor actual y cambia tras la seleccion; el texto `Clasificacion` no tiene por si solo un rol de campo asociado.
  - Requiere un data-testid nuevo: Recomendable, no obligatorio: `data-testid="producto-seleccionado"` y `data-testid="producto-clasificacion"`.
  - Dependencia de otro caso: No.

#### 1.3. SRC-01 - Cambiar la fuente backend deja visible la seleccion antes de ejecutar

**File:** `tests/planner/src-01.spec.ts`

**Steps:**
  1. Precondicion: iniciar un caso independiente con `await page.goto('/')`; esperar semanticamente al radiogroup `Fuente de consulta MCP`; no ejecutar el workflow.
    - expect: Los radios accesibles `DEMO VALIDADO` y `CONTEXTO EMPRESARIAL` son visibles.
    - expect: `DEMO VALIDADO` aparece seleccionado inicialmente.
  2. Seleccionar el radio accesible `CONTEXTO EMPRESARIAL`.
    - expect: `CONTEXTO EMPRESARIAL` aparece seleccionado.
    - expect: `DEMO VALIDADO` deja de aparecer seleccionado.
  3. Comprobar el estado textual visible del modo de fuente antes de cualquier accion de workflow.
    - expect: La interfaz muestra `Modo empresarial: si la BD operativa aun no fue sembrada con este producto/sala puede devolver SIN_RESULTADOS.`
    - expect: El caso termina en este estado y no pulsa ni inspecciona el resultado de `EJECUTAR`.

  **Auditoria:**
  - ID del caso Planner: SRC-01
  - Flujo del inventario cubierto: SRC-01
  - Precondicion: `await page.goto('/')`; interfaz operativa cargada; `DEMO VALIDADO` inicialmente seleccionado; workflow sin ejecutar.
  - Pasos de la persona: seleccionar el radio `CONTEXTO EMPRESARIAL` y observar el estado de fuente.
  - Resultado observable esperado: `CONTEXTO EMPRESARIAL` queda seleccionado, `DEMO VALIDADO` deja de estarlo y aparece el aviso de `Modo empresarial`.
  - Localizadores recomendados: `getByRole('radiogroup', { name: 'Fuente de consulta MCP' })`, `getByRole('radio', { name: 'DEMO VALIDADO' })`, `getByRole('radio', { name: 'CONTEXTO EMPRESARIAL' })`, `getByText('Modo empresarial:', { exact: false })`.
  - Datos propios necesarios: fuente inicial `DEMO VALIDADO`; fuente final `CONTEXTO EMPRESARIAL`.
  - Riesgos o fragilidad: además del estado checked, el texto de modo es el indicador visible; el aviso completo puede cambiar por datos disponibles en la BD.
  - Requiere un data-testid nuevo: No; si se necesita aislar el indicador, recomendar `data-testid="fuente-consulta-mcp"`.
  - Dependencia de otro caso: No.

#### 1.4. NOTE-01 - Conservar nota operativa sin reemplazar la pregunta principal

**File:** `tests/planner/note-01.spec.ts`

**Steps:**
  1. Precondicion: iniciar un caso independiente con `await page.goto('/')`; esperar semanticamente a que los textboxes `Pregunta que entra a LangGraph` y `Nota operativa adicional (queda en evidencia, no altera automaticamente la pregunta)` sean visibles; no ejecutar el workflow.
    - expect: Ambos campos son visibles.
    - expect: La pregunta principal tiene un valor inicial visible.
  2. Leer y guardar el valor inicial del textbox `Pregunta que entra a LangGraph`; despues escribir `Nota controlada NOTE-01` en el textbox de nota operativa usando su etiqueta accesible.
    - expect: El textbox de nota conserva exactamente `Nota controlada NOTE-01`.
    - expect: El valor del textbox de pregunta sigue siendo igual al valor inicial capturado.
  3. Volver a comprobar los dos valores despues del rerender de la interfaz, usando los nombres accesibles de los textboxes y no referencias dinamicas del snapshot.
    - expect: La nota permanece visible con `Nota controlada NOTE-01`.
    - expect: La pregunta principal no contiene ni es reemplazada por el texto de la nota.
    - expect: El caso finaliza sin ejecutar el workflow.

  **Auditoria:**
  - ID del caso Planner: NOTE-01
  - Flujo del inventario cubierto: NOTE-01
  - Precondicion: `await page.goto('/')`; ambos textboxes visibles; workflow sin ejecutar.
  - Pasos de la persona: capturar el valor inicial de `Pregunta que entra a LangGraph`, escribir `Nota controlada NOTE-01` en la nota y volver a leer ambos valores tras el rerender.
  - Resultado observable esperado: la nota permanece exactamente y el valor de la pregunta principal permanece igual al inicial, sin ser sustituido por la nota.
  - Localizadores recomendados: `getByRole('textbox', { name: 'Pregunta que entra a LangGraph' })` y `getByRole('textbox', { name: /Nota operativa adicional/ })`.
  - Datos propios necesarios: nota `Nota controlada NOTE-01`; valor inicial de pregunta capturado desde la interfaz, sin fijarlo como dato dinamico.
  - Riesgos o fragilidad: al escribir, Streamlit puede mostrar temporalmente `Press Ctrl+Enter to apply` y regenerar parte del snapshot; usar aserciones sobre `inputValue()` o valor accesible y esperas semanticas, nunca esperas fijas.
  - Requiere un data-testid nuevo: No; recomendar `data-testid="pregunta-langgraph"` y `data-testid="nota-operativa"` como respaldo si cambian las etiquetas.
  - Dependencia de otro caso: No.

  ## Auditoria final

  - Cantidad total de casos propuestos: 4.
  - Casos aceptables tal como estan: CTX-01, PRD-01, SRC-01 y NOTE-01; cada uno comienza con `await page.goto('/')`, es independiente y no ejecuta el workflow.
  - Riesgos de localizadores encontrados: Streamlit cambia el nombre accesible de los combobox al cambiar su valor; las refs del snapshot son dinamicas; Cadena y Sala son controles dependientes; el texto de clasificacion no esta expuesto como un campo con etiqueta propia; la escritura de nota puede provocar rerender.
  - data-testid adicionales recomendados, sin modificar la aplicacion: `sala-empresarial-result`, `producto-seleccionado`, `producto-clasificacion`, `fuente-consulta-mcp`, `pregunta-langgraph`, `nota-operativa`.
  - Tokens: tokens no expuestos por la interfaz.
  - Restricciones respetadas: no se generaron tests, no se llamo al Generator, no se modificaron `playwright.config.ts`, `seed.spec.ts` ni codigo de la aplicacion, y no se analizaron otros flujos.
