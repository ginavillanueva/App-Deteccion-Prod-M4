# PR_03 — Orquestador + Cola Observer

**Proyecto:** App Detección Prod — Motor de Workflow BPMN 2.0  
**Estado:** APROBADO / ENTREGA FINAL  
**Entrega:** 05  
**Tipo:** Feature técnica / orquestación

## 1. Objetivo del PR

Implementar la capa de orquestación del motor BPMN, responsable de:

- encolar tareas `READY`;
- notificar eventos mediante patrón Observer;
- asignar workers por especialidad y carga;
- iniciar y completar tareas usando el runtime aprobado;
- reencolar automáticamente tareas destino después de una navegación `FORWARD`;
- preparar el mecanismo de SLA reactivo sin uso de cron.

## 2. Contexto funcional

En App Detección Prod, un caso de producto próximo a vencer atraviesa varios roles:

1. Mercaderista detecta el producto.
2. Supervisor valida evidencia.
3. IA clasifica riesgo.
4. Vendedor define acción comercial.
5. Gerencia aprueba cambio de precio cuando aplica.
6. Mercaderista ejecuta acción en sala.
7. Supervisor revisa y cierra.
8. Dashboard se actualiza.

La capa de runtime ya podía representar ese flujo. Este PR agrega la capacidad de **operarlo** mediante cola y asignación balanceada.

## 3. Archivos modificados/agregados

```text
src/orchestration/
├── __init__.py
├── assignment.py
├── events.py
├── orchestrator.py
└── queue.py

tests/test_orchestration.py

docs/README_ORCHESTRATION.md
PR_implementation/PR_03_orchestrator_queue.md
docs/TRAZABILIDAD_ENTREGA_05.md
```

## 4. Decisiones de diseño

### 4.1 ReadyQueue con `collections.deque`

Se implementa una cola FIFO en memoria para mantener el foco académico en el algoritmo. La cola es explícita, auditable y desacoplada del runtime.

**Trade-off:**

- Ventaja: simple, rápida y fácil de probar.
- Desventaja: no sobrevive reinicios todavía.
- Mitigación: la siguiente entrega implementará persistencia SQLite.

### 4.2 Observer explícito

`ReadyQueue` acepta observers y emite `OrchestrationEvent`. El `Orchestrator` se suscribe a la cola. Esto evita acoplar la cola a un framework externo y permite explicar claramente el patrón solicitado.

### 4.3 Asignación por especialidad y menor carga

`WorkerPool.select_worker()` filtra por `required_worker_type`, respeta `capacity` y selecciona el worker menos cargado.

**Justificación:** es la política recomendada para el MVP porque se entiende, se prueba y se defiende mejor ante evaluación docente.

### 4.4 Separación runtime/orquestación

El runtime continúa controlando estados, traza, recursos, incidentes y navegación. El orquestador solo reacciona a eventos, decide asignación y mueve tareas por métodos públicos del runtime.

## 5. Eventos implementados

| Evento | Emisor | Significado |
|---|---|---|
| `task_ready` | `ReadyQueue` | Una tarea entró a cola de listos |
| `workflow_submitted` | `Orchestrator` | Una instancia fue enviada al orquestador |
| `task_assigned` | `Orchestrator` | Una tarea fue asignada a un worker |
| `task_started` | `Orchestrator` | Una tarea pasó a `IN_PROGRESS` |
| `task_completed` | `Orchestrator` | Una tarea finalizó correctamente |
| `task_partially_completed` | `Orchestrator` | Una tarea multi-asignada recibió una finalización parcial |
| `sla_breached` | `Orchestrator` | Una tarea superó deadline de asignación/completado |
| `task_skipped_not_ready` | `Orchestrator` | Elemento de cola descartado por estado no válido |

## 6. Validación técnica

Comandos ejecutados:

```bash
python -m compileall src
python -m unittest discover -s tests
```

Resultado:

```text
Ran 13 tests in ...s
OK
```

## 7. Tests agregados

| Test | Propósito |
|---|---|
| `test_ready_queue_notifies_observers` | Verifica evento `task_ready` |
| `test_orchestrator_assigns_ready_task_by_skill_and_load` | Verifica asignación por especialidad |
| `test_orchestrator_completes_task_and_enqueues_forward_target` | Verifica navegación y reencolado posterior |
| `test_worker_pool_uses_least_loaded_candidate` | Verifica balanceo least-loaded |

## 8. Trazabilidad hacia FSD

| Requerimiento FSD | Implementación |
|---|---|
| Cola de tareas listas | `ReadyQueue` |
| Orquestador Observer | `Orchestrator` + `OrchestrationObserver` |
| Worker pool | `WorkerPool` |
| Asignación balanceada | `select_worker()` |
| No cron | `check_sla()` reactivo, no scheduler temporal |
| Auditoría | `OrchestrationEvent` + `execution_path` runtime |
| Integración con flujo App Detección Prod | worker types: `MERCHANDISER`, `SUPERVISOR`, `SELLER`, `MANAGER`, `SYSTEM_AI` |

## 9. Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Cola en memoria no persistente | Pérdida de tareas tras reinicio | Entrega 06: SQLite |
| Worker sin capacidad disponible | Tarea queda sin asignar | Excepción explícita y evento futuro de escalamiento |
| Duplicidad de tareas en cola | Asignación repetida | `_known` evita duplicados |
| Mezclar runtime con orquestación | Código difícil de probar | Runtime conserva estado; orquestador solo coordina |

## 10. Definition of Done

- [x] Cola FIFO implementada con `deque`.
- [x] Observer implementado con eventos tipados.
- [x] Orquestador suscrito a la cola.
- [x] WorkerPool con skill-based + least-loaded.
- [x] Reencolado de targets `FORWARD`.
- [x] Pruebas unitarias agregadas.
- [x] `compileall` exitoso.
- [x] `unittest` exitoso.
- [x] Documentación y trazabilidad actualizadas.
