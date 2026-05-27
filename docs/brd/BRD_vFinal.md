# Business Requirements Document (BRD) vFinal — App Detección Prod

> **Ubicación sugerida en el repositorio:** `docs/brd/BRD_vFinal.md`  
> **Estado:** `APROBADO`  
> **Versión:** `vFinal-2.0.0-APROBADO`  
> **Release objetivo:** `release/2.0.0`  
> **Cadena de trazabilidad:** `BRD → MRD → PRD → FSD → DTI → ADR/POC/PROMPT_MAPPING`  
> **Estado de aprobación:** aprobado por la autora para ser usado como fuente de verdad del MRD, PRD, FSD y DTI.

---

## 0. Metadatos

| Campo | Valor |
|---|---|
| Producto | **App Detección Prod** |
| Tipo de producto | Plataforma digital de gestión, trazabilidad e inteligencia comercial para productos próximos a vencer en canal retail |
| Organización objetivo | Empresas distribuidoras e importadoras que operan en supermercados, micromercados, farmacias y tiendas especializadas |
| Grupo | Proyecto académico — Maestría en Desarrollo de Productos de Software con IA |
| Versión del documento | `vFinal-2.0.0-APROBADO` |
| Fecha | 26/05/2026 |
| Autora | Gina Fabiana Villanueva Viscarra |
| Sponsor de negocio | Gerencia Comercial / Dirección Comercial |
| Stakeholders principales | Mercaderistas, vendedores, supervisores regionales, gerencia comercial, administración/finanzas, logística, trade marketing, TI/arquitectura, clientes retail |
| Estado | Aprobado |
| Insumos principales | Consigna M2 App Detección Prod, entrevistas a gerente, supervisor y vendedor, plan de investigación UX, plantilla BRD M4 |
| Prompts utilizados | `PR-BRD-001` pendiente de registrar en `docs/PROMPT_MAPPING.md` |
| Artefactos hijos esperados | `docs/mrd/MRD_vFinal.md`, `docs/prd/PRD_vFinal.md`, `docs/fsd/FSD_vFinal.md`, `docs/DTI.md`, `docs/adr/*`, `pocs/*` |

---

## 1. Resumen ejecutivo

**App Detección Prod** responde a un problema estructural en empresas distribuidoras e importadoras que operan en canal retail: la gestión de productos próximos a vencer depende de reportes informales por WhatsApp, fotografías no estandarizadas, archivos Excel dispersos y comunicación verbal entre mercaderistas, vendedores, supervisores y gerencia. Esta dinámica produce pérdida de trazabilidad, decisiones tardías, acciones comerciales no medibles, ausencia de control sobre cambios de precio, dificultad para cuantificar impacto financiero y aumento de merma por vencimiento.

El problema de negocio no es solamente “falta de una app”; es la desconexión entre la operación en campo y la inteligencia comercial. El mercaderista detecta el producto en sala, el supervisor intenta validar la información, el vendedor necesita decidir acciones comerciales y la gerencia necesita visualizar indicadores confiables. Sin embargo, el proceso actual no conecta esos niveles con una fuente única de verdad.

La propuesta consiste en crear una plataforma digital que centralice el registro de productos próximos a vencer, evidencia visual, fecha de vencimiento, cantidad, precio actual, precio modificado, acción comercial aplicada, responsable, estado del caso e impacto financiero. El objetivo es pasar de un modelo reactivo y fragmentado a un sistema trazable, medible y orientado a decisiones.

El valor esperado se expresa en tres dimensiones: reducción de merma, disminución del tiempo de validación y mejora de la visibilidad gerencial. Como metas iniciales se plantea: **reducir al menos 30 % el tiempo de validación**, lograr que **80 % de productos críticos tengan acción registrada antes del umbral definido** y construir una línea base de impacto financiero por producto, sala, región y acción comercial.

La decisión requerida del sponsor es aprobar la continuidad del producto hacia MRD, PRD, FSD y DTI, habilitando validación con usuarios, reglas comerciales, datos de productos, políticas de devolución/cambio y métricas históricas de merma.

---

## 2. Contexto del negocio

### 2.1 Organización objetivo

El producto está orientado a empresas distribuidoras e importadoras que comercializan productos en canal retail, incluyendo supermercados, micromercados, cadenas de farmacias y tiendas especializadas. Estas empresas gestionan múltiples marcas, productos, salas, rutas, acuerdos comerciales, promociones y políticas de cambio o devolución.

En este contexto, los productos próximos a vencer representan un riesgo comercial y financiero porque pueden generar pérdida directa, devolución, cambio, costo logístico, reducción de margen, deterioro de reputación y ocupación ineficiente de espacio en góndola o inventario.

### 2.2 Unidad impactada

| Unidad / Área | Situación actual | Necesidad de negocio |
|---|---|---|
| Mercaderismo | Reporte manual, fotos dispersas, presión de tiempo | Registro simple, rápido y estandarizado en campo |
| Ventas | Decisiones con información incompleta | Claridad de prioridades, acciones pendientes y estado de producto |
| Supervisión | Validación lenta y poco confiable | Visibilidad operativa, control de SLA y seguimiento por equipo |
| Gerencia comercial | Falta de KPIs consolidados e impacto financiero | Dashboard ejecutivo, indicadores y comparativos estratégicos |
| Trade marketing | Acciones comerciales difíciles de medir | Medición de promociones, bandeos, descuentos y retiros |
| Administración / Finanzas | Costos de devolución y reposición poco trazables | Evidencia y datos para cuantificar pérdida, ahorro y ROI |
| Logística | Cambios o retiros tardíos | Planificación anticipada de retiro, reposición o movimiento |
| TI / Arquitectura | Necesidad futura de integración y seguridad | Solución gobernable, segura, escalable y trazable |

### 2.3 Procesos de negocio afectados

1. Detección de productos próximos a vencer.
2. Registro de evidencia en punto de venta.
3. Validación de información reportada por mercaderistas.
4. Priorización de productos críticos.
5. Definición de acción comercial.
6. Ejecución de descuento, bandeo, promoción, retiro, cambio o reposición.
7. Control de precio actual y precio modificado.
8. Seguimiento de cantidad intervenida.
9. Consolidación de indicadores.
10. Análisis de impacto financiero.
11. Retroalimentación a equipos de campo.

