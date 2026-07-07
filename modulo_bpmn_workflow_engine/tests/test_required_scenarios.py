"""Mandatory scenario coverage for the BPMN workflow engine.

These tests map one-to-one to the scenarios required by the course assignment:
linear flow, parallel split, AND/OR joins, complex/external gates, rework cycles,
multiple final tasks, incidents with reset, retry exhaustion, SLA/timeout,
multi-assignment and concurrent execution.
"""

from __future__ import annotations

import time
import unittest
from datetime import timedelta

from src.domain import (
    CompletionPolicy,
    GateType,
    IncidentType,
    LogicGate,
    ResetScope,
    ResourceSpec,
    ResourceType,
    Task,
    TaskStatus,
    TaskType,
    Worker,
    WorkerType,
    Workflow,
    WorkflowStatus,
    build_app_deteccion_workflow,
)
from src.orchestration import ThreadedExecutor
from src.runtime import WorkflowInstance


class MandatoryWorkflowScenarioTest(unittest.TestCase):
    def setUp(self) -> None:
        self.merch = Worker("m-001", "Mercaderista", WorkerType.MERCHANDISER, capacity=2)
        self.supervisor = Worker("s-001", "Supervisor", WorkerType.SUPERVISOR, capacity=2)
        self.seller = Worker("v-001", "Vendedor", WorkerType.SELLER, capacity=2)
        self.manager = Worker("g-001", "Gerente", WorkerType.MANAGER, capacity=1)

    def _simple_task(self, task_id: str, *, final: bool = False, gate: LogicGate | None = None) -> Task:
        return Task(
            id=task_id,
            name=task_id.replace("_", " ").title(),
            task_type=TaskType.END if final else TaskType.HUMAN,
            is_final=final,
            logic_gate=gate,
        )

    def _complete_without_worker(self, instance: WorkflowInstance, task_id: str) -> None:
        instance.begin_task(task_id)
        instance.complete_task(task_id)

    def _prepare_app_workflow_after_validation(self) -> WorkflowInstance:
        """Advance the reference App Deteccion workflow until the parallel split."""
        instance = WorkflowInstance(build_app_deteccion_workflow())
        instance.start()
        instance.assign_task("detect_product_case", [self.merch])
        instance.begin_task("detect_product_case")
        instance.complete_task("detect_product_case", worker=self.merch)
        instance.assign_task("validate_evidence", [self.supervisor])
        instance.begin_task("validate_evidence")
        instance.complete_task("validate_evidence", worker=self.supervisor)
        return instance

    def _prepare_app_workflow_until_execute_in_progress(self) -> WorkflowInstance:
        """Advance the reference workflow until execute_retail_action is active."""
        instance = self._prepare_app_workflow_after_validation()
        self._complete_without_worker(instance, "classify_risk")
        instance.assign_task("validate_price_data", [self.seller])
        instance.begin_task("validate_price_data")
        instance.complete_task("validate_price_data", worker=self.seller)
        instance.assign_task("decide_commercial_action", [self.seller])
        instance.begin_task("decide_commercial_action")
        instance.complete_task("decide_commercial_action", worker=self.seller)
        instance.assign_task("approve_price_change", [self.manager])
        instance.begin_task("approve_price_change")
        instance.complete_task("approve_price_change", worker=self.manager)
        instance.assign_task("execute_retail_action", [self.merch])
        instance.begin_task("execute_retail_action")
        return instance

    def test_01_linear_flow_a_b_c_d_completes(self) -> None:
        a = self._simple_task("A")
        b = self._simple_task("B")
        c = self._simple_task("C")
        d = self._simple_task("D", final=True)
        a.add_target(b)
        b.add_target(c)
        c.add_target(d)
        workflow = Workflow("wf-linear", "Linear mandatory scenario", 1, a, [d], [a, b, c, d])
        instance = WorkflowInstance(workflow)

        instance.start()
        for task_id in ["A", "B", "C", "D"]:
            self._complete_without_worker(instance, task_id)

        self.assertEqual(instance.status, WorkflowStatus.COMPLETED)
        self.assertEqual(instance.task("D").status, TaskStatus.COMPLETED)
        self.assertEqual([entry.task_id for entry in instance.execution_path if entry.status == TaskStatus.COMPLETED], ["A", "B", "C", "D"])

    def test_02_parallel_split_creates_multiple_current_tasks(self) -> None:
        instance = self._prepare_app_workflow_after_validation()

        current_ids = {task.definition.id for task in instance.current_tasks if task.status == TaskStatus.READY}

        self.assertIn("classify_risk", current_ids)
        self.assertIn("validate_price_data", current_ids)
        self.assertEqual(instance.task("classify_risk").status, TaskStatus.READY)
        self.assertEqual(instance.task("validate_price_data").status, TaskStatus.READY)

    def test_03_join_and_waits_for_both_parallel_branches(self) -> None:
        instance = self._prepare_app_workflow_after_validation()

        self._complete_without_worker(instance, "classify_risk")
        self.assertNotEqual(instance.task("decide_commercial_action").status, TaskStatus.READY)

        instance.assign_task("validate_price_data", [self.seller])
        instance.begin_task("validate_price_data")
        instance.complete_task("validate_price_data", worker=self.seller)

        self.assertEqual(instance.task("decide_commercial_action").status, TaskStatus.READY)

    def test_04_join_or_starts_after_one_completed_branch(self) -> None:
        a = self._simple_task("A")
        b = self._simple_task("B")
        c = self._simple_task("C")
        d = self._simple_task("D", final=True)
        d.logic_gate = LogicGate(GateType.OR, depends_on=[b, c])
        a.add_target(b)
        a.add_target(c)
        b.add_target(d)
        c.add_target(d)
        workflow = Workflow("wf-or", "OR join mandatory scenario", 1, a, [d], [a, b, c, d])
        instance = WorkflowInstance(workflow)

        instance.start()
        self._complete_without_worker(instance, "A")
        self._complete_without_worker(instance, "B")

        self.assertEqual(instance.task("D").status, TaskStatus.READY)
        self.assertEqual(instance.task("C").status, TaskStatus.READY)

    def test_05_complex_script_rest_and_lambda_gates_are_mockable(self) -> None:
        a = self._simple_task("A")
        b = self._simple_task("B")
        statuses = {"A": TaskStatus.COMPLETED, "B": TaskStatus.COMPLETED}

        complex_gate = LogicGate(GateType.COMPLEX, depends_on=[a, b], expression="2_OF_M")
        script_gate = LogicGate(GateType.SCRIPT, expression="var:evidence_valid")
        rest_gate = LogicGate(GateType.REST, endpoint="https://mock-risk.local/approve")
        lambda_gate = LogicGate(GateType.LAMBDA, endpoint="arn:aws:lambda:mock:approve")

        self.assertTrue(complex_gate.can_start(statuses))
        self.assertTrue(script_gate.can_start(statuses, {"evidence_valid": "true"}))
        self.assertTrue(rest_gate.can_start(statuses, {"mock:https://mock-risk.local/approve": "true"}))
        self.assertTrue(lambda_gate.can_start(statuses, {"mock:arn:aws:lambda:mock:approve": "true"}))

    def test_06_cycle_rework_resets_downstream_and_restarts_iteration(self) -> None:
        instance = self._prepare_app_workflow_until_execute_in_progress()

        incident = instance.raise_incident(
            from_task_id="execute_retail_action",
            to_task_id="validate_evidence",
            type=IncidentType.PRICE_MISMATCH,
            reason="La evidencia de ejecución no coincide con el precio aprobado.",
            raised_by=self.merch,
            reset_scope=ResetScope.ALL_DOWNSTREAM,
        )

        self.assertEqual(instance.status, WorkflowStatus.IN_PROGRESS)
        self.assertEqual(instance.iteration, 2)
        self.assertEqual(instance.task("validate_evidence").status, TaskStatus.READY)
        self.assertTrue(instance.task("execute_retail_action").was_reset)
        self.assertTrue(any(entry.incident_id == incident.id and entry.was_reset for entry in instance.execution_path))

    def test_07_multiple_final_tasks_are_supported(self) -> None:
        a = self._simple_task("A")
        success = self._simple_task("SUCCESS_END", final=True)
        rejected = self._simple_task("REJECTED_END", final=True)
        a.add_target(success)
        a.add_target(rejected)
        workflow = Workflow("wf-finals", "Multiple final tasks scenario", 1, a, [success, rejected], [a, success, rejected])
        instance = WorkflowInstance(workflow)

        instance.start()
        self._complete_without_worker(instance, "A")
        self._complete_without_worker(instance, "SUCCESS_END")

        self.assertEqual(instance.status, WorkflowStatus.COMPLETED)
        self.assertEqual(instance.task("SUCCESS_END").status, TaskStatus.COMPLETED)
        self.assertEqual(instance.task("REJECTED_END").status, TaskStatus.READY)

    def test_08_retry_exhaustion_finishes_workflow_in_error(self) -> None:
        instance = self._prepare_app_workflow_until_execute_in_progress()

        for attempt in range(3):
            instance.raise_incident(
                from_task_id="execute_retail_action",
                to_task_id="validate_evidence",
                type=IncidentType.PRICE_MISMATCH,
                reason=f"Reintento {attempt + 1}: el precio aplicado sigue incorrecto.",
                raised_by=self.merch,
                reset_scope=ResetScope.ALL_DOWNSTREAM,
            )
            if instance.status == WorkflowStatus.ERROR:
                break
            # Simulates the same task reaching execution again after rework.
            instance.task("execute_retail_action").status = TaskStatus.IN_PROGRESS

        self.assertEqual(instance.status, WorkflowStatus.ERROR)
        self.assertTrue(instance.task("execute_retail_action").retries_exhausted)

    def test_09_sla_timeout_marks_ready_task_as_timed_out(self) -> None:
        instance = WorkflowInstance(build_app_deteccion_workflow())
        instance.start()
        instance.assign_task("detect_product_case", [self.merch])
        instance.begin_task("detect_product_case")
        instance.complete_task("detect_product_case", worker=self.merch)
        validate = instance.task("validate_evidence")
        self.assertEqual(validate.status, TaskStatus.READY)
        self.assertIsNotNone(validate.assign_deadline)

        timed_out = instance.timed_out_tasks(now=validate.assign_deadline + timedelta(seconds=1))

        self.assertIn(validate, timed_out)
        self.assertEqual(validate.status, TaskStatus.TIMED_OUT)
        self.assertTrue(any(entry.task_id == "validate_evidence" and entry.status == TaskStatus.TIMED_OUT for entry in instance.execution_path))

    def test_10_multi_assignment_quorum_policy(self) -> None:
        a = self._simple_task("A", final=True)
        a.completion_policy = CompletionPolicy.QUORUM
        a.quorum = 2
        a.required_worker_type = WorkerType.MERCHANDISER
        workflow = Workflow("wf-quorum", "Quorum multi-assignment scenario", 1, a, [a], [a])
        instance = WorkflowInstance(workflow)
        second = Worker("m-002", "Mercaderista Dos", WorkerType.MERCHANDISER)
        third = Worker("m-003", "Mercaderista Tres", WorkerType.MERCHANDISER)

        instance.start()
        instance.assign_task("A", [self.merch, second, third])
        instance.begin_task("A")
        instance.complete_task("A", worker=self.merch)
        self.assertEqual(instance.task("A").status, TaskStatus.IN_PROGRESS)
        instance.complete_task("A", worker=second)

        self.assertEqual(instance.status, WorkflowStatus.COMPLETED)
        self.assertEqual(instance.task("A").status, TaskStatus.COMPLETED)

    def test_11_concurrent_execution_completes_parallel_branches(self) -> None:
        instance = self._prepare_app_workflow_after_validation()
        instance.assign_task("validate_price_data", [self.seller])

        def complete_classify() -> str:
            instance.begin_task("classify_risk")
            time.sleep(0.01)
            instance.complete_task("classify_risk")
            return "classify_risk"

        def complete_price_validation() -> str:
            instance.begin_task("validate_price_data")
            time.sleep(0.01)
            instance.complete_task("validate_price_data", worker=self.seller)
            return "validate_price_data"

        with ThreadedExecutor(max_workers=2) as executor:
            futures = [executor.submit(complete_classify), executor.submit(complete_price_validation)]
            completed_ids = {future.result(timeout=2) for future in futures}

        self.assertEqual(completed_ids, {"classify_risk", "validate_price_data"})
        self.assertEqual(instance.task("decide_commercial_action").status, TaskStatus.READY)
        self.assertTrue(all(future.done() for future in futures))

    def test_12_mandatory_resources_block_completion_when_missing(self) -> None:
        a = Task(
            id="A",
            name="Requires product photo",
            required_resources=[ResourceSpec("product_photo", "photo-url", ResourceType.FILE, mandatory=True)],
            is_final=True,
            task_type=TaskType.END,
        )
        workflow = Workflow("wf-resource", "Mandatory resources scenario", 1, a, [a], [a])
        instance = WorkflowInstance(workflow)
        instance.start()
        instance.begin_task("A")

        with self.assertRaises(ValueError):
            instance.complete_task("A")


if __name__ == "__main__":
    unittest.main()
