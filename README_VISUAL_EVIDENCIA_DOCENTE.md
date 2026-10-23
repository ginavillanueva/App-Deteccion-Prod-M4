# App Detección Prod — Demo visual con evidencia fotográfica

Paquete de demostración aplicado para evaluación. La demo muestra dos features trazables del producto:

- **FEAT-001:** registro visual de producto crítico desde rol mercaderista, con acción comercial, cambio de precio, cálculo de riesgo y evidencia fotográfica.
- **FEAT-002:** bandeja de supervisión y dashboard gerencial con análisis nacional/regional, filtros, gráficos, KPIs y trazabilidad documental.

## Mejora incorporada

La interfaz permite adjuntar evidencia fotográfica visible en el registro. La imagen queda vinculada al caso y se muestra en la bandeja de supervisión para que el supervisor valide con respaldo visual.

## Ejecución local

1. Ejecutar `01_CREAR_ENTORNO_E_INSTALAR.bat`.
2. Ejecutar `02_EJECUTAR_DEMO.bat`.
3. Abrir `http://127.0.0.1:8000/app`.
4. Ejecutar `03_EJECUTAR_TESTS.bat` para validar pruebas y cobertura.

## Resultado técnico esperado

- `50 passed`
- Cobertura total: `100%`
- Regla mínima: `>=90%`

## Trazabilidad

La demo mantiene la cadena:

`PRD → FSD → DD → ADR → Prompt → Código → Tests → Demo visual`
