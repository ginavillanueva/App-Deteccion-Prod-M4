# Checklist de implementación UC

## Antes de programar
- [x] Elegir una UC del FSD.
- [x] Crear FSD vivo en `docs/product/FSD.md`.
- [x] Crear Design Doc `DD-UC-001`.
- [x] Crear ADR `ADR-0006`.
- [x] Crear prompt de implementación `PR-IMPL-001`.
- [x] Actualizar `PROMPT_MAPPING.md`.
- [x] Confirmar regla de no tocar `docs/baseline/**`.

## Durante implementación
- [x] Crear dominio.
- [x] Crear caso de uso.
- [x] Crear API.
- [x] Crear dashboard.
- [x] Crear eventos.
- [x] Crear validación supervisor.
- [x] Crear tests.

## Antes de entregar
- [ ] Ejecutar `pytest --cov=src --cov-report=term-missing --cov-fail-under=90`.
- [ ] Ejecutar demo con `uvicorn app_deteccion.main:app --reload`.
- [ ] Probar `POST /cases`.
- [ ] Probar `GET /dashboard`.
- [ ] Probar `GET /traceability`.
- [ ] Subir rama a GitHub.
