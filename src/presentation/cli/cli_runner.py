"""Command-line interface runner for Parcial V Dynamic Programming."""
from ...infrastructure.repositories.preloaded_data import ParcialVPreloadedRepository
from ...infrastructure.solvers.forward_dp_solver import ForwardDPSolver
from ...infrastructure.solvers.backward_dp_solver import BackwardDPSolver
from ...infrastructure.solvers.bellman_ford_solver import BellmanFordSolver
from ...infrastructure.solvers.floyd_warshall_solver import FloydWarshallSolver
from ...infrastructure.solvers.knapsack_dp_solver import KnapsackDPSolver
from ...infrastructure.exporters.report_text_exporter import ReportTextExporter
from ...application.use_cases.compare_algorithms import CompareAlgorithmsUseCase
from ...application.use_cases.export_reports import ExportReportUseCase


def run_cli(export_path: str = "reporte_problema.txt") -> None:
    print("=" * 80)
    print("  UNIVERSIDAD JOSÉ ANTONIO PÁEZ - FACULTAD DE INGENIERÍA")
    print("  PARCIAL V: PROGRAMACIÓN DINÁMICA (RESOLUCIÓN AUTOMATIZADA)")
    print("=" * 80)

    repo = ParcialVPreloadedRepository()
    graph = repo.get_default_graph()
    knapsack = repo.get_default_knapsack_problem()

    print("\n[1/3] Resolviendo Problema 1: Rutas más cortas...")
    forward_solver = ForwardDPSolver()
    backward_solver = BackwardDPSolver()
    bellman_solver = BellmanFordSolver()
    floyd_solver = FloydWarshallSolver()

    src = 1
    dst = 13

    res_fwd = forward_solver.solve(graph, src, dst)
    res_bwd = backward_solver.solve(graph, src, dst)
    res_bell = bellman_solver.solve(graph, src, dst)
    res_floyd = floyd_solver.solve(graph, src, dst)

    comparator = CompareAlgorithmsUseCase()
    comp_res = comparator.execute(res_fwd, res_bwd, res_bell, res_floyd)

    print(f"  -> Forward DP      : Costo = {res_fwd.total_cost:.1f} | Ruta: {res_fwd.optimal_path}")
    print(f"  -> Backward DP     : Costo = {res_bwd.total_cost:.1f} | Ruta: {res_bwd.optimal_path}")
    print(f"  -> Bellman-Ford    : Costo = {res_bell.total_cost:.1f} | Ruta: {res_bell.optimal_path}")
    print(f"  -> Floyd-Warshall  : Costo = {res_floyd.total_cost:.1f} | Ruta: {res_floyd.optimal_path}")
    print(f"  -> Consenso        : {comp_res.summary}")

    print("\n[2/3] Resolviendo Problema 2: Volumen de Carga (10 kg)...")
    knapsack_solver = KnapsackDPSolver()
    res_knap = knapsack_solver.solve(knapsack)

    print(f"  -> Algoritmo       : {res_knap.algorithm_name}")
    print(f"  -> Capacidad       : {res_knap.capacity} kg")
    print(f"  -> Peso Utilizado  : {res_knap.total_weight:.1f} kg (Holgura libre: {res_knap.slack_capacity:.1f} kg)")
    print(f"  -> Valor Máximo    : ${res_knap.total_value:.2f}")
    selected_names = [it.name for it in res_knap.selected_items]
    print(f"  -> Paquetes Óptimos: {', '.join(selected_names)}")

    print(f"\n[3/3] Exportando reporte oficial del problema...")
    exporter = ReportTextExporter()
    export_uc = ExportReportUseCase(exporter)
    export_uc.execute(
        forward_res=res_fwd,
        backward_res=res_bwd,
        bellman_res=res_bell,
        floyd_res=res_floyd,
        knapsack_res=res_knap,
        comparison=comp_res,
        file_path=export_path
    )
    print(f"  -> Archivo generado exitosamente: '{export_path}'")
    print("=" * 80)


if __name__ == "__main__":
    run_cli()
