# PR_02_runtime_engine — Instancias runtime, traza, navegación e incidentes

**Proyecto:** App Detección Prod — Motor de Workflow BPMN 2.0  
**Estado:** APROBADO / ENTREGA FINAL  
**Relaciona:** Plan aprobado + PRD aprobado + FSD aprobado + PR_01_domain_model aprobado

## 1. Objetivo del PR

Implementar la capa runtime del motor BPMN. El objetivo de este PR es pasar del modelo de definición aprobado a una ejecución real del proceso, manteniendo la separación conceptual entre:

| Definición | Runtime |
|---|---|
| `Workflow` | `WorkflowInstance` |
| `Task` | `TaskInstance` |
| `ResourceSpec` | `ResourceInstance` |
| `Transition` | navegación e incidente aplicado |

## 2. Alcance funcional

Se implementan:

- `WorkflowInstance`;
- `TaskInstance`;
- `TraceEntry`;
- ciclo de vida runtime de tareas;
- navegación `FORWARD`;
- evaluación de compuertas embebidas;
- propagación de recursos;
- variables vivas del workflow;
- incidentes `BACKWARD`;
- reset `ALL_DOWNSTREAM` y `SPECIFIC`;
- reintentos por transición;
- cierre terminal `ERROR` cuando se supera `max_retries`;
- soporte inicial de SLA reactivo con `timed_out_tasks()`;
- soporte de multi-asignación mediante `CompletionPolicy`.

## 3. Decisiones de diseño

### 3.1 Separación definición/runtime

La definición del workflow no guarda estado mutable de ejecución. Cada ejecución crea una instancia independiente con sus propias tareas runtime. Esto replica el patrón de motores BPMN reales: definición del proceso versus instancia en ejecución.

### 3.2 `execution_path` como auditoría append-only

Cada avance, inicio, asignación, completado, incidente, reset y error terminal se registra como `TraceEntry`. Esto permite reconstruir el flujo completo del caso, incluyendo ciclos y reintentos.

### 3.3 Variables vivas del workflow

Además de los recursos adjuntos a cada tarea, `WorkflowInstance.variables` mantiene el contexto vivo: evidencia, fecha de vencimiento, precio, cantidad, acción comercial y aprobación. Esto permite que ramas paralelas reciban datos relevantes aunque no provengan directamente de la tarea inmediatamente anterior.

### 3.4 Incidentes como transición `BACKWARD`

`raise_incident()` valida que exista una transición de retorno desde la tarea origen hacia la tarea destino. Luego registra el incidente, incrementa el retry por transición y aplica reset.

### 3.5 Reset aguas abajo

Para `ALL_DOWNSTREAM`, se usa la matriz de dependencias aprobada para encontrar todas las tareas alcanzables por caminos `FORWARD` desde la tarea destino del retorno. Cada tarea reseteada vuelve a `PENDING`, marca `was_reset=true` y aumenta `reset_count`.

### 3.6 Reintentos por transición

El contador de retry vive en `TaskInstance.retry_count`, indexado por `transition.id`. Esto permite distinguir reintentos de distintas rutas backward, como `SupervisorReview → ValidateEvidence` y `ExecuteRetailAction → ValidateEvidence`.

### 3.7 SLA reactivo

La función `timed_out_tasks()` no usa cron. Revisa deadlines cuando el runtime/orquestador la invoca. Esta decisión prepara el próximo PR de orquestador, donde la revisión se activará por eventos.

## 4. Trazabilidad hacia FSD

| Requisito FSD | Código | Estado |
|---|---|---|
| Separar definición e instancia | `Workflow` / `WorkflowInstance`, `Task` / `TaskInstance` | Implementado |
| Máquina de estados de tarea | `TaskInstance.enqueue`, `assign_workers`, `start`, `complete`, `reset` | Implementado |
| Traza de ejecución | `TraceEntry`, `WorkflowInstance.execution_path` | Implementado |
| Recursos runtime | `ResourceInstance`, propagación y variables | Implementado |
| Join embebido en tarea destino | `WorkflowInstance.can_start_task()` | Implementado |
| Navegación por grafo | `navigate_to_targets()` | Implementado |
| Incidente con glosa | `raise_incident()` + `Incident` | Implementado |
| Reset aguas abajo/específico | `_resolve_reset_task_ids()` + `TaskInstance.reset()` | Implementado |
| Reintentos y fin en error | `retry_for()` + `WorkflowStatus.ERROR` | Implementado |
| Multi-asignación | `CompletionPolicy.ALL/ANY/QUORUM` | Implementado |
| SLA sin cron | `timed_out_tasks()` | Implementado inicial |

## 5. Pruebas incluidas

```text
tests/test_runtime_engine.py
```

Casos validados:

1. inicio del workflow y navegación a validación;
2. propagación de recursos;
3. join `AND` entre clasificación de riesgo y validación de precio;
4. incidente por error de precio con reset;
5. reintentos agotados con estado terminal `ERROR`;
6. multi-asignación con política `ANY`;
7. recursos runtime manuales.

## 6. Validación técnica

Comandos ejecutados:

```bash
python -m compileall src
python -m unittest discover -s tests
```

Resultado:

```text
Ran 9 tests
OK
```

## 7. Impacto en App Detección Prod

El runtime ya permite demostrar ante el docente que App Detección Prod no es solo un flujo documentado, sino un motor ejecutable que puede:

- abrir un caso de producto próximo a vencer;
- validar evidencia;
- dividir el flujo en ramas paralelas;
- unir ramas mediante compuerta `AND`;
- aprobar cambio de precio;
- registrar ejecución;
- devolver por incidente;
- resetear tareas;
- cortar el proceso en error si se exceden reintentos;
- dejar evidencia completa en la traza.

## 8. Próximo PR

El siguiente entregable será `PR_03_orchestrator_queue.md` y el código de `src/orchestration/`, donde se implementará:

- cola de tareas listas con `collections.deque`;
- patrón Observer;
- asignación skill-based + least-loaded;
- eventos `onReady`, `onAssign`, `onComplete`, `onIncident`, `onRetryExhausted`, `onSlaBreach`.
