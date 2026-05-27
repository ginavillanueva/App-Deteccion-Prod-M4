# POC-01 — Registro transaccional + dashboard inmediato + Outbox

Esta carpeta contiene la POC-01 de App Detección Prod.

## Objetivo
Validar que el flujo crítico de registro de productos próximos a vencer puede mantener consistencia transaccional, actualizar el dashboard gerencial crítico de forma inmediata y generar eventos confiables para procesos posteriores.

## Cómo ejecutar

```bash
cd pocs/POC-01
python scripts/poc01_benchmark.py
```

## Estructura

```text
pocs/POC-01/
├── POC-01.md
├── README.md
├── MANIFEST.json
├── scripts/
├── evidencia/
├── diagramas/
└── docs/
```

## Qué mirar para la defensa

1. `POC-01.md`: documento principal.
2. `docs/DEFENSE_GUIDE.md`: guion de defensa.
3. `docs/TRACEABILITY_MATRIX.md`: trazabilidad con aprobados.
4. `evidencia/metrics.json`: resultados numéricos.
5. `evidencia/dashboard_snapshot.json`: dashboard inmediato.
6. `evidencia/poc01_app_deteccion_prod.sqlite`: evidencia verificable.
