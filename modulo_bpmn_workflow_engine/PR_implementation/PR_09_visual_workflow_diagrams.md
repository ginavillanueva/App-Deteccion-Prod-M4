# PR-09 — Visual workflow diagrams

**Estado:** APROBADO / COMPLEMENTO VISUAL  
**Feature:** Documentación visual del workflow principal  
**Módulo:** BPMN Workflow Engine aplicado a App Detección Prod

## 1. Objetivo

Agregar una vista visual del workflow para que el flujo no se vea únicamente como código Python en `src/domain/factory.py`, sino también como diagrama comprensible para defensa docente.

## 2. Problema resuelto

El workflow ya estaba implementado y probado, pero al abrir `factory.py` el flujo se veía como código. Para defensa oral, esto podía dificultar explicar rápidamente cómo fluye el proceso.

## 3. Solución implementada

Se agregó documentación visual en Mermaid:

```text
docs/WORKFLOW_VISUAL.md
docs/diagrams/workflow_principal.mmd
docs/diagrams/workflow_incidentes_reintentos.mmd
docs/diagrams/workflow_runtime_layers.mmd
```

## 4. Trazabilidad

| Elemento visual | Código relacionado | Documento relacionado |
|---|---|---|
| Workflow principal | `src/domain/factory.py` | `docs/FSD.md` |
| Incidentes y reintentos | `src/runtime/instances.py` | `docs/README_RUNTIME_ENGINE.md` |
| Capas del motor | `src/domain`, `src/runtime`, `src/orchestration`, `src/persistence` | `docs/TRAZABILIDAD_FINAL.md` |

## 5. Impacto técnico

No modifica la lógica del motor. No cambia tests. No altera persistencia. Solo mejora la explicabilidad del workflow.

## 6. Defensa

> Este PR agrega la representación visual del workflow principal. Cada bloque del diagrama corresponde a una tarea implementada en `factory.py`; cada flecha corresponde a una transición del motor; y cada retorno por error corresponde a una transición `BACKWARD` validada por tests.
