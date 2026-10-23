# Demo 2 - App Deteccion Prod


Fecha prevista: 26 de octubre de 2026
Rama de trabajo: demo-2-preparacion
Release objetivo: release/8.2.0
Caso de uso identificado: FSD-UC-001

## Funcionalidades

1. Registro de productos criticos por mercaderista.
2. Fotografia, lote, vencimiento, precios y riesgo.
3. Revision y aprobacion del supervisor.
4. Dashboard gerencial con filtros y consulta detallada.
5. Persistencia SQLite y registro de eventos.
6. Paginacion SQL e indice compuesto.

## Evidencia comprobada

- Ocho pruebas automatizadas basicas aprobadas.
- Cinco endpoints HTTP 200.
- OpenAPI 3.1.0 generado y sincronizado.
- Spectral: cero errores y dos advertencias.
- Recuperacion SQLite de producto, foto y validacion comprobada.
- Dos paginas diferentes de diez registros sobre cien datos simulados.
- EXPLAIN QUERY PLAN confirma uso de idx_cases_created_id.

## Pendientes

- Verificar criterios exactos del FSD.
- Ejecutar CI en GitHub.
- Validar integracion grupal en release/8.2.0.
- Revisar privacidad del catalogo comercial antes de publicar.


## Registro individual de funcionalidades — Demo 2

| Integrante | Funcionalidades implementadas | Casos de uso FSD | Repositorio |
|---|---|---|---|
| Gina Villanueva Viscarra (participación individual) | FEAT-001: Registro visual de producto crítico; FEAT-002: Supervisión y dashboard gerencial; contribución técnica: OpenAPI y CI | FSD-UC-001; FSD-UC-002 | https://github.com/ginavillanueva/App-Deteccion-Prod-M4/tree/release/8.2.0 |

## Criterios de aceptación vinculados

**FEAT-001 / FSD-UC-001:** registrar tienda, producto, lote, vencimiento, cantidad, precio y acción comercial; calcular vencimiento, valor financiero, descuento y riesgo; mostrar el caso en la bandeja supervisora.

**FEAT-002 / FSD-UC-002:** revisar un caso y su evidencia; aprobarlo con comentario; cambiar su estado a VALIDADO_SUPERVISOR; actualizar los indicadores gerenciales.

**OpenAPI y CI:** contrato generado desde FastAPI, archivo openapi.json versionado, verificación de drift y lint con Spectral mediante .github/workflows/openapi-ci.yml.

**Evidencia:** registro visual, validación supervisora exitosa, dashboard de seis casos (uno validado), ocho pruebas básicas aprobadas y ejecuciones verdes de GitHub Actions.
