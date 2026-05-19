# Entregable técnico: Saga Pattern, Outbox Pattern, CQRS y flujos asíncronos candidatos

**Proyecto:** App Detección Prod  
**Contexto:** Gestión de productos próximos a vencer en canal retail  
**Enfoque:** Arquitectura de software, microservicios, comunicación asíncrona, trazabilidad y consistencia eventual  
**Autor:** Gina Fabiana Villanueva Viscarra  
**Fecha:** 19 de mayo de 2026

---

## 1. Resumen ejecutivo

App Detección Prod busca transformar un proceso actualmente informal, fragmentado y reactivo —basado en WhatsApp, fotografías no estandarizadas, Excel y comunicación verbal— en una plataforma digital trazable, medible y orientada a decisiones comerciales. El problema principal del producto no es solo registrar productos próximos a vencer, sino asegurar que la información fluya correctamente entre mercaderistas, vendedores, supervisores y gerencia.

En este contexto, **Saga Pattern**, **Outbox Pattern** y **CQRS** son patrones especialmente relevantes porque permiten diseñar una arquitectura capaz de manejar:

- procesos de negocio con varios pasos;
- operaciones distribuidas entre módulos o microservicios;
- eventos confiables;
- comunicación asíncrona;
- dashboards y reportes rápidos;
- trazabilidad completa de acciones comerciales;
- consistencia eventual sin depender de transacciones distribuidas rígidas.

El análisis concluye que App Detección Prod tiene múltiples flujos candidatos a comunicación asíncrona, especialmente en registro de detecciones, generación de alertas, aprobación de acciones comerciales, actualización de dashboards, cálculo de impacto financiero, seguimiento de vencimientos y sincronización móvil cuando exista conectividad variable.

---

## 2. Problema arquitectónico del producto

El proyecto parte de una necesidad clara: centralizar el registro de productos próximos a vencer, integrar acciones comerciales, controlar precios, registrar cantidades intervenidas, generar indicadores estratégicos y reducir la merma.

Actualmente, el proceso presenta los siguientes dolores:

- reportes enviados por WhatsApp o Excel;
- fotos sin identificación clara;
- información duplicada o incompleta;
- ausencia de trazabilidad;
- dificultad para saber si un producto ya fue gestionado;
- demoras en validación del supervisor;
- decisiones comerciales tomadas con incertidumbre;
- imposibilidad de medir impacto financiero de descuentos, bandeos, promociones, cambios o devoluciones.

Desde arquitectura, esto implica que el sistema no debe limitarse a ser una aplicación CRUD. Debe comportarse como una plataforma de eventos operativos y comerciales, donde cada acción relevante deje evidencia, dispare procesos posteriores y alimente métricas para la toma de decisiones.

---

## 3. Investigación técnica de patrones

### 3.1 Saga Pattern

#### Definición

**Saga Pattern** es un patrón de gestión de fallos y consistencia en sistemas distribuidos. Permite coordinar una operación de negocio compuesta por varios pasos ejecutados en distintos servicios. Cada paso tiene su propia transacción local y, si algo falla, se ejecutan acciones compensatorias para dejar el proceso en un estado controlado.

En lugar de usar una gran transacción distribuida, la Saga divide el proceso en transacciones pequeñas y coordinadas.

#### Problema que resuelve

En microservicios, cada servicio suele tener su propia base de datos. Por eso, una operación de negocio como “gestionar un producto próximo a vencer” puede involucrar varios servicios:

1. registrar detección;
2. validar producto;
3. actualizar estado;
4. registrar acción comercial;
5. notificar supervisor;
6. calcular impacto financiero;
7. actualizar dashboard.

Si uno de esos pasos falla, no se puede depender de una transacción única tradicional. Saga permite manejar ese flujo con consistencia eventual y compensaciones.

#### Tipos de Saga

##### a) Saga por coreografía

Cada servicio reacciona a eventos emitidos por otros servicios. No existe un coordinador central.

Ejemplo:

```text
ProductoDetectado
   → Servicio Comercial escucha y evalúa acción
   → Servicio de Alertas escucha y notifica supervisor
   → Servicio de Analytics escucha y actualiza métricas
```

