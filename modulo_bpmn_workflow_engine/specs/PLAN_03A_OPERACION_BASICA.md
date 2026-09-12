# PLAN 03A - Operacion basica App Deteccion Prod

## Application Overview

Plan exclusivamente de auditoria Playwright para OPE-01, OPE-02, OPE-03 y OPE-04 contra http://127.0.0.1:8501/. La exploracion se realizo sobre la aplicacion real usando un thread independiente por caso. No se generan tests ni se llama al Generator. Los resultados se validan solo por evidencia observable estructurada: estado, escenario/intencion, fuente, tool, checkpoint/NEXT y observaciones MCP; no se valida redaccion libre de LLM. Tokens no expuestos por la interfaz.

## Test Scenarios

### 1. Operacion basica OPE-01 a OPE-04

**Seed:** `seed.spec.ts`

#### 1.1. OPE-01 - Thread nuevo sin ejecutar queda en NO_EXISTE

**File:** `NO GENERAR TEST - caso de planificacion`

**Steps:**
  1. await page.goto('/');
    - expect: La aplicacion carga en la vista 1 · Operacion y expone controles semanticos para Thread ID y estado del thread.
  2. Usar getByRole('button', { name: /Nuevo thread/i }) para abrir un thread nuevo.
    - expect: Se muestra un Thread ID nuevo o activo en el panel de control.
    - expect: No se pulsa EJECUTAR ni PAUSAR.
  3. Usar getByRole('alert') y getByText('NO_EXISTE') para comprobar el estado del thread.
    - expect: El estado visible del thread es exactamente NO_EXISTE.
    - expect: La interfaz mantiene el mensaje de thread nuevo y no muestra workflow finalizado, tool ejecutada, checkpoint ni observacion de ejecucion.
    - expect: Resultado observable: OPE-01 aceptable si NO_EXISTE esta visible en el panel de Estado thread.
  4. Localizadores recomendados: getByRole('button', { name: /Nuevo thread/i }), getByRole('alert'), getByText('NO_EXISTE') o getByRole('heading', { name: /NO_EXISTE/ }).
    - expect: Datos propios necesarios: ninguno; el thread recien creado es el dato propio.
    - expect: Riesgo/fragilidad: el Thread ID es dinamico y no debe usarse como localizador; el estado puede aparecer en mas de un bloque si se inspecciona el historial.
    - expect: data-testid: no requerido; opcionalmente recomendar data-testid='thread-status' para el estado y data-testid='new-thread' para el boton.
    - expect: Dependencia de otro caso: no.
    - expect: Tokens: tokens no expuestos por la interfaz.

#### 1.2. OPE-02 - VENCIMIENTO finaliza y deja evidencia de detalle/vencimiento

**File:** `NO GENERAR TEST - caso de planificacion`

