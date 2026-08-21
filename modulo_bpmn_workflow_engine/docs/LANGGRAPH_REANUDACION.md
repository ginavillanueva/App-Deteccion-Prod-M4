# Pausa y Reanudacion de Workflows con LangGraph

## App Deteccion Prod

Este documento registra la implementacion de pausa y reanudacion
de workflows utilizando checkpoints persistentes de LangGraph.

---

## 1. Objetivo

El objetivo es permitir que una ejecucion pueda:

- detenerse antes de un nodo determinado;
- conservar el estado en SQLite;
- finalizar el proceso Python;
- recuperar el mismo thread posteriormente;
- continuar desde el nodo pendiente;
- evitar repetir los nodos ya ejecutados.

---

## 2. Persistencia utilizada

La reanudacion utiliza la capa implementada con:

- LangGraph;
- AsyncSqliteSaver;
- SQLite;
- configurable.thread_id.

Base utilizada:

```text
data/langgraph_checkpoints.sqlite
```

La base no se versiona en Git.

---

## 3. Runtime

Archivo principal:

```text
src/langgraph_orchestration/persistent_runtime.py
```

El runtime incorpora las siguientes operaciones.

### ejecutar_hasta_pausa

```python
await ejecutar_hasta_pausa(
    pregunta=pregunta,
    thread_id=thread_id,
    interrupt_before=[
        "consultar_detalle_mcp"
    ],
)
```

Permite ejecutar el workflow y detenerlo antes de un nodo.

---

### reanudar_persistente

```python
await reanudar_persistente(
    thread_id
)
```

Continua una ejecucion utilizando el checkpoint previamente
almacenado.

La reanudacion utiliza:

```python
await grafo.ainvoke(
    None,
    config=config,
)
```

No se crea nuevamente el estado inicial.

---

### obtener_checkpoint_persistido

```python
await obtener_checkpoint_persistido(
    thread_id
)
```

Permite recuperar:

- values;
- next;
- metadata.

---

### obtener_estado_ejecucion

```python
await obtener_estado_ejecucion(
    thread_id
)
```

Puede devolver:

```text
NO_EXISTE
PAUSADO
FINALIZADO
```

---

## 4. Prueba de pausa

Se utilizo:

```text
thread_id:
reanudacion-vencimiento-001
```

El workflow ejecuto:

```text
validar_entrada
        |
        v
clasificar_intencion
        |
        v
extraer_contexto
        |
        v
PAUSA
```

El checkpoint registro:

```text
NEXT: ('consultar_detalle_mcp',)

TOOLS: []

NODOS:
[
    'validar_entrada',
    'clasificar_intencion',
    'extraer_contexto'
]
```

Resultado:

```text
PAUSA PERSISTENTE CREADA: OK
```

Esto demuestra que el nodo MCP todavia no habia sido ejecutado.

---

## 5. Reanudacion desde otro proceso

Posteriormente se inicio otro proceso Python utilizando el mismo:

```text
thread_id:
reanudacion-vencimiento-001
```

Antes de reanudar:

```text
NEXT: ('consultar_detalle_mcp',)
TOOLS: []
```

Se ejecuto:

```python
await grafo.ainvoke(
    None,
    config=config,
)
```

Resultado:

```text
INTENCION: VENCIMIENTO
PRODUCTO: Yogur natural 1 litro
TIENDA: Sala 12

TOOLS:
[
    'consultar_detalle_producto'
]

NODOS:
[
    'validar_entrada',
    'clasificar_intencion',
    'extraer_contexto',
    'consultar_detalle_mcp'
]
```

Checkpoint final:

```text
NEXT: ()
TOTAL OBSERVACIONES: 1
```

Resultado:

```text
REANUDACION ENTRE PROCESOS: OK
```

---

## 6. Diferencia entre recuperacion y reanudacion

La recuperacion implementada previamente permite:

```text
checkpoint
    |
    v
aget_state()
    |
    v
leer estado
```

La reanudacion agrega:

```text
checkpoint pausado
       |
       v
ainvoke(None)
       |
       v
continuar nodo pendiente
       |
       v
FINALIZADO
```

Por tanto, recuperar un estado y continuar un workflow son
capacidades diferentes.

---

## 7. Regresion de reanudacion

Se probaron seis escenarios.

### VENCIMIENTO

Pausa:

```text
NEXT: ['consultar_detalle_mcp']
TOOLS: []
ESTADO: PAUSADO
```

Final:

```text
INTENCION: VENCIMIENTO
TOOLS: ['consultar_detalle_producto']
NEXT: []
ESTADO: FINALIZADO
RESULTADO: PASS
```

