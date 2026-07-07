"""Embedded logic gates for join decisions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Optional, Sequence, TYPE_CHECKING

from .enums import GateType, TaskStatus

if TYPE_CHECKING:  # pragma: no cover
    from .tasks import Task


@dataclass
class LogicGate:
    """Decides if a target task can start based on predecessor state.

    This implementation keeps external REST/Lambda behavior as deterministic
    mocks because the course assignment only requires demonstrating the concept.
    """

    type: GateType
    depends_on: list["Task"] = field(default_factory=list)
    expression: Optional[str] = None
    endpoint: Optional[str] = None

    def can_start(
        self,
        predecessor_statuses: Mapping[str, TaskStatus],
        variables: Optional[Mapping[str, str]] = None,
    ) -> bool:
        """Evaluate the gate from predecessor task statuses and variables.

        Runtime classes will later adapt TaskInstance/WorkflowInstance to this
        domain-level contract.
        """
        variables = variables or {}
        statuses = [predecessor_statuses.get(task.id) for task in self.depends_on]
        completed = [status == TaskStatus.COMPLETED for status in statuses]

        if self.type == GateType.AND:
            return bool(completed) and all(completed)
        if self.type == GateType.OR:
            return any(completed)
        if self.type == GateType.XOR:
            return sum(1 for is_completed in completed if is_completed) == 1
        if self.type == GateType.COMPLEX:
            return self._evaluate_complex(completed, variables)
        if self.type == GateType.SCRIPT:
            return self._evaluate_script(variables)
        if self.type in {GateType.REST, GateType.LAMBDA}:
            return self._evaluate_mock_external(variables)
        raise ValueError(f"Unsupported gate type: {self.type}")

    def dependency_ids(self) -> list[str]:
        return [task.id for task in self.depends_on]

    def _evaluate_complex(self, completed: Sequence[bool], variables: Mapping[str, str]) -> bool:
        """Small deterministic DSL for advanced gates.

        Supported examples:
        - expression="2_OF_M" means at least two dependencies completed.
        - expression="ALL_AND_PRICE_APPROVED" combines all dependencies with a variable.
        """
        expression = (self.expression or "").strip().upper()
        if expression.endswith("_OF_M"):
            required = int(expression.split("_", 1)[0])
            return sum(1 for item in completed if item) >= required
        if expression == "ALL_AND_PRICE_APPROVED":
            return bool(completed) and all(completed) and variables.get("price_approved") == "true"
        if expression == "ANY_AND_EVIDENCE_VALID":
            return any(completed) and variables.get("evidence_valid") == "true"
        return bool(completed) and all(completed)

    def _evaluate_script(self, variables: Mapping[str, str]) -> bool:
        expression = (self.expression or "").strip().lower()
        if expression in {"true", "return true", "allow"}:
            return True
        if expression in {"false", "return false", "deny"}:
            return False
        if expression.startswith("var:"):
            key = expression.replace("var:", "", 1)
            return variables.get(key) == "true"
        return False

    def _evaluate_mock_external(self, variables: Mapping[str, str]) -> bool:
        """Mock REST/Lambda decision.

        The endpoint is not called. Runtime can set a variable such as
        mock:http://risk-service/approve=true to emulate external approval.
        """
        if not self.endpoint:
            return False
        return variables.get(f"mock:{self.endpoint}") == "true"
