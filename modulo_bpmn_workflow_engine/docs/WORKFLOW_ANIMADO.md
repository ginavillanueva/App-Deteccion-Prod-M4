# Workflow animado para defensa — App Detección Prod BPMN Engine

## Propósito

Este documento agrega una vista visual e interactiva del workflow principal de App Detección Prod. Su objetivo es facilitar la defensa académica mostrando cómo fluye un caso paso a paso, no solo como código Python.

## Archivo principal de la demo

```text
demo/animated_workflow.html
```

La demo es un archivo HTML autocontenido. No necesita instalación ni dependencias externas.

## Qué permite mostrar

- Inicio del caso.
- Detección del producto próximo a vencer.
- Validación de evidencia.
- Clasificación de riesgo.
- Validación de precio.
- Join AND antes de decidir la acción comercial.
- Aprobación humana del cambio de precio.
- Ejecución en sala.
- Revisión de supervisor.
- Cierre del caso.
- Actualización del dashboard.
- Incidente y retorno controlado a validación.
- Bitácora visual de ejecución.

## Flujo representado

```text
Start
  ↓
DetectProductCase
  ↓
ValidateEvidence
  ↓
Split paralelo
  ├── ClassifyRisk
  └── ValidatePriceData
        ↓
      Join AND
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
  ↓
End
```

## Cómo se relaciona con la implementación

| Vista visual | Implementación |
|---|---|
| Caja del flujo | `Task` en `src/domain/factory.py` |
| Flecha entre cajas | `add_target()` |
| Retorno por error | `add_backward_transition()` |
| Estado del caso | `WorkflowInstance` en `src/runtime/instances.py` |
| Bitácora | `TraceEvent` en `src/runtime/trace.py` |
| Asignación de tareas | `src/orchestration/assignment.py` |
| Cola de ejecución | `src/orchestration/queue.py` |
| Persistencia | `src/persistence/sqlite_repository.py` |
| Pruebas | `tests/test_required_scenarios.py` |

## Cómo usarlo en defensa

1. Abrir `demo/animated_workflow.html`.
2. Presionar **Ejecutar flujo** para mostrar el camino normal.
3. Presionar **Simular incidente** para mostrar cómo el proceso vuelve a validación cuando hay error.
4. Explicar que la demo visual corresponde al workflow implementado en `factory.py`.
5. Mostrar los tests para evidenciar que el motor cumple los escenarios obligatorios.

## Frase sugerida para defensa

> Esta demo animada permite visualizar el workflow principal de App Detección Prod. Cada bloque representa una tarea del motor BPMN implementada en Python. El flujo muestra el camino normal, el procesamiento paralelo de riesgo y precio, el Join AND antes de decidir la acción comercial, la aprobación humana del cambio de precio, la ejecución en tienda, la revisión del supervisor y el cierre con actualización del dashboard. También permite simular incidentes y rework.
