"""Use case for comparing graph shortest path algorithms."""
from typing import Dict, List
from ...domain.models import AlgorithmComparison, ShortestPathResult


class CompareAlgorithmsUseCase:
    """Produces structured comparison and academic explanation for exam resolution."""

    def execute(
        self,
        forward_res: ShortestPathResult,
        backward_res: ShortestPathResult,
        bellman_res: ShortestPathResult,
        floyd_res: ShortestPathResult
    ) -> AlgorithmComparison:
        algos = [
            forward_res.algorithm_name,
            backward_res.algorithm_name,
            bellman_res.algorithm_name,
            floyd_res.algorithm_name,
        ]

        costs = {
            forward_res.algorithm_name: forward_res.total_cost,
            backward_res.algorithm_name: backward_res.total_cost,
            bellman_res.algorithm_name: bellman_res.total_cost,
            floyd_res.algorithm_name: floyd_res.total_cost,
        }

        paths = {
            forward_res.algorithm_name: forward_res.optimal_path,
            backward_res.algorithm_name: backward_res.optimal_path,
            bellman_res.algorithm_name: bellman_res.optimal_path,
            floyd_res.algorithm_name: floyd_res.optimal_path,
        }

        complexities = {
            forward_res.algorithm_name: "O(V + E) sobre DAG estructurado en etapas",
            backward_res.algorithm_name: "O(V + E) sobre DAG estructurado en etapas",
            bellman_res.algorithm_name: "O(V · E) para cualquier grafo dirigido sin ciclos negativos",
            floyd_res.algorithm_name: "O(V³) calcula todos los pares de nodos simultáneamente",
        }

        # Check if all reached the same cost
        unique_costs = set(costs.values())
        is_consistent = len(unique_costs) == 1

        summary = (
            f"Todos los algoritmos convergen al costo óptimo de {forward_res.total_cost} "
            f"con la ruta {forward_res.optimal_path}."
            if is_consistent
            else "Se detectaron discrepancias entre los algoritmos evaluados."
        )

        theoretical_notes = (
            "1. Equivalencia Teórica: Dado que el grafo del Parcial V es un grafo acíclico dirigido (DAG) "
            "y cumple con el Principio de Optimalidad de Bellman, los enfoques de Programación Dinámica "
            "(Adelante y Atrás) descomponen el problema en etapas de decisión idénticas en costo final.\n"
            "2. Bellman-Ford confirma la ausencia de ciclos negativos relajando todas las aristas |V|-1 veces, "
            "obteniendo la misma distancia mínima desde el nodo origen.\n"
            "3. Floyd-Warshall evalúa recursivamente todos los vértices intermedios k in {1..13}, "
            "confirmando que la submatriz D(13)[1][13] es idéntica a la distancia hallada por DP y Bellman-Ford."
        )

        return AlgorithmComparison(
            summary=summary,
            algorithms_evaluated=algos,
            costs=costs,
            paths=paths,
            complexities=complexities,
            theoretical_notes=theoretical_notes
        )
