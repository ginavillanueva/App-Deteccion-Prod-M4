"""Enumerations for the App Deteccion Prod BPMN workflow engine domain model.

The object model intentionally uses English names, as required by the course
assignment, while the surrounding documentation remains in Spanish.
"""

from __future__ import annotations

from enum import Enum


class WorkflowStatus(Enum):
    """Lifecycle states for a workflow definition or workflow instance."""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SUSPENDED = "SUSPENDED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    ERROR = "ERROR"


class TaskStatus(Enum):
    """Lifecycle states for a runtime task instance."""

    PENDING = "PENDING"
    READY = "READY"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    CANCELLED = "CANCELLED"


class GateType(Enum):
    """Supported embedded join gate types."""

    AND = "AND"
    OR = "OR"
    XOR = "XOR"
    COMPLEX = "COMPLEX"
    SCRIPT = "SCRIPT"
    REST = "REST"
    LAMBDA = "LAMBDA"


class ResourceType(Enum):
    """Resource categories handled by tasks."""

    FILE = "FILE"
    TEXT = "TEXT"
    URL = "URL"
    NUMBER = "NUMBER"
    MONEY = "MONEY"
    BOOLEAN = "BOOLEAN"
    OTHER = "OTHER"


class TaskType(Enum):
    """BPMN-inspired task categories."""

    HUMAN = "HUMAN"
    SERVICE = "SERVICE"
    SCRIPT = "SCRIPT"
    DECISION = "DECISION"
    START = "START"
    END = "END"


class Role(Enum):
    """Access role for a worker."""

    WORKER = "WORKER"
    ADMIN = "ADMIN"


class WorkerType(Enum):
    """Business specialties used for skill-based assignment."""

    MERCHANDISER = "MERCHANDISER"
    SUPERVISOR = "SUPERVISOR"
    SELLER = "SELLER"
    MANAGER = "MANAGER"
    SYSTEM_AI = "SYSTEM_AI"
    ADMIN = "ADMIN"


class TransitionType(Enum):
    """Typed graph edge."""

    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"


class IncidentType(Enum):
    """Reasons that explain a backward transition / rework."""

    QUALITY = "QUALITY"
    VALIDATION = "VALIDATION"
    MISSING_RESOURCE = "MISSING_RESOURCE"
    BUSINESS_RULE = "BUSINESS_RULE"
    PRICE_MISMATCH = "PRICE_MISMATCH"
    EVIDENCE_INCOMPLETE = "EVIDENCE_INCOMPLETE"
    OTHER = "OTHER"


class CompletionPolicy(Enum):
    """How a task with multiple assigned workers becomes completed."""

    ALL = "ALL"
    ANY = "ANY"
    QUORUM = "QUORUM"


class ResetScope(Enum):
    """Scope applied when a backward incident resets already advanced work."""

    ALL_DOWNSTREAM = "ALL_DOWNSTREAM"
    SPECIFIC = "SPECIFIC"