**Steps:**
  1. await page.goto('/');
    - expect: La aplicacion carga en estado inicial y permite comenzar un thread independiente.
  2. Usar getByRole('button', { name: /Nuevo thread/i }) para crear el thread del caso.
    - expect: El nuevo thread muestra NO_EXISTE antes de ejecutar.
  3. En el combobox cuyo nombre accesible contiene Escenario, abrir la lista y seleccionar la opcion visible Vencimiento / riesgo de merma. Mantener la fuente DEMO VALIDADO visible, salvo que el caso decida probar CONTEXTO EMPRESARIAL.
    - expect: El escenario seleccionado queda visible como Vencimiento / riesgo de merma.
    - expect: La fuente de consulta MCP seleccionada queda visible como DEMO VALIDADO o CONTEXTO EMPRESARIAL, y se registra cual se uso.
  4. Conservar o introducir los datos operativos observados: producto Yogur natural 1 litro, Sala 12 y pregunta 'Cuantos dias faltan para vencer el Yogur natural 1 litro de la Sala 12'. Usar getByRole('textbox', { name: 'Pregunta que entra a LangGraph' }) solo si hace falta completar la pregunta.
    - expect: La pregunta/datos necesarios quedan visibles antes de ejecutar; no se valida la redaccion libre de la respuesta.
  5. Usar getByRole('button', { name: /EJECUTAR/i }) para ejecutar el workflow.
    - expect: La interfaz muestra la alerta de ejecucion real completada y evidencia trazada, o equivalente observable de finalizacion.
  6. Esperar por una señal de UI, no por tiempo fijo, y comprobar getByText('FINALIZADO') o el heading de estado final.
    - expect: El estado visible es FINALIZADO.
    - expect: La intencion/escenario visible es VENCIMIENTO.
    - expect: La evidencia estructurada muestra Tools ejecutadas = 1 y Observaciones = 1.
    - expect: El flujo real visible marca consultar_detalle_mcp como Ejecutado y muestra la secuencia terminada en END.
    - expect: La seccion Tools MCP muestra consultar_detalle_producto.
    - expect: La seccion Fuentes de datos muestra productos_vencimiento.
    - expect: La seccion NEXT/checkpoint muestra [].
    - expect: La seccion Resultados / observaciones MCP contiene la observacion expandible de consultar_detalle_producto.
    - expect: Resultado observable: OPE-02 aceptable si se ven estado final y evidencia de consulta de detalle/vencimiento mediante tool y/o fuente; no se exige texto exacto de la respuesta.
  7. Localizadores recomendados: getByRole('combobox', { name: /Escenario/i }), getByRole('option', { name: /Vencimiento/i }), getByRole('radio', { name: /DEMO VALIDADO/i }) o CONTEXTO EMPRESARIAL, getByRole('textbox', { name: 'Pregunta que entra a LangGraph' }), getByRole('button', { name: /EJECUTAR/i }), getByText('FINALIZADO'), getByText('consultar_detalle_producto'), getByText('productos_vencimiento'), getByText('Resultados / observaciones MCP').
    - expect: Datos propios necesarios: producto Yogur natural 1 litro, Sala 12 y pregunta de vencimiento; fuente seleccionada debe quedar registrada en la auditoria.
    - expect: Riesgo/fragilidad: el combobox es custom y su nombre incluye el valor actual; preferir regex por Escenario y opcion por texto visible. Los bloques JSON/renderizados pueden cambiar de estructura, por lo que conviene afirmar tool/fuente/checkpoint por texto estructurado, no por refs del snapshot.
    - expect: data-testid: no requerido para el flujo; recomendar data-testid='workflow-status', 'workflow-intent', 'executed-tools', 'data-sources', 'checkpoint-next' y 'mcp-observation' si los roles/textos estructurados no fueran estables.
    - expect: Dependencia de otro caso: no; debe comenzar desde await page.goto('/').
    - expect: Tokens: tokens no expuestos por la interfaz.

#### 1.3. OPE-03 - CAMBIO_PRECIO es consulta informativa trazable

**File:** `NO GENERAR TEST - caso de planificacion`

**Steps:**
  1. await page.goto('/');
    - expect: La aplicacion carga en la vista Operacion y permite iniciar un thread nuevo.
  2. Usar getByRole('button', { name: /Nuevo thread/i }) para crear un thread independiente.
    - expect: El thread nuevo muestra NO_EXISTE antes de ejecutar.
  3. Abrir el combobox de Escenario y seleccionar la opcion visible Cambio de precio (informativo, sin aprobacion). Mantener DEMO VALIDADO o seleccionar CONTEXTO EMPRESARIAL y registrar la fuente.
    - expect: El escenario visible contiene Cambio de precio (informativo, sin aprobacion).
    - expect: La interfaz mantiene visible la regla de que CAMBIO_PRECIO nunca aprueba ni modifica precios.
  4. Usar los datos observados: producto Yogur natural 1 litro, Sala 12 y pregunta 'El Yogur natural 1 litro tuvo cambios de precio en la Sala 12'. Completar el textbox de pregunta solo si el valor no esta ya cargado.
    - expect: La pregunta de consulta queda visible antes de ejecutar.
  5. Pulsar getByRole('button', { name: /EJECUTAR/i }).
    - expect: La interfaz muestra evidencia de ejecucion completada.
  6. Esperar por estado visible y comprobar FINALIZADO, sin validar la redaccion libre de la respuesta.
    - expect: El estado visible es FINALIZADO.
    - expect: La intencion/escenario visible es CAMBIO_PRECIO.
    - expect: La evidencia muestra Tools ejecutadas = 1 y Observaciones = 1.
    - expect: El flujo real marca consultar_cambios_precio_mcp como Ejecutado y termina en END.
    - expect: La seccion Tools MCP muestra consultar_cambios_precio.
    - expect: La seccion Fuentes de datos muestra cambios_precio; cualquier fuente adicional visible se registra sin convertirla en criterio de aprobacion.
    - expect: La seccion NEXT/checkpoint muestra [].
    - expect: La observacion MCP expandible identifica consultar_cambios_precio.
    - expect: Resultado observable: OPE-03 aceptable si se demuestra una consulta informativa trazable por estado, tool y/o fuente.
    - expect: Regla obligatoria: consulta informativa; no es aprobacion de precio. No proponer ni verificar aprobacion, modificacion o autorizacion de precios.
  7. Localizadores recomendados: getByRole('combobox', { name: /Escenario/i }), getByRole('option', { name: /Cambio de precio.*informativo/i }), getByRole('textbox', { name: 'Pregunta que entra a LangGraph' }), getByRole('button', { name: /EJECUTAR/i }), getByText('FINALIZADO'), getByText('consultar_cambios_precio'), getByText('cambios_precio'), getByText('Resultados / observaciones MCP').
    - expect: Datos propios necesarios: producto Yogur natural 1 litro, Sala 12, pregunta de cambios de precio y fuente seleccionada.
    - expect: Riesgo/fragilidad: no usar el texto de la respuesta como oracle; el nombre del combobox cambia con la opcion elegida. No usar refs eNN del snapshot.
    - expect: data-testid: no requerido; recomendar data-testid='workflow-intent', 'executed-tools', 'data-sources', 'checkpoint-next' y 'mcp-observation' si las afirmaciones por rol/texto resultan ambiguas.
    - expect: Dependencia de otro caso: no.
    - expect: Tokens: tokens no expuestos por la interfaz.

