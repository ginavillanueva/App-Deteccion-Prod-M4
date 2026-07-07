# Trazabilidad — Entrega 06 Persistencia SQLite

> **Nota de lectura final:** este archivo es histórico y conserva el estado del paquete en el momento de esa entrega parcial. El estado final aprobado se verifica en `00_CONTROL_APROBACIONES.md`, `docs/TRAZABILIDAD_FINAL.md` y `docs/AUDITORIA_FINAL_ZIP.md`.


**Proyecto:** App Detección Prod — Motor de Workflow BPMN 2.0  
**Entrega:** 06  
**Estado del nuevo entregable:** PARA REVISIÓN

## 1. Cadena de aprobaciones

| Orden | Entregable | Estado | Evidencia |
|---:|---|---|---|
| 0 | Plan maestro de ejecución | APROBADO | `00_PLAN_EJECUCION_APROBADO.md` |
| 1 | PRD ligero | APROBADO | `docs/PRD.md` |
| 2 | FSD ligero | APROBADO | `docs/FSD.md` |
| 3 | Modelo de dominio Python | APROBADO | `src/domain/`, `docs/README_DOMAIN_MODEL.md`, `PR_implementation/PR_01_domain_model.md` |
| 4 | Runtime engine | APROBADO | `src/runtime/`, `docs/README_RUNTIME_ENGINE.md`, `PR_implementation/PR_02_runtime_engine.md` |
| 5 | Orquestador + cola Observer | APROBADO | `src/orchestration/`, `docs/README_ORCHESTRATION.md`, `PR_implementation/PR_03_orchestrator_queue.md` |
| 6 | Persistencia SQLite | PARA REVISIÓN | `src/persistence/`, `docs/README_PERSISTENCE.md`, `PR_implementation/PR_04_persistence_sqlite.md` |

## 2. Trazabilidad negocio → persistencia

| Dolor de negocio App Detección Prod | Necesidad funcional | Implementación Entrega 06 |
|---|---|---|
| Reportes dispersos por WhatsApp/Excel | Guardar información en un repositorio estructurado | SQLite con tablas normalizadas |
| Falta de trazabilidad | Persistir la ejecución completa | `trace_entries` |
| No se controla cambio de precio | Guardar recursos y variables del caso | `task_instances.resources_json`, `variables_json` |
| Acciones comerciales no medibles | Persistir estado de cada tarea | `task_instances` |
| Incidentes sin historial | Guardar glosa, origen, destino y reset | `incidents` |
| Gerencia necesita evidencias | Recuperar snapshot auditable | `load_workflow_instance_snapshot()` |
| Docente debe revisar consistencia | Conectar FSD, código y pruebas | `PR_04_persistence_sqlite.md` + tests |

## 3. Trazabilidad FSD → código

| FSD | Código Entrega 06 | Validación |
|---|---|---|
| Elección de persistencia justificada | `SQLiteWorkflowRepository` | `docs/README_PERSISTENCE.md` |
| Persistir `Workflow` | `save_workflow_definition()` | `test_save_workflow_definition_payload` |
| Persistir `WorkflowInstance` | `save_workflow_instance()` | `test_save_runtime_snapshot_with_trace_and_task_state` |
| Persistir `TaskInstance` | tabla `task_instances` | snapshot de tarea completada |
| Persistir `TraceEntry` | tabla `trace_entries` | recuento y recuperación de traza |
| Persistir `Incident` | tabla `incidents` | `test_save_snapshot_after_rework_incident` |
| Persistir `Worker` | tabla `workers` | `save_worker()` + `count_rows()` |

## 4. Trazabilidad PR implementation

| PR | Estado | Descripción |
|---|---|---|
| `PR_01_domain_model.md` | APROBADO | Modelo de dominio base |
| `PR_02_runtime_engine.md` | APROBADO | Runtime de ejecución, traza, navegación, incidentes |
| `PR_03_orchestrator_queue.md` | APROBADO | Cola, Observer, worker pool y orquestador |
| `PR_04_persistence_sqlite.md` | PARA REVISIÓN | Persistencia durable SQLite |

## 5. Evidencia técnica

Comandos ejecutados:

```bash
python -m compileall src
python -m unittest discover -s tests
```

Resultado:

```text
Ran 16 tests in 0.042s
OK
```

## 6. Archivos nuevos de la entrega

```text
src/persistence/__init__.py
src/persistence/sqlite_repository.py
tests/test_persistence_sqlite.py
docs/README_PERSISTENCE.md
PR_implementation/PR_04_persistence_sqlite.md
docs/TRAZABILIDAD_ENTREGA_06.md
```

## 7. Próxima aprobación esperada

Para aprobar este entregable, responder:

```text
aprobado persistencia
```

Luego se generará el **Entregable 07: Tests obligatorios completos**.
