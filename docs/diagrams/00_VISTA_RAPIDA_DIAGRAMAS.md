# Vista rápida — Diagramas Mermaid App Detección Prod
Este archivo permite visualizar los diagramas directamente en GitHub o en un visor Markdown con soporte Mermaid.

## 01_c4_context_profesional.mmd
```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Arial, sans-serif", "primaryColor": "#E8F1FF", "primaryTextColor": "#0B1F3A", "primaryBorderColor": "#2F6FED", "lineColor": "#5B6B7A", "secondaryColor": "#F6F8FA", "tertiaryColor": "#FFF7E6", "clusterBkg": "#F8FAFC", "clusterBorder": "#CBD5E1"}, "flowchart": {"curve": "basis", "htmlLabels": true, "nodeSpacing": 45, "rankSpacing": 55}, "sequence": {"mirrorActors": false, "showSequenceNumbers": true}}}%%

flowchart LR
  %% C4 Nivel 1 — Contexto
  title["C4 Nivel 1 — Contexto del Sistema App Detección Prod"]

  subgraph Operacion["Nivel operativo y táctico"]
    M["Mercaderista\nRegistra producto, evidencia, precio y cantidad"]
    V["Vendedor Canal Moderno\nDefine/ejecuta acción comercial"]
    S["Supervisor Regional\nValida, prioriza y controla SLA"]
  end

  subgraph Estrategia["Nivel estratégico"]
    G["Gerencia Comercial\nConsulta KPIs, margen, merma, rotación y precio"]
    F["Finanzas / Administración\nEvalúa impacto económico y desviaciones"]
  end

  SYS[["App Detección Prod\nPlataforma trazable para productos próximos a vencer\nregistro + acciones + precio + dashboard + IA asistiva"]]

  subgraph Externos["Sistemas / canales externos"]
    ERP[("ERP / Inventario futuro\nstock, costo, ventas")]
    POS[("POS / Ventas futuro\nrotación real")]
    WA["WhatsApp / Excel actual\ncanal a reemplazar"]
    AWS["AWS Cloud\ndespliegue, seguridad, observabilidad"]
  end

  M -->|Reporta producto, lote, vencimiento, foto, precio actual| SYS
  V -->|Registra acción comercial, descuento, bandeo, precio nuevo| SYS
  S -->|Valida, aprueba, prioriza, solicita corrección| SYS
  G -->|Consulta dashboard inmediato y KPIs financieros| SYS
  F -->|Audita impacto, margen protegido y diferencias de precio| SYS

  SYS <-->|Integración planificada| ERP
  SYS <-->|Integración planificada| POS
  WA -. proceso actual a sustituir .-> SYS
  SYS -->|Infraestructura segura y observable| AWS

  classDef actor fill:#E8F1FF,stroke:#2F6FED,stroke-width:1.5px,color:#0B1F3A;
  classDef system fill:#DCFCE7,stroke:#16A34A,stroke-width:2px,color:#052E16;
  classDef external fill:#FFF7E6,stroke:#F59E0B,stroke-width:1.5px,color:#3B2500;
  class M,V,S,G,F actor;
  class SYS system;
  class ERP,POS,WA,AWS external;
```

