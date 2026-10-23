# App Detección Prod — Demo final visual, trazable y con evidencia fotográfica

Este paquete contiene una demo aplicada de dos features del producto, preparada para evaluación docente y revisión pública.

## Features demostradas

1. **FEAT-001 — Registro visual desde rol mercaderista**
   - Registro de producto crítico próximo a vencer.
   - Captura de tienda, producto, lote, vencimiento, cantidad, precio actual, nuevo precio y acción comercial.
   - Evidencia fotográfica visible para supervisión.
   - Cálculo de score, riesgo, SLA, valor financiero en riesgo y valor intervenido.

2. **FEAT-002 — Supervisión + dashboard gerencial**
   - Bandeja de casos para validación supervisora.
   - Visualización de evidencia fotográfica antes de aprobar o rechazar.
   - Dashboard con análisis nacional/regional, filtros, KPIs, gráficos, ranking regional e insights ejecutivos.

## Trazabilidad

La demo mantiene la cadena:

`PRD → FSD → DD → ADR → Prompt → Código → Tests → Demo visual`

## Ejecución local

1. Ejecutar `01_CREAR_ENTORNO_E_INSTALAR.bat`.
2. Ejecutar `02_EJECUTAR_DEMO.bat`.
3. Abrir `http://127.0.0.1:8000/app`.
4. Ejecutar `03_EJECUTAR_TESTS.bat` para validar pruebas.

## Resultado técnico validado

- 50 tests aprobados.
- Cobertura total: 100%.
- Regla mínima requerida: >=90%.

## Rama recomendada

`release/4.2.0-demo-visual-evidencia-dashboard`
