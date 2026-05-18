
# AVANCE DTI — MICROSERVICES PATTERNS APLICADO A APP DETECCIÓN PROD
## Evaluación Arquitectónica Evolutiva Basada en Microservices Patterns de Chris Richardson

---

# Programa
Maestría en Desarrollo de Productos de Software con IA

# Módulo
Arquitectura de Software y Diseño de Sistemas

# Proyecto
App Detección Prod

# Autor
Gina Fabiana Villanueva Viscarra

---

# 1. Introducción

El presente documento constituye un avance arquitectónico del DTI (Documento Técnico Integral) del proyecto “App Detección Prod”, elaborado a partir del análisis del Capítulo 1 del libro *Microservices Patterns* de Chris Richardson y complementado con investigación técnica de nivel medio‑alto sobre:

- Circuit Breaker
- Consistent Hashing

El objetivo del entregable es:

- analizar la arquitectura actual del producto,
- evaluar la aplicabilidad de microservicios,
- identificar riesgos de complejidad distribuida,
- proponer una estrategia evolutiva adecuada,
- relacionar resiliencia y escalabilidad con el contexto real del negocio,
- mapear dichas decisiones dentro del DTI:
  - Logical View,
  - Process View,
  - Development View,
  - Physical View,
  - Scenarios.

Este análisis integra:

- investigación UX,
- arquitectura de información,
- entrevistas,
- visión estratégica,
- contexto organizacional,
- comportamiento operativo real,
- evolución futura del producto.

---

# 2. Contexto Estratégico del Proyecto

## 2.1 Problema Organizacional

App Detección Prod nace como respuesta a un problema estructural presente en distribuidoras e importadoras que operan en el canal retail.

Actualmente, la gestión de productos próximos a vencer depende principalmente de:

- WhatsApp,
- fotografías dispersas,
- Excel,
- comunicación verbal,
- validaciones humanas,
- coordinación manual entre áreas.

Esto genera:

- pérdida de trazabilidad,
- ausencia de métricas,
- sobrecarga cognitiva,
- retrasos operativos,
- decisiones reactivas,
- falta de visibilidad estratégica,
- incremento de merma,
- impacto financiero negativo.

El documento base del proyecto establece que el problema no es únicamente tecnológico, sino estructural y sistémico. Existe una desconexión entre operación y estrategia comercial. fileciteturn2file0L1-L220

---

# 2.2 Objetivo Transformacional

El proyecto busca transformar un modelo operativo reactivo y fragmentado en un sistema:

- centralizado,
- trazable,
- medible,
- resiliente,
- alineado con objetivos estratégicos,
- centrado en el usuario.

---

# 3. Flujo Operativo Real Validado

Luego de reanalizar entrevistas, avances previos y comportamiento operativo real, se identificó el siguiente flujo organizacional:

# Flujo principal

Mercaderista → Vendedor → Supervisor → Gerencia

---

# Flujo alternativo detectado

Mercaderista → Supervisor → Gerencia

Este bypass operacional ocurre cuando:

- el vendedor no responde,
- existe urgencia comercial,
- hay riesgo inmediato de vencimiento,
- el supervisor solicita información directa,
- se requiere validación rápida.

---

# 3.1 Implicancias Arquitectónicas del Flujo

Este comportamiento evidencia:

- alta dependencia humana,
- falta de centralización,
- ausencia de trazabilidad transversal,
- debilidad en sincronización,
- arquitectura operacional informal,
- procesos no estructurados.

Desde una perspectiva arquitectónica, esto implica que:

el sistema futuro deberá soportar:

- asincronía,
- validaciones distribuidas,
- resiliencia,
- consistencia operativa,
- visibilidad en tiempo real.

---

# 4. Relación con Microservices Patterns

Chris Richardson plantea que la arquitectura de microservicios aparece cuando:

- los sistemas crecen,
- existen múltiples dominios,
- la complejidad funcional aumenta,
- se requiere escalabilidad,
- aparecen necesidades de despliegue independiente.

Sin embargo, también advierte que los microservicios introducen nuevos desafíos:

- complejidad distribuida,
- fallos parciales,
- problemas de observabilidad,
- resiliencia obligatoria,
- latencia,
- consistencia eventual,
- complejidad DevOps.

Por ello:

NO todos los sistemas deben comenzar directamente con microservicios.

---

# 5. Evaluación Arquitectónica del DTI

# 5.1 Logical View

# 5.1.1 Dominios Identificados

## Detection Context
Gestión de productos próximos a vencer.

## Commercial Context
Promociones, descuentos y bandeos.

## Pricing Context
Control de precios modificados.

## Analytics Context
KPIs y métricas estratégicas.

## Notification Context
Alertas y seguimiento operacional.

## Media Context
Evidencia fotográfica.

## User Management Context
Roles y permisos.

## Reporting Context
Dashboards gerenciales.

---

# 5.1.2 Análisis Arquitectónico

