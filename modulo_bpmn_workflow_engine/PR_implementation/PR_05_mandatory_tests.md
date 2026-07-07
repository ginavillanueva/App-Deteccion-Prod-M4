# PR-05 — Tests obligatorios completos

**Estado:** APROBADO / ENTREGA FINAL  
**Entrega:** 07  
**Feature:** Cobertura ejecutable de escenarios BPMN obligatorios  
**Proyecto:** App Detección Prod BPMN Workflow Engine

## 1. Objetivo

Implementar y documentar una suite de pruebas automatizadas que demuestre, de forma verificable, que el motor BPMN 2.0 aplicado a App Detección Prod soporta los escenarios exigidos por la consigna:

- flujo lineal;
- split paralelo;
- join AND;
- join OR;
- compuertas complejas y mocks REST/Lambda;
- ciclo/rework;
- múltiples finales;
- incidente con reset;
- reintentos con finalización en error;
- SLA/timeout;
- multi-asignación;
- ejecución concurrente.

## 2. Cambios implementados

### 2.1 Nuevo archivo de pruebas obligatorias

```text
tests/test_required_scenarios.py
```

Contiene 12 pruebas nuevas organizadas por escenario obligatorio.

### 2.2 Módulo de ejecución concurrente

```text
src/orchestration/executor.py
```

Se agregó para materializar el contrato `Executor/Future` solicitado por la consigna:

- `FutureLike`;
- `Executor`;
- `ImmediateFuture`;
- `SequentialExecutor`;
- `ThreadedExecutor`.

### 2.3 Export público

Se actualizó:

```text
src/orchestration/__init__.py
```

para exponer los nuevos contratos y adaptadores.

### 2.4 Documentación técnica

Se agregó:

```text
docs/README_TESTS.md
```

con cobertura, comandos de ejecución, resultado esperado y guía de defensa.

## 3. Resultado técnico

Comandos ejecutados:

```bash
python -m compileall src
python -m unittest discover -s tests
```

Resultado:

```text
Ran 28 tests
OK
```

## 4. Decisiones de diseño

| Decisión | Justificación |
|---|---|
| Usar `unittest` estándar | Evita dependencias externas y facilita ejecución por el docente. |
| Agregar `ThreadedExecutor` | Permite demostrar ejecución concurrente real con biblioteca estándar. |
| Mantener tests de negocio aplicados a App Detección Prod | Evita que el motor sea solamente genérico; valida el caso real del proyecto. |
| Separar pruebas obligatorias en un archivo dedicado | Facilita revisión docente y trazabilidad. |
| Probar happy path y errores | Aumenta defendibilidad: no solo se prueba que funciona, sino que falla correctamente. |

## 5. Trazabilidad FSD → Código → Tests

| Requisito FSD | Código | Test |
|---|---|---|
| Grafo lineal | `Workflow`, `Task.add_target` | `test_01_linear_flow_a_b_c_d_completes` |
| Paralelismo | `current_tasks`, múltiples targets | `test_02_parallel_split_creates_multiple_current_tasks` |
| Join AND | `LogicGate(GateType.AND)` | `test_03_join_and_waits_for_both_parallel_branches` |
| Join OR | `LogicGate(GateType.OR)` | `test_04_join_or_starts_after_one_completed_branch` |
| Lógica compleja/mock | `LogicGate.COMPLEX/SCRIPT/REST/LAMBDA` | `test_05_complex_script_rest_and_lambda_gates_are_mockable` |
| Rework | `raise_incident`, `ResetScope` | `test_06_cycle_rework_resets_downstream_and_restarts_iteration` |
| Múltiples finales | `Workflow.final_tasks` | `test_07_multiple_final_tasks_are_supported` |
| Reintentos/error | `retry_count`, `retries_exhausted`, `WorkflowStatus.ERROR` | `test_08_retry_exhaustion_finishes_workflow_in_error` |
| SLA | `assign_deadline`, `timed_out_tasks` | `test_09_sla_timeout_marks_ready_task_as_timed_out` |
| Multi-asignación | `CompletionPolicy.QUORUM` | `test_10_multi_assignment_quorum_policy` |
| Concurrencia | `ThreadedExecutor` | `test_11_concurrent_execution_completes_parallel_branches` |
| Recursos obligatorios | `ResourceSpec.mandatory` | `test_12_mandatory_resources_block_completion_when_missing` |

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Que el docente vea tests aislados sin relación con la consigna | Se creó `README_TESTS.md` con matriz de escenarios obligatorios. |
| Que la concurrencia parezca simulada | Se agregó `ThreadedExecutor` sobre `ThreadPoolExecutor`. |
| Que el flujo sea genérico y no del proyecto | Las pruebas principales usan `build_app_deteccion_workflow()`. |
| Que los errores no estén cubiertos | Se agregaron pruebas de recursos faltantes, timeout e incidentes con agotamiento. |

## 7. Conclusión del PR

El PR-05 deja el proyecto en un estado mucho más defendible: el motor ya no solo está documentado e implementado, sino que su comportamiento está probado frente a los escenarios obligatorios del curso y frente al flujo de negocio real de App Detección Prod.
