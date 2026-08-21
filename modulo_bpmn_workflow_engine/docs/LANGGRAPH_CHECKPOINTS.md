# Persistencia de Estado y Checkpoints con LangGraph

## App Deteccion Prod

Este documento registra la implementacion de persistencia de estado
para la orquestacion LangGraph utilizada por App Deteccion Prod.

---

## 1. Objetivo

El objetivo es permitir que el estado de una ejecucion LangGraph pueda:

- persistirse en SQLite;
- identificarse mediante `thread_id`;
- recuperarse despues de finalizar el proceso Python;
- conservar historial de checkpoints;
- mantener trazabilidad de nodos ejecutados;
- trabajar de forma asincrona con los nodos MCP existentes.

---

## 2. Tecnologias utilizadas

La implementacion utiliza:

- LangGraph 1.2.11
- langgraph-checkpoint-sqlite 3.1.1
- AsyncSqliteSaver
- aiosqlite
- SQLite
- configurable.thread_id

La base utilizada por LangGraph es:

~~~text
data/langgraph_checkpoints.sqlite
~~~

Esta base es generada en runtime y no se versiona en Git.

La regla existente en `.gitignore` es:

~~~text
*.sqlite
~~~

---

## 3. Separacion de responsabilidades

El proyecto mantiene dos niveles diferentes de persistencia.

### 3.1 Persistencia del motor BPMN

Archivo:

~~~text
src/persistence/sqlite_repository.py
~~~

Esta capa conserva informacion operacional del motor, como:

- definiciones de workflows;
- instancias;
- tareas;
- trazas;
- incidentes;
- workers.

### 3.2 Persistencia nativa de LangGraph

Archivo:

~~~text
src/persistence/langgraph_checkpointer.py
~~~

Esta capa se encarga de:

- checkpoints del StateGraph;
- estado asociado a un thread;
- historial de ejecucion;
- recuperacion del estado;
- continuidad mediante `thread_id`.

Por lo tanto:

~~~text
Persistencia BPMN
        !=
Persistencia de checkpoints LangGraph
~~~

Ambas utilizan SQLite, pero cumplen responsabilidades diferentes.

---

## 4. Configuracion mediante thread_id

LangGraph identifica la ejecucion persistente mediante:

~~~python
{
    "configurable": {
        "thread_id": "identificador-del-thread"
    }
}
~~~

En el proyecto esta configuracion se genera mediante:

~~~python
crear_config_checkpoint(thread_id)
~~~

Ejemplo:

~~~python
{
    "configurable": {
        "thread_id": "persistencia-vencimiento-001"
    }
}
~~~

El `thread_id` permite recuperar posteriormente los checkpoints
correspondientes a la misma ejecucion.

---

## 5. Checkpointer asincrono

Se utiliza:

~~~python
AsyncSqliteSaver
~~~

Esto permite mantener la arquitectura asincrona existente.

El flujo puede continuar utilizando:

~~~python
await grafo.ainvoke(...)
~~~

El checkpointer se abre mediante:

~~~python
async with abrir_checkpointer_langgraph() as checkpointer:
    ...
~~~

y se inicializa mediante:

~~~python
await checkpointer.setup()
~~~

---

## 6. Base SQLite de LangGraph

La prueba de inicializacion confirmo la creacion correcta de:

~~~text
data/langgraph_checkpoints.sqlite
~~~

Resultado obtenido:

~~~text
CHECKPOINTER ABIERTO:
<class 'langgraph.checkpoint.sqlite.aio.AsyncSqliteSaver'>

SETUP COMPLETADO: OK
EXISTE DESPUES: True
CHECKPOINT DATABASE OK
~~~

LangGraph creo automaticamente las tablas:

~~~text
checkpoints
writes
~~~

Estas tablas pertenecen al mecanismo interno de persistencia de
LangGraph.

---

## 7. Runtime persistente reutilizable

Archivo:

~~~text
src/langgraph_orchestration/persistent_runtime.py
~~~

El runtime encapsula la integracion entre:

~~~text
EstadoDeteccion
      |
      v
StateGraph
      |
      v
AsyncSqliteSaver
      |
      v
SQLite
~~~

Expone las siguientes funciones.

### ejecutar_persistente

~~~python
await ejecutar_persistente(
    pregunta,
    thread_id,
)
~~~

Ejecuta el workflow utilizando checkpoints persistentes.

### recuperar_estado_persistido

~~~python
await recuperar_estado_persistido(
    thread_id
)
~~~

Recupera el ultimo estado almacenado.

Esta operacion no necesita volver a ejecutar el workflow.

### obtener_historial_persistido

~~~python
await obtener_historial_persistido(
    thread_id
)
~~~

Recupera los checkpoints asociados al thread.

### existe_estado_persistido

~~~python
await existe_estado_persistido(
    thread_id
)
~~~

Comprueba si existe estado almacenado para ese identificador.

---

## 8. Prueba de persistencia real

Se ejecuto el caso:

~~~text
THREAD:
persistencia-vencimiento-001

PREGUNTA:
Cuantos dias faltan para vencer el Yogur natural 1 litro de la Sala 12
~~~

