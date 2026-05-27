# ADR-0001: Adoptar monolito modular con arquitectura hexagonal como base evolutiva

> **Ubicación sugerida en el repositorio:** `docs/adr/0001-estilo-arquitectonico.md`  
> **Estado:** `PARA REVISIÓN`  
> **Versión:** `vFinal-2.0.0-mejorada`  
> **Release objetivo:** `release/2.0.0`  
> **Producto:** App Detección Prod  
> **Autora:** Gina Fabiana Villanueva Viscarra  
> **Cadena de trazabilidad:** `BRD → MRD → PRD → FSD → ADR → DTI → POC → Demo`  
> **Decisión principal:** iniciar App Detección Prod como **monolito modular con arquitectura hexagonal**, manteniendo límites internos por bounded context, puertos/adaptadores, eventos de dominio internos y una ruta evolutiva hacia event-driven, CQRS y microservicios únicamente cuando existan métricas reales que lo justifiquen.

---

## 0. Resumen ejecutivo de la decisión

App Detección Prod resuelve un problema operativo y financiero en distribuidoras/importadoras retail: la gestión de productos próximos a vencer se realiza actualmente con WhatsApp, Excel, fotografías no estandarizadas y comunicación fragmentada. Esta situación genera pérdida de trazabilidad, ausencia de métricas, errores en acciones comerciales, demora en decisiones, baja visibilidad gerencial y dificultad para medir impacto financiero.

La arquitectura seleccionada debe responder a dos necesidades simultáneas:

1. **Construir una solución suficientemente simple, implementable y defendible en el contexto del módulo.**
2. **Evitar que esa simplicidad derive en un sistema desordenado, difícil de mantener, sin trazabilidad ni evolución futura.**

Por ello se adopta un **monolito modular con arquitectura hexagonal**. Esta opción evita microservicios prematuros, conserva un único despliegue inicial, protege el dominio del negocio, facilita pruebas, ordena los casos de uso del FSD y deja límites claros para evolucionar después hacia microservicios o event-driven cuando el producto tenga carga, equipos, ownership y métricas reales.

La decisión no es “hacer un monolito porque es más fácil”; es **usar un monolito modular como etapa arquitectónica consciente**, con reglas estrictas de dependencia, módulos de dominio, eventos internos, auditoría, puertos para IA, y una estrategia explícita de extracción futura.

---

## 1. Metadatos

| Campo | Valor |
|---|---|
| Número | ADR-0001 |
| Título | Adoptar monolito modular con arquitectura hexagonal como base evolutiva |
| Fecha | 26/05/2026 |
| Autora | Gina Fabiana Villanueva Viscarra |
| Estado | Para revisión |
| Alcance | Todo el sistema App Detección Prod |
| Release | `release/2.0.0` |
| Documentos padre | `docs/brd/BRD_vFinal.md`, `docs/mrd/MRD_vFinal.md`, `docs/prd/PRD_vFinal.md`, `docs/fsd/FSD_vFinal.md` |
| Documentos hijos impactados | `docs/DTI.md`, `AGENTS.md`, `docs/diagrams/*.mmd`, `docs/PROMPT_MAPPING.md`, `pocs/POC-01`, `pocs/POC-02` |
| Stakeholders considerados | Mercaderista, Supervisor Regional, Vendedor Canal Moderno, Gerencia Comercial, Finanzas/Admin, Arquitectura/Desarrollo |
| ADRs relacionados | ADR-0002 Bounded Contexts, ADR-0003 Event-driven + Outbox, ADR-0004 Capa IA + Guardrails, ADR-0005 Cloud/AWS |

---

## 2. Contexto del problema

### 2.1 Contexto operativo

La empresa objetivo opera en canal retail: supermercados, micromercados, cadenas de farmacias y tiendas especializadas. Los mercaderistas detectan productos próximos a vencer en sala, toman fotografías, reportan por WhatsApp o Excel y esperan que supervisores, vendedores o gerencia tomen decisiones.

El problema real no es simplemente “falta una app”. El problema es que el proceso actual no integra:

- relevamiento operativo;
- evidencia fotográfica;
- fecha de vencimiento;
- cantidad intervenida;
- precio actual;
- nuevo precio o descuento;
- acción comercial aplicada;
- validación supervisora;
- impacto financiero;
- estado de seguimiento;
- métricas gerenciales.

El sistema propuesto debe conectar niveles operativos, tácticos y estratégicos. Por eso la arquitectura debe reflejar la estructura real del negocio, no solo una división técnica por pantallas o tablas.

### 2.2 Evidencia de entrevistas

La arquitectura se justifica desde evidencia del proyecto:

| Rol | Dolor evidenciado | Implicación arquitectónica |
|---|---|---|
| Mercaderista | Reporta en campo, con presión de tiempo y herramientas informales. | El registro debe ser rápido, guiado y tolerante a errores. |
| Supervisor | Recibe información por WhatsApp/Excel, valida manualmente, pierde tiempo y opera con incertidumbre. | Debe existir flujo formal de validación, estados, auditoría y priorización. |
| Vendedor | Recibe información dispersa y toma decisiones comerciales sin certeza sobre acciones previas. | Las acciones comerciales deben ser trazables, versionadas y consultables. |
| Gerencia | Necesita visibilidad completa, KPIs, rotación, impacto financiero y costos asociados. | La analítica debe ser una capacidad central, no un reporte posterior improvisado. |

### 2.3 Contexto académico y de evaluación

La defensa final evalúa coherencia documental, calidad arquitectónica, C4, hexagonal, arquitectura distribuida, IA, AWS, ADRs, POCs, diagramas, AGENTS.md y PROMPT_MAPPING.md. Por tanto, la arquitectura debe ser:

