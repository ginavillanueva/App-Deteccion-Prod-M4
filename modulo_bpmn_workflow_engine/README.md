# App Detección Prod — BPMN Workflow Engine

**Curso:** Fundamentos de Programación y Frameworks Modernos para IA  
**Proyecto:** App Detección Prod  
**Entregable:** Motor de workflow inspirado en BPMN 2.0 aplicado a productos próximos a vencer  
**Stack:** Python, dataclasses, Enum, type hints, SQLite, unittest  
**Estado documental:** Entrega acumulada con Plan, PRD, FSD, dominio, runtime, orquestador, persistencia, tests, prompt mappings y aportes aprobados.  
**Fecha:** 2026-07-07

---

## 1. Resumen ejecutivo

Este repositorio implementa un **motor de workflow tipo BPMN 2.0** aplicado al caso **App Detección Prod**, una solución orientada a gestionar productos próximos a vencer en empresas distribuidoras e importadoras del canal retail.

El objetivo del motor es transformar un proceso operativo informal —basado en WhatsApp, fotografías dispersas, validaciones manuales, decisiones comerciales no trazables y ausencia de KPIs— en un flujo digital estructurado, auditable y programable.

El workflow permite orquestar:

1. detección de producto próximo a vencer;
2. validación de evidencia;
3. clasificación de riesgo;
4. validación de precio y cantidad;
5. decisión comercial;
6. aprobación de cambio de precio;
7. ejecución en sala;
8. revisión de supervisor;
9. cierre trazable;
10. actualización de indicadores.

La implementación no pretende reemplazar un motor BPMN industrial como Camunda o Activiti. Su propósito académico es demostrar, en Python, cómo un proceso de negocio puede representarse como un **grafo dirigido con tareas, transiciones, compuertas, recursos, workers, instancias, trazas, incidentes, reintentos, SLA, multi-asignación y concurrencia**.

---

## 2. Relación con la consigna

El repositorio responde a los componentes solicitados por la consigna:

| Requisito | Implementación en el repositorio |
|---|---|
| Motor de workflow inspirado en BPMN 2.0 | `src/domain/`, `src/runtime/`, `src/orchestration/` |
| Python con `dataclasses`, `Enum`, `type hints` | Modelo de dominio y runtime |
| Modelo de objetos en inglés | Clases como `Workflow`, `Task`, `LogicGate`, `WorkflowInstance`, `TaskInstance` |
| Documentación en español | `docs/PRD.md`, `docs/FSD.md`, READMEs y trazabilidad |
| Separación definición vs instancia | `Workflow` / `WorkflowInstance`, `Task` / `TaskInstance` |
| Compuertas embebidas en tarea destino | `LogicGate` asociada a `Task` |
| Flujos lineales, paralelos, AND, OR y cíclicos | Tests en `tests/test_required_scenarios.py` |
| Incidentes y retornos `BACKWARD` | `src/domain/incidents.py`, `src/runtime/instances.py` |
| Reset y reintentos | Runtime + tests de rework/error |
| SLA/timeout | Runtime + tests obligatorios |
| Multi-asignación | `CompletionPolicy.ALL/ANY/QUORUM` |
| Concurrencia | `src/orchestration/executor.py` |
| Persistencia justificada | SQLite en `src/persistence/` y `docs/README_PERSISTENCE.md` |
| Orquestador Observer + cola | `src/orchestration/queue.py`, `src/orchestration/orchestrator.py` |
| Trazabilidad IA | `docs/prompt_mappings.md` |
| PR implementation por feature | Carpeta `PR_implementation/` |
| Contribución individual | `docs/APORTES.md` |

---

## 3. Problema de negocio aplicado

En App Detección Prod, el problema central es la falta de una plataforma estructurada para controlar productos próximos a vencer. El proceso actual suele depender de reportes informales, fotografías no estandarizadas, WhatsApp, Excel y validaciones manuales.

Esto provoca:

- falta de trazabilidad;
- pérdida de visibilidad para supervisión y gerencia;
- dificultad para validar precios y cantidades;
- acciones comerciales no medibles;
- cambios de precio sin auditoría suficiente;
- riesgo de merma por vencimiento;
- decisiones tardías o basadas en información incompleta.

El motor BPMN resuelve este problema modelando el proceso como una cadena de tareas ejecutables, con estados, compuertas, workers, incidentes, trazas y KPIs derivados.

---

## 4. Workflow principal implementado

```text
DetectProductCase
    ↓
ValidateEvidence
    ↓
ClassifyRisk
    ↓
ValidatePriceData
    ↓
DecideCommercialAction
    ↓
ApprovePriceChange
    ↓
ExecuteRetailAction
    ↓
SupervisorReview
    ↓
CloseCaseAndUpdateDashboard
```

### Variantes soportadas

