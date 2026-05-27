# POC-02 — IA con guardrails y scoring cuantificado

Esta carpeta contiene la POC-02 de App Detección Prod.

## Objetivo

Validar que una capa IA puede clasificar productos próximos a vencer en BAJO/MEDIO/ALTO usando criterios cuantificados, sin ejecutar acciones comerciales irreversibles.

## Cómo ejecutar

```bash
cd pocs/POC-02
python scripts/poc02_ai_guardrails.py
```

## Archivos clave

- `POC-02.md`: documento formal alineado al template.
- `data/poc02_dataset.csv`: dataset sintético.
- `evidencia/metrics.json`: métricas de ejecución.
- `docs/TRACEABILITY_MATRIX.md`: trazabilidad con documentos aprobados.
- `docs/DEFENSE_GUIDE.md`: guía de defensa oral.