### 2.4 Estrategia organizacional vinculada

| Objetivo estratégico | Relación con App Detección Prod |
|---|---|
| Reducir merma por vencimiento | Detecta anticipadamente productos críticos y permite accionar antes de que generen pérdida |
| Mejorar rentabilidad por producto | Relaciona acción comercial con precio, cantidad e impacto financiero |
| Profesionalizar la operación comercial | Sustituye WhatsApp/Excel por trazabilidad estructurada |
| Acelerar decisiones comerciales | Centraliza datos para supervisión y ventas |
| Mejorar visibilidad ejecutiva | Provee KPIs para gerencia sin exigirle participar en la operación diaria |
| Incrementar madurez digital | Convierte un proceso informal en un flujo medible, auditable y escalable |

---

## 3. Problema y oportunidad de negocio

### 3.1 Problema

Las empresas distribuidoras e importadoras que operan en canal retail enfrentan una brecha crítica entre lo que ocurre en sala y lo que el negocio puede ver, medir y decidir. Los mercaderistas detectan productos próximos a vencer durante visitas físicas, pero el reporte se realiza principalmente por WhatsApp, fotografías sin estandarización o archivos Excel. La información llega incompleta, mezclada entre conversaciones y sin relación formal con producto, lote, sala, fecha de vencimiento, cantidad, precio actual, nuevo precio o acción comercial ejecutada.

Esta falta de estructura genera consecuencias acumulativas: el supervisor invierte demasiado tiempo validando datos; el vendedor toma decisiones comerciales con incertidumbre; la gerencia recibe información tardía, dispersa o insuficiente; y el negocio no puede medir qué acciones reducen realmente la merma. Los productos pueden quedar demasiado tiempo en sala sin acción, ser descontados tarde, ser retirados sin medición o generar devoluciones/cambios con costos adicionales.

El problema de fondo es la inexistencia de un **sistema de trazabilidad operativo-comercial** que conecte campo, ventas, supervisión y gerencia mediante datos confiables, oportunos y accionables.

### 3.2 Evidencia de campo sintetizada

| Fuente | Hallazgo principal | Implicación para el BRD |
|---|---|---|
| Investigación M2 | El negocio carece de integración entre relevamiento, acción comercial, precio, cantidad, seguimiento y métricas | El BRD debe plantear una solución integral, no solo captura de datos |
| Entrevista supervisor | Validar reportes puede tomar de 15 minutos a una hora o incluso días en casos complejos | El tiempo de validación debe ser KPI central |
| Entrevista vendedor | La información dispersa genera decisiones “a ciegas” sobre descuentos, bandeos o promociones | El producto debe reducir incertidumbre comercial |
| Entrevista gerente | La gerencia necesita visibilidad total, métricas de rotación e impacto financiero | Gerencia debe ser principalmente informada por dashboards e indicadores |

### 3.3 Consecuencias actuales

| Consecuencia | Descripción | Impacto de negocio |
|---|---|---|
| Falta de trazabilidad | No se conoce con certeza quién reportó, qué producto, cuándo, dónde y con qué evidencia | Dificulta auditoría y seguimiento |
| Decisiones tardías | La información debe validarse manualmente antes de actuar | Se pierden oportunidades de venta |
| Acciones no medibles | Descuentos, bandeos o retiros no se relacionan con impacto económico | No se aprende qué estrategia funciona |
| Duplicidad de esfuerzos | Vendedor, supervisor y mercaderista consultan datos varias veces | Baja productividad |
| Riesgo financiero | Cambios, devoluciones y reposiciones aumentan costos | Reduce margen y rentabilidad |
| Visibilidad gerencial limitada | La gerencia recibe datos consolidados tarde o incompletos | Decisiones estratégicas débiles |
| Baja madurez digital | El proceso depende de personas y chats, no de un sistema | Escalabilidad limitada |

### 3.4 Oportunidad

La oportunidad de negocio es crear una plataforma que convierta cada detección de producto próximo a vencer en un **caso trazable**, con ciclo de vida, responsable, evidencia, acción comercial, impacto financiero y aprendizaje. Esto permitiría:

- Priorizar productos críticos antes de que se conviertan en pérdida.
- Reducir tiempo de validación de reportes.
- Mejorar la coordinación entre mercaderistas, vendedores y supervisores.
- Informar a gerencia con KPIs confiables, no con mensajes dispersos.
- Medir efectividad de descuentos, bandeos, promociones, cambios o retiros.
- Construir una base histórica para decisiones comerciales futuras.
- Evolucionar hacia analítica predictiva e IA asistida para priorización de riesgo.

### 3.5 Valor económico estimado

> Los valores son supuestos de business case académico y deben reemplazarse por datos reales del sponsor durante discovery financiero.

| Dimensión | Supuesto inicial | Valor de referencia |
|---|---:|---:|
| Productos críticos detectados por mes | 300 casos | 3.600 casos/año |
| Valor promedio comprometido por caso | 120 BOB | 432.000 BOB/año expuestos |
| Pérdida evitable por acción temprana | 25 % a 40 % | 108.000 a 172.800 BOB/año |
| Reducción esperada inicial de merma | 15 % a 25 % | Meta conservadora año 1 |
| Reducción de tiempo de validación | 30 % a 50 % | Productividad supervisión/ventas |
| Mejora en trazabilidad de acciones | 0 % formal actual → 90 % digital | Control operativo y gerencial |

---

## 4. Usuarios objetivo / Personas clave

### 4.1 Usuario primario: Mercaderista de canal retail

| Atributo | Valor |
|---|---|
| Rol | Usuario operativo en campo |
| Contexto | Visita salas, revisa góndolas, identifica productos próximos a vencer, toma fotos y reporta hallazgos |
| Jobs-to-be-done | Registrar productos próximos a vencer; adjuntar evidencia; informar cantidad, precio y fecha; indicar urgencia; recibir claridad sobre qué pasó con su reporte |
| Dolores principales | Reportes informales, duplicidad de mensajes, presión de tiempo, falta de estructura, poca retroalimentación |
| Ganancia esperada | Registrar rápido, con menos carga cognitiva y con trazabilidad visible |
| Responsabilidad de negocio | Ejecutar el registro operativo correcto y oportuno |

### 4.2 Usuario táctico: Supervisor regional

