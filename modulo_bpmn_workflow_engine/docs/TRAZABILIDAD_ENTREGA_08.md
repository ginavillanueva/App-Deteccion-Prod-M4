# Trazabilidad — Entrega 08: Prompt mappings

> **Nota de lectura final:** este archivo es histórico y conserva el estado del paquete en el momento de esa entrega parcial. El estado final aprobado se verifica en `00_CONTROL_APROBACIONES.md`, `docs/TRAZABILIDAD_FINAL.md` y `docs/AUDITORIA_FINAL_ZIP.md`.


**Proyecto:** App Detección Prod BPMN Workflow Engine  
**Estado:** Plan + PRD + FSD + Dominio + Runtime + Orquestador + Persistencia + Tests aprobados; Prompt mappings para revisión.

## 1. Cadena de trazabilidad acumulada

| Nivel | Artefacto | Estado | Evidencia |
|---|---|---|---|
| Plan | `00_PLAN_EJECUCION_APROBADO.md` | APROBADO | Define ruta incremental y entregables acumulados. |
| Producto | `docs/PRD.md` | APROBADO | Define objetivo, usuarios y valor del workflow aplicado a App Detección Prod. |
| Funcional | `docs/FSD.md` | APROBADO | Define modelo, runtime, compuertas, recursos, SLA, incidentes y comparación Camunda/Activiti. |
| Código dominio | `src/domain/` | APROBADO | Define `Workflow`, `Task`, `LogicGate`, `Transition`, `Resource`, `Worker`. |
| Código runtime | `src/runtime/` | APROBADO | Define `WorkflowInstance`, `TaskInstance`, traza, navegación, reset y reintentos. |
| Código orquestación | `src/orchestration/` | APROBADO | Define cola, Observer, asignación y eventos. |
| Persistencia | `src/persistence/` | APROBADO | Define repositorio SQLite y snapshots. |
| Pruebas | `tests/` | APROBADO | Valida escenarios obligatorios del motor BPMN. |
| Trazabilidad IA | `docs/prompt_mappings.md` | PARA REVISIÓN | Mapea prompts usados con artefactos generados. |

## 2. Requisito de consigna cubierto

| Requisito | Evidencia |
|---|---|
| Registrar prompts usados con IA | `docs/prompt_mappings.md` |
| Mapear prompts a resultados | Tabla PM-00 a PM-08 |
| Conservar trazabilidad del proceso | `00_CONTROL_APROBACIONES.md` + matrices por entrega |
| Mantener paquete acumulado | ZIP de Entrega 08 |

## 3. Relación prompt → artefacto

| Prompt | Artefacto generado | Estado |
|---|---|---|
| PM-00 | Plan maestro | APROBADO |
| PM-01 | PRD | APROBADO |
| PM-02 | FSD | APROBADO |
| PM-03 | Dominio | APROBADO |
| PM-04 | Runtime | APROBADO |
| PM-05 | Orquestador | APROBADO |
| PM-06 | Persistencia | APROBADO |
| PM-07 | Tests | APROBADO |
| PM-08 | Prompt mappings | PARA REVISIÓN |

## 4. Evidencia de ejecución técnica

Aunque esta entrega es documental, se volvió a ejecutar la suite completa para validar que el paquete acumulado sigue consistente.

```bash
python -m compileall src
python -m unittest discover -s tests
```

```text
Ran 28 tests
OK
```

## 5. Matriz PR implementation

| PR | Archivo | Estado |
|---|---|---|
| PR-01 | `PR_implementation/PR_01_domain_model.md` | APROBADO |
| PR-02 | `PR_implementation/PR_02_runtime_engine.md` | APROBADO |
| PR-03 | `PR_implementation/PR_03_orchestrator_queue.md` | APROBADO |
| PR-04 | `PR_implementation/PR_04_persistence_sqlite.md` | APROBADO |
| PR-05 | `PR_implementation/PR_05_mandatory_tests.md` | APROBADO |
| PR-06 | `PR_implementation/PR_06_prompt_mappings.md` | PARA REVISIÓN |

## 6. Lectura para el docente

Esta entrega demuestra que el uso de IA fue gestionado como parte del proceso de ingeniería, no como una generación aislada. Cada prompt se asocia a un resultado, cada resultado a un archivo, y cada archivo a un estado de aprobación.
