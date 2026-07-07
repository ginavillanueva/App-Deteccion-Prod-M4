"""Tests for ReadyQueue, Observer and Orchestrator assignment."""

from __future__ import annotations

import unittest

from src.domain import ResourceInstance, ResourceType, Worker, WorkerType, build_app_deteccion_workflow
from src.orchestration import InMemoryEventLog, Orchestrator, ReadyQueue, WorkerPool
from src.runtime import WorkflowInstance


class OrchestrationTestCase(unittest.TestCase):
    def _workers(self) -> list[Worker]:
        return [
            Worker("m1", "Mercaderista Uno", WorkerType.MERCHANDISER, capacity=2),
            Worker("m2", "Mercaderista Dos", WorkerType.MERCHANDISER, capacity=1),
            Worker("s1", "Supervisor Uno", WorkerType.SUPERVISOR, capacity=2),
            Worker("v1", "Vendedor Uno", WorkerType.SELLER, capacity=2),
            Worker("g1", "Gerente Uno", WorkerType.MANAGER, capacity=1),
            Worker("ai1", "AI Worker", WorkerType.SYSTEM_AI, capacity=5),
        ]

    def test_ready_queue_notifies_observers(self) -> None:
        workflow = WorkflowInstance(build_app_deteccion_workflow())
        start = workflow.start()
        queue = ReadyQueue()
        log = InMemoryEventLog()
        queue.subscribe(log)

        queue.enqueue(workflow, start)

        self.assertEqual(len(queue), 1)
        self.assertIn("task_ready", log.names())
        self.assertEqual(queue.task_ids(), ["detect_product_case"])

    def test_orchestrator_assigns_ready_task_by_skill_and_load(self) -> None:
        workflow = WorkflowInstance(build_app_deteccion_workflow())
        registry = {workflow.id: workflow}
        queue = ReadyQueue()
        pool = WorkerPool(self._workers())
        orchestrator = Orchestrator(queue, pool)

        orchestrator.submit_workflow(workflow)
        assignment = orchestrator.assign_next(registry)

        self.assertIsNotNone(assignment)
        self.assertEqual(assignment.worker.worker_type, WorkerType.MERCHANDISER)
        self.assertEqual(workflow.task("detect_product_case").assigned_workers[0], assignment.worker)
        self.assertIn("task_assigned", [event.name for event in orchestrator.events])

    def test_orchestrator_completes_task_and_enqueues_forward_target(self) -> None:
        workflow = WorkflowInstance(build_app_deteccion_workflow())
        registry = {workflow.id: workflow}
        queue = ReadyQueue()
        pool = WorkerPool(self._workers())
        orchestrator = Orchestrator(queue, pool)

        orchestrator.submit_workflow(workflow)
        assignment = orchestrator.assign_next(registry)
        self.assertIsNotNone(assignment)

        orchestrator.complete_task(workflow, "detect_product_case", worker=assignment.worker)

        self.assertEqual(queue.task_ids(), ["validate_evidence"])
        self.assertEqual(workflow.task("validate_evidence").resources[0].source_task_id, "detect_product_case")
        self.assertIn("task_completed", [event.name for event in orchestrator.events])

    def test_worker_pool_uses_least_loaded_candidate(self) -> None:
        workflow = WorkflowInstance(build_app_deteccion_workflow())
        start = workflow.start()
        workers = [
            Worker("m1", "Mercaderista Uno", WorkerType.MERCHANDISER, capacity=2),
            Worker("m2", "Mercaderista Dos", WorkerType.MERCHANDISER, capacity=2),
        ]
        pool = WorkerPool(workers)
        pool.mark_assigned(workflow.id, start, workers[0])

        assignment = pool.select_worker(start)

        self.assertEqual(assignment.worker.employee_id, "m2")


if __name__ == "__main__":
    unittest.main()
