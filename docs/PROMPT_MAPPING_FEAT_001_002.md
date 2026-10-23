# Prompt Mapping — FEAT-001 y FEAT-002

**Estado:** PARA REVISIÓN  
**Propósito:** Mantener trazabilidad entre problema, FSD, diseño, ADR, prompt, código, tests y demo.

## 1. Mapa de trazabilidad principal

| Necesidad / Dolor | Feature | FSD | Diseño | ADR | Prompt | Código esperado | Tests esperados | Evidencia demo |
|---|---|---|---|---|---|---|---|---|
| Reportes por WhatsApp y fotos dispersas | FEAT-001 | FSD-FEAT-001-002 §3 | DD §6 | ADR-0007 | PR-IMPL-002 | web_ui.py, register_case.html | test_register_case_from_ui | Captura formulario registro |
| Falta de control de precio | FEAT-001 | FSD §3 Reglas | DD §8 | ADR-0007 | PR-IMPL-002 | domain/scoring.py, use_cases.py | test_price_change_requires_reason | Captura auditoría de precio |
| Falta de acciones comerciales trazables | FEAT-001 | FSD §3 | DD §6 | ADR-0007 | PR-IMPL-002 | entities.py, events.py | test_events_visible | Captura eventos |
| Supervisor valida manualmente datos dispersos | FEAT-002 | FSD §4 | DD §6 | ADR-0007 | PR-IMPL-002 | supervisor.html, validate route | test_supervisor_can_validate_case | Captura bandeja supervisor |
| Gerencia no tiene KPIs claros | FEAT-002 | FSD §4 KPIs | DD §6 | ADR-0007 | PR-IMPL-002 | dashboard.html, dashboard use case | test_dashboard_updates_after_validation | Captura dashboard |
| Necesidad de trazabilidad docente | FEAT-001/002 | FSD §6 | DD §12 | ADR-0007 | PR-IMPL-002 | traceability.html | test_traceability_visible | Captura trazabilidad |

## 2. Mapeo de endpoints API existentes a UI

| API / lógica existente | Uso en demo aplicada |
|---|---|
| GET /health | Confirmar que la app está operativa |
| POST /cases | Base para formulario visual de registro |
| GET /cases | Base para bandeja supervisor |
| GET /cases/{case_id} | Base para detalle de caso |
| PATCH /cases/{case_id}/validate | Base para validación visual |
| GET /dashboard | Base para dashboard gerencial visual |
| GET /events | Base para vista de eventos |
| GET /traceability | Base para vista de trazabilidad |

## 3. Mapeo de tests

| Test | Feature | Cubre |
|---|---|---|
| test_register_case_from_ui | FEAT-001 | Formulario, creación y redirección |
| test_register_case_calculates_risk | FEAT-001 | Cálculo de scoring |
| test_price_change_requires_reason | FEAT-001 | Guardrail de precio |
| test_supervisor_can_validate_case | FEAT-002 | Aprobación supervisor |
| test_reject_case_from_supervisor | FEAT-002 | Rechazo supervisor |
| test_dashboard_updates_after_validation | FEAT-002 | KPIs postvalidación |
| test_events_visible | FEAT-001/002 | Eventos de dominio |
| test_traceability_visible | FEAT-001/002 | Trazabilidad documental |

## 4. Criterio de consistencia

No se considera completa una feature si solo existe en código. Debe tener:

```text
Necesidad → FSD → DD → ADR → Prompt → Código → Test → Captura → Tutorial → Defensa
```

## 5. Estado de aprobación

| Elemento | Estado |
|---|---|
| Plan de dos features | Aprobado por estudiante responsable |
| Fase 1 documentación | Pendiente de aprobación |
| Fase 2 código | No iniciar todavía |
| Fase 3 tests | No iniciar todavía |
| Fase 4 tutorial/defensa | No iniciar todavía |
| Fase 5 ZIP final | No iniciar todavía |
