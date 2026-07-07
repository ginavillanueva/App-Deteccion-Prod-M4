"""Runtime instances for the App Deteccion Prod BPMN workflow engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from src.domain import (
    CompletionPolicy,
    Incident,
    IncidentType,
    ResetScope,
    ResourceInstance,
    ResourceSpec,
    Role,
    Task,
    TaskStatus,
    Transition,
    TransitionType,
    Worker,
    Workflow,
    WorkflowStatus,
)

from .trace import TraceEntry


TERMINAL_TASK_STATUSES = {TaskStatus.COMPLETED, TaskStatus.CANCELLED, TaskStatus.TIMED_OUT}
RESETTABLE_STATUSES = {
    TaskStatus.READY,
    TaskStatus.ASSIGNED,
    TaskStatus.IN_PROGRESS,
    TaskStatus.COMPLETED,
    TaskStatus.FAILED,
    TaskStatus.TIMED_OUT,
}


@dataclass
class TaskInstance:
    """Runtime state for one Task definition inside one WorkflowInstance."""

    definition: Task
    id: str = field(default_factory=lambda: str(uuid4()))
    status: TaskStatus = TaskStatus.PENDING
    assigned_workers: list[Worker] = field(default_factory=list)
    per_worker_status: dict[Worker, TaskStatus] = field(default_factory=dict)
    resources: list[ResourceInstance] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    ready_at: Optional[datetime] = None
    assigned_at: Optional[datetime] = None
    assign_deadline: Optional[datetime] = None
    complete_deadline: Optional[datetime] = None
    retry_count: dict[str, int] = field(default_factory=dict)
    retries_exhausted: bool = False
    was_reset: bool = False
    reset_count: int = 0
    reset_incident_ref: Optional[Incident] = None

    def enqueue(self, *, now: Optional[datetime] = None) -> None:
        """Move the task to READY and calculate assignment SLA deadline."""
        now = now or datetime.now(timezone.utc)
        if self.status == TaskStatus.PENDING:
            self.status = TaskStatus.READY
            self.ready_at = now
            if self.definition.max_time_to_assign:
                self.assign_deadline = now + self.definition.max_time_to_assign

    def assign_workers(self, workers: list[Worker], *, now: Optional[datetime] = None) -> None:
        """Assign one or more workers respecting the task specialty."""
        if not workers:
            raise ValueError("At least one worker is required")
        for worker in workers:
            if not self._worker_matches(worker):
                raise ValueError(
                    f"Worker {worker.employee_id} type {worker.worker_type.value} cannot execute task "
                    f"{self.definition.id} requiring {self.definition.required_worker_type.value}"
                )
        now = now or datetime.now(timezone.utc)
        self.assigned_workers = list(workers)
        self.per_worker_status = {worker: TaskStatus.ASSIGNED for worker in workers}
        self.status = TaskStatus.ASSIGNED
        self.assigned_at = now
        if self.definition.max_time_to_complete:
            self.complete_deadline = now + self.definition.max_time_to_complete

    def start(self, *, now: Optional[datetime] = None) -> None:
        """Start work after the workflow has evaluated the gate."""
        if self.status not in {TaskStatus.READY, TaskStatus.ASSIGNED}:
            raise ValueError(f"Task {self.definition.id} cannot start from {self.status.value}")
        now = now or datetime.now(timezone.utc)
        if self.status == TaskStatus.READY and not self.assigned_workers:
            # Service/system tasks may be started without a human assignment.
            self.per_worker_status = {}
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = now

    def add_resource(self, resource: ResourceInstance) -> None:
        """Attach or replace a runtime resource by key/type."""
        self.resources = [
            existing
            for existing in self.resources
            if not (existing.key == resource.key and existing.type == resource.type)
        ]
        self.resources.append(resource)

    def assign_resources(self, resources: list[ResourceInstance]) -> None:
        for resource in resources:
            self.add_resource(resource)

    def has_mandatory_resources(self) -> bool:
        """Validate mandatory inputs declared by the task definition."""
        for required in self.definition.required_resources:
            if required.mandatory and not self._has_resource(required):
                return False
        return True

    def complete(self, worker: Optional[Worker] = None, *, now: Optional[datetime] = None) -> bool:
        """Complete one worker contribution and return True when task is completed."""
        if self.status not in {TaskStatus.IN_PROGRESS, TaskStatus.ASSIGNED, TaskStatus.READY}:
            raise ValueError(f"Task {self.definition.id} cannot complete from {self.status.value}")
        if not self.has_mandatory_resources():
            missing = [spec.key for spec in self.definition.required_resources if spec.mandatory and not self._has_resource(spec)]
            raise ValueError(f"Task {self.definition.id} cannot complete; missing mandatory resources: {missing}")

        now = now or datetime.now(timezone.utc)
        self._materialize_produced_resources()

        if self.assigned_workers:
            if worker is None:
                if len(self.assigned_workers) == 1:
                    worker = self.assigned_workers[0]
                else:
                    raise ValueError("worker is required for multi-assigned tasks")
            if worker not in self.per_worker_status:
                raise ValueError(f"Worker {worker.employee_id} is not assigned to task {self.definition.id}")
            self.per_worker_status[worker] = TaskStatus.COMPLETED
            if not self._completion_policy_satisfied():
                self.status = TaskStatus.IN_PROGRESS
                return False

        self.status = TaskStatus.COMPLETED
        self.completed_at = now
        return True

    def reset(self, incident: Incident) -> None:
        """Reset runtime state after a BACKWARD incident."""
        if self.status in RESETTABLE_STATUSES:
            self.status = TaskStatus.PENDING
            self.assigned_workers.clear()
            self.per_worker_status.clear()
            self.resources.clear()
            self.started_at = None
            self.completed_at = None
            self.ready_at = None
            self.assigned_at = None
            self.assign_deadline = None
            self.complete_deadline = None
            self.was_reset = True
            self.reset_count += 1
            self.reset_incident_ref = incident

    def retry_for(self, transition: Transition) -> int:
        """Increase retry counter for a BACKWARD transition and return count."""
        self.retry_count[transition.id] = self.retry_count.get(transition.id, 0) + 1
        return self.retry_count[transition.id]

    def _has_resource(self, spec: ResourceSpec) -> bool:
        return any(resource.key == spec.key and resource.type == spec.type and resource.value != "" for resource in self.resources)

    def _materialize_produced_resources(self) -> None:
        for produced in self.definition.produced_resources:
            if not self._has_resource(produced):
                self.add_resource(ResourceInstance.from_spec(produced, source_task_id=self.definition.id))

    def _completion_policy_satisfied(self) -> bool:
        completed_count = sum(1 for status in self.per_worker_status.values() if status == TaskStatus.COMPLETED)
        total = len(self.assigned_workers)
        policy = self.definition.completion_policy
        if total == 0:
            return True
        if policy == CompletionPolicy.ALL:
            return completed_count == total
        if policy == CompletionPolicy.ANY:
            return completed_count >= 1
        if policy == CompletionPolicy.QUORUM:
            return completed_count >= (self.definition.quorum or total)
        raise ValueError(f"Unsupported completion policy: {policy}")

    def _worker_matches(self, worker: Worker) -> bool:
        if worker.role == Role.ADMIN:
            return True
        return self.definition.required_worker_type is None or worker.worker_type == self.definition.required_worker_type


@dataclass
class WorkflowInstance:
    """Runtime execution of a Workflow definition."""

    definition: Workflow
    id: str = field(default_factory=lambda: str(uuid4()))
    task_instances: dict[str, TaskInstance] = field(init=False)
    current_tasks: list[TaskInstance] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PENDING
    execution_path: list[TraceEntry] = field(default_factory=list)
    incidents: list[Incident] = field(default_factory=list)
    variables: dict[str, str] = field(default_factory=dict)
    iteration: int = 1

    def __post_init__(self) -> None:
        self.definition.validate()
        self.task_instances = {task.id: TaskInstance(definition=task) for task in self.definition.tasks}

    def start(self) -> TaskInstance:
        """Start the workflow instance by enqueueing the start task."""
        if self.status not in {WorkflowStatus.PENDING, WorkflowStatus.SUSPENDED}:
            raise ValueError(f"Workflow cannot start from {self.status.value}")
        self.status = WorkflowStatus.IN_PROGRESS
        start_instance = self.enqueue_task(self.definition.start_task.id)
        self._trace(start_instance.definition.id, start_instance.status, "Workflow started; start task READY")
        return start_instance

    def task(self, task_id: str) -> TaskInstance:
        try:
            return self.task_instances[task_id]
        except KeyError as exc:
            raise KeyError(f"Unknown task id: {task_id}") from exc

    def enqueue_task(self, task_id: str) -> TaskInstance:
        """Put a task in READY if its gate allows it."""
        task_instance = self.task(task_id)
        self._hydrate_required_resources(task_instance)
        if not self.can_start_task(task_id):
            return task_instance
        task_instance.enqueue()
        if task_instance not in self.current_tasks and task_instance.status == TaskStatus.READY:
            self.current_tasks.append(task_instance)
        self._trace(task_id, task_instance.status, "Task enqueued as READY")
        return task_instance

    def assign_task(self, task_id: str, workers: list[Worker]) -> TaskInstance:
        task_instance = self.task(task_id)
        task_instance.assign_workers(workers)
        self._trace(task_id, task_instance.status, "Task assigned", worker_id=workers[0].employee_id)
        return task_instance

    def begin_task(self, task_id: str) -> TaskInstance:
        if not self.can_start_task(task_id):
            raise ValueError(f"Task {task_id} cannot start because its LogicGate is not satisfied")
        task_instance = self.task(task_id)
        task_instance.start()
        self._trace(task_id, task_instance.status, "Task started")
        return task_instance

    def complete_task(
        self,
        task_id: str,
        *,
        worker: Optional[Worker] = None,
        resources: Optional[list[ResourceInstance]] = None,
    ) -> TaskInstance:
        """Complete a task and navigate to its forward targets when applicable."""
        if self.status != WorkflowStatus.IN_PROGRESS:
            raise ValueError(f"Workflow must be IN_PROGRESS to complete tasks; current={self.status.value}")
        task_instance = self.task(task_id)
        if resources:
            task_instance.assign_resources(resources)
        completed = task_instance.complete(worker)
        self._publish_task_resources(task_instance)
        if not completed:
            self._trace(task_id, task_instance.status, "Partial completion recorded for assigned worker", worker_id=worker.employee_id if worker else None)
            return task_instance

        self._trace(task_id, task_instance.status, "Task completed", worker_id=worker.employee_id if worker else None)
        if task_instance in self.current_tasks:
            self.current_tasks.remove(task_instance)

        if task_instance.definition.is_final:
            self.status = WorkflowStatus.COMPLETED
            self._trace(task_id, self.status, "Workflow completed by final task")
            return task_instance

        self.navigate_to_targets(task_id)
        return task_instance

    def navigate_to_targets(self, source_task_id: str) -> list[TaskInstance]:
        """Propagate resources and enqueue all eligible FORWARD targets."""
        source_instance = self.task(source_task_id)
        enqueued: list[TaskInstance] = []
        for target in source_instance.definition.targets:
            target_instance = self.task(target.id)
            self._propagate_resources(source_instance, target_instance)
            if self.can_start_task(target.id):
                target_instance.enqueue()
                if target_instance not in self.current_tasks:
                    self.current_tasks.append(target_instance)
                self._trace(target.id, target_instance.status, f"Navigated FORWARD from {source_task_id}")
                enqueued.append(target_instance)
            else:
                self._trace(target.id, target_instance.status, f"Target waiting for LogicGate after {source_task_id}")
        return enqueued

    def can_start_task(self, task_id: str) -> bool:
        """Evaluate incoming dependencies and embedded LogicGate."""
        task_def = self.task(task_id).definition
        if not task_def.incoming:
            return True
        predecessor_statuses = {
            predecessor.id: self.task(predecessor.id).status for predecessor in task_def.incoming
        }
        if task_def.logic_gate:
            return task_def.logic_gate.can_start(predecessor_statuses, self.variables)
        return all(status == TaskStatus.COMPLETED for status in predecessor_statuses.values())

    def raise_incident(
        self,
        *,
        from_task_id: str,
        to_task_id: str,
        type: IncidentType,
        reason: str,
        raised_by: Worker,
        reset_scope: ResetScope = ResetScope.ALL_DOWNSTREAM,
        reset_targets: Optional[list[str]] = None,
    ) -> Incident:
        """Apply a BACKWARD transition with trace, reset and retry control."""
        from_instance = self.task(from_task_id)
        transition = self._find_backward_transition(from_instance.definition, to_task_id)
        retry_count = from_instance.retry_for(transition)

        selected_reset_targets = [self.task(task_id).definition for task_id in (reset_targets or [])]
        incident = Incident(
            from_task=from_instance.definition,
            to_task=self.task(to_task_id).definition,
            type=type,
            reason=reason,
            raised_by=raised_by,
            iteration=self.iteration,
            reset_scope=reset_scope,
            reset_targets=selected_reset_targets,
        )
        self.incidents.append(incident)
        self._trace(
            from_task_id,
            "INCIDENT",
            f"BACKWARD incident {from_task_id}->{to_task_id}: {reason}",
            worker_id=raised_by.employee_id,
            incident_id=incident.id,
        )

        if retry_count > (transition.max_retries or 0):
            from_instance.retries_exhausted = True
            self.status = transition.exhausted_status
            self._trace(
                from_task_id,
                self.status,
                f"Retries exhausted for transition {from_task_id}->{to_task_id}; workflow moved to {self.status.value}",
                worker_id=raised_by.employee_id,
                incident_id=incident.id,
            )
            return incident

        self.iteration += 1
        for task_id in self._resolve_reset_task_ids(to_task_id, reset_scope, reset_targets or []):
            instance = self.task(task_id)
            instance.reset(incident)
            self._trace(task_id, instance.status, "Task reset by incident", incident_id=incident.id, was_reset=True)

        self.current_tasks = []
        resumed = self.enqueue_task(to_task_id)
        if resumed.status == TaskStatus.READY and resumed not in self.current_tasks:
            self.current_tasks.append(resumed)
        return incident

    def timed_out_tasks(self, *, now: Optional[datetime] = None) -> list[TaskInstance]:
        """Reactive SLA check; caller/orchestrator invokes it when events occur."""
        now = now or datetime.now(timezone.utc)
        timed_out: list[TaskInstance] = []
        for task_instance in self.task_instances.values():
            deadline = None
            if task_instance.status == TaskStatus.READY:
                deadline = task_instance.assign_deadline
            elif task_instance.status in {TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS}:
                deadline = task_instance.complete_deadline
            if deadline and now > deadline:
                task_instance.status = TaskStatus.TIMED_OUT
                timed_out.append(task_instance)
                self._trace(task_instance.definition.id, task_instance.status, "SLA deadline breached")
        return timed_out

    def _find_backward_transition(self, from_task: Task, to_task_id: str) -> Transition:
        for transition in from_task.backward_transitions:
            if transition.type == TransitionType.BACKWARD and transition.target.id == to_task_id:
                return transition
        raise ValueError(f"No BACKWARD transition from {from_task.id} to {to_task_id}")

    def _resolve_reset_task_ids(self, to_task_id: str, reset_scope: ResetScope, reset_targets: list[str]) -> set[str]:
        if reset_scope == ResetScope.SPECIFIC:
            return set(reset_targets)
        return self.definition.dependency_matrix.reachable_from(to_task_id)

    def _publish_task_resources(self, task_instance: TaskInstance) -> None:
        for resource in task_instance.resources:
            self.variables[resource.key] = resource.value

    def _hydrate_required_resources(self, task_instance: TaskInstance) -> None:
        for spec in task_instance.definition.required_resources:
            if spec.key in self.variables and not any(
                resource.key == spec.key and resource.type == spec.type for resource in task_instance.resources
            ):
                task_instance.add_resource(
                    ResourceInstance(
                        key=spec.key,
                        value=self.variables[spec.key],
                        type=spec.type,
                        source_task_id="workflow_variables",
                        mandatory=spec.mandatory,
                        propagate=False,
                    )
                )

    def _propagate_resources(self, source: TaskInstance, target: TaskInstance) -> None:
        for resource in source.resources:
            if not resource.propagate:
                continue
            for required in target.definition.required_resources:
                if resource.key == required.key and resource.type == required.type:
                    target.add_resource(
                        ResourceInstance(
                            key=resource.key,
                            value=resource.value,
                            type=resource.type,
                            source_task_id=source.definition.id,
                            mandatory=required.mandatory,
                            propagate=False,
                        )
                    )
        self._hydrate_required_resources(target)

    def _trace(
        self,
        task_id: str,
        status: TaskStatus | WorkflowStatus | str,
        message: str,
        *,
        worker_id: Optional[str] = None,
        incident_id: Optional[str] = None,
        was_reset: bool = False,
    ) -> None:
        self.execution_path.append(
            TraceEntry(
                task_id=task_id,
                status=status,
                message=message,
                worker_id=worker_id,
                incident_id=incident_id,
                iteration=self.iteration,
                was_reset=was_reset,
            )
        )