```text
Flujo lineal:
A → B → C → D

Split paralelo:
A → {B, C}

Join AND:
{B, C} → D cuando ambas tareas están completadas

Join OR:
{B, C} → D cuando al menos una rama habilita el avance

Rework:
SupervisorReview → ValidateEvidence

Incidente:
ExecuteRetailAction → ValidateEvidence

Error por reintentos agotados:
WorkflowInstance.status = ERROR

Múltiples finales:
CloseCaseSuccessfully
CloseCaseWithRejectedAction
CloseCaseWithExpiredProduct
CloseCaseWithErrorAfterRetries
```

---

## 5. Estructura del repositorio

```text
.
├── README.md
├── 00_CONTROL_APROBACIONES.md
├── 00_PLAN_EJECUCION_APROBADO.md
├── docs/
│   ├── PRD.md
│   ├── FSD.md
│   ├── APORTES.md
│   ├── prompt_mappings.md
│   ├── AUDITORIA_FINAL_ZIP.md
│   ├── README_DOMAIN_MODEL.md
│   ├── README_RUNTIME_ENGINE.md
│   ├── README_ORCHESTRATION.md
│   ├── README_PERSISTENCE.md
│   ├── README_TESTS.md
│   ├── README_PROMPT_MAPPINGS.md
│   ├── README_APORTES.md
│   ├── README_REPOSITORY.md
│   └── TRAZABILIDAD_ENTREGA_*.md
├── PR_implementation/
│   ├── PR_01_domain_model.md
│   ├── PR_02_runtime_engine.md
│   ├── PR_03_orchestrator_queue.md
│   ├── PR_04_persistence_sqlite.md
│   ├── PR_05_mandatory_tests.md
│   ├── PR_06_prompt_mappings.md
│   ├── PR_07_individual_contribution.md
│   └── PR_08_repository_readme.md
├── src/
│   ├── domain/
│   ├── runtime/
│   ├── orchestration/
│   └── persistence/
└── tests/
    ├── test_domain_model.py
    ├── test_runtime_engine.py
    ├── test_orchestration.py
    ├── test_persistence_sqlite.py
    └── test_required_scenarios.py
```

---

## 6. Instalación y ejecución

### 6.1 Requisitos

- Python 3.10 o superior.
- No requiere dependencias externas obligatorias para correr los tests actuales.
- SQLite se usa mediante la librería estándar `sqlite3`.

### 6.2 Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

### 6.3 Ejecutar validación de sintaxis

```bash
python -m compileall src
```

### 6.4 Ejecutar todos los tests

```bash
python -m unittest discover -s tests
```

Resultado esperado:

```text
Ran 28 tests
OK
```

---

## 7. Escenarios obligatorios cubiertos por tests

| Escenario | Archivo principal | Estado |
|---|---|---|
| Flujo lineal | `tests/test_required_scenarios.py` | Cubierto |
| Split paralelo | `tests/test_required_scenarios.py` | Cubierto |
| Join AND | `tests/test_required_scenarios.py` | Cubierto |
| Join OR | `tests/test_required_scenarios.py` | Cubierto |
| Ciclo / rework | `tests/test_required_scenarios.py` | Cubierto |
| Múltiples finales | `tests/test_required_scenarios.py` | Cubierto |
| Incidente con reset | `tests/test_required_scenarios.py` | Cubierto |
| Reintentos con fin en error | `tests/test_required_scenarios.py` | Cubierto |
| SLA / timeout | `tests/test_required_scenarios.py` | Cubierto |
| Multi-asignación | `tests/test_required_scenarios.py` | Cubierto |
| Ejecución concurrente | `tests/test_required_scenarios.py` + `src/orchestration/executor.py` | Cubierto |

---

## 8. Componentes principales

### 8.1 Dominio

Ubicación: `src/domain/`

Contiene las entidades de definición del workflow:

- `Workflow`
- `Task`
- `LogicGate`
- `Transition`
- `ResourceSpec`
- `Worker`
- `Incident`
- Enums de estado, tipo de tarea, tipo de compuerta, roles, recursos y políticas de completado.

### 8.2 Runtime

Ubicación: `src/runtime/`

Contiene la ejecución real del proceso:

- `WorkflowInstance`
- `TaskInstance`
- `ResourceInstance`
- `TraceEntry`
- navegación a tareas destino;
- registro de traza;
- incidentes;
- resets;
- reintentos;
- finalización.

### 8.3 Orquestación

Ubicación: `src/orchestration/`

Contiene:

- cola de tareas listas con `collections.deque`;
- eventos Observer;
- asignación de workers por especialidad y menor carga;
- executor/future para concurrencia;
- orquestador de tareas.

### 8.4 Persistencia

Ubicación: `src/persistence/`

Se implementa persistencia SQLite para guardar snapshots de:

