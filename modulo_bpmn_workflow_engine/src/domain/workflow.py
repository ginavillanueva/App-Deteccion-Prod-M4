"""Workflow definition and dependency matrix."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .enums import WorkflowStatus
from .tasks import Task


@dataclass
class DependencyMatrix:
    """Adjacency matrix representation of workflow forward edges."""

    tasks: list[Task]
    matrix: list[list[bool]] = field(init=False)
    index_by_task_id: dict[str, int] = field(init=False)

    def __post_init__(self) -> None:
        self.index_by_task_id = {task.id: index for index, task in enumerate(self.tasks)}
        size = len(self.tasks)
        self.matrix = [[False for _ in range(size)] for _ in range(size)]
        for source in self.tasks:
            source_index = self.index_by_task_id[source.id]
            for target in source.targets:
                if target.id in self.index_by_task_id:
                    self.matrix[source_index][self.index_by_task_id[target.id]] = True

    def has_direct_edge(self, source_task_id: str, target_task_id: str) -> bool:
        return self.matrix[self.index_by_task_id[source_task_id]][self.index_by_task_id[target_task_id]]

    def direct_targets(self, source_task_id: str) -> list[str]:
        source_index = self.index_by_task_id[source_task_id]
        return [
            task.id
            for task, has_edge in zip(self.tasks, self.matrix[source_index])
            if has_edge
        ]

    def reachable_from(self, start_task_id: str) -> set[str]:
        """Return all task ids reachable by FORWARD edges from start_task_id."""
        visited: set[str] = set()
        stack = [start_task_id]
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            stack.extend(task_id for task_id in self.direct_targets(current) if task_id not in visited)
        return visited

    def has_cycle(self) -> bool:
        """Detect whether FORWARD edges contain a cycle."""
        visiting: set[str] = set()
        visited: set[str] = set()

        def dfs(task_id: str) -> bool:
            if task_id in visiting:
                return True
            if task_id in visited:
                return False
            visiting.add(task_id)
            for target_id in self.direct_targets(task_id):
                if dfs(target_id):
                    return True
            visiting.remove(task_id)
            visited.add(task_id)
            return False

        return any(dfs(task.id) for task in self.tasks if task.id not in visited)


@dataclass
class Workflow:
    """Definition/template of a directed business process graph."""

    id: str
    name: str
    version: int
    start_task: Task
    final_tasks: list[Task] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PENDING

    def __post_init__(self) -> None:
        if self.start_task not in self.tasks:
            self.tasks.insert(0, self.start_task)
        for final_task in self.final_tasks:
            if final_task not in self.tasks:
                self.tasks.append(final_task)

    @property
    def dependency_matrix(self) -> DependencyMatrix:
        return DependencyMatrix(self.tasks)

    def add_task(self, task: Task) -> None:
        if task not in self.tasks:
            self.tasks.append(task)

    def validate(self) -> None:
        """Validate workflow-level consistency before runtime instantiation."""
        if not self.id.strip():
            raise ValueError("Workflow id is required")
        if not self.name.strip():
            raise ValueError("Workflow name is required")
        if self.version <= 0:
            raise ValueError("Workflow version must be positive")
        if not self.final_tasks:
            raise ValueError("Workflow requires at least one final task")
        task_ids = [task.id for task in self.tasks]
        if len(task_ids) != len(set(task_ids)):
            raise ValueError("Workflow task ids must be unique")
        for task in self.tasks:
            task.validate()
        reachable = self.dependency_matrix.reachable_from(self.start_task.id)
        missing_final = [task.id for task in self.final_tasks if task.id not in reachable]
        if missing_final:
            raise ValueError(f"Final tasks not reachable from start task: {missing_final}")

    def orphan_tasks(self) -> list[Task]:
        """Return tasks that are not reachable from the start task."""
        reachable = self.dependency_matrix.reachable_from(self.start_task.id)
        return [task for task in self.tasks if task.id not in reachable]

    @classmethod
    def from_tasks(
        cls,
        *,
        workflow_id: str,
        name: str,
        version: int,
        start_task: Task,
        final_tasks: Iterable[Task],
        tasks: Iterable[Task],
    ) -> "Workflow":
        return cls(
            id=workflow_id,
            name=name,
            version=version,
            start_task=start_task,
            final_tasks=list(final_tasks),
            tasks=list(tasks),
        )
