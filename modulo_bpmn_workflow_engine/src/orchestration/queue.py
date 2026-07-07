"""Ready queue implemented with collections.deque.

The course assignment asks for a queue + Observer orchestrator, emulating AWS
SQS without cron. This module provides the queue side of that contract.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable

from src.domain import TaskStatus
from src.runtime import TaskInstance, WorkflowInstance

from .events import OrchestrationEvent, OrchestrationObserver


@dataclass(frozen=True)
class ReadyQueueItem:
    """Pointer to a READY task inside a workflow instance."""

    workflow_id: str
    task_id: str


class ReadyQueue:
    """FIFO queue for READY tasks with Observer notifications.

    A task enters the queue only when its runtime status is READY. The queue
    does not execute business logic; it publishes events so an Orchestrator can
    assign workers and drive execution.
    """

    def __init__(self) -> None:
        self._items: deque[ReadyQueueItem] = deque()
        self._known: set[ReadyQueueItem] = set()
        self._observers: list[OrchestrationObserver] = []

    def subscribe(self, observer: OrchestrationObserver) -> None:
        self._observers.append(observer)

    def enqueue(self, workflow: WorkflowInstance, task_instance: TaskInstance) -> ReadyQueueItem:
        if task_instance.status != TaskStatus.READY:
            raise ValueError(
                f"Task {task_instance.definition.id} must be READY before entering the ReadyQueue; "
                f"current={task_instance.status.value}"
            )
        item = ReadyQueueItem(workflow_id=workflow.id, task_id=task_instance.definition.id)
        if item not in self._known:
            self._items.append(item)
            self._known.add(item)
            self._notify(
                OrchestrationEvent(
                    name="task_ready",
                    workflow_id=workflow.id,
                    task_id=task_instance.definition.id,
                    status=task_instance.status.value,
                    message="Task entered ReadyQueue",
                )
            )
        return item

    def enqueue_from_workflow(self, workflow: WorkflowInstance, task_id: str) -> ReadyQueueItem:
        task_instance = workflow.enqueue_task(task_id)
        return self.enqueue(workflow, task_instance)

    def pop(self) -> ReadyQueueItem | None:
        if not self._items:
            return None
        item = self._items.popleft()
        self._known.discard(item)
        return item

    def remove(self, item: ReadyQueueItem) -> None:
        if item not in self._known:
            return
        self._items = deque(existing for existing in self._items if existing != item)
        self._known.discard(item)

    def contains(self, workflow_id: str, task_id: str) -> bool:
        return ReadyQueueItem(workflow_id=workflow_id, task_id=task_id) in self._known

    def task_ids(self) -> list[str]:
        return [item.task_id for item in self._items]

    def items(self) -> list[ReadyQueueItem]:
        return list(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def _notify(self, event: OrchestrationEvent) -> None:
        for observer in list(self._observers):
            observer.handle(event)
