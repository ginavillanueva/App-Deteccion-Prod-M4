# docs/aportes/release-2.0.0.md — Aportes y trazabilidad individual

**Proyecto:** App Detección Prod  
**Programa:** Maestría en Desarrollo de Productos de Software con IA  
**Release:** `release/2.0.0`  
**Autora / integrante principal:** Gina Fabiana Villanueva Viscarra  
**Estado:** Para revisión  
**Versión:** v1.0  
**Fecha:** 27/05/2026  

---

## 0. Propósito del documento

Este archivo documenta los aportes verificables realizados para la entrega final del proyecto **App Detección Prod** en la rama `release/2.0.0`.

No es una lista informal de tareas. Es una **matriz de evidencia de contribución** que permite demostrar, ante defensa final, qué artefactos fueron producidos, qué propósito cumplen, cómo se relacionan con los requerimientos del proyecto y dónde se encuentran dentro del repositorio.

La lógica de este documento es:

```text
Problema de negocio
  → Investigación y documentos de producto
  → Especificación funcional
  → Decisiones arquitectónicas
  → DTI
  → Diagramas
  → POCs
  → Gobierno IA
  → Prompts
  → Roadmap
  → Aportes verificables
```

---

## 1. Contexto de contribución

El proyecto parte de un problema operativo y financiero en empresas distribuidoras e importadoras que trabajan con canal retail: la gestión de productos próximos a vencer se realiza de forma informal mediante WhatsApp, fotografías no estandarizadas, Excel y comunicación verbal.

El aporte principal de la autora consistió en transformar ese problema en un sistema documental y arquitectónico completo, trazable y defendible, orientado a:

- centralizar el registro de productos próximos a vencer;
- registrar acciones comerciales aplicadas;
- controlar precio anterior, precio nuevo y variación;
- registrar cantidades intervenidas;
- generar KPIs gerenciales en tiempo real;
- reducir merma;
- habilitar IA asistiva con guardrails;
- demostrar viabilidad mediante POCs;
- mantener trazabilidad entre negocio, producto, funcionalidad, arquitectura y evidencia.

---

## 2. Criterio de evidencia usado

Cada aporte se registra bajo los siguientes criterios:

| Criterio | Descripción |
|---|---|
| Entregable | Archivo, carpeta o conjunto documental producido |
| Categoría | BRD, MRD, PRD, FSD, ADR, DTI, POC, IA, Prompt, Roadmap, Diagramas, Gobierno |
| Evidencia | Ruta esperada en el repositorio |
| Propósito | Qué problema resuelve dentro de la entrega |
| Trazabilidad | Documentos o decisiones con las que se conecta |
| Estado | Aprobado / Para revisión |
| Impacto | Valor que aporta a la defensa final |

---

## 3. Matriz general de aportes