El sistema presenta bounded contexts claramente diferenciados.

Esto evidencia:

- separación natural de responsabilidades,
- crecimiento funcional modular,
- posibilidades futuras de desacoplamiento.

Sin embargo:

- el producto aún se encuentra validando hipótesis,
- no existen equipos independientes,
- el MVP aún no alcanza complejidad distribuida crítica.

---

# 5.1.3 Decisión Arquitectónica

⚠️ Microservicios NO recomendados inicialmente.

✅ Arquitectura recomendada:
Monolito Modular Evolutivo.

---

# 5.1.4 Justificación Técnica

El sistema sí cumple criterios de:

- decomposition by business capability,
- decomposition by subdomain.

Pero actualmente NO requiere:

- despliegues independientes complejos,
- coordinación distribuida avanzada,
- infraestructura cloud madura.

---

# 5.1.5 Referencias Aplicadas

- §3.5 — Decomposition by Business Capability
- §3.5.1 — Decomposition by Subdomain

---

# 5.1.6 Aplicabilidad Real

La modularización permitirá:

- desacoplar analytics,
- separar multimedia,
- independizar dashboards,
- escalar módulos específicos,
- reducir deuda técnica futura.

---

# 5.2 Process View

# 5.2.1 Flujo Operativo Actual

Mercaderista:
- detecta productos,
- toma fotografías,
- registra vencimientos.

Vendedor:
- analiza oportunidades,
- coordina promociones,
- gestiona acciones comerciales.

Supervisor:
- valida,
- controla indicadores,
- supervisa ejecución.

Gerencia:
- analiza impacto financiero,
- revisa KPIs,
- toma decisiones estratégicas.

---

# 5.2.2 Problemas Detectados

## Operativos

- Información dispersa.
- Validaciones manuales.
- Duplicidad.
- Retrasos.
- Dependencia humana.

## Cognitivos

- Estrés.
- Incertidumbre.
- Sobrecarga mental.
- Baja confianza en información.

## Estratégicos

- Falta de KPIs.
- Baja visibilidad.
- Decisiones tardías.
- Imposibilidad de medir impacto financiero.

Las entrevistas muestran que la incertidumbre y desorganización afectan directamente productividad y eficiencia. fileciteturn2file1L70-L130 fileciteturn2file2L1-L150 fileciteturn2file3L1-L130

---

# 5.2.3 Circuit Breaker

# Definición

Circuit Breaker es un patrón de resiliencia que evita llamadas repetidas hacia servicios fallidos.

Su objetivo es:

- prevenir cascadas de errores,
- estabilizar el sistema,
- proteger recursos,
- mejorar tolerancia a fallos.

---

# Estados del patrón

| Estado | Descripción |
|---|---|
| Closed | Operación normal |
| Open | Servicio bloqueado |
| Half‑Open | Validación de recuperación |

---

# 5.2.4 Aplicabilidad al Proyecto

## Casos futuros

| Servicio | Riesgo |
|---|---|
| Multimedia | Alto |
| Alertas | Medio |
| APIs externas | Alto |
| Analytics | Medio |
| Sincronización móvil | Alto |

---

# Escenario Aplicado

Si falla el servicio multimedia:

- el mercaderista debe seguir registrando información,
- el vendedor debe continuar operando,
- la aplicación no debe colapsar completamente.

Circuit Breaker permitiría:

- degradación controlada,
- continuidad operativa,
- resiliencia móvil,
- reducción de fallos en cascada.

---

# 5.2.5 Decisión

✅ Sí aplicar Circuit Breaker en evolución futura.

---

# 5.2.6 Referencias Aplicadas

- §22 — Reliability Patterns
- §23 — Service Discovery and Resilience

---

# 5.2.7 Aplicabilidad Real

Será especialmente útil cuando existan:

- sincronización offline,
- dashboards desacoplados,
- procesamiento multimedia independiente,
- APIs externas,
- notificaciones en tiempo real.

---

# 5.3 Development View

# 5.3.1 Estado Actual del Proyecto

Actualmente el proyecto se encuentra en:

- UX Research,
- arquitectura conceptual,
- diseño estructural,
- wireframes,
- validación funcional.

No existe aún:

- observabilidad distribuida,
- Kubernetes,
- CI/CD avanzado,
- monitoreo distribuido,
- service mesh.

---

# 5.3.2 Riesgos de Microservicios Prematuros

| Riesgo | Impacto |
|---|---|
| Sobrecosto DevOps | Alto |
| Complejidad técnica | Alta |
| Mayor debugging | Alto |
| Latencia distribuida | Media |
| Tiempo de desarrollo | Alto |

---

# 5.3.3 Decisión Arquitectónica

❌ No implementar microservicios completos en MVP.

---

# 5.3.4 Arquitectura Recomendada

✅ Monolito Modular Evolutivo

Con:

