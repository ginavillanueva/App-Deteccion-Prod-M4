# README — Modelo de Dominio Python

**Proyecto:** App Detección Prod — Motor de Workflow BPMN 2.0  
**Entrega:** 03 — Modelo de dominio Python  
**Estado:** APROBADO / ENTREGA FINAL  
**Idioma:** documentación en español; modelo de objetos en inglés.

## 1. Propósito

Este entregable implementa la capa de dominio del motor de workflow tipo BPMN 2.0 aplicado a App Detección Prod. El objetivo es dejar definidas las clases que representan la plantilla del proceso antes de avanzar hacia runtime, cola, orquestador, persistencia y pruebas completas.

El modelo permite representar el flujo de negocio de detección de productos próximos a vencer como un grafo dirigido compuesto por `Workflow`, `Task`, `Transition`, `LogicGate`, `ResourceSpec` y `Worker`.

## 2. Archivos incluidos

```text
src/domain/
├── __init__.py
├── enums.py
├── resources.py
├── workers.py
├── transitions.py
├── gates.py
├── tasks.py
├── incidents.py
├── workflow.py
└── factory.py
```

## 3. Decisiones implementadas

| Decisión | Implementación | Justificación |
|---|---|---|
| Modelo en inglés | Clases `Workflow`, `Task`, `LogicGate`, `Transition`, `Worker` | Cumple la consigna del curso. |
| Python moderno | `dataclasses`, `Enum`, `type hints` | Permite claridad, validación y legibilidad. |
| Grafo dirigido | `targets`, `incoming`, `DependencyMatrix` | Representa nodos y aristas del workflow. |
| Compuertas embebidas | `LogicGate` dentro de `Task` | Mantiene el enfoque de join dentro de la tarea destino. |
| Incidentes/rework | `TransitionType.BACKWARD` + `Incident` | Distingue avance normal de retorno por error operativo. |
| Recursos | `ResourceSpec` y `ResourceInstance` | Soporta evidencia, precio, cantidad, acción comercial y aprobación. |
| Workers | `Worker` + `WorkerType` | Prepara asignación balanceada por especialidad. |
| Flujo de referencia | `build_app_deteccion_workflow()` | Aterriza el dominio en el caso real App Detección Prod. |

## 4. Flujo de referencia implementado

```text
DetectProductCase
  → ValidateEvidence
  → {ClassifyRisk, ValidatePriceData}
  → DecideCommercialAction
  → ApprovePriceChange
  → ExecuteRetailAction
  → SupervisorReview
  → CloseCaseAndUpdateDashboard
```

También se modelan retornos por incidente:

```text
SupervisorReview → ValidateEvidence
ExecuteRetailAction → ValidateEvidence
```

Estos retornos representan errores de evidencia, precio, cantidad o ejecución comercial.

## 5. Cómo validar esta entrega

Desde la raíz del paquete:

```bash
python -m compileall src
python -m unittest discover -s tests
```

El test incluido valida que el workflow de referencia se pueda construir, que exista join AND, que haya transición BACKWARD y que la matriz de dependencias identifique rutas alcanzables.
