"""Use case for exporting the solution text report file."""
from ...domain.models import AlgorithmComparison, KnapsackResult, ShortestPathResult
from ..interfaces import ITextExporter


class ExportReportUseCase:
    """Coordinates generation and file writing of the complete academic output."""

    def __init__(self, exporter: ITextExporter) -> None:
        self._exporter = exporter

    def execute(
        self,
        forward_res: ShortestPathResult,
        backward_res: ShortestPathResult,
        bellman_res: ShortestPathResult,
        floyd_res: ShortestPathResult,
        knapsack_res: KnapsackResult,
        comparison: AlgorithmComparison,
        file_path: str = "reporte_problema.txt"
    ) -> str:
        return self._exporter.export_report(
            forward_res=forward_res,
            backward_res=backward_res,
            bellman_res=bellman_res,
            floyd_res=floyd_res,
            knapsack_res=knapsack_res,
            comparison=comparison,
            file_path=file_path
        )
