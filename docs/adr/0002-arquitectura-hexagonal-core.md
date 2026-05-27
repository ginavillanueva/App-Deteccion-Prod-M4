# ADR-0002: Arquitectura Hexagonal del Core Funcional de App Detección Prod

## Metadatos

| Campo | Valor |
|---|---|
| Número | ADR-0002 |
| Título | Arquitectura Hexagonal del Core Funcional de App Detección Prod |
| Fecha | 26/05/2026 |
| Producto | App Detección Prod |
| Rama objetivo | `release/2.0.0` |
| Estado | Propuesta para revisión |
| Autor | Gina Fabiana Villanueva Viscarra |
| Alcance | Diseño interno del core funcional: casos de uso, dominio, puertos, adaptadores, reglas, eventos, IA asistiva y pruebas |
| Documentos fuente | `docs/brd/BRD_vFinal.md`, `docs/mrd/MRD_vFinal.md`, `docs/prd/PRD_vFinal.md`, `docs/fsd/FSD_vFinal.md` |
| Documentos impactados | `docs/DTI.md` §3, §4, §5, §7, §9, §11, §12, §16, §17; `AGENTS.md`; `docs/PROMPT_MAPPING.md`; diagramas C4 nivel 3 y hexagonal |
| ADR relacionado | ADR-0001 — Estilo arquitectónico base: monolito modular evolutivo |
| Decisión previa asumida | El producto se construirá inicialmente como monolito modular evolutivo; este ADR profundiza únicamente en el diseño interno del core funcional. |

---

## 1. Propósito de este ADR y relación con ADR-0001

El ADR-0001 ya resolvió la decisión de **estilo arquitectónico base**: iniciar App Detección Prod como un **monolito modular evolutivo**, evitando microservicios prematuros y dejando fronteras claras para una posible evolución distribuida.

Este ADR no vuelve a decidir si el sistema será monolito, microservicios o serverless. Esa decisión ya fue tomada. Este ADR responde una pregunta más específica y profunda:

> **¿Cómo debe organizarse internamente el core funcional de App Detección Prod para que las reglas de negocio, los casos de uso, la trazabilidad, la auditoría y la futura integración con IA/eventos no queden acopladas a pantallas, base de datos, frameworks o servicios externos?**

Por tanto, el ADR-0002 profundiza en el **diseño interno** del monolito modular decidido en ADR-0001. Su objetivo es evitar que el producto se convierta en un CRUD acoplado y difícil de defender, y garantizar que el DTI pueda mostrar una arquitectura consistente con C4 nivel 3, hexagonal, NFRs, POCs, Prompt Mapping y futuras decisiones event-driven/cloud.

### 1.1 Diferencia exacta entre ADR-0001 y ADR-0002

| Aspecto | ADR-0001 | ADR-0002 |
|---|---|---|
| Pregunta que responde | ¿Cuál es el estilo arquitectónico base del producto? | ¿Cómo se estructura internamente el core del producto? |
| Nivel de decisión | Macroarquitectura | Arquitectura interna del core |
| Resultado | Monolito modular evolutivo | Arquitectura hexagonal por casos de uso, puertos y adaptadores |
| Riesgo mitigado | Microservicios prematuros o arquitectura sobredimensionada | CRUD acoplado, reglas dispersas, baja testabilidad y baja trazabilidad |
| Impacto principal | DTI §3, §6, §8, §17; roadmap técnico | DTI §4, §5, §7, §9, §11, §12; FSD, pruebas, PROMPT_MAPPING |
| Relación con evolución futura | Define que la evolución puede darse por bounded contexts | Define cómo aislar dominio y adaptadores para que esa evolución sea posible |

---

## 2. Contexto funcional del producto

App Detección Prod surge en empresas distribuidoras e importadoras que operan en canal retail, donde la gestión de productos próximos a vencer se realiza actualmente de forma informal, fragmentada y no estructurada. La operación depende de WhatsApp, Excel, fotografías sin estandarización y comunicación verbal. Esto produce falta de trazabilidad, ausencia de métricas, baja visibilidad estratégica, demoras de decisión, desalineación entre operación y gerencia, incremento de merma e imposibilidad de medir el impacto de descuentos, bandeos, promociones o retiros.

Los documentos aprobados del proyecto establecen que el producto no debe limitarse a capturar datos. Debe transformar un flujo operativo reactivo en una plataforma trazable y medible que conecte:

1. **Mercaderistas**, que registran productos próximos a vencer en tienda.
2. **Supervisores**, que validan información, priorizan casos y reducen incertidumbre.
3. **Vendedores**, que gestionan acciones comerciales como descuentos, bandeos, promociones o retiro.
4. **Gerencia Comercial**, que consume información consolidada, KPIs, impacto financiero, rotación y alertas para tomar decisiones estratégicas.

El FSD aprobado baja esta visión a casos de uso funcionales como:

