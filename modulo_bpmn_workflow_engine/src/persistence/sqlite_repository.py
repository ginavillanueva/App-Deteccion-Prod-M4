"""SQLite persistence adapter for App Deteccion Prod BPMN Workflow Engine.

The course assignment lets each team choose its persistence mechanism and justify
it. This adapter uses only Python's standard ``sqlite3`` module, keeping the
implementation lightweight while still providing durable auditability for
workflow definitions, workflow instances, task instances, incidents and trace
entries.
"""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Optional

from src.domain import Incident, ResourceInstance, Task, TransitionType, Worker, Workflow
from src.runtime import TraceEntry, WorkflowInstance


ISO_UTC_SUFFIX = "+00:00"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _enum_value(value: Any) -> Any:
    """Return raw enum value while leaving simple values untouched."""
    if isinstance(value, Enum):
        return value.value
    return value


def _dt_iso(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    return value.isoformat()


def _json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


class SQLiteWorkflowRepository:
    """Durable repository for workflow snapshots and audit data.

    The repository does not replace the domain/runtime objects. It persists their
    current state so a reviewer can inspect the execution path, resources,
    incident history and workflow status after a demo run.
    """

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        if self.db_path.parent and str(self.db_path.parent) != ".":
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize_schema()

    @contextmanager
    def connect(self):
        """Open a SQLite connection, commit the transaction and close it safely."""
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def initialize_schema(self) -> None:
        """Create all persistence tables if they do not exist."""
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS workflow_definitions (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    task_count INTEGER NOT NULL,
                    final_task_ids_json TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS workflow_instances (
                    id TEXT PRIMARY KEY,
                    definition_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    current_task_ids_json TEXT NOT NULL,
                    variables_json TEXT NOT NULL,
                    iteration INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY(definition_id) REFERENCES workflow_definitions(id)
                );

                CREATE TABLE IF NOT EXISTS task_instances (
                    id TEXT PRIMARY KEY,
                    workflow_instance_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    assigned_worker_ids_json TEXT NOT NULL,
                    per_worker_status_json TEXT NOT NULL,
                    resources_json TEXT NOT NULL,
                    retry_count_json TEXT NOT NULL,
                    retries_exhausted INTEGER NOT NULL,
                    was_reset INTEGER NOT NULL,
                    reset_count INTEGER NOT NULL,
                    started_at TEXT,
                    completed_at TEXT,
                    ready_at TEXT,
                    assigned_at TEXT,
                    assign_deadline TEXT,
                    complete_deadline TEXT,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY(workflow_instance_id) REFERENCES workflow_instances(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS trace_entries (
                    id TEXT PRIMARY KEY,
                    workflow_instance_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT NOT NULL,
                    iteration INTEGER NOT NULL,
                    worker_id TEXT,
                    incident_id TEXT,
                    was_reset INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY(workflow_instance_id) REFERENCES workflow_instances(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS incidents (
                    id TEXT PRIMARY KEY,
                    workflow_instance_id TEXT NOT NULL,
                    from_task_id TEXT NOT NULL,
                    to_task_id TEXT NOT NULL,
                    type TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    raised_by_id TEXT NOT NULL,
                    iteration INTEGER NOT NULL,
                    reset_scope TEXT NOT NULL,
                    reset_targets_json TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY(workflow_instance_id) REFERENCES workflow_instances(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS workers (
                    employee_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    worker_type TEXT NOT NULL,
                    capacity INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_task_instances_workflow
                    ON task_instances(workflow_instance_id);
                CREATE INDEX IF NOT EXISTS idx_trace_workflow
                    ON trace_entries(workflow_instance_id, timestamp);
                CREATE INDEX IF NOT EXISTS idx_incidents_workflow
                    ON incidents(workflow_instance_id);
                """
            )

    def save_workflow_definition(self, workflow: Workflow) -> None:
        """Persist the workflow template/definition as an auditable JSON payload."""
        workflow.validate()
        now = _now_iso()
        payload = self._workflow_definition_payload(workflow)
        with self.connect() as connection:
            existing = connection.execute(
                "SELECT created_at FROM workflow_definitions WHERE id = ?", (workflow.id,)
            ).fetchone()
            created_at = existing["created_at"] if existing else now
            connection.execute(
                """
                INSERT INTO workflow_definitions (
                    id, name, version, status, task_count, final_task_ids_json,
                    payload_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name = excluded.name,
                    version = excluded.version,
                    status = excluded.status,
                    task_count = excluded.task_count,
                    final_task_ids_json = excluded.final_task_ids_json,
                    payload_json = excluded.payload_json,
                    updated_at = excluded.updated_at
                """,
                (
                    workflow.id,
                    workflow.name,
                    workflow.version,
                    workflow.status.value,
                    len(workflow.tasks),
                    _json_dumps([task.id for task in workflow.final_tasks]),
                    _json_dumps(payload),
                    created_at,
                    now,
                ),
            )

    def save_worker(self, worker: Worker) -> None:
        """Persist one worker so assignments remain inspectable."""
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO workers (employee_id, name, worker_type, capacity, role, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(employee_id) DO UPDATE SET
                    name = excluded.name,
                    worker_type = excluded.worker_type,
                    capacity = excluded.capacity,
                    role = excluded.role,
                    updated_at = excluded.updated_at
                """,
                (
                    worker.employee_id,
                    worker.name,
                    worker.worker_type.value,
                    worker.capacity,
                    worker.role.value,
                    _now_iso(),
                ),
            )

    def save_workers(self, workers: Iterable[Worker]) -> None:
        for worker in workers:
            self.save_worker(worker)

    def save_workflow_instance(self, instance: WorkflowInstance) -> None:
        """Persist a full runtime snapshot and append-only audit state.

        For simplicity and determinism during tests, child rows are replaced by
        the current snapshot each time the instance is saved. The trace rows keep
        their original identifiers and timestamps, so the execution path remains
        reproducible.
        """
        self.save_workflow_definition(instance.definition)
        now = _now_iso()
        with self.connect() as connection:
            existing = connection.execute(
                "SELECT created_at FROM workflow_instances WHERE id = ?", (instance.id,)
            ).fetchone()
            created_at = existing["created_at"] if existing else now
            connection.execute(
                """
                INSERT INTO workflow_instances (
                    id, definition_id, status, current_task_ids_json,
                    variables_json, iteration, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    status = excluded.status,
                    current_task_ids_json = excluded.current_task_ids_json,
                    variables_json = excluded.variables_json,
                    iteration = excluded.iteration,
                    updated_at = excluded.updated_at
                """,
                (
                    instance.id,
                    instance.definition.id,
                    instance.status.value,
                    _json_dumps([task.definition.id for task in instance.current_tasks]),
                    _json_dumps(instance.variables),
                    instance.iteration,
                    created_at,
                    now,
                ),
            )
            connection.execute("DELETE FROM task_instances WHERE workflow_instance_id = ?", (instance.id,))
            connection.execute("DELETE FROM trace_entries WHERE workflow_instance_id = ?", (instance.id,))
            connection.execute("DELETE FROM incidents WHERE workflow_instance_id = ?", (instance.id,))

            for task_instance in instance.task_instances.values():
                connection.execute(
                    """
                    INSERT INTO task_instances (
                        id, workflow_instance_id, task_id, status, assigned_worker_ids_json,
                        per_worker_status_json, resources_json, retry_count_json,
                        retries_exhausted, was_reset, reset_count, started_at,
                        completed_at, ready_at, assigned_at, assign_deadline,
                        complete_deadline, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        task_instance.id,
                        instance.id,
                        task_instance.definition.id,
                        task_instance.status.value,
                        _json_dumps([worker.employee_id for worker in task_instance.assigned_workers]),
                        _json_dumps({worker.employee_id: status.value for worker, status in task_instance.per_worker_status.items()}),
                        _json_dumps([self._resource_payload(resource) for resource in task_instance.resources]),
                        _json_dumps(task_instance.retry_count),
                        int(task_instance.retries_exhausted),
                        int(task_instance.was_reset),
                        task_instance.reset_count,
                        _dt_iso(task_instance.started_at),
                        _dt_iso(task_instance.completed_at),
                        _dt_iso(task_instance.ready_at),
                        _dt_iso(task_instance.assigned_at),
                        _dt_iso(task_instance.assign_deadline),
                        _dt_iso(task_instance.complete_deadline),
                        now,
                    ),
                )

            for trace_entry in instance.execution_path:
                connection.execute(
                    """
                    INSERT INTO trace_entries (
                        id, workflow_instance_id, task_id, status, message, iteration,
                        worker_id, incident_id, was_reset, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        trace_entry.id,
                        instance.id,
                        trace_entry.task_id,
                        str(_enum_value(trace_entry.status)),
                        trace_entry.message,
                        trace_entry.iteration,
                        trace_entry.worker_id,
                        trace_entry.incident_id,
                        int(trace_entry.was_reset),
                        _dt_iso(trace_entry.timestamp),
                    ),
                )

            for incident in instance.incidents:
                connection.execute(
                    """
                    INSERT INTO incidents (
                        id, workflow_instance_id, from_task_id, to_task_id, type, reason,
                        raised_by_id, iteration, reset_scope, reset_targets_json, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        incident.id,
                        instance.id,
                        incident.from_task.id,
                        incident.to_task.id,
                        incident.type.value,
                        incident.reason,
                        incident.raised_by.employee_id,
                        incident.iteration,
                        incident.reset_scope.value,
                        _json_dumps([task.id for task in incident.reset_targets]),
                        _dt_iso(incident.timestamp),
                    ),
                )

    def load_workflow_definition_payload(self, workflow_id: str) -> dict[str, Any]:
        """Load the persisted workflow definition as a JSON-compatible dict."""
        with self.connect() as connection:
            row = connection.execute(
                "SELECT payload_json FROM workflow_definitions WHERE id = ?", (workflow_id,)
            ).fetchone()
        if row is None:
            raise KeyError(f"Workflow definition not found: {workflow_id}")
        return json.loads(row["payload_json"])

    def load_workflow_instance_snapshot(self, instance_id: str) -> dict[str, Any]:
        """Load a workflow instance snapshot for inspection/reporting."""
        with self.connect() as connection:
            instance_row = connection.execute(
                "SELECT * FROM workflow_instances WHERE id = ?", (instance_id,)
            ).fetchone()
            if instance_row is None:
                raise KeyError(f"Workflow instance not found: {instance_id}")
            task_rows = connection.execute(
                "SELECT * FROM task_instances WHERE workflow_instance_id = ? ORDER BY task_id", (instance_id,)
            ).fetchall()
            trace_rows = connection.execute(
                "SELECT * FROM trace_entries WHERE workflow_instance_id = ? ORDER BY timestamp, id", (instance_id,)
            ).fetchall()
            incident_rows = connection.execute(
                "SELECT * FROM incidents WHERE workflow_instance_id = ? ORDER BY timestamp, id", (instance_id,)
            ).fetchall()
        return {
            "workflow_instance": self._decode_row_json(self._row_to_dict(instance_row)),
            "task_instances": [self._decode_row_json(self._row_to_dict(row)) for row in task_rows],
            "trace_entries": [self._decode_row_json(self._row_to_dict(row)) for row in trace_rows],
            "incidents": [self._decode_row_json(self._row_to_dict(row)) for row in incident_rows],
        }

    def count_rows(self, table: str) -> int:
        """Return table row count for tests and demo verification."""
        allowed = {
            "workflow_definitions",
            "workflow_instances",
            "task_instances",
            "trace_entries",
            "incidents",
            "workers",
        }
        if table not in allowed:
            raise ValueError(f"Unsupported table: {table}")
        with self.connect() as connection:
            row = connection.execute(f"SELECT COUNT(*) AS count FROM {table}").fetchone()
        return int(row["count"])

    def _workflow_definition_payload(self, workflow: Workflow) -> dict[str, Any]:
        return {
            "id": workflow.id,
            "name": workflow.name,
            "version": workflow.version,
            "status": workflow.status.value,
            "start_task_id": workflow.start_task.id,
            "final_task_ids": [task.id for task in workflow.final_tasks],
            "tasks": [self._task_payload(task) for task in workflow.tasks],
            "forward_edges": [
                {"source": task.id, "target": target.id, "type": TransitionType.FORWARD.value}
                for task in workflow.tasks
                for target in task.targets
            ],
        }

    def _task_payload(self, task: Task) -> dict[str, Any]:
        return {
            "id": task.id,
            "name": task.name,
            "task_type": task.task_type.value,
            "is_final": task.is_final,
            "required_worker_type": task.required_worker_type.value if task.required_worker_type else None,
            "incoming_ids": [incoming.id for incoming in task.incoming],
            "target_ids": [target.id for target in task.targets],
            "logic_gate": {
                "type": task.logic_gate.type.value,
                "depends_on": [dependency.id for dependency in task.logic_gate.depends_on],
                "expression": task.logic_gate.expression,
                "endpoint": task.logic_gate.endpoint,
            }
            if task.logic_gate
            else None,
            "required_resources": [self._resource_spec_payload(resource) for resource in task.required_resources],
            "produced_resources": [self._resource_spec_payload(resource) for resource in task.produced_resources],
            "backward_transitions": [
                {
                    "id": transition.id,
                    "source": transition.source.id,
                    "target": transition.target.id,
                    "type": transition.type.value,
                    "max_retries": transition.max_retries,
                    "exhausted_status": transition.exhausted_status.value,
                    "error_code": transition.error_code,
                }
                for transition in task.backward_transitions
            ],
            "completion_policy": task.completion_policy.value,
            "quorum": task.quorum,
            "max_time_to_assign_seconds": task.max_time_to_assign.total_seconds() if task.max_time_to_assign else None,
            "max_time_to_complete_seconds": task.max_time_to_complete.total_seconds() if task.max_time_to_complete else None,
        }

    def _resource_spec_payload(self, resource: Any) -> dict[str, Any]:
        return {
            "key": resource.key,
            "value": resource.value,
            "type": resource.type.value,
            "mandatory": resource.mandatory,
            "propagate": resource.propagate,
        }

    def _resource_payload(self, resource: ResourceInstance) -> dict[str, Any]:
        return {
            "key": resource.key,
            "value": resource.value,
            "type": resource.type.value,
            "source_task_id": resource.source_task_id,
            "mandatory": resource.mandatory,
            "propagate": resource.propagate,
        }

    def _row_to_dict(self, row: sqlite3.Row) -> dict[str, Any]:
        return {key: row[key] for key in row.keys()}

    def _decode_row_json(self, row: dict[str, Any]) -> dict[str, Any]:
        for key in list(row.keys()):
            if key.endswith("_json") and isinstance(row[key], str):
                decoded_key = key.removesuffix("_json")
                row[decoded_key] = json.loads(row[key])
                del row[key]
        return row
