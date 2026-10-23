# Checklist — Demo aplicada de dos features

**Estado:** PARA REVISIÓN  
**Uso:** verificar antes de aprobar cada fase.

## Fase 1 — Documentación y trazabilidad

- [ ] FSD-FEAT-001-002 revisado.
- [ ] DD-FEAT-001-002 revisado.
- [ ] ADR-0007 revisado.
- [ ] PR-IMPL-002 revisado.
- [ ] PROMPT_MAPPING_FEAT_001_002 revisado.
- [ ] Matriz de trazabilidad incluida.
- [ ] estudiante responsable aprobó Fase 1.

## Fase 2 — Código de demo aplicada

- [ ] Existe ruta `/app`.
- [ ] Existe pantalla de inicio.
- [ ] Existe pantalla de registro mercaderista.
- [ ] El formulario registra caso.
- [ ] Se calcula riesgo.
- [ ] Se calcula valor financiero en riesgo.
- [ ] Se audita cambio de precio.
- [ ] Existe bandeja supervisor.
- [ ] Supervisor puede aprobar.
- [ ] Supervisor puede rechazar.
- [ ] Existe dashboard gerencial visual.
- [ ] Existen eventos visibles.
- [ ] Existe trazabilidad visible.
- [ ] estudiante responsable aprobó Fase 2.

## Fase 3 — Tests y cobertura

- [ ] Tests de FEAT-001.
- [ ] Tests de FEAT-002.
- [ ] Tests de UI routes.
- [ ] Tests de eventos.
- [ ] Tests de trazabilidad.
- [ ] Cobertura >= 90%.
- [ ] Captura de tests guardada.
- [ ] estudiante responsable aprobó Fase 3.

## Fase 4 — Tutorial y defensa

- [ ] Tutorial docente en Word/PDF.
- [ ] PowerPoint de defensa.
- [ ] Guion de 5 minutos.
- [ ] Capturas de la app aplicada.
- [ ] Explicación de errores corregidos.
- [ ] Explicación de trazabilidad.
- [ ] estudiante responsable aprobó Fase 4.

## Fase 5 — ZIP final

- [ ] Solo contiene archivos aprobados.
- [ ] No contiene `.venv`.
- [ ] No contiene `__pycache__`.
- [ ] No contiene `.pyc`.
- [ ] No contiene `.pytest_cache`.
- [ ] Incluye MANIFEST.
- [ ] Incluye README de entrega.
- [ ] Incluye docs, src, tests, tutoriales y presentación.
- [ ] estudiante responsable aprobó ZIP final.

## Comandos esperados de validación

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=src --cov-fail-under=90
.\.venv\Scripts\python.exe -m uvicorn app_deteccion.main:app --app-dir src --reload
```

## Evidencia mínima para defensa

- Captura de app `/app`.
- Captura de registro FEAT-001.
- Captura del detalle con riesgo y precio.
- Captura de bandeja supervisor FEAT-002.
- Captura de validación.
- Captura del dashboard final.
- Captura de eventos.
- Captura de trazabilidad.
- Captura de tests y cobertura.
- Captura de rama GitHub.