| Atributo | Valor |
|---|---|
| Rol | Usuario táctico de validación y control |
| Contexto | Recibe reportes de varios mercaderistas, valida datos, prioriza productos, coordina acciones y responde por indicadores de ejecución |
| Jobs-to-be-done | Ver productos críticos; validar reportes; controlar SLA; priorizar acciones; hacer seguimiento por equipo/ruta/sala |
| Dolores principales | Información dispersa, fotos sin contexto, validación lenta, presión por errores y pérdida de control |
| Ganancia esperada | Visibilidad operativa en tiempo real y tablero de seguimiento confiable |
| Responsabilidad de negocio | Asegurar calidad de la información y continuidad del flujo operativo |

### 4.3 Usuario comercial: Vendedor de canal moderno

| Atributo | Valor |
|---|---|
| Rol | Usuario comercial ejecutor |
| Contexto | Gestiona acciones comerciales con clientes retail y coordina descuentos, bandeos, promociones, retiros o cambios |
| Jobs-to-be-done | Saber qué productos requieren acción; revisar historial; coordinar aprobación; evitar acciones duplicadas o tardías |
| Dolores principales | Incertidumbre, decisiones a ciegas, pérdida de tiempo buscando información y aprobaciones tardías |
| Ganancia esperada | Decidir con confianza y priorizar oportunidades comerciales reales |
| Responsabilidad de negocio | Ejecutar o gestionar acciones comerciales autorizadas |

### 4.4 Persona decisora / informada ejecutiva: Gerencia comercial

| Atributo | Valor |
|---|---|
| Rol | Sponsor estratégico, decisor de políticas y consumidor principal de información ejecutiva |
| Contexto | Responsable de rentabilidad, indicadores comerciales, devoluciones, cambios, rotación y eficiencia |
| Jobs-to-be-done | Ver impacto financiero; comparar productos/regiones; controlar costos; decidir políticas comerciales; evaluar ROI |
| Dolores principales | Falta de datos consolidados, incertidumbre financiera, imposibilidad de medir impacto de acciones |
| Ganancia esperada | Dashboard ejecutivo con KPIs, alertas agregadas y análisis de rentabilidad |
| Responsabilidad de negocio | Aprobar lineamientos y recibir información confiable; no operar ni validar cada caso diario |

---

## 5. Propuesta de valor

| Eje | Contenido |
|---|---|
| Para quién | Empresas distribuidoras e importadoras que gestionan productos en canal retail |
| Que necesitan | Detectar, priorizar, gestionar y medir productos próximos a vencer antes de que generen merma |
| Nuestra propuesta es | Una plataforma digital que centraliza detecciones, evidencia, acciones comerciales, precios, cantidades y KPIs |
| Que le aporta | Trazabilidad completa; reducción de merma; decisiones más rápidas; medición de impacto financiero; coordinación entre campo, ventas, supervisión y gerencia |
| A diferencia de | WhatsApp, Excel, fotos sueltas, reportes manuales y comunicación verbal |
| Nuestro diferencial es | Integra flujo operativo + decisión comercial + medición financiera en una sola cadena trazable |

### 5.1 Value Proposition Canvas resumido

| Customer Jobs | Pains | Gains | Pain Relievers | Gain Creators |
|---|---|---|---|---|
| Registrar producto próximo a vencer | Fotos dispersas y sin contexto | Registro rápido | Formulario guiado | Evidencia estandarizada |
| Validar información | Datos incompletos | Menor tiempo de revisión | Campos obligatorios | Estado del caso visible |
| Ejecutar acción comercial | Incertidumbre sobre acciones previas | Decisión con confianza | Historial de acciones | Priorización de urgencia |
| Medir impacto | No hay KPIs financieros | Control de rentabilidad | Dashboard gerencial | Comparativos por sala/producto |
| Coordinar equipos | Comunicación fragmentada | Alineación operativa | Flujo de estados | Alertas y responsables |

---

## 6. Panorama competitivo y alternativas actuales

| Alternativa / Competidor | Tipo | Fortaleza percibida | Debilidad percibida | Implicación para App Detección Prod |
|---|---|---|---|---|
| WhatsApp | Do-nothing / proceso actual | Rápido, conocido, bajo costo | Sin trazabilidad, sin estructura, sin KPIs, difícil de auditar | Debe superarse sin perder facilidad de uso |
| Excel / Google Sheets | Sustituto manual | Flexible, conocido por supervisores | Error humano, baja oportunidad, difícil de operar en campo | El producto debe exportar datos, pero no depender de hojas |
| ERP comercial genérico | Indirecto | Maneja inventario, ventas y clientes | No cubre evidencia de sala ni flujo operativo de vencimientos | Debe integrarse o complementar, no necesariamente reemplazar |
| Formularios genéricos | Indirecto | Captura datos estructurados | Sin workflow comercial ni análisis financiero específico | App debe ofrecer flujo end-to-end |
| Software de auditoría retail | Directo parcial | Auditoría y visita en punto de venta | Puede no estar especializado en productos próximos a vencer ni acciones comerciales | Diferenciar por foco en merma, vencimiento e impacto financiero |
| Sistema interno ad hoc | Directo potencial | Adaptado a la empresa | Costoso, difícil de mantener, sin visión producto | App debe proponer modelo escalable y replicable |

---

## 7. Business Model Canvas

| Bloque | Elementos concretos |
|---|---|
| 1. Segmentos de clientes | Distribuidoras de consumo masivo / Importadoras con productos perecederos o de vencimiento regulado / Empresas con mercaderistas en canal retail |
| 2. Propuesta de valor | Reducción de merma / Trazabilidad de acciones comerciales / Indicadores financieros por producto-sala-región |
| 3. Canales | Venta directa B2B / Pilotos con empresas distribuidoras / Alianzas con consultoras de trade marketing |
| 4. Relación con clientes | Implementación asistida / Capacitación a equipos de campo / Soporte operativo y mejora continua |
| 5. Fuentes de ingresos | Suscripción SaaS mensual / Fee de implementación / Módulos premium de analítica e IA |
| 6. Recursos clave | Plataforma digital / Base histórica de detecciones / Equipo UX-producto-arquitectura / Conocimiento de procesos retail |
| 7. Actividades clave | Relevamiento de procesos / Configuración de reglas de negocio / Desarrollo de dashboard y flujos / Soporte y analítica |
| 8. Socios clave | Empresas distribuidoras / Retailers o cadenas de supermercados / Proveedores cloud / Consultores de trade marketing |
| 9. Estructura de costos | Desarrollo y mantenimiento / Infraestructura cloud / Soporte y capacitación / Seguridad, observabilidad y evolución IA |

