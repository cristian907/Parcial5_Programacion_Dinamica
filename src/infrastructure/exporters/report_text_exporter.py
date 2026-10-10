"""Exporter to generate the complete academic text report."""
from typing import List
from ...application.interfaces import ITextExporter
from ...domain.models import AlgorithmComparison, KnapsackResult, ShortestPathResult


class ReportTextExporter(ITextExporter):
    """Generates an academic, cleanly formatted plain text report of all problem outputs."""

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
        lines: List[str] = []

        def sep(title: str = "") -> None:
            if title:
                lines.append("=" * 76)
                lines.append(f"  {title.upper()}")
                lines.append("=" * 76)
            else:
                lines.append("=" * 76)

        def subsep(title: str = "") -> None:
            lines.append("-" * 76)
            if title:
                lines.append(f"  {title}")
                lines.append("-" * 76)

        sep("UNIVERSIDAD JOSÉ ANTONIO PÁEZ - FACULTAD DE INGENIERÍA")
        lines.append("ESCUELA DE INGENIERÍA EN COMPUTACIÓN")
        lines.append("PARCIAL V: PROGRAMACIÓN DINÁMICA")
        lines.append("INFORME DE SALIDAS Y RESOLUCIÓN COMPUTACIONAL")
        sep()
        lines.append("")

        # ---------------------------------------------------------------------
        # SECCIÓN 1: PROBLEMA 1 (GRAFO Y RUTAS MÁS CORTAS)
        # ---------------------------------------------------------------------
        sep("1. PROBLEMA 1: RUTA MÁS CORTA EN GRAFO POR PROGRAMACIÓN DINÁMICA")
        lines.append("Nodo Origen : 1 (Oficina anterior)")
        lines.append("Nodo Destino: 13 (Oficina nueva)")
        lines.append("")

        # a) Adelante hacia Atrás
        subsep("a) Programación Dinámica: Adelante hacia Atrás (Forward DP)")
        lines.append(forward_res.explanation)
        lines.append(f"Ruta Óptima: {' -> '.join(str(n) for n in forward_res.optimal_path)}")
        lines.append(f"Costo Mínimo Total: {forward_res.total_cost:.2f}")
        lines.append("")
        lines.append("Tablas de Etapas (Forward):")
        for st in forward_res.stages:
            lines.append(f"  [{st.stage_name}]: {st.description}")
            for r in st.rows:
                evals_str = ", ".join(f"{p} -> {c:.0f}" for p, c in sorted(r.evaluations.items()))
                lines.append(f"    * Estado {r.state:2d} | Evals: [{evals_str}] | f*={r.optimal_cost:.0f} | Decisión x*={r.optimal_decision}")
        lines.append("")

        # b) De Atrás hacia Adelante
        subsep("b) Programación Dinámica: De Atrás hacia Adelante (Backward DP)")
        lines.append(backward_res.explanation)
        lines.append(f"Ruta Óptima: {' -> '.join(str(n) for n in backward_res.optimal_path)}")
        lines.append(f"Costo Mínimo Total: {backward_res.total_cost:.2f}")
        lines.append("")
        lines.append("Tablas de Etapas (Backward):")
        for st in backward_res.stages:
            lines.append(f"  [{st.stage_name}]: {st.description}")
            for r in st.rows:
                evals_str = ", ".join(f"{s} -> {c:.0f}" for s, c in sorted(r.evaluations.items()))
                lines.append(f"    * Estado {r.state:2d} | Evals: [{evals_str}] | f*={r.optimal_cost:.0f} | Decisión x*={r.optimal_decision}")
        lines.append("")

        # c) Bellman-Ford y Floyd-Warshall
        subsep("c) Algoritmos Bellman-Ford y Floyd-Warshall (Python) y Explicación")
        lines.append("--- BELLMAN-FORD ---")
        lines.append(bellman_res.explanation)
        lines.append(f"Ruta: {' -> '.join(str(n) for n in bellman_res.optimal_path)} | Costo: {bellman_res.total_cost:.2f}")
        lines.append("")
        lines.append("--- FLOYD-WARSHALL ---")
        lines.append(floyd_res.explanation)
        lines.append(f"Ruta: {' -> '.join(str(n) for n in floyd_res.optimal_path)} | Costo: {floyd_res.total_cost:.2f}")
        lines.append("")
        lines.append("--- COMPARACIÓN DE COMPLEJIDAD Y EQUIVALENCIA TEÓRICA ---")
        lines.append(comparison.summary)
        lines.append(comparison.theoretical_notes)
        for algo in comparison.algorithms_evaluated:
            lines.append(f"  - {algo}: Costo = {comparison.costs[algo]}, Complejidad = {comparison.complexities[algo]}")
        lines.append("")

        # ---------------------------------------------------------------------
        # SECCIÓN 2: PROBLEMA 2 (VOLUMEN DE CARGA)
        # ---------------------------------------------------------------------
        sep("2. PROBLEMA 2: PROBLEMA DE VOLUMEN DE CARGA (ALGORITMO VOLUMENCARGA)")
        lines.append(f"Capacidad máxima de carga: {knapsack_res.capacity} kg")
        lines.append("Productos disponibles:")
        lines.append("  1. Tablet Samsung      | Peso: 2 kg | Precio: $40")
        lines.append("  2. Dron DJI Mini        | Peso: 3 kg | Precio: $50")
        lines.append("  3. Proyector portátil   | Peso: 4 kg | Precio: $65")
        lines.append("  4. Laptop ASUS ZenBook  | Peso: 5 kg | Precio: $60")
        lines.append("")
        subsep("Resolución Paso a Paso por Etapas:")
        for exp in knapsack_res.stage_explanations:
            lines.append(exp)
            lines.append("")

        subsep("Matriz de Estados de Programación Dinámica V[i][w]:")
        lines.extend(self._format_compact_dp_table(knapsack_res))
        lines.append("")

        subsep("Paquetes Seleccionados y Valor Total Máximo (Respuestas Oficiales):")
        lines.append("Paquetes que se deben llevar al stand:")
        for it in knapsack_res.selected_items:
            lines.append(f"  -> {it.name} (Peso: {it.weight:.1f} kg, Valor: ${it.price:.2f})")
        lines.append("")
        lines.append(f"Peso Total Ocupado : {knapsack_res.total_weight:.1f} kg")
        lines.append(f"Espacio Libre      : {knapsack_res.slack_capacity:.1f} kg (Holgura)")
        lines.append(f"VALOR TOTAL MÁXIMO : ${knapsack_res.total_value:.2f}")
        lines.append("")

        subsep("Análisis de Resultados y Conclusión (Redacción para Examen):")
        lines.append(knapsack_res.conclusion)
        sep("FIN DEL REPORTE ACADÉMICO")

        content = "\n".join(lines)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return content

    def _format_compact_dp_table(self, knapsack_res: KnapsackResult) -> List[str]:
        """Formats the DP matrix into a clean, compact ASCII table that fits within 76 columns."""
        output_lines: List[str] = []
        weights = knapsack_res.weights_header
        total_w = len(weights)
        chunk_size = 11  # Capacities 0 to 10 per table chunk

        col0_w = 17
        item_labels = [
            "Base f0(w)",
            "1. Tablet (2kg)",
            "2. Dron (3kg)",
            "3. Proyector(4kg)",
            "4. Laptop (5kg)",
        ]

        # Chunk columns to guarantee max width <= 76 chars in any scenario
        for start_idx in range(0, total_w, chunk_size):
            end_idx = min(start_idx + chunk_size, total_w)
            chunk_weights = weights[start_idx:end_idx]

            border = "+" + "-" * (col0_w + 2) + "+" + "+".join(["----"] * len(chunk_weights)) + "+"
            header = "| " + "Capacidad (kg)".ljust(col0_w) + " |" + "".join(f"{int(w):>3} |" for w in chunk_weights)

            output_lines.append(border)
            output_lines.append(header)
            output_lines.append(border)

            for i, row in enumerate(knapsack_res.dp_table):
                label = item_labels[i] if i < len(item_labels) else f"Etapa {i}"
                chunk_vals = row[start_idx:end_idx]
                row_cells = "".join(f"{int(v):>3} |" for v in chunk_vals)
                output_lines.append(f"| {label[:col0_w].ljust(col0_w)} |{row_cells}")

            output_lines.append(border)

        return output_lines
