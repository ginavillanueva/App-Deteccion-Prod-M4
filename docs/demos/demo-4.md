# Demo Evaluada 4 — App Deteccion de Productos

**Release:** 8.4.0
**Integrante:** Gina Villanueva
**Rama:** release/8.4.0

## 1. Funcionalidades presentadas

| Funcionalidad | Caso de uso FSD | Criterios de aceptacion | Evidencia |
|---|---|---|---|
| FEAT-001: Registro y clasificacion de productos proximos a vencer | FSD-UC-001 | Registro del caso, calculo de dias al vencimiento, clasificacion de riesgo, valor financiero y generacion de eventos | POST /cases, GET /cases/{case_id}, GET /dashboard |
| FEAT-002: Aprobacion del supervisor | FSD-UC-002 | Estado APROBADO, identificacion del supervisor, evento CaseValidated.v1 y dashboard actualizado | PATCH /cases/{case_id}/validate, GET /events, GET /dashboard |

Las funcionalidades fueron implementadas y verificadas anteriormente.
Para Demo 4 se conserva su integracion con la aplicacion.

## 2. Contrato OpenAPI e integracion continua

El contrato `openapi.json` se genera desde el codigo FastAPI mediante:

`python scripts/export_openapi.py`

Verificacion local realizada:

`python scripts/export_openapi.py --check`

Resultado: `OK: OpenAPI coincide con el codigo.`

El workflow `.github/workflows/openapi-ci.yml` incluye:
- Exportacion y comprobacion de diferencias OpenAPI.
- Validacion mediante Spectral.

La ejecucion exitosa del workflow en GitHub debe verificarse por separado.

## 3. Prueba de rendimiento con k6

**Ruta:** GET /dashboard

**Script:** `bench/demo4-dashboard.js`

**Resultado:** `bench/resultados/demo4-final.json`

Configuracion:
- Ejecutor: constant-arrival-rate.
- Ritmo: 5 solicitudes por segundo.
- Duracion: 30 segundos.
- VUs preasignados: 10.
- Maximo: 20 VUs.

Resultados finales:

| Metrica | Resultado |
|---|---:|
| Solicitudes | 151 |
| p95 | 10,77 ms |
| Promedio | 7,94 ms |
| Mediana | 7,50 ms |
| Maximo | 18,31 ms |
| Errores HTTP | 0 % |

Se cumplieron los umbrales configurados para esta carga.

## 4. OpenTelemetry y Grafana Tempo

Se implemento instrumentacion distribuida para FastAPI.

Componentes:
- `src/app_deteccion/observability.py`
- `src/app_deteccion/application/use_cases.py`
- `compose.observability.yaml`
- `observability/tempo.yaml`
- Grafana Explore y Tempo.

Traza seleccionada de la prueba final:
- Trace ID: `142ca14f17c1d94d862839a0e2e190db`
- Servicio: `app-deteccion-prod`
- Ruta: `GET /dashboard`
- Duracion total: 3,26 ms
- Cantidad de spans: 5

Desglose observado:

| Span | Duracion |
|---|---:|
| dashboard.sqlite.list_all | 626,23 microsegundos |
| dashboard.calculate_metrics | 486,38 microsegundos |
| Envio HTTP 1 | 37,14 microsegundos |
| Envio HTTP 2 | 21 microsegundos |

**Interpretacion:** entre las operaciones internas instrumentadas,
la recuperacion de productos desde SQLite consume mas tiempo
que el calculo de indicadores. Otras operaciones de FastAPI
tambien forman parte de la duracion total.

El p95 de k6 representa una distribucion de solicitudes;
la traza corresponde a una solicitud individual.

## 5. Pruebas de regresion

`python -m pytest -q`

Resultado: 8 pruebas superadas.

La verificacion local OpenAPI tambien finalizo correctamente.

## 6. Reproduccion del stack

`docker compose -f compose.yaml -f compose.observability.yaml up -d --build --wait`

Servicios:
- API: http://localhost:18080
- Grafana: http://localhost:3300
- Tempo: http://localhost:3200

## 7. Conclusiones

1. Las funcionalidades FEAT-001 y FEAT-002 permanecen integradas con el producto.
2. El contrato OpenAPI coincide con la implementacion.
3. La prueba k6 final registro p95 de 10,77 ms y 0 % de errores bajo la carga evaluada.
4. OpenTelemetry permitio localizar y comparar operaciones internas.
5. SQLite fue el tramo interno medido mas costoso de la traza seleccionada.
6. Los resultados no representan una garantia de rendimiento para cargas mayores.
7. La validacion del workflow en GitHub y la publicacion del release se verificaran al completar la entrega.