| ID FSD | Caso de uso | Implicación arquitectónica |
|---|---|---|
| FSD-UC-001 | Registrar producto próximo a vencer | Requiere validaciones de datos, evidencia, tienda, lote, fecha, cantidad y precio. |
| FSD-UC-002 | Validar y priorizar alerta de producto crítico | Requiere reglas de prioridad, estados, auditoría y control táctico. |
| FSD-UC-003 | Registrar acción comercial aplicada | Requiere reglas sobre descuento, bandeo, promoción, retiro, nuevo precio y cantidad intervenida. |
| FSD-UC-004 | Aprobar o rechazar acción comercial | Requiere flujo de autorización, roles, reglas y trazabilidad. |
| FSD-UC-005 | Consultar dashboard gerencial | Requiere lectura agregada y métricas sin contaminar el dominio transaccional. |
| FSD-UC-006 | Generar alerta automática por umbral de vencimiento | Requiere cálculo de riesgo, scheduler/eventos y notificación. |
| FSD-UC-007 | Clasificar riesgo con IA | Requiere IA asistiva controlada por guardrails y no invasiva al dominio. |
| FSD-UC-008 | Auditar historial de cambios | Requiere eventos/auditoría como capacidad transversal. |

Estos casos de uso muestran que el core del producto contiene reglas reales: estados, umbrales, aprobaciones, cálculo de riesgo, impacto financiero, evidencia, historial y trazabilidad. Por eso, una implementación orientada solo a pantallas y tablas sería insuficiente para defender la calidad arquitectónica del proyecto.

---

## 3. Problema arquitectónico específico

El problema que resuelve este ADR es el riesgo de que la aplicación se implemente como un sistema CRUD acoplado, donde:

- las reglas de vencimiento estén dentro de controladores;
- los cálculos de prioridad estén mezclados con queries SQL;
- las reglas de aprobación comercial dependan de pantallas;
- el historial de auditoría dependa de actualizaciones manuales;
- la IA escriba directamente sobre entidades del negocio;
- la publicación de alertas esté acoplada a la persistencia;
- el dashboard gerencial lea directamente tablas transaccionales sin modelo de lectura controlado;
- las pruebas solo validen endpoints, no reglas de negocio;
- el código no pueda trazarse claramente contra FSD-UC, PRD-REQ o NFR.

Ese diseño podría funcionar en una demo superficial, pero no sostendría una defensa de arquitectura porque no demostraría separación de responsabilidades, testabilidad, trazabilidad ni preparación para evolución futura.

La pregunta de decisión queda formalizada así:

> **¿Qué estructura interna debe adoptar el core funcional para preservar reglas de negocio, trazabilidad y evolución, sin duplicar complejidad ni repetir la decisión macroarquitectónica del ADR-0001?**

---

## 4. Drivers arquitectónicos derivados de documentos aprobados

| Driver | Origen documental | Interpretación arquitectónica | Decisión derivada |
|---|---|---|---|
| Centralización del registro | BRD/MRD/PRD/FSD | El registro no es solo formulario; debe crear un caso trazable con evidencia y estado. | Caso de uso `RegistrarProductoProximoVencerUseCase`. |
| Trazabilidad de acciones comerciales | BRD/FSD | Cada descuento, bandeo, retiro o promoción debe quedar ligado al producto, usuario, tienda y fecha. | Entidad `AccionComercial` + puerto de auditoría. |
| Control de precios y cantidades | BRD/PRD/FSD | Precio actual, nuevo precio y cantidad intervenida son parte del valor de negocio. | Value Objects `Precio`, `Cantidad`, `PeriodoVencimiento`. |
| Validación táctica | Entrevista supervisor / FSD | El supervisor necesita validar, priorizar y reducir incertidumbre. | Caso de uso `ValidarAlertaProductoUseCase`. |
| Visibilidad gerencial | Entrevista gerente / PRD | Gerencia consume KPIs, no opera cada caso. | Separar comandos transaccionales de consultas analíticas. |
| Acción comercial ejecutable | Entrevista vendedor / FSD | El vendedor necesita claridad sobre qué acción fue tomada y estado actual. | Caso de uso `RegistrarAccionComercialUseCase`. |
| IA asistiva con control | PRD/FSD/DTI futuro | La IA puede clasificar riesgo, pero no aprobar decisiones irreversibles. | Puerto `RiskClassifierPort` con guardrails. |
| Auditoría | BRD/FSD | El sistema debe explicar quién hizo qué, cuándo y por qué. | Puerto `AuditLogPort` + eventos de dominio. |
| Evolución event-driven | ADR-0001 / DTI futuro | Alertas, notificaciones y dashboards pueden evolucionar a flujos asíncronos. | Puerto `DomainEventPublisherPort`. |
| Testabilidad | Rúbrica/FSD | La defensa debe evidenciar reglas verificables, no solo UI. | Dominio testeable sin framework ni BD. |

---

## 5. Alternativas consideradas

### 5.1 Alternativa A — MVC tradicional por capas técnicas

Estructurar el sistema como `Controller → Service → Repository`, con reglas dentro de servicios de aplicación y queries directas a base de datos.

**Ventajas**

