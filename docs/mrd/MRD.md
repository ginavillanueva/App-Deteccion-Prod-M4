### MRD.md – Market Requirements Document (actualizado con 4 actores)

# MRD – App Detección Prod

## 0. Metadatos

| Campo                   | Valor                            |
| ----------------------- | -------------------------------- |
| Producto                | App Detección Prod               |
| Grupo                   | G07                              |
| Versión                 | v0.2                             |
| Fecha                   | 14/05/2026                       |
| Product Manager / Autor | Gina Fabiana Villanueva Viscarra |
| Revisores               | Docente + stakeholders           |
| Estado                  | Borrador                         |
| Relación con BRD        | BRD v0.1                         |

## 1. Resumen ejecutivo

App Detección Prod centraliza la gestión de productos críticos próximos a vencer para distribuidores e importadores en canal moderno. Permite a **mercaderistas, vendedores, supervisores y gerentes comerciales** registrar, validar y analizar información operativa y comercial, generando indicadores estratégicos y alertas en tiempo real. La plataforma mejora la eficiencia operativa, reduce pérdidas y soporta decisiones estratégicas basadas en datos confiables.

## 2. Visión del producto

"Para distribuidores e importadores en canal moderno, una plataforma digital centralizada que optimiza la gestión de productos críticos, reduce pérdidas y mejora decisiones estratégicas en tiempo real para todos los actores del ecosistema."

## 3. Análisis de mercado

### 3.1 Tamaño de mercado

| Métrica | Valor        | Fuente                                      |
| ------- | ------------ | ------------------------------------------- |
| TAM     | 500 empresas | Datos internos y Cámara de Comercio Bolivia |
| SAM     | 350 empresas | Segmento con adopción tecnológica inicial   |
| SOM     | 200 empresas | Objetivo alcanzable en 12 meses             |

### 3.2 Tendencias del sector

* Incremento de soluciones digitales de trazabilidad en retail.
* Demanda de métricas estratégicas en tiempo real.
* Integración de IA para alertas y decisiones predictivas.

### 3.3 Factores regulatorios

* Ley 164 Bolivia, ASFI, PCI-DSS, GDPR.

### 3.4 Cadencia de Continuous Discovery

| Aspecto            | Valor                                                        |
| ------------------ | ------------------------------------------------------------ |
| Entrevistas        | Semanal                                                      |
| Usuarios por ciclo | 6 (Mercaderistas, Vendedores, Supervisores, Gerentes)        |
| Formato hipótesis  | Cuando `<situación>`, espero `<resultado>`, porque `<razón>` |
| Output track       | Actualiza segmentos, personas, requerimientos y métricas     |

## 4. Segmentación y personas

### 4.1 Segmentos de clientes

| Segmento             | Tamaño | Necesidad principal                                              | Origen M2   |
| -------------------- | ------ | ---------------------------------------------------------------- | ----------- |
| Mercaderistas        | 300    | Registro y reportes de productos críticos                        | M2/Personas |
| Vendedores           | 50     | Consolidación de información y ejecución de acciones comerciales | M2/Personas |
| Supervisores         | 50     | Validación y control de acciones                                 | M2/Personas |
| Gerentes Comerciales | 20     | Toma de decisiones estratégicas                                  | M2/Personas |

### 4.2 Personas

#### Persona 1 – Mercaderista

* Rol: Operativo en campo
* Contexto: visita diaria a puntos de venta
* Jobs-to-be-done: registrar productos, reportar acciones, enviar evidencia
* Dolores: información dispersa, alta carga cognitiva
* Ganancia: trazabilidad completa, reducción de errores y tiempo operativo
* Frase representativa: "Reporto, pero no sé qué pasa después."

#### Persona 2 – Vendedor

* Rol: Comercial / ejecutor
* Contexto: gestiona varias salas, activa promociones
* Jobs-to-be-done: consolidar información, aplicar descuentos, verificar disponibilidad
* Dolores: información fragmentada, retrasos y errores por múltiples fuentes
* Ganancia: visibilidad centralizada, rapidez en la toma de decisiones

#### Persona 3 – Supervisor Regional

* Rol: Táctico / validación
* Contexto: supervisa múltiples rutas de mercaderistas y vendedores
* Jobs-to-be-done: validar reportes, controlar acciones, corregir desviaciones
* Dolores: tiempo elevado en validación manual, falta de visibilidad en tiempo real
* Ganancia: alertas y dashboards consolidados, capacidad de decisión rápida

#### Persona 4 – Gerente Comercial

* Rol: Estratégico
* Contexto: analiza KPIs y decisiones de negocio
* Jobs-to-be-done: priorizar productos, optimizar rentabilidad, supervisar cumplimiento de objetivos
* Dolores: falta de visibilidad de acciones operativas, incertidumbre sobre impacto financiero
* Ganancia: métricas confiables, decisiones basadas en datos, reducción de pérdidas

