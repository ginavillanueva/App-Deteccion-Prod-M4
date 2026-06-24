# Guía paso a paso para Gina — desde cero

Esta guía está escrita como si nunca hubieras subido código a GitHub.

## Parte 1 — Qué estás haciendo

No estás construyendo toda la app. Estás construyendo una sola funcionalidad completa del FSD.

Funcionalidad elegida:

**FSD-UC-001 — Registrar producto próximo a vencer con acción comercial, cambio de precio y dashboard.**

La idea es demostrar esta cadena:

`FSD → Design Doc → ADR → Prompt → Código → Tests → Demo → DTP`

## Parte 2 — Descargar el repo

Abre Git Bash o terminal y escribe:

```bash
git clone https://github.com/ginavillanueva/App-Deteccion-Prod-M4.git
```

Entra a la carpeta:

```bash
cd App-Deteccion-Prod-M4
```

## Parte 3 — Crear rama nueva

```bash
git checkout -b release/3.0.0-implementacion-uc
```

Esto crea una rama nueva para no mezclar tu entrega anterior con esta implementación.

## Parte 4 — Copiar archivos

Descomprime el ZIP de este paquete.

Copia TODO el contenido del paquete dentro de tu repo.

Te debe quedar así:

```text
AGENTS.md
README.md
requirements.txt
pyproject.toml
docs/
src/
tests/
scripts/
```

No subas el ZIP. Sube el contenido.

## Parte 5 — Crear entorno virtual

```bash
python -m venv .venv
```

Si estás en Windows:

```bash
.venv\Scripts\activate
```

Si estás en Mac, Linux o Git Bash:

```bash
source .venv/bin/activate
```

## Parte 6 — Instalar dependencias

```bash
pip install -r requirements.txt
```

## Parte 7 — Ejecutar tests

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

Esto debe pasar. Si pasa, significa que cumpliste la regla de 90%.

## Parte 8 — Ejecutar la demo

```bash
uvicorn app_deteccion.main:app --reload
```

Abre en navegador:

```text
http://127.0.0.1:8000/docs
```

## Parte 9 — Probar demo en Swagger

Primero ejecuta:

`GET /health`

Luego ejecuta:

`POST /cases`

Copia este JSON:

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
  "price_change_reason": "Descuento autorizado por supervisor",
  "evidence_note": "Foto clara de gondola y etiqueta de precio",
  "created_by": "mercaderista.demo"
}
```

Después ejecuta:

`GET /dashboard`

Y luego:

`GET /traceability`

## Parte 10 — Subir a GitHub

Verifica qué cambió:

```bash
git status
```

Agrega todo:

```bash
git add .
```

Crea commit:

```bash
git commit -m "feat: implementar FSD-UC-001 registro producto critico"
```

Sube la rama:

```bash
git push -u origin release/3.0.0-implementacion-uc
```

Tu link será:

```text
https://github.com/ginavillanueva/App-Deteccion-Prod-M4/tree/release/3.0.0-implementacion-uc
```

## Parte 11 — Qué decir en defensa

> Para esta entrega desarrollé una funcionalidad completa del FSD, no toda la plataforma. Elegí FSD-UC-001 porque representa el núcleo del proyecto: registrar un producto próximo a vencer, asociar una acción comercial, controlar cambio de precio, calcular riesgo, emitir eventos y alimentar un dashboard gerencial básico.
>
> Antes de programar hice el Design Doc DD-UC-001, donde explico cómo se construye. También registré el ADR-0006, porque tomé una decisión técnica: implementar la demo como monolito modular con FastAPI y adaptador SQLite local. Luego documenté el prompt PR-IMPL-001 y lo conecté en PROMPT_MAPPING.md.
>
> En la demo muestro el endpoint de registro, el dashboard, los eventos, la trazabilidad y la ejecución de tests con cobertura mínima del 90%.