## 02_c4_container_profesional.mmd
```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Arial, sans-serif", "primaryColor": "#E8F1FF", "primaryTextColor": "#0B1F3A", "primaryBorderColor": "#2F6FED", "lineColor": "#5B6B7A", "secondaryColor": "#F6F8FA", "tertiaryColor": "#FFF7E6", "clusterBkg": "#F8FAFC", "clusterBorder": "#CBD5E1"}, "flowchart": {"curve": "basis", "htmlLabels": true, "nodeSpacing": 45, "rankSpacing": 55}, "sequence": {"mirrorActors": false, "showSequenceNumbers": true}}}%%

flowchart TB
  title["C4 Nivel 2 — Contenedores técnicos y responsabilidades"]

  subgraph Users["Usuarios"]
    MobileUser["Mercaderista / Vendedor\nMóvil / Web responsive"]
    SupervisorUser["Supervisor\nWeb operativo"]
    ManagerUser["Gerencia / Finanzas\nDashboard ejecutivo"]
  end

  subgraph App["App Detección Prod — Monolito modular evolutivo"]
    FE["Frontend Web/Móvil\nUX por rol, formularios guiados, dashboard"]
    API["API Backend Modular\nAutenticación, RBAC, casos de uso"]
    CORE["Core de Dominio Hexagonal\nreglas, workflows, KPIs, precio"]
    DASH["Read Model Dashboard Inmediato\nKPIs críticos actualizados al commit"]
    OUTBOX["Outbox Transaccional\neventos confiables post-commit"]
    WORKER["Workers Asíncronos\nalertas, notificaciones, auditoría enriquecida"]
    AI["Adaptador IA\nclasificación, resumen, recomendación con guardrails"]
  end

  subgraph Data["Datos"]
    DB[("PostgreSQL / RDS\nfuente de verdad transaccional")]
    OBJ[("S3\nevidencia visual / fotos")]
    AUD[("Audit Log\nhistorial de cambios y decisiones")]
  end

  subgraph Cloud["AWS / evolución"]
    EB["EventBridge / SQS\neventos y colas"]
    SNS["SNS / Email / Push\nnotificaciones"]
    CW["CloudWatch + Logs\nobservabilidad"]
    IAM["IAM / Secrets / KMS\nseguridad"]
  end

  MobileUser --> FE
  SupervisorUser --> FE
  ManagerUser --> FE
  FE --> API
  API --> CORE
  CORE --> DB
  CORE --> DASH
  CORE --> OUTBOX
  FE --> DASH
  CORE --> OBJ
  CORE --> AUD
  OUTBOX --> WORKER
  WORKER --> EB
  WORKER --> SNS
  WORKER --> AUD
  AI --> CORE
  WORKER --> AI
  API --> CW
  WORKER --> CW
  DB --> CW
  API --> IAM
  AI --> IAM

  classDef user fill:#E8F1FF,stroke:#2563EB,color:#0B1F3A;
  classDef core fill:#DCFCE7,stroke:#16A34A,stroke-width:2px,color:#052E16;
  classDef data fill:#F3E8FF,stroke:#7E22CE,color:#2E1065;
  classDef cloud fill:#FFF7E6,stroke:#F59E0B,color:#3B2500;
  class MobileUser,SupervisorUser,ManagerUser user;
  class FE,API,CORE,DASH,OUTBOX,WORKER,AI core;
  class DB,OBJ,AUD data;
  class EB,SNS,CW,IAM cloud;
```

## 03_c4_component_core_profesional.mmd
```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Arial, sans-serif", "primaryColor": "#E8F1FF", "primaryTextColor": "#0B1F3A", "primaryBorderColor": "#2F6FED", "lineColor": "#5B6B7A", "secondaryColor": "#F6F8FA", "tertiaryColor": "#FFF7E6", "clusterBkg": "#F8FAFC", "clusterBorder": "#CBD5E1"}, "flowchart": {"curve": "basis", "htmlLabels": true, "nodeSpacing": 45, "rankSpacing": 55}, "sequence": {"mirrorActors": false, "showSequenceNumbers": true}}}%%

flowchart TB
  title["C4 Nivel 3 — Componentes internos del Core"]

  subgraph API["Capa de entrada / inbound adapters"]
    REST["REST Controllers\nvalidan contrato HTTP"]
    AUTH["Auth/RBAC Filter\nrol, permiso, alcance"]
  end

  subgraph Application["Capa de aplicación / casos de uso"]
    UC1["RegistrarProductoProximoVencer"]
    UC2["ValidarReporteProducto"]
    UC3["RegistrarAccionComercial"]
    UC4["RegistrarCambioPrecio"]
    UC5["CalcularKPIsDashboard"]
    UC6["ClasificarRiesgoIA"]
  end

  subgraph Domain["Dominio protegido"]
    AG1["ProductoReportado\nagregado raíz"]
    AG2["AccionComercial\ndescuento, bandeo, retiro"]
    AG3["PrecioIntervenido\nprecio anterior/nuevo/aprobado/aplicado"]
    POL["Políticas de negocio\n3 meses, criticidad, aprobaciones"]
    EVT["Eventos de dominio\nProductReported, PriceChanged, ActionApplied"]
  end

  subgraph Ports["Puertos"]
    RepoPort["ProductoRepositoryPort"]
    EvidencePort["EvidenceStoragePort"]
    EventPort["DomainEventPublisherPort"]
    AIPort["RiskClassifierPort"]
    AuditPort["AuditLogPort"]
    DashboardPort["DashboardProjectionPort"]
  end

  subgraph Outbound["Adaptadores de salida"]
    DB["PostgreSQL Adapter"]
    S3["S3 Evidence Adapter"]
    Outbox["Outbox Adapter"]
    IA["LLM/IA Adapter"]
    Audit["Audit Adapter"]
    Dash["Dashboard Read Model Adapter"]
  end

  REST --> AUTH --> UC1
  AUTH --> UC2
  AUTH --> UC3
  AUTH --> UC4
  AUTH --> UC5
  AUTH --> UC6

  UC1 --> AG1
  UC2 --> AG1
  UC3 --> AG2
  UC4 --> AG3
  UC5 --> POL
  UC6 --> POL
  AG1 --> EVT
  AG2 --> EVT
  AG3 --> EVT
  POL --> EVT

  UC1 --> RepoPort
  UC1 --> EvidencePort
  UC2 --> AuditPort
  UC3 --> EventPort
  UC4 --> DashboardPort
  UC4 --> EventPort
  UC6 --> AIPort

  RepoPort --> DB
  EvidencePort --> S3
  EventPort --> Outbox
  AIPort --> IA
  AuditPort --> Audit
  DashboardPort --> Dash

  classDef app fill:#E8F1FF,stroke:#2563EB,color:#0B1F3A;
  classDef domain fill:#DCFCE7,stroke:#16A34A,stroke-width:2px,color:#052E16;
  classDef port fill:#FEF3C7,stroke:#D97706,color:#3B2500;
  classDef adapter fill:#F3E8FF,stroke:#7E22CE,color:#2E1065;
  class REST,AUTH,UC1,UC2,UC3,UC4,UC5,UC6 app;
  class AG1,AG2,AG3,POL,EVT domain;
  class RepoPort,EvidencePort,EventPort,AIPort,AuditPort,DashboardPort port;
  class DB,S3,Outbox,IA,Audit,Dash adapter;
```

