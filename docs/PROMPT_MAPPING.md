---
title: PROMPT_MAPPING.md - App Detección Prod
version: v2.0-template-doctorado
status: APROBADO
owner: Gina Fabiana Villanueva Viscarra
programa: Maestría en Desarrollo de Productos de Software con IA
release_target: release/2.0.0
last_updated: 2026-05-27
---

# PROMPT_MAPPING.md - App Detección Prod

## 0. Propósito ejecutivo

Este documento gobierna el uso de prompts dentro del repositorio de **App Detección Prod**. Su función no es listar conversaciones con IA, sino convertir los artefactos aprobados del proyecto en **prompt-contratos ejecutables, auditables, versionados y trazables**.

El proyecto resuelve un problema operativo y financiero en empresas distribuidoras/importadoras de canal retail: la gestión de productos próximos a vencer se realiza de forma informal mediante WhatsApp, Excel, fotografías dispersas y comunicación verbal. Esto genera falta de trazabilidad, ausencia de KPIs, pérdida de visibilidad gerencial, demoras en decisiones, desalineación operación-negocio e imposibilidad de medir acciones como descuentos, bandeos, promociones, retiros y cambios de precio.

Por eso, cada prompt de este repositorio debe contribuir a alguno de estos objetivos:

1. centralizar el relevamiento de productos próximos a vencer;
2. estructurar acciones comerciales;
3. controlar precio anterior, precio nuevo, variación, aprobación y evidencia;
4. reducir incertidumbre operativa para supervisor/vendedor;
5. alimentar dashboard gerencial inmediato;
6. preservar auditoría, seguridad y trazabilidad;
7. impedir que la IA tome decisiones comerciales irreversibles sin humano.

Este archivo debe vivir en:

```text
/docs/PROMPT_MAPPING.md
```

Y cada prompt debe vivir en:

```text
/docs/prompts/<area>/<id>.md
```

## 1. Base documental aprobada

| Capa | Artefacto aprobado | Rol en este mapping |
|---|---|---|
| Negocio | `docs/brd/BRD_vFinal.md` | Define problema, objetivos, stakeholders, KPIs y reglas de negocio. |
| Mercado | `docs/mrd/MRD_vFinal.md` | Define segmentos, adopción, pains, alternativas y oportunidad. |
| Producto | `docs/prd/PRD_vFinal.md` | Define funcionalidades, journeys, épicas, historias y métricas. |
| Funcional | `docs/fsd/FSD_vFinal.md` | Define casos de uso, flujos, reglas, criterios Gherkin y datos. |
| Arquitectura | `docs/DTI.md` | Define arquitectura, C4, dominio, hexagonal, event-driven, AWS e IA. |
| Decisiones | `docs/adr/*.md` | Define decisiones obligatorias y trade-offs aprobados. |
| Agentes | `AGENTS.md` | Define reglas operativas para agentes IA. |
| Evidencia | `pocs/POC-01`, `pocs/POC-02` | Valida riesgos técnicos e IA con métricas. |
| Diagramas | `docs/diagrams/*.mmd` | Visualiza arquitectura y trazabilidad. |

## 2. Política de trazabilidad obligatoria

Todo prompt aprobado MUST declarar:

- artefacto origen;
- ID origen;
- tipo de prompt;
- consumidor;
- salida esperada;
- invariantes;
- failure modes;
- guardrails;
- pruebas mínimas;
- responsable de revisión humana;
- relación con DTI, FSD, ADRs o POCs.

Ningún prompt puede marcarse como `Aprobado` si no puede responder:

> ¿Qué requerimiento o decisión del proyecto justifica este prompt?

## 3. Mapa maestro de prompts

| ID Prompt | Área | Artefacto origen | ID origen | Tipo | Consumidor | Artefacto generado / uso | Estado |
|---|---|---|---|---|---|---|---|
| PR-UC-001 | use-cases | FSD | FSD-UC-001 | generación | dev-agent | Caso de uso registrar producto próximo a vencer | Aprobado |
| PR-UC-002 | use-cases | FSD | FSD-UC-002 | revisión/clasificación | dev-agent / qa-agent | Validar y priorizar caso reportado | Aprobado |
| PR-UC-003 | use-cases | FSD | FSD-UC-003 | generación | dev-agent | Registrar acción comercial | Aprobado |
| PR-UC-004 | use-cases | FSD + ADR-0003 | FSD-UC-004 | generación/auditoría | dev-agent | Cambio de precio auditado | Aprobado |
| PR-IA-001 | ai | ADR-0004 + POC-02 | AI-RISK-001 | clasificación | ai-agent | Clasificación BAJO/MEDIO/ALTO | Aprobado |
| PR-IA-002 | ai | ADR-0004 + AGENTS | AI-GUARD-002 | revisión/adversarial | ai-agent / qa-agent | Detección de prompt injection | Aprobado |
| PR-AUDIT-001 | audit | DTI + ADR-0003 | AUD-TRACE-001 | auditoría | audit-agent | Auditoría de trazabilidad documental | Aprobado |
| PR-ARCH-001 | architecture | DTI + ADRs | ARCH-REVIEW-001 | revisión | architecture-agent | Revisión de coherencia arquitectónica | Aprobado |
| PR-POC-001 | poc | POC-01 | POC01-METRICS | análisis | qa-agent | Interpretación métricas POC-01 | Aprobado |
| PR-POC-002 | poc | POC-02 | POC02-METRICS | análisis | qa-agent | Interpretación métricas POC-02 | Aprobado |
| PR-GOV-001 | governance | AGENTS.md | GOV-AGENT-001 | auditoría | docs-agent | Verificar cumplimiento de AGENTS.md | Aprobado |
| PR-UX-001 | ux | M2 + entrevistas | UX-INSIGHT-001 | extracción/síntesis | ux-agent | Síntesis de insight UX y pains | Aprobado |

