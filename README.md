# App Detección Prod — Implementación FSD-UC-001

Este paquete implementa una funcionalidad completa del FSD como **vertical slice trazable**:

> Registrar producto próximo a vencer con acción comercial, cambio de precio, scoring de riesgo, eventos de dominio, validación de supervisor y dashboard gerencial básico.

## Por qué esta funcionalidad
Esta UC concentra el valor principal del proyecto:

- reemplaza reportes dispersos por WhatsApp/Excel;
- centraliza producto, tienda, lote, vencimiento, cantidad y evidencia;
- registra acción comercial;
- controla cambio de precio;
- calcula riesgo BAJO/MEDIO/ALTO;
- actualiza KPIs para gerencia;
- demuestra trazabilidad desde FSD hasta tests.

## Estructura principal

```text
AGENTS.md
README.md
requirements.txt
pyproject.toml
docs/
  baseline/                 # No tocar. M4 congelado.
  product/                  # PRD/FSD/DTP vivos.
  design/                   # DD-UC-001.
  adr/                      # ADR-0006.
  prompts/impl/             # PR-IMPL-001.
  PROMPT_MAPPING.md
src/app_deteccion/
  domain/                   # Entidades, reglas, scoring y eventos.
  application/              # Casos de uso y queries.
  infrastructure/           # Repositorios in-memory y SQLite.
  adapters/                 # API FastAPI.
tests/
scripts/
```

## Instalación

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Mac/Linux/Git Bash:

```bash
source .venv/bin/activate
```

Instala dependencias:

```bash
pip install -r requirements.txt
```

## Ejecutar tests con cobertura 90%

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

## Ejecutar demo

```bash
uvicorn app_deteccion.main:app --reload
```

Abre en el navegador:

```text
http://127.0.0.1:8000/docs
```

## Endpoints principales

- `GET /health`
- `POST /cases`
- `GET /cases`
- `GET /cases/{case_id}`
- `PATCH /cases/{case_id}/validate`
- `GET /dashboard`
- `GET /traceability`
- `DELETE /cases/reset`

## Payload de prueba

```json
{
  "store": "Hipermaxi Sur",
  "product_name": "Yogurt Natural 1L",
  "batch": "L-2026-07",
  "expiration_date": "2026-07-20",
  "quantity": 25,
  "current_price": 18.5,
  "new_price": 14.5,
  "commercial_action": "DESCUENTO",
  "price_change_approved": true,
  "evidence_note": "Foto clara de góndola y etiqueta de precio",
  "created_by": "mercaderista.demo"
}
```

## Qué demostrar en defensa

1. Abre `docs/product/FSD.md` y muestra `FSD-UC-001`.
2. Abre `docs/design/DD-UC-001-registro-producto-critico.md`.
3. Abre `docs/adr/ADR-0006-demo-monolito-modular-fastapi-sqlite.md`.
4. Abre `docs/prompts/impl/PR-IMPL-001-registro-producto-critico.md`.
5. Abre `docs/PROMPT_MAPPING.md`.
6. Ejecuta la API.
7. Registra un caso.
8. Muestra dashboard.
9. Ejecuta tests con cobertura.

Frase clave:

> Esta implementación demuestra trazabilidad completa: PRD → FSD → Design Doc → ADR → Prompt → Código → Tests → DTP.