## 04_hexagonal_core_profesional.mmd
```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Arial, sans-serif", "primaryColor": "#E8F1FF", "primaryTextColor": "#0B1F3A", "primaryBorderColor": "#2F6FED", "lineColor": "#5B6B7A", "secondaryColor": "#F6F8FA", "tertiaryColor": "#FFF7E6", "clusterBkg": "#F8FAFC", "clusterBorder": "#CBD5E1"}, "flowchart": {"curve": "basis", "htmlLabels": true, "nodeSpacing": 45, "rankSpacing": 55}, "sequence": {"mirrorActors": false, "showSequenceNumbers": true}}}%%

flowchart LR
  title["Arquitectura Hexagonal — Dominio aislado de infraestructura"]

  subgraph Inbound["Adaptadores de entrada"]
    Web["Web/Móvil UI"]
    Api["REST API"]
    Batch["Job programado\nalertas por vencimiento"]
    Test["Tests / POCs"]
  end

  subgraph Hexagon["Núcleo hexagonal"]
    subgraph AppLayer["Casos de uso"]
      U1["Registrar producto"]
      U2["Validar reporte"]
      U3["Aplicar acción comercial"]
      U4["Cambiar precio"]
      U5["Actualizar dashboard"]
      U6["Solicitar clasificación IA"]
    end
    subgraph DomLayer["Dominio"]
      D1["Reglas de vencimiento"]
      D2["Política de precio"]
      D3["Política de aprobación"]
      D4["Eventos de dominio"]
    end
  end

  subgraph Outbound["Adaptadores de salida"]
    Pg["PostgreSQL/RDS"]
    S3["S3 evidencia visual"]
    Outbox["Outbox + EventBridge/SQS"]
    AI["Proveedor IA"]
    Notify["Notificaciones"]
    Obs["Logs/Métricas"]
  end

  Web --> Api --> U1
  Api --> U2
  Api --> U3
  Api --> U4
  Batch --> U5
  Test --> U1
  U1 --> D1
  U2 --> D3
  U3 --> D2
  U4 --> D2
  U5 --> D4
  U6 --> D3
  D1 --> Pg
  D2 --> Pg
  D3 --> Pg
  D4 --> Outbox
  U1 --> S3
  U6 --> AI
  Outbox --> Notify
  Api --> Obs

  classDef inbound fill:#E8F1FF,stroke:#2563EB,color:#0B1F3A;
  classDef core fill:#DCFCE7,stroke:#16A34A,stroke-width:2px,color:#052E16;
  classDef outbound fill:#FFF7E6,stroke:#F59E0B,color:#3B2500;
  class Web,Api,Batch,Test inbound;
  class U1,U2,U3,U4,U5,U6,D1,D2,D3,D4 core;
  class Pg,S3,Outbox,AI,Notify,Obs outbound;
```

