# Matriz de trazabilidad — Entrega 01

> **Nota de lectura final:** este archivo es histórico y conserva el estado del paquete en el momento de esa entrega parcial. El estado final aprobado se verifica en `00_CONTROL_APROBACIONES.md`, `docs/TRAZABILIDAD_FINAL.md` y `docs/AUDITORIA_FINAL_ZIP.md`.


**Proyecto:** App Detección Prod Workflow Engine BPMN 2.0  
**Fecha:** 2026-07-06  
**Estado del paquete:** Plan aprobado + PRD para revisión  

---

## 1. Trazabilidad entre consigna y PRD

| Fuente / requisito | Interpretación en el proyecto | Ubicación en PRD |
|---|---|---|
| Motor BPMN 2.0 como grafo dirigido | Workflow de productos próximos a vencer como grafo de tareas | Secciones 1, 4, 7, 9 |
| Python con `dataclasses`, `Enum`, type hints | Implementación técnica base del motor | Secciones 12, 16 |
| Modelo de dominio en inglés | Clases `Workflow`, `Task`, `LogicGate`, etc. | Secciones 6, 9, 17 |
| Documentación en español | PRD/FSD/README en español | Todo el documento |
| Compuertas embebidas en tarea destino | `LogicGate` en tareas de join | Secciones 7, 10 |
| Persistencia justificada | SQLite por reproducibilidad académica | Secciones 7, 12, 16 |
| REST/Lambda mock | Servicios simulados de clasificación o validación | Secciones 7, 16 |
| PRD ligero | Documento actual | `docs/PRD.md` |
| FSD ligero | Próximo entregable | `docs/FSD.md` |
| Repo Python | Estructura inicial preparada | `src/`, `tests/` |
| Prompt mappings | Pendiente de generar y mantener | `docs/prompt_mappings.md` |
| PR implementation | Pendiente por feature | `PR_implementation/` |
| Aportes individuales | Pendiente | `docs/APORTES.md` |

---

## 2. Trazabilidad entre App Detección Prod y motor

| Dolor de negocio | Requisito del motor | Task / componente |
|---|---|---|
| Reportes por WhatsApp y fotos dispersas | Registro estructurado con recursos obligatorios | `DetectProductCase`, `ResourceSpec` |
| Falta de validación | Tarea de validación y compuertas | `ValidateEvidence`, `LogicGate` |
| Falta de control de precio | Recurso y tarea de aprobación de precio | `ApprovePriceChange` |
| Acciones comerciales no trazadas | Task específica para decisión y ejecución | `DecideCommercialAction`, `ExecuteRetailAction` |
| Falta de KPIs | Cierre con actualización de dashboard | `CloseCaseAndUpdateDashboard` |
| Retrasos operativos | SLA y timeout | `TaskInstance.assignDeadline`, `completeDeadline` |
| Errores repetidos | Incidentes y reintentos | `Incident`, `TransitionType.BACKWARD` |
| Necesidad gerencial | Trazabilidad y estados finales | `executionPath`, `TraceEntry` |

---

## 3. Trazabilidad de aprobación

| Entregable | Estado | Qué se conserva en siguiente paquete |
|---|---|---|
| Plan | APROBADO | Sí, como baseline congelada |
| PRD | PARA REVISIÓN | Se aprobará o corregirá antes del FSD |
