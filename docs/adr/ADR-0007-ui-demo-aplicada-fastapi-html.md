# ADR-0007 — Implementar demo aplicada con FastAPI + HTML server-side render

**Estado:** PROPUESTO / PARA REVISIÓN  
**Fecha:** 2026-07-08  
**Contexto:** Desarrollo de dos features reales para App Detección Prod con demo visible al docente.

## 1. Contexto

El proyecto ya cuenta con una base funcional de API, tests, documentación y trazabilidad. Sin embargo, la nueva necesidad es demostrar dos features del producto como experiencia aplicada, es decir, que el docente pueda navegar una interfaz y observar el flujo real de registro, validación y dashboard.

El problema de negocio exige reducir reportes dispersos, centralizar información, controlar precios, registrar acciones comerciales y mostrar indicadores gerenciales. Por lo tanto, una demo basada únicamente en Swagger no comunica suficientemente la experiencia del producto.

## 2. Decisión

Se decide implementar una interfaz web ligera usando:

- FastAPI como backend ya existente.
- Jinja2 templates para HTML server-side render.
- CSS local simple para estilo de demo.
- Rutas `/app/*` para separar demo visual de endpoints `/cases`, `/dashboard`, `/events` y `/traceability`.
- Reutilización de casos de uso y entidades existentes.

## 3. Opciones consideradas

### Opción A — Mantener solo Swagger

**Ventajas:** rápido, ya funciona, útil para APIs.  
**Desventajas:** no muestra producto aplicado ni experiencia por rol.

### Opción B — Crear frontend SPA con React/Vue

**Ventajas:** más moderno, más cercano a producto final.  
**Desventajas:** aumenta complejidad, dependencias, build, tiempo y riesgo.

### Opción C — FastAPI + Jinja2 + CSS local

**Ventajas:** simple, trazable, ejecutable localmente, suficiente para demo docente.  
**Desventajas:** menor riqueza visual que SPA, pero adecuada para demostrar flujo.

## 4. Decisión seleccionada

Se selecciona la **Opción C**.

## 5. Justificación

Esta opción permite mostrar una app navegable sin romper el alcance del módulo ni introducir complejidad innecesaria. Además, mantiene una sola base Python/FastAPI, facilita tests, evita dependencias de Node.js y permite enfocar la defensa en las features y su trazabilidad.

## 6. Consecuencias positivas

- Demo aplicada visible para docente.
- Flujo por roles más claro.
- Menor complejidad técnica.
- Reutilización de backend existente.
- Mayor trazabilidad FSD → diseño → código → test → demo.
- Facilita capturas para PowerPoint y tutorial.

## 7. Consecuencias negativas

- La UI no representa la versión final productiva.
- No hay autenticación real.
- Menos interacción que una SPA.
- Requiere explicar que es demo funcional, no producto final UI/UX.

## 8. Guardrails

- La UI no debe contener reglas de negocio duplicadas.
- La UI no debe aprobar precios automáticamente.
- La UI no debe ocultar estados de validación.
- La UI debe mostrar trazabilidad y eventos.
- La UI debe permitir reproducir el flujo sin editar código.

## 9. Relación con documentos

| Documento | Relación |
|---|---|
| FSD-FEAT-001-002 | Define alcance funcional |
| DD-FEAT-001-002 | Define implementación técnica |
| PR-IMPL-002 | Controla prompt de implementación |
| PROMPT_MAPPING_FEAT_001_002 | Conecta requerimientos, código y tests |
| CHECKLIST_DEMO_DOS_FEATURES | Verifica cumplimiento antes de entrega |

## 10. Criterios de aceptación de la decisión

- Existe ruta `/app`.
- Existen pantallas de registro, supervisor, dashboard, eventos y trazabilidad.
- Las rutas usan los casos de uso existentes.
- Los tests cubren UI y lógica.
- La demo se ejecuta localmente con instrucciones claras.
