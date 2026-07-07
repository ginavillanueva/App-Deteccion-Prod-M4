import unittest

from src.domain import (
    CompletionPolicy,
    IncidentType,
    ResetScope,
    ResourceInstance,
    ResourceType,
    TaskStatus,
    Worker,
    WorkerType,
    WorkflowStatus,
    build_app_deteccion_workflow,
)
from src.runtime import WorkflowInstance


class RuntimeEngineTest(unittest.TestCase):
    def setUp(self):
        self.workflow = build_app_deteccion_workflow()
        self.instance = WorkflowInstance(self.workflow)
        self.merch = Worker("m-001", "Mercaderista Uno", WorkerType.MERCHANDISER)
        self.supervisor = Worker("s-001", "Supervisor Uno", WorkerType.SUPERVISOR)
        self.seller = Worker("v-001", "Vendedor Uno", WorkerType.SELLER)
        self.manager = Worker("g-001", "Gerente Comercial", WorkerType.MANAGER)

    def _complete_detect_and_validate(self):
        self.instance.start()
        self.instance.assign_task("detect_product_case", [self.merch])
        self.instance.begin_task("detect_product_case")
        self.instance.complete_task("detect_product_case", worker=self.merch)

        self.instance.assign_task("validate_evidence", [self.supervisor])
        self.instance.begin_task("validate_evidence")
        self.instance.complete_task("validate_evidence", worker=self.supervisor)

    def test_start_and_forward_navigation_propagates_resources(self):
        self.instance.start()
        self.instance.assign_task("detect_product_case", [self.merch])
        self.instance.begin_task("detect_product_case")
        self.instance.complete_task("detect_product_case", worker=self.merch)

        validate = self.instance.task("validate_evidence")
        self.assertEqual(validate.status, TaskStatus.READY)
        self.assertIn("expiration_date", self.instance.variables)
        self.assertTrue(any(r.key == "product_photo" for r in validate.resources))
        self.assertGreaterEqual(len(self.instance.execution_path), 4)

    def test_and_join_waits_until_both_parallel_predecessors_complete(self):
        self._complete_detect_and_validate()

        classify = self.instance.task("classify_risk")
        price = self.instance.task("validate_price_data")
        self.assertEqual(classify.status, TaskStatus.READY)
        self.assertEqual(price.status, TaskStatus.READY)

        self.instance.begin_task("classify_risk")
        self.instance.complete_task("classify_risk")
        self.assertNotEqual(self.instance.task("decide_commercial_action").status, TaskStatus.READY)

        self.instance.assign_task("validate_price_data", [self.seller])
        self.instance.begin_task("validate_price_data")
        self.instance.complete_task("validate_price_data", worker=self.seller)
        self.assertEqual(self.instance.task("decide_commercial_action").status, TaskStatus.READY)

    def test_backward_incident_resets_downstream_and_records_trace(self):
        self._complete_detect_and_validate()
        self.instance.begin_task("classify_risk")
        self.instance.complete_task("classify_risk")
        self.instance.assign_task("validate_price_data", [self.seller])
        self.instance.begin_task("validate_price_data")
        self.instance.complete_task("validate_price_data", worker=self.seller)
        self.instance.assign_task("decide_commercial_action", [self.seller])
        self.instance.begin_task("decide_commercial_action")
        self.instance.complete_task("decide_commercial_action", worker=self.seller)
        self.instance.assign_task("approve_price_change", [self.manager])
        self.instance.begin_task("approve_price_change")
        self.instance.complete_task("approve_price_change", worker=self.manager)
        self.instance.assign_task("execute_retail_action", [self.merch])
        self.instance.begin_task("execute_retail_action")

        incident = self.instance.raise_incident(
            from_task_id="execute_retail_action",
            to_task_id="validate_evidence",
            type=IncidentType.PRICE_MISMATCH,
            reason="Precio aplicado en sala no coincide con precio aprobado.",
            raised_by=self.merch,
            reset_scope=ResetScope.ALL_DOWNSTREAM,
        )

        self.assertEqual(len(self.instance.incidents), 1)
        self.assertEqual(self.instance.incidents[0].id, incident.id)
        self.assertEqual(self.instance.task("validate_evidence").status, TaskStatus.READY)
        self.assertTrue(self.instance.task("execute_retail_action").was_reset)
        self.assertTrue(any(entry.incident_id == incident.id for entry in self.instance.execution_path))

    def test_retry_exhaustion_moves_workflow_to_error(self):
        self._complete_detect_and_validate()
        self.instance.begin_task("classify_risk")
        self.instance.complete_task("classify_risk")
        self.instance.assign_task("validate_price_data", [self.seller])
        self.instance.begin_task("validate_price_data")
        self.instance.complete_task("validate_price_data", worker=self.seller)
        self.instance.assign_task("decide_commercial_action", [self.seller])
        self.instance.begin_task("decide_commercial_action")
        self.instance.complete_task("decide_commercial_action", worker=self.seller)
        self.instance.assign_task("approve_price_change", [self.manager])
        self.instance.begin_task("approve_price_change")
        self.instance.complete_task("approve_price_change", worker=self.manager)
        self.instance.assign_task("execute_retail_action", [self.merch])
        self.instance.begin_task("execute_retail_action")

        # The factory defines max_retries=2 for execute -> validate. The third
        # incident must terminate the workflow in ERROR.
        for idx in range(3):
            self.instance.raise_incident(
                from_task_id="execute_retail_action",
                to_task_id="validate_evidence",
                type=IncidentType.PRICE_MISMATCH,
                reason=f"Rework attempt {idx + 1} due to price mismatch.",
                raised_by=self.merch,
                reset_scope=ResetScope.ALL_DOWNSTREAM,
            )
            if self.instance.status == WorkflowStatus.ERROR:
                break
            # Put the same source task back in progress to simulate the worker
            # finding the same incident again after rework.
            self.instance.task("execute_retail_action").status = TaskStatus.IN_PROGRESS

        self.assertEqual(self.instance.status, WorkflowStatus.ERROR)
        self.assertTrue(self.instance.task("execute_retail_action").retries_exhausted)

    def test_multi_assignment_any_policy(self):
        self.instance.start()
        task = self.instance.task("detect_product_case")
        task.definition.completion_policy = CompletionPolicy.ANY
        second_merch = Worker("m-002", "Mercaderista Dos", WorkerType.MERCHANDISER)
        self.instance.assign_task("detect_product_case", [self.merch, second_merch])
        self.instance.begin_task("detect_product_case")
        self.instance.complete_task("detect_product_case", worker=self.merch)
        self.assertEqual(task.status, TaskStatus.COMPLETED)

    def test_manual_runtime_resource_can_be_added(self):
        self.instance.start()
        custom = ResourceInstance("store_code", "LP-001", ResourceType.TEXT, source_task_id="manual")
        self.instance.task("detect_product_case").add_resource(custom)
        self.assertTrue(any(r.key == "store_code" for r in self.instance.task("detect_product_case").resources))


if __name__ == "__main__":
    unittest.main()
