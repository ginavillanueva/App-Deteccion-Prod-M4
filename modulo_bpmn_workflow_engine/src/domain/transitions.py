"""Typed graph transitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from .enums import TransitionType, WorkflowStatus

if TYPE_CHECKING:  # pragma: no cover - imported for type checking only
    from .tasks import Task


@dataclass
class Transition:
    """Directed graph edge between tasks.

    FORWARD transitions represent normal progress. BACKWARD transitions
    represent incidents/rework and must define retry constraints.
    """

    source: "Task"
    target: "Task"
    type: TransitionType = TransitionType.FORWARD
    max_retries: Optional[int] = None
    exhausted_status: WorkflowStatus = WorkflowStatus.ERROR
    error_code: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if self.type == TransitionType.BACKWARD:
            if self.max_retries is None:
                raise ValueError("BACKWARD transitions must define max_retries")
            if self.max_retries < 0:
                raise ValueError("max_retries cannot be negative")
        elif self.max_retries is not None:
            raise ValueError("Only BACKWARD transitions may define max_retries")