---

## 8. Métricas clave de éxito

### 8.1 North Star Metric

| ID | KPI | North Star | Línea base | Meta | Horizonte | Fuente del dato |
|---|---|---|---|---|---|---|
| KPI-NS-01 | **Porcentaje de productos críticos gestionados antes del umbral de vencimiento** | Sí | Por medir; actualmente no existe medición formal | ≥ 80 % de productos críticos con acción registrada antes del umbral | Q4 2026 | App Detección Prod + reglas de vencimiento |

### 8.2 KPIs de apoyo

| ID | KPI | Línea base | Meta | Horizonte | Fuente |
|---|---:|---:|---|---|
| KPI-01 | Tiempo promedio de validación de reporte | Estimado: 60 min en casos complejos | Reducir ≥ 30 % | Primer piloto | Timestamps del flujo |
| KPI-02 | Porcentaje de reportes completos al primer envío | Por medir | ≥ 90 % | Primer piloto | Campos obligatorios del registro |
| KPI-03 | Trazabilidad de acción comercial | Baja / informal | ≥ 90 % de casos con acción y responsable | Q4 2026 | Historial del caso |
| KPI-04 | Reducción estimada de merma por vencimiento | Por medir | 15 % a 25 % | Año 1 | Dashboard financiero |
| KPI-05 | Casos críticos sin responsable asignado | Por medir | ≤ 5 % | Primer piloto | Workflow |
| KPI-06 | Satisfacción de usuarios internos | Por medir | ≥ 4/5 | Validación post piloto | Encuesta UX |
| KPI-07 | Uso gerencial del dashboard | 0 actual | ≥ 1 revisión semanal de indicadores | Piloto | Registro de dashboard/reunión comercial |
| KPI-08 | Reportes ejecutivos generados sin reproceso manual | 0 actual | ≥ 80 % reportes generados desde la plataforma | Q4 2026 | Módulo de reportes |

---

## 9. Objetivos de negocio SMART

| ID | Objetivo | Métrica | Línea base | Meta | Horizonte |
|---|---|---|---|---|---|
| BO-01 | Reducir la pérdida operativa asociada a productos próximos a vencer | % de merma por vencimiento | Por medir con datos históricos | Reducir 15 % a 25 % | Año 1 |
| BO-02 | Disminuir el tiempo de validación de reportes críticos | Minutos promedio por caso | Estimado 60 min en casos complejos | Reducir ≥ 30 % | Primer piloto |
| BO-03 | Aumentar trazabilidad de acciones comerciales | % de casos con acción, responsable, fecha y evidencia | Informal / no medido | ≥ 90 % | Q4 2026 |
| BO-04 | Mejorar visibilidad gerencial | # KPIs ejecutivos disponibles | 0 integrados | ≥ 8 KPIs críticos en dashboard | Release 2.0.0 / piloto |
| BO-05 | Reducir decisiones comerciales basadas en información incompleta | % reportes completos | Por medir | ≥ 90 % completos al primer envío | Primer piloto |
| BO-06 | Construir base histórica de aprendizaje comercial | Casos registrados con ciclo completo | 0 estructurados | ≥ 1.000 casos acumulados | Año 1 |

---

## 10. Stakeholders y modelo RACI corregido

### 10.1 Criterio de corrección aplicado

La matriz RACI fue reanalizada porque el primer borrador mezclaba **jerarquía organizacional** con **responsabilidad operativa real**. En este proyecto, la gerencia comercial es sponsor y dueña del valor de negocio, pero en la operación diaria su necesidad principal es **visualizar información confiable**, recibir alertas ejecutivas, revisar KPIs, evaluar impacto financiero y decidir políticas. Por eso, para los flujos operativos, gerencia debe figurar principalmente como **I — Informed**, no como responsable de ejecutar ni validar cada caso.

Definiciones usadas:

| Letra | Significado | Criterio aplicado en este BRD |
|---|---|---|
| R | Responsible / Responsable | Ejecuta directamente la actividad |
| A | Accountable / Dueño final | Responde por el resultado o aprobación final de esa actividad |
| C | Consulted / Consultado | Aporta criterio antes o durante la decisión |
| I | Informed / Informado | Recibe visibilidad, reporte o resultado; no ejecuta la actividad |

### 10.2 RACI por actividad del proceso de negocio

| Actividad / Decisión de negocio | Mercaderista | Supervisor Regional | Vendedor Canal Moderno | Gerencia Comercial | Trade Marketing | Administración / Finanzas | Logística | TI / Arquitectura | Cliente retail |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Registrar producto próximo a vencer con evidencia | **R** | A | I | I | I | I | I | C | I |
| Corregir datos incompletos del reporte | **R** | **A** | C | I | I | I | I | C | I |
| Validar reporte operativo | C | **R/A** | C | I | I | I | I | C | I |
| Priorizar casos críticos por urgencia | C | **R/A** | C | I | C | I | I | C | I |
| Definir acción comercial sugerida | I | C | **R** | I | C | C | C | I | C |
| Aprobar acción comercial dentro de política estándar | I | **A** | **R** | I | C | C | C | I | C |
| Aprobar excepción comercial de alto impacto | I | C | R | **A** | C | C | C | I | C |
| Ejecutar descuento, bandeo, promoción o retiro coordinado | C | A | **R** | I | C | I | R/C | I | C |
| Registrar precio actual, precio modificado y cantidad intervenida | R/C | A | **R** | I | C | C | I | C | I |
| Realizar retiro, cambio o movimiento logístico | I | A | C | I | I | C | **R** | I | C |
| Medir impacto financiero de la acción | I | C | C | I | C | **R/A** | C | C | I |
| Revisar dashboard ejecutivo de merma, rotación e impacto | I | C | C | **I** | C | C | I | R/C | I |
| Definir KPIs ejecutivos y reglas de seguimiento | I | C | C | **A** | C | C | I | R/C | I |
| Configurar reglas del sistema y permisos | I | C | C | C | C | C | I | **R/A** | I |
| Auditar historial del caso ante reclamo o revisión | C | R | C | I | C | C | C | C | C |

