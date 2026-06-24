from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(frozen=True)
class DomainEvent:
    name: str
    aggregate_id: str
    payload: dict
    id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "aggregate_id": self.aggregate_id,
            "payload": self.payload,
            "occurred_at": self.occurred_at.isoformat(),
        }
