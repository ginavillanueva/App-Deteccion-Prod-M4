# Prompt Mappings — App Detección Prod BPMN Workflow Engine

**Proyecto:** App Detección Prod — Motor de Workflow tipo BPMN 2.0  
**Programa:** Maestría en Desarrollo de Productos de Software con IA  
**Curso:** Fundamentos de Programación y Frameworks Modernos para IA  
**Fecha de corte:** 2026-07-07  
**Estado del archivo:** APROBADO / ENTREGA FINAL  
**Entregable relacionado:** Entrega 08  

---

## 1. Propósito del documento

Este documento registra los prompts usados durante el desarrollo asistido por IA y los mapea contra los artefactos generados. Su finalidad es dejar evidencia verificable de:

1. qué instrucción originó cada entregable;
2. qué archivo o componente produjo dicha instrucción;
3. cuál fue el estado de revisión/aprobación;
4. cómo se conserva la trazabilidad entre consigna, documentación, código, pruebas y ZIP acumulado.

Este archivo no reemplaza el PRD, FSD ni los PR implementation. Actúa como bitácora de trazabilidad del uso de IA durante el proceso de construcción incremental.

---

## 2. Criterio de registro

Se registran los prompts explícitos entregados al asistente durante esta fase de construcción. Para mantener una documentación académica clara, los prompts largos se conservan como transcripción resumida fiel, sin alterar intención ni restricciones.

No se incluye razonamiento interno del asistente. Solo se documentan instrucciones visibles, decisiones aprobadas, artefactos generados y evidencia resultante.

---

## 3. Matriz principal de prompts y resultados

| ID | Fecha | Prompt / instrucción del usuario | Intención del prompt | Artefactos producidos | Estado |
|---|---|---|---|---|---|
| PM-00 | 2026-07-06 | “Las instrucciones están en el archivo adjunto. Deben responder cómo hacer paso a paso y uno por uno la consigna, así como el desarrollo de cada uno de ellos… hacer todo el proyecto en función a mi proyecto de App Detección… todos los entregables deben estar bien explicados y documentados… revisar paso a paso esperando mi aprobación… entregable aprobado más ZIP…” | Interpretar la consigna BPMN, adaptarla a App Detección Prod y definir una ruta incremental con aprobaciones. | `00_PLAN_EJECUCION_APROBADO.md` como plan maestro; estrategia de entregas acumuladas; regla de aprobación por entregable. | APROBADO |
| PM-01 | 2026-07-06 | “aprobado plan ojo que también debes darme los entregables aprobados el propuesto y el zip todo debemos de tener bien trazabilizado y aprobado” | Aprobar el plan y ordenar que cada entrega incluya aprobados + nuevo propuesto + ZIP acumulado. | `docs/PRD.md`; `00_CONTROL_APROBACIONES.md`; `docs/TRAZABILIDAD_ENTREGA_01.md`; ZIP `App_Deteccion_Prod_BPMN_Entrega_01_PLAN_APROBADO_PRD_REVISION.zip`. | PRD APROBADO posteriormente |
| PM-02 | 2026-07-06 | “aprobado PRD” | Aprobar PRD y avanzar al FSD. | `docs/FSD.md`; `docs/TRAZABILIDAD_ENTREGA_02.md`; ZIP `App_Deteccion_Prod_BPMN_Entrega_02_PRD_APROBADO_FSD_REVISION.zip`. | FSD APROBADO posteriormente |
| PM-03 | 2026-07-06 | “aprobado” | Aprobar el FSD pendiente de revisión y avanzar al modelo de dominio Python. | `src/domain/`; `docs/README_DOMAIN_MODEL.md`; `PR_implementation/PR_01_domain_model.md`; `docs/TRAZABILIDAD_ENTREGA_03.md`; ZIP de Entrega 03. | DOMINIO APROBADO posteriormente |
| PM-04 | 2026-07-07 | “aprobado” | Aprobar dominio y avanzar al runtime engine. | `src/runtime/`; `docs/README_RUNTIME_ENGINE.md`; `PR_implementation/PR_02_runtime_engine.md`; `docs/TRAZABILIDAD_ENTREGA_04.md`; ZIP de Entrega 04. | RUNTIME APROBADO posteriormente |
| PM-05 | 2026-07-07 | “aprobado” | Aprobar runtime y avanzar al orquestador con cola Observer. | `src/orchestration/`; `docs/README_ORCHESTRATION.md`; `PR_implementation/PR_03_orchestrator_queue.md`; `docs/TRAZABILIDAD_ENTREGA_05.md`; ZIP de Entrega 05. | ORQUESTADOR APROBADO posteriormente |
| PM-06 | 2026-07-07 | “aprobado” | Aprobar orquestador y avanzar a persistencia SQLite. | `src/persistence/`; `docs/README_PERSISTENCE.md`; `PR_implementation/PR_04_persistence_sqlite.md`; `docs/TRAZABILIDAD_ENTREGA_06.md`; ZIP de Entrega 06. | PERSISTENCIA APROBADA posteriormente |
| PM-07 | 2026-07-07 | “aprobado” | Aprobar persistencia y avanzar a tests obligatorios completos. | `tests/test_required_scenarios.py`; `src/orchestration/executor.py`; `docs/README_TESTS.md`; `PR_implementation/PR_05_mandatory_tests.md`; `docs/TRAZABILIDAD_ENTREGA_07.md`; ZIP de Entrega 07. | TESTS APROBADOS posteriormente |
| PM-08 | 2026-07-07 | “aprobado” | Aprobar tests y avanzar a `prompt_mappings.md`. | `docs/prompt_mappings.md`; `docs/README_PROMPT_MAPPINGS.md`; `PR_implementation/PR_06_prompt_mappings.md`; `docs/TRAZABILIDAD_ENTREGA_08.md`; ZIP de Entrega 08. | APROBADO posteriormente |

