"""Use case for solving the Cargo Volume (Knapsack) problem."""
from ...domain.entities import KnapsackProblem
from ...domain.models import KnapsackResult
from ..interfaces import IKnapsackSolver


class SolveKnapsackUseCase:
    """Solves the Cargo Volume problem with stage-by-stage dynamic programming."""

    def __init__(self, solver: IKnapsackSolver) -> None:
        self._solver = solver

    def execute(self, problem: KnapsackProblem) -> KnapsackResult:
        return self._solver.solve(problem)
