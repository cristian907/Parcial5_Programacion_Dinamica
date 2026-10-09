"""Backward Dynamic Programming Solver (De Atrás hacia Adelante)."""
from collections import defaultdict, deque
from typing import Dict, List, Optional, Set
from ...application.interfaces import IShortestPathSolver
from ...domain.entities import Graph
from ...domain.exceptions import NodeNotFoundError, PathNotFoundError
from ...domain.models import ShortestPathResult, StageTable, StageTableRow


class BackwardDPSolver(IShortestPathSolver):
    """Solves shortest path using Backward Dynamic Programming induction:
    f*(s) = min_{x in Suc(s)} [ c(s, x) + f*(x) ]
    Starting from destination node towards source node.
    """

    def solve(self, graph: Graph, source: int, destination: int) -> ShortestPathResult:
        if source not in graph.nodes:
            raise NodeNotFoundError(f"El nodo origen {source} no existe en el grafo.")
        if destination not in graph.nodes:
            raise NodeNotFoundError(f"El nodo destino {destination} no existe en el grafo.")

        # Compute topological order
        topo_order = self._get_topological_order(graph)
        if not topo_order:
            # Fallback if cycles exist, though exam graph is DAG
            topo_order = sorted(list(graph.nodes.keys()))

        # Backward traversal: reverse topological order
        rev_order = list(reversed(topo_order))

        # f_cost[node] = minimal cost to reach destination
        f_cost: Dict[int, float] = {destination: 0.0}
        decision: Dict[int, Optional[int]] = {destination: None}
        evaluations_by_node: Dict[int, Dict[int, float]] = {}

        for u in rev_order:
            if u == destination:
                continue
            successors = graph.get_successors(u)
            if not successors:
                continue

            evals: Dict[int, float] = {}
            best_cost = float("inf")
            best_dec = None

            for v, weight in successors:
                if v in f_cost and f_cost[v] < float("inf"):
                    cand_cost = weight + f_cost[v]
                    evals[v] = cand_cost
                    if cand_cost < best_cost:
                        best_cost = cand_cost
                        best_dec = v

            if evals:
                evaluations_by_node[u] = evals
                f_cost[u] = best_cost
                decision[u] = best_dec

        if source not in f_cost or f_cost[source] == float("inf"):
            raise PathNotFoundError(f"No existe una ruta desde el nodo {source} hasta el nodo {destination}.")

        # Reconstruct path from source to destination using decision map
        optimal_path: List[int] = [source]
        curr = source
        visited: Set[int] = {curr}
        while curr != destination:
            nxt = decision.get(curr)
            if nxt is None or nxt in visited:
                break
            optimal_path.append(nxt)
            visited.add(nxt)
            curr = nxt

        # Build StageTables grouped logically by distance-to-destination layers
        stages = self._build_backward_stage_tables(graph, rev_order, destination, evaluations_by_node, f_cost, decision)

        explanation = (
            f"Resolución de Atrás hacia Adelante (Inducción Hacia Atrás):\n"
            f"1. Se establece la condición de frontera en el nodo destino: f*({destination}) = 0.\n"
            f"2. Se evalúa recursivamente en sentido inverso cada etapa k mediante la ecuación de Bellman:\n"
            f"   f_n*(s) = min_{{x}} [ c(s, x) + f_{{n+1}}^*(x) ]\n"
            f"3. Al alcanzar el nodo origen {source}, se obtiene el costo mínimo total de {f_cost[source]}.\n"
            f"4. Siguiendo las decisiones óptimas x*(s) desde {source} hasta {destination}, la ruta es: "
            f"{' -> '.join(str(n) for n in optimal_path)}."
        )

        return ShortestPathResult(
            algorithm_name="Programación Dinámica (De Atrás hacia Adelante)",
            source=source,
            destination=destination,
            total_cost=f_cost[source],
            optimal_path=optimal_path,
            stages=stages,
            intermediate_data={
                "costs": f_cost,
                "decisions": decision,
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

    def _build_backward_stage_tables(
        self,
        graph: Graph,
        rev_order: List[int],
        destination: int,
        evaluations_by_node: Dict[int, Dict[int, float]],
        f_cost: Dict[int, float],
        decision: Dict[int, Optional[int]],
    ) -> List[StageTable]:
        # Compute step depth from destination to group into stages
        depth_from_dest: Dict[int, int] = {destination: 0}
        for u in rev_order:
            if u not in depth_from_dest:
                # Find min depth among successors
                sucs = [depth_from_dest[v] for v, _ in graph.get_successors(u) if v in depth_from_dest]
                if sucs:
                    depth_from_dest[u] = min(sucs) + 1
                else:
                    depth_from_dest[u] = 99

        # Group nodes by stage (depth)
        stages_dict: Dict[int, List[int]] = defaultdict(list)
        for u in rev_order:
            if u == destination or u not in evaluations_by_node:
                continue
            stage_num = depth_from_dest.get(u, 1)
            stages_dict[stage_num].append(u)

        stage_tables: List[StageTable] = []
        for stage_idx, s_num in enumerate(sorted(stages_dict.keys()), start=1):
            nodes_in_stage = stages_dict[s_num]
            rows: List[StageTableRow] = []
            for u in sorted(nodes_in_stage):
                evals = evaluations_by_node.get(u, {})
                cands = sorted(list(evals.keys()))
                opt_cost = f_cost.get(u, float("inf"))
                opt_dec = decision.get(u)
                rows.append(
                    StageTableRow(
                        state=u,
                        candidate_decisions=cands,
                        evaluations=evals,
                        optimal_cost=opt_cost,
                        optimal_decision=opt_dec,
                    )
                )

            stage_tables.append(
                StageTable(
                    stage_number=stage_idx,
                    stage_name=f"Etapa {stage_idx} (Hacia Atrás, distancia {s_num} al destino)",
                    description=f"Evaluación de estados {nodes_in_stage} minimizando c(s, x) + f*(x)",
                    rows=rows,
                )
            )

        return stage_tables
