# README — Persistencia SQLite

**Proyecto:** App Detección Prod — Motor de Workflow BPMN 2.0  
**Entrega:** 06  
**Estado:** APROBADO / ENTREGA FINAL

## 1. Propósito

Esta entrega agrega persistencia durable al motor BPMN 2.0 usando SQLite. El objetivo no es reemplazar el dominio ni el runtime, sino guardar evidencia consultable de:

- definición del workflow;
- instancia de workflow;
- estado de cada tarea;
- recursos runtime;
- trazabilidad completa (`execution_path`);
- incidentes y reintentos;
- workers usados en la ejecución.

En App Detección Prod esto es clave porque el proyecto busca pasar de reportes dispersos por WhatsApp/Excel/fotos a un flujo auditable donde cada detección, validación, decisión comercial, cambio de precio, acción ejecutada e incidente quede trazado.

## 2. Decisión de persistencia

Se eligió **SQLite** por cuatro razones:

1. **Cumple la consigna:** la persistencia era decisión del grupo y debía justificarse.
2. **Es simple de ejecutar:** usa `sqlite3`, incluido en la biblioteca estándar de Python.
3. **Es suficiente para demo académica:** permite persistir snapshots, trazas e incidentes sin levantar un servidor externo.
4. **Es defendible técnicamente:** ofrece más realismo que memoria pura, pero evita complejidad innecesaria de PostgreSQL/Mongo para una primera versión del motor.

## 3. Archivos nuevos

```text
src/persistence/__init__.py
src/persistence/sqlite_repository.py
tests/test_persistence_sqlite.py
docs/README_PERSISTENCE.md
PR_implementation/PR_04_persistence_sqlite.md
docs/TRAZABILIDAD_ENTREGA_06.md
```

## 4. Tablas creadas

| Tabla | Propósito |
|---|---|
| `workflow_definitions` | Guarda la plantilla del workflow como JSON auditable. |
| `workflow_instances` | Guarda estado general de cada ejecución. |
| `task_instances` | Guarda estado runtime por tarea. |
| `trace_entries` | Guarda la traza append-only del flujo. |
| `incidents` | Guarda incidentes `BACKWARD`, glosa, reset y reintentos. |
| `workers` | Guarda trabajadores y especialidad. |

## 5. API principal

| Método | Uso |
|---|---|
| `save_workflow_definition(workflow)` | Persiste la plantilla del grafo. |
| `save_workflow_instance(instance)` | Persiste snapshot completo del runtime. |
| `save_worker(worker)` / `save_workers(workers)` | Persiste empleados/sistema. |
| `load_workflow_definition_payload(workflow_id)` | Recupera definición serializada. |
| `load_workflow_instance_snapshot(instance_id)` | Recupera estado, tareas, traza e incidentes. |
| `count_rows(table)` | Verificación simple para tests/demo. |

## 6. Ejemplo de uso

```python
from pathlib import Path
from src.domain import build_app_deteccion_workflow
from src.persistence import SQLiteWorkflowRepository
from src.runtime import WorkflowInstance

workflow = build_app_deteccion_workflow()
instance = WorkflowInstance(definition=workflow)
instance.start()

repository = SQLiteWorkflowRepository(Path("data/app_deteccion_workflow.db"))
repository.save_workflow_instance(instance)

snapshot = repository.load_workflow_instance_snapshot(instance.id)
print(snapshot["workflow_instance"]["status"])
```

## 7. Qué demuestra ante el docente

Esta entrega demuestra que el motor no solo ejecuta tareas en memoria, sino que deja evidencia durable del proceso. Esto permite defender:

- separación definición/instancia;
- trazabilidad de ejecución;
- auditoría de recursos;
- historial de incidentes;
- reconstrucción del estado actual;
- consistencia entre FSD, código y pruebas.

## 8. Validación técnica

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