---

## 4. Contexto documental usado como base de prompts

| Fuente | Rol dentro del trabajo | Uso realizado |
|---|---|---|
| `bpmn-workflow-engine-design.md` | Consigna técnica principal del curso | Definió stack Python, modelo BPMN, compuertas, runtime, cola, Observer, persistencia, tests y entregables. |
| `M2. Consigna de Trabajo Final (App Deteccion Prod).docx` | Contexto de negocio y UX de App Detección Prod | Aportó problema real: productos próximos a vencer, WhatsApp/Excel, falta de trazabilidad, control de precios, KPIs y actores. |
| `Entrevista Gerente.docx` | Evidencia de usuario estratégico | Sustentó necesidad de dashboard, impacto financiero, visibilidad y decisiones rápidas. |
| `Entrevista Supervisor.docx` | Evidencia de usuario táctico | Sustentó validación, centralización, alertas, reducción de errores y trazabilidad operativa. |
| `Entrevista Vededor.docx` | Evidencia de usuario comercial | Sustentó necesidad de estado de producto, acción comercial, historial y cambio de precio. |
| Repositorio GitHub M4 indicado por el usuario | Antecedente técnico del proyecto | Permitió mantener continuidad con App Detección Prod y no plantear un motor genérico aislado. |

---

## 5. Trazabilidad por entregable generado

| Entrega | Prompt habilitante | Artefacto principal | Estado actual | Evidencia técnica |
|---|---|---|---|---|
| 00 | PM-00 | `00_PLAN_EJECUCION_APROBADO.md` | APROBADO | Ruta incremental definida. |
| 01 | PM-01 | `docs/PRD.md` | APROBADO | PRD aplicado a App Detección Prod BPMN. |
| 02 | PM-02 | `docs/FSD.md` | APROBADO | FSD con dominio, runtime, gates, recursos, workers, persistencia y comparación Camunda/Activiti. |
| 03 | PM-03 | `src/domain/` | APROBADO | `python -m compileall src`; tests unitarios OK. |
| 04 | PM-04 | `src/runtime/` | APROBADO | Runtime con instancias, trace, incidentes, reset y retries. |
| 05 | PM-05 | `src/orchestration/` | APROBADO | Cola `deque`, Observer, worker assignment. |
| 06 | PM-06 | `src/persistence/` | APROBADO | SQLite con snapshots y tests. |
| 07 | PM-07 | `tests/` | APROBADO | 28 tests OK. |
| 08 | PM-08 | `docs/prompt_mappings.md` | APROBADO | Registro de prompts y outputs. |

---

## 6. Mapeo prompt → decisión de diseño

| Decisión de diseño | Prompt relacionado | Justificación |
|---|---|---|
| Mantener App Detección Prod como caso de negocio | PM-00 | El usuario pidió desarrollar la consigna en función de su proyecto existente. |
| Entrega incremental con aprobación | PM-00, PM-01 | El usuario solicitó revisar paso a paso y recibir siempre aprobados + propuesto + ZIP. |
| Documentación en español y modelo en inglés | PM-00 + consigna técnica | La consigna exige modelo de objetos en inglés y documentación en español. |
| Python con `dataclasses`, `Enum`, `type hints` | PM-00 + consigna técnica | El stack fue confirmado por el curso. |
| SQLite como persistencia | PM-06 | Decisión defendible por simplicidad, durabilidad y uso local para evaluación. |
| Observer + cola | PM-05 | La consigna exige orquestador Observer y cola tipo SQS simulada. |
| Tests obligatorios completos | PM-07 | La consigna exige probar lineal, paralelo, AND, OR, ciclos, SLA, incidentes, retries, multi-asignación y concurrencia. |
| Registro formal de prompts | PM-08 | La consigna exige `prompt_mappings` como trazabilidad del uso de IA. |

---

## 7. Evidencia de aprobación acumulada

| Elemento aprobado | Prompt de aprobación | Evidencia en control |
|---|---|---|
| Plan | `aprobado plan` | `00_CONTROL_APROBACIONES.md` |
| PRD | `aprobado PRD` | `00_CONTROL_APROBACIONES.md` |
| FSD | `aprobado` después de FSD para revisión | `00_CONTROL_APROBACIONES.md` |
| Dominio | `aprobado` después de dominio para revisión | `00_CONTROL_APROBACIONES.md` |
| Runtime | `aprobado` después de runtime para revisión | `00_CONTROL_APROBACIONES.md` |
| Orquestador | `aprobado` después de orquestador para revisión | `00_CONTROL_APROBACIONES.md` |
| Persistencia | `aprobado` después de persistencia para revisión | `00_CONTROL_APROBACIONES.md` |
| Tests | `aprobado` después de tests para revisión | `00_CONTROL_APROBACIONES.md` |
| Prompt mappings | `aprobado` después de prompt mappings para revisión | `00_CONTROL_APROBACIONES.md` |

---

## 8. Cómo leer este archivo en defensa

Este documento puede defenderse con la siguiente explicación:

> El archivo `prompt_mappings.md` registra cómo se usó IA durante el desarrollo. Cada prompt está vinculado a un artefacto concreto: PRD, FSD, dominio, runtime, orquestador, persistencia, tests y documentación de trazabilidad. Además, cada avance fue sometido a aprobación incremental del usuario, por lo que el paquete final no surge de una generación única, sino de un proceso controlado, verificable y acumulativo.

---

## 9. Estado de revisión

**Estado:** APROBADO / ENTREGA FINAL  
**Evidencia:** aprobado e integrado al paquete final.  
**Siguiente entregable:** no aplica; el paquete final ya fue consolidado.
