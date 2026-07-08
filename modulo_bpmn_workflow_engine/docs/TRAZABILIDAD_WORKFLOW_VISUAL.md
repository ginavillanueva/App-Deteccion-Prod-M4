# Trazabilidad del workflow visual

**Estado:** APROBADO / COMPLEMENTO VISUAL  
**Objetivo:** Agregar una vista visual del workflow principal sin alterar la lógica del motor ya aprobado.

| Necesidad de defensa | Evidencia visual | Evidencia técnica | Evidencia de prueba |
|---|---|---|---|
| Mostrar el flujo completo del proceso | `docs/WORKFLOW_VISUAL.md` | `src/domain/factory.py` | `tests/test_required_scenarios.py` |
| Explicar tareas y responsables | Sección 2 de `WORKFLOW_VISUAL.md` | `Task`, `WorkerType`, `ResourceSpec` | `test_domain_model.py` |
| Mostrar paralelismo y join AND | Diagrama principal | `LogicGate(type=GateType.AND)` | `test_required_scenarios.py` |
| Mostrar rework e incidentes | Diagrama de incidentes | `add_backward_transition(...)` | `test_runtime_engine.py` |
| Mostrar ejecución del motor | Diagrama por capas | `src/runtime`, `src/orchestration` | 28 tests OK |

## Relación con el entregable aprobado

Este complemento no reemplaza el PRD, FSD ni código aprobado. Solo agrega una capa visual para que el flujo sea más fácil de explicar durante la defensa.

## Archivos agregados

```text
docs/WORKFLOW_VISUAL.md
docs/diagrams/workflow_principal.mmd
docs/diagrams/workflow_incidentes_reintentos.mmd
docs/diagrams/workflow_runtime_layers.mmd
docs/TRAZABILIDAD_WORKFLOW_VISUAL.md
PR_implementation/PR_09_visual_workflow_diagrams.md
```