## 05_domain_model_profesional.mmd
```mermaid
classDiagram
  direction LR

  class ProductoReportado {
    +UUID id
    +String sku
    +String nombre
    +String lote
    +Date fechaVencimiento
    +int diasParaVencer
    +int cantidadDetectada
    +EstadoCaso estado
    +NivelRiesgo riesgo
    +registrar()
    +validar()
    +cerrar()
  }

  class Tienda {
    +UUID id
    +String nombre
    +String cadena
    +String zona
    +String ciudad
  }

  class EvidenciaVisual {
    +UUID id
    +String urlFoto
    +Date fechaCaptura
    +String hash
    +String calidad
  }

  class AccionComercial {
    +UUID id
    +TipoAccion tipo
    +String motivo
    +EstadoAprobacion estado
    +Date fechaAplicacion
    +aplicar()
    +aprobar()
    +rechazar()
  }

  class PrecioIntervenido {
    +Money precioAnterior
    +Money precioNuevoPropuesto
    +Money precioAprobado
    +Money precioAplicado
    +Decimal variacionPct
    +Money valorEconomicoIntervenido
    +calcularVariacion()
    +detectarDiferencia()
  }

  class Usuario {
    +UUID id
    +String nombre
    +Rol rol
    +String region
  }

  class DashboardKPI {
    +Money valorRiesgo
    +Money margenProtegido
    +Decimal variacionPrecioPromedio
    +int productosCriticos
    +int accionesPendientes
    +Date actualizadoEn
  }

  class EventoDominio {
    +UUID eventId
    +String tipo
    +Date occurredAt
    +String correlationId
    +String causationId
  }

  ProductoReportado "1" --> "1" Tienda : ocurre en
  ProductoReportado "1" --> "1..*" EvidenciaVisual : respalda
  ProductoReportado "1" --> "0..*" AccionComercial : gestiona
  AccionComercial "1" --> "0..1" PrecioIntervenido : puede modificar
  Usuario "1" --> "0..*" ProductoReportado : reporta/valida
  Usuario "1" --> "0..*" AccionComercial : aprueba/ejecuta
  ProductoReportado "1" --> "0..*" EventoDominio : emite
  PrecioIntervenido "1" --> "0..*" EventoDominio : PriceChanged
  DashboardKPI ..> ProductoReportado : consolida
  DashboardKPI ..> AccionComercial : mide impacto
  DashboardKPI ..> PrecioIntervenido : mide precio
```

## 06_sequence_registro_producto_profesional.mmd
```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Arial, sans-serif", "primaryColor": "#E8F1FF", "primaryTextColor": "#0B1F3A", "primaryBorderColor": "#2F6FED", "lineColor": "#5B6B7A", "secondaryColor": "#F6F8FA", "tertiaryColor": "#FFF7E6", "clusterBkg": "#F8FAFC", "clusterBorder": "#CBD5E1"}, "flowchart": {"curve": "basis", "htmlLabels": true, "nodeSpacing": 45, "rankSpacing": 55}, "sequence": {"mirrorActors": false, "showSequenceNumbers": true}}}%%

sequenceDiagram
  autonumber
  actor M as Mercaderista
  participant UI as App móvil/web
  participant API as API Backend
  participant UC as Caso de uso: RegistrarProducto
  participant DB as PostgreSQL/RDS
  participant S3 as S3 Evidencia
  participant Dash as Dashboard inmediato
  participant Outbox as Outbox
  participant Sup as Supervisor

  M->>UI: Captura producto, lote, vencimiento, cantidad, precio actual, foto
  UI->>API: POST /productos-reportados
  API->>UC: Validar contrato + rol Mercaderista
  UC->>UC: Aplicar reglas mínimas: datos obligatorios, vencimiento, evidencia
  UC->>S3: Guardar evidencia visual
  S3-->>UC: URL/hash de evidencia
  UC->>DB: Transacción: guardar ProductoReportado + estado PENDIENTE_VALIDACION
  UC->>Dash: Actualizar KPIs críticos del día desde transacción
  UC->>Outbox: Insertar ProductReported.v1 en la misma transacción
  DB-->>UC: Commit exitoso
  UC-->>API: Resultado + ID de caso
  API-->>UI: Confirmación y estado
  Outbox-->>Sup: Notificación/cola para revisión táctica
```