Ventajas:

- bajo acoplamiento;
- buena escalabilidad;
- natural para arquitectura orientada a eventos.

Riesgos:

- flujo difícil de visualizar;
- debugging más complejo;
- riesgo de reglas distribuidas en muchos servicios.

##### b) Saga por orquestación

Existe un componente coordinador, llamado orquestador, que indica qué paso sigue.

Ejemplo:

```text
OrquestadorGestionVencimiento
   1. registrar detección
   2. solicitar validación
   3. aprobar acción comercial
   4. actualizar estado
   5. publicar alerta
   6. actualizar métricas
```

Ventajas:

- mayor control del flujo;
- mejor trazabilidad;
- más fácil para procesos críticos.

Riesgos:

- el orquestador puede concentrar lógica;
- requiere diseño cuidadoso para no convertirse en un “super servicio”.

#### Aplicación a App Detección Prod

Saga es útil para procesos de negocio donde hay más de un actor y más de un paso, especialmente cuando una acción no puede considerarse final hasta que otras tareas hayan ocurrido.

Ejemplo candidato: **gestión completa de un producto próximo a vencer**.

```text
1. Mercaderista registra producto próximo a vencer.
2. Sistema valida datos mínimos.
3. Se crea caso de vencimiento.
4. Se notifica al supervisor.
5. Supervisor valida o rechaza.
6. Vendedor define acción comercial.
7. Se registra descuento, bandeo, retiro o promoción.
8. Se actualiza estado del caso.
9. Se recalcula impacto financiero.
10. Gerencia visualiza métricas actualizadas.
```

Si falla la aplicación del descuento, por ejemplo, el sistema podría:

- dejar el caso en estado “acción pendiente”;
- emitir alerta de excepción;
- evitar marcar el producto como gestionado;
- mantener evidencia para auditoría;
- reintentar el paso fallido.

No siempre conviene “deshacer” todo. En App Detección Prod muchas compensaciones serían lógicas, no físicas. Por ejemplo: cambiar un estado, registrar una incidencia o solicitar intervención manual.

---

### 3.2 Outbox Pattern

#### Definición

**Transactional Outbox Pattern** es un patrón que garantiza que un cambio en la base de datos y la publicación de un evento ocurran de forma confiable. La idea es guardar el evento en una tabla o colección “outbox” dentro de la misma transacción local que modifica el dato principal. Luego, un proceso separado publica esos eventos hacia un broker o sistema de mensajería.

#### Problema que resuelve

Sin Outbox puede ocurrir este problema:

```text
1. Se registra producto próximo a vencer en la base de datos.
2. El sistema intenta publicar el evento ProductoDetectado.
3. El broker de mensajes falla.
4. El evento se pierde.
5. Supervisor y dashboard nunca se enteran.
```

Esto sería crítico para App Detección Prod porque repetiría el problema actual: información registrada, pero no visible para quien debe tomar decisiones.

Con Outbox:

```text
1. Se registra producto próximo a vencer.
2. En la misma transacción se guarda un evento en outbox_events.
3. Un publicador lee eventos pendientes.
4. El evento se envía al broker.
5. Si falla, queda pendiente y se reintenta.
```

#### Estructura conceptual de una tabla Outbox

```text
outbox_events
- id
- aggregate_id
- aggregate_type
- event_type
- payload
- status
- created_at
- published_at
- retry_count
- error_message
```

#### Aplicación a App Detección Prod

Cada acción crítica debe generar un evento confiable:

- ProductoDetectado;
- FotoAdjuntada;
- DeteccionValidada;
- DeteccionRechazada;
- AccionComercialPropuesta;
- AccionComercialAprobada;
- DescuentoAplicado;
- ProductoRetirado;
- PrecioModificado;
- AlertaVencimientoGenerada;
- ImpactoFinancieroCalculado;
- DashboardActualizado.

Outbox es altamente recomendable porque el producto depende de trazabilidad. El objetivo del sistema no es solo guardar datos, sino asegurar que esos datos generen visibilidad operativa y estratégica.