- Rápida de implementar.
- Familiar para equipos pequeños.
- Suficiente para prototipos CRUD.

**Desventajas**

- Tiende a mezclar lógica de negocio con lógica de framework.
- Dificulta probar reglas sin base de datos o servidor web.
- Favorece servicios grandes y poco expresivos.
- Reduce trazabilidad entre FSD-UC y código.
- Dificulta evolucionar a eventos, IA, colas o integraciones sin reescritura.

**Evaluación para App Detección Prod**

No se elige porque el producto no es un CRUD simple. Tiene reglas de vencimiento, validación, aprobación, estados, evidencia, auditoría, impacto financiero y asistencia IA. MVC puede ser usado en adaptadores web, pero no como estructura del core.

---

### 5.2 Alternativa B — Arquitectura hexagonal dentro del monolito modular

Organizar el core por casos de uso, dominio, puertos de entrada, puertos de salida y adaptadores externos. El dominio queda independiente de framework, base de datos, IA, mensajería o UI.

**Ventajas**

- Protege reglas de negocio.
- Permite trazabilidad explícita FSD → Use Case → Test.
- Mejora testabilidad del dominio.
- Reduce acoplamiento con base de datos, frontend, IA y cloud.
- Permite incorporar eventos, notificaciones, IA y analytics mediante puertos.
- Es coherente con el monolito modular del ADR-0001.
- Evita sobreingeniería de microservicios manteniendo diseño profesional.

**Desventajas**

- Requiere disciplina de diseño.
- Introduce más clases/interfaces que un CRUD básico.
- Puede ser mal aplicada si se crean puertos innecesarios.
- Exige convenciones claras en `AGENTS.md` y DTI.

**Evaluación para App Detección Prod**

Es la opción elegida porque equilibra calidad arquitectónica y complejidad razonable. Permite defender el core del producto sin sobredimensionarlo.

---

### 5.3 Alternativa C — Clean Architecture estricta

Aplicar capas concéntricas formales: entities, use cases, interface adapters, frameworks/drivers.

**Ventajas**

- Muy fuerte en independencia del dominio.
- Buena para sistemas complejos y longevos.
- Se alinea con principios de arquitectura limpia.

**Desventajas**

- Puede ser más rígida y pesada para el alcance actual.
- Riesgo de documentación excesiva sin implementación proporcional.
- Puede duplicar abstracciones si no se aplica con criterio.

**Evaluación para App Detección Prod**

Se descarta como forma estricta, pero se toman sus principios: independencia del dominio, inversión de dependencias, casos de uso explícitos y separación de detalles técnicos.

---

### 5.4 Alternativa D — Microservicios por bounded context desde el inicio

Crear servicios separados para detección, acciones comerciales, supervisión, analytics, notificaciones e IA.

**Ventajas**

- Escalabilidad y despliegue independiente.
- Separación fuerte por dominio.
- Alineación con arquitectura distribuida avanzada.

**Desventajas**

- Repite y contradice el análisis del ADR-0001 si se adopta ahora.
- Aumenta complejidad operativa.
- Exige observabilidad distribuida, contratos, eventos, versionado y DevOps maduros.
- Riesgo de distributed monolith.

**Evaluación para App Detección Prod**

No se elige para el estado actual del producto. Sus fronteras se preparan mediante módulos y puertos, pero no se distribuyen físicamente aún.

---

## 6. Matriz de decisión

Escala: 1 = bajo / 5 = alto. Peso según importancia para este proyecto.

| Criterio | Peso | MVC tradicional | Hexagonal en monolito modular | Clean estricta | Microservicios iniciales |
|---|---:|---:|---:|---:|---:|
| Trazabilidad FSD → código → pruebas | 5 | 2 | 5 | 5 | 4 |
| Protección de reglas de negocio | 5 | 2 | 5 | 5 | 4 |
| Simplicidad operativa | 4 | 5 | 4 | 3 | 1 |
| Preparación para IA/eventos | 4 | 2 | 5 | 4 | 5 |
| Facilidad de defensa arquitectónica | 5 | 2 | 5 | 4 | 4 |
| Riesgo de sobreingeniería | 4 | 5 | 4 | 3 | 1 |
| Evolución futura | 4 | 2 | 5 | 4 | 5 |
| Testabilidad | 5 | 2 | 5 | 5 | 4 |
| **Resultado ponderado** | — | **80** | **156** | **143** | **120** |

**Conclusión:** la arquitectura hexagonal dentro del monolito modular es la opción más equilibrada. Maximiza trazabilidad, protección del dominio y evolución futura sin asumir los costos operativos de una arquitectura distribuida completa.

---

## 7. Decisión

Se decide adoptar **Arquitectura Hexagonal para el core funcional de App Detección Prod**, organizada alrededor de casos de uso del FSD, entidades de dominio, value objects, servicios de dominio, puertos de entrada, puertos de salida y adaptadores.

La regla central será:

> **El dominio y los casos de uso no dependerán de frameworks, base de datos, frontend, servicios cloud, IA, mensajería ni APIs externas. Todos esos elementos serán detalles implementados mediante adaptadores.**

