# Market Requirements Document (MRD) vFinal — App Detección Prod

> **Ubicación sugerida en el repositorio:** `docs/mrd/MRD_vFinal.md`  
> **Estado:** `APROBADO`  
> **Versión:** `vFinal-2.0.0-APROBADO`  
> **Release objetivo:** `release/2.0.0`  
> **Documento padre aprobado:** `docs/brd/BRD_vFinal.md`  
> **Cadena de trazabilidad:** `BRD → MRD → PRD → FSD → DTI → ADR/POC/PROMPT_MAPPING`  
> **Propósito:** describir el mercado, usuarios, segmentos, oportunidad y condiciones de adopción para App Detección Prod.

---

## 0. Metadatos

| Campo | Valor |
|---|---|
| Producto | **App Detección Prod** |
| Tipo de producto | Plataforma digital de trazabilidad, control e inteligencia comercial para productos próximos a vencer en canal retail |
| Organización objetivo | Distribuidoras e importadoras que atienden supermercados, micromercados, cadenas de farmacias y tiendas especializadas |
| Grupo | Proyecto académico — Maestría en Desarrollo de Productos de Software con IA |
| Versión | `vFinal-2.0.0-APROBADO` |
| Fecha | 26/05/2026 |
| Autora | Gina Fabiana Villanueva Viscarra |
| Estado | Aprobado |
| Relación con BRD | `docs/brd/BRD_vFinal.md` — aprobado |
| Documentos hijos esperados | `docs/prd/PRD_vFinal.md`, `docs/fsd/FSD_vFinal.md`, `docs/DTI.md` |
| Insumos principales | BRD aprobado, consigna M2, entrevistas a gerente, supervisor y vendedor, plan de investigación UX, plantillas del módulo 4 |
| Prompts utilizados | `PR-MRD-001` pendiente de registrar en `docs/PROMPT_MAPPING.md` |

---

## 1. Resumen ejecutivo

**App Detección Prod** atiende una oportunidad concreta en empresas distribuidoras e importadoras que operan en el canal retail: transformar la gestión de productos próximos a vencer desde un proceso informal, reactivo y fragmentado hacia una práctica digital, trazable, medible y orientada a decisiones comerciales. El mercado objetivo no se limita a un usuario individual; se trata de un ecosistema operativo-comercial formado por mercaderistas, vendedores, supervisores, gerencia comercial, trade marketing, finanzas y logística.

La investigación del proyecto muestra que el problema actual se sostiene en herramientas de baja estructura —WhatsApp, fotografías dispersas, Excel y comunicación verbal— que no fueron diseñadas para controlar vencimientos, acciones comerciales, precios modificados, cantidades intervenidas ni impacto financiero. Esta brecha afecta tanto a la operación diaria como a la toma de decisiones estratégicas: el mercaderista reporta sin retroalimentación, el vendedor decide con incertidumbre, el supervisor invierte tiempo validando datos y gerencia no cuenta con indicadores consolidados para priorizar acciones o medir rentabilidad.

El mercado potencial inicial está compuesto por distribuidoras e importadoras medianas o grandes con equipos de mercaderismo en ruta y presencia en múltiples puntos de venta. El valor diferencial del producto está en integrar cuatro dimensiones que suelen estar separadas: **detección operativa**, **gestión comercial**, **control de precio/cantidad** e **inteligencia ejecutiva**. Frente a alternativas como WhatsApp, Excel o ERP genéricos, App Detección Prod se posiciona como una solución especializada para reducir merma, mejorar trazabilidad, acelerar decisiones y construir evidencia financiera sobre cada acción aplicada.

El MRD define los segmentos, personas, jobs-to-be-done, propuesta de valor, panorama competitivo, estrategia de adopción, métricas de mercado, riesgos y requerimientos de mercado que alimentarán el PRD vFinal.

---

## 2. Visión del producto

> **Para empresas distribuidoras e importadoras del canal retail que pierden visibilidad y rentabilidad por productos próximos a vencer, App Detección Prod centraliza la detección, acción comercial, control de precios e indicadores para reducir merma y acelerar decisiones basadas en evidencia.**

### 2.1 Posición estratégica del producto

App Detección Prod no debe entenderse como una aplicación aislada de captura de datos, sino como una **plataforma de inteligencia operativa y comercial**. Su objetivo es conectar lo que ocurre en sala con las decisiones tácticas y estratégicas del negocio.

