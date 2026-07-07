# Trazabilidad — Entrega 07: Tests obligatorios completos

> **Nota de lectura final:** este archivo es histórico y conserva el estado del paquete en el momento de esa entrega parcial. El estado final aprobado se verifica en `00_CONTROL_APROBACIONES.md`, `docs/TRAZABILIDAD_FINAL.md` y `docs/AUDITORIA_FINAL_ZIP.md`.


**Proyecto:** App Detección Prod BPMN Workflow Engine  
**Estado:** Plan + PRD + FSD + Dominio + Runtime + Orquestador + Persistencia aprobados; Tests para revisión.

## 1. Cadena de trazabilidad acumulada

| Nivel | Artefacto | Estado | Evidencia |
|---|---|---|---|
| Plan | `00_PLAN_EJECUCION_APROBADO.md` | APROBADO | Define ruta incremental y entregables acumulados |
| Producto | `docs/PRD.md` | APROBADO | Define objetivo, usuarios y valor del workflow aplicado a App Detección Prod |
| Funcional | `docs/FSD.md` | APROBADO | Define modelo, runtime, compuertas, recursos, SLA, incidentes y comparación Camunda/Activiti |
| Código dominio | `src/domain/` | APROBADO | Define `Workflow`, `Task`, `LogicGate`, `Transition`, `Resource`, `Worker` |
| Código runtime | `src/runtime/` | APROBADO | Define `WorkflowInstance`, `TaskInstance`, traza, navegación, reset y reintentos |
| Código orquestación | `src/orchestration/` | APROBADO | Define cola, Observer, asignación y eventos |
| Persistencia | `src/persistence/` | APROBADO | Define repositorio SQLite y snapshots |
| Pruebas | `tests/` | PARA REVISIÓN | Valida escenarios obligatorios y comportamiento integrado |

## 2. Requisitos de la consigna cubiertos por esta entrega

| Requisito/escenario | Evidencia de prueba | Resultado esperado |
|---|---|---|
| Flujo lineal | `test_01_linear_flow_a_b_c_d_completes` | `WorkflowStatus.COMPLETED` |
| Split paralelo | `test_02_parallel_split_creates_multiple_current_tasks` | Dos tareas `READY` simultáneas |
| Join AND | `test_03_join_and_waits_for_both_parallel_branches` | Espera ambas ramas |
| Join OR | `test_04_join_or_starts_after_one_completed_branch` | Avanza con una rama completa |
| Lógica compleja/REST/Lambda mock | `test_05_complex_script_rest_and_lambda_gates_are_mockable` | Gates retornan decisión controlada |
| Ciclos/rework | `test_06_cycle_rework_resets_downstream_and_restarts_iteration` | Iteración incrementa y tareas se resetean |
| Múltiples finales | `test_07_multiple_final_tasks_are_supported` | Una finalTask cierra el workflow |
| Retorno por incidente con reset | `test_06...` + runtime tests existentes | `was_reset=true` y traza con incidente |
| Reintentos con fin en error | `test_08_retry_exhaustion_finishes_workflow_in_error` | `WorkflowStatus.ERROR` |
| SLA/timeout | `test_09_sla_timeout_marks_ready_task_as_timed_out` | `TaskStatus.TIMED_OUT` |
| Multi-asignación | `test_10_multi_assignment_quorum_policy` | Quorum completa la tarea |
| Ejecución concurrente | `test_11_concurrent_execution_completes_parallel_branches` | `ThreadedExecutor` completa ramas paralelas |
| Recursos obligatorios | `test_12_mandatory_resources_block_completion_when_missing` | Error controlado si falta recurso obligatorio |

## 3. Evidencia de ejecución

```bash
python -m compileall src
python -m unittest discover -s tests
```

```text
Ran 28 tests
OK
```

## 4. Matriz PR implementation

| PR | Archivo | Estado |
|---|---|---|
| PR-01 | `PR_implementation/PR_01_domain_model.md` | APROBADO |
| PR-02 | `PR_implementation/PR_02_runtime_engine.md` | APROBADO |
| PR-03 | `PR_implementation/PR_03_orchestrator_queue.md` | APROBADO |
| PR-04 | `PR_implementation/PR_04_persistence_sqlite.md` | APROBADO |
| PR-05 | `PR_implementation/PR_05_mandatory_tests.md` | PARA REVISIÓN |

## 5. Lectura para el docente

Esta entrega demuestra que la implementación no depende únicamente de explicación documental. El comportamiento requerido por la consigna está automatizado y puede ejecutarse localmente con biblioteca estándar de Python. La suite valida tanto el motor como el flujo aplicado a App Detección Prod.