La arquitectura interna queda definida así:

```text
app-deteccion-prod/
└── backend/
    └── src/main/
        └── java/.../appdeteccion/
            ├── detection/                  # Módulo: detección de producto próximo a vencer
            │   ├── domain/                 # Entidades, Value Objects, reglas puras
            │   ├── application/            # Casos de uso y orquestación
            │   │   ├── port/in/            # Puertos de entrada
            │   │   └── port/out/           # Puertos de salida
            │   └── adapter/                # Web, persistence, events, AI, storage
            │       ├── in/web/
            │       ├── out/persistence/
            │       ├── out/events/
            │       ├── out/storage/
            │       └── out/ai/
            │
            ├── commercialaction/           # Módulo: acciones comerciales
            ├── supervision/                # Módulo: validación y priorización
            ├── analytics/                  # Módulo: KPIs y dashboard
            ├── notification/               # Módulo: alertas/notificaciones
            └── sharedkernel/               # Tipos compartidos controlados
```

---

## 8. Modelo hexagonal propuesto

### 8.1 Núcleo de dominio

El dominio contendrá conceptos estables del negocio, no conceptos técnicos.

| Tipo | Nombre | Responsabilidad | Reglas principales |
|---|---|---|---|
| Aggregate Root | `ProductoDetectado` | Representa un producto próximo a vencer reportado en una tienda. | Debe tener tienda, producto, fecha de vencimiento, cantidad, precio actual, evidencia y estado. |
| Entity | `AlertaVencimiento` | Representa una alerta asociada al riesgo de vencimiento. | Puede estar en estado `NUEVA`, `VALIDADA`, `PRIORIZADA`, `DESCARTADA`, `ACCION_EN_CURSO`, `CERRADA`. |
| Entity | `AccionComercial` | Representa una acción aplicada: descuento, bandeo, promoción, retiro o reposición. | Debe registrar responsable, tipo, precio nuevo si aplica, cantidad intervenida y justificación. |
| Entity | `EvidenciaVisual` | Referencia controlada a imagen/foto del producto. | No debe almacenar binarios en dominio; solo referencia, metadata y validación mínima. |
| Value Object | `FechaVencimiento` | Fecha crítica de producto. | Calcula días restantes y umbral de riesgo. |
| Value Object | `Precio` | Precio actual o intervenido. | No acepta valores negativos; moneda explícita. |
| Value Object | `Cantidad` | Cantidad reportada/intervenida. | No acepta cero cuando el producto está reportado como disponible. |
| Value Object | `RiesgoVencimiento` | Clasificación bajo/medio/alto/crítico. | Derivado de días restantes, cantidad, rotación y acción comercial. |
| Domain Service | `PoliticaPriorizacionVencimiento` | Determina prioridad de atención. | Aplica reglas declaradas en FSD y NFRs. |
| Domain Service | `CalculadoraImpactoFinanciero` | Calcula pérdida evitada o impacto estimado. | Usa precio, cantidad, descuento y costo asociado si existe. |

### 8.2 Puertos de entrada

Cada caso de uso crítico del FSD tendrá un puerto de entrada explícito.

| Puerto de entrada | FSD relacionado | Responsabilidad |
|---|---|---|
| `RegistrarProductoProximoVencerUseCase` | FSD-UC-001 | Crear un caso trazable de producto próximo a vencer. |
| `ValidarAlertaProductoUseCase` | FSD-UC-002 | Validar información, asignar prioridad y registrar decisión de supervisor. |
| `RegistrarAccionComercialUseCase` | FSD-UC-003 | Registrar descuento, bandeo, promoción, retiro o reposición. |
| `AprobarAccionComercialUseCase` | FSD-UC-004 | Aprobar, rechazar o solicitar ajuste de una acción comercial. |
| `ConsultarDashboardGerencialQuery` | FSD-UC-005 | Exponer KPIs consolidados sin mezclar con comandos transaccionales. |
| `GenerarAlertasVencimientoUseCase` | FSD-UC-006 | Detectar productos que requieren atención según umbrales. |
| `ClasificarRiesgoProductoUseCase` | FSD-UC-007 | Solicitar clasificación asistida por IA y validar resultado. |
| `AuditarHistorialProductoQuery` | FSD-UC-008 | Consultar historial completo por producto, tienda, usuario y acción. |

### 8.3 Puertos de salida

Los puertos de salida representan dependencias del core hacia el exterior.

