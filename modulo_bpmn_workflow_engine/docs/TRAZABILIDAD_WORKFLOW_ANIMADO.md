# Trazabilidad — Demo animada del workflow

## Objetivo

Agregar una representación visual e interactiva del flujo para facilitar la defensa del motor BPMN.

## Relación con entregables existentes

| Elemento agregado | Relación con el proyecto |
|---|---|
| `demo/animated_workflow.html` | Visualiza el flujo principal definido en el FSD y codificado en `factory.py`. |
| `demo/README_ANIMATED_WORKFLOW.md` | Explica cómo abrir y presentar la demo. |
| `docs/WORKFLOW_ANIMADO.md` | Documenta la finalidad académica y la relación con el motor. |
| `PR_implementation/PR_10_animated_workflow_demo.md` | Registra la mejora como feature adicional trazable. |

## Trazabilidad funcional

| Flujo visual | Código relacionado | Evidencia |
|---|---|---|
| DetectProductCase | `src/domain/factory.py` | `tests/test_required_scenarios.py` |
| ValidateEvidence | `src/domain/factory.py` | `tests/test_runtime_engine.py` |
| ClassifyRisk | `src/domain/factory.py` | `tests/test_required_scenarios.py` |
| ValidatePriceData | `src/domain/factory.py` | `tests/test_required_scenarios.py` |
| DecideCommercialAction | `src/domain/factory.py` | `tests/test_required_scenarios.py` |
| ApprovePriceChange | `src/domain/factory.py` | `tests/test_required_scenarios.py` |
| ExecuteRetailAction | `src/domain/factory.py` | `tests/test_runtime_engine.py` |
| SupervisorReview | `src/domain/factory.py` | `tests/test_required_scenarios.py` |
| CloseCaseAndUpdateDashboard | `src/domain/factory.py` | `tests/test_runtime_engine.py` |

## Criterio de aceptación

- La demo debe abrirse en navegador sin instalación.
- Debe mostrar flujo normal.
- Debe mostrar incidente/rework.
- Debe mantener correspondencia con `factory.py`.
- No debe reemplazar los tests ni el motor; solo visualiza el proceso.
