# Trazabilidad — Entrega 05 Orquestador + Cola Observer

> **Nota de lectura final:** este archivo es histórico y conserva el estado del paquete en el momento de esa entrega parcial. El estado final aprobado se verifica en `00_CONTROL_APROBACIONES.md`, `docs/TRAZABILIDAD_FINAL.md` y `docs/AUDITORIA_FINAL_ZIP.md`.


**Proyecto:** App Detección Prod — Motor de Workflow BPMN 2.0  
**Entrega:** 05  
**Estado del nuevo entregable:** PARA REVISIÓN

## 1. Cadena de aprobaciones

| Orden | Entregable | Estado | Evidencia |
|---:|---|---|---|
| 0 | Plan maestro de ejecución | APROBADO | `00_PLAN_EJECUCION_APROBADO.md` |
| 1 | PRD ligero | APROBADO | `docs/PRD.md` |
| 2 | FSD ligero | APROBADO | `docs/FSD.md` |
| 3 | Modelo de dominio Python | APROBADO | `src/domain/`, `docs/README_DOMAIN_MODEL.md`, `PR_implementation/PR_01_domain_model.md` |
| 4 | Runtime engine | APROBADO | `src/runtime/`, `docs/README_RUNTIME_ENGINE.md`, `PR_implementation/PR_02_runtime_engine.md` |
| 5 | Orquestador + cola Observer | PARA REVISIÓN | `src/orchestration/`, `docs/README_ORCHESTRATION.md`, `PR_implementation/PR_03_orchestrator_queue.md` |

## 2. Trazabilidad negocio → orquestación

| Dolor de negocio App Detección Prod | Necesidad funcional | Implementación Entrega 05 |
|---|---|---|
| Información dispersa por WhatsApp | Centralizar el trabajo pendiente | `ReadyQueue` |
| Validación manual lenta | Enrutar tareas al rol correcto | `WorkerPool.select_worker()` |
| Supervisor pierde tiempo buscando información | Asignar y auditar tareas de validación | eventos `task_ready`, `task_assigned` |
| Vendedor toma decisiones sin claridad | Tareas comerciales visibles y asignadas | worker type `SELLER` |
| Gerencia necesita aprobar precios críticos | Tareas de aprobación direccionadas | worker type `MANAGER` |
| Falta de trazabilidad operativa | Eventos auditables y runtime trace | `OrchestrationEvent` + `execution_path` |
| Dependencia de revisión manual o cron | Reacción por eventos | `Orchestrator` como Observer |

## 3. Trazabilidad FSD → código

| FSD | Código Entrega 05 | Validación |
|---|---|---|
| Cola de tareas listas | `src/orchestration/queue.py` | `test_ready_queue_notifies_observers` |
| Observer | `src/orchestration/events.py` | `InMemoryEventLog` |
| Orquestador | `src/orchestration/orchestrator.py` | `test_orchestrator_assigns_ready_task_by_skill_and_load` |
| Asignación balanceada | `src/orchestration/assignment.py` | `test_worker_pool_uses_least_loaded_candidate` |
| Navegación posterior a completar | `complete_task()` + `enqueue_current_ready_tasks()` | `test_orchestrator_completes_task_and_enqueues_forward_target` |
| SLA reactivo | `check_sla()` | preparado para pruebas de SLA completas |

## 4. Trazabilidad PR implementation

| PR | Estado | Descripción |
|---|---|---|
| `PR_01_domain_model.md` | APROBADO | Modelo de dominio base |
| `PR_02_runtime_engine.md` | APROBADO | Runtime de ejecución, traza, navegación, incidentes |
| `PR_03_orchestrator_queue.md` | PARA REVISIÓN | Cola, Observer, worker pool y orquestador |

## 5. Evidencia técnica

Comandos ejecutados:

```bash
python -m compileall src
python -m unittest discover -s tests
```

Resultado:

```text
Ran 13 tests in 0.009s
OK
```

## 6. Archivos nuevos de la entrega

```text
src/orchestration/events.py
src/orchestration/queue.py
src/orchestration/assignment.py
src/orchestration/orchestrator.py
src/orchestration/__init__.py
tests/test_orchestration.py
docs/README_ORCHESTRATION.md
PR_implementation/PR_03_orchestrator_queue.md
docs/TRAZABILIDAD_ENTREGA_05.md
```

## 7. Próxima aprobación esperada

Para aprobar este entregable, responder:

```text
aprobado orquestador
```

Luego se generará el **Entregable 06: Persistencia SQLite**.