- explicable oralmente;
- trazable a BRD/MRD/PRD/FSD;
- defendible con trade-offs;
- suficientemente técnica;
- no sobreingenierizada;
- preparada para DTI y diagramas C4;
- compatible con IA y agentes;
- lista para POCs medibles.

---

## 3. Problema arquitectónico que resuelve este ADR

Se debe decidir el **estilo arquitectónico base** para App Detección Prod.

La decisión debe responder:

1. ¿Conviene iniciar con monolito, monolito modular, microservicios o serverless?
2. ¿Cómo proteger las reglas de negocio de vencimiento, acciones comerciales, precios, auditoría e IA?
3. ¿Cómo evitar que el sistema se convierta en un “Big Ball of Mud”?
4. ¿Cómo demostrar arquitectura distribuida/event-driven sin caer en microservicios prematuros?
5. ¿Cómo preparar el DTI y los diagramas C4 de forma coherente?
6. ¿Cómo permitir que agentes IA de desarrollo puedan trabajar sin romper la trazabilidad FSD → código?

---

## 4. Drivers arquitectónicos

| ID | Driver | Fuente funcional / negocio | Implicación arquitectónica |
|---|---|---|---|
| DA-01 | Registro de producto próximo a vencer rápido y confiable | PRD/FSD: registro operativo por mercaderista | Caso de uso independiente de UI, validaciones en dominio, persistencia desacoplada. |
| DA-02 | Validación supervisora con reducción de incertidumbre | Entrevista supervisor / FSD validación | Estado formal del caso, flujo de aprobación, auditoría y reglas explícitas. |
| DA-03 | Gestión comercial trazable | Entrevista vendedor / PRD acciones comerciales | Módulo propio para acciones, precios, descuentos, bandeos, retiros y aprobaciones. |
| DA-04 | Visibilidad gerencial e impacto financiero | Entrevista gerente / BRD KPIs | Lecturas analíticas, métricas y posible read model separado. |
| DA-05 | Auditoría completa | BRD/FSD trazabilidad | Registro append-only de decisiones, cambios y usuario responsable. |
| DA-06 | IA asistiva controlada | PRD/FSD capa IA | Puerto hacia IA, guardrails, human-in-the-loop y auditoría de prompts. |
| DA-07 | Evolución a event-driven | DTI futuro / POCs | Eventos de dominio internos y Outbox futuro. |
| DA-08 | Simplicidad operativa inicial | Contexto académico/MVP | Un despliegue inicial con módulos internos bien delimitados. |
| DA-09 | Escalabilidad futura | Roadmap producto | Seams para extraer analytics, notificaciones, IA o acciones comerciales. |
| DA-10 | Trazabilidad documental | Rúbrica final | Cada decisión debe reflejarse en DTI, diagramas, AGENTS.md y POCs. |

---

## 5. Fuerzas en tensión

| Fuerza | Lo que se necesita | Tensión / riesgo |
|---|---|---|
| Rapidez de entrega | Construir y defender un producto coherente. | Microservicios completos retrasan documentación, POCs y demo. |
| Rigor arquitectónico | Mostrar DTI, C4, hexagonal, eventos, IA y AWS. | Un MVC simple no alcanza nivel de maestría. |
| Dominio rico | Vencimientos, acciones, precios, auditoría, impactos financieros. | Mezclar reglas en controladores haría el sistema frágil. |
| Evolución futura | Posible separación de analytics, notificaciones, IA o acciones. | Un monolito sin módulos claros bloquearía crecimiento. |
| Operación en campo | Mercaderistas necesitan flujo simple y estable. | Arquitectura excesivamente distribuida puede fallar más y complicar soporte. |
| Gerencia informada | Necesita KPIs y visibilidad, no tareas operativas. | La analítica no debe depender de consultas improvisadas al modelo transaccional. |
| IA controlada | IA debe asistir, no decidir sola. | Sin puertos y guardrails, se acopla al dominio y genera riesgo. |
| Auditoría | Cada decisión crítica debe rastrearse. | Eventos o logs mal diseñados pueden perder evidencia. |
| Costos y equipo | Equipo académico/pequeño, tiempo limitado. | Microservicios elevan costo cognitivo y operativo. |

---

## 6. Alternativas consideradas

### 6.1 Tabla comparativa general

| Alternativa | Descripción | Pros | Contras | Costo inicial | Costo evolutivo | Veredicto |
|---|---|---|---|---|---|---|
| A. MVC / monolito por capas tradicional | Controllers → Services → Repositories, con dominio acoplado al framework. | Rápido, simple, fácil de prototipar. | Riesgo de reglas dispersas, baja testabilidad, difícil trazabilidad FSD→dominio, débil para defensa. | Bajo | Alto | Rechazada. |
| B. Monolito modular + hexagonal | Un despliegue inicial, módulos por dominio, puertos/adaptadores. | Balancea simplicidad, rigor, testabilidad, evolución y trazabilidad. | Requiere disciplina de límites y arquitectura. | Medio | Medio/bajo | Aceptada. |
| C. Microservicios completos desde v1 | Servicios independientes por dominio. | Escalado y despliegue independiente. | Complejidad operativa, consistencia eventual, observabilidad distribuida, riesgo de distributed monolith. | Alto | Alto | Rechazada para v1; opción futura. |
| D. Serverless-first AWS | API Gateway/Lambda/DynamoDB/SQS/S3 desde el inicio. | Escalado automático, pago por uso, cloud-native. | Lock-in temprano, debugging complejo, cold starts, curva de pruebas locales. | Medio/alto | Medio/alto | Diferida; útil para componentes específicos. |
| E. Event-driven puro | Todos los flujos mediante eventos. | Desacoplamiento fuerte, auditoría natural. | Sobrecarga conceptual, consistencia eventual en exceso, difícil para flujos síncronos. | Alto | Medio/alto | Rechazada como estilo dominante; aceptada parcialmente. |
| F. Microkernel / plugins | Núcleo + plugins para acciones, reglas o integraciones. | Extensible si hay muchos clientes o reglas variables. | Complejo para MVP, aún no hay variabilidad suficiente. | Alto | Medio | Diferida. |