| Puerto de salida | Adaptador esperado | Razón arquitectónica |
|---|---|---|
| `ProductoDetectadoRepositoryPort` | PostgreSQL/JPA | Persistir agregados sin acoplar dominio a ORM. |
| `AccionComercialRepositoryPort` | PostgreSQL/JPA | Persistir acciones comerciales y estados. |
| `EvidenceStoragePort` | S3/local storage | Guardar fotografías sin acoplar dominio a almacenamiento. |
| `AuditLogPort` | Tabla audit log / OpenSearch futuro | Registrar quién hizo qué, cuándo y por qué. |
| `DomainEventPublisherPort` | Outbox/SNS/SQS futuro | Publicar eventos sin acoplar core a broker. |
| `NotificationPort` | Email/WhatsApp corporativo/push futuro | Emitir alertas sin contaminar casos de uso. |
| `RiskClassifierPort` | IA/heurística/reglas | Clasificar riesgo sin que IA escriba directamente en el dominio. |
| `AnalyticsReadModelPort` | SQL view/materialized view/CQRS futuro | Alimentar dashboard gerencial sin sobrecargar el modelo transaccional. |
| `ClockPort` | Sistema/fixture de pruebas | Controlar tiempo para reglas de vencimiento y pruebas determinísticas. |

---

## 9. Reglas de dependencia

La decisión se implementará con estas reglas obligatorias:

1. `domain` no importa clases de framework web, ORM, cloud, IA ni mensajería.
2. `application` conoce puertos, comandos, resultados y casos de uso; no conoce detalles de adaptadores.
3. `adapter/in` traduce HTTP/UI/eventos externos hacia comandos de caso de uso.
4. `adapter/out` implementa puertos de salida.
5. Todo caso de uso debe citar su ID FSD en nombre, comentario o prueba.
6. Todo NFR crítico debe tener mecanismo de verificación asociado.
7. La IA no muta entidades directamente; solo devuelve una recomendación estructurada que el caso de uso valida.
8. Los eventos se generan desde casos de uso o dominio, pero se publican mediante puerto de salida.
9. El dashboard gerencial consume modelos de lectura, no manipula el agregado transaccional.
10. No se permite lógica de negocio en controllers.

---

## 10. Trazabilidad FSD → Core hexagonal

| FSD | Caso de uso / capacidad | Puerto de entrada | Dominio involucrado | Puertos de salida | Pruebas esperadas |
|---|---|---|---|---|---|
| FSD-UC-001 | Registrar producto próximo a vencer | `RegistrarProductoProximoVencerUseCase` | `ProductoDetectado`, `FechaVencimiento`, `Cantidad`, `Precio` | `ProductoDetectadoRepositoryPort`, `EvidenceStoragePort`, `AuditLogPort`, `DomainEventPublisherPort` | Unitarias de validación + integración de persistencia + contrato API |
| FSD-UC-002 | Validar y priorizar alerta | `ValidarAlertaProductoUseCase` | `AlertaVencimiento`, `RiesgoVencimiento`, `PoliticaPriorizacionVencimiento` | `ProductoDetectadoRepositoryPort`, `AuditLogPort`, `DomainEventPublisherPort` | Unitarias de estados + Gherkin de validación |
| FSD-UC-003 | Registrar acción comercial | `RegistrarAccionComercialUseCase` | `AccionComercial`, `Precio`, `Cantidad`, `CalculadoraImpactoFinanciero` | `AccionComercialRepositoryPort`, `AuditLogPort`, `DomainEventPublisherPort` | Unitarias de reglas + integración repository |
| FSD-UC-004 | Aprobar/rechazar acción | `AprobarAccionComercialUseCase` | `AccionComercial`, `EstadoAccionComercial` | `AuditLogPort`, `NotificationPort`, `DomainEventPublisherPort` | Tests de autorización y transición |
| FSD-UC-005 | Dashboard gerencial | `ConsultarDashboardGerencialQuery` | Modelo de lectura/KPIs | `AnalyticsReadModelPort` | Pruebas de agregación + consistencia de métricas |
| FSD-UC-006 | Alertas automáticas | `GenerarAlertasVencimientoUseCase` | `FechaVencimiento`, `RiesgoVencimiento` | `NotificationPort`, `DomainEventPublisherPort`, `ClockPort` | Tests con reloj controlado + casos de umbral |
| FSD-UC-007 | Clasificación IA | `ClasificarRiesgoProductoUseCase` | `RiesgoVencimiento`, `PoliticaPriorizacionVencimiento` | `RiskClassifierPort`, `AuditLogPort` | Prompt tests + guardrails + fallback heurístico |
| FSD-UC-008 | Auditoría | `AuditarHistorialProductoQuery` | Historial/audit view | `AuditLogPort` | Tests de trazabilidad y consulta histórica |

---

## 11. Integración de IA sin invadir el dominio

La IA forma parte del producto como capacidad asistiva, no como autoridad de negocio. Por ello, la arquitectura hexagonal define la IA como **adaptador externo** detrás del puerto `RiskClassifierPort`.

### 11.1 Reglas para IA

| Regla | Justificación |
|---|---|
| La IA no aprueba descuentos, retiros ni promociones de forma autónoma. | Son decisiones comerciales con impacto financiero. |
| La IA solo devuelve clasificación sugerida, explicación y nivel de confianza. | Permite supervisión humana y auditoría. |
| El caso de uso valida el output contra reglas del FSD. | Evita que un modelo contradiga reglas de negocio. |
| Debe existir fallback heurístico si el modelo falla. | Mantiene continuidad operativa. |
| Toda ejecución IA registra prompt, versión, entrada, salida, confianza y decisión humana posterior. | Soporta auditoría y PROMPT_MAPPING. |
| Prompt injection o salida no estructurada produce rechazo controlado. | Protege integridad de decisiones. |

