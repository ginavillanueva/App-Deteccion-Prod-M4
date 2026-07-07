# Entregable 0 — PLAN_EJECUCION_APROBADO

**Proyecto:** App Detección Prod — Motor de Workflow tipo BPMN 2.0  
**Curso:** Fundamentos de Programación y Frameworks Modernos para IA  
**Estado:** APROBADO  
**Aprobación del usuario:** “aprobado plan”  
**Fecha de registro:** 2026-07-06  
**Idioma documentación:** Español  
**Idioma modelo de objetos:** Inglés  

---

## 1. Decisión estratégica aprobada

Se aprueba desarrollar la consigna del motor de workflow tipo BPMN 2.0 **sin cambiar de proyecto**, tomando como dominio aplicado la solución **App Detección Prod**.

La decisión aprobada es construir un motor de workflow en Python que orqueste el ciclo completo de gestión de productos próximos a vencer:

```text
DetectProductCase
→ ValidateEvidence
→ ClassifyRisk
→ DecideCommercialAction
→ ApprovePriceChange
→ ExecuteRetailAction
→ SupervisorReview
→ CloseCaseAndUpdateDashboard
```

Este enfoque permite mantener continuidad con los módulos anteriores y transformar el proyecto existente en una solución más técnica, evaluable y demostrable para el curso.

---

## 2. Alcance aprobado

El motor deberá cubrir:

1. Representación de workflows como grafos dirigidos.
2. Separación entre definición e instancia:
   - `Workflow` / `Task`
   - `WorkflowInstance` / `TaskInstance`
3. Flujos lineales, paralelos, condicionales, convergentes y cíclicos.
4. Compuertas embebidas en la tarea destino mediante `LogicGate`.
5. Recursos de entrada/salida mediante `ResourceSpec` y `ResourceInstance`.
6. Workers por especialidad y asignación balanceada.
7. Orquestación con cola y patrón Observer.
8. Persistencia justificada con SQLite.
9. Integraciones REST/Lambda simuladas mediante mocks.
10. Trazabilidad completa mediante `TraceEntry`.
11. Incidentes, reintentos, reset, SLA, multi-asignación y concurrencia.

---

## 3. Workflow de negocio aprobado para App Detección Prod

### 3.1 Flujo principal

| Código | Task del motor | Rol principal | Descripción de negocio |
|---|---|---|---|
| A | `DetectProductCase` | Mercaderista | Registra producto próximo a vencer, evidencia, precio, cantidad y tienda. |
| B | `ValidateEvidence` | Supervisor | Verifica evidencia, datos obligatorios, foto y coherencia del caso. |
| C | `ClassifyRisk` | Servicio/IA mock | Clasifica riesgo bajo, medio o alto. |
| D | `DecideCommercialAction` | Vendedor/Supervisor | Define descuento, bandeo, retiro, promoción o seguimiento. |
| E | `ApprovePriceChange` | Supervisor/Admin | Aprueba cambio de precio cuando corresponda. |
| F | `ExecuteRetailAction` | Mercaderista/Vendedor | Ejecuta la acción comercial en sala. |
| G | `SupervisorReview` | Supervisor | Revisa si la acción fue correctamente aplicada. |
| H | `CloseCaseAndUpdateDashboard` | Sistema/Gerencia | Cierra el caso y actualiza indicadores. |

### 3.2 Flujos especiales aprobados

| Requisito BPMN | Aplicación en App Detección Prod |
|---|---|
| Lineal | Registro → Validación → Clasificación → Decisión |
| Paralelo | Validación de evidencia y validación de precio en paralelo |
| Join AND | La decisión comercial espera clasificación de riesgo + validación de precio |
| Join OR | Avance por evidencia completa o validación manual del supervisor |
| Ciclo/rework | Revisión del supervisor devuelve el caso a validación |
| Incidente | Evidencia incompleta, precio incorrecto, cantidad inconsistente |
| Reintentos | Si el caso falla más de N veces, termina en estado `ERROR` |
| SLA/timeout | Caso crítico no atendido dentro del plazo pasa a `TIMED_OUT` |
| Multi-asignación | Validación puede requerir supervisor + vendedor |
| Concurrencia | Varias tareas/casos pueden ejecutarse en paralelo |

---

## 4. Orden de entregables aprobado

| Orden | Entregable | Archivo esperado | Estado actual |
|---:|---|---|---|
| 0 | Plan maestro | `00_PLAN_EJECUCION_APROBADO.md` | APROBADO |
| 1 | PRD ligero | `docs/PRD.md` | PARA REVISIÓN |
| 2 | FSD ligero | `docs/FSD.md` | PENDIENTE |
| 3 | Modelo de dominio Python | `src/domain/` | PENDIENTE |
| 4 | Runtime del workflow | `src/runtime/` | PENDIENTE |
| 5 | Orquestador y cola | `src/orchestration/` | PENDIENTE |
| 6 | Persistencia SQLite | `src/persistence/` | PENDIENTE |
| 7 | Pruebas obligatorias | `tests/` | PENDIENTE |
| 8 | PR implementation | `PR_implementation/` | PENDIENTE |
| 9 | Prompt mappings | `docs/prompt_mappings.md` | PENDIENTE |
| 10 | Aportes individuales | `docs/APORTES.md` | PENDIENTE |
| 11 | README final | `README.md` | PENDIENTE |
| 12 | ZIP final | `.zip` | PENDIENTE |

---

## 5. Regla de aprobación incremental

A partir de este plan, cada entrega seguirá la misma regla:

1. Se entrega el archivo nuevo en estado **PARA REVISIÓN**.
2. Se conserva todo lo previamente aprobado.
3. Se actualiza `00_CONTROL_APROBACIONES.md`.
4. Se genera un ZIP con:
   - entregables aprobados,
   - entregable nuevo propuesto,
   - matriz de trazabilidad,
   - manifiesto del paquete.
5. El usuario aprueba con una frase explícita:
   - `aprobado PRD`
   - `aprobado FSD`
   - `aprobado dominio`
   - etc.

---

## 6. Criterio de defensa ante el docente

Este proyecto se defenderá como:

> Un motor de workflow tipo BPMN 2.0 implementado en Python, aplicado al proceso real de App Detección Prod, donde cada producto próximo a vencer se modela como una instancia de workflow trazable, con tareas, recursos, workers, compuertas, incidentes, reintentos, SLAs, concurrencia y dashboard de cierre.

---

## 7. Estado

**Este documento queda aprobado y congelado como baseline del proyecto.**
