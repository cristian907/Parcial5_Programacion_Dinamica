"""Preloaded exam problems and data from Parcial V."""
from typing import List
from ...application.interfaces import IPreloadedDataRepository
from ...domain.entities import Edge, Graph, Item, KnapsackProblem, TrueFalseQuestion


class ParcialVPreloadedRepository(IPreloadedDataRepository):
    """Provides the preloaded problems exactly as defined in the Parcial V examination."""

    def get_default_graph(self) -> Graph:
        g = Graph(name="Grafo Parcial V - UJAP (Ruta más Corta)")

        # Coordinates mapped visually to match the exam graph diagram layout
        # (x from 50 to 750, y from 60 to 440)
        nodes_data = [
            (1, "1 (Oficina anterior)", 60, 240),
            (2, "2", 180, 110),
            (3, "3", 180, 240),
            (4, "4", 180, 370),
            (5, "5", 300, 180),
            (6, "6", 300, 370),
            (7, "7", 420, 110),
            (8, "8", 420, 240),
            (9, "9", 420, 410),
            (10, "10", 540, 160),
            (11, "11", 540, 370),
            (12, "12", 640, 410),
            (13, "13 (Oficina nueva)", 660, 190),
        ]

        for nid, lbl, x, y in nodes_data:
            g.add_node(nid, lbl, float(x), float(y))

        edges_data = [
            (1, 2, 100.0),
            (1, 3, 50.0),
            (1, 4, 40.0),
            (3, 4, 20.0),
            (2, 5, 100.0),
            (3, 5, 100.0),
            (4, 6, 100.0),
            (5, 6, 40.0),
            (5, 7, 120.0),
            (5, 8, 130.0),
            (7, 8, 50.0),
            (6, 9, 100.0),
            (8, 9, 100.0),
            (7, 10, 60.0),
            (8, 10, 70.0),
            (9, 11, 100.0),
            (10, 13, 100.0),
            (10, 12, 200.0),
            (11, 12, 50.0),
            (12, 13, 100.0),
        ]

        for src, tgt, w in edges_data:
            g.add_edge(src, tgt, w)

        return g

    def get_default_knapsack_problem(self) -> KnapsackProblem:
        kp = KnapsackProblem(
            name="Problema de Volumen de Carga (Stand Feria Tecnológica)",
            capacity=10.0,
            allow_repetition=False
        )
        kp.add_item(1, "Tablet Samsung", 2.0, 40.0)
        kp.add_item(2, "Dron DJI Mini", 3.0, 50.0)
        kp.add_item(3, "Proyector portátil", 4.0, 65.0)
        kp.add_item(4, "Laptop ASUS ZenBook", 5.0, 60.0)
        return kp

    def get_theoretical_questions(self) -> List[TrueFalseQuestion]:
        return [
            TrueFalseQuestion(
                id="1.a",
                statement="Si un problema tiene subproblemas superpuestos pero no cumple con el principio de optimalidad, puede resolverse eficientemente con programación dinámica.",
                correct_answer=False,
                justification=(
                    "FALSO. Para que la Programación Dinámica sea aplicable y garantice la solución global óptima, "
                    "el problema debe satisfacer OBLIGATORIAMENTE dos propiedades fundamentales: subproblemas superpuestos "
                    "y subestructura óptima (Principio de Optimalidad de Bellman). Si no cumple con el principio de "
                    "optimalidad (por ejemplo, el problema del camino simple más largo sin pesos negativos, o problemas "
                    "donde las decisiones pasadas imponen restricciones acumulativas irreversibles), las decisiones óptimas "
                    "de los subproblemas no componen necesariamente una solución global óptima."
                )
            ),
            TrueFalseQuestion(
                id="1.b",
                statement="El algoritmo de Floyd-Warshall para rutas más cortas aplica programación dinámica, evaluando todas las posibles rutas intermedias entre pares de nodos.",
                correct_answer=True,
                justification=(
                    "VERDADERO. Floyd-Warshall es un clásico algoritmo de Programación Dinámica que calcula la ruta más corta "
                    "entre todos los pares de nodos (all-pairs shortest paths). Su ecuación de recurrencia es "
                    "D^(k)[i][j] = min(D^(k-1)[i][j], D^(k-1)[i][k] + D^(k-1)[k][j]), donde en cada etapa k evalúa si el "
                    "vértice k puede utilizarse como un nodo intermedio admisible para acortar el camino entre cada par (i, j)."
                )
            ),
            TrueFalseQuestion(
                id="1.c",
                statement="En un problema de volumen de carga, si todos los paquetes tienen pesos que son múltiplos de un mismo valor, se puede reducir el espacio de la tabla de programación dinámica sin afectar la solución óptima.",
                correct_answer=True,
                justification=(
                    "VERDADERO. Si todos los pesos w_i y la capacidad W son múltiplos de un factor común g = mcd(w_1, ..., w_n, W), "
                    "se puede dividir toda la escala por g (w'_i = w_i / g, W' = ⌊W / g⌋). Esto reduce el número de columnas de la tabla "
                    "de estados discretos en un factor de g, reduciendo drásticamente el espacio en memoria y el tiempo de cálculo "
                    "sin alterar en absoluto las decisiones óptimas ni la solución final."
                )
            ),
            TrueFalseQuestion(
                id="1.d",
                statement="La programación dinámica puede adaptarse para resolver problemas de múltiples restricciones, como capacidad de peso y volumen simultáneamente.",
                correct_answer=True,
                justification=(
                    "VERDADERO. Esto corresponde a la Mochila Multidimensional (Multi-dimensional Knapsack Problem). "
                    "La Programación Dinámica se adapta generalizando el estado a un vector multi-dimensional: "
                    "f_i(w, v) = max(f_{i-1}(w, v), f_{i-1}(w - w_i, v - v_i) + p_i), donde cada restricción adicional "
                    "(como volumen, peso, fragilidad) agrega una dimensión a la tabla de estados."
                )
            ),
            TrueFalseQuestion(
                id="1.e",
                statement="La solución óptima de un problema de volumen de carga puede involucrar dejar espacio libre en la mochila.",
                correct_answer=True,
                justification=(
                    "VERDADERO. En problemas de optimización con variables enteras discretas (mochila 0/1), el objetivo "
                    "es MAXIMIZAR el valor total, no obligatoriamente saturar el 100% de la capacidad disponible. "
                    "De hecho, en el Problema 2 de este examen, la solución óptima selecciona Tablet (2 kg) + Dron (3 kg) + "
                    "Proyector (4 kg) = 9 kg con valor $155, dejando 1 kg de capacidad libre, ya que intentar forzar 10 kg con "
                    "la Laptop ZenBook (5 kg) produce combinaciones de menor valor ($150)."
                )
            ),
        ]
