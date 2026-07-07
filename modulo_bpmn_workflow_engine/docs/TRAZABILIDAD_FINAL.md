# Trazabilidad Final — App Detección Prod BPMN Workflow Engine

## Cadena de trazabilidad

| Nivel | Artefacto | Evidencia |
|---|---|---|
| Consigna | Motor workflow inspirado en BPMN 2.0 | `docs/FSD.md`, `src/`, `tests/` |
| Producto | App Detección Prod | `docs/PRD.md`, `docs/FSD.md` |
| Diseño funcional | Modelo de dominio, runtime, compuertas, recursos, workers, incidentes | `src/domain/`, `src/runtime/` |
| Orquestación | Cola Observer, asignación balanceada, ejecución sin cron | `src/orchestration/` |
| Persistencia | SQLite justificado | `src/persistence/`, `docs/README_PERSISTENCE.md` |
| Calidad | Escenarios obligatorios | `tests/`, `docs/README_TESTS.md` |
| Trazabilidad IA | Prompts usados y resultados | `docs/prompt_mappings.md` |
| Trazabilidad por feature | Implementaciones explicadas por PR | `PR_implementation/` |
| Contribución individual | Aportes por integrante | `docs/APORTES.md` |
| Repositorio | Guía de ejecución y defensa | `README.md` |

## Escenarios obligatorios cubiertos

| Escenario | Evidencia |
|---|---|
| Flujo lineal | `tests/test_required_scenarios.py` |
| Split paralelo | `tests/test_required_scenarios.py` |
| Join AND | `tests/test_required_scenarios.py` |
| Join OR | `tests/test_required_scenarios.py` |
| Ciclo / rework | `tests/test_required_scenarios.py` |
| Múltiples finales | `tests/test_required_scenarios.py` |
| Retorno por incidente con reset | `tests/test_required_scenarios.py` |
| Reintentos con fin en error | `tests/test_required_scenarios.py` |
| SLA / timeout | `tests/test_required_scenarios.py` |
| Multi-asignación | `tests/test_required_scenarios.py` |
| Ejecución concurrente | `src/orchestration/executor.py`, `tests/test_required_scenarios.py` |

## Estado final

Todos los entregables se encuentran aprobados y consolidados en el ZIP final.