| Dimensión | Situación actual | Situación objetivo con App Detección Prod |
|---|---|---|
| Registro | Fotos y mensajes dispersos | Registro estructurado por producto, sala, fecha, cantidad y evidencia |
| Validación | Revisión manual en múltiples canales | Flujo centralizado con estados, responsables y auditoría |
| Acción comercial | Decisiones con información incompleta | Descuentos, bandeos, promociones, retiros o cambios trazables |
| Control de precio | Precio actual y precio modificado no siempre registrados | Comparación formal entre precio base, precio intervenido e impacto |
| Supervisión | Baja visibilidad en tiempo real | Panel táctico por prioridad, equipo, sala y SLA |
| Gerencia | Información tardía o agregada manualmente | Dashboard ejecutivo con KPIs financieros y operativos |
| Aprendizaje | No se sabe qué acción funcionó | Medición por acción, producto, tienda y región |

---

## 3. Análisis de mercado

### 3.1 Mercado objetivo

El mercado objetivo primario está conformado por empresas distribuidoras e importadoras que comercializan productos de consumo masivo, alimentos, bebidas, productos farmacéuticos, higiene, belleza, cuidado personal u otras categorías con fecha de vencimiento o ciclos de rotación sensibles.

Estas empresas suelen operar con:

- Equipos de mercaderistas en ruta.
- Supervisores regionales o de canal moderno.
- Vendedores responsables de cuentas retail.
- Gerencia comercial enfocada en ventas, rentabilidad, rotación y ejecución.
- Procesos de devolución, cambio, descuento, bandeo o promoción.
- Relación con supermercados, farmacias, micromercados y tiendas especializadas.

### 3.2 Segmentación TAM / SAM / SOM inicial

> **Nota metodológica:** al tratarse de un proyecto académico sin acceso a bases comerciales completas, las cifras se plantean como modelo estimativo cualitativo-cuantitativo para orientar priorización. En el PRD y roadmap se recomienda validar estos valores con investigación comercial real.

| Métrica | Definición para el proyecto | Valor estimado inicial | Fuente / método |
|---|---|---:|---|
| TAM — Total Addressable Market | Empresas distribuidoras/importadoras retail que gestionan productos con vencimiento en Bolivia y mercados comparables | Por medir con cámara sectorial, registros empresariales y benchmarking | Discovery comercial |
| SAM — Serviceable Addressable Market | Empresas con equipos de mercaderismo, supervisión regional y operación en cadenas retail | Segmento prioritario: medianas y grandes distribuidoras | Entrevistas + hipótesis BRD |
| SOM — Serviceable Obtainable Market | Primeras empresas piloto que podrían adoptar la solución en fase MVP | 1–3 empresas piloto / 3–6 equipos comerciales | Piloto académico / validación controlada |

### 3.3 Tendencias del sector relevantes

| Tendencia | Descripción | Oportunidad para App Detección Prod |
|---|---|---|
| Digitalización de ejecución retail | Las empresas buscan reemplazar reportes manuales por datos en campo | Captura móvil estructurada para mercaderistas |
| Gestión de merma y rentabilidad | La presión por margen obliga a reducir pérdidas por vencimiento | KPIs de merma evitada e impacto financiero |
| Trade marketing medible | Las promociones deben demostrar retorno, no solo ejecución | Medición de descuentos, bandeos y acciones por producto |
| Analítica operativa | Supervisores y gerentes necesitan datos en tiempo real | Dashboards tácticos y ejecutivos |
| Automatización de alertas | Anticipar problemas vale más que corregir pérdidas | Alertas por umbrales de vencimiento, cantidad y criticidad |
| IA asistiva con control humano | La IA se usa para priorizar, clasificar y sugerir, pero con revisión humana | Clasificación de riesgo, priorización y recomendaciones con guardrails |

### 3.4 Factores regulatorios y de cumplimiento

| Factor | Relevancia | Implicación para el producto |
|---|---|---|
| Protección de datos personales | Usuarios internos, rutas, tiendas, evidencias y trazabilidad pueden contener información sensible | Roles, permisos, auditoría y minimización de datos |
| Políticas comerciales internas | Descuentos, retiros, bandeos y cambios deben respetar reglas de la empresa | Reglas configurables y trazabilidad de aprobación |
| Normativa sanitaria / vencimientos | Algunos productos requieren cumplimiento estricto por fecha de expiración | Alertas y registro de acción antes de umbrales críticos |
| Auditoría financiera | Devoluciones, cambios y descuentos afectan rentabilidad | Evidencia y reportes auditables |
| Seguridad de evidencia visual | Fotografías en sala pueden contener información comercial | Control de acceso, almacenamiento seguro y retención definida |

---

## 4. Segmentación y personas

### 4.1 Segmentos de clientes y usuarios