## 07_sequence_cambio_precio_profesional.mmd
```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Arial, sans-serif", "primaryColor": "#E8F1FF", "primaryTextColor": "#0B1F3A", "primaryBorderColor": "#2F6FED", "lineColor": "#5B6B7A", "secondaryColor": "#F6F8FA", "tertiaryColor": "#FFF7E6", "clusterBkg": "#F8FAFC", "clusterBorder": "#CBD5E1"}, "flowchart": {"curve": "basis", "htmlLabels": true, "nodeSpacing": 45, "rankSpacing": 55}, "sequence": {"mirrorActors": false, "showSequenceNumbers": true}}}%%

sequenceDiagram
  autonumber
  actor V as Vendedor
  actor S as Supervisor
  participant UI as App Web
  participant API as API Backend
  participant UC as Caso de uso: RegistrarCambioPrecio
  participant DB as PostgreSQL/RDS
  participant Dash as Dashboard Gerencial Inmediato
  participant Outbox as Outbox
  participant Audit as Auditoría
  actor G as Gerencia

  V->>UI: Propone cambio de precio por producto próximo a vencer
  UI->>API: POST /acciones/{id}/cambio-precio
  API->>UC: Validar permisos, producto, cantidad, motivo y evidencia
  UC->>DB: Leer precio anterior, precio aprobado vigente y stock/cantidad reportada
  UC->>UC: Calcular variación %, valor económico intervenido y diferencia aprobado/aplicado
  alt Cambio requiere aprobación
    UC->>DB: Guardar cambio como PENDIENTE_APROBACION
    UC->>Outbox: PriceChangeRequested.v1
    S->>UI: Revisa evidencia y aprueba/rechaza
    S->>API: PATCH /cambio-precio/{id}/aprobar
  end
  UC->>DB: Transacción: guardar precio aprobado/aplicado + responsable + motivo
  UC->>Dash: Actualizar KPI precio crítico inmediatamente al commit
  UC->>Audit: Registrar trazabilidad completa
  UC->>Outbox: PriceChanged.v1 + CommercialActionApplied.v1
  API-->>UI: Cambio registrado y auditable
  G->>Dash: Consulta variación de precio, valor intervenido y margen protegido actualizado
```

## 08_event_driven_outbox_dashboard_profesional.mmd
```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Arial, sans-serif", "primaryColor": "#E8F1FF", "primaryTextColor": "#0B1F3A", "primaryBorderColor": "#2F6FED", "lineColor": "#5B6B7A", "secondaryColor": "#F6F8FA", "tertiaryColor": "#FFF7E6", "clusterBkg": "#F8FAFC", "clusterBorder": "#CBD5E1"}, "flowchart": {"curve": "basis", "htmlLabels": true, "nodeSpacing": 45, "rankSpacing": 55}, "sequence": {"mirrorActors": false, "showSequenceNumbers": true}}}%%

flowchart TB
  title["Event-Driven + Outbox — Dashboard inmediato y procesos asíncronos seguros"]

  subgraph Sync["Ruta síncrona transaccional — no puede quedar desactualizada"]
    A["Comando de negocio\nregistrar producto / validar / cambiar precio"]
    B["Caso de uso del core\nreglas + autorización + cálculo KPI"]
    C[("PostgreSQL/RDS\nfuente de verdad")]
    D["Dashboard Read Model Inmediato\nKPIs críticos al commit"]
    E["Outbox row\nevento persistido en la misma transacción"]
  end

  subgraph Async["Ruta asíncrona — enriquecimiento, alertas e integración"]
    P["Outbox Poller / CDC"]
    Q["EventBridge / SQS"]
    R["Workers\nalertas, notificaciones, IA, auditoría enriquecida"]
    DLQ["DLQ\nfallos re-procesables"]
    AN["Analytics histórico\ntendencias, rotación, cohortes"]
    N["Notificaciones\nemail/push/WhatsApp futuro"]
  end

  A --> B --> C
  B --> D
  B --> E
  C -->|commit| D
  E --> P --> Q --> R
  R --> AN
  R --> N
  R -->|error permanente| DLQ
  DLQ -->|reintento controlado| R

  note1["Principio clave:\nGerencia decide con KPIs críticos del estado transaccional, no con proyecciones atrasadas."]
  note2["Outbox asegura que si hay commit de negocio, también existe evento auditable."]
  D --- note1
  E --- note2

  classDef sync fill:#DCFCE7,stroke:#16A34A,stroke-width:2px,color:#052E16;
  classDef async fill:#E8F1FF,stroke:#2563EB,color:#0B1F3A;
  classDef risk fill:#FEE2E2,stroke:#DC2626,color:#450A0A;
  class A,B,C,D,E sync;
  class P,Q,R,AN,N async;
  class DLQ risk;
```