---

### 3.3 CQRS

#### Definición

**CQRS** significa **Command Query Responsibility Segregation**. El patrón separa las operaciones de escritura, llamadas comandos, de las operaciones de lectura, llamadas consultas.

- **Command:** modifica el estado del sistema.
- **Query:** consulta información sin modificarla.

#### Problema que resuelve

En App Detección Prod existen dos necesidades muy diferentes:

##### Necesidad operativa

Mercaderistas, vendedores y supervisores necesitan registrar o actualizar información:

- registrar detección;
- subir evidencia;
- aprobar o rechazar caso;
- asignar acción comercial;
- modificar precio;
- cerrar caso.

Estas acciones requieren validaciones, reglas de negocio y trazabilidad.

##### Necesidad analítica

Gerencia y supervisores necesitan leer información consolidada:

- productos próximos a vencer por tienda;
- casos críticos por fecha;
- productos con mayor riesgo de merma;
- impacto de descuentos;
- costos de devolución;
- cumplimiento por mercaderista;
- efectividad de acciones comerciales;
- comparativos por región, sala o categoría.

Estas consultas requieren rapidez, agregaciones y modelos optimizados para dashboard.

CQRS permite separar ambos mundos.

#### Modelo propuesto

```text
Command Side
- Registrar detección
- Validar caso
- Aprobar acción comercial
- Aplicar descuento
- Cerrar caso

Write Database
- Modelo transaccional normalizado
- Reglas de negocio
- Estados oficiales
- Auditoría

Eventos
- ProductoDetectado
- AccionAprobada
- CasoCerrado

Read Side
- Proyecciones
- Dashboard
- KPIs
- Reportes
- Vistas por rol
```

#### Aplicación a App Detección Prod

CQRS es especialmente útil porque la aplicación tendrá usuarios con necesidades muy distintas:

| Rol | Principal necesidad | Tipo de carga |
|---|---|---|
| Mercaderista | registrar rápido en campo | escritura |
| Vendedor | revisar productos y acciones | lectura + escritura |
| Supervisor | validar, priorizar, controlar | lectura + escritura |
| Gerente | analizar KPIs e impacto financiero | lectura intensiva |

La lectura gerencial no debería afectar el rendimiento del registro operativo en campo. Separar lectura y escritura ayuda a que el sistema escale mejor y mantenga una experiencia rápida para cada rol.

---

## 4. Relación entre Saga, Outbox y CQRS

Estos patrones se complementan.

```text
CQRS separa escritura y lectura.
Outbox asegura que los eventos de escritura no se pierdan.
Saga coordina procesos de negocio distribuidos cuando hay múltiples pasos y servicios.
```

Flujo integrado:

```text
1. Usuario ejecuta comando: RegistrarProductoProximoAVencer.
2. Command Side valida y guarda en Write DB.
3. En la misma transacción se guarda evento en Outbox.
4. Publicador envía ProductoDetectado al broker.
5. Servicios consumidores actualizan proyecciones, alertas y métricas.
6. Si el proceso requiere varios pasos, una Saga coordina la secuencia.
7. Read Side expone dashboards y reportes por rol.
```

---

## 5. Criterios para identificar flujos asíncronos candidatos

No todo debe ser asíncrono. En App Detección Prod, un flujo es candidato a asincronía cuando cumple uno o más de estos criterios:

1. No requiere respuesta inmediata para completar la pantalla del usuario.
2. Involucra notificaciones a otros roles.
3. Alimenta dashboards o métricas.
4. Puede ejecutarse en segundo plano.
5. Puede fallar y reintentarse sin bloquear al usuario.
6. Implica integración con servicios externos.
7. Depende de conectividad móvil variable.
8. Genera eventos relevantes para auditoría.
9. Forma parte de un proceso de negocio de varios pasos.
10. Requiere procesamiento pesado, como cálculo de impacto financiero o consolidación de indicadores.

---

## 6. Flujos asíncronos candidatos del producto

### 6.1 Registro de producto próximo a vencer

**Descripción:** El mercaderista registra producto, fecha de vencimiento, cantidad, sala, precio actual, evidencia fotográfica y observaciones.