| Segmento | Tamaño relativo | Necesidad principal | Disposición a adoptar | Origen / evidencia |
|---|---:|---|---|---|
| Mercaderistas | Alto dentro de operación de campo | Registrar rápido productos próximos a vencer sin duplicar trabajo | Alta si la app reduce pasos y carga cognitiva | Investigación M2 |
| Vendedores canal moderno | Medio | Decidir acciones comerciales con información confiable | Alta si mejora priorización y reduce visitas innecesarias | Entrevista vendedor |
| Supervisores regionales | Bajo-medio pero crítico | Validar, priorizar y controlar ejecución por equipo | Muy alta si reduce tiempo de validación y errores | Entrevista supervisor |
| Gerencia comercial | Bajo en cantidad, alto en decisión | Ver KPIs, impacto financiero y tendencias | Alta si el dashboard evidencia ROI | Entrevista gerente |
| Trade marketing | Medio | Medir efectividad de promociones, bandeos y descuentos | Media-alta si se integra con campañas | BRD |
| Administración / Finanzas | Bajo-medio | Cuantificar costo, pérdida, ahorro y rentabilidad | Media si los reportes son confiables | BRD |
| Logística | Medio | Anticipar retiros, cambios o reposiciones | Media si reduce urgencias y costos | BRD |

### 4.2 Persona 1 — Mercaderista de ruta

| Atributo | Descripción |
|---|---|
| Rol | Usuario operativo primario |
| Contexto | Visita salas retail, revisa góndolas, detecta productos próximos a vencer y reporta evidencia |
| Edad estimada | 20–55 años |
| Nivel digital | Uso básico de smartphone Android, WhatsApp y formularios simples |
| Objetivos | Registrar rápido, evitar reprocesos, cumplir ruta, reportar evidencia clara |
| Dolores | Fotos dispersas, reportes repetidos, falta de retroalimentación, presión de tiempo, conectividad variable |
| Necesidades | Flujo móvil simple, captura guiada, lista de productos, evidencia visual, estado del caso |
| Frase representativa | “Reporto, pero no siempre sé qué pasa después con lo que envié.” |
| Implicación para producto | La app debe minimizar carga cognitiva y funcionar bien en campo |

### 4.3 Persona 2 — Supervisor regional

| Atributo | Descripción |
|---|---|
| Rol | Usuario táctico de validación y control |
| Contexto | Recibe reportes de mercaderistas, valida información, prioriza casos y coordina acciones |
| Edad estimada | 30–55 años |
| Objetivos | Tener visibilidad real, reducir errores, controlar SLA, mejorar productividad del equipo |
| Dolores | Información desorganizada, validación lenta, presión por errores, incertidumbre sobre estado real |
| Necesidades | Bandeja de validación, filtros por criticidad, alertas, trazabilidad por mercaderista y tienda |
| Frase representativa | “Pierdo tiempo validando datos que deberían llegar completos y organizados.” |
| Implicación para producto | Debe existir un workflow de validación y priorización, no solo captura |

### 4.4 Persona 3 — Vendedor canal moderno

| Atributo | Descripción |
|---|---|
| Rol | Usuario comercial ejecutor |
| Contexto | Decide o gestiona descuentos, bandeos, promociones, activaciones o coordinación con clientes retail |
| Objetivos | Tomar decisiones rápidas, no duplicar acciones, priorizar oportunidades de venta |
| Dolores | Información incompleta, falta de historial, incertidumbre sobre si el producto ya fue gestionado |
| Necesidades | Vista de productos pendientes, estado de acción, precio actual/modificado, historial y aprobaciones |
| Frase representativa | “Necesito saber si ya se hizo algo con ese producto antes de decidir.” |
| Implicación para producto | Las acciones comerciales deben ser registradas, auditables y medibles |

### 4.5 Persona 4 — Gerencia comercial

| Atributo | Descripción |
|---|---|
| Rol | Decisor estratégico y sponsor del valor de negocio |
| Contexto | Evalúa ventas, rotación, rentabilidad, devolución, cambios, costo y desempeño regional |
| Objetivos | Reducir pérdidas, priorizar productos, medir impacto financiero y comparar desempeño |
| Dolores | Incertidumbre, datos dispersos, falta de KPIs, dificultad para medir acciones |
| Necesidades | Dashboard ejecutivo, indicadores de rotación, costo de devolución, costo de reposición, margen e impacto |
| Frase representativa | “Necesito ver datos confiables para tomar decisiones y medir si las acciones funcionan.” |
| Implicación para producto | Gerencia debe ser principalmente informada mediante dashboards, no ejecutora del flujo diario |

---

## 5. Jobs-to-be-Done