## 09_ai_guardrails_human_loop_profesional.mmd
```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Arial, sans-serif", "primaryColor": "#E8F1FF", "primaryTextColor": "#0B1F3A", "primaryBorderColor": "#2F6FED", "lineColor": "#5B6B7A", "secondaryColor": "#F6F8FA", "tertiaryColor": "#FFF7E6", "clusterBkg": "#F8FAFC", "clusterBorder": "#CBD5E1"}, "flowchart": {"curve": "basis", "htmlLabels": true, "nodeSpacing": 45, "rankSpacing": 55}, "sequence": {"mirrorActors": false, "showSequenceNumbers": true}}}%%

flowchart LR
  title["IA con Guardrails — Asistencia, no autonomía comercial irreversible"]

  Input["Datos del caso\nproducto, vencimiento, precio, cantidad, foto, historial"] --> Pre["Preprocesamiento\nnormalización + validación + minimización de datos"]
  Pre --> GuardIn["Guardrails de entrada\nno secretos, no PII innecesaria, prompt seguro"]
  GuardIn --> AI["Modelo IA / LLM\nclasifica riesgo, resume evidencia, sugiere prioridad"]
  AI --> GuardOut["Guardrails de salida\nJSON schema, rangos permitidos, no acción irreversible"]
  GuardOut --> Explain["Explicación trazable\npor qué es riesgo alto/medio/bajo"]
  Explain --> Human["Human-in-the-loop\nSupervisor/Vendedor aprueba acción"]
  Human --> Core["Core transaccional\nregistra decisión humana"]
  Core --> Dash["Dashboard\nIA como señal, no fuente de verdad"]
  Core --> Audit["Auditoría\nprompt id, versión, usuario, decisión"]

  Bad["La IA NO puede:\n- cambiar precios automáticamente\n- retirar productos\n- aprobar descuentos\n- cerrar casos críticos"]
  GuardOut --- Bad

  classDef ai fill:#F3E8FF,stroke:#7E22CE,color:#2E1065;
  classDef control fill:#DCFCE7,stroke:#16A34A,stroke-width:2px,color:#052E16;
  classDef danger fill:#FEE2E2,stroke:#DC2626,color:#450A0A;
  class Input,Pre,GuardIn,AI,GuardOut,Explain ai;
  class Human,Core,Dash,Audit control;
  class Bad danger;
```

## 10_aws_deployment_profesional.mmd
```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Arial, sans-serif", "primaryColor": "#E8F1FF", "primaryTextColor": "#0B1F3A", "primaryBorderColor": "#2F6FED", "lineColor": "#5B6B7A", "secondaryColor": "#F6F8FA", "tertiaryColor": "#FFF7E6", "clusterBkg": "#F8FAFC", "clusterBorder": "#CBD5E1"}, "flowchart": {"curve": "basis", "htmlLabels": true, "nodeSpacing": 45, "rankSpacing": 55}, "sequence": {"mirrorActors": false, "showSequenceNumbers": true}}}%%

flowchart TB
  title["Deployment AWS — Evolución cloud segura y observable"]

  subgraph Internet["Acceso usuarios"]
    U1["Usuarios móviles/web"]
    DNS["Route 53"]
    CDN["CloudFront + WAF"]
  end

  subgraph VPC["VPC privada"]
    ALB["Application Load Balancer"]
    ECS["ECS Fargate / App Backend\nmonolito modular"]
    RDS[("Amazon RDS PostgreSQL\ntransaccional + dashboard inmediato")]
    S3["S3\nevidencias visuales"]
    SQS["SQS / EventBridge\neventos outbox"]
    Worker["Worker Fargate\nalertas, IA, auditoría"]
  end

  subgraph Security["Seguridad"]
    IAM["IAM Roles"]
    Secrets["Secrets Manager"]
    KMS["KMS Encryption"]
  end

  subgraph Observability["Observabilidad"]
    CW["CloudWatch Logs/Metrics"]
    Alarms["CloudWatch Alarms\nlatencia, errores, outbox lag, dashboard freshness"]
    XRay["X-Ray / tracing futuro"]
  end

  U1 --> DNS --> CDN --> ALB --> ECS
  ECS --> RDS
  ECS --> S3
  ECS --> SQS
  SQS --> Worker
  Worker --> RDS
  Worker --> S3
  ECS --> IAM
  ECS --> Secrets
  RDS --> KMS
  S3 --> KMS
  ECS --> CW
  Worker --> CW
  RDS --> CW
  CW --> Alarms
  ECS --> XRay

  classDef net fill:#E8F1FF,stroke:#2563EB,color:#0B1F3A;
  classDef compute fill:#DCFCE7,stroke:#16A34A,stroke-width:2px,color:#052E16;
  classDef sec fill:#FEE2E2,stroke:#DC2626,color:#450A0A;
  classDef obs fill:#FFF7E6,stroke:#F59E0B,color:#3B2500;
  class U1,DNS,CDN,ALB net;
  class ECS,RDS,S3,SQS,Worker compute;
  class IAM,Secrets,KMS sec;
  class CW,Alarms,XRay obs;
```