### 11.2 Contrato conceptual de salida IA

```json
{
  "productoDetectadoId": "uuid",
  "riesgoSugerido": "BAJO | MEDIO | ALTO | CRITICO",
  "confianza": 0.0,
  "factores": ["dias_restantes", "cantidad", "rotacion", "accion_pendiente"],
  "explicacion": "texto breve auditable",
  "requiereRevisionHumana": true
}
```

La decisión final seguirá viviendo en el caso de uso y en el rol humano responsable, no en el modelo.

---

## 12. Eventos de dominio preparados por el core

Aunque el ADR-0002 no decide la arquitectura event-driven completa, sí prepara el core para emitir eventos mediante un puerto. Esto evita repetir el ADR-0001 y deja habilitado el futuro ADR de eventos/outbox.

| Evento de dominio | Productor | Consumidores futuros | Motivo |
|---|---|---|---|
| `ProductoProximoVencerRegistrado` | FSD-UC-001 | Notificaciones, Analytics, Auditoría | Inicia trazabilidad del caso. |
| `AlertaVencimientoValidada` | FSD-UC-002 | Analytics, Supervisión, Notificaciones | Marca decisión táctica. |
| `AccionComercialRegistrada` | FSD-UC-003 | Dashboard, Auditoría, Gerencia | Permite medir impacto comercial. |
| `AccionComercialAprobada` | FSD-UC-004 | Notificación, Ejecución comercial | Habilita acción. |
| `AccionComercialRechazada` | FSD-UC-004 | Auditoría, Retroalimentación | Explica bloqueo o corrección. |
| `RiesgoProductoClasificado` | FSD-UC-007 | Supervisión, Auditoría IA | Traza recomendación asistida. |

Estos eventos se publicarán inicialmente de forma interna o vía outbox cuando se apruebe el ADR correspondiente. El core no dependerá directamente de SNS, SQS, Kafka, RabbitMQ ni cualquier broker.

---

## 13. Impacto en DTI

Este ADR debe reflejarse explícitamente en el DTI de la siguiente manera:

| Sección DTI | Contenido derivado de este ADR |
|---|---|
| §3 Arquitectura de Alto Nivel | C4 nivel 3 del core usando casos de uso, dominio y adaptadores. |
| §4 Modelo de Dominio | Bounded contexts, entidades, value objects y aggregates definidos aquí. |
| §5 Arquitectura Hexagonal del Core | Puertos de entrada, puertos de salida, adaptadores y reglas de dependencia. |
| §7 Arquitectura Event-Driven | Eventos preparados por el core mediante `DomainEventPublisherPort`. |
| §9 Capa IA / Agentes | IA como adaptador externo con puerto, guardrails y fallback. |
| §11 NFRs Consolidados | Testabilidad, observabilidad, auditoría, seguridad y performance por caso de uso. |
| §12 POCs Críticas | POCs deben validar core transaccional e IA/guardrails. |
| §16 Antipatrones auditados | Evitar CRUD anémico, God Service y lógica en controllers. |
| §17 Trade-offs | Se documenta balance entre pureza, simplicidad y evolución. |
| §21 Registro ADR | Registrar ADR-0002 como aceptado una vez aprobado. |

---

## 14. Impacto en AGENTS.md

`AGENTS.md` debe incorporar estas reglas para que cualquier agente IA o humano mantenga la arquitectura:

```md
## Reglas de arquitectura hexagonal

- Toda funcionalidad crítica debe iniciar desde un FSD-UC-NNN.
- Crear o modificar un caso de uso requiere ubicarlo en `application/port/in`.
- Las reglas de negocio viven en `domain`, no en controllers ni repositories.
- Los adaptadores implementan puertos, no contienen reglas de negocio.
- Ningún archivo en `domain` puede importar Spring, JPA, AWS SDK, clientes IA o librerías web.
- Toda integración externa debe entrar por un puerto de salida.
- Toda recomendación IA debe pasar por un caso de uso que valide guardrails.
- Todo test debe declarar qué FSD-UC, BR o NFR verifica.
```

---

## 15. Impacto en PROMPT_MAPPING.md

Los prompts no deben generar código o decisiones sin trazabilidad. Deben mapearse a puertos/casos de uso.

| Prompt | Origen | Consumidor | Artefacto generado | Restricción derivada |
|---|---|---|---|---|
| `PR-UC-001` | FSD-UC-001 | Dev Agent | Caso de uso registrar producto | No generar lógica en controller. |
| `PR-UC-002` | FSD-UC-002 | Dev Agent | Validación y priorización | Aplicar `PoliticaPriorizacionVencimiento`. |
| `PR-UC-003` | FSD-UC-003 | Dev Agent | Acción comercial | Respetar `AccionComercial` y auditoría. |
| `PR-IA-001` | FSD-UC-007 | AI Agent | Clasificación de riesgo | Output estructurado + guardrails + fallback. |
| `PR-AUDIT-001` | FSD-UC-008 | Auditor Agent | Reporte trazabilidad | No inventar eventos ni reglas. |

