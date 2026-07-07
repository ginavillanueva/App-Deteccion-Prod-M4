"""Task definition model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from typing import Optional

from .enums import CompletionPolicy, TaskType, TransitionType, WorkerType
from .gates import LogicGate
from .resources import ResourceSpec
from .transitions import Transition


@dataclass
class Task:
    """Definition of a workflow node.

    A Task is part of the template/definition layer. It does not store runtime
    execution state; that will be handled by TaskInstance in the next delivery.
    """

    id: str
    name: str
    targets: list["Task"] = field(default_factory=list)
    incoming: list["Task"] = field(default_factory=list)
    backward_transitions: list[Transition] = field(default_factory=list)
    logic_gate: Optional[LogicGate] = None
    required_resources: list[ResourceSpec] = field(default_factory=list)
    produced_resources: list[ResourceSpec] = field(default_factory=list)
    required_worker_type: Optional[WorkerType] = None
    task_type: TaskType = TaskType.HUMAN
    is_final: bool = False
    completion_policy: CompletionPolicy = CompletionPolicy.ALL
    quorum: Optional[int] = None
    max_time_to_assign: Optional[timedelta] = None
    max_time_to_complete: Optional[timedelta] = None

    def add_target(self, target: "Task") -> Transition:
        """Add a FORWARD edge to another task and maintain reverse incoming refs."""
        if target not in self.targets:
            self.targets.append(target)
        if self not in target.incoming:
            target.incoming.append(self)
        return Transition(source=self, target=target, type=TransitionType.FORWARD)

    def add_backward_transition(
        self,
        target: "Task",
        *,
        max_retries: int,
        error_code: Optional[str] = None,
    ) -> Transition:
        """Add a BACKWARD transition used for incidents/rework."""
        transition = Transition(
            source=self,
            target=target,
            type=TransitionType.BACKWARD,
            max_retries=max_retries,
            error_code=error_code,
        )
        self.backward_transitions.append(transition)
        return transition

    def requires_join_gate(self) -> bool:
        return len(self.incoming) > 1

    def validate(self) -> None:
        """Validate local task consistency."""
        if not self.id.strip():
            raise ValueError("Task id is required")
        if not self.name.strip():
            raise ValueError("Task name is required")
        if self.requires_join_gate() and self.logic_gate is None:
            raise ValueError(f"Task {self.id} has multiple incoming edges and requires a LogicGate")
        if self.completion_policy == CompletionPolicy.QUORUM:
            if self.quorum is None or self.quorum <= 0:
                raise ValueError("QUORUM completion policy requires a positive quorum")
        if self.max_time_to_assign is not None and self.max_time_to_assign.total_seconds() <= 0:
            raise ValueError("max_time_to_assign must be positive")
        if self.max_time_to_complete is not None and self.max_time_to_complete.total_seconds() <= 0:
            raise ValueError("max_time_to_complete must be positive")