---

### CAMBIO_PRECIO

Pausa:

```text
NEXT: ['consultar_cambios_precio_mcp']
TOOLS: []
ESTADO: PAUSADO
```

Final:

```text
INTENCION: CAMBIO_PRECIO
TOOLS: ['consultar_cambios_precio']
NEXT: []
ESTADO: FINALIZADO
RESULTADO: PASS
```

El cambio de precio mantiene finalidad informativa y no representa
una aprobacion automatica.

---

### ACCION_COMERCIAL

Pausa:

```text
NEXT: ['consultar_acciones_comerciales_mcp']
TOOLS: []
ESTADO: PAUSADO
```

Final:

```text
INTENCION: ACCION_COMERCIAL
TOOLS: ['consultar_acciones_comerciales']
NEXT: []
ESTADO: FINALIZADO
RESULTADO: PASS
```

La accion comercial es consultada como registro y no es ejecutada
autonomamente por LangGraph.

---

## 8. Auditoria con pausa intermedia

Esta prueba verifica una reanudacion mas compleja.

Antes de la pausa ya se habia ejecutado:

```text
consultar_detalle_mcp
```

Estado:

```text
TOOLS:
[
    'consultar_detalle_producto'
]

NEXT:
[
    'consultar_cambios_precio_mcp'
]

ESTADO: PAUSADO
```

El flujo se encontraba en:

```text
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
PAUSA
        |
        v
consultar_cambios_precio_mcp
        |
        v
consultar_acciones_comerciales_mcp
```

Despues de reanudar:

```text
INTENCION: AUDITORIA_COMPLETA

TOOLS:
[
    'consultar_detalle_producto',
    'consultar_cambios_precio',
    'consultar_acciones_comerciales'
]

NEXT: []
ESTADO: FINALIZADO
RESULTADO: PASS
```

El nodo `consultar_detalle_mcp` no fue reiniciado desde cero.

---

## 9. Seguridad

Se verifico nuevamente un intento de prompt injection.

Resultado:

```text
BLOQUEADO: True
PROBLEMA: PROMPT_INJECTION
TOOLS: []
NODOS: ['validar_entrada']
NEXT: []
ESTADO: FINALIZADO
RESULTADO: PASS
```

El guardrail termina la ejecucion antes de alcanzar los nodos MCP.

La configuracion de pausa no debilita el mecanismo de seguridad.

---

## 10. Thread inexistente

Tambien se verifico un identificador que no posee checkpoints.

Resultado:

```text
ESTADO: NO_EXISTE
EXISTE: False
CHECKPOINT: {}
RESULTADO: PASS
```

Esto permite diferenciar claramente:

```text
NO_EXISTE
PAUSADO
FINALIZADO
```

---

## 11. Resultado final

La regresion obtuvo:

```text
APROBADOS: 6
TOTAL: 6

REGRESION REANUDACION 6/6: OK
```

---

## 12. Arquitectura

```text
Usuario / Aplicacion
        |
        v
ejecutar_hasta_pausa()
        |
        v
StateGraph
        |
        v
nodos iniciales
        |
        v
interrupt_before
        |
        v
PAUSADO
        |
        v
AsyncSqliteSaver
        |
        v
SQLite
        |
        v
checkpoint + thread_id


NUEVO PROCESO
        |
        v
thread_id
        |
        v
reanudar_persistente()
        |
        v
ainvoke(None)
        |
        v
nodo pendiente
        |
        v
MCP
        |
        v
FINALIZADO
```

---

## 13. Resultado tecnico

La implementacion demuestra:

- persistencia de estado;
- checkpoints SQLite;
- historial de checkpoints;
- pausa controlada;
- identificacion del nodo pendiente;
- recuperacion entre procesos;
- reanudacion entre procesos;
- continuacion sin reiniciar el workflow;
- pausa intermedia en auditorias;
- integracion MCP;
- proteccion mediante guardrails;
- deteccion de estados NO_EXISTE, PAUSADO y FINALIZADO.

---

## 14. Conclusion

App Deteccion Prod puede conservar una ejecucion incompleta y
continuarla posteriormente utilizando el mismo `thread_id`.

El workflow no necesita reiniciarse desde su primer nodo.

LangGraph recupera el checkpoint almacenado mediante
`AsyncSqliteSaver` y continua desde el nodo pendiente.

Esta capacidad permite implementar procesos de larga duracion,
interrupciones controladas, reanudacion posterior y mayor
trazabilidad del workflow.