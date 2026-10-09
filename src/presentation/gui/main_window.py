"""Main GUI Window built with PyQt6."""
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QTabWidget,
)
from ...infrastructure.repositories.preloaded_data import ParcialVPreloadedRepository
from ..controllers import (
    GraphController,
    KnapsackController,
    ReportController,
)
from .styles.theme import DARK_THEME_QSS
from .tabs.graph_tab import GraphTab
from .tabs.knapsack_tab import KnapsackTab
from .tabs.report_tab import ReportTab


class MainWindow(QMainWindow):
    """Main desktop window for the Dynamic Programming application."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("UJAP - Parcial V: Programación Dinámica (Clean Architecture)")
        self.resize(1300, 850)
        self.setMinimumSize(1050, 700)

        # Repositories & Controllers
        repo = ParcialVPreloadedRepository()
        self.graph_controller = GraphController(repo)
        self.knapsack_controller = KnapsackController(repo)
        self.report_controller = ReportController(repo)

        # Main Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.tab_graph = GraphTab(self.graph_controller)
        self.tab_knapsack = KnapsackTab(self.knapsack_controller)
        self.tab_report = ReportTab(self.report_controller)

        self.tabs.addTab(self.tab_graph, "1. Grafo y Rutas más Cortas")
        self.tabs.addTab(self.tab_knapsack, "2. Volumen de Carga (Mochila)")
        self.tabs.addTab(self.tab_report, "3. Reporte del Problema (.txt)")

        self.setCentralWidget(self.tabs)

        # Status Bar
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Universidad José Antonio Páez • Escuela de Ingeniería en Computación • Métodos Cuantitativos")
        self.setStatusBar(self.status_bar)

        # Apply dark theme
        self.setStyleSheet(DARK_THEME_QSS)


def run_gui():
    """Entry point function to launch the desktop application."""
    app = QApplication(sys.argv)
    app.setApplicationName("ParcialV_ProgramacionDinamica")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()