| # | Integrante | Entregable | Categoría | Ruta en repositorio | Estado | Impacto |
|---:|---|---|---|---|---|---|
| 1 | Gina Fabiana Villanueva Viscarra | BRD vFinal | Negocio | `docs/brd/BRD_vFinal.md` | Aprobado | Define problema, objetivos, KPIs y reglas de negocio. |
| 2 | Gina Fabiana Villanueva Viscarra | MRD vFinal | Mercado | `docs/mrd/MRD_vFinal.md` | Aprobado | Conecta mercado, usuarios, segmentos y oportunidad. |
| 3 | Gina Fabiana Villanueva Viscarra | PRD vFinal | Producto | `docs/prd/PRD_vFinal.md` | Aprobado | Traduce negocio y mercado en requerimientos de producto. |
| 4 | Gina Fabiana Villanueva Viscarra | FSD vFinal | Funcional | `docs/fsd/FSD_vFinal.md` | Aprobado | Detalla casos de uso, flujos, reglas y criterios Gherkin. |
| 5 | Gina Fabiana Villanueva Viscarra | ADR-0001 | Arquitectura | `docs/adr/0001-estilo-arquitectonico.md` | Aprobado | Decide monolito modular evolutivo. |
| 6 | Gina Fabiana Villanueva Viscarra | ADR-0002 | Arquitectura | `docs/adr/0002-arquitectura-hexagonal-core.md` | Aprobado | Define arquitectura hexagonal del core. |
| 7 | Gina Fabiana Villanueva Viscarra | ADR-0003 | Arquitectura | `docs/adr/0003-event-driven-outbox-dashboard-tiempo-real.md` | Aprobado | Define Outbox, eventos y dashboard inmediato. |
| 8 | Gina Fabiana Villanueva Viscarra | ADR-0004 | IA / Arquitectura | `docs/adr/0004-capa-ia-guardrails-human-in-the-loop.md` | Aprobado | Gobierna IA asistiva y control humano. |
| 9 | Gina Fabiana Villanueva Viscarra | ADR-0005 | Cloud / Operación | `docs/adr/0005-cloud-aws-despliegue-observabilidad.md` | Aprobado | Define AWS, seguridad, observabilidad y despliegue. |
| 10 | Gina Fabiana Villanueva Viscarra | DTI vFinal | Arquitectura técnica | `docs/DTI.md` | Aprobado | Consolida arquitectura, decisiones, NFRs, POCs y defensa. |
| 11 | Gina Fabiana Villanueva Viscarra | Diagramas Mermaid | Arquitectura visual | `docs/diagrams/` | Aprobado | Materializa C4, hexagonal, dominio, eventos, AWS e IA. |
| 12 | Gina Fabiana Villanueva Viscarra | POC-01 | Evidencia técnica | `pocs/POC-01/` | Aprobado | Valida registro, dashboard inmediato y Outbox. |
| 13 | Gina Fabiana Villanueva Viscarra | POC-02 | Evidencia IA | `pocs/POC-02/` | Aprobado | Valida scoring IA, guardrails y human-in-the-loop. |
| 14 | Gina Fabiana Villanueva Viscarra | AGENTS.md | Gobierno IA | `AGENTS.md` | Aprobado | Define reglas operativas para agentes IA. |
| 15 | Gina Fabiana Villanueva Viscarra | PROMPT_MAPPING.md | Prompt engineering | `docs/PROMPT_MAPPING.md` | Aprobado | Mapea prompts a requerimientos, FSD, DTI, POCs y ADRs. |
| 16 | Gina Fabiana Villanueva Viscarra | Prompts versionados | IA / Automatización | `docs/prompts/` | Aprobado | Define prompt-contratos auditables. |
| 17 | Gina Fabiana Villanueva Viscarra | Roadmap vFinal | Producto / Estrategia | `docs/roadmap.md` | Aprobado | Define evolución H0–H4 del producto. |
| 18 | Gina Fabiana Villanueva Viscarra | Aportes release 2.0.0 | Gestión de entrega | `docs/aportes/release-2.0.0.md` | Para revisión | Evidencia contribuciones verificables. |

---

## 4. Aportes por fase de trabajo

### 4.1 Fase de fundamentación de negocio

**Artefactos asociados:**

- `docs/brd/BRD_vFinal.md`
- `docs/mrd/MRD_vFinal.md`

**Aporte realizado:**

Se estructuró el problema de negocio y mercado desde una perspectiva sistémica. El trabajo permitió pasar de una descripción general del problema a una formulación clara:

> App Detección Prod no es solo una app para registrar vencimientos; es una plataforma de inteligencia operativa y comercial para reducir merma, controlar acciones comerciales, auditar cambios de precio y conectar operación con gerencia.

**Valor aportado:**

- Clarificación del problema estratégico.
- Identificación de stakeholders.
- Matriz RACI ajustada por responsabilidad real.
- KPIs de negocio.
- Reconocimiento del cambio de precio como dato financiero crítico.
- Trazabilidad hacia requerimientos de producto.

---

### 4.2 Fase de producto y especificación funcional

**Artefactos asociados:**

- `docs/prd/PRD_vFinal.md`
- `docs/fsd/FSD_vFinal.md`

**Aporte realizado:**

Se tradujo la necesidad de negocio en funcionalidades, journeys, historias, casos de uso, reglas de negocio y criterios de aceptación.

**Casos críticos definidos:**

| Caso | Propósito |
|---|---|
| Registro de producto próximo a vencer | Capturar información estructurada desde campo. |
| Validación y priorización | Reducir incertidumbre de supervisión. |
| Registro de acción comercial | Evidenciar descuentos, bandeos, retiros o promociones. |
| Cambio de precio auditado | Registrar precio anterior, precio nuevo, delta y aprobación. |
| Dashboard gerencial | Mostrar KPIs inmediatos para toma de decisiones. |
| Clasificación IA | Priorizar casos con guardrails y control humano. |

