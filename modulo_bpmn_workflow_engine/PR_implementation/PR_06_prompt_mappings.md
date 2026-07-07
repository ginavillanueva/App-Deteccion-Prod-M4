# PR-06 — Prompt mappings y trazabilidad de uso de IA

**Proyecto:** App Detección Prod BPMN Workflow Engine  
**Entrega:** 08  
**Estado:** APROBADO / ENTREGA FINAL  

## 1. Objetivo

Documentar el uso de IA durante el desarrollo incremental del motor de workflow BPMN 2.0 aplicado a App Detección Prod.

El objetivo no es solo listar prompts, sino vincular cada instrucción con un resultado verificable dentro del repositorio.

## 2. Archivos modificados/agregados

| Archivo | Acción | Descripción |
|---|---|---|
| `docs/prompt_mappings.md` | Agregado | Registro principal de prompts, intención, outputs y estado. |
| `docs/README_PROMPT_MAPPINGS.md` | Agregado | Guía de revisión del entregable. |
| `docs/TRAZABILIDAD_ENTREGA_08.md` | Agregado | Matriz de trazabilidad acumulada. |
| `00_CONTROL_APROBACIONES.md` | Actualizado | Marca tests como aprobados y prompt mappings como revisión. |
| `README_REVISION.md` | Actualizado | Explica qué revisar en la Entrega 08. |

## 3. Decisiones de documentación

### 3.1 Registro resumido fiel

Los prompts extensos se documentan como resumen fiel, preservando:

- intención;
- restricciones;
- entregable solicitado;
- estado de aprobación;
- resultado producido.

### 3.2 No inclusión de razonamiento interno

El archivo documenta prompts y outputs visibles, no razonamiento interno del asistente.

### 3.3 Interpretación de aprobaciones genéricas

Cuando el usuario respondió únicamente `aprobado`, se interpretó en función del entregable que se encontraba explícitamente en revisión en el turno anterior. Esta regla queda reflejada en `00_CONTROL_APROBACIONES.md`.

## 4. Trazabilidad

| Prompt | Resultado |
|---|---|
| PM-00 | Plan maestro aprobado |
| PM-01 | PRD generado y luego aprobado |
| PM-02 | FSD generado y luego aprobado |
| PM-03 | Modelo de dominio generado y luego aprobado |
| PM-04 | Runtime generado y luego aprobado |
| PM-05 | Orquestador generado y luego aprobado |
| PM-06 | Persistencia generada y luego aprobada |
| PM-07 | Tests obligatorios generados y luego aprobados |
| PM-08 | Prompt mappings generado y aprobado |

## 5. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Que el docente perciba el uso de IA como no trazable | Se crea matriz prompt → output → estado. |
| Que las aprobaciones genéricas sean ambiguas | Se documenta la regla de interpretación por entregable pendiente. |
| Que el archivo parezca una bitácora informal | Se estructura como documento académico verificable. |
| Que se confunda prompt mapping con PRD/FSD | Se declara su alcance como evidencia de proceso, no especificación funcional. |

## 6. Criterio de aceptación

Este PR se considera aceptado cuando:

1. `docs/prompt_mappings.md` registra todos los prompts principales usados en la fase incremental.
2. Cada prompt se vincula con artefactos producidos.
3. El control de aprobaciones coincide con el estado del paquete.
4. El ZIP final incluye prompt mappings aprobado junto con los entregables previos.

## 7. Defensa ante el docente

> El prompt mapping evidencia que el uso de IA fue controlado, incremental y trazable. Cada instrucción generó un artefacto revisable y cada aprobación quedó registrada antes de avanzar al siguiente entregable.
