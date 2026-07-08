# App Detección Prod — Demo visual trazable de 2 features

Este paquete contiene una demo aplicada para evaluación académica. La app permite demostrar dos features del producto desde interfaz web, no solo desde Swagger.

## Objetivo de la demo

Mostrar cómo App Detección Prod transforma un proceso operativo disperso en un flujo digital trazable:

1. El mercaderista registra un producto crítico desde una interfaz visual.
2. El sistema calcula riesgo, score, SLA, descuento, valor financiero en riesgo y valor intervenido.
3. El supervisor valida el caso con decisión y comentario.
4. Gerencia analiza indicadores mediante dashboard con filtros nacionales, regionales, por canal, cadena, riesgo y acción comercial.
5. La demo evidencia trazabilidad documental: FSD → DD → ADR → Prompt → Código → Tests.

## Features incluidas

### FEAT-001 — Registro visual del mercaderista

Pantalla para registrar tienda, producto, lote, vencimiento, cantidad, precio actual, nuevo precio, acción comercial, evidencia y responsable.

### FEAT-002 — Supervisión + dashboard gerencial avanzado

Incluye bandeja de supervisión, validación del caso y dashboard con KPIs, gráficos, filtros, ranking regional e insights ejecutivos.

## Ejecutar en Windows

1. Doble clic en `01_CREAR_ENTORNO_E_INSTALAR.bat`.
2. Doble clic en `02_EJECUTAR_DEMO.bat`.
3. Abrir en Chrome: `http://127.0.0.1:8000/app`.
4. Para pruebas: doble clic en `03_EJECUTAR_TESTS.bat`.

## Ejecutar manualmente

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app_deteccion.main:app --app-dir src --reload
```

Abrir:

```text
http://127.0.0.1:8000/app
```

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

Resultado esperado:

```text
50 passed
Total coverage: 100.00%
```

## Archivos principales

```text
src/app_deteccion/           Código de la app
tests/                       Pruebas automatizadas
docs/product/                FSD/PRD/DTP
docs/design/                 Design Docs
docs/adr/                    Decisiones arquitectónicas
docs/prompts/impl/           Prompts de implementación
docs/demo/                   Guías de demo
docs/defensa/                Guion de defensa
docs/traceability/           Matrices de trazabilidad
```

## Nota para evaluación

La demo no reemplaza la documentación. La complementa mostrando que las decisiones documentadas fueron llevadas a una interfaz funcional y verificable con tests.
