# Demo 3 - Release 8.3.0

**Proyecto:** App Deteccion de Productos Proximos a Vencer
**Responsable:** Gina Villanueva
**Fecha:** 03/11/2026
**Rama:** release/8.3.0

## 1. Objetivo

Presentar dos funcionalidades del sistema, su correspondencia con los casos de uso del FSD, el despliegue con Docker Compose y un analisis de posible extraccion de microservicio.

## 2. Funcionalidad FEAT-001 - Registro de producto

**Caso de uso:** FSD-UC-001.

El mercaderista registra tienda, producto, vencimiento, cantidad, precio actual, nuevo precio y accion comercial.

Criterios de aceptacion definidos en el FSD:
- Registrar el caso.
- Calcular dias al vencimiento.
- Calcular valor financiero en riesgo.
- Calcular descuento porcentual.
- Clasificar el riesgo.
- Mostrar el caso en la bandeja de supervision.

Referencia: docs/product/FSD-FEAT-001-002.md

**Estado de verificacion:** criterios identificados en el FSD; no se ejecutaron pruebas funcionales completas durante esta preparacion.

## 3. Funcionalidad FEAT-002 - Supervisor y dashboard

**Caso de uso:** FSD-UC-002.

El supervisor revisa un caso pendiente y lo aprueba con comentario.

Criterios de aceptacion definidos en el FSD:
- Cambiar el estado a APROBADO.
- Generar el evento CaseValidated.v1.
- Incrementar validated_cases en el dashboard.
- Mantener trazabilidad documental y tecnica.

El dashboard debe mostrar total de casos, casos validados, valor financiero en riesgo, cantidad intervenida, cambios de precio y acciones por tipo.

Referencia: docs/product/FSD-FEAT-001-002.md

**Estado de verificacion:** criterios documentados; no se afirma aprobacion de pruebas funcionales no ejecutadas.

## 4. Despliegue con Docker

Se preparo un Dockerfile multi-stage:
- builder: instalacion de dependencias Python.
- runtime: ejecucion de FastAPI mediante Uvicorn como usuario no root.

Se preparo compose.yaml con volumen de datos SQLite y healthcheck.

Comando utilizado:

    docker compose up -d --build --wait

Resultados observados:
- Imagen app-deteccion:8.3.0 construida.
- Contenedor app-deteccion-prod-m4-api-1 healthy.
- GET http://localhost:18080/health: HTTP 200.
- Respuesta: {"status":"ok","feature":"FSD-UC-001","coverage_rule":">=90%"}.

La respuesta del endpoint no constituye por si sola evidencia de cobertura de pruebas igual o superior al 90%.

La comprobacion desde un clon limpio esta pendiente de ejecucion.

## 5. Auditoria de seguridad

Hadolint v2.15.1: ejecucion sin avisos visibles.

Trivy v0.76.1 sobre app-deteccion:8.3.0:
- HIGH: 49 hallazgos.
- CRITICAL: 0 hallazgos detectados.
- Sin version corregida indicada: 45 registros.
- Con version corregida indicada: 4 registros.

Los cuatro registros con correccion corresponden a dos CVE repetidas:
- CVE-2026-23949: jaraco.context 5.3.0; correccion indicada 6.1.0.
- CVE-2026-24049: wheel 0.45.1; correccion indicada 0.46.2.

Existe una discrepancia entre los metadatos analizados por Trivy y la consulta al Python del sistema, que informo wheel 0.46.3 y no encontro jaraco.context.

Los hallazgos no se consideran resueltos. Se requiere localizar los metadatos afectados, revisar cada CVE, verificar versiones disponibles y repetir el escaneo.

Medidas ya presentes:
- Imagen base slim.
- Construccion multi-stage.
- Ejecucion como usuario sin privilegios root.

Estas medidas reducen superficie de ataque, pero no eliminan ni justifican automaticamente las vulnerabilidades HIGH.

**Estado de seguridad:** 49 hallazgos HIGH pendientes de tratamiento o justificacion individual. No se declara cumplimiento pleno de la condicion de seguridad del release.

## 6. Analisis de extraccion de microservicio - Opcion B

### Modulo candidato

Gestion de eventos de dominio, actualmente implementada mediante SQLiteEventPublisher en:

    src/app_deteccion/infrastructure/sqlite_repository.py