La ejecucion paso por:

~~~text
validar_entrada
        |
        v
clasificar_intencion
        |
        v
extraer_contexto
        |
        v
consultar_detalle_mcp
        |
        v
END
~~~

Resultado:

~~~text
INTENCION: VENCIMIENTO
PRODUCTO: Yogur natural 1 litro
TIENDA: Sala 12
TOOLS: ['consultar_detalle_producto']
~~~

---

## 9. Recuperacion desde otro proceso Python

Despues de terminar completamente el primer proceso Python,
se inicio un segundo proceso.

En el segundo proceso no se ejecuto nuevamente:

~~~python
ainvoke(...)
~~~

Tampoco se volvieron a ejecutar las herramientas MCP.

Solo se solicito el estado mediante el mismo `thread_id`.

El resultado recuperado desde SQLite fue:

~~~text
SNAPSHOT EXISTE: True
NEXT: ()

THREAD: persistencia-vencimiento-001
INTENCION: VENCIMIENTO
PRODUCTO: Yogur natural 1 litro
TIENDA: Sala 12
BLOQUEADO: False
TOOLS: ['consultar_detalle_producto']
FUENTES: ['productos_vencimiento']
TOTAL OBSERVACIONES: 1
~~~

Resultado:

~~~text
PERSISTENCIA ENTRE PROCESOS: OK
~~~

Esta prueba demuestra que el estado sobrevive al ciclo de vida
del proceso Python.

---

## 10. Historial de checkpoints

Para el thread:

~~~text
persistencia-vencimiento-001
~~~

se recuperaron:

~~~text
TOTAL CHECKPOINTS: 6
~~~

La secuencia registrada permite observar la evolucion del workflow.

### Checkpoint final

~~~text
NEXT: ()
INTENCION: VENCIMIENTO
PRODUCTO: Yogur natural 1 litro
TIENDA: Sala 12
TOOLS: ['consultar_detalle_producto']
~~~

### Checkpoint anterior

~~~text
NEXT: ('consultar_detalle_mcp',)
~~~

### Checkpoint de contexto

~~~text
NEXT: ('extraer_contexto',)
~~~

### Checkpoint de clasificacion

~~~text
NEXT: ('clasificar_intencion',)
~~~

### Checkpoint de validacion

~~~text
NEXT: ('validar_entrada',)
~~~

### Checkpoint de entrada

~~~text
NEXT: ('__start__',)
~~~

Resultado:

~~~text
HISTORIAL CHECKPOINTS: OK
~~~

---

## 11. Regresion persistente

Se realizo una regresion sobre seis escenarios del sistema.

### 11.1 VENCIMIENTO

Resultado:

~~~text
INTENCION: VENCIMIENTO
BLOQUEADO: False
PRODUCTO: Yogur natural 1 litro
TIENDA: Sala 12
TOOLS: ['consultar_detalle_producto']
FUENTES: ['productos_vencimiento']
CHECKPOINTS: 6
RESULTADO: PASS
~~~

---

### 11.2 CAMBIO_PRECIO

Resultado:

~~~text
INTENCION: CAMBIO_PRECIO
BLOQUEADO: False
PRODUCTO: Yogur natural 1 litro
TIENDA: Sala 12
TOOLS: ['consultar_cambios_precio']
FUENTES:
[
    'cambios_precio',
    'productos_vencimiento'
]
CHECKPOINTS: 6
RESULTADO: PASS
~~~

La consulta de cambios de precio es informativa y de trazabilidad.

No representa aprobacion de un cambio de precio.

---

### 11.3 ACCION_COMERCIAL

Resultado:

~~~text
INTENCION: ACCION_COMERCIAL
BLOQUEADO: False
PRODUCTO: Yogur natural 1 litro
TIENDA: Sala 12
TOOLS: ['consultar_acciones_comerciales']
CHECKPOINTS: 6
RESULTADO: PASS
~~~

La herramienta consulta acciones comerciales previamente registradas.

LangGraph no ejecuta autonomamente una accion comercial.

---

### 11.4 AUDITORIA_EXPLICITA

Ejemplo de consulta:

~~~text
Necesito una auditoria completa
del Yogur natural 1 litro de la Sala 12
~~~

Resultado:

~~~text
INTENCION: AUDITORIA_COMPLETA
BLOQUEADO: False

TOOLS:
[
    'consultar_detalle_producto',
    'consultar_cambios_precio',
    'consultar_acciones_comerciales'
]

CHECKPOINTS: 8
RESULTADO: PASS
~~~

El flujo ejecuta las tres consultas necesarias de forma orquestada.

---

### 11.5 AUDITORIA_MULTIPLE

Ejemplo:

~~~text
Revisa vencimiento, cambios de precio
y accion comercial del Yogur natural
1 litro de la Sala 12
~~~

Resultado:

~~~text
INTENCION: AUDITORIA_COMPLETA
BLOQUEADO: False

TOOLS:
[
    'consultar_detalle_producto',
    'consultar_cambios_precio',
    'consultar_acciones_comerciales'
]

CHECKPOINTS: 8
RESULTADO: PASS
~~~

La deteccion de multiples categorias produce una auditoria completa.

