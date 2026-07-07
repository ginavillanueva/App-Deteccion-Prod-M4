"""Runtime trace entries for App Deteccion Prod BPMN Workflow Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from src.domain import TaskStatus, WorkflowStatus


@dataclass
class TraceEntry:
    """Append-only audit item used to reconstruct the workflow path.

    The trace intentionally stores task id, status, worker id, incident id and
    iteration so the same task can appear multiple times when a rework cycle
    occurs. This is the runtime evidence expected by the assignment.
    """

    task_id: str
    status: TaskStatus | WorkflowStatus | str
    message: str
    iteration: int
    worker_id: Optional[str] = None
    incident_id: Optional[str] = None
    was_reset: bool = False
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id: str = field(default_factory=lambda: str(uuid4()))
