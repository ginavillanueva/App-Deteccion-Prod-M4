"""Skill-based and least-loaded worker assignment policy."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.domain import Role, Worker, WorkerType
from src.runtime import TaskInstance


@dataclass(frozen=True)
class Assignment:
    """Auditable assignment decision."""

    task_id: str
    worker: Worker
    active_assignments_before: int
    capacity: int
    reason: str


@dataclass
class WorkerPool:
    """Pool of workers with active assignment counters.

    Policy implemented: filter by specialty, then choose the least-loaded worker
    with available capacity. This is the recommended baseline for the course
    because it is deterministic, explainable and easy to audit.
    """

    workers: list[Worker]
    active_assignments: dict[str, set[str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.workers:
            raise ValueError("WorkerPool requires at least one worker")
        for worker in self.workers:
            self.active_assignments.setdefault(worker.employee_id, set())

    def select_worker(self, task_instance: TaskInstance) -> Assignment:
        candidates = self._eligible_workers(task_instance)
        if not candidates:
            required = task_instance.definition.required_worker_type
            required_label = required.value if required else "ANY"
            raise ValueError(f"No available worker for task {task_instance.definition.id} requiring {required_label}")

        def score(worker: Worker) -> tuple[float, int, str]:
            active = len(self.active_assignments.get(worker.employee_id, set()))
            load_ratio = active / max(worker.capacity, 1)
            return (load_ratio, active, worker.employee_id)

        selected = min(candidates, key=score)
        active_before = len(self.active_assignments.get(selected.employee_id, set()))
        return Assignment(
            task_id=task_instance.definition.id,
            worker=selected,
            active_assignments_before=active_before,
            capacity=selected.capacity,
            reason="skill-based + least-loaded",
        )

    def mark_assigned(self, workflow_id: str, task_instance: TaskInstance, worker: Worker) -> None:
        key = self.assignment_key(workflow_id, task_instance.definition.id)
        self.active_assignments.setdefault(worker.employee_id, set()).add(key)

    def mark_completed(self, workflow_id: str, task_id: str, worker: Worker) -> None:
        key = self.assignment_key(workflow_id, task_id)
        self.active_assignments.setdefault(worker.employee_id, set()).discard(key)

    def active_count(self, worker: Worker) -> int:
        return len(self.active_assignments.get(worker.employee_id, set()))

    @staticmethod
    def assignment_key(workflow_id: str, task_id: str) -> str:
        return f"{workflow_id}:{task_id}"

    def _eligible_workers(self, task_instance: TaskInstance) -> list[Worker]:
        required: WorkerType | None = task_instance.definition.required_worker_type
        eligible: list[Worker] = []
        for worker in self.workers:
            active = self.active_count(worker)
            if not worker.can_take_more(active):
                continue
            if worker.role == Role.ADMIN or required is None or worker.worker_type == required:
                eligible.append(worker)
        return eligible