---

## 16. Consecuencias positivas

1. **Trazabilidad fuerte**: cada caso de uso del FSD puede mapearse a un puerto de entrada, dominio, adaptadores y pruebas.
2. **Dominio protegido**: las reglas de negocio no dependen de detalles técnicos.
3. **Mejor defensa arquitectónica**: el DTI puede mostrar arquitectura C4 nivel 3 y hexagonal con claridad.
4. **Mejor testabilidad**: reglas de vencimiento, prioridad, estado e impacto financiero pueden probarse sin infraestructura.
5. **IA controlada**: la IA queda como adaptador externo, con guardrails y validación humana.
6. **Preparación event-driven**: eventos de dominio pueden publicarse vía outbox sin reescribir casos de uso.
7. **Evolución segura**: si un bounded context crece, sus puertos y casos de uso ya definen el seam de extracción.
8. **Menor riesgo de CRUD anémico**: obliga a modelar reglas y estados del negocio.
9. **Mayor coherencia con documentos aprobados**: BRD, MRD, PRD y FSD se reflejan en código y DTI.

---

## 17. Consecuencias negativas y costos

1. **Mayor disciplina inicial**: exige nombrar casos de uso, comandos, puertos y adaptadores correctamente.
2. **Más archivos que un MVC simple**: puede parecer más pesado en un MVP si no se explica bien.
3. **Riesgo de sobreabstracción**: crear puertos innecesarios puede volver el sistema artificial.
4. **Curva de aprendizaje**: el equipo debe entender dominio, puertos, adaptadores y reglas de dependencia.
5. **Necesidad de convenciones**: sin `AGENTS.md` claro, los agentes IA podrían romper la arquitectura.
6. **Mayor exigencia en pruebas**: cada caso de uso debe tener pruebas vinculadas a criterios de aceptación.

---

## 18. Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Convertir hexagonal en burocracia | Media | Medio | Crear puertos solo para dependencias externas reales. |
| Controllers con lógica de negocio | Alta si no hay disciplina | Alto | Reglas en `AGENTS.md`, revisión de PR y tests por FSD-UC. |
| Dominio anémico | Media | Alto | Modelar estados, invariantes y value objects. |
| IA actuando fuera del caso de uso | Media | Alto | `RiskClassifierPort` + validación + guardrails + auditoría. |
| Eventos publicados sin transacción | Media | Alto | Preparar `DomainEventPublisherPort`; futuro ADR de Outbox. |
| Dashboard acoplado a tablas transaccionales | Media | Medio | Separar query/read model. |
| Duplicación con ADR-0001 | Baja tras esta versión | Medio | ADR-0002 limita alcance al core interno. |

---

## 19. Plan de implementación incremental

### Fase 1 — Base del core

- Crear paquetes `domain`, `application/port/in`, `application/port/out`, `adapter`.
- Implementar `ProductoDetectado`, `FechaVencimiento`, `Precio`, `Cantidad`.
- Implementar `RegistrarProductoProximoVencerUseCase`.
- Crear pruebas unitarias de reglas básicas.

### Fase 2 — Validación y acción comercial

- Implementar `AlertaVencimiento`.
- Implementar `ValidarAlertaProductoUseCase`.
- Implementar `AccionComercial`.
- Implementar `RegistrarAccionComercialUseCase`.
- Agregar auditoría.

### Fase 3 — Lecturas gerenciales y alertas

- Implementar `ConsultarDashboardGerencialQuery`.
- Crear `AnalyticsReadModelPort`.
- Implementar `GenerarAlertasVencimientoUseCase` con `ClockPort`.

### Fase 4 — IA asistiva y eventos

- Implementar `RiskClassifierPort`.
- Crear adaptador heurístico inicial.
- Preparar adaptador IA futuro.
- Emitir eventos de dominio por puerto.
- Conectar con futuro ADR de Outbox/Event-driven.

---

## 20. Validación de la decisión

La decisión se considerará correcta si se cumplen estos criterios:

| Criterio | Métrica / evidencia | Fuente |
|---|---|---|
| Casos de uso trazables | 100 % de FSD-UC críticos tienen puerto de entrada | FSD + código + DTI §5 |
| Dominio desacoplado | 0 imports de framework en `domain` | Revisión estática / PR |
| Pruebas de reglas | ≥ 80 % de reglas críticas con test unitario | Suite de tests |
| IA controlada | 100 % de recomendaciones IA pasan por caso de uso y guardrails | PROMPT_MAPPING + logs |
| Auditoría | Toda acción crítica registra usuario, fecha, estado y motivo | Tests + audit log |
| Eventos preparados | Eventos definidos y publicados vía puerto, no broker directo | Código + DTI §7 |
| Coherencia documental | DTI §5 refleja este ADR y FSD | Revisión documental |