**Evento principal:** ProductoDetectado

**Candidato a asincronía:** Sí.

**Motivo:** El registro debe ser rápido para el mercaderista. La notificación, actualización de dashboard y cálculo de criticidad pueden ejecutarse en segundo plano.

**Patrones recomendados:** Outbox + CQRS.

**Flujo:**

```text
Command: RegistrarProductoProximoAVencer
→ guardar detección
→ guardar evento en outbox
→ publicar ProductoDetectado
→ actualizar bandeja supervisor
→ actualizar dashboard operativo
```

---

### 6.2 Carga y procesamiento de fotografía

**Descripción:** El usuario adjunta fotografía como evidencia del producto.

**Evento principal:** FotoAdjuntada

**Candidato a asincronía:** Sí.

**Motivo:** La foto puede requerir compresión, almacenamiento, validación de formato o futura extracción de datos mediante IA/OCR. No debe bloquear el registro completo.

**Patrones recomendados:** Outbox + procesamiento asíncrono.

**Flujo:**

```text
Foto cargada
→ guardar referencia
→ evento FotoAdjuntada
→ optimizar imagen
→ asociar evidencia al caso
→ marcar evidencia procesada
```

---

### 6.3 Generación de alerta al supervisor

**Descripción:** Al detectar un producto crítico, el supervisor debe recibir alerta.

**Evento principal:** AlertaSupervisorGenerada

**Candidato a asincronía:** Sí.

**Motivo:** La alerta es importante, pero no debe bloquear el registro del mercaderista. Debe admitir reintentos.

**Patrones recomendados:** Outbox.

**Flujo:**

```text
ProductoDetectado
→ evaluar criticidad
→ crear alerta
→ enviar push/email/in-app
→ registrar entrega o fallo
```

---

### 6.4 Validación de detección por supervisor

**Descripción:** El supervisor revisa si la información registrada es correcta.

**Evento principal:** DeteccionValidada o DeteccionRechazada

**Candidato a asincronía:** Parcialmente.

**Motivo:** La acción del supervisor debe confirmarse de forma inmediata en su pantalla, pero los efectos posteriores pueden ser asíncronos.

**Patrones recomendados:** CQRS + Outbox.

**Flujo:**

```text
Command: ValidarDeteccion
→ actualizar estado del caso
→ guardar evento outbox
→ notificar vendedor
→ actualizar KPIs de calidad de reporte
```

---

### 6.5 Propuesta de acción comercial

**Descripción:** Vendedor o supervisor propone descuento, bandeo, promoción, retiro o cambio.

**Evento principal:** AccionComercialPropuesta

**Candidato a asincronía:** Sí.

**Motivo:** La propuesta puede iniciar un flujo de aprobación, notificación y seguimiento.

**Patrones recomendados:** Saga + Outbox.

**Flujo:**

```text
AccionComercialPropuesta
→ validar reglas comerciales
→ solicitar aprobación si corresponde
→ notificar responsable
→ dejar estado pendiente
```

---

### 6.6 Aprobación de acción comercial

**Descripción:** El supervisor o gerente aprueba una acción comercial.

**Evento principal:** AccionComercialAprobada

**Candidato a asincronía:** Sí, en los efectos posteriores.

**Motivo:** La aprobación cambia el estado del caso, pero la notificación, actualización de métricas y seguimiento pueden ejecutarse en segundo plano.

**Patrones recomendados:** Saga + Outbox + CQRS.

**Flujo:**

```text
Command: AprobarAccionComercial
→ actualizar acción como aprobada
→ publicar AccionComercialAprobada
→ notificar vendedor/mercaderista
→ actualizar dashboard
→ programar seguimiento
```

---

### 6.7 Aplicación de descuento o cambio de precio

**Descripción:** Se registra precio anterior, nuevo precio, porcentaje de descuento y fecha de vigencia.

**Evento principal:** PrecioModificado o DescuentoAplicado

**Candidato a asincronía:** Sí, si se integra con sistemas externos o requiere aprobación.