- definiciones de workflow;
- instancias de workflow;
- task instances;
- trazas;
- incidentes;
- workers.

La decisión está justificada en `docs/README_PERSISTENCE.md` y en `docs/FSD.md`.

---

## 9. Comandos útiles para el docente

### Ver estructura

```bash
find . -maxdepth 3 -type f | sort
```

### Validar sintaxis

```bash
python -m compileall src
```

### Ejecutar pruebas

```bash
python -m unittest discover -s tests
```

### Ver documentación principal

```bash
cat docs/PRD.md
cat docs/FSD.md
cat docs/prompt_mappings.md
cat docs/APORTES.md
```

---

## 10. Trazabilidad documental

La entrega se construyó de forma incremental y aprobada por etapas.

| Entrega | Artefacto | Estado |
|---:|---|---|
| 0 | Plan maestro | Aprobado |
| 1 | PRD | Aprobado |
| 2 | FSD | Aprobado |
| 3 | Modelo de dominio | Aprobado |
| 4 | Runtime engine | Aprobado |
| 5 | Orquestador + cola Observer | Aprobado |
| 6 | Persistencia SQLite | Aprobado |
| 7 | Tests obligatorios | Aprobado |
| 8 | Prompt mappings | Aprobado |
| 9 | Aportes individuales | Aprobado |
| 10 | README final | Aprobado |

La matriz de control se encuentra en:

```text
00_CONTROL_APROBACIONES.md
```

La trazabilidad por entrega se encuentra en:

```text
docs/TRAZABILIDAD_ENTREGA_01.md
docs/TRAZABILIDAD_ENTREGA_02.md
docs/TRAZABILIDAD_ENTREGA_03.md
docs/TRAZABILIDAD_ENTREGA_04.md
docs/TRAZABILIDAD_ENTREGA_05.md
docs/TRAZABILIDAD_ENTREGA_06.md
docs/TRAZABILIDAD_ENTREGA_07.md
docs/TRAZABILIDAD_ENTREGA_08.md
docs/TRAZABILIDAD_ENTREGA_09.md
docs/TRAZABILIDAD_ENTREGA_10.md
```

---

## 11. Relación PRD → FSD → Código → Tests

| Nivel | Archivo | Propósito |
|---|---|---|
| Producto | `docs/PRD.md` | Define qué se construye y por qué |
| Funcional | `docs/FSD.md` | Define cómo funciona el motor |
| Implementación dominio | `src/domain/` | Modela el grafo, tareas, compuertas, recursos y workers |
| Implementación runtime | `src/runtime/` | Ejecuta instancias, estados, traza e incidentes |
| Implementación orquestación | `src/orchestration/` | Cola, Observer, workers y concurrencia |
| Implementación persistencia | `src/persistence/` | Guarda estado durable en SQLite |
| Evidencia | `tests/` | Verifica los escenarios obligatorios |
| Trazabilidad IA | `docs/prompt_mappings.md` | Registra uso de prompts y resultados |
| Auditoría final | `docs/AUDITORIA_FINAL_ZIP.md` | Verifica coherencia, inventario y estado aprobado del ZIP |
| Contribución | `docs/APORTES.md` | Documenta responsabilidad individual |

---

## 12. Decisiones técnicas defendibles

| Decisión | Justificación |
|---|---|
| Python puro | Cumple consigna y facilita evaluación académica. |
| `dataclasses` y `Enum` | Modelo legible, tipado y simple de auditar. |
| Compuertas en tarea destino | Respeta la decisión didáctica de la consigna. |
| SQLite | Persistencia durable sin complejidad operacional. |
| `collections.deque` | Cola nativa, simple y suficiente para emular ready queue. |
| Observer | Permite reaccionar a eventos sin cron. |
| Threaded executor | Demuestra concurrencia sin introducir complejidad innecesaria. |
| Tests con `unittest` | No requiere dependencias externas y facilita corrección. |

---

## 13. Guion breve de defensa

> Este proyecto implementa un motor de workflow inspirado en BPMN 2.0 aplicado a App Detección Prod. El motor modela el proceso como un grafo dirigido donde las tareas son nodos y las transiciones son aristas. Se separa definición de ejecución mediante `Workflow` y `WorkflowInstance`, se soportan compuertas AND/OR/XOR/COMPLEX, recursos propagables, workers, cola de tareas listas, orquestador Observer, persistencia SQLite, incidentes, resets, reintentos, SLA, multi-asignación y concurrencia. La solución está conectada con el problema real de negocio: controlar productos próximos a vencer, validar evidencia, auditar cambios de precio, ejecutar acciones comerciales y cerrar casos con trazabilidad.

---

## 14. Estado final de la entrega

Este README corresponde al repositorio final **APROBADO**. El paquete completo queda listo para subir a GitHub con todos los artefactos, código, pruebas y trazabilidad consolidados.
