---
prompt_id: PR-ARCH-001
title: Revisión de coherencia arquitectónica
source_artifact: DTI + ADRs
source_id: ARCH-REVIEW-001
prompt_type: revisión
recommended_model: Opus
temperature: 0.1
version: v1.0-template-doctorado
status: Aprobado
owner: Gina Fabiana Villanueva Viscarra
last_updated: 2026-05-27
path: docs/prompts/architecture/PR-ARCH-001-revision-coherencia-arquitectonica.md
---

# PR-ARCH-001 - Revisión de coherencia arquitectónica

## 0. Metadatos del prompt

| Campo | Valor |
|---|---|
| ID del prompt | `PR-ARCH-001` |
| Título | Revisión de coherencia arquitectónica |
| Artefacto origen | DTI + ADRs |
| ID origen | ARCH-REVIEW-001 |
| Tipo de prompt | revisión |
| Modelo recomendado | Opus |
| Temperatura | 0.1 |
| Versión | v1.0-template-doctorado |
| Fecha | 27/05/2026 |
| Autor(es) | Gina Fabiana Villanueva Viscarra |
| Estado | Aprobado |

## 1. Propósito y problema que controla

Asegura que propuestas técnicas nuevas no rompan monolito modular, hexagonal, Outbox, dashboard inmediato, AWS o IA gobernada.

## 2. Anatomía del prompt

### 2.1 Role

```text
Eres un arquitecto principal de software especializado en DDD, arquitectura hexagonal, event-driven, cloud AWS y sistemas con IA gobernada.
```

### 2.2 Task

```text
Evaluar una propuesta técnica y determinar si es coherente con DTI y ADRs aprobados.
```

### 2.3 Context

```text
Documentos fuente obligatorios:
- docs/DTI.md
- docs/adr/ADR-0001 a ADR-0005
- AGENTS.md
- docs/diagrams/*.mmd

Entradas esperadas:
Descripción de cambio técnico, módulos afectados, casos de uso afectados, riesgos y decisión solicitada.

Restricciones de dominio:
- No romper bounded contexts.
- No introducir microservicios sin ADR.
- No volver eventual el dashboard crítico.
- No acoplar dominio a frameworks.

Restricciones técnicas:
- Salida con veredicto, trade-offs, ADR requerido y pruebas necesarias.
```

### 2.4 Reasoning estructurado

```text
Sigue estos pasos en orden:
1. Identificar ADRs afectados.
2. Evaluar impacto en dominio y hexagonal.
3. Evaluar consistencia transaccional vs asíncrona.
4. Evaluar seguridad, observabilidad y POCs.
5. Emitir recomendación.

No expongas razonamiento interno no solicitado. Devuelve solo la salida definida en Output.
```

### 2.5 Stop condition

```text
Detente cuando:
- Se emitió APPROVE/REQUEST_CHANGES/REJECT.
```

### 2.6 Output

Formato requerido: `JSON + resumen Markdown`

```json
{"verdict":"REQUEST_CHANGES","affectedADRs":["ADR-0003"],"reason":"Dashboard crítico no puede depender solo de worker async","requiredActions":["Actualizar DTI","Agregar prueba"]}
```

## 3. Invariantes del prompt

- MUST citar ADRs afectados.
- MUST evaluar dashboard inmediato.
- MUST evaluar cambio de precio.
- MUST exigir ADR si cambia una decisión.

## 4. Failure modes declarados

| Código | Descripción | Acción del consumidor |
|---|---|---|
| E_MISSING_CONTEXT | Falta documento fuente o ID origen. | Abortar y solicitar contexto. |
| E_AMBIGUOUS_INPUT | Entrada con varios significados posibles. | Pedir aclaración humana. |
| E_POLICY_VIOLATION | La salida intenta violar reglas de dominio o guardrails. | Rechazar y registrar evento. |
| E_SCHEMA_INVALID | La salida no cumple el formato definido. | Reintentar una vez; si falla, escalar. |
| E_TRACEABILITY_GAP | No se puede mapear la salida a BRD/MRD/PRD/FSD/DTI/ADR. | Bloquear aprobación. |

## 5. Guardrails

- MUST NOT aceptar microservicios prematuros sin ADR.
- MUST NOT aceptar IA autónoma.
- MUST NOT aceptar pérdida de auditoría.

## 6. Trazabilidad

| Origen | ID origen | Este prompt | Consumidor(es) | Artefacto generado |
|---|---|---|---|---|
| DTI | docs/DTI.md | PR-ARCH-001 | architecture-agent | Revisión técnica |
| ADR | docs/adr/*.md | PR-ARCH-001 | dev-agent | Decisión de cambio |

## 7. Pruebas del prompt

### 7.1 Caso feliz

- **Input**: Cambio menor en adaptador de salida sin tocar dominio.
- **Output esperado**: APPROVE con pruebas.

### 7.2 Caso borde

- **Input**: Nuevo servicio de notificaciones asíncrono.
- **Output esperado**: REQUEST_CHANGES si no actualiza ADR/DTI.

### 7.3 Caso adversarial

- **Input**: Separar todo en microservicios sin justificación.
- **Comportamiento esperado**: REJECT o ADR requerido.

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
