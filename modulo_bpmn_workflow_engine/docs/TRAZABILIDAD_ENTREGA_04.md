# Trazabilidad — Entrega 04 Runtime Engine

> **Nota de lectura final:** este archivo es histórico y conserva el estado del paquete en el momento de esa entrega parcial. El estado final aprobado se verifica en `00_CONTROL_APROBACIONES.md`, `docs/TRAZABILIDAD_FINAL.md` y `docs/AUDITORIA_FINAL_ZIP.md`.


**Proyecto:** App Detección Prod — Motor de Workflow BPMN 2.0  
**Entrega:** 04  
**Estado del nuevo entregable:** PARA REVISIÓN

## 1. Cadena de aprobaciones

| Orden | Entregable | Estado | Evidencia |
|---:|---|---|---|
| 0 | Plan maestro de ejecución | APROBADO | `00_PLAN_EJECUCION_APROBADO.md` |
| 1 | PRD ligero | APROBADO | `docs/PRD.md` |
| 2 | FSD ligero | APROBADO | `docs/FSD.md` |
| 3 | Modelo de dominio Python | APROBADO | `src/domain/`, `docs/README_DOMAIN_MODEL.md`, `PR_implementation/PR_01_domain_model.md` |
| 4 | Runtime engine | PARA REVISIÓN | `src/runtime/`, `docs/README_RUNTIME_ENGINE.md`, `PR_implementation/PR_02_runtime_engine.md` |

## 2. Trazabilidad negocio → runtime

| Dolor de negocio App Detección Prod | Necesidad funcional | Implementación runtime |
|---|---|---|
| Reportes dispersos por WhatsApp/fotos | Caso trazable de producto próximo a vencer | `WorkflowInstance` + `execution_path` |
| Falta de control de precio | Precio como variable y recurso propagado | `variables[current_price]`, `ResourceInstance` |
| Falta de evidencia clara | Recursos obligatorios por tarea | `TaskInstance.has_mandatory_resources()` |
| Incertidumbre ante errores | Incidentes con glosa obligatoria | `raise_incident()` + `Incident.reason` |
| Reprocesos no controlados | Reintentos por transición | `TaskInstance.retry_count` |
| Riesgo de repetir errores sin límite | Cierre terminal en error | `WorkflowStatus.ERROR` al exceder `max_retries` |
| Falta de visibilidad gerencial | Camino completo auditable | `TraceEntry` con iteración, incidente y reset |

## 3. Trazabilidad FSD → código

| FSD | Código Entrega 04 | Validación |
|---|---|---|
| Modelo runtime | `src/runtime/instances.py` | Tests runtime |
| `WorkflowInstance` | `WorkflowInstance` | `test_start_and_forward_navigation_propagates_resources` |
| `TaskInstance` | `TaskInstance` | tests de ciclo de vida |
| Recursos reales | `ResourceInstance` en `TaskInstance.resources` | propagación + recurso manual |
| Compuertas de entrada | `can_start_task()` | test join `AND` |
| Trazabilidad | `TraceEntry`, `execution_path` | tests de incidente |
| Incidentes | `raise_incident()` | test reset |
| Reset aguas abajo | `_resolve_reset_task_ids()` | test backward incident |
| Reintentos | `retry_for()` | test retry exhaustion |
| Multi-asignación | `CompletionPolicy.ANY` | test multi-assignment |
| SLA reactivo | `timed_out_tasks()` | preparado para orquestador |

## 4. Trazabilidad PR implementation

| PR | Estado | Descripción |
|---|---|---|
| `PR_01_domain_model.md` | APROBADO | Modelo de dominio base |
| `PR_02_runtime_engine.md` | PARA REVISIÓN | Runtime de ejecución, traza, navegación, incidentes |

## 5. Evidencia técnica

Comandos ejecutados:

```bash
python -m compileall src
python -m unittest discover -s tests
```

Resultado:

```text
Ran 9 tests in ...s
OK
```

## 6. Próxima aprobación esperada

Para aprobar este entregable, responder:

```text
aprobado runtime
```

Luego se generará el **Entregable 05: Orquestador + cola Observer**.