- Clean Architecture,
- arquitectura hexagonal,
- modularización fuerte,
- separación por dominios,
- APIs desacopladas.

---

# 5.3.5 Justificación

Actualmente el principal riesgo NO es escalabilidad.

El principal riesgo es:

❗ construir complejidad antes de validar el producto.

El enfoque modular permitirá:

- iterar rápidamente,
- reducir costos,
- preparar futura migración,
- mantener flexibilidad.

---

# 5.3.6 Referencias

- Capítulo 1 — Microservices Patterns
- §3.5

---

# 5.4 Physical View

# 5.4.1 Consistent Hashing

# Definición

Consistent Hashing es una técnica de distribución utilizada en:

- cache distribuido,
- balanceo,
- almacenamiento distribuido,
- sistemas escalables.

Reduce redistribuciones cuando cambian nodos.

---

# 5.4.2 Aplicabilidad Futura

| Escenario | Aplicabilidad |
|---|---|
| Cache distribuido | Alta |
| Multimedia | Alta |
| Dashboards | Media |
| Multiempresa | Alta |
| Multi‑región | Media |

---

# 5.4.3 Escenario Evolutivo

Si el sistema escala nacionalmente:

- múltiples regiones,
- múltiples distribuidoras,
- alta concurrencia,
- dashboards simultáneos,
- procesamiento multimedia masivo,

consistent hashing permitiría:

- balanceo eficiente,
- mejor distribución,
- cache optimizado,
- reducción de redistribución.

---

# 5.4.4 Decisión

⚠️ No prioritario actualmente.

✅ Relevante en crecimiento futuro.

---

# 5.4.5 Referencias

- §9 — Data Management Patterns

---

# 5.4.6 Aplicabilidad Real

Especialmente útil si el producto evoluciona hacia:

- cloud distribuido,
- procesamiento multimedia desacoplado,
- analytics independiente,
- almacenamiento distribuido.

---

# 5.5 Scenarios View

# 5.5.1 Escenario Operativo

Mercaderista:
- registra producto,
- fotografía,
- cantidad,
- precio.

Vendedor:
- define promoción,
- coordina acciones.

Supervisor:
- valida ejecución.

Gerencia:
- monitorea KPIs.

---

# 5.5.2 Riesgos Detectados

- Fallas de sincronización.
- Saturación multimedia.
- Retrasos humanos.
- Conectividad limitada.
- Duplicación de información.

---

# 5.5.3 Soluciones Arquitectónicas Futuras

| Problema | Solución |
|---|---|
| Fallas parciales | Circuit Breaker |
| Escalabilidad | Microservicios |
| Balanceo | Consistent Hashing |
| Sincronización | Event‑Driven |
| Alta concurrencia | Cache distribuido |

---

# 5.5.4 Escenario Estratégico

Gerencia requiere:

- KPIs,
- métricas financieras,
- rotación,
- comparativos regionales,
- alertas tempranas,
- impacto de promociones. fileciteturn2file1L80-L130

---

# 5.5.5 Evolución Recomendada

| Etapa | Arquitectura |
|---|---|
| MVP | Monolito Modular |
| Validación operativa | Modularización avanzada |
| Escalamiento regional | Servicios desacoplados |
| Multiempresa | Microservicios híbridos |
| Escala nacional | Arquitectura distribuida |

---

# 6. Conclusiones Generales

El análisis demuestra que App Detección Prod posee características compatibles con una evolución futura hacia microservicios debido a:

- múltiples dominios funcionales,
- crecimiento potencial,
- necesidad futura de resiliencia,
- procesamiento distribuido,
- sincronización móvil,
- analítica estratégica.

Sin embargo:

implementar microservicios desde el inicio sería prematuro.

La mejor estrategia arquitectónica es:

✅ Monolito Modular Evolutivo

porque:

- reduce complejidad,
- facilita validación,
- acelera iteración,
- disminuye costos,
- prepara crecimiento futuro.

Además:

- Circuit Breaker será clave para resiliencia.
- Consistent Hashing será importante para escalabilidad futura.
- Event‑Driven será relevante para sincronización operacional.

Finalmente, el análisis demuestra que:

la arquitectura moderna debe responder no solo a problemas tecnológicos, sino también a problemas humanos, operativos y cognitivos detectados durante UX Research.

---

# Bibliografía

- Richardson, Chris.
  Microservices Patterns.

---

# Referencias Aplicadas

- §3.5 — Decomposition by Business Capability
- §3.5.1 — Decomposition by Subdomain
- §9 — Data Management Patterns
- §22 — Reliability Patterns
- §23 — Service Discovery and Resilience

---

# Evidencia de Investigación Aplicada

- Documento base del proyecto fileciteturn2file0L1-L220
- Entrevista Gerencia fileciteturn2file1L1-L130
- Entrevista Supervisor fileciteturn2file2L1-L150
- Entrevista Vendedor fileciteturn2file3L1-L130