### 6.2 Matriz ponderada de decisión

Escala: 1 = muy débil, 5 = muy fuerte.  
Peso: importancia relativa para este proyecto.

| Criterio | Peso | A. MVC | B. Modular + Hexagonal | C. Microservicios | D. Serverless | E. Event-driven puro |
|---|---:|---:|---:|---:|---:|---:|
| Simplicidad operativa inicial | 15 | 5 | 4 | 1 | 3 | 1 |
| Protección del dominio | 20 | 2 | 5 | 4 | 3 | 4 |
| Trazabilidad FSD→código→test | 15 | 2 | 5 | 4 | 3 | 3 |
| Evolución futura | 15 | 2 | 5 | 5 | 4 | 4 |
| Costo cognitivo para el equipo | 10 | 5 | 4 | 1 | 2 | 2 |
| Coherencia con DTI/C4/ADR | 10 | 2 | 5 | 5 | 4 | 4 |
| Manejo de auditoría/eventos | 10 | 2 | 4 | 5 | 4 | 5 |
| Control de IA/guardrails | 5 | 2 | 5 | 4 | 3 | 4 |
| **Puntaje ponderado** | **100** | **285** | **475** | **365** | **330** | **330** |

**Resultado:** la alternativa B obtiene el mayor puntaje porque equilibra las necesidades del MVP, la defensa académica, la trazabilidad y la evolución arquitectónica futura.

---

## 7. Decisión

Se decide adoptar para App Detección Prod una arquitectura base de:

```text
Monolito modular
+ Arquitectura hexagonal
+ Bounded contexts internos
+ Eventos de dominio internos
+ Outbox futuro para integración asíncrona
+ Puertos explícitos para IA, notificaciones, persistencia, auditoría y analítica
```

### 7.1 Qué significa esta decisión

El sistema iniciará como un único backend desplegable, pero internamente estará organizado por módulos de negocio. Cada módulo tendrá su propio dominio, casos de uso, puertos y adaptadores. Las reglas de negocio no vivirán en controladores, pantallas, SQL disperso ni servicios genéricos. Vivirán en el core de dominio y serán invocadas mediante casos de uso.

### 7.2 Qué NO significa esta decisión

Esta decisión no significa:

- hacer un monolito desordenado;
- rechazar microservicios para siempre;
- ignorar event-driven;
- dejar la analítica como consulta improvisada;
- permitir que IA tome decisiones autónomas;
- construir una arquitectura sobredimensionada sin implementación posible.

Significa empezar con una base simple y fuerte, diseñada para evolucionar.

---

## 8. Arquitectura resultante esperada

### 8.1 Vista conceptual

```text
[Frontend Web/Móvil]
        |
        v
[Adapters In: REST Controllers / UI API]
        |
        v
[Application Layer: Use Cases del FSD]
        |
        v
[Domain Layer: Entidades, Aggregates, Value Objects, Reglas]
        |
        v
[Ports Out]
        |---- Persistence Port → PostgreSQL
        |---- Evidence Storage Port → S3 / almacenamiento local en dev
        |---- Event Publisher Port → Outbox / EventBridge / SQS futuro
        |---- Notification Port → email/push/WhatsApp empresarial futuro
        |---- AI Classification Port → modelo IA con guardrails
        |---- Audit Log Port → auditoría append-only
        |---- Analytics Port → read models / dashboards
```

### 8.2 Módulos internos iniciales

| Módulo | Bounded context | Responsabilidad | Casos de uso asociados | Candidato a extracción futura |
|---|---|---|---|---|
| `detection` | Product Detection | Registro, evidencia, fechas, criticidad inicial y ciclo de vida del producto detectado. | FSD-UC-001, FSD-UC-002 | Sí, si crece volumen de registros por tienda/ruta. |
| `commercial-actions` | Commercial Actions | Descuentos, bandeos, retiros, promociones, devoluciones, cambios y aprobación. | FSD-UC-003, FSD-UC-004, FSD-UC-005 | Sí, si se integra con ERP/precios. |
| `supervision` | Supervision Workflow | Validación táctica, priorización, SLA, seguimiento y escalamiento. | FSD-UC-002, FSD-UC-006 | Posible, si hay equipos regionales separados. |
| `analytics` | Executive Analytics | KPIs, impacto financiero, rotación, ranking, dashboards y métricas gerenciales. | FSD-UC-007, FSD-UC-010 | Sí, candidato fuerte a CQRS/read model. |
| `notifications` | Notifications | Alertas por vencimiento, riesgo alto, falta de acción o vencimiento de SLA. | FSD-UC-006 | Sí, como worker/event consumer. |
| `audit` | Audit Trail | Historial inmutable de decisiones, cambios, evidencias y usuarios. | FSD-UC-008 | Posible append-only service/event store parcial. |
| `ai-assistance` | AI Assistance | Clasificación de riesgo, sugerencias asistidas y validaciones con guardrails. | FSD-UC-009 | Sí, si requiere escalado/model routing propio. |
| `identity-access` | Identity & Access | Roles, permisos, autenticación y autorización. | Transversal | Puede delegarse a IdP externo. |

### 8.3 Regla central de dependencia

```text
Adapters → Application → Domain

Domain NO depende de:
- framework web;
- ORM;
- base de datos;
- AWS SDK;
- proveedor IA;
- formato HTTP;
- librería de UI;
- sistema de mensajería.
```

