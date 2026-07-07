"""Observer events for the App Deteccion Prod BPMN workflow engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol


@dataclass(frozen=True)
class OrchestrationEvent:
    """Immutable event emitted by the ready queue and orchestrator.

    The event is intentionally small: it gives enough information to audit the
    runtime path without coupling observers to a specific UI, database or cloud
    provider. This keeps the design close to AWS SQS / Job Executor semantics.
    """

    name: str
    workflow_id: str
    task_id: str
    status: str
    message: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class OrchestrationObserver(Protocol):
    """Observer contract used by ReadyQueue and Orchestrator."""

    def handle(self, event: OrchestrationEvent) -> None:
        """React to an orchestration event."""


class InMemoryEventLog:
    """Simple observer used in tests and demos to keep an auditable event list."""

    def __init__(self) -> None:
        self.events: list[OrchestrationEvent] = []

    def handle(self, event: OrchestrationEvent) -> None:
        self.events.append(event)

    def names(self) -> list[str]:
        return [event.name for event in self.events]
