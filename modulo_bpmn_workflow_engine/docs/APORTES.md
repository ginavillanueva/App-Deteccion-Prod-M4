# APORTES.md — Contribución individual del equipo

**Proyecto:** App Detección Prod — BPMN Workflow Engine  
**Curso:** Fundamentos de Programación y Frameworks Modernos para IA  
**Fecha:** 2026-07-07  
**Estado:** APROBADO / ENTREGA FINAL  
**Versión:** Entrega 09  

---

## 1. Propósito del documento

Este documento declara la contribución individual asociada al diseño, implementación, documentación y validación del motor de workflow inspirado en BPMN 2.0 aplicado a **App Detección Prod**.

La finalidad es entregar al docente una evidencia clara de responsabilidad, alcance de trabajo y trazabilidad entre:

- requerimientos del PRD;
- especificación funcional del FSD;
- implementación en Python;
- pruebas obligatorias;
- documentación `PR_implementation`;
- uso trazado de IA en `docs/prompt_mappings.md`.

> **Nota de integridad académica:** el asistente de IA no se declara como integrante del grupo. Su uso queda documentado exclusivamente como apoyo metodológico y técnico en `docs/prompt_mappings.md`.

---

## 2. Integrantes documentados

| Integrante | Rol académico / responsabilidad principal | Estado en esta entrega |
|---|---|---|
| Gina Fabiana Villanueva Viscarra | Responsable principal del proyecto, definición de caso App Detección Prod, validación académica de entregables y aprobación incremental | Documentado |

> Si el docente solicita registrar más integrantes, este documento debe actualizarse con nombres reales, responsabilidades reales y porcentajes reales antes de la entrega definitiva. En la versión actual solo se documenta el integrante informado en los antecedentes del proyecto.

---

## 3. Matriz general de contribución

| Integrante | Componente / responsabilidad | Contribución | % estimado |
|---|---|---|---:|
| Gina Fabiana Villanueva Viscarra | Enfoque de negocio y adaptación del caso App Detección Prod | Definición del problema aplicado: productos próximos a vencer, evidencia, acciones comerciales, control de precio, cantidad intervenida, KPIs y reducción de merma. | 15% |
| Gina Fabiana Villanueva Viscarra | PRD y alcance funcional | Validación del alcance del motor BPMN aplicado al flujo de detección, validación, clasificación, decisión comercial, aprobación de precio, ejecución, revisión y cierre. | 10% |
| Gina Fabiana Villanueva Viscarra | FSD y especificación funcional | Revisión y aprobación de dominio, estados, compuertas, recursos, workers, incidentes, SLAs, persistencia y comparación Camunda/Activiti. | 15% |
| Gina Fabiana Villanueva Viscarra | Modelo de dominio Python | Validación de clases `Workflow`, `Task`, `LogicGate`, `Transition`, `ResourceSpec`, `Worker`, enumeraciones y fábrica de workflow App Detección Prod. | 15% |
| Gina Fabiana Villanueva Viscarra | Runtime engine | Validación del runtime: `WorkflowInstance`, `TaskInstance`, traza, recursos runtime, navegación, incidentes, reset y reintentos. | 15% |
| Gina Fabiana Villanueva Viscarra | Orquestador, cola y workers | Validación de `ReadyQueue`, patrón Observer, asignación por especialidad, carga de trabajo y eventos de ejecución. | 10% |
| Gina Fabiana Villanueva Viscarra | Persistencia SQLite | Validación de la decisión SQLite, esquema mínimo, guardado de snapshots, workers, trazas e incidentes. | 5% |
| Gina Fabiana Villanueva Viscarra | Pruebas obligatorias | Validación de escenarios requeridos: lineal, paralelo, AND, OR, ciclo/rework, finales múltiples, incidente/reset, reintentos/error, SLA, multi-asignación y concurrencia. | 10% |
| Gina Fabiana Villanueva Viscarra | Trazabilidad, prompts y aprobaciones | Aprobación incremental por entregable y control documental acumulado mediante `00_CONTROL_APROBACIONES.md`, `TRAZABILIDAD_ENTREGA_NN.md` y `prompt_mappings.md`. | 5% |
| **Total** |  |  | **100%** |

---

## 4. Aportes por entregable aprobado