La implementacion utiliza la tabla outbox_events, con id, name, aggregate_id, payload y occurred_at.

Interfaz actual:
- publish_many(events): guarda eventos.
- list_all(): consulta eventos.
- clear(): elimina eventos para reiniciar la demostracion.
- GET /events: expone los eventos mediante la API actual.

La consulta documental GET /traceability se mantendria inicialmente en la aplicacion principal.

### Justificacion

La persistencia y consulta de eventos constituyen responsabilidades identificables y potencialmente separables. Una extraccion futura podria facilitar escalamiento, mantenimiento y consumidores independientes.

### Interfaz dentro del monolito

Las operaciones se realizan mediante llamadas Python a SQLiteEventPublisher, con almacenamiento local en SQLite.

### Interfaz propuesta como servicio separado

Propuesta de contrato HTTP, no implementada:
- POST /events: recibir eventos identificados con ID, nombre, agregado y payload.
- GET /events: consultar eventos registrados.
- GET /health: comprobar disponibilidad del servicio.

La aplicacion principal llamaria a un cliente adaptador para publicar eventos. Se conservaria una interfaz de aplicacion independiente del mecanismo de transporte.

### Riesgos y consideraciones

- Latencia adicional por comunicaciones HTTP.
- Fallos de red y necesidad de reintentos.
- Eventos duplicados: se requiere idempotencia por ID.
- Consistencia entre escritura del caso y publicacion del evento.
- SQLite no debe compartirse como archivo entre servicios remotos.
- Necesidad de autenticacion, observabilidad y gestion de errores.

Se recomienda evaluar un outbox transaccional con publicacion asincrona antes de separar el servicio.

**Decision:** la extraccion se propone para una iteracion futura. No fue implementada ni medida en esta Demo 3.

## 7. Evidencias y limitaciones

Evidencias obtenidas durante la preparacion:
1. Construccion correcta de Docker multi-stage.
2. Docker Compose con contenedor healthy.
3. HTTP 200 en /health.
4. Hadolint sin avisos.
5. Resultado Trivy: 49 HIGH, 0 CRITICAL.
6. Identificacion de SQLiteEventPublisher y sus interfaces.

Pendiente:
- Pruebas funcionales completas de los escenarios Gherkin.
- Tratamiento o justificacion individual de vulnerabilidades HIGH.
- Verificacion de despliegue desde clon limpio.
- Confirmacion de publicacion del release.

## 8. Conclusion

El despliegue local de la API mediante Docker Compose se verifico satisfactoriamente. Se identificaron dos funcionalidades trazables al FSD y se documento una propuesta de separacion del modulo de eventos. La aceptacion funcional completa y el cierre de seguridad permanecen pendientes de verificacion.

## 9. Verificacion desde clon limpio - 04/11/2026

Se realizo una nueva descarga del repositorio desde GitHub utilizando la etiqueta 8.3.0.

Comando de clonacion:

    git clone --depth 1 --branch 8.3.0 --single-branch https://github.com/ginavillanueva/App-Deteccion-Prod-M4.git App-Deteccion-Demo3-Limpio

Commit verificado: 4dac875.

Desde la carpeta clonada se ejecuto:

    docker compose up -d --build --wait

Resultados observados:
- Imagen app-deteccion:8.3.0 construida correctamente.
- Contenedor app-deteccion-demo3-limpio-api-1 en estado healthy.
- GET http://localhost:18080/health: HTTP 200 OK.
- Respuesta JSON: {"status":"ok","feature":"FSD-UC-001","coverage_rule":">=90%"}.

Conclusion: se verifico el arranque y la respuesta HTTP desde un clon limpio del release publicado. Docker reutilizo capas en cache, por lo que esta prueba no equivale a una compilacion sin cache.

Esta verificacion no resuelve los 49 hallazgos HIGH de Trivy ni sustituye las pruebas funcionales completas.

## 10. Evidencia funcional de FEAT-001 y FEAT-002 - 04/11/2026

Se ejecuto una prueba funcional mediante la API del stack Docker.

### FEAT-001 - Registro de producto

