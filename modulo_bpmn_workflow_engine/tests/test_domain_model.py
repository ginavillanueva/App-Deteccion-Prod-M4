import unittest

from src.domain import (
    GateType,
    LogicGate,
    Task,
    TaskStatus,
    TransitionType,
    build_app_deteccion_workflow,
)


class DomainModelTest(unittest.TestCase):
    def test_reference_workflow_is_valid_and_reachable(self):
        workflow = build_app_deteccion_workflow()
        workflow.validate()
        reachable = workflow.dependency_matrix.reachable_from(workflow.start_task.id)
        self.assertIn("close_case_and_update_dashboard", reachable)
        self.assertEqual(workflow.orphan_tasks(), [])

    def test_backward_transition_requires_retry_limit(self):
        a = Task(id="a", name="A")
        b = Task(id="b", name="B")
        with self.assertRaises(ValueError):
            # max_retries is mandatory for BACKWARD edges.
            from src.domain import Transition

            Transition(source=a, target=b, type=TransitionType.BACKWARD)

    def test_and_gate_requires_all_predecessors_completed(self):
        a = Task(id="a", name="A")
        b = Task(id="b", name="B")
        gate = LogicGate(type=GateType.AND, depends_on=[a, b])
        self.assertFalse(gate.can_start({"a": TaskStatus.COMPLETED, "b": TaskStatus.PENDING}))
        self.assertTrue(gate.can_start({"a": TaskStatus.COMPLETED, "b": TaskStatus.COMPLETED}))


if __name__ == "__main__":
    unittest.main()