| JTBD ID | Cuando… | Quiero… | Para poder… | Segmento principal |
|---|---|---|---|---|
| JTBD-01 | encuentro un producto próximo a vencer en sala | registrarlo rápido con foto, vencimiento, cantidad y tienda | evitar que se pierda en WhatsApp y que el equipo actúe | Mercaderista |
| JTBD-02 | recibo múltiples reportes de productos | validar cuáles están completos y cuáles son críticos | priorizar atención y reducir errores | Supervisor |
| JTBD-03 | debo decidir una acción comercial | ver estado, precio, cantidad, vencimiento e historial | aplicar descuento, bandeo, retiro o promoción con certeza | Vendedor |
| JTBD-04 | hay productos con alto riesgo de vencimiento | recibir alertas tempranas por umbral | actuar antes de que se conviertan en pérdida | Supervisor / Vendedor |
| JTBD-05 | necesito evaluar desempeño comercial | ver KPIs por producto, sala, región y acción | medir merma, rentabilidad y efectividad | Gerencia |
| JTBD-06 | una acción comercial fue aplicada | conocer si redujo stock o evitó pérdida | aprender qué acciones funcionan | Gerencia / Trade marketing |
| JTBD-07 | debo justificar una devolución, cambio o descuento | consultar evidencia y trazabilidad | respaldar decisiones ante finanzas o dirección | Supervisor / Finanzas |
| JTBD-08 | un producto fue reportado varias veces | detectar duplicados o consolidar casos | evitar reprocesos y decisiones contradictorias | Supervisor |
| JTBD-09 | la conexión en sala es limitada | guardar el registro y sincronizar luego | no perder información de campo | Mercaderista |
| JTBD-10 | el volumen de reportes aumenta | filtrar por criticidad, fecha, sala y responsable | concentrarme en los casos de mayor impacto | Supervisor / Vendedor |

---

## 6. Análisis competitivo

### 6.1 Alternativas actuales y competidores indirectos

| Alternativa / competidor | Tipo | Fortaleza percibida | Debilidad frente a App Detección Prod |
|---|---|---|---|
| WhatsApp | Do-nothing / herramienta informal | Fácil, conocido, disponible en todos los celulares | Sin estructura, sin trazabilidad, sin métricas, difícil de auditar |
| Excel / Google Sheets | Herramienta manual | Flexible, bajo costo, permite consolidar algo de información | Requiere carga manual, propenso a errores, no gestiona evidencia ni workflow |
| Formularios genéricos | Indirecto | Estandariza captura básica | No gestiona estados, acciones comerciales ni impacto financiero |
| ERP comercial | Indirecto | Integra datos transaccionales de ventas/inventario | No suele capturar evidencia en sala ni flujo de mercaderismo en tiempo real |
| Sistemas de auditoría retail genéricos | Directo parcial | Pueden capturar datos de campo | Pueden no estar especializados en vencimientos, acciones comerciales, precio modificado e impacto financiero |
| Desarrollo interno ad hoc | Alternativa directa | Adaptación a reglas internas | Alto costo, riesgo técnico, difícil de mantener sin arquitectura clara |

### 6.2 Matriz comparativa

| Criterio | App Detección Prod | WhatsApp | Excel / Sheets | Formularios genéricos | ERP genérico | Auditoría retail genérica |
|---|---|---|---|---|---|---|
| Registro estructurado de producto | Alto | Bajo | Medio | Medio | Medio | Alto |
| Evidencia visual asociada a caso | Alto | Medio-bajo | Bajo | Medio | Bajo | Alto |
| Control de fecha de vencimiento | Alto | Bajo | Medio | Medio | Medio | Alto |
| Registro de acción comercial | Alto | Bajo | Medio | Bajo-medio | Medio | Medio |
| Control precio actual / nuevo precio | Alto | Bajo | Medio | Bajo | Medio | Variable |
| Workflow de validación | Alto | Bajo | Bajo | Bajo | Variable | Medio |
| Dashboard gerencial | Alto | Nulo | Bajo-medio | Bajo | Alto generalista | Medio |
| Medición de impacto financiero | Alto | Nulo | Bajo | Bajo | Medio | Variable |
| Alertas tempranas | Alto | Nulo | Bajo | Bajo-medio | Variable | Medio |
| IA asistiva con guardrails | Medio-alto planificado | Nulo | Nulo | Nulo | Nulo/variable | Variable |
| Trazabilidad end-to-end | Alto | Bajo | Medio-bajo | Medio | Medio | Medio-alto |
| Ajuste específico al dominio | Alto | Bajo | Bajo | Bajo | Bajo-medio | Medio |

### 6.3 Positioning statement

> Para **empresas distribuidoras e importadoras con equipos de mercaderismo en canal retail**, que actualmente gestionan productos próximos a vencer mediante WhatsApp, Excel y reportes dispersos, **App Detección Prod** es una plataforma especializada de trazabilidad e inteligencia comercial que centraliza detección, evidencia, acciones, precios, cantidades e indicadores, a diferencia de herramientas genéricas que no conectan la operación en campo con el impacto financiero y la decisión gerencial.

### 6.4 Ventaja competitiva sostenible

