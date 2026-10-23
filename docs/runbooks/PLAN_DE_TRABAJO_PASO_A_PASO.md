# Plan de trabajo paso a paso

## Paso 1 — Elegir la funcionalidad
Se eligió `FSD-UC-001` porque concentra el valor central del producto: registro de producto próximo a vencer, acción comercial, control de precio, scoring y dashboard.

## Paso 2 — Preparar documentación viva
No se modifica el baseline congelado de M4. La implementación vive en `docs/product`, `docs/design`, `docs/adr` y `docs/prompts/impl`.

## Paso 3 — Crear Design Doc
El archivo `docs/design/DD-UC-001-registro-producto-critico.md` explica cómo se construye la UC.

## Paso 4 — Crear ADR
El archivo `docs/adr/ADR-0006-demo-monolito-modular-fastapi-sqlite.md` justifica la decisión técnica de usar monolito modular con FastAPI y SQLite demo.

## Paso 5 — Crear prompt implementation
El archivo `docs/prompts/impl/PR-IMPL-001-registro-producto-critico.md` registra el prompt de implementación.

## Paso 6 — Crear mapping
El archivo `docs/PROMPT_MAPPING.md` conecta PRD, FSD, DD, ADR, prompt, código y tests.

## Paso 7 — Implementar código
El código vive en `src/app_deteccion` y está separado por capas.

## Paso 8 — Probar
Ejecutar:

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

## Paso 9 — Demo
Ejecutar:

```bash
uvicorn app_deteccion.main:app --reload
```

Abrir `http://127.0.0.1:8000/docs`.

## Paso 10 — Subir a GitHub
Crear rama, copiar contenido, hacer commit y push.
