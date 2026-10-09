"""Application layer interfaces and abstract base classes."""
from abc import ABC, abstractmethod
from typing import List, Tuple
from ..domain.entities import Graph, KnapsackProblem
from ..domain.models import ShortestPathResult, KnapsackResult, AlgorithmComparison


class IShortestPathSolver(ABC):
    """Abstract interface for shortest path algorithm solvers."""

    @abstractmethod
    def solve(self, graph: Graph, source: int, destination: int) -> ShortestPathResult:
        """Solves the shortest path from source to destination."""
        pass


class IKnapsackSolver(ABC):
    """Abstract interface for Cargo Volume (Knapsack) algorithm solvers."""

    @abstractmethod
    def solve(self, problem: KnapsackProblem) -> KnapsackResult:
        """Solves the cargo volume optimization problem."""
        pass


class ITextExporter(ABC):
    """Abstract interface for generating academic text report files."""

    @abstractmethod
    def export_report(
        self,
        forward_res: ShortestPathResult,
        backward_res: ShortestPathResult,
        bellman_res: ShortestPathResult,
        floyd_res: ShortestPathResult,
        knapsack_res: KnapsackResult,
        comparison: AlgorithmComparison,
        file_path: str = "reporte_problema.txt"
    ) -> str:
        """Generates and writes report to file_path, returning the written content."""
        pass


class IPreloadedDataRepository(ABC):
    """Abstract interface for preloaded Parcial V problem data."""

    @abstractmethod
    def get_default_graph(self) -> Graph:
        pass

    @abstractmethod
    def get_default_knapsack_problem(self) -> KnapsackProblem:
        pass
