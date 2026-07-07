"""Resource specifications and runtime resource values."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .enums import ResourceType


@dataclass(frozen=True)
class ResourceSpec:
    """Resource required or produced by a task definition.

    In App Deteccion Prod, typical resources are product photo, expiration date,
    current price, proposed price, quantity, commercial action and approval
    evidence.
    """

    key: str
    value: str
    type: ResourceType
    mandatory: bool = False
    propagate: bool = False

    def matches(self, other: "ResourceSpec") -> bool:
        """Return True when two resource specs can be matched for propagation."""
        return self.key == other.key and self.type == other.type


@dataclass
class ResourceInstance:
    """Concrete runtime value attached to a task execution."""

    key: str
    value: str
    type: ResourceType
    source_task_id: Optional[str] = None
    mandatory: bool = False
    propagate: bool = False

    @classmethod
    def from_spec(cls, spec: ResourceSpec, *, source_task_id: Optional[str] = None) -> "ResourceInstance":
        return cls(
            key=spec.key,
            value=spec.value,
            type=spec.type,
            source_task_id=source_task_id,
            mandatory=spec.mandatory,
            propagate=spec.propagate,
        )