### 8.4 Vertical slice estándar

Cada funcionalidad crítica debe seguir esta cadena:

```text
BRD/MRD/PRD/FSD ID
→ UseCase Port
→ Application Service
→ Domain Model / Domain Service
→ Output Ports
→ Adapters
→ Tests
→ PROMPT_MAPPING.md
→ DTI
```

Ejemplo:

```text
FSD-UC-001 Registrar producto próximo a vencer
→ RegisterExpiringProductUseCase
→ RegisterExpiringProductService
→ ProductDetection / ExpirationRisk / Evidence
→ ProductDetectionRepository + EvidenceStoragePort + AuditLogPort
→ REST Controller + PostgreSQL Adapter + S3 Adapter
→ RegisterExpiringProductTest
→ PR-UC-001
→ DTI §5 Arquitectura Hexagonal
```

---

## 9. Puertos de entrada esperados

| Puerto de entrada | Caso de uso | Actor principal | Resultado esperado |
|---|---|---|---|
| `RegisterExpiringProductUseCase` | Registrar producto próximo a vencer | Mercaderista | Reporte creado con evidencia y estado inicial. |
| `ValidateDetectionReportUseCase` | Validar reporte | Supervisor | Reporte validado, observado o rechazado. |
| `PrioritizeProductRiskUseCase` | Priorizar criticidad | Supervisor / Sistema | Nivel de riesgo calculado y trazado. |
| `RegisterCommercialActionUseCase` | Registrar acción comercial | Vendedor / Supervisor | Acción registrada con precio, cantidad y responsable. |
| `ApproveCommercialActionUseCase` | Aprobar acción | Supervisor / Gerencia en excepción | Acción aprobada/rechazada según política. |
| `TrackCommercialExecutionUseCase` | Dar seguimiento | Supervisor / Vendedor | Estado actualizado y evidencia registrada. |
| `GetExecutiveDashboardUseCase` | Consultar dashboard | Gerencia | KPIs consolidados por producto, tienda, región y acción. |
| `ClassifyRiskWithAIUseCase` | Clasificar riesgo asistido | Sistema + revisión humana | Sugerencia trazable, no ejecución automática. |
| `AuditDecisionHistoryUseCase` | Auditar historial | Supervisor / Gerencia / Finanzas | Línea de tiempo de decisiones y cambios. |

---

## 10. Puertos de salida esperados

| Puerto de salida | Propósito | Adaptador inicial | Adaptador futuro posible |
|---|---|---|---|
| `ProductDetectionRepository` | Persistir reportes y estados. | PostgreSQL/JPA | Servicio detection separado. |
| `CommercialActionRepository` | Persistir acciones comerciales. | PostgreSQL/JPA | Servicio commercial-actions. |
| `EvidenceStoragePort` | Guardar fotos/evidencia. | Filesystem/S3 | S3 con lifecycle policies. |
| `DomainEventPublisher` | Publicar eventos internos. | In-process events | Outbox + SQS/EventBridge. |
| `NotificationPort` | Enviar alertas. | Log/email simulado | WhatsApp Business, push, SES/SNS. |
| `AIClassificationPort` | Clasificar riesgo con IA. | Mock/modelo controlado | Servicio IA/model-router. |
| `AuditLogPort` | Registrar decisiones. | Tabla `audit_log` | Append-only log / event store parcial. |
| `AnalyticsReadModelPort` | Consultar agregados. | SQL views | CQRS/read database. |
| `IdentityProviderPort` | Autenticación/autorización. | Local/RBAC | Cognito/IdP empresarial. |

---

## 11. Modelo de consistencia

| Flujo | Tipo de consistencia | Justificación |
|---|---|---|
| Registro de producto | Consistencia fuerte local | El reporte y su auditoría mínima deben quedar confirmados juntos. |
| Validación supervisora | Consistencia fuerte local | No debe existir decisión sin estado actualizado. |
| Registro de acción comercial | Consistencia fuerte local | Precio, cantidad, acción y responsable deben persistir como unidad. |
| Notificaciones | Consistencia eventual | Puede enviarse segundos después; no debe bloquear el flujo principal. |
| Dashboard gerencial | Consistencia eventual aceptable | Gerencia consume información consolidada; puede tolerar pequeña latencia. |
| IA asistiva | Consistencia eventual / recomendación | La sugerencia no debe bloquear ni sustituir decisión humana. |
| Auditoría | Consistencia fuerte para decisiones críticas | Toda decisión debe quedar registrada con trazabilidad. |

---

## 12. Relación con event-driven

Se adopta event-driven de manera selectiva. No todos los casos de uso deben ser asíncronos. El sistema debe diferenciar entre:

- **comandos síncronos**: acciones del usuario que requieren respuesta inmediata;
- **eventos de dominio**: hechos relevantes ocurridos;
- **procesos asíncronos**: notificaciones, analítica, escalamiento, auditoría extendida.

| Evento de dominio candidato | Productor | Consumidor inicial | Uso |
|---|---|---|---|
| `ProductDetectionRegistered` | `detection` | `audit`, `notifications`, `analytics` | Auditoría, alerta inicial, actualización de indicadores. |
| `DetectionReportValidated` | `supervision` | `commercial-actions`, `analytics` | Habilitar acción comercial y métricas. |
| `ProductRiskEscalated` | `supervision` / `ai-assistance` | `notifications`, `supervision` | Alertar criticidad alta. |
| `CommercialActionRegistered` | `commercial-actions` | `audit`, `analytics`, `notifications` | Registrar acción e iniciar seguimiento. |
| `CommercialActionApproved` | `commercial-actions` | `notifications`, `analytics` | Activar seguimiento y dashboard. |
| `ProductCaseClosed` | `detection` | `analytics`, `audit` | Medir tiempo de ciclo e impacto. |

