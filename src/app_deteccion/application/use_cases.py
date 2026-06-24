from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from app_deteccion.application.ports import CaseRepository, EventPublisher
from app_deteccion.domain.entities import CriticalProductCase, PriceAudit
from app_deteccion.domain.enums import CommercialAction, RiskLevel
from app_deteccion.domain.exceptions import DomainValidationError


@dataclass(frozen=True)
class RegisterCaseCommand:
    store: str
    product_name: str
    batch: str
    expiration_date: date
    quantity: int
    current_price: float
    commercial_action: CommercialAction
    new_price: Optional[float] = None
    price_change_approved: bool = False
    price_change_reason: str = ""
    evidence_note: str = ""
    created_by: str = "mercaderista.demo"


class RegisterCriticalProductUseCase:
    def __init__(self, repository: CaseRepository, event_publisher: EventPublisher) -> None:
        self.repository = repository
        self.event_publisher = event_publisher

    def execute(self, command: RegisterCaseCommand) -> CriticalProductCase:
        price_audit = PriceAudit(
            current_price=command.current_price,
            new_price=command.new_price,
            price_change_approved=command.price_change_approved,
            price_change_reason=command.price_change_reason,
        )
        case = CriticalProductCase(
            store=command.store,
            product_name=command.product_name,
            batch=command.batch,
            expiration_date=command.expiration_date,
            quantity=command.quantity,
            commercial_action=command.commercial_action,
            price_audit=price_audit,
            evidence_note=command.evidence_note,
            created_by=command.created_by,
        )
        saved = self.repository.add(case)
        self.event_publisher.publish_many(saved.events)
        return saved


class ValidateCaseBySupervisorUseCase:
    def __init__(self, repository: CaseRepository, event_publisher: EventPublisher) -> None:
        self.repository = repository
        self.event_publisher = event_publisher

    def execute(self, case_id: str, supervisor_user: str) -> CriticalProductCase:
        case = self.repository.get(case_id)
        if case is None:
            raise DomainValidationError("No existe el caso solicitado")
        case.validate_by_supervisor(supervisor_user)
        self.repository.update(case)
        self.event_publisher.publish_many(case.events[-1:])
        return case


class DashboardQuery:
    def __init__(self, repository: CaseRepository, event_publisher: EventPublisher) -> None:
        self.repository = repository
        self.event_publisher = event_publisher

    def execute(self) -> dict:
        cases = self.repository.list_all()
        total_cases = len(cases)
        high_risk_cases = sum(1 for c in cases if c.risk_level == RiskLevel.ALTO)
        medium_risk_cases = sum(1 for c in cases if c.risk_level == RiskLevel.MEDIO)
        low_risk_cases = sum(1 for c in cases if c.risk_level == RiskLevel.BAJO)
        total_financial_value_at_risk = round(sum(c.financial_value_at_risk for c in cases), 2)
        total_intervened_quantity = sum(c.quantity for c in cases)
        price_change_cases = sum(1 for c in cases if c.price_audit.has_price_change)
        unapproved_price_change_cases = sum(
            1 for c in cases if c.price_audit.has_price_change and not c.price_audit.price_change_approved
        )
        total_intervened_value = round(sum(c.intervened_value for c in cases), 2)
        pending_action_cases = sum(1 for c in cases if c.commercial_action == CommercialAction.PENDIENTE)
        validated_cases = sum(1 for c in cases if c.validated_by)
        avg_discount_percent = 0.0
        if price_change_cases:
            avg_discount_percent = round(
                sum(c.price_audit.discount_percent for c in cases if c.price_audit.has_price_change)
                / price_change_cases,
                2,
            )
        actions = {action.value: 0 for action in CommercialAction}
        for case in cases:
            actions[case.commercial_action.value] += 1
        return {
            "fsd_uc": "FSD-UC-001",
            "total_cases": total_cases,
            "high_risk_cases": high_risk_cases,
            "medium_risk_cases": medium_risk_cases,
            "low_risk_cases": low_risk_cases,
            "pending_action_cases": pending_action_cases,
            "validated_cases": validated_cases,
            "total_financial_value_at_risk": total_financial_value_at_risk,
            "total_intervened_quantity": total_intervened_quantity,
            "price_change_cases": price_change_cases,
            "unapproved_price_change_cases": unapproved_price_change_cases,
            "total_intervened_value": total_intervened_value,
            "average_discount_percent": avg_discount_percent,
            "cases_by_action": actions,
            "domain_events_count": len(self.event_publisher.list_all()),
        }


class TraceabilityQuery:
    def execute(self) -> dict:
        return {
            "prd_req": "PRD-REQ-001",
            "fsd_uc": "FSD-UC-001",
            "design_doc": "docs/design/DD-UC-001-registro-producto-critico.md",
            "adr": "docs/adr/ADR-0006-demo-monolito-modular-fastapi-sqlite.md",
            "prompt": "docs/prompts/impl/PR-IMPL-001-registro-producto-critico.md",
            "code": [
                "src/app_deteccion/domain",
                "src/app_deteccion/application",
                "src/app_deteccion/adapters",
                "src/app_deteccion/infrastructure",
            ],
            "tests": ["tests/test_domain.py", "tests/test_application.py", "tests/test_api.py"],
            "dtp": "docs/product/DTP.md",
        }