### 10.3 RACI resumido por stakeholder

| Stakeholder | Rol dominante en el producto | RACI predominante | Justificación |
|---|---|---|---|
| Mercaderista | Captura operativa en campo | **R** | Registra producto, evidencia, cantidad y datos iniciales |
| Supervisor Regional | Validación y control táctico | **R/A** | Valida, prioriza y asegura continuidad del flujo |
| Vendedor Canal Moderno | Ejecución comercial | **R** | Gestiona acciones comerciales y coordinación con clientes retail |
| Gerencia Comercial | Sponsor estratégico y consumidor ejecutivo de información | **I / A solo en políticas y excepciones** | Su interés principal es ver información consolidada, KPIs e impacto financiero; no operar casos diarios |
| Trade Marketing | Diseño y evaluación de acciones promocionales | **C** | Aporta criterios de promociones, bandeos y campañas |
| Administración / Finanzas | Medición financiera | **R/A en impacto financiero** | Calcula o valida costos, ahorros y pérdidas evitadas |
| Logística | Ejecución de retiro, cambio o reposición | **R en movimiento físico** | Ejecuta acciones físicas cuando corresponden |
| TI / Arquitectura | Habilitación tecnológica | **R/A técnico** | Implementa seguridad, integración, disponibilidad y datos |
| Cliente retail | Actor externo afectado por acciones en sala | **C/I** | Puede aprobar, observar o recibir acciones comerciales según acuerdo |

### 10.4 Lectura ejecutiva del RACI corregido

- **Gerencia Comercial no debe aparecer como responsable de registrar, validar o ejecutar casos diarios.** Su rol principal es estar informada con indicadores confiables y ser accountable solo en políticas comerciales, excepciones de alto impacto o aprobación estratégica del proyecto.
- **Supervisor Regional sí debe ser responsable/accountable de validación y priorización**, porque es quien controla al equipo operativo y reduce incertidumbre antes de escalar decisiones.
- **Vendedor Canal Moderno debe ser responsable de la acción comercial**, porque coordina descuentos, bandeos, promociones o gestiones comerciales con clientes.
- **Mercaderista debe ser responsable del registro inicial**, porque es quien está en sala y captura el dato primario.
- **Finanzas/Admin debe ser responsable del cálculo de impacto financiero**, no gerencia, porque gerencia consume el indicador para decidir.

---

## 11. Requerimientos de negocio

| ID | Requerimiento de negocio | Prioridad | Justificación | Métrica de aceptación | Traza esperada |
|---|---|---|---|---|---|
| BR-001 | El negocio necesita registrar productos próximos a vencer con información completa y evidencia visual | Must | Sin datos completos no hay decisión confiable | ≥ 90 % de reportes completos | MRD-N-01 / PRD-REQ-001 / FSD-UC-001 |
| BR-002 | El negocio necesita conocer precio actual, nuevo precio sugerido/aplicado y cantidad intervenida | Must | Permite medir impacto financiero | ≥ 90 % de acciones con precio y cantidad | MRD-N-02 / PRD-REQ-002 / FSD-UC-003 |
| BR-003 | El negocio necesita registrar acción comercial aplicada por producto | Must | Sin acción no hay aprendizaje ni control | 100 % de casos cerrados con acción o justificación | MRD-N-03 / PRD-REQ-003 / FSD-UC-003 |
| BR-004 | El negocio necesita visibilidad por sala, producto, región y responsable | Must | Permite priorizar y auditar | Dashboard con filtros operativos | MRD-N-04 / PRD-REQ-004 / FSD-UC-005 |
| BR-005 | El negocio necesita alertas tempranas por umbral de vencimiento | Must | Reduce reactividad y pérdida | ≥ 80 % casos críticos alertados antes del vencimiento | MRD-N-05 / PRD-REQ-005 / FSD-UC-006 |
| BR-006 | El negocio necesita validar información antes de ejecutar decisiones sensibles | Must | Evita descuentos/retiros erróneos | Flujo de validación supervisor/vendedor | MRD-N-06 / PRD-REQ-006 / FSD-UC-002 |
| BR-007 | El negocio necesita medir impacto financiero de las acciones | Should | Permite justificar ROI | Dashboard con ahorro, pérdida evitada y costo | MRD-N-07 / PRD-REQ-007 / FSD-UC-005 |
| BR-008 | El negocio necesita historial auditable por producto y caso | Must | Soporta control y resolución de controversias | 100 % de cambios con usuario, fecha y motivo | MRD-N-08 / PRD-REQ-008 / FSD-UC-008 |
| BR-009 | El negocio necesita priorizar productos críticos automáticamente | Should | Reduce sobrecarga operativa | Ranking por riesgo operativo-comercial | MRD-N-09 / PRD-REQ-009 / FSD-UC-007 |
| BR-010 | El negocio necesita operar aun con conectividad variable en campo | Should | Los mercaderistas trabajan en ruta | Captura tolerante a intermitencia | MRD-N-10 / PRD-NFR-002 / FSD-NFR-005 |
| BR-011 | El negocio necesita exportar datos para análisis y auditoría | Could | Facilita adopción y reportes ejecutivos | Exportación CSV/Excel/PDF | MRD-N-11 / PRD-REQ-010 / FSD-UC-005 |
| BR-012 | El negocio necesita configurar reglas por categoría, cliente o política interna | Should | No todos los productos tienen el mismo umbral | Configuración por tipo de producto | MRD-N-12 / PRD-REQ-011 / FSD-UC-006 |
| BR-013 | La gerencia necesita recibir información consolidada sin depender de reprocesos manuales | Must | Su rol principal es informado ejecutivo | Dashboard actualizado con KPIs y filtros | MRD-N-13 / PRD-REQ-012 / FSD-UC-005 |

---

## 12. Reglas de negocio y políticas

