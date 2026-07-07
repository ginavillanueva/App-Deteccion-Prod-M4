# README — Runtime Engine del Motor BPMN

**Proyecto:** App Detección Prod — Motor de Workflow BPMN 2.0  
**Entrega:** 04  
**Estado:** APROBADO / ENTREGA FINAL  
**Base aprobada:** Plan + PRD + FSD + Modelo de dominio Python

## 1. Propósito

Este entregable implementa la capa de ejecución del motor de workflow. La entrega anterior definía la plantilla del proceso (`Workflow`, `Task`, `Transition`, `LogicGate`, `ResourceSpec`, `Worker`). Esta entrega crea la instancia real de ejecución mediante:

- `WorkflowInstance`;
- `TaskInstance`;
- `TraceEntry`;
- navegación `FORWARD`;
- incidentes `BACKWARD`;
- reset de tareas;
- reintentos por transición;
- cierre en `ERROR` cuando se agotan los reintentos;
- validación de recursos obligatorios;
- propagación de recursos hacia tareas destino;
- evaluación de compuertas embebidas;
- soporte inicial de SLA mediante chequeo reactivo.

## 2. Archivos principales

```text
src/runtime/
├── __init__.py
├── instances.py
└── trace.py
```

## 3. Clases implementadas

### 3.1 `TaskInstance`

Representa el estado runtime de una tarea definida en `Task`.

Responsabilidades:

- pasar por estados `PENDING → READY → ASSIGNED → IN_PROGRESS → COMPLETED`;
- asignar uno o varios workers;
- validar recursos obligatorios antes de completar;
- materializar recursos producidos por la tarea;
- aplicar `completionPolicy` (`ALL`, `ANY`, `QUORUM`);
- guardar contadores de retry por transición `BACKWARD`;
- registrar si fue reiniciada por incidente mediante `was_reset` y `reset_count`.

### 3.2 `WorkflowInstance`

Representa una ejecución concreta del workflow.

Responsabilidades:

- crear una `TaskInstance` por cada `Task` de la definición;
- iniciar el proceso desde `start_task`;
- evaluar si una tarea puede iniciar según sus predecesoras y `LogicGate`;
- completar tareas y navegar hacia `targets`;
- propagar recursos entre tareas;
- almacenar variables vivas del proceso;
- levantar incidentes `BACKWARD` con glosa obligatoria;
- resetear tareas aguas abajo o específicas;
- controlar reintentos por transición;
- pasar el workflow a `ERROR` si se excede `max_retries`;
- registrar todo en `execution_path`.

### 3.3 `TraceEntry`

Es una entrada append-only de auditoría. Guarda:

- `task_id`;
- `status`;
- `message`;
- `iteration`;
- `worker_id`;
- `incident_id`;
- `was_reset`;
- `timestamp`.

Esta estructura permite reconstruir el flujo completo incluso cuando una tarea se visita más de una vez por un ciclo de rework.

## 4. Cómo se aplica a App Detección Prod

El runtime permite ejecutar el flujo:

```text
DetectProductCase
→ ValidateEvidence
→ {ClassifyRisk, ValidatePriceData}
→ DecideCommercialAction
→ ApprovePriceChange
→ ExecuteRetailAction
→ SupervisorReview
→ CloseCaseAndUpdateDashboard
```

Casos aplicados:

| Situación de negocio | Implementación runtime |
|---|---|
| Mercaderista registra producto próximo a vencer | `detect_product_case` se completa y produce evidencia, vencimiento, precio y cantidad |
| Supervisor valida evidencia | `validate_evidence` consume foto/vencimiento y produce `evidence_valid` |
| IA clasifica riesgo | `classify_risk` puede ejecutarse como tarea de servicio sin worker humano |
| Vendedor valida precio | `validate_price_data` valida `current_price` |
| Decisión comercial espera dos ramas | `decide_commercial_action` usa join `AND` |
| Gerencia aprueba cambio de precio | `approve_price_change` produce `price_approved=true` |
| Error de precio o evidencia | `raise_incident()` aplica transición `BACKWARD` |
| Reintentos agotados | `WorkflowInstance.status = ERROR` |
| Auditoría del caso | `execution_path` registra cada avance, reset e incidente |

## 5. Tests incluidos

Archivo principal:

```text
tests/test_runtime_engine.py
```

Pruebas cubiertas:

1. inicio del workflow y navegación `FORWARD`;
2. propagación de recursos hacia la validación;
3. join `AND` esperando dos ramas paralelas;
4. incidente `BACKWARD` con reset aguas abajo;
5. reintentos agotados con cierre en `ERROR`;
6. multi-asignación con `CompletionPolicy.ANY`;
7. incorporación manual de recurso runtime.

## 6. Cómo probar

Desde la raíz del paquete:

```bash
python -m compileall src
python -m unittest discover -s tests
```

Resultado validado:

```text
Ran 9 tests in ...s
OK
```

## 7. Qué queda para la siguiente entrega

La siguiente entrega debe implementar el **orquestador + cola**, usando `collections.deque` y patrón Observer. Esa capa será la responsable de consumir tareas `READY`, asignar workers por especialidad y balancear carga.
