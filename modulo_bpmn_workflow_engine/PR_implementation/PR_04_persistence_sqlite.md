# PR Implementation 04 — Persistencia SQLite

**Proyecto:** App Detección Prod — Motor BPMN 2.0  
**Estado:** APROBADO / ENTREGA FINAL  
**Feature:** Persistencia durable de definiciones, instancias, tareas, recursos, trazas e incidentes.

## 1. Objetivo del PR

Implementar una capa de persistencia ligera usando SQLite para guardar evidencia durable del motor de workflow. Esta capa permite demostrar que el proceso de App Detección Prod puede ejecutarse, auditarse y revisarse después de la ejecución.

## 2. Decisión de diseño

Se implementó un adaptador `SQLiteWorkflowRepository` en `src/persistence/sqlite_repository.py`.

La decisión fue usar SQLite porque:

- no requiere servidor externo;
- está incluido en Python mediante `sqlite3`;
- permite revisar la traza con SQL;
- es suficiente para una demo académica;
- es más defendible que persistencia solo en memoria;
- puede evolucionar a PostgreSQL si el producto escala.

## 3. Alcance técnico

El PR agrega persistencia para:

| Entidad | Persistencia |
|---|---|
| `Workflow` | `workflow_definitions` |
| `WorkflowInstance` | `workflow_instances` |
| `TaskInstance` | `task_instances` |
| `TraceEntry` | `trace_entries` |
| `Incident` | `incidents` |
| `Worker` | `workers` |

## 4. Métodos implementados

| Método | Responsabilidad |
|---|---|
| `initialize_schema()` | Crear tablas e índices. |
| `save_workflow_definition()` | Guardar plantilla del grafo como JSON auditable. |
| `save_workflow_instance()` | Guardar snapshot completo de ejecución. |
| `save_worker()` | Persistir trabajadores. |
| `load_workflow_definition_payload()` | Recuperar definición serializada. |
| `load_workflow_instance_snapshot()` | Recuperar estado runtime completo. |
| `count_rows()` | Soporte de verificación para tests. |

## 5. Relación con FSD

| FSD | Implementación |
|---|---|
| Persistencia justificada | SQLite con `sqlite3` estándar. |
| Trazabilidad completa | Tabla `trace_entries`. |
| Incidentes y glosa | Tabla `incidents`. |
| Estado runtime | Tablas `workflow_instances` y `task_instances`. |
| Recursos | JSON dentro de `task_instances.resources_json`. |
| Workers | Tabla `workers`. |

## 6. Relación con App Detección Prod

El motor guarda evidencia de tareas como:

- detección del producto próximo a vencer;
- validación de evidencia;
- clasificación de riesgo;
- validación de precio;
- decisión comercial;
- aprobación de cambio de precio;
- ejecución en sala;
- revisión del supervisor;
- cierre y actualización de dashboard.

Esto protege el objetivo del proyecto: trazabilidad, control de precios, impacto financiero y reducción de merma.

## 7. Pruebas agregadas

Archivo:

```text
tests/test_persistence_sqlite.py
```

Casos:

| Test | Qué valida |
|---|---|
| `test_save_workflow_definition_payload` | Guarda y recupera definición del workflow. |
| `test_save_runtime_snapshot_with_trace_and_task_state` | Persiste instancia, tareas, recursos, traza y worker. |
| `test_save_snapshot_after_rework_incident` | Persiste incidente, reset scope y traza asociada. |

## 8. Evidencia técnica

Comandos ejecutados:

```bash
python -m compileall src
python -m unittest discover -s tests
```

Resultado:

```text
Ran 16 tests
OK
```

## 9. Trade-offs

| Alternativa | Ventaja | Desventaja | Decisión |
|---|---|---|---|
| Memoria | Muy simple | No deja evidencia durable | Descartada |
| SQLite | Ligera, auditable, sin servidor | Menos escalable que PostgreSQL | Elegida |
| PostgreSQL | Más productivo a escala | Requiere servidor/configuración | Futuro |
| MongoDB | Flexible en documentos | Más complejidad operativa | Futuro |

## 10. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Serialización incompleta del grafo | Payload JSON explícito por task, recurso, edge y transition. |
| Pérdida de trazabilidad | `trace_entries` persiste cada `TraceEntry`. |
| Incidentes no auditables | Tabla dedicada `incidents`. |
| Complejidad excesiva | Uso de `sqlite3` estándar y API simple. |

## 11. Definition of Done

- [x] Esquema SQLite creado automáticamente.
- [x] Definiciones persistidas.
- [x] Instancias persistidas.
- [x] Tareas runtime persistidas.
- [x] Trazas persistidas.
- [x] Incidentes persistidos.
- [x] Workers persistidos.
- [x] Tests agregados.
- [x] `compileall` OK.
- [x] `unittest` OK.