---

## 21. Plan de reversión

Si la arquitectura hexagonal resulta demasiado pesada para el alcance real, se podrá reducir su formalidad sin romper los principios esenciales.

### Señales de reversión

- El equipo no logra implementar casos de uso simples por exceso de abstracción.
- Los puertos no agregan valor porque no hay dependencia externa real.
- El dominio queda vacío y toda lógica termina en application services.
- El tiempo de implementación supera el beneficio de testabilidad y trazabilidad.

### Estrategia de reversión controlada

1. Mantener paquetes `domain`, `application` y `adapter`.
2. Reducir puertos innecesarios.
3. Fusionar adaptadores simples cuando no haya variabilidad real.
4. Conservar casos de uso explícitos y pruebas por FSD-UC.
5. No volver a lógica de negocio en controllers.

La reversión no debe regresar a un CRUD sin dominio; solo debe simplificar la cantidad de abstracciones.

---

## 22. Antipatrones que esta decisión evita

| Antipatrón | Cómo se evita |
|---|---|
| CRUD anémico | Entidades, value objects y servicios de dominio con reglas reales. |
| God Service | Casos de uso pequeños por FSD-UC. |
| Lógica en controllers | Controllers solo traducen request/response. |
| Repositorios con reglas | Repositories solo persisten/recuperan. |
| IA con autoridad de negocio | IA como adaptador; caso de uso valida. |
| Dashboard acoplado al modelo transaccional | Queries/read models separados. |
| Eventos acoplados a infraestructura | Puerto `DomainEventPublisherPort`. |
| Monolito accidental | Módulos y puertos alineados a bounded contexts. |

---

## 23. Guion de defensa oral

Para defender este ADR ante el docente:

> “El ADR-0001 decidió el estilo macro: monolito modular evolutivo. El ADR-0002 baja un nivel y define cómo protegeremos el core. Elegimos arquitectura hexagonal porque App Detección Prod no es un CRUD de productos; tiene reglas de vencimiento, validación, acción comercial, auditoría, impacto financiero, alertas e IA asistiva. Si esas reglas quedan en controllers o queries, perdemos trazabilidad y testabilidad. Con hexagonal cada caso de uso del FSD se vuelve un puerto de entrada; la persistencia, eventos, IA, storage y notificaciones quedan como puertos de salida. Esto permite probar el dominio, mapear FSD a código, preparar eventos y mantener IA con guardrails sin sobredimensionar el sistema con microservicios prematuros.”

---

## 24. Decisiones que quedan pendientes para ADRs posteriores

Este ADR no decide todo. Deja pendientes decisiones específicas:

| ADR futuro | Tema | Relación con ADR-0002 |
|---|---|---|
| ADR-0003 | Event-driven + Outbox | Implementará físicamente `DomainEventPublisherPort`. |
| ADR-0004 | Capa IA, guardrails y human-in-the-loop | Profundizará `RiskClassifierPort` y prompt contracts. |
| ADR-0005 | Cloud provider y estilo de despliegue AWS | Mapeará adaptadores a servicios AWS. |
| ADR-0006 opcional | Modelo de lectura / CQRS para dashboard | Profundizará `AnalyticsReadModelPort`. |

---

## 25. Referencias internas

- `docs/brd/BRD_vFinal.md` — problema de negocio, stakeholders, RACI y métricas.
- `docs/mrd/MRD_vFinal.md` — mercado, personas, JTBD y competencia.
- `docs/prd/PRD_vFinal.md` — objetivos de producto, historias y requerimientos.
- `docs/fsd/FSD_vFinal.md` — casos de uso, reglas, Gherkin, NFRs y prompt-contratos.
- `docs/adr/0001-estilo-arquitectonico.md` — decisión macroarquitectónica base.
- `docs/DTI.md` — secciones §4 y §5 deben reflejar este ADR.
- `AGENTS.md` — reglas para preservar la arquitectura en trabajo humano/agéntico.

---

## 26. Historial

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 0.1 | 26/05/2026 | Gina Fabiana Villanueva Viscarra | Versión inicial del ADR-0002. |
| 0.2 | 26/05/2026 | Gina Fabiana Villanueva Viscarra | Versión mejorada: elimina redundancia con ADR-0001, profundiza core hexagonal, trazabilidad FSD, IA, eventos, AGENTS, PROMPT_MAPPING y DTI. |
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


### 6. Impacto específico en ADR-0002

El cambio de precio debe implementarse como caso de uso del núcleo, no como lógica en el controlador ni en el dashboard. Se incorporan puertos de entrada como `RegistrarCambioPrecioUseCase`, `AprobarCambioPrecioUseCase` y `ConsultarImpactoPrecioUseCase`; y puertos de salida como `AccionComercialRepository`, `AuditLogPort`, `DashboardReadModelPort` y `DomainEventPublisherPort`. Esto preserva la arquitectura hexagonal y permite probar reglas de precio sin infraestructura.
