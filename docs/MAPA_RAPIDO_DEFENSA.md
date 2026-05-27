# MAPA_RAPIDO_DEFENSA.md — App Detección Prod

## 1. Propósito

Este documento permite ubicar rápidamente dónde se evidencia cada concepto crítico del proyecto, qué archivo lo respalda, qué sección/documento lo conecta y qué métrica demuestra su impacto. Está diseñado para responder con rapidez durante la defensa final y para reforzar la trazabilidad documental.

## 2. Mapa rápido símbolo → archivo/sección → métrica

| Símbolo / concepto | Archivo principal | Sección o evidencia asociada | Métrica antes / después esperada |
|---|---|---|---|
| Problema de negocio | `docs/brd/BRD_vFinal.md` | Problema, objetivos, stakeholders, KPIs | Antes: reportes dispersos. Después: trazabilidad centralizada. |
| Mercado y usuarios | `docs/mrd/MRD_vFinal.md` | Segmentos, pains, JTBD, adopción | Antes: WhatsApp/Excel. Después: sistema único por rol. |
| Requerimientos de producto | `docs/prd/PRD_vFinal.md` | Épicas, historias, roadmap funcional | Antes: decisiones reactivas. Después: flujo priorizado y medible. |
| Caso de uso registrar producto | `docs/fsd/FSD_vFinal.md` | FSD-UC-001 | Antes: foto/mensaje informal. Después: producto, lote, vencimiento, evidencia y cantidad estructurada. |
| Caso de uso cambio de precio | `docs/fsd/FSD_vFinal.md` + `docs/adr/0003-*.md` | Cambio de precio auditado + evento `PriceChanged.v1` | Antes: precio no trazado. Después: precio anterior/nuevo, delta, responsable y aprobación. |
| Dashboard gerencial inmediato | `docs/DTI.md` + `docs/adr/0003-*.md` | Política de consistencia transaccional | Antes: gerencia ve información tardía. Después: KPIs críticos actualizados al confirmar transacción. |
| Monolito modular evolutivo | `docs/adr/0001-*.md` | Decisión macroarquitectónica | Reduce sobreingeniería y prepara evolución por bounded contexts. |
| Arquitectura hexagonal | `docs/adr/0002-*.md` + `docs/diagrams/04_*.mmd` | Core, puertos, adaptadores | Evita acoplar dominio a UI, base de datos, AWS o IA. |
| Event-driven + Outbox | `docs/adr/0003-*.md` + `pocs/POC-01/` | Outbox transaccional | POC-01: eventos generados y consistencia dashboard/casos/eventos. |
| IA gobernada | `docs/adr/0004-*.md` + `pocs/POC-02/` | Scoring BAJO/MEDIO/ALTO + guardrails | POC-02: accuracy, bloqueo prompt injection, 0 acciones irreversibles automáticas. |
| AWS / cloud-ready | `docs/adr/0005-*.md` + `docs/diagrams/10_*.mmd` | RDS, S3, EventBridge/SQS/SNS, CloudWatch | Prepara escalabilidad, observabilidad y seguridad por capa. |
| Agentes IA | `AGENTS.md` | Reglas MUST/MUST NOT | Evita que agentes rompan DTI, ADRs, pruebas o decisiones humanas. |
| Prompt Mapping | `docs/PROMPT_MAPPING.md` + `docs/prompts/` | Prompt-contratos PR-* | Cada prompt tiene origen, contexto, salida, guardrails y pruebas. |
| POC-01 | `pocs/POC-01/` | Registro + dashboard + Outbox | Valida flujo transaccional crítico. |
| POC-02 | `pocs/POC-02/` | IA + scoring + guardrails | Valida clasificación y control humano. |
| Diagramas versionados | `docs/diagrams/*.mmd` | C4, hexagonal, dominio, secuencias, AWS, IA | Cumple ≥8 diagramas Mermaid versionados. |
| Roadmap | `docs/roadmap.md` | H0–H4 | Evoluciona de defensa documental a MVP, piloto, cloud-ready y escalamiento. |
| Aportes | `docs/aportes/release-2.0.0.md` | Tareas verificables | Evidencia contribución por artefacto y release. |

## 3. Métricas antes/después de mayor valor en defensa

| Dolor original | Métrica de evaluación | Evidencia en entrega |
|---|---|---|
| Reportes por WhatsApp/Excel | % registros estructurados | BRD, FSD-UC-001, POC-01 |
| Falta de control de precio | % cambios con precio anterior/nuevo/aprobación | FSD, ADR-0003, POC-01, PROMPT_MAPPING |
| Gerencia sin visibilidad | Frescura del dashboard / KPIs críticos | ADR-0003, DTI, POC-01 |
| Supervisión valida manualmente | Tiempo de validación / casos con evidencia completa | FSD, roadmap, POC-01 |
| IA riesgosa | Guardrail violation rate / human review | ADR-0004, POC-02, AGENTS |
| Arquitectura no defendible | ADRs + trade-offs + diagramas | ADR-0001..0005, DTI, diagrams |

## 4. Frase de defensa

La entrega no es una colección de documentos; es una cadena trazable donde cada decisión técnica responde a un dolor de negocio y cada POC valida un riesgo arquitectónico o funcional crítico.
