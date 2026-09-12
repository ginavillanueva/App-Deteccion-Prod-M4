# Plan 06 - Trazabilidad

## Application Overview

Plan Playwright exclusivamente para TRZ-01 y TRZ-02 de App Deteccion Prod. Exploracion realizada sobre http://127.0.0.1:8501 con Streamlit real. No se generan tests ni se modifican la aplicacion o tests existentes. Los selectores finales deben ser semanticos y no depender de refs e* del snapshot.

## Test Scenarios

### 1. Trazabilidad

**Seed:** `modulo_bpmn_workflow_engine/seed.spec.ts`

#### 1.1. TRZ-01 - abrir Trazabilidad en thread nuevo

**File:** `NO_GENERAR_TEST_TRZ-01.spec.ts`

**Steps:**
  1. Iniciar el caso con `page.goto('/')` y esperar a que sea visible el encabezado de la aplicacion y el panel `Control`.
    - expect: La URL corresponde a la raiz de la aplicacion.
    - expect: El panel `Control` muestra `Thread ID` y un valor concreto en un elemento `code`.
    - expect: El estado del thread muestra `NO_EXISTE`.
  2. Pulsar el boton accesible `Nuevo thread` para asegurar un thread nuevo e independiente; esperar a que aparezca un Thread ID distinto y el estado `NO_EXISTE`.
    - expect: El Thread ID queda visible en el panel `Control`.
    - expect: El estado visible es `NO_EXISTE`.
    - expect: No se inicia ninguna ejecucion automaticamente.
  3. Pulsar la pestaña accesible `3 · Trazabilidad` y esperar a que el `tabpanel` con ese nombre este visible; no usar refs dinamicas del snapshot.
    - expect: La pestaña `3 · Trazabilidad` queda seleccionada.
    - expect: El `tabpanel` `3 · Trazabilidad` es visible.
  4. Inspeccionar la seccion `Trazabilidad tecnica completa`.
    - expect: Se muestra `Thread:` con el mismo Thread ID visible en `Control` y en Trazabilidad.
    - expect: Se muestra `Estado:` con `NO_EXISTE`.
    - expect: Existe el encabezado `Checkpoint actual`.
    - expect: El contenido JSON del checkpoint actual esta vacio: `{}`.
    - expect: Existe el encabezado `Estado LangGraph`.
    - expect: El contenido JSON del estado LangGraph esta vacio: `{}`.
    - expect: Existe el encabezado `Historial de checkpoints`.
    - expect: Se muestra exactamente `No hay historial cargado.`.
    - expect: Existe el encabezado `Evidencia y contexto empresarial`.
    - expect: Se muestra exactamente `Aun no hay metadata guardada para este thread.`.
  5. Dejar que Streamlit complete sus rerenders mediante assertions de visibilidad o `expect.poll`; no usar `waitForTimeout` ni sleeps.
    - expect: Los elementos esperados permanecen visibles despues del rerender y no hay que depender de posiciones o refs generadas.

#### 1.2. TRZ-02 - abrir Trazabilidad despues de ejecutar

**File:** `NO_GENERAR_TEST_TRZ-02.spec.ts`