**Decisión diferida:** ADR-0003 deberá definir Outbox, idempotencia, DLQ, retries, orden de eventos y garantías de entrega.

---

## 13. Relación con IA

La IA será tratada como un adaptador externo controlado por puertos. No será parte del dominio central ni tendrá autoridad para ejecutar decisiones irreversibles.

| Elemento IA | Regla arquitectónica |
|---|---|
| Clasificación de riesgo | Permitida como recomendación asistida. |
| Recomendación de acción comercial | Permitida como sugerencia explicable. |
| Aprobación de descuento/retiro | Prohibida sin humano responsable. |
| Cambio de precio | Prohibido como acción autónoma de IA. |
| Entrada al modelo | Debe contener datos mínimos necesarios, sin secretos ni PII innecesaria. |
| Salida del modelo | Debe validarse contra esquema, reglas de negocio e invariantes. |
| Auditoría | Registrar `prompt_id`, versión, modelo, entrada resumida, salida, confianza, decisión humana y fecha. |
| Fallback | Si IA falla, el flujo manual debe seguir funcionando. |

**Decisión diferida:** ADR-0004 formalizará modelo, guardrails, prompt mapping, métricas de calidad y observabilidad IA.

---

## 14. Relación con AWS y despliegue

Esta ADR no selecciona todos los servicios AWS definitivos, pero prepara el diseño para un mapeo cloud-native coherente:

| Componente lógico | AWS probable | Justificación |
|---|---|---|
| Backend modular | ECS Fargate / Elastic Beanstalk / App Runner | Un despliegue inicial simple y escalable. |
| Base transaccional | RDS PostgreSQL | Consistencia fuerte y consultas relacionales. |
| Evidencia fotográfica | S3 | Almacenamiento durable y económico. |
| Eventos futuros | SQS / EventBridge | Integración asíncrona y desacoplamiento. |
| Notificaciones | SNS / SES / integración externa | Alertas operativas. |
| Métricas/logs | CloudWatch / OpenTelemetry | Observabilidad. |
| Secretos | Secrets Manager / Parameter Store | Seguridad operacional. |
| Autenticación futura | Cognito / IdP empresarial | RBAC y control de acceso. |

**Decisión diferida:** ADR-0005 formalizará cloud provider, estilo de despliegue y servicios AWS.

---

## 15. Consecuencias positivas

| Consecuencia | Impacto |
|---|---|
| Dominio protegido | Las reglas de vencimiento, criticidad, acciones, precios e impacto financiero no se dispersan en UI o controladores. |
| Trazabilidad fuerte | Cada caso de uso del FSD puede mapearse a puerto, servicio, dominio, test y prompt. |
| Testabilidad | El core puede probarse sin infraestructura externa. |
| Simplicidad operativa | Un único despliegue inicial evita costos de microservicios prematuros. |
| Evolución incremental | Permite extraer módulos cuando haya evidencia. |
| Defensa académica sólida | Permite explicar trade-offs reales con C4, DTI, ADR, POC y AWS. |
| Preparación event-driven | Eventos internos permiten migrar a Outbox sin rediseñar todo. |
| IA segura | La IA queda encapsulada detrás de puertos y guardrails. |
| Mejor colaboración humano/agente | AGENTS.md puede definir reglas claras para implementación. |

---

## 16. Consecuencias negativas y costos

| Consecuencia | Riesgo | Mitigación |
|---|---|---|
| Más estructura que MVC simple | Puede parecer pesado al inicio. | Plantillas, ejemplos de vertical slice y AGENTS.md. |
| Requiere disciplina | Los límites pueden romperse por presión de entrega. | Tests de arquitectura, revisión de PR y reglas de dependencia. |
| Escalado inicial conjunto | Todo el backend escala como unidad. | Aceptable hasta tener métricas; separación futura por módulos. |
| Base de datos inicial compartida | Riesgo de acoplamiento entre módulos. | Ownership de tablas por módulo y cero joins transversales no justificados. |
| Curva de aprendizaje | Puertos/adaptadores exigen diseño. | Documentar patrones en DTI y ejemplos de código. |
| Riesgo de “monolito modular solo de nombre” | Si no hay enforcement, se degrada. | Checklist de ADR/DTI y reglas de arquitectura. |

---

## 17. Impacto en el DTI

El DTI debe reflejar esta ADR en las siguientes secciones:

| Sección DTI | Contenido esperado derivado de ADR-0001 |
|---|---|
| §3 Arquitectura de alto nivel | Monolito modular + hexagonal como estilo adoptado. |
| §3.2 C4 Contenedores | Backend modular, frontend, DB, almacenamiento evidencia, notificaciones, IA, analytics. |
| §3.3 Componentes | Bajar a nivel 3 en el módulo `detection` o `commercial-actions`. |
| §4 Modelo de dominio | Bounded contexts y aggregates derivados del FSD. |
| §5 Hexagonal | Puertos de entrada/salida y adaptadores. |
| §6 Distribuida | Explicar que microservicios son evolución condicionada. |
| §7 Event-driven | Eventos internos y ruta a Outbox. |
| §8 AWS | Mapeo cloud coherente sin forzar microservicios. |
| §9 IA | IA como adaptador con guardrails. |
| §11 NFRs | Latencia, disponibilidad, seguridad, auditoría y observabilidad. |
| §12 POCs | POC-01 registro y POC-02 IA/guardrails. |
| §17 Trade-offs | Monolito modular vs microservicios/serverless/event-driven. |
| §21 ADRs | Registrar ADR-0001 como aceptada cuando sea aprobada. |

