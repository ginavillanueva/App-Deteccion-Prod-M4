from __future__ import annotations

from dataclasses import dataclass

from app_deteccion.domain.enums import RiskLevel


@dataclass(frozen=True)
class RiskAssessment:
    score: int
    level: RiskLevel
    reasons: tuple[str, ...]
    sla_hours: int

    def to_dict(self) -> dict:
        return {
            "score": self.score,
            "level": self.level.value,
            "reasons": list(self.reasons),
            "sla_hours": self.sla_hours,
        }


class RiskScorer:
    """Deterministic, auditable scoring for demo and defense.

    The score is intentionally explainable. It does not approve prices or discounts.
    It only classifies operational priority.
    """

    @staticmethod
    def classify(
        *,
        days_to_expiration: int,
        financial_value_at_risk: float,
        has_commercial_action: bool,
        evidence_present: bool,
        has_price_change: bool,
        price_change_approved: bool,
        intervened_value: float,
    ) -> RiskAssessment:
        score = 0
        reasons: list[str] = []

        if days_to_expiration <= 30:
            score += 35
            reasons.append("Vencimiento crítico: 30 días o menos")
        elif days_to_expiration <= 45:
            score += 28
            reasons.append("Vencimiento alto: 45 días o menos")
        elif days_to_expiration <= 90:
            score += 30
            reasons.append("Vencimiento medio: 90 días o menos")

        if financial_value_at_risk >= 3000:
            score += 25
            reasons.append("Valor financiero en riesgo alto")
        elif financial_value_at_risk >= 1000:
            score += 15
            reasons.append("Valor financiero en riesgo medio")

        if not has_commercial_action:
            score += 25
            reasons.append("No existe acción comercial registrada")

        if not evidence_present:
            score += 12
            reasons.append("Evidencia operativa incompleta")

        if has_price_change and not price_change_approved:
            score += 20
            reasons.append("Cambio de precio sin aprobación")

        if intervened_value >= 1000:
            score += 12
            reasons.append("Valor económico intervenido significativo")

        critical_rule = (
            (days_to_expiration <= 45 and not has_commercial_action)
            or (has_price_change and not price_change_approved and intervened_value >= 1000)
            or (days_to_expiration <= 30 and not evidence_present)
        )

        if critical_rule or score >= 60:
            return RiskAssessment(score=score, level=RiskLevel.ALTO, reasons=tuple(reasons), sla_hours=24)
        if score >= 30:
            return RiskAssessment(score=score, level=RiskLevel.MEDIO, reasons=tuple(reasons), sla_hours=48)
        if not reasons:
            reasons.append("Caso monitoreable sin urgencia inmediata")
        return RiskAssessment(score=score, level=RiskLevel.BAJO, reasons=tuple(reasons), sla_hours=120)