Caso de prueba:
- Producto: Yogur Natural 1L.
- Tienda: Sucursal Demo.
- Lote: LOTE-DEMO-001.
- Vencimiento: 08/11/2026.
- Cantidad: 20 unidades.
- Precio actual: 15.
- Nuevo precio: 12.
- Accion comercial: DESCUENTO.

Resultados observados:
- Registro exitoso.
- Dias al vencimiento: 4.
- Valor financiero en riesgo: 300.
- Descuento: 20 %.
- Clasificacion de riesgo: MEDIO, score 35.
- Estado inicial: REGISTRADO.
- Eventos generados: ProductCaseRegistered.v1, PriceChanged.v1 y CaseRiskClassified.v1.

### FEAT-002 - Validacion del supervisor

Se aprobo el caso utilizando PATCH /cases/{case_id}/validate.

Resultados observados:
- Decision: APROBADO.
- Estado interno: VALIDADO_SUPERVISOR.
- Supervisor: supervisor.demo.
- Comentario de aprobacion almacenado.
- Evento generado: CaseValidatedBySupervisor.v1.

### Dashboard y persistencia

Resultados confirmados mediante GET /dashboard, GET /events y GET /cases/{case_id}:
- total_cases: 1.
- validated_cases: 1.
- total_financial_value_at_risk: 300.
- total_intervened_quantity: 20.
- price_change_cases: 1.
- domain_events_count: 4.
- Caso recuperado correctamente con su estado y decision del supervisor.

### Diferencias encontradas respecto al FSD

1. El FSD menciona el estado APROBADO; la implementacion utiliza VALIDADO_SUPERVISOR y conserva APROBADO en supervisor_decision.
2. El FSD menciona CaseValidated.v1; la implementacion genera CaseValidatedBySupervisor.v1.

Estas diferencias requieren alineacion del contrato funcional o una decision de diseno documentada.

### Alcance de la prueba

Se comprobo un flujo funcional de registro, aprobacion, consulta de eventos y dashboard.
No se afirma cobertura completa de todos los escenarios Gherkin ni de casos negativos.
Los hallazgos HIGH de Trivy siguen pendientes de tratamiento.

## 11. Mejora de seguridad del Dockerfile - 04/11/2026

Se actualizaron y fijaron versiones de dependencias Python en las
etapas builder y runtime del Dockerfile multi-stage.

Versiones utilizadas:
- setuptools==84.2.1
- wheel==0.48.0

Se identificaron dependencias vulnerables incorporadas en setuptools/_vendor.
La actualizacion elimino las detecciones HIGH de Python.

### Comparacion de Trivy

| Categoria | Antes | Despues |
|---|---:|---:|
| Python HIGH | 4 | 0 |
| Debian HIGH | 45 | 45 |
| Total HIGH | 49 | 45 |
| Total CRITICAL | 0 | 0 |

Herramienta: Trivy v0.76.1.

### Validaciones posteriores

- Construccion Docker sin cache: exitosa.
- Contenedor Docker Compose: healthy.
- GET /health: HTTP 200 OK.
- Hadolint v2.15.1: sin advertencias.

### Riesgos pendientes

Permanecen 45 hallazgos HIGH asociados a Debian 13.7.
No se consideran corregidos ni justificados individualmente.
Se requiere revisar sus identificadores CVE, exposicion real,
medidas de mitigacion y actualizaciones disponibles.

La mejora documentada corresponde a la rama release/8.3.0
posterior a la publicacion inicial del tag 8.3.0.

## Validacion final FSD - 04/11/2026

Se corrigio la implementacion de aprobacion del supervisor
para alinearla con los criterios de aceptacion del FSD.

### Correcciones

- Estado de aprobacion: APROBADO.
- Evento generado: CaseValidated.v1.
- Campo del evento: supervisor_user.

### Prueba funcional real

Se registro un caso mediante POST /cases y se aprobo
mediante PATCH /cases/{id}/validate.

Resultados:
- Estado final: APROBADO.
- Decision del supervisor: APROBADO.
- Evento CaseValidated.v1: verificado.
- Supervisor: supervisor.demo.
- Dashboard validated_cases: 1.
- Dashboard domain_events_count: 4.
- API ejecutada en Docker Compose con contenedor Healthy.

Resultado: PASA para la ruta de aprobacion probada.

Commit de implementacion: 253f533.

Las decisiones de rechazo y observacion no forman
parte de esta prueba especifica.