**Motivo:** Puede formar parte de una Saga si involucra validación, autorización, actualización de estado y medición de impacto.

**Patrones recomendados:** Saga + Outbox.

**Compensación posible:** Si el descuento no se aplica correctamente, el caso queda como “acción fallida” o “pendiente de corrección”, no como gestionado.

---

### 6.8 Registro de bandeo, promoción o exhibición especial

**Descripción:** Acción comercial física aplicada en sala.

**Evento principal:** BandeoRegistrado o PromocionActivada

**Candidato a asincronía:** Sí.

**Motivo:** Alimenta reportes, seguimiento y evaluación posterior.

**Patrones recomendados:** Outbox + CQRS.

---

### 6.9 Retiro de producto de sala

**Descripción:** Producto retirado por riesgo de vencimiento, política comercial o baja rotación.

**Evento principal:** ProductoRetirado

**Candidato a asincronía:** Sí.

**Motivo:** Puede requerir actualización de inventario, cálculo de pérdida, evidencia y reporte gerencial.

**Patrones recomendados:** Saga + Outbox.

**Flujo:**

```text
ProductoRetirado
→ actualizar estado caso
→ registrar cantidad retirada
→ calcular pérdida estimada
→ actualizar dashboard financiero
→ notificar gerencia si supera umbral
```

---

### 6.10 Cálculo de impacto financiero

**Descripción:** Cálculo del efecto económico de descuentos, devoluciones, cambios, reposición, distribución y merma evitada.

**Evento principal:** ImpactoFinancieroCalculado

**Candidato a asincronía:** Sí.

**Motivo:** Es procesamiento analítico. No debe bloquear operaciones de campo.

**Patrones recomendados:** CQRS + eventos.

**Flujo:**

```text
AccionComercialAplicada
→ calcular costo/descuento/merma evitada
→ actualizar proyección financiera
→ refrescar dashboard gerencial
```

---

### 6.11 Actualización de dashboards por rol

**Descripción:** Proyecciones para supervisor, vendedor y gerencia.

**Evento principal:** DashboardProjectionUpdated

**Candidato a asincronía:** Sí.

**Motivo:** Los dashboards deben ser rápidos y no depender de consultas complejas sobre la base transaccional.

**Patrones recomendados:** CQRS.

**Proyecciones candidatas:**

- productos críticos por tienda;
- productos próximos a vencer por categoría;
- acciones pendientes;
- acciones aprobadas;
- merma estimada;
- merma evitada;
- cumplimiento por mercaderista;
- tiempos de respuesta del supervisor;
- productos con reincidencia;
- ranking de salas con más riesgo.

---

### 6.12 Notificaciones automáticas por vencimiento cercano

**Descripción:** El sistema genera alertas cuando un producto está cerca de una fecha crítica.

**Evento principal:** VencimientoCriticoDetectado

**Candidato a asincronía:** Sí.

**Motivo:** Puede ejecutarse mediante jobs programados y reglas de negocio.

**Patrones recomendados:** eventos + Outbox.

**Flujo:**

```text
Job diario revisa productos activos
→ detecta vencimientos críticos
→ genera alerta
→ notifica responsables
→ actualiza prioridad del caso
```

---

### 6.13 Escalamiento por falta de atención

**Descripción:** Si un caso no es validado o gestionado dentro de cierto tiempo, se escala.

**Evento principal:** CasoEscalado

**Candidato a asincronía:** Sí.

**Motivo:** Se ejecuta en segundo plano según reglas SLA.

**Patrones recomendados:** Saga / proceso orquestado.

**Flujo:**

```text
Caso pendiente > SLA
→ generar evento CasoEscalado
→ notificar supervisor superior o gerencia
→ marcar prioridad alta
```

---

### 6.14 Sincronización offline móvil

**Descripción:** El mercaderista puede registrar datos con conectividad limitada y sincronizarlos después.

**Evento principal:** RegistroMovilSincronizado

**Candidato a asincronía:** Sí, crítico.

**Motivo:** El trabajo en campo puede tener conectividad variable. El sistema debe soportar cola local y sincronización posterior.

**Patrones recomendados:** Outbox local + Outbox servidor + resolución de conflictos.

