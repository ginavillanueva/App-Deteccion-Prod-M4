# PR_01_domain_model — Modelo de dominio del motor BPMN

**Proyecto:** App Detección Prod — Motor de Workflow BPMN 2.0  
**Estado:** APROBADO  
**Relaciona:** PRD aprobado + FSD aprobado  

## 1. Objetivo del PR

Implementar el primer bloque de código del motor: el modelo de dominio en Python. Este PR no ejecuta aún el workflow completo; define la estructura semántica que permitirá construir el runtime en la siguiente entrega.

## 2. Alcance funcional

Se implementan:

- enumeraciones de estados y tipos;
- recursos requeridos/producidos;
- trabajadores y especialidades;
- tareas como nodos del grafo;
- transiciones `FORWARD` y `BACKWARD`;
- incidentes con glosa obligatoria;
- compuertas embebidas `AND`, `OR`, `XOR`, `COMPLEX`, `SCRIPT`, `REST`, `LAMBDA`;
- matriz de dependencias;
- factory del workflow de referencia App Detección Prod.

## 3. Decisiones de diseño

### 3.1 `Task` como nodo de grafo

Cada tarea representa un nodo del flujo de negocio. Los caminos hacia adelante se modelan mediante `targets` y `incoming`. Esto permite mantener doble navegación y preparar validaciones de alcanzabilidad.

### 3.2 `LogicGate` embebida en la tarea destino

Se implementa la compuerta como atributo de `Task`, no como nodo independiente. Esto respeta la decisión didáctica del curso y simplifica la traducción del BPMN hacia teoría de grafos.

### 3.3 `TransitionType.BACKWARD` para incidentes

Los retornos por evidencia inválida, error de precio o ejecución comercial incorrecta no se mezclan con el avance normal. Se modelan como `BACKWARD` y exigen `max_retries`.

### 3.4 Recursos como contrato entre tareas

`ResourceSpec` expresa qué información requiere o produce cada tarea. En App Detección Prod se usa para evidencia, vencimiento, precio actual, precio propuesto, cantidad, acción comercial y aprobación.

### 3.5 Factory de referencia

`build_app_deteccion_workflow()` crea el workflow base del proyecto para que el docente pueda ver que el modelo no es genérico aislado, sino aplicado al caso de negocio.

## 4. Trazabilidad hacia FSD

| FSD | Código | Resultado |
|---|---|---|
| Modelo de dominio en inglés | `src/domain/*.py` | Implementado |
| Workflow como grafo dirigido | `Workflow`, `Task`, `DependencyMatrix` | Implementado |
| Compuertas embebidas | `LogicGate` en `Task` | Implementado |
| Recursos de entrada/salida | `ResourceSpec`, `ResourceInstance` | Implementado |
| Worker por especialidad | `Worker`, `WorkerType` | Implementado |
| Retorno por incidente | `Transition`, `Incident` | Implementado |
| Ciclo/rework | Factory con `BACKWARD` | Implementado |
| Validaciones iniciales | `validate()` | Implementado |

## 5. Validación técnica

Comandos:

```bash
python -m compileall src
python -m unittest discover -s tests
```

Resultado esperado:

- todos los módulos compilan;
- el workflow de referencia se construye correctamente;
- la matriz de dependencias detecta la ruta desde inicio hasta cierre;
- las transiciones backward exigen `max_retries`;
- la compuerta AND permite avanzar solo cuando las dependencias están completadas.

## 6. Próximo PR

El siguiente entregable será `PR_02_runtime_engine.md` y el código de `src/runtime/`, donde se implementarán `WorkflowInstance`, `TaskInstance`, traza, estados runtime, incidentes aplicados, reset y navegación real del proceso.