---

## 18. Impacto en C4

| Nivel C4 | Decisión de modelado |
|---|---|
| Nivel 1 — Contexto | App Detección Prod como sistema central entre mercaderista, supervisor, vendedor, gerencia y sistemas externos. |
| Nivel 2 — Contenedores | Frontend, backend modular, PostgreSQL, S3/evidencias, módulo IA, notificaciones, analytics/read model. |
| Nivel 3 — Componentes | Para `detection`: controller/adaptador, use case, domain service, repository port, event publisher, audit port. |
| Dynamic diagrams | Secuencia de registro, validación, acción comercial, alerta y consulta gerencial. |
| Deployment | AWS con backend, RDS, S3, CloudWatch y colas futuras. |

---

## 19. Impacto en AGENTS.md

AGENTS.md debe instruir a cualquier agente IA de desarrollo que:

1. No cree reglas de negocio en controladores.
2. No agregue dependencias de infraestructura en `domain`.
3. Todo cambio debe citar un ID FSD/PRD.
4. Cada caso de uso nuevo debe tener puerto de entrada.
5. Cada integración externa debe pasar por puerto de salida.
6. Todo flujo con IA debe aplicar guardrails y auditoría.
7. Todo evento crítico debe prepararse para Outbox si afecta consistencia.
8. Toda modificación arquitectónica significativa debe crear o actualizar ADR.

---

## 20. Plan de reversión / evolución

La reversión de esta decisión no implica rehacer el sistema. Implica extraer módulos con bajo costo relativo gracias a los puertos y límites internos.

| Señal de fallo o crecimiento | Acción de reversión/evolución |
|---|---|
| `analytics` afecta rendimiento transaccional | Crear read model separado o servicio analytics. |
| `notifications` requiere retries/DLQ/alta disponibilidad | Separar worker event-driven. |
| `ai-assistance` requiere escalado o seguridad diferenciada | Extraer servicio IA. |
| `commercial-actions` requiere integración ERP/precios compleja | Separar módulo o crear anti-corruption layer. |
| Módulos rompen límites internos | Agregar tests de arquitectura y refactorizar dependencias. |
| Equipos necesitan releases independientes | Evaluar microservicios por bounded context. |
| DB se vuelve cuello de botella | Separar read models, réplicas o partición por módulo. |

Costo estimado de reversión: **medio**, porque los puertos y boundaries permiten extracción incremental. En MVC tradicional, el costo sería alto.

---

## 21. Riesgos remanentes

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Monolito modular solo declarativo | Media | Alto | Reglas de dependencia, AGENTS.md, revisión de PR. |
| Base de datos compartida acopla módulos | Media | Alto | Ownership por tabla, esquemas por módulo y repositorios separados. |
| Dashboard exige consultas pesadas | Media | Medio/alto | Read models y CQRS progresivo. |
| Eventos sin garantía transaccional | Media | Alto | ADR-0003 Outbox antes de producción. |
| IA se usa sin guardrails | Media | Alto | ADR-0004, prompt tests y human-in-the-loop. |
| Sobre-diseño sin demo | Media | Medio | POCs ejecutables y vertical slices mínimos. |
| Equipo no mantiene documentación | Media | Medio | PROMPT_MAPPING y checklist por release. |

---

## 22. Validación de la decisión

| Métrica / evidencia | Umbral | Fuente de validación |
|---|---:|---|
| Casos de uso críticos con puerto de entrada | 100 % | FSD + DTI §5 |
| Reglas de negocio fuera de controladores | 100 % | Revisión código / tests |
| Dominio sin dependencias de framework | 100 % | Test de arquitectura |
| Acciones comerciales auditadas | 100 % | Tests FSD-UC-003/004/005 |
| Registro de producto con latencia p95 | ≤ 500 ms | POC-01 |
| Registro operativo completo | ≤ 3 min | POC/usabilidad/demo |
| Recomendaciones IA con revisión humana | 100 % | POC-02 |
| Eventos críticos identificados | ≥ 6 eventos | DTI §7 |
| Gaps FSD→DTI críticos | 0 | Checklist release/2.0.0 |
| Diagramas relacionados | ≥ 8 `.mmd` | `docs/diagrams/` |

---

## 23. Trazabilidad hacia documentos aprobados

| Documento | Elemento relacionado | Cómo impacta esta ADR |
|---|---|---|
| BRD vFinal | Trazabilidad, control financiero, visibilidad gerencial, reducción de merma. | La arquitectura protege auditoría, KPIs e impacto financiero como capacidades de negocio. |
| MRD vFinal | Mercado retail, segmentos y necesidad de diferenciación. | Los módulos reflejan roles reales y necesidades del canal retail. |
| PRD vFinal | Épicas de registro, validación, acción comercial, alertas, dashboard e IA. | Cada épica se proyecta a bounded context y casos de uso. |
| FSD vFinal | Casos de uso, reglas, Gherkin, NFRs y prompt-contratos. | Cada UC debe mapearse a puerto, servicio de aplicación y test. |
| DTI futuro | Arquitectura alto nivel, hexagonal, distribuida, event-driven, IA y AWS. | El DTI debe implementar esta decisión como eje técnico. |
| POCs futuras | POC-01 rendimiento/trazabilidad y POC-02 IA/guardrails. | Validan que la decisión sea viable. |
| AGENTS.md futuro | Reglas para agentes IA de desarrollo. | Evita drift y mantiene trazabilidad FSD→código. |

---

## 24. Antipatrones evitados