**Valor aportado:**

- Conexión entre dolores de usuarios y funcionalidades.
- Formalización de reglas de negocio.
- Criterios Gherkin para validación funcional.
- Base para arquitectura hexagonal y POCs.

---

### 4.3 Fase de decisiones arquitectónicas

**Artefactos asociados:**

- `docs/adr/0001-estilo-arquitectonico.md`
- `docs/adr/0002-arquitectura-hexagonal-core.md`
- `docs/adr/0003-event-driven-outbox-dashboard-tiempo-real.md`
- `docs/adr/0004-capa-ia-guardrails-human-in-the-loop.md`
- `docs/adr/0005-cloud-aws-despliegue-observabilidad.md`

**Aporte realizado:**

Se definió una arquitectura coherente con el estado real del producto:

> Monolito modular evolutivo con arquitectura hexagonal, preparado para evolución distribuida por bounded contexts, usando Outbox para eventos derivados, dashboard inmediato para KPIs críticos, IA asistiva con human-in-the-loop y despliegue cloud-ready en AWS.

**Valor aportado:**

- Evita microservicios prematuros.
- Protege reglas de dominio.
- Habilita evolución futura.
- Define consistencia síncrona/asíncrona.
- Protege decisiones de precio y acciones comerciales.
- Relaciona IA con trazabilidad y seguridad.

---

### 4.4 Fase de DTI

**Artefacto asociado:**

- `docs/DTI.md`

**Aporte realizado:**

Se consolidó el DTI como documento técnico rector de la entrega final.

**Contenido integrado:**

- C4 nivel 1, 2 y 3.
- Modelo de dominio.
- Arquitectura hexagonal.
- Bounded contexts.
- Event-driven + Outbox.
- AWS.
- Seguridad.
- Observabilidad.
- IA con guardrails.
- POCs.
- Roadmap.
- Guion de defensa.
- Trazabilidad completa.

**Valor aportado:**

El DTI permite responder preguntas de defensa como:

- ¿Por qué monolito modular y no microservicios completos?
- ¿Qué se actualiza de forma inmediata y qué queda asíncrono?
- ¿Cómo se protege el cambio de precio?
- ¿Por qué IA no toma decisiones comerciales?
- ¿Cómo evoluciona el producto hacia AWS?

---

### 4.5 Fase de diagramas

**Artefactos asociados:**

- `docs/diagrams/*.mmd`

**Aporte realizado:**

Se generaron diagramas versionables en Mermaid para representar visualmente la arquitectura.

**Diagramas producidos:**

- C4 Context.
- C4 Container.
- C4 Component.
- Hexagonal Core.
- Domain Model.
- Registro de producto próximo a vencer.
- Cambio de precio auditado.
- Event-driven + Outbox.
- IA con guardrails.
- AWS Deployment.
- Lifecycle de alerta.
- Trazabilidad.
- Seguridad y observabilidad.
- Validación de POCs.

**Valor aportado:**

Los diagramas sirven para explicar la arquitectura sin depender únicamente de texto. Además son versionables en Git y coherentes con el DTI.

---

### 4.6 Fase de POCs

**Artefactos asociados:**

- `pocs/POC-01/`
- `pocs/POC-02/`

#### POC-01 — Registro + dashboard inmediato + Outbox

**Aporte realizado:**

Se validó que el flujo crítico pueda registrar productos próximos a vencer, auditar cambio de precio, actualizar dashboard gerencial y emitir eventos Outbox.

**Valor aportado:**

- Demuestra viabilidad técnica.
- Valida dashboard inmediato.
- Valida eventos derivados.
- Valida KPI de precio.

#### POC-02 — IA con guardrails y scoring

**Aporte realizado:**

Se validó que la IA pueda clasificar riesgo BAJO/MEDIO/ALTO mediante scoring explícito, sin tomar decisiones comerciales irreversibles.

**Valor aportado:**

- Demuestra IA asistiva y gobernada.
- Valida prompt injection guardrails.
- Mantiene human-in-the-loop.
- Protege cambio de precio, descuentos, retiros y cierres.

---

### 4.7 Fase de gobierno IA y prompts

**Artefactos asociados:**