**Flujo:**

```text
App móvil guarda registro local
→ cola local pendiente
→ recupera conexión
→ sincroniza comando
→ servidor valida
→ publica eventos
→ actualiza estado local
```

---

### 6.15 Auditoría de acciones

**Descripción:** Registro histórico de quién hizo qué, cuándo, desde dónde y con qué evidencia.

**Evento principal:** AuditLogCreated

**Candidato a asincronía:** Sí.

**Motivo:** La auditoría puede procesarse en segundo plano, siempre que no se pierda.

**Patrones recomendados:** Outbox.

---

### 6.16 Consolidación de reportes gerenciales

**Descripción:** Reportes diarios/semanales/mensuales para gerencia.

**Evento principal:** ReporteGerencialGenerado

**Candidato a asincronía:** Sí.

**Motivo:** Es procesamiento batch o programado.

**Patrones recomendados:** CQRS + jobs asíncronos.

---

### 6.17 Comparación de rotación por producto o sala

**Descripción:** Comparativos entre productos, tiendas, regiones o acciones comerciales.

**Evento principal:** IndicadorRotacionActualizado

**Candidato a asincronía:** Sí.

**Motivo:** Requiere agregación y cálculo analítico.

**Patrones recomendados:** CQRS.

---

### 6.18 Cierre de caso de vencimiento

**Descripción:** El caso se cierra cuando se confirma venta, retiro, devolución, cambio o acción aplicada.

**Evento principal:** CasoCerrado

**Candidato a asincronía:** Parcialmente.

**Motivo:** El cierre debe actualizar estado inmediatamente, pero los efectos analíticos pueden ser asíncronos.

**Patrones recomendados:** Saga + Outbox + CQRS.

---

## 7. Matriz de flujos asíncronos candidatos

| Nº | Flujo | Evento principal | Asíncrono | Patrón recomendado | Prioridad |
|---:|---|---|---|---|---|
| 1 | Registro de producto próximo a vencer | ProductoDetectado | Sí | Outbox + CQRS | Alta |
| 2 | Procesamiento de fotografía | FotoAdjuntada | Sí | Outbox | Media |
| 3 | Alerta al supervisor | AlertaSupervisorGenerada | Sí | Outbox | Alta |
| 4 | Validación de detección | DeteccionValidada | Parcial | CQRS + Outbox | Alta |
| 5 | Propuesta de acción comercial | AccionComercialPropuesta | Sí | Saga + Outbox | Alta |
| 6 | Aprobación de acción comercial | AccionComercialAprobada | Sí | Saga + Outbox + CQRS | Alta |
| 7 | Aplicación de descuento | DescuentoAplicado | Sí | Saga + Outbox | Alta |
| 8 | Bandeo/promoción | PromocionActivada | Sí | Outbox + CQRS | Media |
| 9 | Retiro de producto | ProductoRetirado | Sí | Saga + Outbox | Alta |
| 10 | Cálculo de impacto financiero | ImpactoFinancieroCalculado | Sí | CQRS | Alta |
| 11 | Actualización de dashboards | DashboardProjectionUpdated | Sí | CQRS | Alta |
| 12 | Alertas por vencimiento cercano | VencimientoCriticoDetectado | Sí | Outbox + Jobs | Alta |
| 13 | Escalamiento por SLA | CasoEscalado | Sí | Saga / Orquestación | Media-Alta |
| 14 | Sincronización offline móvil | RegistroMovilSincronizado | Sí | Outbox local + servidor | Alta |
| 15 | Auditoría de acciones | AuditLogCreated | Sí | Outbox | Alta |
| 16 | Reporte gerencial | ReporteGerencialGenerado | Sí | CQRS + Batch | Media |
| 17 | Indicadores de rotación | IndicadorRotacionActualizado | Sí | CQRS | Media-Alta |
| 18 | Cierre de caso | CasoCerrado | Parcial | Saga + Outbox + CQRS | Alta |

---

## 8. Eventos de dominio propuestos

### Eventos de detección

