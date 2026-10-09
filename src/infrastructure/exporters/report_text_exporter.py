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
                lines.append("=" * 80)
                lines.append(f"  {title.upper()}")
                lines.append("=" * 80)
            else:
                lines.append("=" * 80)

        def subsep(title: str = "") -> None:
            lines.append("-" * 80)
            if title:
                lines.append(f"  {title}")
                lines.append("-" * 80)

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
                evals_str = ", ".join(f"pred {p} -> {c:.1f}" for p, c in r.evaluations.items())
                lines.append(f"    * Estado {r.state:2d} | Evaluaciones: [{evals_str}] | f*={r.optimal_cost:.1f} | Decisión x*={r.optimal_decision}")
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
                evals_str = ", ".join(f"suc {s} -> {c:.1f}" for s, c in r.evaluations.items())
                lines.append(f"    * Estado {r.state:2d} | Evaluaciones: [{evals_str}] | f*={r.optimal_cost:.1f} | Decisión x*={r.optimal_decision}")
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
        headers = ["Etapa / Prod"] + [f"{int(w):2d}kg" for w in knapsack_res.weights_header]
        lines.append(" | ".join(f"{h:>12}" for h in headers))
        lines.append("-" * (14 * len(headers)))
        for i, row in enumerate(knapsack_res.dp_table):
            row_label = knapsack_res.items_header[i] if i < len(knapsack_res.items_header) else f"Etapa {i}"
            row_vals = [f"${v:>5.0f}" for v in row]
            lines.append(f"{row_label:>12} | " + " | ".join(f"{val:>12}" for val in row_vals))
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