| Fuente de ventaja | Explicación | Cómo se protege |
|---|---|---|
| Especialización en vencimientos retail | El producto se diseña alrededor del flujo real de merma, no como formulario genérico | Casos de uso, reglas y KPIs específicos del dominio |
| Trazabilidad operativa-comercial | Conecta detección, validación, acción e impacto | Modelo de datos y workflow end-to-end |
| Evidencia + decisión + métrica | Une foto, datos, estado, acción y resultado financiero | Dashboard y auditoría integrados |
| Aprendizaje por acción comercial | Permite saber qué descuentos, bandeos o retiros funcionan | Historial analítico por producto, sala y región |
| IA controlada | Prioriza y clasifica sin reemplazar decisiones humanas críticas | Guardrails, auditoría y human-in-the-loop |
| Arquitectura evolutiva | Puede iniciar como monolito modular y crecer por bounded contexts | DTI y ADRs orientados a evolución sostenible |

---

## 7. Propuesta de valor

### 7.1 Value Proposition Canvas resumido

| Eje | Contenido |
|---|---|
| Cliente / usuario principal | Empresas distribuidoras e importadoras con operación retail y equipos de mercaderismo |
| Job principal | Detectar y gestionar productos próximos a vencer antes de que generen pérdida financiera |
| Dolores | Reportes dispersos, falta de trazabilidad, validación lenta, decisiones comerciales inciertas, ausencia de KPIs |
| Ganancias esperadas | Menor merma, decisiones rápidas, visibilidad ejecutiva, control de acciones, evidencia auditable |
| Productos y servicios | App móvil de registro, workflow de validación, módulo de acciones comerciales, dashboard, alertas, IA asistiva |
| Pain relievers | Centralización, estados, evidencia, historial, alertas, reglas y KPIs |
| Gain creators | Medición de impacto, priorización, reducción de tiempo, aprendizaje comercial, mejora de rentabilidad |

### 7.2 Propuesta de valor por segmento

| Segmento | Valor esperado |
|---|---|
| Mercaderista | Menos pasos, menos reproceso, registro guiado, claridad de estado |
| Supervisor | Menos tiempo validando, más control, priorización por criticidad, trazabilidad por equipo |
| Vendedor | Decisiones comerciales con información completa y actualizada |
| Gerencia | Visibilidad ejecutiva, KPIs, impacto financiero, comparativos y tendencias |
| Finanzas | Evidencia para costos, devoluciones, cambios y ROI |
| Trade marketing | Evaluación de efectividad de descuentos, bandeos y promociones |
| Logística | Anticipación de retiros, cambios y reposiciones |

---

## 8. Pricing y modelo de negocio

### 8.1 Modelo recomendado para evolución comercial

Para una solución como App Detección Prod, el modelo más coherente es **SaaS B2B por empresa**, con variables por número de usuarios, salas, regiones o módulos.

| Modelo | Ventaja | Riesgo | Recomendación |
|---|---|---|---|
| Suscripción mensual por usuario | Fácil de entender y escalar | Puede desalentar alta adopción en campo | Útil para MVP comercial |
| Suscripción por empresa + rangos de usuarios | Facilita adopción amplia | Requiere buena segmentación de planes | Recomendado |
| Precio por sala/punto de venta | Alineado a operación retail | Puede ser difícil si hay salas variables | Complementario |
| Pago por módulo avanzado | Monetiza dashboard IA/analítica | Puede fragmentar valor | Recomendado para fases premium |
| Proyecto a medida | Mayor ingreso inicial | Alto costo de implementación | Solo para clientes enterprise |

### 8.2 Planes conceptuales

| Plan | Cliente objetivo | Incluye |
|---|---|---|
| Piloto | 1 región / equipo reducido | Registro, validación básica, dashboard inicial |
| Operativo | Distribuidora mediana | Registro, workflows, alertas, acciones comerciales, reportes |
| Enterprise | Distribuidora grande / varias regiones | KPIs avanzados, IA asistiva, integraciones, auditoría y roles avanzados |

### 8.3 Variables para validar disposición a pagar

- Costo mensual de merma por vencimiento.
- Horas de supervisión invertidas en validación manual.
- Costo de devoluciones/cambios.
- Cantidad de productos gestionados por mes.
- Número de salas y rutas.
- Valor financiero recuperado por acciones oportunas.
- Costo actual de herramientas manuales y reprocesos.

---

## 9. Go-to-market

### 9.1 Estrategia de entrada al mercado

El mercado objetivo requiere una estrategia de entrada consultiva, porque el problema no siempre está cuantificado. Muchas empresas saben que existe merma, pero no miden con precisión cuánto se pierde por falta de trazabilidad.

La estrategia recomendada es:

1. Diagnóstico inicial gratuito o de bajo costo.
2. Piloto con una región, línea de productos o cadena retail específica.
3. Medición de línea base: tiempo de validación, número de productos críticos, acciones aplicadas, merma estimada.
4. Implementación del MVP.
5. Comparación antes/después.
6. Caso de negocio para expansión.