#### 1.4. OPE-04 - ACCION_COMERCIAL consulta registros sin ejecucion autonoma

**File:** `NO GENERAR TEST - caso de planificacion`

**Steps:**
  1. await page.goto('/');
    - expect: La aplicacion carga en la vista Operacion y permite iniciar un thread nuevo.
  2. Usar getByRole('button', { name: /Nuevo thread/i }) para crear un thread independiente.
    - expect: El thread nuevo muestra NO_EXISTE antes de ejecutar.
  3. Abrir el combobox de Escenario y seleccionar la opcion visible Accion comercial registrada. Mantener DEMO VALIDADO o seleccionar CONTEXTO EMPRESARIAL y registrar la fuente.
    - expect: El escenario seleccionado queda visible como Accion comercial registrada.
    - expect: La interfaz conserva la regla de que la aplicacion consulta registros y no ejecuta acciones comerciales de forma autonoma.
  4. Usar los datos observados: producto Yogur natural 1 litro, Sala 12 y pregunta 'Que accion comercial tiene el Yogur natural 1 litro en la Sala 12'. Completar getByRole('textbox', { name: 'Pregunta que entra a LangGraph' }) solo si es necesario.
    - expect: La pregunta/datos necesarios quedan visibles antes de ejecutar.
  5. Pulsar getByRole('button', { name: /EJECUTAR/i }).
    - expect: La interfaz muestra evidencia de ejecucion completada.
  6. Esperar por estado visible y comprobar FINALIZADO, sin validar la redaccion libre de la respuesta.
    - expect: El estado visible es FINALIZADO.
    - expect: La intencion/escenario visible es ACCION_COMERCIAL.
    - expect: La evidencia muestra Tools ejecutadas = 1 y Observaciones = 1.
    - expect: El flujo real marca consultar_acciones_comerciales_mcp como Ejecutado y termina en END.
    - expect: La seccion Tools MCP muestra consultar_acciones_comerciales.
    - expect: La seccion Fuentes de datos muestra acciones_comerciales.
    - expect: La seccion NEXT/checkpoint muestra [].
    - expect: La observacion MCP expandible identifica consultar_acciones_comerciales.
    - expect: Resultado observable: OPE-04 aceptable si se demuestra la consulta de registros comerciales por estado, tool y/o fuente.
    - expect: Regla obligatoria: consulta registros; no ejecuta acciones comerciales autónomas. No proponer ni verificar una ejecución de campañas, promociones, cambios de exhibición o cualquier otra acción comercial real.
  7. Localizadores recomendados: getByRole('combobox', { name: /Escenario/i }), getByRole('option', { name: /Accion comercial registrada/i }), getByRole('textbox', { name: 'Pregunta que entra a LangGraph' }), getByRole('button', { name: /EJECUTAR/i }), getByText('FINALIZADO'), getByText('consultar_acciones_comerciales'), getByText('acciones_comerciales'), getByText('Resultados / observaciones MCP').
    - expect: Datos propios necesarios: producto Yogur natural 1 litro, Sala 12, pregunta de registros comerciales y fuente seleccionada.
    - expect: Riesgo/fragilidad: no usar texto libre como oracle; el selector de escenario es un combobox custom y la estructura JSON de observacion puede variar.
    - expect: data-testid: no requerido; recomendar data-testid='workflow-intent', 'executed-tools', 'data-sources', 'checkpoint-next' y 'mcp-observation' si los roles/textos no fueran suficientes.
    - expect: Dependencia de otro caso: no.
    - expect: Tokens: tokens no expuestos por la interfaz.