- ProductoDetectado
- ProductoDuplicadoDetectado
- FotoAdjuntada
- EvidenciaProcesada
- DeteccionValidada
- DeteccionRechazada

### Eventos comerciales

- AccionComercialPropuesta
- AccionComercialAprobada
- AccionComercialRechazada
- DescuentoAplicado
- PrecioModificado
- BandeoRegistrado
- PromocionActivada
- ProductoRetirado

### Eventos de seguimiento

- CasoAsignado
- CasoEscalado
- CasoReabierto
- CasoCerrado
- VencimientoCriticoDetectado
- SLAIncumplido

### Eventos analíticos

- ImpactoFinancieroCalculado
- MermaEstimadaActualizada
- MermaEvitadaCalculada
- IndicadorRotacionActualizado
- DashboardProjectionUpdated
- ReporteGerencialGenerado

### Eventos técnicos

- RegistroMovilSincronizado
- PublicacionEventoFallida
- EventoReintentado
- AuditLogCreated

---

## 9. Comandos candidatos para CQRS

### Comandos operativos

- RegistrarProductoProximoAVencer
- AdjuntarFotoProducto
- EditarDeteccion
- EnviarDeteccion
- SincronizarRegistroMovil

### Comandos de supervisión

- ValidarDeteccion
- RechazarDeteccion
- SolicitarCorreccion
- EscalarCaso
- AsignarResponsable

### Comandos comerciales

- ProponerAccionComercial
- AprobarAccionComercial
- RechazarAccionComercial
- AplicarDescuento
- RegistrarBandeo
- RegistrarRetiroProducto
- ModificarPrecio

### Comandos de cierre

- CerrarCasoPorVenta
- CerrarCasoPorRetiro
- CerrarCasoPorDevolucion
- ReabrirCaso

---

## 10. Consultas candidatas para CQRS

### Consultas para mercaderista

- MisProductosReportados
- CasosPendientesDeCorreccion
- HistorialDeReportesPorRuta
- EstadoDeMisDetecciones

### Consultas para vendedor

- ProductosPendientesDeAccionComercial
- ProductosConDescuentoPendiente
- ProductosPorSalaYCliente
- HistorialDeAccionesPorProducto

### Consultas para supervisor

- CasosPendientesDeValidacion
- CasosCriticosPorFechaDeVencimiento
- CumplimientoPorMercaderista
- TiempoPromedioDeValidacion
- AlertasPorSala

### Consultas para gerencia

- DashboardImpactoFinanciero
- MermaEstimadaVsMermaEvitada
- ProductosConMayorRiesgo
- CostosPorDevolucionYCambio
- RankingDeSalasCriticas
- EfectividadDeAccionesComerciales
- RotacionPorProductoCategoriaRegion

---

## 11. Recomendación arquitectónica para el proyecto

### 11.1 Recomendación de implementación gradual

No se recomienda implementar todo como microservicios desde el inicio. Para un MVP académico y funcional, se recomienda una arquitectura modular con patrones claros, que pueda evolucionar a microservicios si el producto escala.

#### Fase 1: Modular monolith con eventos internos

- Módulo de Detecciones
- Módulo Comercial
- Módulo de Alertas
- Módulo de Reportes
- Módulo de Auditoría
- Tabla Outbox
- Proyecciones simples para dashboard

#### Fase 2: CQRS parcial

- Separar comandos críticos de consultas gerenciales.
- Crear proyecciones para dashboards.
- Actualizar reportes mediante eventos.

#### Fase 3: Procesos Saga

- Implementar Saga para gestión completa de acción comercial.
- Implementar Saga para retiro/devolución/cierre de caso.
- Agregar estados intermedios y compensaciones.

#### Fase 4: Microservicios si el volumen lo justifica

- Servicio de Detecciones
- Servicio Comercial
- Servicio de Notificaciones
- Servicio de Analytics
- Servicio de Auditoría

---

## 12. Diseño recomendado de estados del caso

```text
BORRADOR
→ REGISTRADO
→ PENDIENTE_VALIDACION
→ VALIDADO
→ ACCION_PROPUESTA
→ ACCION_APROBADA
→ EN_EJECUCION
→ GESTIONADO
→ CERRADO
```

