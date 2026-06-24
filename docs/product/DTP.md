---
producto: App Detección Prod
documento: DTP
version: v1.0
fecha: 24/06/2026
status: vivo
audiencia: dual
baseline_ref:
  dti: docs/baseline/DTI_vFinal.md
  tag: release/2.0.0
release: release/3.0.0
stack:
  - Python 3.11+
  - FastAPI
  - Pytest
  - SQLite demo adapter
repo: https://github.com/ginavillanueva/App-Deteccion-Prod-M4
agents_md: /AGENTS.md
---

# DTP — Documento Técnico del Producto vivo

## A.1 Changelog de implementación

| Fecha | Cambio | Disparador | ADR | Prompt | Autor |
|---|---|---|---|---|---|
| 24/06/2026 | Implementación de vertical slice: registro de producto próximo a vencer, acción comercial, cambio de precio, scoring, eventos, validación de supervisor y dashboard | FSD-UC-001 / DD-UC-001 | ADR-0006 | PR-IMPL-001 | Gina |

## A.2 Deltas respecto al DTI vFinal

| # | Sección afectada | Qué cambia | Motivo | ADR |
|---|---|---|---|---|
| 1 | Persistencia de demo | Se agrega repositorio in-memory y adaptador SQLite local para demo | Permitir ejecución local sin infraestructura cloud | ADR-0006 |
| 2 | Dashboard operacional | Se implementan KPIs calculados al consultar datos locales | Demostrar valor gerencial del UC | ADR-0006 |

## A.3 Estado de implementación por FSD-UC

| FSD-UC | Design Doc | Estado | Release | Tests/Evals | Notas |
|---|---|---|---|---|---|
| FSD-UC-001 | DD-UC-001 | implementado | release/3.0.0 | pytest-cov >=90% | Demo backend ejecutable |

## A.4 Trazabilidad código ↔ DTP

`PRD-REQ-001` → `FSD-UC-001` → `DD-UC-001` → `ADR-0006` → `PR-IMPL-001` → `src/app_deteccion/**` → `tests/**` → `DTP`

## B. Contenido técnico vigente

### Arquitectura implementada

Se implementa un monolito modular demostrativo con separación de capas:

- Dominio: entidades, reglas, scoring, eventos y guardrails.
- Aplicación: comandos, casos de uso y queries.
- Infraestructura: repositorio in-memory y adaptador SQLite.
- Adaptadores: API FastAPI.

### Endpoints

- `POST /cases`
- `GET /cases`
- `GET /cases/{case_id}`
- `PATCH /cases/{case_id}/validate`
- `GET /dashboard`
- `GET /events`
- `GET /traceability`
- `DELETE /cases/reset`

### Comando de verificación

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```
