"""Factory for the App Deteccion Prod reference workflow definition."""

from __future__ import annotations

from datetime import timedelta

from .enums import GateType, ResourceType, TaskType, WorkerType
from .gates import LogicGate
from .resources import ResourceSpec
from .tasks import Task
from .workflow import Workflow


def build_app_deteccion_workflow() -> Workflow:
    """Build the reference process used throughout the documentation.

    Process summary:
    DetectProductCase -> ValidateEvidence -> {ClassifyRisk, ValidatePriceData}
    -> DecideCommercialAction -> ApprovePriceChange -> ExecuteRetailAction
    -> SupervisorReview -> CloseCaseAndUpdateDashboard
    """

    detect = Task(
        id="detect_product_case",
        name="Detect product near expiration",
        task_type=TaskType.START,
        required_worker_type=WorkerType.MERCHANDISER,
        produced_resources=[
            ResourceSpec("product_photo", "photo-url", ResourceType.FILE, mandatory=True, propagate=True),
            ResourceSpec("expiration_date", "YYYY-MM-DD", ResourceType.TEXT, mandatory=True, propagate=True),
            ResourceSpec("current_price", "0.00", ResourceType.MONEY, mandatory=True, propagate=True),
            ResourceSpec("quantity", "0", ResourceType.NUMBER, mandatory=True, propagate=True),
        ],
        max_time_to_complete=timedelta(hours=4),
    )

    validate = Task(
        id="validate_evidence",
        name="Validate evidence and product data",
        required_worker_type=WorkerType.SUPERVISOR,
        required_resources=[
            ResourceSpec("product_photo", "photo-url", ResourceType.FILE, mandatory=True),
            ResourceSpec("expiration_date", "YYYY-MM-DD", ResourceType.TEXT, mandatory=True),
        ],
        produced_resources=[ResourceSpec("evidence_valid", "true", ResourceType.BOOLEAN, mandatory=True, propagate=True)],
        max_time_to_assign=timedelta(hours=8),
        max_time_to_complete=timedelta(hours=24),
    )

    classify = Task(
        id="classify_risk",
        name="Classify expiration and financial risk",
        task_type=TaskType.SERVICE,
        required_worker_type=WorkerType.SYSTEM_AI,
        required_resources=[
            ResourceSpec("expiration_date", "YYYY-MM-DD", ResourceType.TEXT, mandatory=True),
            ResourceSpec("quantity", "0", ResourceType.NUMBER, mandatory=True),
        ],
        produced_resources=[ResourceSpec("risk_level", "MEDIUM", ResourceType.TEXT, mandatory=True, propagate=True)],
    )

    validate_price = Task(
        id="validate_price_data",
        name="Validate current price and proposed price data",
        required_worker_type=WorkerType.SELLER,
        required_resources=[ResourceSpec("current_price", "0.00", ResourceType.MONEY, mandatory=True)],
        produced_resources=[ResourceSpec("price_data_valid", "true", ResourceType.BOOLEAN, mandatory=True, propagate=True)],
    )

    decide = Task(
        id="decide_commercial_action",
        name="Decide discount, bundle, withdrawal or monitoring action",
        task_type=TaskType.DECISION,
        required_worker_type=WorkerType.SELLER,
        logic_gate=LogicGate(type=GateType.AND, depends_on=[classify, validate_price]),
        required_resources=[
            ResourceSpec("risk_level", "MEDIUM", ResourceType.TEXT, mandatory=True),
            ResourceSpec("price_data_valid", "true", ResourceType.BOOLEAN, mandatory=True),
        ],
        produced_resources=[ResourceSpec("commercial_action", "DISCOUNT", ResourceType.TEXT, mandatory=True, propagate=True)],
    )

    approve_price = Task(
        id="approve_price_change",
        name="Approve price change if commercial action requires it",
        required_worker_type=WorkerType.MANAGER,
        required_resources=[ResourceSpec("commercial_action", "DISCOUNT", ResourceType.TEXT, mandatory=True)],
        produced_resources=[ResourceSpec("price_approved", "true", ResourceType.BOOLEAN, mandatory=True, propagate=True)],
    )

    execute = Task(
        id="execute_retail_action",
        name="Execute retail action in store",
        required_worker_type=WorkerType.MERCHANDISER,
        logic_gate=LogicGate(type=GateType.COMPLEX, depends_on=[approve_price], expression="ALL_AND_PRICE_APPROVED"),
        required_resources=[ResourceSpec("price_approved", "true", ResourceType.BOOLEAN, mandatory=True)],
        produced_resources=[ResourceSpec("execution_evidence", "photo-url", ResourceType.FILE, mandatory=True, propagate=True)],
    )

    review = Task(
        id="supervisor_review",
        name="Review execution evidence and close decision",
        required_worker_type=WorkerType.SUPERVISOR,
        required_resources=[ResourceSpec("execution_evidence", "photo-url", ResourceType.FILE, mandatory=True)],
        produced_resources=[ResourceSpec("case_reviewed", "true", ResourceType.BOOLEAN, mandatory=True, propagate=True)],
    )

    close = Task(
        id="close_case_and_update_dashboard",
        name="Close case and update dashboard indicators",
        task_type=TaskType.END,
        is_final=True,
        required_worker_type=WorkerType.SYSTEM_AI,
        required_resources=[ResourceSpec("case_reviewed", "true", ResourceType.BOOLEAN, mandatory=True)],
    )

    detect.add_target(validate)
    validate.add_target(classify)
    validate.add_target(validate_price)
    classify.add_target(decide)
    validate_price.add_target(decide)
    decide.add_target(approve_price)
    approve_price.add_target(execute)
    execute.add_target(review)
    review.add_target(close)

    # Rework cycles required by the assignment.
    review.add_backward_transition(validate, max_retries=2, error_code="EVIDENCE_REWORK")
    execute.add_backward_transition(validate, max_retries=2, error_code="PRICE_OR_EXECUTION_REWORK")

    workflow = Workflow(
        id="app-deteccion-prod-bpmn-v1",
        name="App Deteccion Prod - Product Expiration Workflow",
        version=1,
        start_task=detect,
        final_tasks=[close],
        tasks=[detect, validate, classify, validate_price, decide, approve_price, execute, review, close],
    )
    workflow.validate()
    return workflow
