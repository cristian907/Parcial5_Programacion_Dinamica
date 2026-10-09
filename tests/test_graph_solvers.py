"""Unit tests for graph solvers: Forward DP, Backward DP, Bellman-Ford, Floyd-Warshall."""
import unittest
from src.infrastructure.repositories.preloaded_data import ParcialVPreloadedRepository
from src.infrastructure.solvers.forward_dp_solver import ForwardDPSolver
from src.infrastructure.solvers.backward_dp_solver import BackwardDPSolver
from src.infrastructure.solvers.bellman_ford_solver import BellmanFordSolver
from src.infrastructure.solvers.floyd_warshall_solver import FloydWarshallSolver


class TestGraphSolvers(unittest.TestCase):

    def setUp(self):
        self.repo = ParcialVPreloadedRepository()
        self.graph = self.repo.get_default_graph()
        self.source = 1
        self.dest = 13
        self.expected_cost = 430.0
        self.expected_path = [1, 3, 5, 7, 10, 13]

    def test_forward_dp_solver(self):
        solver = ForwardDPSolver()
        res = solver.solve(self.graph, self.source, self.dest)
        self.assertEqual(res.total_cost, self.expected_cost)
        self.assertEqual(res.optimal_path, self.expected_path)
        self.assertTrue(len(res.stages) > 0)

    def test_backward_dp_solver(self):
        solver = BackwardDPSolver()
        res = solver.solve(self.graph, self.source, self.dest)
        self.assertEqual(res.total_cost, self.expected_cost)
        self.assertEqual(res.optimal_path, self.expected_path)
        self.assertTrue(len(res.stages) > 0)

    def test_bellman_ford_solver(self):
        solver = BellmanFordSolver()
        res = solver.solve(self.graph, self.source, self.dest)
        self.assertEqual(res.total_cost, self.expected_cost)
        self.assertEqual(res.optimal_path, self.expected_path)

    def test_floyd_warshall_solver(self):
        solver = FloydWarshallSolver()
        res = solver.solve(self.graph, self.source, self.dest)
        self.assertEqual(res.total_cost, self.expected_cost)
        self.assertEqual(res.optimal_path, self.expected_path)


if __name__ == "__main__":
    unittest.main()