## 11_state_lifecycle_alerta_profesional.mmd
```mermaid
stateDiagram-v2
  [*] --> Reportado: Mercaderista registra producto
  Reportado --> PendienteValidacion: datos mínimos completos
  Reportado --> RequiereCorreccion: evidencia incompleta / datos ambiguos
  RequiereCorreccion --> Reportado: mercaderista corrige

  PendienteValidacion --> Validado: supervisor valida
  PendienteValidacion --> Rechazado: duplicado / falso positivo

  Validado --> Critico: vencimiento cercano / alto valor en riesgo
  Validado --> EnObservacion: riesgo medio / baja cantidad
  Validado --> AccionRequerida: requiere descuento, bandeo, retiro o precio

  Critico --> AccionRequerida: prioridad alta
  EnObservacion --> AccionRequerida: cambia condición / alerta automática

  AccionRequerida --> PrecioPendienteAprobacion: cambio de precio requerido
  PrecioPendienteAprobacion --> PrecioAprobado: supervisor/vendedor autorizado
  PrecioPendienteAprobacion --> AccionRequerida: rechazado o requiere ajuste

  PrecioAprobado --> AccionAplicada: se aplica precio/acción comercial
  AccionRequerida --> AccionAplicada: acción sin cambio de precio

  AccionAplicada --> CerradoVendido: producto vendido / rotado
  AccionAplicada --> CerradoRetirado: producto retirado / devolución
  AccionAplicada --> EscaladoGerencia: impacto económico alto o excepción
  EscaladoGerencia --> AccionAplicada: decisión ejecutiva

  Rechazado --> [*]
  CerradoVendido --> [*]
  CerradoRetirado --> [*]
```

## 12_traceability_map_profesional.mmd
```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Arial, sans-serif", "primaryColor": "#E8F1FF", "primaryTextColor": "#0B1F3A", "primaryBorderColor": "#2F6FED", "lineColor": "#5B6B7A", "secondaryColor": "#F6F8FA", "tertiaryColor": "#FFF7E6", "clusterBkg": "#F8FAFC", "clusterBorder": "#CBD5E1"}, "flowchart": {"curve": "basis", "htmlLabels": true, "nodeSpacing": 45, "rankSpacing": 55}, "sequence": {"mirrorActors": false, "showSequenceNumbers": true}}}%%

flowchart LR
  title["Mapa de trazabilidad — de necesidad de negocio a arquitectura y evidencia"]

  BRD["BRD\nproblema de negocio, KPIs, RACI, valor"] --> MRD["MRD\nmercado, segmentos, JTBD, competencia"]
  MRD --> PRD["PRD\nobjetivos, épicas, historias, NFRs"]
  PRD --> FSD["FSD\ncasos de uso, reglas, Gherkin, datos"]
  FSD --> ADR1["ADR-0001\nmonolito modular evolutivo"]
  FSD --> ADR2["ADR-0002\nhexagonal core"]
  FSD --> ADR3["ADR-0003\nevent-driven + outbox + dashboard inmediato"]
  FSD --> ADR4["ADR-0004\nIA con guardrails"]
  FSD --> ADR5["ADR-0005\nAWS + observabilidad + seguridad"]
  ADR1 --> DTI["DTI\ncontrato técnico rector"]
  ADR2 --> DTI
  ADR3 --> DTI
  ADR4 --> DTI
  ADR5 --> DTI
  DTI --> DIAG["Diagramas .mmd\nC4, dominio, flujos, AWS"]
  DTI --> POC["POCs\nrendimiento, outbox, IA, precio"]
  DTI --> AG["AGENTS.md\nreglas para agentes IA"]
  DTI --> PM["PROMPT_MAPPING.md\ntrazabilidad prompts → artefactos"]
  DTI --> ROAD["roadmap.md\nevolución técnica/producto"]

  KPI["KPI transversal precio\nprecio anterior/nuevo, variación, valor intervenido, diferencia aprobado/aplicado"]
  KPI -. aparece en .-> BRD
  KPI -. aparece en .-> PRD
  KPI -. aparece en .-> FSD
  KPI -. aparece en .-> ADR3
  KPI -. aparece en .-> ADR5
  KPI -. aparece en .-> DTI
  KPI -. valida .-> POC

  classDef doc fill:#E8F1FF,stroke:#2563EB,color:#0B1F3A;
  classDef arch fill:#DCFCE7,stroke:#16A34A,stroke-width:2px,color:#052E16;
  classDef kpi fill:#FFF7E6,stroke:#F59E0B,color:#3B2500;
  class BRD,MRD,PRD,FSD,DIAG,POC,AG,PM,ROAD doc;
  class ADR1,ADR2,ADR3,ADR4,ADR5,DTI arch;
  class KPI kpi;
```

