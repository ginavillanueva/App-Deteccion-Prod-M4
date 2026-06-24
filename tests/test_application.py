from datetime import date, timedelta

import pytest

from app_deteccion.application.use_cases import (
    DashboardQuery,
    RegisterCaseCommand,
    RegisterCriticalProductUseCase,
    TraceabilityQuery,
    ValidateCaseBySupervisorUseCase,
)
from app_deteccion.domain.enums import CommercialAction
from app_deteccion.domain.exceptions import DomainValidationError
from app_deteccion.infrastructure.memory import InMemoryCaseRepository, InMemoryEventPublisher


def setup_use_case():
    repo = InMemoryCaseRepository()
    publisher = InMemoryEventPublisher()
    return repo, publisher, RegisterCriticalProductUseCase(repo, publisher)


def command(**overrides):
    data = {
        "store": "Farmacorp Centro",
        "product_name": "Crema Facial",
        "batch": "B-100",
        "expiration_date": date.today() + timedelta(days=30),
        "quantity": 5,
        "current_price": 80.0,
        "new_price": 65.0,
        "price_change_approved": True,
        "price_change_reason": "Descuento autorizado por rotación",
        "commercial_action": CommercialAction.DESCUENTO,
        "evidence_note": "Evidencia OK",
        "created_by": "mercaderista.demo",
    }
    data.update(overrides)
    return RegisterCaseCommand(**data)


def test_register_use_case_persists_case_and_events():
    repo, publisher, use_case = setup_use_case()
    case = use_case.execute(command())
    assert repo.get(case.id) == case
    assert len(repo.list_all()) == 1
    assert len(publisher.list_all()) == 3


def test_dashboard_query_summarizes_cases():
    repo, publisher, use_case = setup_use_case()
    use_case.execute(command(quantity=20, current_price=10.0, new_price=None, commercial_action=CommercialAction.PENDIENTE))
    use_case.execute(command(expiration_date=date.today() + timedelta(days=120), quantity=10, current_price=5.0, new_price=4.0))
    dashboard = DashboardQuery(repo, publisher).execute()
    assert dashboard["total_cases"] == 2
    assert dashboard["high_risk_cases"] == 1
    assert dashboard["price_change_cases"] == 1
    assert dashboard["total_financial_value_at_risk"] == 250.0
    assert dashboard["total_intervened_quantity"] == 30
    assert dashboard["total_intervened_value"] == 10.0
    assert dashboard["domain_events_count"] == 5


def test_validate_case_by_supervisor():
    repo, publisher, use_case = setup_use_case()
    case = use_case.execute(command())
    validated = ValidateCaseBySupervisorUseCase(repo, publisher).execute(case.id, "supervisor.demo")
    assert validated.validated_by == "supervisor.demo"
    assert DashboardQuery(repo, publisher).execute()["validated_cases"] == 1


def test_validate_missing_case_raises_error():
    repo = InMemoryCaseRepository()
    publisher = InMemoryEventPublisher()
    with pytest.raises(DomainValidationError):
        ValidateCaseBySupervisorUseCase(repo, publisher).execute("missing", "supervisor.demo")


def test_traceability_query_has_all_artifacts():
    trace = TraceabilityQuery().execute()
    assert trace["fsd_uc"] == "FSD-UC-001"
    assert "DD-UC-001" in trace["design_doc"]
    assert "PR-IMPL-001" in trace["prompt"]


def test_repository_and_publisher_clear():
    repo, publisher, use_case = setup_use_case()
    use_case.execute(command())
    repo.clear()
    publisher.clear()
    assert repo.list_all() == []
    assert publisher.list_all() == []