---

### 11.6 SEGURIDAD

Se probo un intento de prompt injection.

Resultado:

~~~text
INTENCION: OTRO
BLOQUEADO: True
PROBLEMA: PROMPT_INJECTION
PRODUCTO:
TIENDA:
TOOLS: []
FUENTES: []
NODOS: ['validar_entrada']
CHECKPOINTS: 3
RESULTADO: PASS
~~~

El guardrail detiene el flujo antes de ejecutar herramientas MCP.

---

## 12. Resultado final de regresion

La regresion persistente final produjo:

~~~text
APROBADOS: 6
TOTAL: 6
REGRESION PERSISTENTE 6/6: OK
~~~

Esto demuestra que incorporar checkpoints no rompio las ramas
funcionales existentes.

---

## 13. Arquitectura resultante

~~~text
Usuario / Aplicacion
        |
        v
crear_estado_inicial
        |
        v
validar_entrada
        |
        v
clasificar_intencion
        |
        v
extraer_contexto
        |
        +--------------------------+
        |            |             |
        v            v             v
 VENCIMIENTO    CAMBIO_PRECIO   ACCION_COMERCIAL
        |            |             |
        +------------+-------------+
                     |
                     v
               Nodos MCP
                     |
                     v
                 tools/call
                     |
                     v
              Datos de negocio


En paralelo:

StateGraph
    |
    v
configurable.thread_id
    |
    v
AsyncSqliteSaver
    |
    v
langgraph_checkpoints.sqlite
    |
    +--> checkpoints
    |
    +--> writes
~~~

---

## 14. Flujo de persistencia

~~~text
Pregunta
   |
   v
thread_id
   |
   v
crear_config_checkpoint
   |
   v
configurable.thread_id
   |
   v
StateGraph compilado
con checkpointer
   |
   v
ejecucion de nodos
   |
   v
AsyncSqliteSaver
   |
   v
SQLite
   |
   v
checkpoint persistido
~~~

Posteriormente:

~~~text
Nuevo proceso Python
        |
        v
mismo thread_id
        |
        v
aget_state()
        |
        v
SQLite
        |
        v
estado recuperado
~~~

---

## 15. Evidencias tecnicas obtenidas

La implementacion demuestra:

- StateGraph real;
- routing condicional;
- integracion con MCP;
- ejecucion asincrona;
- estado explicito;
- guardrails;
- extraccion de contexto;
- auditoria multi-herramienta;
- configurable.thread_id;
- AsyncSqliteSaver;
- SQLite persistente;
- checkpoints;
- historial;
- recuperacion entre procesos;
- trazabilidad por nodos;
- regresion funcional 6/6.

---

## 16. Archivos principales

### Checkpointer

~~~text
src/persistence/langgraph_checkpointer.py
~~~

Responsable de:

- ruta del SQLite;
- inicializacion;
- AsyncSqliteSaver;
- configuracion del thread.

### Runtime

~~~text
src/langgraph_orchestration/persistent_runtime.py
~~~

Responsable de:

- ejecutar con persistencia;
- recuperar estado;
- consultar historial;
- verificar existencia del estado.

### Grafo

~~~text
src/langgraph_orchestration/graph.py
~~~

Contiene la definicion del StateGraph y sus rutas.

### Nodos MCP

~~~text
src/langgraph_orchestration/mcp_nodes.py
~~~

Contiene los nodos que reutilizan las herramientas MCP.

---

## 17. Consideracion de negocio sobre precios

La funcionalidad de cambio de precio tiene finalidad:

~~~text
CONSULTA_INFORMATIVA_SIN_APROBACION
~~~

El sistema consulta y muestra que existio un cambio de precio.

No aprueba autonomamente cambios de precio.

---

## 18. Consideracion de negocio sobre acciones comerciales

La funcionalidad de accion comercial utiliza:

~~~text
CONSULTA_DE_REGISTRO_SIN_EJECUCION_AUTONOMA
~~~

El sistema consulta acciones comerciales registradas.

No ejecuta autonomamente promociones, descuentos o retiros.

---

## 19. Seguridad

El nodo:

~~~text
validar_entrada
~~~

se ejecuta antes de:

- clasificacion;
- extraccion de contexto;
- MCP;
- consultas de negocio.

Ante un intento de prompt injection:

~~~text
BLOQUEADO: True
PROBLEMA: PROMPT_INJECTION
TOOLS: []
~~~

Por tanto, el flujo malicioso no alcanza las herramientas MCP.

---

## 20. Conclusion

App Deteccion Prod incorpora persistencia nativa de LangGraph mediante
`AsyncSqliteSaver`.

El estado del StateGraph ya no existe solamente durante la ejecucion
en memoria.

Cada ejecucion puede:

- identificarse mediante `thread_id`;
- persistirse en SQLite;
- recuperarse desde otro proceso Python;
- conservar un historial de checkpoints;
- mantener trazabilidad;
- seguir respetando las reglas de seguridad y negocio existentes.

La solucion mantiene separada la persistencia operacional del motor
BPMN de la persistencia interna de LangGraph, preservando una
arquitectura con responsabilidades claramente definidas.