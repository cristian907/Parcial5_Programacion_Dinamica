"""Floyd-Warshall Algorithm Solver."""
from typing import Dict, List, Optional
from ...application.interfaces import IShortestPathSolver
from ...domain.entities import Graph
from ...domain.exceptions import NegativeCycleError, NodeNotFoundError, PathNotFoundError
from ...domain.models import ShortestPathResult, StageTable, StageTableRow


class FloydWarshallSolver(IShortestPathSolver):
    """Solves all-pairs shortest paths using the Floyd-Warshall Dynamic Programming algorithm:
    D^(k)[i][j] = min(D^(k-1)[i][j], D^(k-1)[i][k] + D^(k-1)[k][j])
    """

    def solve(self, graph: Graph, source: int, destination: int) -> ShortestPathResult:
        if source not in graph.nodes:
            raise NodeNotFoundError(f"El nodo origen {source} no existe en el grafo.")
        if destination not in graph.nodes:
            raise NodeNotFoundError(f"El nodo destino {destination} no existe en el grafo.")

        nodes = graph.get_node_ids()
        n = len(nodes)
        node_to_idx = {nid: idx for idx, nid in enumerate(nodes)}
        idx_to_node = {idx: nid for idx, nid in enumerate(nodes)}

        # Distance matrix D and Next-node matrix Next for path reconstruction
        dist = [[float("inf")] * n for _ in range(n)]
        nxt: List[List[Optional[int]]] = [[None] * n for _ in range(n)]

        for i in range(n):
            dist[i][i] = 0.0

        for edge in graph.edges:
            u_idx = node_to_idx[edge.source]
            v_idx = node_to_idx[edge.target]
            if edge.weight < dist[u_idx][v_idx]:
                dist[u_idx][v_idx] = edge.weight
                nxt[u_idx][v_idx] = v_idx

        # Snapshot history for key intermediate stages
        matrix_history: List[Dict[str, Any]] = [{
            "k_node": None,
            "dist_matrix": [row[:] for row in dist],
            "next_matrix": [row[:] for row in nxt],
        }]

        stage_tables: List[StageTable] = []

        # Run Floyd-Warshall considering each vertex k as intermediate node
        for k in range(n):
            k_node = idx_to_node[k]
            improved_pairs: List[Tuple[int, int, float]] = []

            for i in range(n):
                for j in range(n):
                    if dist[i][k] != float("inf") and dist[k][j] != float("inf"):
                        through_k = dist[i][k] + dist[k][j]
                        if through_k < dist[i][j]:
                            dist[i][j] = through_k
                            nxt[i][j] = nxt[i][k]
                            improved_pairs.append((idx_to_node[i], idx_to_node[j], through_k))

            matrix_history.append({
                "k_node": k_node,
                "dist_matrix": [row[:] for row in dist],
                "next_matrix": [row[:] for row in nxt],
            })

            # For the stage table, show focus on transitions from source or to destination
            src_idx = node_to_idx[source]
            rows: List[StageTableRow] = []
            for j in range(n):
                target_node = idx_to_node[j]
                current_cost = dist[src_idx][j]
                next_hop = idx_to_node[nxt[src_idx][j]] if nxt[src_idx][j] is not None else None
                rows.append(
                    StageTableRow(
                        state=target_node,
                        candidate_decisions=[k_node],
                        evaluations={k_node: current_cost},
                        optimal_cost=current_cost,
                        optimal_decision=next_hop,
                    )
                )

            stage_tables.append(
                StageTable(
                    stage_number=k + 1,
                    stage_name=f"Etapa {k + 1}: Nodo intermedio k = {k_node}",
                    description=(
                        f"Evaluando paso por {k_node}. "
                        + (f"{len(improved_pairs)} pares mejorados." if improved_pairs else "Sin mejoras directas.")
                    ),
                    rows=rows,
                )
            )

        # Negative cycle check on diagonals
        for i in range(n):
            if dist[i][i] < 0:
                raise NegativeCycleError(f"Ciclo negativo detectado en el nodo {idx_to_node[i]}.")

        s_idx = node_to_idx[source]
        d_idx = node_to_idx[destination]

        if dist[s_idx][d_idx] == float("inf"):
            raise PathNotFoundError(f"No existe camino desde {source} hasta {destination}.")

        # Reconstruct path using nxt matrix
        optimal_path: List[int] = [source]
        curr_idx = s_idx
        while curr_idx != d_idx:
            curr_idx = nxt[curr_idx][d_idx]
            if curr_idx is None:
                raise PathNotFoundError(f"No se pudo completar la reconstrucción de ruta.")
            optimal_path.append(idx_to_node[curr_idx])

        explanation = (
            f"Algoritmo Floyd-Warshall (Todos los pares de caminos más cortos):\n"
            f"1. Complejidad: O(V³). Evalúa recursivamente D^(k)[i][j] = min(D^(k-1)[i][j], D^(k-1)[i][k] + D^(k-1)[k][j]).\n"
            f"2. Se procesaron {n} etapas intermedias (un paso por cada nodo del grafo).\n"
            f"3. La distancia óptima final entre origen {source} y destino {destination} es {dist[s_idx][d_idx]}.\n"
            f"4. Ruta óptima recuperada: {' -> '.join(str(n) for n in optimal_path)}."
        )

        return ShortestPathResult(
            algorithm_name="Floyd-Warshall",
            source=source,
            destination=destination,
            total_cost=dist[s_idx][d_idx],
            optimal_path=optimal_path,
            stages=stage_tables,
            intermediate_data={
                "nodes": nodes,
                "node_to_idx": node_to_idx,
                "idx_to_node": idx_to_node,
                "dist_matrix": dist,
                "next_matrix": nxt,
                "matrix_history": matrix_history,
            },
            explanation=explanation,
        )