| ID | Regla | Tipo | Origen | Impacto |
|---|---|---|---|---|
| RB-001 | Todo producto próximo a vencer debe registrarse con producto, sala, fecha de vencimiento, cantidad y evidencia | Validación | Proceso operativo | Evita reportes incompletos |
| RB-002 | Un producto crítico no puede cerrarse sin acción comercial o justificación documentada | Política | Gerencia comercial | Garantiza trazabilidad |
| RB-003 | Toda modificación de precio debe registrar precio anterior, precio nuevo, fecha, responsable y motivo | Control comercial | Auditoría interna | Permite medir impacto |
| RB-004 | Las acciones comerciales sensibles deben ser validadas por supervisor o responsable comercial | Gobernanza | Política comercial | Evita decisiones unilaterales |
| RB-005 | Las fotografías deben estar asociadas a producto, sala, fecha y usuario | Evidencia | Proceso de auditoría | Reduce ambigüedad |
| RB-006 | Todo cambio de estado debe registrar usuario, fecha/hora y motivo | Auditoría | Buenas prácticas | Soporta trazabilidad completa |
| RB-007 | Los umbrales de vencimiento deben ser configurables por categoría, cliente o política interna | Parametrización | Negocio | Evita reglas rígidas |
| RB-008 | Las acciones fuera de política estándar requieren aprobación de gerencia o rol delegado | Excepción | Gobierno comercial | Controla riesgo económico |
| RB-009 | La gerencia debe visualizar indicadores consolidados, no participar en validaciones operativas rutinarias | Gobernanza | Modelo RACI corregido | Evita sobrecargar a nivel estratégico |
| RB-010 | Las métricas financieras deben diferenciar ahorro estimado, pérdida evitada y costo real | Medición | Finanzas/Gerencia | Evita sobreestimar beneficios |
| RB-011 | La IA, si se aplica, solo puede clasificar/priorizar; no puede aprobar descuentos o retiros automáticamente | Gobierno IA | Riesgo comercial | Mantiene human-in-the-loop |
| RB-012 | Ningún caso puede eliminarse físicamente si ya tuvo acción o validación; debe quedar archivado/auditado | Auditoría | Buenas prácticas | Preserva evidencia histórica |

---

## 13. Supuestos, restricciones y dependencias

### 13.1 Supuestos

- Los mercaderistas cuentan con smartphone Android o dispositivo móvil equivalente.
- La empresa puede definir umbrales de vencimiento por categoría, marca o cliente.
- Existen responsables comerciales capaces de validar acciones.
- La gerencia dispone de datos históricos o estimados de merma para construir línea base.
- El proceso actual ya genera evidencia visual, aunque de forma no estandarizada.
- El sponsor acepta iniciar con un piloto acotado antes de escalar a toda la operación.
- Finanzas o administración puede apoyar con costos de devolución, reposición y pérdida estimada.

### 13.2 Restricciones

| Restricción | Descripción | Implicación |
|---|---|---|
| Conectividad variable | Trabajo en sala/ruta puede tener señal limitada | La solución debe tolerar captura parcial o diferida |
| Adopción operativa | Mercaderistas pueden resistirse si el flujo es complejo | UX debe ser simple y rápida |
| Datos incompletos históricos | La merma puede no estar cuantificada formalmente | Se debe crear línea base inicial |
| Presupuesto académico / piloto | No se implementa solución enterprise completa de inicio | Priorizar MVP y POCs |
| Seguridad de datos | Evidencia y reportes pueden incluir información sensible comercial | Definir permisos y auditoría |
| Tiempo de módulo | Entrega final exige documentación y defensa | Priorizar trazabilidad y coherencia |

### 13.3 Dependencias

| Dependencia | Tipo | Riesgo si no se obtiene |
|---|---|---|
| Catálogo de productos | Datos maestros | Registros inconsistentes |
| Listado de salas/clientes | Datos maestros | Dificultad para filtrar y medir |
| Políticas de vencimiento | Negocio | Alertas incorrectas |
| Políticas de descuento/retiro | Comercial | Acciones inconsistentes |
| Datos históricos de merma | Finanzas | Business case menos preciso |
| Validación de usuarios | UX/Product | Riesgo de baja adopción |
| Acceso a sponsor | Gobierno | Decisiones bloqueadas |
| Criterios de excepción comercial | Gerencia/Comercial | RACI ambiguo en acciones de alto impacto |

---

## 14. Alcance de negocio

### 14.1 En alcance

- Registro estructurado de productos próximos a vencer.
- Evidencia fotográfica asociada a producto y sala.
- Registro de cantidad, fecha de vencimiento, precio actual y precio modificado.
- Registro y seguimiento de acción comercial.
- Validación por supervisor o responsable comercial.
- Alertas tempranas por umbral.
- Dashboard gerencial básico.
- Métricas de merma, pérdida evitada y trazabilidad.
- Historial auditable.
- Priorización inicial por riesgo.
- Base documental para MRD, PRD, FSD y DTI.

### 14.2 Fuera de alcance

| Elemento fuera de alcance | Justificación |
|---|---|
| Reemplazar ERP completo | El foco es gestión de vencimientos y acciones comerciales, no contabilidad total |
| Automatizar aprobación final sin humanos | Las decisiones comerciales sensibles requieren responsabilidad humana |
| Integración obligatoria con todos los retailers en v1 | Aumentaría complejidad y dependencia externa |
| Predicción avanzada de demanda en v1 | Puede ser roadmap posterior cuando exista data histórica |
| Optimización logística completa | El producto puede emitir alertas, pero no reemplaza planificación logística |
| Facturación o cobranza | No pertenece al flujo núcleo del problema actual |
| Obligar a gerencia a operar casos diarios | Contradice la necesidad ejecutiva: gerencia debe ver información consolidada |

---

## 15. Beneficios esperados y business case resumido

### 15.1 Beneficios cualitativos

- Mayor control de productos próximos a vencer.
- Menor incertidumbre para vendedores y supervisores.
- Toma de decisiones más rápida y con evidencia.
- Mayor profesionalización del proceso comercial.
- Mejor visibilidad gerencial sin reprocesos manuales.
- Base de datos histórica para análisis.
- Reducción de errores por información incompleta.
- Menor dependencia de conversaciones informales.

### 15.2 Beneficios cuantitativos estimados

> Los montos deben validarse con datos reales de la empresa. Se expresan en BOB como referencia académica.

