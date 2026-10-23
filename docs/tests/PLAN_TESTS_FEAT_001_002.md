# Plan de tests — FEAT-001 y FEAT-002

## Objetivo

Demostrar con pruebas automatizadas que las dos features de la demo aplicada funcionan como producto y no únicamente como endpoints técnicos.

## Alcance

| Feature | Archivo de test | Qué valida |
|---|---|---|
| FEAT-001 | `tests/test_feature_001_registration.py` | Registro visual, KPIs, auditoría de precio, riesgo y guardrails |
| FEAT-002 | `tests/test_feature_002_supervisor_dashboard.py` | Validación supervisor, dashboard, métricas y eventos |
| UI | `tests/test_ui_routes.py` | Interfaz `/app` y redirección desde `/` |
| Trazabilidad | `tests/test_traceability_features.py` | FSD, DD, ADR, prompt, código y tests |

## Criterios de aceptación

- Todos los tests deben pasar.
- La cobertura debe ser igual o mayor a 90%.
- Las features deben estar conectadas con documentación y código.
- La UI debe estar disponible en `/app`.
- El dashboard debe actualizarse luego de validar un caso.
- El sistema debe bloquear instrucciones adversariales en campos operativos.

## Comando de ejecución

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=src/app_deteccion --cov-report=term-missing
```

En Linux/Mac:

```bash
pytest --cov=src/app_deteccion --cov-report=term-missing
```
