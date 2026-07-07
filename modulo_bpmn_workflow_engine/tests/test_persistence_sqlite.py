"""Tests for SQLite persistence adapter."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.domain import IncidentType, Worker, WorkerType, build_app_deteccion_workflow
from src.persistence import SQLiteWorkflowRepository
from src.runtime import WorkflowInstance


class SQLiteWorkflowRepositoryTest(unittest.TestCase):
    def test_save_workflow_definition_payload(self) -> None:
        workflow = build_app_deteccion_workflow()
        with tempfile.TemporaryDirectory() as tmp_dir:
            repository = SQLiteWorkflowRepository(Path(tmp_dir) / "workflow.db")
            repository.save_workflow_definition(workflow)

            payload = repository.load_workflow_definition_payload(workflow.id)

            self.assertEqual(payload["id"], "app-deteccion-prod-bpmn-v1")
            self.assertEqual(payload["start_task_id"], "detect_product_case")
            self.assertIn("close_case_and_update_dashboard", payload["final_task_ids"])
            self.assertGreaterEqual(len(payload["tasks"]), 9)
            self.assertEqual(repository.count_rows("workflow_definitions"), 1)

    def test_save_runtime_snapshot_with_trace_and_task_state(self) -> None:
        workflow = build_app_deteccion_workflow()
        worker = Worker(
            employee_id="MER-001",
            name="Mercaderista Demo",
            worker_type=WorkerType.MERCHANDISER,
            capacity=2,
        )
        instance = WorkflowInstance(definition=workflow)
        instance.start()
        instance.assign_task("detect_product_case", [worker])
        instance.begin_task("detect_product_case")
        instance.complete_task("detect_product_case", worker=worker)

        with tempfile.TemporaryDirectory() as tmp_dir:
            repository = SQLiteWorkflowRepository(Path(tmp_dir) / "workflow.db")
            repository.save_worker(worker)
            repository.save_workflow_instance(instance)
            snapshot = repository.load_workflow_instance_snapshot(instance.id)

            self.assertEqual(snapshot["workflow_instance"]["status"], "IN_PROGRESS")
            self.assertIn("validate_evidence", snapshot["workflow_instance"]["current_task_ids"])
            self.assertGreaterEqual(len(snapshot["trace_entries"]), 4)
            detect_rows = [row for row in snapshot["task_instances"] if row["task_id"] == "detect_product_case"]
            self.assertEqual(detect_rows[0]["status"], "COMPLETED")
            self.assertEqual(repository.count_rows("workers"), 1)
            self.assertEqual(repository.count_rows("workflow_instances"), 1)

    def test_save_snapshot_after_rework_incident(self) -> None:
        workflow = build_app_deteccion_workflow()
        supervisor = Worker(
            employee_id="SUP-001",
            name="Supervisor Demo",
            worker_type=WorkerType.SUPERVISOR,
            capacity=1,
        )
        instance = WorkflowInstance(definition=workflow)
        instance.start()
        incident = instance.raise_incident(
            from_task_id="supervisor_review",
            to_task_id="validate_evidence",
            type=IncidentType.EVIDENCE_INCOMPLETE,
            reason="La evidencia de ejecución no permite validar el cambio de precio aplicado.",
            raised_by=supervisor,
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            repository = SQLiteWorkflowRepository(Path(tmp_dir) / "workflow.db")
            repository.save_workflow_instance(instance)
            snapshot = repository.load_workflow_instance_snapshot(instance.id)

            self.assertEqual(len(snapshot["incidents"]), 1)
            self.assertEqual(snapshot["incidents"][0]["id"], incident.id)
            self.assertEqual(snapshot["incidents"][0]["reset_scope"], "ALL_DOWNSTREAM")
            self.assertGreaterEqual(repository.count_rows("trace_entries"), 1)


if __name__ == "__main__":
    unittest.main()
