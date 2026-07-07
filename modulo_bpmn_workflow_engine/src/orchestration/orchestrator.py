"""Observer-based orchestrator for workflow execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from src.domain import ResourceInstance, TaskStatus, Worker, WorkflowStatus
from src.runtime import TaskInstance, WorkflowInstance

from .assignment import Assignment, WorkerPool
from .events import OrchestrationEvent, OrchestrationObserver
from .queue import ReadyQueue, ReadyQueueItem


@dataclass
class Orchestrator(OrchestrationObserver):
    """Assigns workers and reacts to queue/runtime events.

    The orchestrator intentionally avoids cron. It reacts when tasks enter the
    ReadyQueue, when a task is assigned/completed, or when the caller asks for a
    reactive SLA check after a business event.
    """

    ready_queue: ReadyQueue
    worker_pool: WorkerPool
    events: list[OrchestrationEvent] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.ready_queue.subscribe(self)

    def handle(self, event: OrchestrationEvent) -> None:
        self.events.append(event)

    def submit_workflow(self, workflow: WorkflowInstance) -> TaskInstance:
        """Start a workflow and enqueue its start task."""
        start_instance = workflow.start()
        self.ready_queue.enqueue(workflow, start_instance)
        self._emit(
            name="workflow_submitted",
            workflow=workflow,
            task_id=start_instance.definition.id,
            status=workflow.status.value,
            message="Workflow submitted to orchestrator",
        )
        return start_instance

    def assign_next(self, workflow_registry: dict[str, WorkflowInstance]) -> Assignment | None:
        """Pop one READY item and assign the best worker."""
        item = self.ready_queue.pop()
        if item is None:
            return None
        workflow = workflow_registry[item.workflow_id]
        task_instance = workflow.task(item.task_id)
        if task_instance.status != TaskStatus.READY:
            self._emit(
                name="task_skipped_not_ready",
                workflow=workflow,
                task_id=item.task_id,
                status=task_instance.status.value,
                message="Queue item skipped because task is no longer READY",
            )
            return None

        assignment = self.worker_pool.select_worker(task_instance)
        workflow.assign_task(item.task_id, [assignment.worker])
        self.worker_pool.mark_assigned(workflow.id, task_instance, assignment.worker)
        self._emit(
            name="task_assigned",
            workflow=workflow,
            task_id=item.task_id,
            status=task_instance.status.value,
            message=f"Task assigned to {assignment.worker.employee_id}",
            payload={
                "worker_id": assignment.worker.employee_id,
                "worker_type": assignment.worker.worker_type.value,
                "policy": assignment.reason,
                "active_assignments_before": assignment.active_assignments_before,
            },
        )
        return assignment

    def assign_all_ready(self, workflow_registry: dict[str, WorkflowInstance]) -> list[Assignment]:
        assignments: list[Assignment] = []
        while len(self.ready_queue) > 0:
            assignment = self.assign_next(workflow_registry)
            if assignment is not None:
                assignments.append(assignment)
        return assignments

    def start_assigned_task(self, workflow: WorkflowInstance, task_id: str) -> TaskInstance:
        task_instance = workflow.begin_task(task_id)
        self._emit(
            name="task_started",
            workflow=workflow,
            task_id=task_id,
            status=task_instance.status.value,
            message="Assigned task moved to IN_PROGRESS",
        )
        return task_instance

    def complete_task(
        self,
        workflow: WorkflowInstance,
        task_id: str,
        *,
        worker: Optional[Worker] = None,
        resources: Optional[list[ResourceInstance]] = None,
        auto_start: bool = True,
    ) -> TaskInstance:
        """Complete a task and enqueue newly READY targets.

        The runtime owns the actual state transition and graph navigation. The
        orchestrator adds worker accounting, event emission and queue hydration.
        """
        task_instance = workflow.task(task_id)
        if auto_start and task_instance.status in {TaskStatus.READY, TaskStatus.ASSIGNED}:
            workflow.begin_task(task_id)
            self._emit(
                name="task_started",
                workflow=workflow,
                task_id=task_id,
                status=workflow.task(task_id).status.value,
                message="Task auto-started before completion",
            )

        completed_instance = workflow.complete_task(task_id, worker=worker, resources=resources)
        if worker is not None and completed_instance.status == TaskStatus.COMPLETED:
            self.worker_pool.mark_completed(workflow.id, task_id, worker)

        self._emit(
            name="task_completed" if completed_instance.status == TaskStatus.COMPLETED else "task_partially_completed",
            workflow=workflow,
            task_id=task_id,
            status=completed_instance.status.value,
            message="Task completion processed by orchestrator",
            payload={"worker_id": worker.employee_id if worker else None},
        )
        self.enqueue_current_ready_tasks(workflow)
        return completed_instance

    def enqueue_current_ready_tasks(self, workflow: WorkflowInstance) -> list[ReadyQueueItem]:
        """Put all current READY tasks into ReadyQueue, avoiding duplicates."""
        items: list[ReadyQueueItem] = []
        if workflow.status != WorkflowStatus.IN_PROGRESS:
            return items
        for task_instance in workflow.current_tasks:
            if task_instance.status == TaskStatus.READY and not self.ready_queue.contains(workflow.id, task_instance.definition.id):
                items.append(self.ready_queue.enqueue(workflow, task_instance))
        return items

    def check_sla(self, workflow: WorkflowInstance) -> list[TaskInstance]:
        """Reactive SLA check invoked after events, not by cron."""
        breached = workflow.timed_out_tasks()
        for task_instance in breached:
            self._emit(
                name="sla_breached",
                workflow=workflow,
                task_id=task_instance.definition.id,
                status=task_instance.status.value,
                message="Task breached assignment/completion SLA",
            )
        return breached

    def _emit(
        self,
        *,
        name: str,
        workflow: WorkflowInstance,
        task_id: str,
        status: str,
        message: str,
        payload: Optional[dict] = None,
    ) -> None:
        self.handle(
            OrchestrationEvent(
                name=name,
                workflow_id=workflow.id,
                task_id=task_id,
                status=status,
                message=message,
                payload=payload or {},
            )
        )
