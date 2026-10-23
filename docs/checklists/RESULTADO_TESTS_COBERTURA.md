# Resultado de tests y cobertura

Comando ejecutado:

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

Resultado verificado en este paquete:

```text
41 passed
Cobertura total: 99.54%
Regla requerida: mínimo 90%
Resultado: PASS
```

Esto permite defender que la UC implementada cumple la regla de cobertura definida en `AGENTS.md`.