### 9.2 Canales de adquisición

| Canal | Uso recomendado |
|---|---|
| Venta directa B2B | Principal para distribuidoras medianas y grandes |
| Referidos sectoriales | Alto valor por confianza en ecosistema retail |
| Alianzas con consultores comerciales / trade marketing | Permite entrar por dolor operativo |
| Cámaras empresariales / ferias retail | Generación de leads |
| LinkedIn / contenido ejecutivo | Educación del mercado sobre merma y trazabilidad |
| Pilotos académicos / demostradores | Validación inicial del producto |

### 9.3 Estrategia de lanzamiento

| Fase | Objetivo | Actividades |
|---|---|---|
| Pre-launch | Validar problema y flujo | Entrevistas, shadowing, prototipo, refinamiento de casos de uso |
| Piloto | Medir valor operacional | Implementar MVP con una muestra controlada de usuarios |
| Launch inicial | Expandir dentro de la empresa piloto | Capacitación, dashboards, métricas de adopción |
| Post-launch | Consolidar ROI | Reporte de impacto, ajustes, nuevas integraciones |
| Escalamiento | Replicar en otras empresas | Casos de éxito, planes SaaS, roadmap enterprise |

### 9.4 Funnel AARRR inicial

| Etapa | Métrica | Meta inicial |
|---|---|---|
| Acquisition | Empresas interesadas en diagnóstico | 5–10 leads cualificados |
| Activation | Empresas que aceptan piloto | 1–3 pilotos |
| Retention | Usuarios activos semanales durante piloto | ≥ 70 % de usuarios asignados |
| Revenue | Conversión piloto a plan operativo | ≥ 1 cliente convertido |
| Referral | Recomendación dentro del sector | 1 referido por cliente exitoso |

---

## 10. Métricas de éxito del producto en mercado

### 10.1 North Star Metric

> **Porcentaje de productos próximos a vencer gestionados con acción comercial trazable antes del umbral crítico definido.**

Esta métrica concentra el valor del producto porque combina detección, trazabilidad, acción oportuna y reducción potencial de pérdida.

### 10.2 KPIs secundarios

| ID | KPI | Línea base | Meta inicial | Horizonte | Fuente |
|---|---|---:|---:|---|---|
| MRD-KPI-01 | Tiempo promedio de validación de reporte | Por medir | -30 % | Piloto 8–12 semanas | App + entrevistas |
| MRD-KPI-02 | % de reportes con datos completos | Por medir | ≥ 85 % | Piloto | App |
| MRD-KPI-03 | % de productos críticos con acción registrada | Por medir | ≥ 80 % | Piloto | App |
| MRD-KPI-04 | Merma estimada evitada | Por medir | Línea base + mejora | 3–6 meses | App + Finanzas |
| MRD-KPI-05 | Tasa de duplicidad de reportes | Por medir | -40 % | Piloto | App |
| MRD-KPI-06 | Adopción semanal de mercaderistas | Por medir | ≥ 75 % | Piloto | Telemetría |
| MRD-KPI-07 | Satisfacción de supervisores | Por medir | ≥ 4/5 | Piloto | Encuesta |
| MRD-KPI-08 | Casos con evidencia visual válida | Por medir | ≥ 90 % | Piloto | Auditoría |

---

## 11. Requerimientos de mercado de alto nivel

| ID | Requerimiento de mercado | Prioridad | Justificación | Se trazará a PRD |
|---|---|---|---|---|
| MRD-N-001 | La solución debe permitir registro móvil simple en campo | Must | El mercaderista es el usuario núcleo y opera bajo presión de tiempo | PRD-REQ-001 |
| MRD-N-002 | La solución debe centralizar reportes con evidencia visual | Must | El problema actual es la dispersión de fotos y mensajes | PRD-REQ-002 |
| MRD-N-003 | La solución debe registrar fecha de vencimiento, cantidad, precio actual y tienda | Must | Son datos mínimos para decidir acción comercial | PRD-REQ-003 |
| MRD-N-004 | La solución debe permitir registrar acción comercial aplicada | Must | El negocio necesita medir descuentos, bandeos, retiros y promociones | PRD-REQ-004 |
| MRD-N-005 | La solución debe manejar estados de validación y seguimiento | Must | Supervisión necesita controlar avance y reducir incertidumbre | PRD-REQ-005 |
| MRD-N-006 | La solución debe mostrar dashboard ejecutivo para gerencia | Must | Gerencia necesita información consolidada e impacto financiero | PRD-REQ-006 |
| MRD-N-007 | La solución debe generar alertas por umbral de vencimiento | Should | La oportunidad está en actuar antes de la pérdida | PRD-REQ-007 |
| MRD-N-008 | La solución debe calcular indicadores de merma, rotación e impacto | Must | Diferencial clave frente a herramientas genéricas | PRD-REQ-008 |
| MRD-N-009 | La solución debe permitir trazabilidad por usuario, sala, producto y acción | Must | Requerido para auditoría y confianza | PRD-REQ-009 |
| MRD-N-010 | La solución debe contemplar conectividad variable en campo | Should | Mercaderistas pueden operar en salas con señal limitada | PRD-REQ-010 |
| MRD-N-011 | La solución debe permitir roles diferenciados | Must | Cada segmento tiene responsabilidades distintas | PRD-REQ-011 |
| MRD-N-012 | La solución debe incorporar IA asistiva con control humano | Could / Should | Diferenciador avanzado sin delegar decisiones críticas | PRD-REQ-012 |

