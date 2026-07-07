# Trazabilidad — Entrega 03 Modelo de Dominio Python

> **Nota de lectura final:** este archivo es histórico y conserva el estado del paquete en el momento de esa entrega parcial. El estado final aprobado se verifica en `00_CONTROL_APROBACIONES.md`, `docs/TRAZABILIDAD_FINAL.md` y `docs/AUDITORIA_FINAL_ZIP.md`.


**Proyecto:** App Detección Prod — Motor BPMN 2.0  
**Estado:** Dominio Python para revisión  

## 1. Trazabilidad de consigna a código

| Requisito de consigna | Implementación Entrega 03 | Archivo | Estado |
|---|---|---|---|
| Python con `dataclasses`, `Enum`, `type hints` | Clases de dominio tipadas | `src/domain/*.py` | Cubierto |
| Modelo de objetos en inglés | `Workflow`, `Task`, `LogicGate`, `Transition`, `Worker` | `src/domain/` | Cubierto |
| Workflow como grafo dirigido | `Task.targets`, `Task.incoming`, `DependencyMatrix` | `tasks.py`, `workflow.py` | Cubierto |
| Separación definición/runtime | Solo se modela definición; runtime queda para entrega 04 | `src/domain/` | Cubierto parcialmente por alcance |
| Compuertas embebidas | `Task.logic_gate` | `tasks.py`, `gates.py` | Cubierto |
| Recursos | `ResourceSpec`, `ResourceInstance` | `resources.py` | Cubierto |
| Workers | `Worker`, `WorkerType` | `workers.py`, `enums.py` | Cubierto |
| Incidentes y rework | `TransitionType.BACKWARD`, `Incident` | `transitions.py`, `incidents.py` | Cubierto |
| App Detección Prod | Factory del flujo de negocio | `factory.py` | Cubierto |

## 2. Trazabilidad de negocio App Detección Prod a dominio

| Necesidad de negocio | Elemento de dominio | Explicación |
|---|---|---|
| Registrar productos próximos a vencer | `detect_product_case` | Inicio del flujo operativo de campo. |
| Validar evidencia | `validate_evidence` + `product_photo` | Evita fotos sin estandarización o datos incompletos. |
| Clasificar riesgo | `classify_risk` | Prepara priorización por vencimiento e impacto. |
| Controlar precio | `validate_price_data`, `approve_price_change` | Permite auditar precio actual y aprobación. |
| Ejecutar acción comercial | `execute_retail_action` | Representa descuento, bandeo, retiro o promoción. |
| Supervisar y cerrar | `supervisor_review`, `close_case_and_update_dashboard` | Cierra con trazabilidad e indicadores. |
| Rehacer por error | `BACKWARD` hacia `validate_evidence` | Soporta errores de evidencia, precio o ejecución. |

## 3. Trazabilidad PRD → FSD → Código

| PRD/FSD aprobado | Código generado | Validación |
|---|---|---|
| Escenarios lineal/paralelo/join/ciclo | Factory con split y join AND; backward transitions | `test_domain_model.py` |
| Modelo de dominio | `Workflow`, `Task`, `LogicGate`, `ResourceSpec`, `Worker` | `python -m compileall src` |
| Trazabilidad de incidentes | `Incident.reason` obligatorio | Validación `__post_init__` |
| Reintentos | `Transition.max_retries` obligatorio en BACKWARD | Test unitario |
| Multi-asignación preparada | `CompletionPolicy`, `Worker.capacity` | Será usada en runtime/orquestador |
| SLA preparado | `max_time_to_assign`, `max_time_to_complete` | Será usado en runtime/orquestador |

## 4. Estado de aprobación

- Plan: aprobado.
- PRD: aprobado.
- FSD: aprobado.
- Dominio Python: para revisión.

## 5. Siguiente paso

Al aprobar esta entrega se implementará el runtime:

```text
src/runtime/
├── workflow_instance.py
├── task_instance.py
├── trace.py
└── __init__.py
```
