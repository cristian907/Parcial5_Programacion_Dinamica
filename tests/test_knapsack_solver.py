"""Unit tests for Cargo Volume (Knapsack) DP solver."""
import unittest
from src.infrastructure.repositories.preloaded_data import ParcialVPreloadedRepository
from src.infrastructure.solvers.knapsack_dp_solver import KnapsackDPSolver


class TestKnapsackSolver(unittest.TestCase):

    def setUp(self):
        self.repo = ParcialVPreloadedRepository()
        self.problem = self.repo.get_default_knapsack_problem()
        self.solver = KnapsackDPSolver()

    def test_parcial_knapsack_01(self):
        # Default capacity 10 kg, 0-1 knapsack
        res = self.solver.solve(self.problem)

        self.assertEqual(res.total_value, 155.0)
        self.assertEqual(res.total_weight, 9.0)
        self.assertEqual(res.slack_capacity, 1.0)

        # Selected items: Tablet (1), Dron (2), Proyector (3)
        selected_ids = sorted([it.id for it in res.selected_items])
        self.assertEqual(selected_ids, [1, 2, 3])

    def test_unbounded_knapsack(self):
        self.problem.allow_repetition = True
        res = self.solver.solve(self.problem)

        # In unbounded, taking 5 Tablets (2kg each) gives 5 * $40 = $200 (weight 10kg)
        self.assertEqual(res.total_value, 200.0)
        self.assertEqual(res.total_weight, 10.0)
        self.assertEqual(res.slack_capacity, 0.0)
        self.assertEqual(res.item_counts[1], 5)


if __name__ == "__main__":
    unittest.main()