| Antipatrón | Cómo se evita |
|---|---|
| Big Ball of Mud | Módulos por bounded context, reglas de dependencia y puertos. |
| God Service | Casos de uso separados por módulo, no un servicio gigante. |
| Anemic Domain Model | Reglas de negocio dentro del dominio, no solo DTOs. |
| Distributed Monolith | No se separan microservicios sin ownership, datos y despliegue independiente. |
| Chatty Services | Se evita microservicio temprano con llamadas síncronas en cascada. |
| Data Swamp | Auditoría, ownership de datos y read models definidos. |
| AI Autopilot Risk | IA no ejecuta decisiones irreversibles sin humano. |
| Documentation Drift | ADR→DTI→AGENTS→PROMPT_MAPPING como cadena obligatoria. |

---

## 25. Decisiones explícitamente no tomadas en este ADR

| Tema | Motivo | Documento/ADR futuro |
|---|---|---|
| Servicios AWS definitivos | Requiere mapeo completo del DTI. | ADR-0005 |
| Broker/event bus final | Requiere diseño de eventos y garantías. | ADR-0003 |
| Estrategia Outbox detallada | Depende de eventos críticos y POC. | ADR-0003 |
| Modelo IA definitivo | Requiere evaluación de calidad, costo y guardrails. | ADR-0004 |
| Extracción real a microservicios | Depende de métricas futuras. | ADR posterior |
| Estrategia de cache | Depende de perfiles de carga reales. | DTI/POC |

---

## 26. Guion de defensa oral de este ADR

Para defender este ADR ante el docente:

> “Elegimos monolito modular con arquitectura hexagonal porque App Detección Prod aún está en etapa de consolidación de dominio y no tiene evidencia real que justifique microservicios completos. Sin embargo, el problema sí requiere rigor: trazabilidad, reglas de negocio claras, auditoría, acciones comerciales, KPIs e IA controlada. Un MVC simple sería rápido pero débil; microservicios serían sofisticados pero prematuros. La opción intermedia nos permite proteger el dominio, mapear cada caso de uso del FSD a puertos y adaptadores, preparar eventos internos y dejar seams para evolucionar a microservicios, CQRS o workers asíncronos cuando existan métricas reales.”

Posible pregunta del docente:

**¿Por qué no microservicios desde el inicio?**

Respuesta:

> “Porque no tenemos todavía evidencia de carga diferenciada, equipos autónomos por dominio ni necesidad de despliegue independiente. Implementarlos ahora aumentaría la complejidad operativa, la consistencia eventual y el riesgo de distributed monolith. La decisión no bloquea microservicios: los prepara mediante bounded contexts, puertos, eventos y ownership de datos.”

Posible pregunta:

**¿Cómo demuestras que no será un monolito desordenado?**

Respuesta:

> “Con reglas explícitas: dominio sin dependencias de framework, casos de uso como puertos de entrada, adaptadores de salida para infraestructura, ownership por módulo, auditoría obligatoria y tests de arquitectura. Además, AGENTS.md debe impedir que agentes IA creen código fuera de esta estructura.”

---

## 27. Referencias internas

- `docs/brd/BRD_vFinal.md`
- `docs/mrd/MRD_vFinal.md`
- `docs/prd/PRD_vFinal.md`
- `docs/fsd/FSD_vFinal.md`
- `docs/DTI.md` — pendiente
- `AGENTS.md` — pendiente
- `docs/PROMPT_MAPPING.md` — pendiente
- `pocs/POC-01/POC-01.md` — pendiente
- `pocs/POC-02/POC-02.md` — pendiente

---

## 28. Referencias conceptuales

- Robert C. Martin — Clean Architecture: independencia del dominio frente a detalles de infraestructura.
- Simon Brown — C4 Model: documentación por niveles de abstracción.
- Chris Richardson — Microservices Patterns: microservicios, sagas, outbox, event-driven y consistencia distribuida.
- AWS Well-Architected Framework: excelencia operacional, seguridad, confiabilidad, performance y costos.
- Dual-Track Agile / Continuous Discovery: validación continua de hipótesis antes de escalar decisiones.

---

## 29. Historial

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v0.1 | 26/05/2026 | Gina Fabiana Villanueva Viscarra | Creación inicial del ADR-0001 para revisión. |
| v0.2 | 26/05/2026 | Gina Fabiana Villanueva Viscarra | Mejora con matriz ponderada, relación DTI/C4/AGENTS, consistencia, IA, AWS, guion de defensa y validación. |

---

## 30. Checklist de aprobación

- [ ] La decisión está alineada con BRD, MRD, PRD y FSD aprobados.
- [ ] Se evaluaron al menos 3 alternativas reales.
- [ ] Se explica por qué MVC simple es insuficiente.
- [ ] Se explica por qué microservicios completos son prematuros.
- [ ] Se incluye matriz ponderada de decisión.
- [ ] Se describen fuerzas, drivers y trade-offs.
- [ ] Se definen módulos, puertos de entrada y puertos de salida.
- [ ] Se establece relación con DTI, C4, AGENTS.md y POCs.
- [ ] Se incorpora ruta a event-driven y Outbox futuro.
- [ ] Se define relación con IA y guardrails.
- [ ] Se identifica impacto AWS sin cerrar ADR-0005.
- [ ] Se registran riesgos y mitigaciones.
- [ ] Se incluye plan de reversión/evolución.
- [ ] Se puede defender oralmente en Q&A docente.
---

## Actualización transversal v1.1 — Control de cambios de precio y KPI de precio intervenido

> **Motivo de la actualización:** durante la revisión del paquete aprobado se identificó que el cambio de precio estaba mencionado como dato operativo, pero no suficientemente elevado a indicador estratégico, regla de trazabilidad, evento auditable y métrica de decisión gerencial. Esta actualización corrige ese vacío y alinea BRD → MRD → PRD → FSD → ADR → DTI.

### 1. Principio de negocio actualizado

