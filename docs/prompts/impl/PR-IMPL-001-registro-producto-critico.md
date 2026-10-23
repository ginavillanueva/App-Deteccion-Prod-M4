# PR-IMPL-001 — Implementación FSD-UC-001

## 1. Objetivo
Implementar una demo funcional para registrar productos próximos a vencer con acción comercial, cambio de precio, scoring de riesgo, eventos, validación de supervisor y dashboard.

## 2. Contexto
Producto: App Detección Prod.
Caso de uso: FSD-UC-001.
Design Doc: DD-UC-001.
ADR: ADR-0006.

## 3. Instrucciones
Crear una aplicación Python/FastAPI con separación:

- Dominio: entidades, reglas, guardrails, scoring y eventos.
- Aplicación: comandos, use cases y dashboard query.
- Infraestructura: repositorio in-memory y SQLite.
- Adaptadores: API REST.
- Tests: unitarios, aplicación y API.

## 4. Reglas obligatorias
- No modificar `docs/baseline/**`.
- Cobertura mínima 90%.
- Bloquear instrucciones adversariales en evidencia y motivo.
- No aprobar descuentos automáticamente.
- No cambiar precios automáticamente.
- Calcular valor financiero en riesgo.
- Calcular valor intervenido por cambio de precio.
- Emitir eventos de dominio.
- Exponer endpoint de trazabilidad.

## 5. Archivos esperados
- `src/app_deteccion/domain/**`
- `src/app_deteccion/application/**`
- `src/app_deteccion/infrastructure/**`
- `src/app_deteccion/adapters/api.py`
- `tests/**`

## 6. Criterio de aceptación del prompt
La implementación se acepta si:

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

pasa correctamente.
