# Matriz de trazabilidad — Entrega 02

> **Nota de lectura final:** este archivo es histórico y conserva el estado del paquete en el momento de esa entrega parcial. El estado final aprobado se verifica en `00_CONTROL_APROBACIONES.md`, `docs/TRAZABILIDAD_FINAL.md` y `docs/AUDITORIA_FINAL_ZIP.md`.


**Proyecto:** App Detección Prod Workflow Engine BPMN 2.0  
**Fecha:** 2026-07-06  
**Estado del paquete:** Plan aprobado + PRD aprobado + FSD para revisión  

---

## 1. Trazabilidad de aprobaciones

| Entregable | Estado anterior | Estado actual | Evidencia |
|---|---|---|---|
| Plan maestro | APROBADO | APROBADO | Usuario indicó: “aprobado plan” |
| PRD | PARA REVISIÓN | APROBADO | Usuario indicó: “aprobado PRD” |
| FSD | PENDIENTE | PARA REVISIÓN | Generado desde PRD aprobado |

---

## 2. Trazabilidad consigna → FSD

| Requisito de consigna | Especificación en FSD | Archivo destino de implementación |
|---|---|---|
| Motor como grafo dirigido | Workflow principal y grafo lógico | `src/domain/tasks.py`, `src/domain/workflow.py` |
| Separar definición e instancia | Modelo definition/runtime | `src/domain/`, `src/runtime/` |
| Flujos lineales | Escenario obligatorio lineal | `tests/test_linear_flow.py` |
| Flujos paralelos | Split `ValidateEvidence -> ClassifyRisk/ValidatePriceData` | `tests/test_parallel_and_join.py` |
| Join AND | `DecideCommercialAction` espera dos ramas | `src/domain/gates.py` |
| Join OR | Cierre por evidencia o validación administrativa | `tests/test_or_join.py` |
| Ciclos/rework | `SupervisorReview -> ValidateEvidence` | `tests/test_rework_incident.py` |
| Múltiples finales | Cierre exitoso, rechazo, expirado, error | `tests/test_multiple_end_states.py` |
| Incidentes con reset | Algoritmo de incidente y reset | `src/runtime/incidents.py` |
| Reintentos con error | `max_retries` + `exhausted_status` | `tests/test_retry_exhausted.py` |
| SLA/timeout | Deadlines reactivos sin cron | `src/orchestration/orchestrator.py` |
| Multi-asignación | `CompletionPolicy.ALL/ANY/QUORUM` | `tests/test_multi_assignment.py` |
| Concurrencia | `Executor` + `Future` | `src/orchestration/executor.py` |
| Persistencia justificada | SQLite | `src/persistence/sqlite_repository.py` |
| REST/Lambda mock | `GateType.REST`, `GateType.LAMBDA` | `src/domain/gates.py` |
| Comparación Camunda/Activiti | Sección comparativa | `docs/FSD.md` |

---

## 3. Trazabilidad App Detección Prod → FSD

| Dolor del proyecto | Diseño funcional en FSD | Resultado esperado |
|---|---|---|
| Reportes dispersos por WhatsApp/fotos | `DetectProductCase` con recursos obligatorios | Registro estructurado |
| Falta de validación de datos | `ValidateEvidence` y reglas de recursos | Menos errores operativos |
| Falta de control de precios | `ValidatePriceData` y `ApprovePriceChange` | Cambio de precio auditable |
| Acciones comerciales no trazables | `DecideCommercialAction` y `ExecuteRetailAction` | Acción y responsable visibles |
| Falta de visibilidad gerencial | `CloseCaseAndUpdateDashboard` + `TraceEntry` | KPIs y trazabilidad |
| Errores repetidos | `Incident`, `BACKWARD`, `max_retries` | Rework controlado |
| Retrasos en decisiones | SLA y orquestación por cola | Escalamiento y control |
| Necesidad de múltiples roles | `WorkerType`, `Role`, `WorkerPool` | Asignación por especialidad |

---

## 4. Línea base congelada

A partir de esta entrega quedan como baseline aprobada:

```text
00_PLAN_EJECUCION_APROBADO.md
docs/PRD.md
```

El archivo `docs/FSD.md` queda en revisión. No debe marcarse como aprobado hasta recibir la frase explícita:

```text
aprobado FSD
```

---

## 5. Próximo paquete esperado

Cuando el FSD sea aprobado, el siguiente paquete deberá contener:

1. Plan aprobado.
2. PRD aprobado.
3. FSD aprobado.
4. Modelo de dominio propuesto para revisión en `src/domain/`.
5. ZIP acumulado actualizado.
