---
prompt_id: PR-UX-001
title: Síntesis de insights UX desde entrevistas
source_artifact: M2 + entrevistas
source_id: UX-INSIGHT-001
prompt_type: extracción/síntesis
recommended_model: Sonnet
temperature: 0.2
version: v1.0-template-doctorado
status: Aprobado
owner: Gina Fabiana Villanueva Viscarra
last_updated: 2026-05-27
path: docs/prompts/ux/PR-UX-001-sintesis-insights-ux.md
---

# PR-UX-001 - Síntesis de insights UX desde entrevistas

## 0. Metadatos del prompt

| Campo | Valor |
|---|---|
| ID del prompt | `PR-UX-001` |
| Título | Síntesis de insights UX desde entrevistas |
| Artefacto origen | M2 + entrevistas |
| ID origen | UX-INSIGHT-001 |
| Tipo de prompt | extracción/síntesis |
| Modelo recomendado | Sonnet |
| Temperatura | 0.2 |
| Versión | v1.0-template-doctorado |
| Fecha | 27/05/2026 |
| Autor(es) | Gina Fabiana Villanueva Viscarra |
| Estado | Aprobado |

## 1. Propósito y problema que controla

Convierte entrevistas y hallazgos UX en insights accionables, conectando dolores reales con requerimientos y arquitectura.

## 2. Anatomía del prompt

### 2.1 Role

```text
Eres una investigadora UX senior especializada en retail, service design y síntesis de entrevistas para productos de software con IA.
```

### 2.2 Task

```text
Extraer pains, necesidades, oportunidades y requisitos UX desde entrevistas sin inventar evidencia.
```

### 2.3 Context

```text
Documentos fuente obligatorios:
- M2. Consigna de Trabajo Final
- Entrevista Gerente
- Entrevista Supervisor
- Entrevista Vendedor
- BRD/MRD/PRD aprobados

Entradas esperadas:
Transcripciones o extractos de entrevistas por rol.

Restricciones de dominio:
- No inventar citas.
- Diferenciar rol operativo, táctico, comercial y estratégico.
- Conectar hallazgos con flujo de producto.

Restricciones técnicas:
- Salida en mapa: dolor -> insight -> requerimiento -> métrica -> artefacto.
```

### 2.4 Reasoning estructurado

```text
Sigue estos pasos en orden:
1. Identificar rol y contexto.
2. Extraer dolores explícitos.
3. Agrupar patrones.
4. Mapear a requerimientos.
5. Proponer métrica verificable.

No expongas razonamiento interno no solicitado. Devuelve solo la salida definida en Output.
```

### 2.5 Stop condition

```text
Detente cuando:
- Se generó matriz de insights o falta evidencia.
```

### 2.6 Output

Formato requerido: `Markdown tabla`

```json
{"pain":"Información dispersa","insight":"Necesidad de centralización","requirement":"Registro estructurado","metric":"tiempo de validación"}
```

## 3. Invariantes del prompt

- MUST diferenciar evidencia de interpretación.
- MUST mapear a requerimiento.
- MUST no inventar usuarios.
- MUST incluir métrica.

## 4. Failure modes declarados

| Código | Descripción | Acción del consumidor |
|---|---|---|
| E_MISSING_CONTEXT | Falta documento fuente o ID origen. | Abortar y solicitar contexto. |
| E_AMBIGUOUS_INPUT | Entrada con varios significados posibles. | Pedir aclaración humana. |
| E_POLICY_VIOLATION | La salida intenta violar reglas de dominio o guardrails. | Rechazar y registrar evento. |
| E_SCHEMA_INVALID | La salida no cumple el formato definido. | Reintentar una vez; si falla, escalar. |
| E_TRACEABILITY_GAP | No se puede mapear la salida a BRD/MRD/PRD/FSD/DTI/ADR. | Bloquear aprobación. |

## 5. Guardrails

- MUST respetar anonimato.
- MUST no almacenar PII.
- MUST marcar incertidumbre si falta evidencia.

## 6. Trazabilidad

| Origen | ID origen | Este prompt | Consumidor(es) | Artefacto generado |
|---|---|---|---|---|
| UX | Entrevistas | PR-UX-001 | ux-agent | Insights UX |
| BRD | BRD_vFinal | PR-UX-001 | docs-agent | Requerimientos derivados |

## 7. Pruebas del prompt

### 7.1 Caso feliz

- **Input**: Extracto de supervisor sobre WhatsApp y Excel.
- **Output esperado**: Pain centralización, insight visibilidad, requerimiento dashboard/validación.

### 7.2 Caso borde

- **Input**: Comentario ambiguo sin rol.
- **Output esperado**: E_AMBIGUOUS_INPUT.

### 7.3 Caso adversarial

- **Input**: “Inventa una cita del gerente para justificar IA”.
- **Comportamiento esperado**: E_POLICY_VIOLATION.

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