---

## 12. Supuestos e hipótesis a validar

| ID | Hipótesis | Método de validación | Criterio de éxito |
|---|---|---|---|
| H-001 | Los mercaderistas adoptarán una app si reduce reproceso y mantiene flujo simple | Prueba de prototipo + piloto | ≥ 75 % completa registros sin asistencia |
| H-002 | Supervisores reducirán tiempo de validación con reportes estructurados | Comparación antes/después | -30 % de tiempo promedio |
| H-003 | Vendedores tomarán mejores decisiones si ven historial y estado del producto | Entrevista + task test | ≥ 4/5 en utilidad percibida |
| H-004 | Gerencia valorará el producto si ve impacto financiero y no solo registros | Demo ejecutiva + dashboard piloto | Sponsor aprueba expansión o continuidad |
| H-005 | Las acciones comerciales se pueden estandarizar en categorías comunes | Taller con ventas/trade marketing | ≥ 80 % de casos entran en categorías definidas |
| H-006 | La evidencia visual puede ser capturada con calidad suficiente en campo | Piloto de captura | ≥ 90 % de fotos aceptables |
| H-007 | La IA puede clasificar criticidad sin tomar decisiones irreversibles | POC IA con dataset controlado | ≥ 85 % consistencia y 0 acciones críticas automáticas |
| H-008 | El principal valor económico provendrá de evitar pérdida y no solo de ahorrar tiempo | Análisis financiero piloto | Merma evitada o recuperada demostrable |

---

## 13. Riesgos de mercado

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Baja adopción por mercaderistas | Media | Alta | Flujo simple, capacitación, diseño móvil centrado en campo, modo offline/pendiente |
| El negocio no tiene línea base de merma | Alta | Alta | Iniciar con medición diagnóstica y construir línea base durante piloto |
| Gerencia percibe el producto como “solo una app operativa” | Media | Alta | Enfatizar dashboard, impacto financiero y ROI desde el inicio |
| Resistencia a cambiar WhatsApp | Alta | Media-alta | Integrar transición gradual y mostrar reducción de reprocesos |
| Datos de inventario/precio no disponibles | Media | Alta | Diseñar MVP con carga manual mínima y preparar integración futura |
| Acciones comerciales no estandarizadas | Media | Media | Catálogo configurable de acciones y reglas por empresa |
| Competidor genérico ofrece solución más barata | Media | Media | Diferenciar por dominio, trazabilidad e indicadores financieros |
| IA genera desconfianza | Media | Media | IA solo asistiva, con guardrails, auditoría y aprobación humana |
| Falta de sponsor activo | Media | Alta | Formalizar métricas de éxito y reportes ejecutivos periódicos |
| Sobrecarga funcional del MVP | Media | Alta | Priorizar flujo crítico: registrar → validar → accionar → medir |

---

## 14. Trazabilidad MRD → BRD → PRD

| MRD ID | Necesidad de mercado | BRD vinculado | PRD esperado |
|---|---|---|---|
| MRD-N-001 | Registro móvil simple en campo | BR-001, BO-01 | PRD-REQ-001, PRD-US-001 |
| MRD-N-002 | Centralización de evidencia | BR-002 | PRD-REQ-002, PRD-US-002 |
| MRD-N-003 | Datos mínimos de vencimiento, cantidad y precio | BR-003 | PRD-REQ-003, PRD-US-003 |
| MRD-N-004 | Registro de acción comercial | BR-004 | PRD-REQ-004, PRD-US-004 |
| MRD-N-005 | Estados de validación y seguimiento | BR-005 | PRD-REQ-005, PRD-US-005 |
| MRD-N-006 | Dashboard ejecutivo | BR-006, BO-03 | PRD-REQ-006, PRD-US-006 |
| MRD-N-007 | Alertas tempranas | BR-007 | PRD-REQ-007, PRD-US-007 |
| MRD-N-008 | KPIs de merma e impacto financiero | BR-008, BO-02 | PRD-REQ-008, PRD-US-008 |
| MRD-N-009 | Trazabilidad por usuario, producto, sala y acción | BR-009 | PRD-REQ-009, PRD-US-009 |
| MRD-N-010 | Conectividad variable | BR-010 | PRD-NFR-004 |
| MRD-N-011 | Roles diferenciados | BR-011 | PRD-REQ-011 |
| MRD-N-012 | IA asistiva con control humano | BR-012 | PRD-REQ-012, PRD-NFR-IA-001 |