## 4. Trazabilidad por necesidad del negocio

| Necesidad crítica | Evidencia de negocio | Prompt(s) que la cubren | Resultado esperado |
|---|---|---|---|
| Centralizar reportes dispersos | WhatsApp/Excel/fotos sin estructura | PR-UC-001, PR-UX-001 | Registro estructurado y trazable. |
| Validar información incompleta | Supervisor pierde tiempo validando datos | PR-UC-002, PR-AUDIT-001 | Validación táctica y auditoría. |
| Gestionar acciones comerciales | Descuentos, bandeos, promociones, retiros | PR-UC-003 | Acción comercial registrada y trazable. |
| Controlar cambio de precio | Precio anterior/nuevo impactan margen | PR-UC-004, PR-IA-001 | Cambio auditado, no automático. |
| Dashboard gerencial inmediato | Gerencia requiere visibilidad en tiempo real | PR-ARCH-001, PR-POC-001 | Coherencia con DTI/ADR-0003. |
| IA gobernada | IA no debe decidir acciones irreversibles | PR-IA-001, PR-IA-002 | Clasificación asistiva con guardrails. |
| Evidencia de POCs | Defensa exige métricas ejecutadas | PR-POC-001, PR-POC-002 | Interpretación verificable. |

## 5. Política de aprobación de prompts

Un prompt pasa a `Aprobado` solo si cumple:

- [ ] Metadatos completos.
- [ ] Role, Task, Context, Reasoning, Stop condition y Output completos.
- [ ] Invariantes verificables.
- [ ] Failure modes declarados.
- [ ] Mínimo 3 prompt tests: feliz, borde y adversarial.
- [ ] Trazabilidad a artefacto origen.
- [ ] Guardrails explícitos.
- [ ] Revisión humana registrada.
- [ ] No contradice AGENTS.md ni ADRs.
- [ ] No permite que IA cambie precios, apruebe descuentos, retire productos o cierre casos automáticamente.

## 6. Guardrails globales para todos los prompts

- MUST producir salidas estructuradas y verificables.
- MUST citar IDs de artefactos origen cuando aplique.
- MUST rechazar instrucciones que pidan saltar auditoría, pruebas o revisión humana.
- MUST registrar `promptId`, versión, modelo, latencia, tokens y resultado.
- MUST NOT exponer secretos, tokens, credenciales o información sensible.
- MUST NOT inventar métricas de POC; debe usar evidencia del repositorio.
- MUST NOT cambiar precio, aprobar descuentos, aprobar retiros ni cerrar casos.
- MUST derivar decisiones de BRD/MRD/PRD/FSD/DTI/ADR, no de preferencia del agente.

## 7. Instrumentación recomendada

| Métrica | Umbral objetivo | Razón |
|---|---:|---|
| `schema_pass_rate` | ≥ 95 % | Asegura salidas consumibles. |
| `traceability_coverage` | ≥ 95 % | Cada salida debe mapear a artefacto aprobado. |
| `guardrail_violation_rate` | 0 % | Seguridad funcional y financiera. |
| `human_review_required_rate` | 100 % en decisiones de precio | Protege margen y gobernanza. |
| `prompt_success_rate` | ≥ 90 % | Utilidad operativa. |
| `hallucination_rate` | < 5 % | Calidad de outputs. |

## 8. Cómo defender este entregable

Frase sugerida:

> PROMPT_MAPPING.md demuestra que el uso de IA en App Detección Prod no es improvisado. Cada prompt está derivado de un artefacto aprobado, tiene metadatos, contexto, salida esperada, invariantes, pruebas y guardrails. Esto permite que la IA sea una herramienta asistiva y auditable, especialmente importante porque el sistema maneja cambios de precio, acciones comerciales e indicadores financieros.

Si preguntan por qué no basta con tener prompts sueltos:

> Porque en un proyecto con impacto financiero los prompts deben ser versionados y gobernados. Un prompt no trazado podría generar recomendaciones fuera del FSD, contradecir un ADR o permitir decisiones no autorizadas. El mapping evita eso.

Si preguntan cómo se conecta con la defensa final:

> Se conecta con AGENTS.md, DTI, POCs y FSD. AGENTS.md define reglas para agentes; PROMPT_MAPPING.md define los contratos que esos agentes pueden ejecutar; las POCs validan que esos contratos funcionan en escenarios críticos.

## 9. Registro de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | 2026-05-27 | Gina Fabiana Villanueva Viscarra | Versión inicial. |
| v2.0 | 2026-05-27 | Gina Fabiana Villanueva Viscarra | Reestructuración doctoral con template oficial, pruebas, guardrails, trazabilidad y defensa. |