Estados alternativos:

```text
RECHAZADO
SOLICITA_CORRECCION
ESCALADO
ACCION_FALLIDA
VENCIDO_SIN_ACCION
REABIERTO
```

Estos estados son necesarios para que Saga y CQRS funcionen correctamente. Cada transición debe emitir un evento.

---

## 13. Riesgos y controles

### Riesgo 1: Eventos duplicados

**Control:** consumidores idempotentes. Cada evento debe tener event_id único.

### Riesgo 2: Eventos fuera de orden

**Control:** versionado por aggregate_id y secuencia.

### Riesgo 3: Dashboard desactualizado

**Control:** mostrar fecha/hora de última actualización y monitorear retraso de proyecciones.

### Riesgo 4: Complejidad excesiva

**Control:** aplicar CQRS y Saga solo en flujos que lo justifiquen.

### Riesgo 5: Pérdida de eventos

**Control:** Outbox obligatorio para eventos de negocio críticos.

### Riesgo 6: Fallos en notificaciones

**Control:** reintentos, estado de entrega y fallback a bandeja interna.

---

## 14. Decisiones arquitectónicas candidatas a ADR

### ADR-001: Adoptar Outbox Pattern para eventos críticos

**Decisión:** Todo cambio relevante de negocio deberá registrar un evento en Outbox dentro de la misma transacción local.

**Justificación:** Evita pérdida de eventos y garantiza trazabilidad.

---

### ADR-002: Aplicar CQRS parcial para dashboards y reportes

**Decisión:** Separar operaciones de escritura operativa de consultas analíticas para gerencia y supervisión.

**Justificación:** Los dashboards requieren agregaciones rápidas y no deben afectar el registro de campo.

---

### ADR-003: Usar Saga orquestada para gestión completa de acción comercial

**Decisión:** Procesos como aprobación, aplicación y cierre de acciones comerciales deben coordinarse mediante una Saga orquestada.

**Justificación:** Son flujos multipaso con estados intermedios y posibles fallos.

---

### ADR-004: Diseñar eventos de dominio como contrato interno

**Decisión:** Cada transición relevante emitirá eventos con estructura estandarizada.

**Justificación:** Permite trazabilidad, auditoría, integración futura y actualización de proyecciones.

---

## 15. Conclusión

Saga Pattern, Outbox Pattern y CQRS son altamente aplicables a App Detección Prod porque el problema central del producto es la desconexión entre operación en campo, gestión comercial y visibilidad gerencial.

El producto necesita registrar datos, pero también necesita que esos datos activen procesos, alertas, aprobaciones, métricas y decisiones. Por eso, los flujos asíncronos son una parte esencial de la arquitectura.

La recomendación principal es comenzar con una arquitectura modular, incorporar Outbox desde el inicio para trazabilidad, aplicar CQRS en dashboards y reportes, y reservar Saga para los procesos realmente críticos: acción comercial, retiro/devolución y cierre de caso.

Con esta aproximación, App Detección Prod puede evolucionar desde un MVP ordenado hacia una plataforma robusta, escalable y preparada para operar con consistencia eventual, evidencia trazable y decisiones basadas en datos.

---

## 16. Fuentes consultadas

- AWS Prescriptive Guidance. “Saga pattern”. Consulta: 19 de mayo de 2026. https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-data-persistence/saga-pattern.html
- Microservices.io. “Pattern: Transactional outbox”. Consulta: 19 de mayo de 2026. https://microservices.io/patterns/data/transactional-outbox
- Microsoft Learn / Azure Architecture Center. “CQRS pattern”. Consulta: 19 de mayo de 2026. https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs
- Microsoft Learn / Azure Architecture Center. “Patrón CQRS”. Consulta: 19 de mayo de 2026. https://learn.microsoft.com/es-es/azure/architecture/patterns/cqrs
- Laigner, R., Almeida, A. C., Assunção, W. K. G., Zhou, Y. “An Empirical Study on Challenges of Event Management in Microservice Architectures”. 2024. https://arxiv.org/abs/2408.00440
