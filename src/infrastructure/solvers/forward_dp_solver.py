"""Forward Dynamic Programming Solver (Adelante hacia Atrás)."""
from collections import defaultdict, deque
from typing import Dict, List, Optional, Set
from ...application.interfaces import IShortestPathSolver
from ...domain.entities import Graph
from ...domain.exceptions import NodeNotFoundError, PathNotFoundError
from ...domain.models import ShortestPathResult, StageTable, StageTableRow


class ForwardDPSolver(IShortestPathSolver):
    """Solves shortest path using Forward Dynamic Programming induction:
    f*(s) = min_{x in Pred(s)} [ f*(x) + c(x, s) ]
    Starting from source node moving forward to destination.
    """

    def solve(self, graph: Graph, source: int, destination: int) -> ShortestPathResult:
        if source not in graph.nodes:
            raise NodeNotFoundError(f"El nodo origen {source} no existe en el grafo.")
        if destination not in graph.nodes:
            raise NodeNotFoundError(f"El nodo destino {destination} no existe en el grafo.")

        topo_order = self._get_topological_order(graph)
        if not topo_order:
            topo_order = sorted(list(graph.nodes.keys()))

        # f_cost[node] = minimal cost to reach node from source
        f_cost: Dict[int, float] = {source: 0.0}
        predecessor: Dict[int, Optional[int]] = {source: None}
        evaluations_by_node: Dict[int, Dict[int, float]] = {}

        for v in topo_order:
            if v == source:
                continue

            preds = graph.get_predecessors(v)
            if not preds:
                continue

            evals: Dict[int, float] = {}
            best_cost = float("inf")
            best_pred = None

            for u, weight in preds:
                if u in f_cost and f_cost[u] < float("inf"):
                    cand_cost = f_cost[u] + weight
                    evals[u] = cand_cost
                    if cand_cost < best_cost:
                        best_cost = cand_cost
                        best_pred = u

            if evals:
                evaluations_by_node[v] = evals
                f_cost[v] = best_cost
                predecessor[v] = best_pred

        if destination not in f_cost or f_cost[destination] == float("inf"):
            raise PathNotFoundError(f"No existe una ruta desde el nodo {source} hasta el nodo {destination}.")

        # Reconstruct path from destination backwards to source
        optimal_path: List[int] = []
        curr: Optional[int] = destination
        visited: Set[int] = set()
        while curr is not None:
            optimal_path.append(curr)
            visited.add(curr)
            if curr == source:
                break
            curr = predecessor.get(curr)
            if curr in visited:
                break
        optimal_path.reverse()

        # Build StageTables grouped logically by distance from source
        stages = self._build_forward_stage_tables(graph, topo_order, source, evaluations_by_node, f_cost, predecessor)

        explanation = (
            f"Resolución de Adelante hacia Atrás (Inducción Hacia Adelante):\n"
            f"1. Se establece la condición inicial en el nodo origen: f*({source}) = 0.\n"
            f"2. Se evalúa progresivamente cada etapa k mediante la ecuación recursiva:\n"
            f"   f_n*(s) = min_{{x}} [ f_{{n-1}}^*(x) + c(x, s) ], donde x in Pred(s)\n"
            f"3. Al alcanzar el nodo destino {destination}, se obtiene el costo mínimo total de {f_cost[destination]}.\n"
            f"4. Reconstruyendo la ruta a partir de los predecesores óptimos x*(s), se obtiene: "
            f"{' -> '.join(str(n) for n in optimal_path)}."
        )

        return ShortestPathResult(
            algorithm_name="Programación Dinámica (Adelante hacia Atrás)",
            source=source,
            destination=destination,
            total_cost=f_cost[destination],
            optimal_path=optimal_path,
            stages=stages,
            intermediate_data={
                "costs": f_cost,
                "predecessors": predecessor,
                "evaluations": evaluations_by_node,
            },
            explanation=explanation,
        )

    def _get_topological_order(self, graph: Graph) -> List[int]:
        in_degree: Dict[int, int] = {nid: 0 for nid in graph.nodes}
        for e in graph.edges:
            in_degree[e.target] = in_degree.get(e.target, 0) + 1

        queue = deque([nid for nid, deg in in_degree.items() if deg == 0])
        order: List[int] = []

        while queue:
            u = queue.popleft()
            order.append(u)
            for v, _ in graph.get_successors(u):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        return order if len(order) == len(graph.nodes) else []

    def _build_forward_stage_tables(
        self,
        graph: Graph,
        topo_order: List[int],
        source: int,
        evaluations_by_node: Dict[int, Dict[int, float]],
        f_cost: Dict[int, float],
        predecessor: Dict[int, Optional[int]],
    ) -> List[StageTable]:
        # Compute step depth from source
        depth_from_src: Dict[int, int] = {source: 0}
        for v in topo_order:
            if v not in depth_from_src:
                preds = [depth_from_src[u] for u, _ in graph.get_predecessors(v) if u in depth_from_src]
                if preds:
                    depth_from_src[v] = min(preds) + 1
                else:
                    depth_from_src[v] = 99

        stages_dict: Dict[int, List[int]] = defaultdict(list)
        for v in topo_order:
            if v == source or v not in evaluations_by_node:
                continue
            stage_num = depth_from_src.get(v, 1)
            stages_dict[stage_num].append(v)

        stage_tables: List[StageTable] = []
        for stage_idx, s_num in enumerate(sorted(stages_dict.keys()), start=1):
            nodes_in_stage = stages_dict[s_num]
            rows: List[StageTableRow] = []
            for v in sorted(nodes_in_stage):
                evals = evaluations_by_node.get(v, {})
                cands = sorted(list(evals.keys()))
                opt_cost = f_cost.get(v, float("inf"))
                opt_dec = predecessor.get(v)
                rows.append(
                    StageTableRow(
                        state=v,
                        candidate_decisions=cands,
                        evaluations=evals,
                        optimal_cost=opt_cost,
                        optimal_decision=opt_dec,
                    )
                )

            stage_tables.append(
                StageTable(
                    stage_number=stage_idx,
                    stage_name=f"Etapa {stage_idx} (Hacia Adelante, paso {s_num} desde origen)",
                    description=f"Evaluación de estados {nodes_in_stage} minimizando f*(x) + c(x, s)",
                    rows=rows,
                )
            )

        return stage_tables
