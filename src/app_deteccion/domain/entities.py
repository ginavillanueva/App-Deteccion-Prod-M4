from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import uuid4

from app_deteccion.domain.enums import CaseStatus, CommercialAction, RiskLevel
from app_deteccion.domain.events import DomainEvent
from app_deteccion.domain.exceptions import DomainValidationError
from app_deteccion.domain.guardrails import validate_human_note_is_safe
from app_deteccion.domain.scoring import RiskAssessment, RiskScorer


@dataclass(frozen=True)
class PriceAudit:
    current_price: float
    new_price: Optional[float] = None
    price_change_approved: bool = False
    price_change_reason: str = ""

    def __post_init__(self) -> None:
        if self.current_price <= 0:
            raise DomainValidationError("El precio actual debe ser mayor a 0")
        if self.new_price is not None and self.new_price <= 0:
            raise DomainValidationError("El precio nuevo debe ser mayor a 0 cuando se informa")
        validate_human_note_is_safe(self.price_change_reason)

    @property
    def has_price_change(self) -> bool:
        return self.new_price is not None and self.new_price != self.current_price

    @property
    def price_difference(self) -> float:
        if not self.has_price_change or self.new_price is None:
            return 0.0
        return round(self.current_price - self.new_price, 2)

    @property
    def discount_percent(self) -> float:
        if not self.has_price_change:
            return 0.0
        return round((self.price_difference / self.current_price) * 100, 2)

    def to_dict(self) -> dict:
        return {
            "current_price": self.current_price,
            "new_price": self.new_price,
            "price_change_approved": self.price_change_approved,
            "price_change_reason": self.price_change_reason,
            "has_price_change": self.has_price_change,
            "price_difference": self.price_difference,
            "discount_percent": self.discount_percent,
        }


@dataclass
class CriticalProductCase:
    store: str
    product_name: str
    batch: str
    expiration_date: date
    quantity: int
    commercial_action: CommercialAction
    price_audit: PriceAudit
    evidence_note: str = ""
    created_by: str = "mercaderista.demo"
    created_at: date = field(default_factory=date.today)
    id: str = field(default_factory=lambda: str(uuid4()))
    status: CaseStatus = CaseStatus.REGISTRADO
    risk: RiskAssessment = field(init=False)
    events: list[DomainEvent] = field(default_factory=list, init=False)
    validated_by: Optional[str] = None

    def __post_init__(self) -> None:
        self._required("store", self.store)
        self._required("product_name", self.product_name)
        self._required("batch", self.batch)
        self._required("created_by", self.created_by)
        if self.quantity <= 0:
            raise DomainValidationError("La cantidad debe ser mayor a 0")
        validate_human_note_is_safe(self.evidence_note)
        self.risk = self._calculate_risk()
        self._record_creation_events()

    @staticmethod
    def _required(field_name: str, value: str) -> None:
        if value is None or not str(value).strip():
            raise DomainValidationError(f"{field_name} es obligatorio")

    @property
    def days_to_expiration(self) -> int:
        return (self.expiration_date - self.created_at).days

    @property
    def has_commercial_action(self) -> bool:
        return self.commercial_action != CommercialAction.PENDIENTE

    @property
    def evidence_present(self) -> bool:
        return bool(self.evidence_note and self.evidence_note.strip())

    @property
    def financial_value_at_risk(self) -> float:
        return round(self.quantity * self.price_audit.current_price, 2)

    @property
    def intervened_value(self) -> float:
        if not self.price_audit.has_price_change:
            return 0.0
        return round(abs(self.price_audit.price_difference) * self.quantity, 2)

    @property
    def risk_level(self) -> RiskLevel:
        return self.risk.level

    def _calculate_risk(self) -> RiskAssessment:
        return RiskScorer.classify(
            days_to_expiration=self.days_to_expiration,
            financial_value_at_risk=self.financial_value_at_risk,
            has_commercial_action=self.has_commercial_action,
            evidence_present=self.evidence_present,
            has_price_change=self.price_audit.has_price_change,
            price_change_approved=self.price_audit.price_change_approved,
            intervened_value=self.intervened_value,
        )

    def _record_creation_events(self) -> None:
        self.events.append(
            DomainEvent(
                name="ProductCaseRegistered.v1",
                aggregate_id=self.id,
                payload={
                    "fsd_uc": "FSD-UC-001",
                    "store": self.store,
                    "product_name": self.product_name,
                    "risk_level": self.risk.level.value,
                },
            )
        )
        if self.price_audit.has_price_change:
            self.events.append(
                DomainEvent(
                    name="PriceChanged.v1",
                    aggregate_id=self.id,
                    payload={
                        "current_price": self.price_audit.current_price,
                        "new_price": self.price_audit.new_price,
                        "approved": self.price_audit.price_change_approved,
                        "intervened_value": self.intervened_value,
                    },
                )
            )
        self.events.append(
            DomainEvent(
                name="CaseRiskClassified.v1",
                aggregate_id=self.id,
                payload=self.risk.to_dict(),
            )
        )

    def validate_by_supervisor(self, supervisor_user: str) -> None:
        self._required("supervisor_user", supervisor_user)
        self.status = CaseStatus.VALIDADO_SUPERVISOR
        self.validated_by = supervisor_user
        self.events.append(
            DomainEvent(
                name="CaseValidatedBySupervisor.v1",
                aggregate_id=self.id,
                payload={"validated_by": supervisor_user, "status": self.status.value},
            )
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "fsd_uc": "FSD-UC-001",
            "store": self.store,
            "product_name": self.product_name,
            "batch": self.batch,
            "expiration_date": self.expiration_date.isoformat(),
            "quantity": self.quantity,
            "commercial_action": self.commercial_action.value,
            "evidence_note": self.evidence_note,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "days_to_expiration": self.days_to_expiration,
            "financial_value_at_risk": self.financial_value_at_risk,
            "intervened_value": self.intervened_value,
            "price_audit": self.price_audit.to_dict(),
            "risk": self.risk.to_dict(),
            "risk_level": self.risk.level.value,
            "status": self.status.value,
            "validated_by": self.validated_by,
            "events": [event.to_dict() for event in self.events],
        }
