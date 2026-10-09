"""Presentation Controllers connecting UI with Clean Architecture Use Cases."""
from typing import List, Optional, Tuple
from ..domain.entities import Edge, Graph, Item, KnapsackProblem
from ..domain.models import AlgorithmComparison, KnapsackResult, ShortestPathResult
from ..application.interfaces import IPreloadedDataRepository
from ..application.use_cases.solve_shortest_path import (
    SolveShortestPathForwardUseCase,
    SolveShortestPathBackwardUseCase,
    SolveBellmanFordUseCase,
    SolveFloydWarshallUseCase,
)
from ..application.use_cases.solve_knapsack import SolveKnapsackUseCase
from ..application.use_cases.compare_algorithms import CompareAlgorithmsUseCase
from ..application.use_cases.export_reports import ExportReportUseCase
from ..infrastructure.solvers.forward_dp_solver import ForwardDPSolver
from ..infrastructure.solvers.backward_dp_solver import BackwardDPSolver
from ..infrastructure.solvers.bellman_ford_solver import BellmanFordSolver
from ..infrastructure.solvers.floyd_warshall_solver import FloydWarshallSolver
from ..infrastructure.solvers.knapsack_dp_solver import KnapsackDPSolver
from ..infrastructure.exporters.report_text_exporter import ReportTextExporter


class GraphController:
    """Controller for graph shortest path operations."""

    def __init__(self, repo: IPreloadedDataRepository):
        self.repo = repo
        self._graph: Graph = self.repo.get_default_graph()

        # Instantiate solvers & use cases
        self.uc_forward = SolveShortestPathForwardUseCase(ForwardDPSolver())
        self.uc_backward = SolveShortestPathBackwardUseCase(BackwardDPSolver())
        self.uc_bellman = SolveBellmanFordUseCase(BellmanFordSolver())
        self.uc_floyd = SolveFloydWarshallUseCase(FloydWarshallSolver())
        self.uc_compare = CompareAlgorithmsUseCase()

    def get_graph(self) -> Graph:
        return self._graph

    def reset_to_default_graph(self) -> Graph:
        self._graph = self.repo.get_default_graph()
        return self._graph

    def add_edge(self, source: int, target: int, weight: float) -> Edge:
        return self._graph.add_edge(source, target, weight)

    def remove_edge(self, source: int, target: int) -> bool:
        return self._graph.remove_edge(source, target)

    def solve(
        self, source: int, destination: int, algorithm_key: str = "forward"
    ) -> Tuple[ShortestPathResult, Optional[AlgorithmComparison]]:
        # Always run all 4 to enable comparison if requested
        res_fwd = self.uc_forward.execute(self._graph, source, destination)
        res_bwd = self.uc_backward.execute(self._graph, source, destination)
        res_bell = self.uc_bellman.execute(self._graph, source, destination)
        res_floyd = self.uc_floyd.execute(self._graph, source, destination)

        comparison = self.uc_compare.execute(res_fwd, res_bwd, res_bell, res_floyd)

        if algorithm_key == "forward":
            return res_fwd, None
        elif algorithm_key == "backward":
            return res_bwd, None
        elif algorithm_key == "bellman":
            return res_bell, None
        elif algorithm_key == "floyd":
            return res_floyd, None
        else:  # "all"
            return res_fwd, comparison


class KnapsackController:
    """Controller for cargo volume optimization operations."""

    def __init__(self, repo: IPreloadedDataRepository):
        self.repo = repo
        self._problem: KnapsackProblem = self.repo.get_default_knapsack_problem()
        self.uc_solve = SolveKnapsackUseCase(KnapsackDPSolver())

    def get_problem(self) -> KnapsackProblem:
        return self._problem

    def reset_to_default(self) -> KnapsackProblem:
        self._problem = self.repo.get_default_knapsack_problem()
        return self._problem

    def add_item(self, name: str, weight: float, price: float) -> Item:
        next_id = max([it.id for it in self._problem.items], default=0) + 1
        return self._problem.add_item(next_id, name, weight, price)

    def remove_item(self, item_id: int) -> bool:
        return self._problem.remove_item(item_id)

    def solve(self, capacity: float, allow_repetition: bool = False) -> KnapsackResult:
        self._problem.capacity = capacity
        self._problem.allow_repetition = allow_repetition
        return self.uc_solve.execute(self._problem)


class ReportController:
    """Controller for generating and writing the official problem report."""

    def __init__(self, repo: IPreloadedDataRepository):
        self.repo = repo
        self.uc_forward = SolveShortestPathForwardUseCase(ForwardDPSolver())
        self.uc_backward = SolveShortestPathBackwardUseCase(BackwardDPSolver())
        self.uc_bellman = SolveBellmanFordUseCase(BellmanFordSolver())
        self.uc_floyd = SolveFloydWarshallUseCase(FloydWarshallSolver())
        self.uc_compare = CompareAlgorithmsUseCase()
        self.uc_knapsack = SolveKnapsackUseCase(KnapsackDPSolver())
        self.uc_export = ExportReportUseCase(ReportTextExporter())

    def generate_report(self, file_path: str = "reporte_problema.txt") -> str:
        graph = self.repo.get_default_graph()
        knap = self.repo.get_default_knapsack_problem()

        fwd = self.uc_forward.execute(graph, 1, 13)
        bwd = self.uc_backward.execute(graph, 1, 13)
        bell = self.uc_bellman.execute(graph, 1, 13)
        floyd = self.uc_floyd.execute(graph, 1, 13)
        comp = self.uc_compare.execute(fwd, bwd, bell, floyd)
        knap_res = self.uc_knapsack.execute(knap)

        return self.uc_export.execute(
            forward_res=fwd,
            backward_res=bwd,
            bellman_res=bell,
            floyd_res=floyd,
            knapsack_res=knap_res,
            comparison=comp,
            file_path=file_path,
        )
