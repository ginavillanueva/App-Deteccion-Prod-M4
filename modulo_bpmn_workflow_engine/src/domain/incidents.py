"""Incident definition used for backward transitions and rework."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import uuid4

from .enums import IncidentType, ResetScope

if TYPE_CHECKING:  # pragma: no cover
    from .tasks import Task
    from .workers import Worker


@dataclass
class Incident:
    """Typed reason for a BACKWARD transition.

    The reason/glosa is mandatory because the teacher's design asks for full
    traceability of rework decisions.
    """

    from_task: "Task"
    to_task: "Task"
    type: IncidentType
    reason: str
    raised_by: "Worker"
    iteration: int
    reset_scope: ResetScope = ResetScope.ALL_DOWNSTREAM
    reset_targets: list["Task"] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.reason or not self.reason.strip():
            raise ValueError("Incident reason is mandatory")
        if self.iteration <= 0:
            raise ValueError("Incident iteration must be positive")
        if self.reset_scope == ResetScope.SPECIFIC and not self.reset_targets:
            raise ValueError("SPECIFIC reset scope requires reset_targets")
