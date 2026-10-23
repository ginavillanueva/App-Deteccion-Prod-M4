# Demo minuto a minuto

## Minuto 0:00 a 0:40 — Contexto

Decir:

> El problema original era que el control de productos próximos a vencer se hacía con WhatsApp, fotos y reportes dispersos. Esta demo implementa una funcionalidad del FSD para registrar esos casos de forma estructurada.

## Minuto 0:40 a 1:30 — Trazabilidad documental

Abrir:

- `docs/product/FSD.md`
- `docs/design/DD-UC-001-registro-producto-critico.md`
- `docs/adr/ADR-0006-demo-monolito-modular-fastapi-sqlite.md`
- `docs/prompts/impl/PR-IMPL-001-registro-producto-critico.md`
- `docs/PROMPT_MAPPING.md`

Decir:

> Primero está el caso de uso. Luego el Design Doc explica cómo se construye. El ADR justifica la decisión técnica. El prompt registra cómo se usó IA. El mapping conecta todo con código y tests.

## Minuto 1:30 a 2:20 — Ejecutar app

```bash
uvicorn app_deteccion.main:app --reload
```

Abrir:

```text
http://127.0.0.1:8000/docs
```

## Minuto 2:20 a 3:20 — Registrar caso

Ejecutar `POST /cases` con el JSON de ejemplo.

Mostrar:

- `risk_level`
- `score`
- `price_audit`
- `events`

## Minuto 3:20 a 4:00 — Dashboard

Ejecutar `GET /dashboard`.

Mostrar:

- total cases
- high risk cases
- total financial value at risk
- price change cases
- total intervened value

## Minuto 4:00 a 4:30 — Trazabilidad

Ejecutar `GET /traceability`.

Decir:

> Este endpoint resume la cadena PRD, FSD, Design Doc, ADR, prompt, código, tests y DTP.

## Minuto 4:30 a 5:00 — Tests

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

Decir:

> La funcionalidad cumple la regla de cobertura mínima del 90% definida en AGENTS.md.
