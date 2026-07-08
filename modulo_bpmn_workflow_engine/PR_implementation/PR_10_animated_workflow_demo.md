# PR-10 — Demo animada del workflow para defensa

## Objetivo

Agregar una visualización interactiva y animada del workflow BPMN principal de App Detección Prod para facilitar la defensa académica.

## Archivos agregados

```text
demo/animated_workflow.html
demo/README_ANIMATED_WORKFLOW.md
docs/WORKFLOW_ANIMADO.md
docs/TRAZABILIDAD_WORKFLOW_ANIMADO.md
PR_implementation/PR_10_animated_workflow_demo.md
```

## Justificación

El workflow ya estaba implementado en Python y documentado en FSD, pero para defensa resultaba útil contar con una vista visual que muestre cómo fluye el proceso paso a paso.

Esta mejora no cambia el motor ni los tests. Agrega una capa de presentación didáctica para explicar:

- Flujo principal.
- Split paralelo.
- Join AND.
- Incidentes.
- Rework.
- Cierre del caso.
- Trazabilidad visual.

## Decisión técnica

Se eligió un archivo HTML autocontenido con CSS y JavaScript embebido porque:

- No requiere dependencias.
- No requiere servidor local.
- Puede abrirse con doble clic.
- Es fácil de mostrar en una defensa.
- No afecta el motor Python existente.

## Relación con el código existente

| Demo visual | Código real |
|---|---|
| Bloques del flujo | `Task` en `src/domain/factory.py` |
| Flechas | `add_target()` |
| Incidentes/rework | `add_backward_transition()` |
| Estado runtime | `WorkflowInstance` |
| Bitácora visual | `TraceEvent` |
| Validación | Tests existentes |

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Confundir demo visual con motor real | Documentar que es una visualización didáctica. |
| Dependencia externa | No se usa ninguna. |
| Cambiar comportamiento del motor | No se modifica código Python existente. |

## Resultado esperado

El docente puede ver de forma visual cómo el caso avanza desde la detección hasta el cierre, y luego revisar el código para comprobar que ese flujo está implementado.