| Tipo | Año 1 | Año 2 | Año 3 |
|---|---:|---:|---:|
| Ahorro por reducción de merma | 108.000 – 172.800 | 140.000 – 220.000 | 180.000 – 280.000 |
| Ahorro operativo por menor validación manual | 24.000 – 48.000 | 36.000 – 60.000 | 48.000 – 72.000 |
| Ingresos protegidos por acciones tempranas | 80.000 – 120.000 | 120.000 – 180.000 | 160.000 – 240.000 |
| Inversión inicial estimada | 60.000 – 90.000 | 20.000 – 40.000 | 20.000 – 50.000 |
| Costo operación / soporte | 18.000 – 36.000 | 24.000 – 48.000 | 30.000 – 60.000 |
| Beneficio neto estimado | Positivo si se captura ≥ 20 % de pérdida evitable | Positivo | Positivo |
| Horizonte de payback | 8 – 14 meses | — | — |

### 15.3 Interpretación ejecutiva

El business case es atractivo si se cumplen tres condiciones:

1. La empresa registra suficiente volumen de productos críticos por mes.
2. La acción temprana reduce al menos 15 % de merma o costo asociado.
3. La adopción operativa alcanza al menos 70 % de uso en rutas/salas piloto.

---

## 16. Riesgos de negocio

| Riesgo | Probabilidad | Impacto | Mitigación | Responsable |
|---|---|---|---|---|
| Baja adopción de mercaderistas | Media | Alta | UX simple, capacitación, piloto con feedback | Product Owner / Supervisión |
| Datos incompletos | Alta | Alta | Campos obligatorios, validaciones, catálogo de productos | Producto / TI |
| Falta de línea base financiera | Media | Alta | Construir línea base durante piloto | Finanzas / Gerencia informada |
| Sobrecarga de supervisores | Media | Media | Priorización automática y filtros | Producto / Supervisión |
| Resistencia al cambio | Media | Alta | Sponsorship visible y beneficios por rol | Gerencia Comercial / PM |
| Reglas de negocio ambiguas | Alta | Media | Talleres con sponsor para definir umbrales | Product Manager |
| Uso incorrecto de IA | Media | Alta | Human-in-the-loop, guardrails y auditoría | Arquitectura / Gobierno IA |
| Integración compleja con sistemas existentes | Media | Media | MVP desacoplado e integración gradual | TI |
| Expectativas sobredimensionadas | Media | Media | Roadmap por fases y métricas realistas | Sponsor / PM |
| Calidad baja de evidencia fotográfica | Media | Media | Guías de captura y validación de imagen | Operaciones |
| RACI mal interpretado | Media | Alta | Separar gobierno, operación y reporting ejecutivo | PM / Sponsor |

---

## 17. Criterios de éxito del proyecto de negocio

El proyecto será considerado exitoso si cumple, como mínimo:

1. **Trazabilidad operativa:** ≥ 90 % de casos con producto, sala, fecha, cantidad, evidencia, responsable y estado.
2. **Acción comercial medible:** ≥ 80 % de productos críticos con acción registrada antes del umbral de vencimiento.
3. **Reducción de tiempo:** ≥ 30 % menos tiempo promedio de validación de reportes.
4. **Visibilidad gerencial:** dashboard con al menos 8 KPIs ejecutivos.
5. **Business case positivo:** evidencia de reducción de pérdida o recuperación de valor durante piloto.
6. **Adopción:** ≥ 70 % de usuarios piloto usando el flujo completo.
7. **Satisfacción interna:** calificación ≥ 4/5 en utilidad percibida por rol.
8. **Calidad documental:** trazabilidad BRD → MRD → PRD → FSD → DTI sin rupturas.
9. **RACI defendible:** responsabilidades alineadas con la operación real y la evidencia de entrevistas.

---

## 18. Trazabilidad a documentos hijos

| BRD ID | Necesidad de negocio | MRD relacionado | PRD relacionado | Caso de uso FSD esperado | DTI/ADR esperado |
|---|---|---|---|---|---|
| BR-001 | Registro estructurado de producto próximo a vencer | MRD-N-01 | PRD-REQ-001 | FSD-UC-001 | DTI §4, §5 |
| BR-002 | Control de precio y cantidad intervenida | MRD-N-02 | PRD-REQ-002 | FSD-UC-003 | DTI §4 |
| BR-003 | Registro de acción comercial | MRD-N-03 | PRD-REQ-003 | FSD-UC-003 | ADR-0002 |
| BR-004 | Visibilidad por sala/producto/región | MRD-N-04 | PRD-REQ-004 | FSD-UC-005 | DTI §3, §8 |
| BR-005 | Alertas tempranas | MRD-N-05 | PRD-REQ-005 | FSD-UC-006 | ADR-0003 |
| BR-006 | Validación de reportes | MRD-N-06 | PRD-REQ-006 | FSD-UC-002 | DTI §5 |
| BR-007 | Impacto financiero | MRD-N-07 | PRD-REQ-007 | FSD-UC-005 | DTI §11 |
| BR-008 | Historial auditable | MRD-N-08 | PRD-REQ-008 | FSD-UC-008 | ADR-0003 |
| BR-009 | Priorización por riesgo | MRD-N-09 | PRD-REQ-009 | FSD-UC-007 | ADR-0004 |
| BR-010 | Operación en conectividad variable | MRD-N-10 | PRD-NFR-002 | FSD-NFR-005 | DTI §11, §15 |
| BR-011 | Exportación y reportes | MRD-N-11 | PRD-REQ-010 | FSD-UC-005 | DTI §14 |
| BR-012 | Configuración de reglas | MRD-N-12 | PRD-REQ-011 | FSD-UC-006 | ADR-0001 |
| BR-013 | Información ejecutiva para gerencia | MRD-N-13 | PRD-REQ-012 | FSD-UC-005 | DTI §14, §17 |

---

## 19. Aprobaciones

| Rol | Nombre | Firma | Fecha |
|---|---|---|---|
| Sponsor de negocio | Gerencia Comercial | Pendiente | Pendiente |
| Product Owner | Gina Fabiana Villanueva Viscarra | Pendiente | 26/05/2026 |
| Arquitectura | Responsable DTI | Pendiente | Pendiente |
| Revisor académico | Docente Módulo 4 | Pendiente | Pendiente |

---

