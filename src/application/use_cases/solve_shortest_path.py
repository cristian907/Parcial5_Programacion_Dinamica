"""Use cases for solving shortest path algorithms."""
from ...domain.entities import Graph
from ...domain.models import ShortestPathResult
from ..interfaces import IShortestPathSolver


class SolveShortestPathForwardUseCase:
    """Calculates shortest path using Forward Dynamic Programming (Adelante hacia Atrás)."""

    def __init__(self, solver: IShortestPathSolver) -> None:
        self._solver = solver

    def execute(self, graph: Graph, source: int, destination: int) -> ShortestPathResult:
        return self._solver.solve(graph, source, destination)


class SolveShortestPathBackwardUseCase:
    """Calculates shortest path using Backward Dynamic Programming (De Atrás hacia Adelante)."""

    def __init__(self, solver: IShortestPathSolver) -> None:
        self._solver = solver

    def execute(self, graph: Graph, source: int, destination: int) -> ShortestPathResult:
        return self._solver.solve(graph, source, destination)


class SolveBellmanFordUseCase:
    """Calculates shortest path using Bellman-Ford algorithm."""

    def __init__(self, solver: IShortestPathSolver) -> None:
        self._solver = solver

    def execute(self, graph: Graph, source: int, destination: int) -> ShortestPathResult:
        return self._solver.solve(graph, source, destination)


class SolveFloydWarshallUseCase:
    """Calculates all-pairs shortest paths using Floyd-Warshall algorithm."""

    def __init__(self, solver: IShortestPathSolver) -> None:
        self._solver = solver

    def execute(self, graph: Graph, source: int, destination: int) -> ShortestPathResult:
        return self._solver.solve(graph, source, destination)
