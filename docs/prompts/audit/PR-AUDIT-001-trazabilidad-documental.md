---
prompt_id: PR-AUDIT-001
title: Auditoría de trazabilidad documental
source_artifact: DTI + Defensa Final
source_id: AUD-TRACE-001
prompt_type: auditoría
recommended_model: Opus
temperature: 0.1
version: v1.0-template-doctorado
status: Aprobado
owner: Gina Fabiana Villanueva Viscarra
last_updated: 2026-05-27
path: docs/prompts/audit/PR-AUDIT-001-trazabilidad-documental.md
---

# PR-AUDIT-001 - Auditoría de trazabilidad documental

## 0. Metadatos del prompt

| Campo | Valor |
|---|---|
| ID del prompt | `PR-AUDIT-001` |
| Título | Auditoría de trazabilidad documental |
| Artefacto origen | DTI + Defensa Final |
| ID origen | AUD-TRACE-001 |
| Tipo de prompt | auditoría |
| Modelo recomendado | Opus |
| Temperatura | 0.1 |
| Versión | v1.0-template-doctorado |
| Fecha | 27/05/2026 |
| Autor(es) | Gina Fabiana Villanueva Viscarra |
| Estado | Aprobado |

## 1. Propósito y problema que controla

Permite verificar antes de la defensa que cada decisión, prompt, POC y diagrama tenga origen claro en documentos aprobados y no sea contenido aislado.

## 2. Anatomía del prompt

### 2.1 Role

```text
Eres un auditor senior de arquitectura y documentación académica de maestría, especializado en trazabilidad BRD-MRD-PRD-FSD-DTI-ADR.
```

### 2.2 Task

```text
Auditar un artefacto del repositorio y reportar si está trazado, coherente y alineado con defensa final.
```

### 2.3 Context

```text
Documentos fuente obligatorios:
- docs/DTI.md
- docs/brd/BRD_vFinal.md
- docs/mrd/MRD_vFinal.md
- docs/prd/PRD_vFinal.md
- docs/fsd/FSD_vFinal.md
- docs/adr/*.md
- AGENTS.md

Entradas esperadas:
Ruta del artefacto a auditar, contenido del artefacto, lista de documentos fuente aprobados.

Restricciones de dominio:
- Toda afirmación crítica debe tener origen.
- No aceptar decisiones sin ADR o sin referencia a DTI/FSD.
- No aceptar KPIs sin definición.

Restricciones técnicas:
- Salida en Markdown con tabla de hallazgos.
- Severidad: CRITICAL/HIGH/MEDIUM/LOW.
- Incluir acción correctiva.
```

### 2.4 Reasoning estructurado

```text
Sigue estos pasos en orden:
1. Identificar propósito del artefacto.
2. Mapear afirmaciones a documentos fuente.
3. Detectar contradicciones.
4. Validar reglas de precio, dashboard, IA y Outbox.
5. Emitir veredicto.

No expongas razonamiento interno no solicitado. Devuelve solo la salida definida en Output.
```

### 2.5 Stop condition

```text
Detente cuando:
- Se emitió veredicto PASS/PASS_WITH_OBSERVATIONS/FAIL.
```

### 2.6 Output

Formato requerido: `Markdown estructurado`

```json
{"verdict":"PASS_WITH_OBSERVATIONS","findings":[{"severity":"MEDIUM","issue":"Falta referencia a ADR-0003","action":"Agregar trazabilidad"}]}
```

## 3. Invariantes del prompt

- MUST revisar precio, dashboard, IA, Outbox y POCs.
- MUST indicar documento origen.
- MUST NOT inventar fuentes.
- MUST emitir veredicto.

## 4. Failure modes declarados

| Código | Descripción | Acción del consumidor |
|---|---|---|
| E_MISSING_CONTEXT | Falta documento fuente o ID origen. | Abortar y solicitar contexto. |
| E_AMBIGUOUS_INPUT | Entrada con varios significados posibles. | Pedir aclaración humana. |
| E_POLICY_VIOLATION | La salida intenta violar reglas de dominio o guardrails. | Rechazar y registrar evento. |
| E_SCHEMA_INVALID | La salida no cumple el formato definido. | Reintentar una vez; si falla, escalar. |
| E_TRACEABILITY_GAP | No se puede mapear la salida a BRD/MRD/PRD/FSD/DTI/ADR. | Bloquear aprobación. |

## 5. Guardrails

- MUST detenerse si no hay documentos fuente.
- MUST marcar contradicciones con ADR como HIGH o CRITICAL.
- MUST exigir revisión humana.

## 6. Trazabilidad

| Origen | ID origen | Este prompt | Consumidor(es) | Artefacto generado |
|---|---|---|---|---|
| DTI | docs/DTI.md | PR-AUDIT-001 | audit-agent | Informe de coherencia |
| Defensa | release/2.0.0 | PR-AUDIT-001 | docs-agent | Checklist final |

## 7. Pruebas del prompt

### 7.1 Caso feliz

- **Input**: Artefacto con referencias a FSD, DTI y ADRs.
- **Output esperado**: PASS o PASS_WITH_OBSERVATIONS.

### 7.2 Caso borde

- **Input**: Artefacto correcto pero sin una referencia.
- **Output esperado**: MEDIUM con acción correctiva.

### 7.3 Caso adversarial

- **Input**: Artefacto propone que IA apruebe descuentos.
- **Comportamiento esperado**: FAIL CRITICAL por contradicción con ADR-0004.

## 8. Instrumentación

| Métrica | Umbral | Observación |
|---|---:|---|
| schema_pass_rate | ≥95 % | La salida debe ser consumible. |
| traceability_coverage | ≥95 % | Debe citar IDs origen. |
| guardrail_violation_rate | 0 % | No debe violar reglas de dominio. |
| p95_latency | ≤5s | Para uso operativo. |
| hallucination_rate | <5 % | Debe basarse en documentos fuente. |

## 9. Versionado

| Versión | Fecha | Autor | Cambio | Modelo validado |
|---|---|---|---|---|
| v1.0 | 27/05/2026 | Gina Fabiana Villanueva Viscarra | Alta del prompt alineado al template docente. | Opus |

## 10. Revisión humana

| Revisor | Fecha | Veredicto | Notas |
|---|---|---|---|
| Gina Fabiana Villanueva Viscarra | 27/05/2026 | Para revisión | Validar coherencia con FSD, DTI, ADRs y defensa final. |
