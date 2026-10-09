"""Bellman-Ford Algorithm Solver."""
from typing import Dict, List, Optional
from ...application.interfaces import IShortestPathSolver
from ...domain.entities import Graph
from ...domain.exceptions import NegativeCycleError, NodeNotFoundError, PathNotFoundError
from ...domain.models import ShortestPathResult, StageTable, StageTableRow


class BellmanFordSolver(IShortestPathSolver):
    """Solves shortest path using the Bellman-Ford algorithm with step-by-step iteration recording."""

    def solve(self, graph: Graph, source: int, destination: int) -> ShortestPathResult:
        if source not in graph.nodes:
            raise NodeNotFoundError(f"El nodo origen {source} no existe en el grafo.")
        if destination not in graph.nodes:
            raise NodeNotFoundError(f"El nodo destino {destination} no existe en el grafo.")

        nodes = graph.get_node_ids()
        num_vertices = len(nodes)

        # dist[v]: current shortest distance from source to v
        dist: Dict[int, float] = {v: float("inf") for v in nodes}
        pred: Dict[int, Optional[int]] = {v: None for v in nodes}
        dist[source] = 0.0

        iteration_history: List[Dict[str, Dict[int, Any]]] = []
        stage_tables: List[StageTable] = []

        # Relax edges up to |V| - 1 times
        for i in range(1, num_vertices):
            changed = False
            prev_dist = dist.copy()
            prev_pred = pred.copy()
            evals_this_round: Dict[int, Dict[int, float]] = {v: {} for v in nodes}

            for edge in graph.edges:
                u, v, w = edge.source, edge.target, edge.weight
                if prev_dist[u] != float("inf"):
                    new_cost = prev_dist[u] + w
                    evals_this_round[v][u] = new_cost
                    if new_cost < dist[v]:
                        dist[v] = new_cost
                        pred[v] = u
                        changed = True

            iteration_history.append({
                "iteration": i,
                "dist": dist.copy(),
                "pred": pred.copy(),
            })

            # Create an iteration stage table
            rows: List[StageTableRow] = []
            for v in nodes:
                cands = list(evals_this_round[v].keys())
                rows.append(
                    StageTableRow(
                        state=v,
                        candidate_decisions=cands,
                        evaluations=evals_this_round[v],
                        optimal_cost=dist[v],
                        optimal_decision=pred[v],
                    )
                )

            stage_tables.append(
                StageTable(
                    stage_number=i,
                    stage_name=f"Iteración {i} (Relajación de aristas)",
                    description=(
                        f"Iteración {i}/{num_vertices - 1}. "
                        + ("Hubo actualizaciones de distancia." if changed else "No hubo cambios (convergencia temprana).")
                    ),
                    rows=rows,
                )
            )

            # Optimization: if no distances changed, algorithm has converged
            if not changed:
                break

        # Check for negative-weight cycles (|V|-th iteration)
        for edge in graph.edges:
            u, v, w = edge.source, edge.target, edge.weight
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                raise NegativeCycleError("El grafo contiene un ciclo de peso negativo accesible desde el origen.")

        if dist[destination] == float("inf"):
            raise PathNotFoundError(f"No existe camino desde {source} hasta {destination}.")

        # Reconstruct optimal path
        optimal_path: List[int] = []
        curr: Optional[int] = destination
        visited = set()
        while curr is not None:
            optimal_path.append(curr)
            visited.add(curr)
            if curr == source:
                break
            curr = pred.get(curr)
            if curr in visited:
                break
        optimal_path.reverse()

        explanation = (
            f"Algoritmo Bellman-Ford:\n"
            f"1. Complejidad: O(V · E). Capaz de detectar ciclos negativos y manejar pesos arbitrarios.\n"
            f"2. Se ejecutaron {len(iteration_history)} iteraciones de relajación de aristas.\n"
            f"3. La distancia mínima final calculada desde {source} hasta {destination} es {dist[destination]}.\n"
            f"4. Ruta óptima recuperada: {' -> '.join(str(n) for n in optimal_path)}."
        )

        return ShortestPathResult(
            algorithm_name="Bellman-Ford",
            source=source,
            destination=destination,
            total_cost=dist[destination],
            optimal_path=optimal_path,
            stages=stage_tables,
            intermediate_data={
                "distances": dist,
                "predecessors": pred,
                "iterations": iteration_history,
            },
            explanation=explanation,
        )