| Entrega | Artefacto | Aporte documentado | Estado |
|---:|---|---|---|
| 0 | `00_PLAN_EJECUCION_APROBADO.md` | Alineación del proyecto a App Detección Prod y definición de ruta incremental con aprobación paso a paso. | Aprobado |
| 1 | `docs/PRD.md` | Definición del producto, usuarios, escenarios y criterios de éxito del workflow engine. | Aprobado |
| 2 | `docs/FSD.md` | Especificación funcional del motor, dominio, runtime, compuertas, recursos, orquestación, persistencia y comparación. | Aprobado |
| 3 | `src/domain/` | Implementación del modelo de dominio en inglés con `dataclasses`, `Enum` y `type hints`. | Aprobado |
| 4 | `src/runtime/` | Implementación de instancias, estados runtime, traza, navegación e incidentes. | Aprobado |
| 5 | `src/orchestration/` | Implementación de cola, Observer, worker pool y asignación balanceada. | Aprobado |
| 6 | `src/persistence/` | Implementación de persistencia SQLite y repositorio de snapshots. | Aprobado |
| 7 | `tests/` | Validación de escenarios obligatorios y ejecución satisfactoria de pruebas automatizadas. | Aprobado |
| 8 | `docs/prompt_mappings.md` | Registro trazable de prompts, intención, artefacto generado y aprobación. | Aprobado |
| 9 | `docs/APORTES.md` | Declaración de contribución individual y responsabilidad académica. | APROBADO |

---

## 5. Trazabilidad de responsabilidad por componente técnico

| Capa | Carpeta / archivo | Responsabilidad funcional | Evidencia |
|---|---|---|---|
| Dominio | `src/domain/` | Define el grafo, tareas, compuertas, recursos, workers, transiciones e incidentes. | `PR_implementation/PR_01_domain_model.md` |
| Runtime | `src/runtime/` | Ejecuta instancias, estados, traza, recursos runtime, navegación e incidentes. | `PR_implementation/PR_02_runtime_engine.md` |
| Orquestación | `src/orchestration/` | Maneja cola, Observer, asignación y concurrencia base. | `PR_implementation/PR_03_orchestrator_queue.md` |
| Persistencia | `src/persistence/` | Guarda snapshots del workflow y evidencia de ejecución. | `PR_implementation/PR_04_persistence_sqlite.md` |
| Pruebas | `tests/` | Comprueba escenarios obligatorios y regresión técnica. | `PR_implementation/PR_05_mandatory_tests.md` |
| Trazabilidad IA | `docs/prompt_mappings.md` | Mapea prompts usados con artefactos producidos. | `PR_implementation/PR_06_prompt_mappings.md` |
| Aportes | `docs/APORTES.md` | Declara contribución individual y responsabilidad académica. | `PR_implementation/PR_07_individual_contribution.md` |

---

## 6. Declaración de uso responsable de IA

Durante la elaboración del proyecto se utilizó IA generativa como apoyo para estructurar documentación, proponer código, ordenar trazabilidad y generar pruebas. Sin embargo:

1. La decisión del caso de negocio corresponde al proyecto App Detección Prod.
2. La revisión y aprobación incremental de entregables fue realizada por la autora del proyecto.
3. La IA no se declara como autora académica ni como integrante.
4. Los prompts y sus resultados quedan documentados en `docs/prompt_mappings.md`.
5. El código y documentos finales deben ser revisados por la autora antes de ser enviados al docente.

---

## 7. Evidencia de validación técnica acumulada

La entrega técnica se validó con:

```bash
python -m compileall src
python -m unittest discover -s tests
```

Resultado acumulado de la última validación:

```text
Ran 28 tests
OK
```

---

## 8. Cómo defender este documento ante el docente

Este documento puede explicarse de la siguiente manera:

> La contribución individual se documentó por componente y por entregable, no solo como una tabla nominal. Cada aporte está conectado con evidencia concreta en el repositorio: PRD, FSD, código, pruebas, PR_implementation, prompt_mappings y matriz de aprobaciones. Esto permite auditar qué se diseñó, qué se implementó, qué se probó y cómo fue aprobado incrementalmente.

---

## 9. Estado de revisión

| Documento | Estado |
|---|---|
| `docs/APORTES.md` | APROBADO |
| `docs/README_APORTES.md` | APROBADO |
| `PR_implementation/PR_07_individual_contribution.md` | APROBADO |
| `docs/TRAZABILIDAD_ENTREGA_09.md` | Histórico de revisión / aprobado en entrega final |

**Estado final:** documento aprobado e integrado al ZIP final.
