# AGENTS.md – Lista de agentes IA

## 0. Metadatos
| Campo | Valor |
|-------|-------|
| Versión | 1.0 |
| Fecha | 14/05/2026 |
| Autor | Gina Fabiana Villanueva Viscarra |
| Estado | Completo |
| Branch | release/1.0.0 |
| Relación | DTI, POCs, FSD |

## 1. Propósito
Este documento describe todos los agentes IA utilizados en la App Detección Prod, sus roles, herramientas asociadas, responsabilidades y cómo interactúan con los cuatro actores principales: Mercaderista, Vendedor, Supervisor y Gerente Comercial.

## 2. Tabla de agentes

| Agente | Rol | Herramientas / Tecnología | Responsabilidad | Entradas | Salidas | UC / POC asociado |
|--------|-----|--------------------------|----------------|----------|---------|-----------------|
| agent-orchestrator | Orquestador IA | Python, Prompts, RAG-service | Coordina tareas IA, aplica guardrails y rutea solicitudes | Productos críticos, acciones comerciales | Alertas, validación de datos, prompts procesados | FSD-UC-001, POC-01 |
| rag-service | Recuperación semántica | Python, Vector DB | Recupera contexto y referencias para alertas y prompts | Queries de productos críticos | Respuestas contextuales para prompts y dashboards | FSD-UC-001, POC-01 |
| model-router | Selección modelo | Python, ML models | Determina el modelo IA óptimo según latencia, costo y criticidad | Prompt y datos de entrada | Modelo seleccionado y configurado | FSD-UC-002, FSD-UC-004 |
| prompt-validator | Validación de prompts | Python | Verifica que los prompts cumplen los invariantes y guardrails | Prompts de UC | Resultado de validación | FSD-UC-001 a UC-004 |
| analytics-agent | Métricas y KPIs | Node.js, PostgreSQL | Calcula y actualiza KPIs y métricas para dashboard | Acciones y registros de productos | Dashboard y reportes | FSD-UC-004, POC-02 |
| alerting-agent | Generación de alertas | Python, SNS/SQS | Crea y distribuye alertas operativas a supervisores y gerentes | Registros de productos críticos y acciones | Notificaciones en dashboards o correo | FSD-UC-001, POC-01 |

## 3. Roles de los agentes por actor

| Actor | Agentes principales involucrados | Función principal |
|-------|---------------------------------|-----------------|
| Mercaderista | agent-orchestrator, rag-service | Recibe validación y alertas de productos críticos |
| Vendedor | model-router, prompt-validator | Consolida información, aplica reglas de negocio y prompts |
| Supervisor | alerting-agent, analytics-agent | Monitorea alertas y KPIs, toma decisiones de validación |
| Gerente Comercial | analytics-agent, model-router | Analiza KPIs estratégicos y métricas para decisiones |

## 4. Interacciones y flujo de datos
flowchart LR
  M[Mercaderista] --> AO[agent-orchestrator]
  V[Vendedor] --> MR[model-router]
  AO --> RAG[rag-service]
  AO --> Alert[alerting-agent]
  RAG --> MR
  MR --> Dash[analytics-agent]
  Dash --> S[Supervisor]
  Dash --> G[Gerente Comercial]

## 5. Observaciones
Todos los agentes respetan la arquitectura hexagonal.
Los agentes son independientes y escalables, siguiendo los principios de Clean Architecture.
Guardrails y validaciones aseguran que los datos críticos nunca se pierdan o sean incorrectos.
## 6. Historial
| Versión | Fecha      | Autor        | Cambio                                                               |
| ------- | ---------- | ------------ | -------------------------------------------------------------------- |
| 1.0     | 14/05/2026 | Gina Fabiana | Creación del documento AGENTS.md completo con roles y flujo de datos |