## 20. Registro de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v0.1 | 2026-05-26 | Gina Fabiana Villanueva Viscarra | Versión inicial alineada a plantillas M4 |
| vFinal-2.0.0 | 2026-05-26 | Gina Fabiana Villanueva Viscarra + asistencia IA | Reestructuración completa con trazabilidad BRD→MRD→PRD→FSD→DTI |
| vFinal-2.0.0-RACI-CORREGIDO | 2026-05-26 | Gina Fabiana Villanueva Viscarra + asistencia IA | Corrección profunda de matriz RACI, separando operación diaria, reporting gerencial y gobierno del proyecto |

---

## 21. Anexo — PR-FAQ Amazon-style

### 21.1 Press Release

```text
La Paz, Q4 2026 — App Detección Prod anuncia una nueva plataforma digital para empresas distribuidoras e importadoras que necesitan controlar productos próximos a vencer en canal retail antes de que generen pérdidas económicas.

La solución permite a mercaderistas, vendedores, supervisores y gerencia trabajar sobre una misma fuente de verdad: productos detectados, evidencia visual, precio actual, precio modificado, cantidad intervenida, acción comercial aplicada y estado del caso.

“Durante años hemos tomado decisiones comerciales con información dispersa. App Detección Prod transforma ese proceso en trazabilidad, medición y acción oportuna”, señaló la Gerencia Comercial.

A diferencia del uso de WhatsApp, Excel y fotografías aisladas, App Detección Prod permite priorizar productos críticos, activar acciones comerciales y medir el impacto financiero de cada decisión. El objetivo es reducir merma, acelerar validaciones y mejorar la rentabilidad por producto, sala y región.
```

### 21.2 External FAQ

**1. ¿Qué es App Detección Prod?**  
Es una plataforma digital para registrar, gestionar y medir productos próximos a vencer en canal retail.

**2. ¿A quién está dirigida?**  
A empresas distribuidoras e importadoras que trabajan con mercaderistas, vendedores, supervisores y gerencia comercial.

**3. ¿Qué problema resuelve?**  
Resuelve la falta de trazabilidad, centralización, control de acciones comerciales e indicadores financieros sobre productos próximos a vencer.

**4. ¿Reemplaza WhatsApp?**  
No necesariamente elimina la comunicación informal, pero sí reemplaza a WhatsApp como fuente principal de registro, evidencia y seguimiento.

**5. ¿Qué gana la gerencia?**  
La gerencia obtiene visibilidad consolidada, KPIs, comparativos regionales e impacto financiero sin depender de reprocesos manuales.

**6. ¿Qué gana el supervisor?**  
Reduce tiempo de validación, prioriza casos críticos y controla el estado de las acciones.

**7. ¿Qué gana el vendedor?**  
Recibe información clara para ejecutar descuentos, bandeos, promociones, retiros o cambios con menor incertidumbre.

**8. ¿Qué gana el mercaderista?**  
Tiene un flujo guiado de registro y evidencia, con menos carga cognitiva y mayor claridad del proceso.

### 21.3 Internal FAQ

**1. ¿Por qué ahora?**  
Porque el proceso actual genera pérdidas, incertidumbre y falta de visibilidad, mientras la empresa necesita decisiones más rápidas y basadas en datos.

**2. ¿Cuál es el riesgo de no hacerlo?**  
Continuar con decisiones tardías, reportes dispersos, merma no cuantificada y acciones comerciales sin medición.

**3. ¿Quién debe operar el sistema?**  
Mercaderistas registran, supervisores validan, vendedores gestionan acciones, finanzas mide impacto y gerencia se informa mediante KPIs.

**4. ¿La gerencia debe validar cada caso?**  
No. La gerencia debe estar informada con indicadores y participar solo en políticas, excepciones o decisiones de alto impacto.

**5. ¿La IA puede aprobar descuentos?**  
No. La IA puede clasificar o priorizar riesgos, pero las decisiones comerciales sensibles requieren validación humana.

**6. ¿Cómo se mide éxito?**  
Por reducción de merma, menor tiempo de validación, mayor trazabilidad, adopción del flujo y visibilidad gerencial.

---

## 22. Checklist de revisión BRD

| Ítem | Estado |
|---|---|
| Metadatos completos | Completado |
| Resumen ejecutivo | Completado |
| Contexto de negocio | Completado |
| Problema y oportunidad | Completado |
| Evidencia de discovery | Completado |
| Personas clave | Completado |
| Propuesta de valor | Completado |
| Panorama competitivo | Completado |
| Business Model Canvas | Completado |
| KPIs y North Star | Completado |
| Objetivos SMART | Completado |
| Matriz RACI corregida | Completado |
| Requerimientos de negocio | Completado |
| Reglas de negocio | Completado |
| Supuestos, restricciones y dependencias | Completado |
| Alcance / fuera de alcance | Completado |
| Business case resumido | Completado |
| Riesgos | Completado |
| Criterios de éxito | Completado |
| Trazabilidad a documentos hijos | Completado |
| PR-FAQ | Completado |

---

## 23. Nota para continuidad documental

Este BRD debe alimentar directamente:

- **MRD vFinal:** profundizará mercado, segmentos, competencia, JTBD y oportunidad comercial.
- **PRD vFinal:** convertirá los requerimientos de negocio en objetivos, épicas, historias de usuario, NFRs y roadmap.
- **FSD vFinal:** especificará casos de uso, reglas, datos, prompt-contratos, Gherkin y trazabilidad.
- **DTI vFinal:** justificará arquitectura, C4, hexagonal, event-driven, AWS, IA, seguridad, observabilidad y ADRs.

La corrección RACI debe mantenerse consistente en los documentos posteriores: gerencia como **consumidor ejecutivo de información y sponsor estratégico**, no como operador del flujo diario.
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


### 6. Lectura ejecutiva para BRD

En el BRD, el KPI de cambio de precio se considera un **KPI de negocio Must**, porque conecta la acción comercial con rentabilidad. La gerencia no necesita registrar precios, pero sí necesita estar informada sobre:

- cuánto valor económico fue intervenido por descuentos o promociones;
- cuántas acciones cambiaron precio sin aprobación;
- qué salas, productos o vendedores aplican mayor variación de precio;
- si el cambio de precio redujo pérdida por vencimiento o afectó margen innecesariamente.

Esto refuerza la matriz RACI corregida: Gerencia es principalmente **Informed** sobre la operación diaria, pero **Accountable** sobre políticas de precio, umbrales de autorización y metas de rentabilidad.