**Steps:**
  1. Iniciar el caso con `page.goto('/')` y esperar el panel `Control` y el estado inicial `NO_EXISTE`.
    - expect: La pagina carga en la raiz y el thread inicial es nuevo.
    - expect: El estado visible es `NO_EXISTE`.
  2. En la pestaña `1 · Operacion`, conservar los valores validos por defecto observados: Departamento `1 - La Paz`, Cadena `Andys`, Sala `101797 — ANDYS SAN MIGUEL`, Producto `0000051432 — Prudential Comfort Total M 4x20`, escenario `Vencimiento / riesgo de merma`, fuente `DEMO VALIDADO`; no depender del texto libre del modelo como assertion.
    - expect: Los controles semanticos muestran los valores validos seleccionados.
    - expect: No es necesaria carga de evidencia para este caso.
  3. Pulsar el boton accesible `▶ EJECUTAR` y esperar con `expect` o `expect.poll` a que el workflow llegue a un estado persistido observable. En la ejecucion real explorada, el primer paso deja el thread en `PAUSADO`.
    - expect: El mismo Thread ID sigue visible.
    - expect: El estado cambia a `PAUSADO` en la instalacion observada, o a otro estado persistido observable que debe capturarse sin asumir un tiempo fijo.
    - expect: Cuando queda `PAUSADO`, aparecen `NEXT` con `consultar_detalle_mcp`, el flujo recorrido `validar_entrada -> clasificar_intencion -> extraer_contexto` y `Tools MCP` sin tools ejecutadas.
  4. Si el estado observable es `PAUSADO`, pulsar `⏯ REANUDAR` y esperar con `expect` o `expect.poll` a que aparezca `FINALIZADO`; esta reanudacion es necesaria para obtener el historial completo observado en la ejecucion exploratoria.
    - expect: El mismo Thread ID continua, sin pulsar `Nuevo thread`.
    - expect: El estado final visible es `FINALIZADO`.
    - expect: El flujo final conserva la regla de negocio de VENCIMIENTO y no introduce aprobacion de precio ni ejecucion comercial autonoma.
  5. Pulsar la pestaña accesible `3 · Trazabilidad` y esperar al `tabpanel` `3 · Trazabilidad`.
    - expect: La pestaña esta seleccionada y el panel es visible.
    - expect: La seccion se titula `Trazabilidad tecnica completa`.
  6. Inspeccionar `Checkpoint actual` y `Estado LangGraph` despues de la ejecucion.
    - expect: `Thread:` muestra exactamente el mismo Thread ID que `Control`.
    - expect: `Estado:` muestra `FINALIZADO` en la ruta completada observada.
    - expect: `Checkpoint actual` contiene un JSON no vacio con `values`, `next` y `metadata`.
    - expect: En `values` son visibles, al menos, la pregunta, `thread_id`, `intencion`=`VENCIMIENTO`, `producto`=`Yogur natural 1 litro` y `tienda`=`Sala 12`.
    - expect: `next` del checkpoint actual aparece vacio al finalizar.
    - expect: `metadata` tecnica del checkpoint muestra al menos `loop` con valor numerico; no asumir un valor exacto si cambia entre ejecuciones.
    - expect: `Estado LangGraph` muestra campos visibles como `pregunta`, `thread_id`, `intencion`, `producto`, `tienda`, `fuentes`, `tools_usadas`, `observaciones`, `bloqueado`, `problema` y `traza`.
    - expect: La evidencia observada muestra `fuentes` con `productos_vencimiento` y `tools_usadas` con `consultar_detalle_producto`.
  7. Inspeccionar `Historial de checkpoints`, usando los botones/summary accesibles por su nombre visible y sin refs dinamicas.
    - expect: El encabezado `Historial de checkpoints` es visible.
    - expect: En la ejecucion explorada aparecen seis entradas expandibles: `Checkpoint 1 · NEXT=[]`, `Checkpoint 2 · NEXT=['consultar_detalle_mcp']`, `Checkpoint 3 · NEXT=['extraer_contexto']`, `Checkpoint 4 · NEXT=['clasificar_intencion']`, `Checkpoint 5 · NEXT=['validar_entrada']` y `Checkpoint 6 · NEXT=['start']`.
    - expect: Cada entrada es tratada como evidencia de historial; no se debe afirmar que el orden o el numero sean invariantes si la aplicacion cambia el grafo. Como assertion minima, debe existir al menos una entrada `Checkpoint` y al menos una entrada con `NEXT`.
  8. Inspeccionar `Evidencia y contexto empresarial` sin confundirlo con la metadata tecnica del JSON.
    - expect: La seccion es visible.
    - expect: En la ejecucion explorada se muestra `Aun no hay metadata guardada para este thread.` porque no se adjunto evidencia ni metadata empresarial.
    - expect: No se exige un token: tokens no expuestos por la interfaz.
  9. Esperar el rerender de Streamlit mediante estados visibles (`FINALIZADO`, encabezados y summaries) o `expect.poll`; no usar sleeps ni `waitForTimeout`.
    - expect: Las assertions se ejecutan sobre el DOM accesible despues del rerender completo.
    - expect: El test no depende de refs `e...`, clases CSS generadas, indices visuales, coordenadas ni tiempos fijos.
