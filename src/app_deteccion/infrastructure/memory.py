from __future__ import annotations

from app_deteccion.domain.entities import CriticalProductCase
from app_deteccion.domain.events import DomainEvent


class InMemoryCaseRepository:
    def __init__(self) -> None:
        self._cases: dict[str, CriticalProductCase] = {}

    def add(self, case: CriticalProductCase) -> CriticalProductCase:
        self._cases[case.id] = case
        return case

    def update(self, case: CriticalProductCase) -> CriticalProductCase:
        self._cases[case.id] = case
        return case

    def get(self, case_id: str) -> CriticalProductCase | None:
        return self._cases.get(case_id)

    def list_all(self) -> list[CriticalProductCase]:
        return list(self._cases.values())

    def clear(self) -> None:
        self._cases.clear()


class InMemoryEventPublisher:
    def __init__(self) -> None:
        self._events: list[DomainEvent] = []

    def publish_many(self, events: list[DomainEvent]) -> None:
        self._events.extend(events)

    def list_all(self) -> list[DomainEvent]:
        return list(self._events)

    def clear(self) -> None:
        self._events.clear()
