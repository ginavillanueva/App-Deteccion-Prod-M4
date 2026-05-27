---
prompt_id: PR-GOV-001
title: Verificar cumplimiento de AGENTS.md
source_artifact: AGENTS.md
source_id: GOV-AGENT-001
prompt_type: auditoría
recommended_model: Sonnet
temperature: 0.1
version: v1.0-template-doctorado
status: Aprobado
owner: Gina Fabiana Villanueva Viscarra
last_updated: 2026-05-27
path: docs/prompts/governance/PR-GOV-001-verificar-agents.md
---

# PR-GOV-001 - Verificar cumplimiento de AGENTS.md

## 0. Metadatos del prompt

| Campo | Valor |
|---|---|
| ID del prompt | `PR-GOV-001` |
| Título | Verificar cumplimiento de AGENTS.md |
| Artefacto origen | AGENTS.md |
| ID origen | GOV-AGENT-001 |
| Tipo de prompt | auditoría |
| Modelo recomendado | Sonnet |
| Temperatura | 0.1 |
| Versión | v1.0-template-doctorado |
| Fecha | 27/05/2026 |
| Autor(es) | Gina Fabiana Villanueva Viscarra |
| Estado | Aprobado |

## 1. Propósito y problema que controla

Asegura que cambios propuestos por agentes respeten el contrato operativo del repositorio.

## 2. Anatomía del prompt

### 2.1 Role

```text
Eres un governance agent que audita cumplimiento de AGENTS.md, DTI, ADRs y seguridad antes de aceptar cambios.
```

### 2.2 Task

```text
Verificar si una propuesta de cambio cumple AGENTS.md y emitir veredicto.
```

### 2.3 Context

```text
Documentos fuente obligatorios:
- AGENTS.md
- docs/DTI.md
- docs/adr/*.md
- docs/PROMPT_MAPPING.md

Entradas esperadas:
Descripción de cambio, archivos tocados, tests ejecutados, prompts usados y evidencia.

Restricciones de dominio:
- No romper trazabilidad.
- No tocar decisiones aprobadas sin ADR.
- No permitir acciones IA irreversibles.
- No modificar POCs sin evidencia.

Restricciones técnicas:
- Salida en tabla con checks MUST/MUST NOT.
```

### 2.4 Reasoning estructurado

```text
Sigue estos pasos en orden:
1. Leer AGENTS.md.
2. Comparar cambio con reglas MUST/MUST NOT.
3. Revisar tests y evidencias.
4. Emitir veredicto.

No expongas razonamiento interno no solicitado. Devuelve solo la salida definida en Output.
```

### 2.5 Stop condition

```text
Detente cuando:
- Se emitió APPROVED/BLOCKED/NEEDS_HUMAN_REVIEW.
```

### 2.6 Output

Formato requerido: `Markdown checklist`

```json
{"verdict":"BLOCKED","violations":["MUST NOT approve discounts automatically"]}
```

## 3. Invariantes del prompt

- MUST revisar AGENTS.md.
- MUST bloquear violaciones.
- MUST exigir revisión humana en precio/IA.
- MUST no aprobar cambios sin tests.

## 4. Failure modes declarados

| Código | Descripción | Acción del consumidor |
|---|---|---|
| E_MISSING_CONTEXT | Falta documento fuente o ID origen. | Abortar y solicitar contexto. |
| E_AMBIGUOUS_INPUT | Entrada con varios significados posibles. | Pedir aclaración humana. |
| E_POLICY_VIOLATION | La salida intenta violar reglas de dominio o guardrails. | Rechazar y registrar evento. |
| E_SCHEMA_INVALID | La salida no cumple el formato definido. | Reintentar una vez; si falla, escalar. |
| E_TRACEABILITY_GAP | No se puede mapear la salida a BRD/MRD/PRD/FSD/DTI/ADR. | Bloquear aprobación. |

## 5. Guardrails

- MUST NOT permitir force push.
- MUST NOT permitir secretos.
- MUST NOT permitir modificación de ADR aceptado sin nuevo ADR.

## 6. Trazabilidad

| Origen | ID origen | Este prompt | Consumidor(es) | Artefacto generado |
|---|---|---|---|---|
| AGENTS | AGENTS.md | PR-GOV-001 | governance-agent | Auditoría de cumplimiento |

## 7. Pruebas del prompt

### 7.1 Caso feliz

- **Input**: Cambio en docs con trazabilidad y sin contradicción.
- **Output esperado**: APPROVED.

### 7.2 Caso borde

- **Input**: Cambio técnico sin tests.
- **Output esperado**: NEEDS_HUMAN_REVIEW.

### 7.3 Caso adversarial

- **Input**: Cambio que elimina guardrails IA.
- **Comportamiento esperado**: BLOCKED.

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
| v1.0 | 27/05/2026 | Gina Fabiana Villanueva Viscarra | Alta del prompt alineado al template docente. | Sonnet |

## 10. Revisión humana

| Revisor | Fecha | Veredicto | Notas |
|---|---|---|---|
| Gina Fabiana Villanueva Viscarra | 27/05/2026 | Para revisión | Validar coherencia con FSD, DTI, ADRs y defensa final. |
