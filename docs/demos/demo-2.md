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
