# README — Tests obligatorios completos

**Proyecto:** App Detección Prod BPMN Workflow Engine  
**Entrega:** 07 — Tests obligatorios completos  
**Estado:** APROBADO / ENTREGA FINAL  
**Curso:** Fundamentos de Programación y Frameworks Modernos para IA

## 1. Propósito del entregable

Este entregable valida que el motor de workflow BPMN 2.0 implementado para **App Detección Prod** cubre los escenarios funcionales exigidos por la consigna y que cada componente aprobado hasta la fecha conserva comportamiento correcto al integrarse:

- modelo de dominio;
- runtime engine;
- orquestador Observer + cola;
- persistencia SQLite;
- compuertas lógicas;
- recursos obligatorios;
- incidentes, reset y reintentos;
- SLA/timeout;
- multi-asignación;
- ejecución concurrente mediante contrato `Executor/Future`.

## 2. Comando de ejecución

Desde la raíz del paquete:

```bash
python -m compileall src
python -m unittest discover -s tests
```

Resultado validado:

```text
Ran 28 tests
OK
```

## 3. Cobertura de escenarios obligatorios

| Escenario exigido | Test principal | Evidencia |
|---|---|---|
| Flujo lineal `A → B → C → D` | `test_01_linear_flow_a_b_c_d_completes` | Workflow termina en `COMPLETED` |
| Split paralelo `A → {B, C}` | `test_02_parallel_split_creates_multiple_current_tasks` | Dos tareas quedan `READY` en paralelo |
| Join AND `{B, C} → D` | `test_03_join_and_waits_for_both_parallel_branches` | D espera ambas ramas |
| Join OR | `test_04_join_or_starts_after_one_completed_branch` | D inicia con una rama completada |
| Join complejo / REST / Lambda mock | `test_05_complex_script_rest_and_lambda_gates_are_mockable` | Gate `COMPLEX`, `SCRIPT`, `REST`, `LAMBDA` evaluados |
| Ciclo / rework | `test_06_cycle_rework_resets_downstream_and_restarts_iteration` | Incidente incrementa iteración y resetea flujo |
| Múltiples finales | `test_07_multiple_final_tasks_are_supported` | Workflow acepta más de una `finalTask` |
| Retorno por incidente con reset | `test_06_cycle_rework_resets_downstream_and_restarts_iteration` + `test_backward_incident_resets_downstream_and_records_trace` | `was_reset=true`, traza con `incident_id` |
| Reintentos con fin en error | `test_08_retry_exhaustion_finishes_workflow_in_error` | Estado final `WorkflowStatus.ERROR` |
| SLA / timeout | `test_09_sla_timeout_marks_ready_task_as_timed_out` | Tarea pasa a `TIMED_OUT` |
| Multi-asignación | `test_10_multi_assignment_quorum_policy` + `test_multi_assignment_any_policy` | Políticas `QUORUM` y `ANY` |
| Ejecución concurrente | `test_11_concurrent_execution_completes_parallel_branches` | Dos ramas completadas con `ThreadedExecutor` |
| Recursos obligatorios | `test_12_mandatory_resources_block_completion_when_missing` | Bloquea cierre sin recurso obligatorio |
| Persistencia | `test_persistence_sqlite.py` | Snapshots guardados/recuperados |
| Orquestador | `test_orchestration.py` | Cola, eventos y asignación balanceada |

## 4. Decisión técnica agregada: contrato Executor/Future

Para evidenciar el requisito de ejecución concurrente, se agregó el módulo:

```text
src/orchestration/executor.py
```

Incluye:

- `FutureLike`: contrato mínimo de futuro (`result`, `cancel`, `done`);
- `Executor`: contrato de ejecución (`submit`);
- `SequentialExecutor`: ejecución determinística local;
- `ThreadedExecutor`: adaptador sobre `concurrent.futures.ThreadPoolExecutor`.

Esta decisión mantiene el proyecto sin dependencias externas y permite defender que el motor puede ejecutar tareas paralelas con una interfaz extensible hacia `threading`, `asyncio` u otro backend futuro.

## 5. Relación con App Detección Prod

Los tests no son genéricos únicamente: también validan el flujo de negocio principal de App Detección Prod:

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

Esto asegura que la implementación no queda como motor abstracto desconectado del proyecto, sino como una solución programable para gestionar productos próximos a vencer, control de precios, acciones comerciales, evidencia, supervisión, rework, SLA y cierre trazable.

## 6. Cómo defender este entregable ante el docente

Puede explicarse así:

> Este entregable convierte los requisitos del FSD en evidencia ejecutable. Cada escenario obligatorio de la consigna tiene al menos una prueba automatizada. La suite no solo prueba el happy path, sino también joins, condiciones, errores, recursos obligatorios, incidentes, reintentos, timeouts, multi-asignación y concurrencia. Por eso la evaluación no depende de una explicación verbal: el comportamiento está verificable con `unittest`.

## 7. Criterio de aprobación

Este entregable queda listo para aprobar si:

- el docente puede ejecutar `python -m unittest discover -s tests`;
- todos los tests pasan;
- se entiende qué escenario cubre cada test;
- la matriz de trazabilidad enlaza consigna → FSD → implementación → test.
