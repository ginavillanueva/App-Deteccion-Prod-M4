# Guía de demo visual para docente y público evaluador

## Propósito

Esta guía explica cómo revisar la demo aplicada de dos features de App Detección Prod.

## Paso 1 — Abrir demo

Ejecutar la aplicación y abrir:

```text
http://127.0.0.1:8000/app
```

## Paso 2 — Reiniciar demo

Presionar **Reiniciar demo** para empezar desde cero.

## Paso 3 — Registrar producto como mercaderista

Ir a **1. Mercaderista registra** y completar o usar los datos por defecto.

El formulario representa el trabajo del mercaderista en sala: tienda, producto, lote, vencimiento, cantidad, precio, acción comercial y evidencia.

## Paso 4 — Interpretar riesgo

Al registrar, el sistema muestra:

- Riesgo BAJO/MEDIO/ALTO.
- Score.
- SLA.
- Valor financiero en riesgo.
- Valor intervenido.
- Descuento.
- Tabla de variables usadas para clasificar.

## Paso 5 — Validar como supervisor

Ir a **2. Bandeja supervisor**, seleccionar un caso y presionar **Validar caso seleccionado**.

La validación deja usuario, decisión, comentario y cambio de estado.

## Paso 6 — Analizar como gerencia

Ir a **3. Gerencia analiza**.

El dashboard permite revisar:

- Casos filtrados.
- Validados y pendientes.
- Riesgo alto, medio y bajo.
- Valor financiero en riesgo.
- Cantidad intervenida.
- Cambios de precio.
- Cambios sin aprobación.
- Descuento promedio.
- Gráficos por riesgo, región, acción comercial y canal.
- Ranking regional.
- Insights ejecutivos.

## Paso 7 — Usar filtros

Probar filtros por:

- Vista nacional/regional.
- Región.
- Canal.
- Cadena.
- Riesgo.
- Acción comercial.

## Paso 8 — Ver trazabilidad

Ir a **4. Eventos y trazabilidad**.

Esta pantalla muestra eventos de dominio y conexión documental: FSD, DD, ADR, prompt, código y tests.

## Paso 9 — Ejecutar tests

Ejecutar:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

Resultado esperado: `50 passed` y cobertura `100%`.
