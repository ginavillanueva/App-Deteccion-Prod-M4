from __future__ import annotations

from datetime import date
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

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
from app_deteccion.adapters.web_ui import router as demo_ui_router


class RegisterCaseRequest(BaseModel):
    store: str = Field(..., min_length=1)
    product_name: str = Field(..., min_length=1)
    batch: str = Field(..., min_length=1)
    expiration_date: date
    quantity: int = Field(..., gt=0)
    current_price: float = Field(..., gt=0)
    new_price: Optional[float] = Field(default=None, gt=0)
    commercial_action: CommercialAction
    price_change_approved: bool = False
    price_change_reason: str = ""
    evidence_note: str = ""
    evidence_photo_name: str = ""
    evidence_photo_data: str = ""
    created_by: str = "mercaderista.demo"


class ValidateCaseRequest(BaseModel):
    supervisor_user: str = Field(..., min_length=1)
    decision: str = "APROBADO"
    comment: str = ""


def create_app(repository=None, event_publisher=None) -> FastAPI:
    repo = repository or InMemoryCaseRepository()
    publisher = event_publisher or InMemoryEventPublisher()

    app = FastAPI(
        title="App Detección Prod — FSD-UC-001",
        version="0.2.0",
        description="Vertical slice trazable: registro, precio, scoring, eventos y dashboard.",
    )

    app.include_router(demo_ui_router)

    @app.get("/")
    def root():
        return RedirectResponse(url="/app")

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "feature": "FSD-UC-001", "coverage_rule": ">=90%"}

    @app.post("/cases")
    def register_case(payload: RegisterCaseRequest) -> dict:
        try:
            command = RegisterCaseCommand(**payload.model_dump())
            case = RegisterCriticalProductUseCase(repo, publisher).execute(command)
            return {"message": "Caso registrado con trazabilidad FSD-UC-001", "case": case.to_dict()}
        except DomainValidationError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/cases")
    def list_cases() -> dict:
        return {"cases": [case.to_dict() for case in repo.list_all()]}

    @app.get("/cases/{case_id}")
    def get_case(case_id: str) -> dict:
        case = repo.get(case_id)
        if case is None:
            raise HTTPException(status_code=404, detail="Caso no encontrado")
        return {"case": case.to_dict()}

    @app.patch("/cases/{case_id}/validate")
    def validate_case(case_id: str, payload: ValidateCaseRequest) -> dict:
        try:
            case = ValidateCaseBySupervisorUseCase(repo, publisher).execute(
                case_id=case_id,
                supervisor_user=payload.supervisor_user,
                decision=payload.decision,
                comment=payload.comment,
            )
            return {"message": "Caso validado por supervisor", "case": case.to_dict()}
        except DomainValidationError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/dashboard")
    def dashboard() -> dict:
        return DashboardQuery(repo, publisher).execute()

    @app.get("/events")
    def events() -> dict:
        return {"events": [event.to_dict() for event in publisher.list_all()]}

    @app.get("/traceability")
    def traceability() -> dict:
        return TraceabilityQuery().execute()

    @app.delete("/cases/reset")
    def reset_demo() -> dict:
        repo.clear()
        publisher.clear()
        return {"message": "Demo reiniciada"}

    return app