## 5. Jobs-to-be-Done (JTBD)

| JTBD ID | Cuando…                               | Quiero…                              | Para poder…                                     |
| ------- | ------------------------------------- | ------------------------------------ | ----------------------------------------------- |
| JTBD-01 | Recibo reporte disperso               | Consolidar información en un sistema | Tomar decisiones rápidas y precisas             |
| JTBD-02 | El producto se aproxima a vencimiento | Aplicar acciones comerciales         | Reducir pérdidas y rotación eficiente           |
| JTBD-03 | Supervisar múltiples rutas            | Visualizar métricas centralizadas    | Detectar desviaciones y priorizar acciones      |
| JTBD-04 | Analizar impacto financiero           | Generar indicadores estratégicos     | Decidir prioridades de inventario y promociones |

## 6. Análisis competitivo

| Criterio              | Nuestro producto    | Competidor A | Competidor B    | Competidor C         |
| --------------------- | ------------------- | ------------ | --------------- | -------------------- |
| Precio                | Suscripción B2B     | Gratuito     | ERP empresarial | App auditoría retail |
| Cobertura geográfica  | Nacional            | Local        | Nacional        | Regional             |
| Integración con pagos | Sí (opcional)       | No           | Parcial         | Parcial              |
| Uso de IA             | Alertas predictivas | No           | Limitado        | No                   |
| SLA                   | 99,9 % uptime       | Variable     | 99 %            | No garantiza         |

### 6.2 Positioning statement

Para supervisores y gerentes, que necesitan visibilidad y trazabilidad, nuestro producto es una plataforma centralizada que permite gestión eficiente y decisiones estratégicas, a diferencia de herramientas manuales como WhatsApp y Excel.

### 6.3 Ventaja competitiva sostenible

* Integración de datos operativos y comerciales.
* Alertas y métricas estratégicas en tiempo real.
* Reducción medible de pérdidas y errores.

## 7. Propuesta de valor

| Gains                      | Pains                 | Gains relievers              | Pain relievers     | Products & services              |
| -------------------------- | --------------------- | ---------------------------- | ------------------ | -------------------------------- |
| Visibilidad en tiempo real | Información dispersa  | Dashboard centralizado       | Alertas inmediatas | Plataforma móvil y dashboard web |
| Toma de decisiones rápida  | Validaciones manuales | Métricas y KPIs estratégicos | Flujo unificado    | Registro de acciones comerciales |

## 8. Pricing y modelo de negocio

* Modelo: SaaS B2B, suscripción anual por usuario.
* Estructura de precios: básica (usuarios limitados), premium (full), enterprise.

## 9. Go-to-market

* Directo: fuerza de ventas internas.
* Digital: email marketing, SEO, LinkedIn.
* Partners: distribuidores y supermercados estratégicos.

## 10. Métricas de éxito

* North Star: % productos críticos gestionados correctamente.
* KPIs secundarios: reducción de devoluciones, tiempo de validación, trazabilidad completa.

## 11. Requerimientos de mercado

| ID       | Requerimiento                      | Prioridad | Justificación            |
| -------- | ---------------------------------- | --------- | ------------------------ |
| MRD-N-01 | Soportar 10k usuarios concurrentes | Must      | Escalabilidad nacional   |
| MRD-N-02 | Integración con pagos QR Bolivia   | Must      | Preferencia del segmento |

## 12. Supuestos e hipótesis

| ID | Hipótesis                                  | Cómo validar        | Criterio de éxito           |
| -- | ------------------------------------------ | ------------------- | --------------------------- |
| H1 | 60 % de usuarios adoptará sistema digital  | Encuesta piloto     | ≥ 55 % adopción             |
| H2 | Alertas predictivas reducen errores        | POC                 | ≥ 80 % precisión en alertas |
| H3 | Centralización reduce tiempo de validación | Test en ruta piloto | -60 % tiempo promedio       |

## 13. Riesgos de mercado

| Riesgo                            | Probabilidad | Impacto | Mitigación              |
| --------------------------------- | ------------ | ------- | ----------------------- |
| Competidor lanza solución similar | Media        | Alto    | Acelerar time-to-market |
| Baja adopción                     | Media        | Alto    | Capacitación y soporte  |

## 14. Trazabilidad

| MRD ID   | BRD    | PRD        |
| -------- | ------ | ---------- |
| MRD-N-01 | BR-001 | PRD-REQ-01 |
| MRD-N-02 | BR-002 | PRD-REQ-02 |

## 15. Anexos

* Resúmenes de entrevistas
* Datos cuantitativos de mercado
* Benchmarks de competencia

## 16. Registro de cambios

| Versión | Fecha      | Autor                            | Cambio                                                              |
| ------- | ---------- | -------------------------------- | ------------------------------------------------------------------- |
| v0.2    | 14/05/2026 | Gina Fabiana Villanueva Viscarra | Personas actualizadas a Mercaderista, Vendedor, Supervisor, Gerente |