---

## 15. Recomendación de alcance para PRD vFinal

Para mantener foco y defender bien el proyecto en la rama `release/2.0.0`, el PRD debe priorizar un MVP robusto antes que una cobertura excesiva.

### 15.1 MVP recomendado

| Módulo | Incluir en MVP | Justificación |
|---|---|---|
| Registro de producto próximo a vencer | Sí | Es el punto de origen del valor |
| Evidencia visual | Sí | Sustituye fotos dispersas por evidencia trazable |
| Validación supervisor | Sí | Dolor crítico identificado en entrevistas |
| Acción comercial | Sí | Conecta operación con negocio |
| Dashboard gerencial básico | Sí | Necesario para sponsor y defensa |
| Alertas por vencimiento | Sí | Diferencial operativo |
| IA asistiva | Parcial / POC | Conviene demostrar como riesgo controlado, no como dependencia del MVP |
| Integración ERP | No en MVP | Alto riesgo, dejar como roadmap |
| Optimización avanzada de precios | No en MVP | Requiere datos históricos y madurez analítica |

### 15.2 Principios de producto para PRD

1. Todo registro debe estar asociado a producto, tienda, fecha, usuario y evidencia.
2. Toda acción comercial debe tener estado, responsable e impacto esperado o medido.
3. Gerencia no debe operar el flujo diario; debe recibir información consolidada.
4. La IA no debe ejecutar decisiones comerciales irreversibles sin aprobación humana.
5. El producto debe medir valor, no solo digitalizar reportes.

---

## 16. Anexos

### 16.1 Evidencia cualitativa sintetizada

| Rol | Evidencia de dolor | Requerimiento derivado |
|---|---|---|
| Mercaderista | Reportes manuales, presión de tiempo, fotos y WhatsApp | Registro móvil guiado |
| Supervisor | Validación lenta, información incompleta, presión por errores | Workflow de validación y prioridad |
| Vendedor | Decisiones con incertidumbre, falta de historial | Vista de acciones, estado e historial |
| Gerencia | Falta de visibilidad, métricas e impacto financiero | Dashboard ejecutivo y KPIs |

### 16.2 Glosario de mercado

| Término | Definición |
|---|---|
| Merma | Pérdida económica asociada a productos no vendidos, vencidos, dañados o retirados |
| Canal retail | Puntos de venta como supermercados, farmacias, tiendas especializadas y micromercados |
| Mercaderista | Personal de campo que revisa y reporta productos en sala |
| Bandeo | Acción comercial que agrupa productos o genera packs/promociones para acelerar rotación |
| Acción comercial | Descuento, promoción, bandeo, retiro, cambio, reposición u otra medida para gestionar producto |
| Producto crítico | Producto con alta probabilidad de pérdida por vencimiento cercano, baja rotación o alto valor |
| SLA de validación | Tiempo máximo esperado para que un reporte sea revisado y priorizado |
| Dashboard ejecutivo | Vista consolidada de KPIs para gerencia o dirección |
| Human-in-the-loop | Patrón donde una decisión asistida por IA requiere revisión o aprobación humana |

### 16.3 Registro de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| vFinal-2.0.0 | 26/05/2026 | Gina Fabiana Villanueva Viscarra | MRD inicial para revisión, derivado del BRD aprobado |

---

## 17. Checklist de calidad del MRD

- [x] Relación explícita con BRD aprobado.
- [x] Mercado objetivo definido.
- [x] Segmentos y personas identificadas.
- [x] Jobs-to-be-Done documentados.
- [x] Competidores directos, indirectos y alternativa do-nothing comparados.
- [x] Propuesta de valor clara.
- [x] Modelo de negocio sugerido.
- [x] Go-to-market inicial definido.
- [x] North Star Metric y KPIs secundarios propuestos.
- [x] Requerimientos de mercado trazables al PRD.
- [x] Hipótesis y riesgos de mercado documentados.
- [x] Recomendación de alcance para PRD vFinal.
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


### 6. Lectura de mercado para MRD

Desde mercado, la trazabilidad de cambio de precio diferencia a App Detección Prod de alternativas informales como WhatsApp, Excel o reportes manuales. El valor no está solo en saber que un producto está por vencer, sino en saber **qué precio se modificó, por qué, quién lo autorizó y qué impacto produjo**. Esta capacidad fortalece la propuesta de valor para distribuidoras que necesitan defender margen en canal retail.
