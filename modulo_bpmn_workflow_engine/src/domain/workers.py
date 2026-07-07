"""Worker domain model."""

from __future__ import annotations

from dataclasses import dataclass

from .enums import Role, WorkerType


@dataclass(frozen=True)
class Worker:
    """Employee or system worker that can receive tasks.

    The capacity field allows the future orchestrator to implement a
    skill-based + least-loaded assignment policy.
    """

    employee_id: str
    name: str
    worker_type: WorkerType
    capacity: int = 1
    role: Role = Role.WORKER

    def can_take_more(self, active_assignments: int) -> bool:
        """Return True when the worker still has available execution capacity."""
        return active_assignments < self.capacity

    def is_admin(self) -> bool:
        return self.role == Role.ADMIN