## 13_observability_security_profesional.mmd
```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Arial, sans-serif", "primaryColor": "#E8F1FF", "primaryTextColor": "#0B1F3A", "primaryBorderColor": "#2F6FED", "lineColor": "#5B6B7A", "secondaryColor": "#F6F8FA", "tertiaryColor": "#FFF7E6", "clusterBkg": "#F8FAFC", "clusterBorder": "#CBD5E1"}, "flowchart": {"curve": "basis", "htmlLabels": true, "nodeSpacing": 45, "rankSpacing": 55}, "sequence": {"mirrorActors": false, "showSequenceNumbers": true}}}%%

flowchart TB
  title["Seguridad, auditoría y observabilidad — controles transversales"]

  subgraph Security["Seguridad"]
    RBAC["RBAC por rol\nMercaderista, Vendedor, Supervisor, Gerencia, Finanzas"]
    Auth["Autenticación\nJWT/OIDC futuro"]
    DataSec["Protección de datos\nKMS, Secrets, cifrado en reposo/tránsito"]
    Policy["Políticas de negocio\naprobación de precio, retiro, descuento"]
  end

  subgraph Audit["Auditoría"]
    AuditLog["Audit Log inmutable\nquién, qué, cuándo, antes/después"]
    Evidence["Evidencia visual\nhash + URL + timestamp"]
    PriceAudit["Auditoría de precio\nprecio anterior/nuevo/aprobado/aplicado"]
    AITrace["Trazabilidad IA\nprompt id, versión, salida, decisión humana"]
  end

  subgraph Observability["Observabilidad"]
    Logs["Logs estructurados\ncorrelationId, causationId"]
    Metrics["Métricas\nlatencia, errores, outbox lag, freshness dashboard"]
    Alerts["Alarmas\nSLO incumplido, DLQ, diferencias de precio"]
    DashOps["Dashboard operativo\nsalud técnica y negocio"]
  end

  Command["Comando crítico\nregistrar/cambiar precio/aprobar/cerrar"] --> RBAC --> Policy --> AuditLog
  Policy --> PriceAudit
  Command --> Evidence
  Command --> Logs
  Logs --> Metrics --> Alerts --> DashOps
  Command --> AITrace
  Auth --> RBAC
  DataSec --> AuditLog
  DataSec --> Evidence

  classDef sec fill:#FEE2E2,stroke:#DC2626,color:#450A0A;
  classDef aud fill:#FEF3C7,stroke:#D97706,color:#3B2500;
  classDef obs fill:#E8F1FF,stroke:#2563EB,color:#0B1F3A;
  class RBAC,Auth,DataSec,Policy sec;
  class AuditLog,Evidence,PriceAudit,AITrace aud;
  class Logs,Metrics,Alerts,DashOps obs;
```

## 14_poc_validation_map_profesional.mmd
```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Arial, sans-serif", "primaryColor": "#E8F1FF", "primaryTextColor": "#0B1F3A", "primaryBorderColor": "#2F6FED", "lineColor": "#5B6B7A", "secondaryColor": "#F6F8FA", "tertiaryColor": "#FFF7E6", "clusterBkg": "#F8FAFC", "clusterBorder": "#CBD5E1"}, "flowchart": {"curve": "basis", "htmlLabels": true, "nodeSpacing": 45, "rankSpacing": 55}, "sequence": {"mirrorActors": false, "showSequenceNumbers": true}}}%%

flowchart LR
  title["POCs y validación — riesgos arquitectónicos convertidos en evidencia"]

  subgraph Risks["Riesgos críticos"]
    R1["R1: registro lento en campo"]
    R2["R2: dashboard gerencial desactualizado"]
    R3["R3: pérdida/duplicidad de eventos"]
    R4["R4: IA produce recomendaciones inseguras"]
    R5["R5: cambios de precio sin trazabilidad"]
  end

  subgraph POCs["POCs propuestas"]
    P1["POC-01\nlatencia registro + dashboard inmediato"]
    P2["POC-02\noutbox + idempotencia + DLQ"]
    P3["POC-03\nIA con guardrails y human-in-the-loop"]
    P4["POC-04\nauditoría de cambio de precio"]
  end

  subgraph Metrics["Métricas de aceptación"]
    M1["p95 registro <= 500 ms"]
    M2["freshness dashboard <= 5 s\npara KPIs críticos"]
    M3["0 eventos perdidos\nidempotencia verificada"]
    M4["0 acciones irreversibles por IA"]
    M5["100% precio con antes/después/responsable"]
  end

  R1 --> P1 --> M1
  R2 --> P1 --> M2
  R3 --> P2 --> M3
  R4 --> P3 --> M4
  R5 --> P4 --> M5

  classDef risk fill:#FEE2E2,stroke:#DC2626,color:#450A0A;
  classDef poc fill:#DCFCE7,stroke:#16A34A,stroke-width:2px,color:#052E16;
  classDef metric fill:#E8F1FF,stroke:#2563EB,color:#0B1F3A;
  class R1,R2,R3,R4,R5 risk;
  class P1,P2,P3,P4 poc;
  class M1,M2,M3,M4,M5 metric;
```