- `AGENTS.md`
- `docs/PROMPT_MAPPING.md`
- `docs/prompts/`

**Aporte realizado:**

Se establecieron reglas operativas para agentes IA y prompts versionados derivados de especificaciones aprobadas.

**Valor aportado:**

- Evita prompts sueltos.
- Convierte prompts en contratos auditables.
- Define invariantes, failure modes, guardrails y pruebas.
- Sincroniza IA con DTI y FSD.
- Limita el poder de la IA en decisiones financieras.

---

### 4.8 Fase de roadmap

**Artefacto asociado:**

- `docs/roadmap.md`

**Aporte realizado:**

Se definió una ruta de evolución desde defensa académica hacia producto real:

| Horizonte | Enfoque |
|---|---|
| H0 | Consolidación documental y defensa final. |
| H1 | MVP funcional trazable. |
| H2 | Piloto operacional controlado. |
| H3 | Producto cloud-ready con IA gobernada. |
| H4 | Escalamiento empresarial y analítica avanzada. |

**Valor aportado:**

El roadmap conecta estrategia, producto, arquitectura, POCs, IA y operación.

---

## 5. Matriz de trazabilidad de aportes

| Problema detectado | Evidencia / necesidad | Artefacto que lo aborda | Tipo de aporte |
|---|---|---|---|
| Reportes por WhatsApp y Excel | Información dispersa | BRD, FSD, DTI, POC-01 | Centralización |
| Falta de trazabilidad | No se sabe qué ocurrió con cada producto | FSD, ADR-0003, DTI, POC-01 | Auditoría |
| Falta de control de precio | No se mide precio anterior / nuevo | PRD, FSD, ADRs, POC-01 | KPI financiero |
| Decisiones con incertidumbre | Gerencia y supervisión carecen de datos | Dashboard, DTI, POC-01 | Visibilidad |
| Riesgo de IA autónoma | IA podría sugerir decisiones financieras | ADR-0004, POC-02, AGENTS | Guardrails |
| Falta de evidencia técnica | Arquitectura solo teórica | POCs | Validación |
| Falta de prompts gobernados | Prompts no versionados | PROMPT_MAPPING | Gobierno IA |
| Falta de evolución clara | Producto sin plan posterior | Roadmap | Estrategia |

---

## 6. Evidencia para defensa oral

Durante la defensa, este documento permite explicar:

1. **Qué se hizo:** se produjo un paquete documental y técnico completo para la entrega final.
2. **Por qué se hizo:** cada artefacto responde a un problema real del negocio.
3. **Cómo se conectan los entregables:** todos siguen una cadena de trazabilidad.
4. **Qué evidencia existe:** POCs, diagramas, ADRs y prompts.
5. **Qué decisiones son defendibles:** monolito modular, hexagonal, Outbox, dashboard inmediato, IA gobernada y AWS.
6. **Qué valor aporta:** reducción de incertidumbre, trazabilidad, control de precio, medición de impacto financiero y reducción de merma.

---

## 7. Conclusión

El aporte realizado no se limita a redactar documentos. Consiste en construir una base completa de producto y arquitectura para transformar un proceso informal, reactivo y fragmentado en una solución digital trazable, medible, auditable y escalable.

El paquete aprobado demuestra coherencia entre:

```text
Negocio → Mercado → Producto → Funcionalidad → Arquitectura → Evidencia → IA gobernada → Roadmap
```

Esta trazabilidad permite defender el proyecto como una solución integral de producto de software con IA, no como una aplicación aislada.

---

## 8. Checklist de validez

- [x] Incluye aportes por artefacto.
- [x] Incluye rutas esperadas en repositorio.
- [x] Incluye estado de aprobación.
- [x] Incluye trazabilidad con documentos aprobados.
- [x] Incluye conexión con POCs.
- [x] Incluye conexión con IA y prompt governance.
- [x] Incluye conexión con roadmap.
- [x] Incluye explicación para defensa oral.
- [x] No contiene secretos ni datos sensibles.
- [x] Está listo para ubicarse en `docs/aportes/release-2.0.0.md`.

---

## 9. Registro de cambios

| Versión | Fecha | Autora | Cambio |
|---|---|---|---|
| v1.0 | 27/05/2026 | Gina Fabiana Villanueva Viscarra | Creación del documento de aportes para `release/2.0.0`. |