En App Detección Prod, todo producto próximo a vencer que reciba una acción comercial debe conservar una trazabilidad completa de precio:

- **precio base / precio actual en sala** antes de la intervención;
- **precio sugerido**, cuando exista recomendación previa;
- **precio aprobado**, cuando supervisor, vendedor o política comercial autorice la acción;
- **precio aplicado en sala**, cuando la acción se ejecuta físicamente;
- **motivo del cambio**: descuento, bandeo, promoción, liquidación, retiro, corrección de sala u otra política comercial;
- **responsable y fecha/hora** de cada cambio;
- **cantidad intervenida** asociada a ese precio;
- **impacto financiero estimado y real**.

Sin esta trazabilidad, el sistema podría registrar que “se hizo una acción comercial”, pero no podría demostrar si la acción protegió margen, redujo merma o solo trasladó pérdida por descuento excesivo.

### 2. KPIs nuevos o reforzados

| ID | KPI | Definición | Fórmula / cálculo | Fuente | Consumidor | Frecuencia / frescura |
|---|---|---|---|---|---|---|
| KPI-PRECIO-01 | **Cobertura de precio intervenido** | Porcentaje de acciones comerciales que registran precio anterior y precio nuevo. | acciones con `oldPrice` + `newPrice` / total de acciones comerciales | Acción comercial / auditoría | Supervisor, Gerencia, Finanzas | Inmediata al registrar acción |
| KPI-PRECIO-02 | **Variación promedio de precio por intervención** | Mide el descuento o cambio promedio aplicado sobre productos próximos a vencer. | promedio((precio anterior - precio nuevo) / precio anterior) × 100 | Acción comercial | Gerencia, Finanzas | Dashboard diario y consulta inmediata |
| KPI-PRECIO-03 | **Valor económico intervenido por cambio de precio** | Monto económico afectado por descuentos, bandeos o promociones. | (precio anterior - precio nuevo) × cantidad intervenida | Acción comercial + cantidad | Gerencia, Finanzas | Inmediata para dashboard crítico |
| KPI-PRECIO-04 | **Acciones con cambio de precio sin aprobación** | Detecta riesgo de control interno. | acciones con `newPrice` distinto de `oldPrice` y sin aprobador / total acciones con cambio | Auditoría / workflow | Supervisor, Gerencia | Inmediata y con alerta |
| KPI-PRECIO-05 | **Diferencia entre precio aprobado y precio aplicado** | Controla desviaciones entre decisión comercial y ejecución en sala. | abs(precio aplicado - precio aprobado) | Validación / evidencia de sala | Supervisor, Vendedor, Auditoría | Inmediata cuando se valida ejecución |
| KPI-PRECIO-06 | **Margen protegido estimado** | Estima valor recuperado frente al escenario de vencimiento o devolución. | ingreso por venta intervenida - pérdida esperada por vencimiento/devolución | Dashboard financiero | Gerencia, Finanzas | Diario / cierre de caso |

### 3. Regla transversal de trazabilidad

**RB-PRECIO-001:** Ninguna acción comercial que implique descuento, bandeo, promoción, liquidación o modificación de precio puede cerrarse sin registrar precio anterior, precio nuevo, cantidad intervenida, responsable, fecha/hora, motivo y evidencia de ejecución cuando aplique.

**RB-PRECIO-002:** Todo cambio de precio debe generar una entrada de auditoría y, si el cambio supera el umbral definido por política comercial, debe requerir aprobación humana explícita.

**RB-PRECIO-003:** El dashboard gerencial debe mostrar KPIs críticos de cambio de precio desde estado confirmado/transaccional o desde una proyección operacional con frescura controlada. No debe basarse únicamente en procesos batch manuales.

### 4. Trazabilidad actualizada

| Capa | Elemento actualizado | Trazabilidad |
|---|---|---|
| BRD | Objetivos, KPIs y reglas de negocio | Control de precio como indicador de rentabilidad y no solo como campo operativo |
| MRD | Necesidad de mercado y propuesta de valor | Diferenciación frente a WhatsApp/Excel: medición formal del impacto de precio |
| PRD | Requerimientos y user stories | Registro, aprobación, consulta y auditoría de cambios de precio |
| FSD | Casos de uso, reglas, datos y Gherkin | `FSD-UC-003`, `FSD-UC-004`, `FSD-UC-005`, `FSD-UC-010` |
| ADR-0001 | Estilo arquitectónico | El precio intervenido es parte del dominio core, no un reporte periférico |
| ADR-0002 | Arquitectura hexagonal | Los cambios de precio deben vivir en casos de uso y puertos del dominio |
| ADR-0003 | Event-driven + dashboard | `PriceChanged.v1` y KPIs críticos de precio se actualizan con consistencia operacional inmediata |
| ADR-0004 | IA con guardrails | La IA puede sugerir o explicar, pero no cambiar precios automáticamente |
| ADR-0005 | AWS / observabilidad | Métricas de precio deben observarse, auditarse y protegerse como dato comercial sensible |

### 5. Impacto en defensa

Esta actualización permite defender que App Detección Prod no solo detecta productos próximos a vencer, sino que mide si la intervención comercial fue económicamente correcta. El precio deja de ser un campo de formulario y se convierte en variable de gobierno comercial, trazabilidad, auditoría, rentabilidad y decisión gerencial.


### 6. Impacto específico en ADR-0001

El control de cambios de precio refuerza la decisión de no tratar App Detección Prod como una simple aplicación CRUD. La variación de precio, la cantidad intervenida y el impacto económico pertenecen al **dominio core** del producto. Por eso el estilo macroarquitectónico debe preservar reglas de negocio, trazabilidad y evolución, en lugar de acoplar estos cálculos a reportes o pantallas.
