"""Graph Shortest Path Tab in PyQt6 with improved, balanced distribution."""
from typing import Optional
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QSplitter,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from ....domain.entities import Graph
from ....domain.models import AlgorithmComparison, ShortestPathResult
from ...controllers import GraphController
from ..components.graph_canvas import GraphCanvas
from ..components.stage_table_view import StageTableView


class GraphTab(QWidget):
    """Tab to configure, visualize, and solve graph shortest paths with modern responsive layout."""

    def __init__(self, controller: GraphController, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.controller = controller

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 12, 14, 12)
        main_layout.setSpacing(10)

        # -------------------------------------------------------------
        # 1. Top Control & Summary Header Strip
        # -------------------------------------------------------------
        header_card = QFrame()
        header_card.setStyleSheet(
            "QFrame { background-color: #131d2e; border: 1px solid #1e2e48; border-radius: 10px; }"
        )
        header_layout = QHBoxLayout(header_card)
        header_layout.setContentsMargins(14, 10, 14, 10)
        header_layout.setSpacing(10)

        # Left controls
        lbl_origen = QLabel("Origen:")
        lbl_origen.setStyleSheet("font-weight: 600; color: #94a3b8;")
        header_layout.addWidget(lbl_origen)

        self.combo_source = QComboBox()
        self.combo_source.setMinimumWidth(140)
        header_layout.addWidget(self.combo_source)

        lbl_destino = QLabel("Destino:")
        lbl_destino.setStyleSheet("font-weight: 600; color: #94a3b8;")
        header_layout.addWidget(lbl_destino)

        self.combo_dest = QComboBox()
        self.combo_dest.setMinimumWidth(140)
        header_layout.addWidget(self.combo_dest)

        lbl_algo = QLabel("Algoritmo:")
        lbl_algo.setStyleSheet("font-weight: 600; color: #94a3b8;")
        header_layout.addWidget(lbl_algo)

        self.combo_algo = QComboBox()
        self.combo_algo.setMinimumWidth(180)
        self.combo_algo.addItem("Forward DP (Adelante)", "forward")
        self.combo_algo.addItem("Backward DP (Atrás)", "backward")
        self.combo_algo.addItem("Bellman-Ford", "bellman")
        self.combo_algo.addItem("Floyd-Warshall", "floyd")
        self.combo_algo.addItem("Comparar Todos", "all")
        self.combo_algo.setCurrentIndex(4)  # Default all
        header_layout.addWidget(self.combo_algo)

        self.btn_solve = QPushButton("Calcular Ruta")
        self.btn_solve.setObjectName("btnPrimary")
        self.btn_solve.setMinimumWidth(115)
        self.btn_solve.clicked.connect(self._on_solve_clicked)
        header_layout.addWidget(self.btn_solve)

        self.btn_reset_graph = QPushButton("Restablecer")
        self.btn_reset_graph.clicked.connect(self._on_reset_graph)
        header_layout.addWidget(self.btn_reset_graph)

        header_layout.addStretch()

        # Right Summary Badges
        v_cost = QVBoxLayout()
        v_cost.setSpacing(2)
        lbl_c_title = QLabel("COSTO MÍNIMO")
        lbl_c_title.setStyleSheet("font-size: 10px; font-weight: 700; color: #64748b; letter-spacing: 0.5px;")
        self.lbl_cost = QLabel("--")
        self.lbl_cost.setStyleSheet("font-size: 20px; font-weight: 800; color: #10b981;")
        v_cost.addWidget(lbl_c_title)
        v_cost.addWidget(self.lbl_cost)
        header_layout.addLayout(v_cost)

        v_path = QVBoxLayout()
        v_path.setSpacing(2)
        lbl_p_title = QLabel("RUTA ÓPTIMA")
        lbl_p_title.setStyleSheet("font-size: 10px; font-weight: 700; color: #64748b; letter-spacing: 0.5px;")
        self.lbl_path = QLabel("--")
        self.lbl_path.setMinimumWidth(230)
        self.lbl_path.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.lbl_path.setStyleSheet("font-family: 'JetBrains Mono'; font-size: 13px; font-weight: 700; color: #38bdf8;")
        v_path.addWidget(lbl_p_title)
        v_path.addWidget(self.lbl_path)
        header_layout.addLayout(v_path)

        main_layout.addWidget(header_card)

        # -------------------------------------------------------------
        # 2. Main Content Splitter (Left: Canvas, Right: Results/Tables)
        # -------------------------------------------------------------
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setChildrenCollapsible(False)

        # Left Widget: Canvas + Compact Edge Editor
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)

        self.canvas = GraphCanvas()
        left_layout.addWidget(self.canvas, 1)

        # Compact Bottom Edge Editor
        edge_box = QGroupBox("Modificar Datos Variables (Aristas del Grafo)")
        edge_box.setStyleSheet("QGroupBox { margin-top: 14px; padding-top: 10px; }")
        edge_layout = QHBoxLayout(edge_box)
        edge_layout.setContentsMargins(10, 6, 10, 8)
        edge_layout.setSpacing(10)

        edge_layout.addWidget(QLabel("Origen U:"))
        self.spin_edge_u = QSpinBox()
        self.spin_edge_u.setRange(1, 99)
        self.spin_edge_u.setValue(1)
        self.spin_edge_u.setFixedWidth(55)
        edge_layout.addWidget(self.spin_edge_u)

        edge_layout.addWidget(QLabel("Destino V:"))
        self.spin_edge_v = QSpinBox()
        self.spin_edge_v.setRange(1, 99)
        self.spin_edge_v.setValue(2)
        self.spin_edge_v.setFixedWidth(55)
        edge_layout.addWidget(self.spin_edge_v)

        edge_layout.addWidget(QLabel("Peso:"))
        self.spin_edge_w = QDoubleSpinBox()
        self.spin_edge_w.setRange(-9999, 9999)
        self.spin_edge_w.setValue(100.0)
        self.spin_edge_w.setFixedWidth(85)
        edge_layout.addWidget(self.spin_edge_w)

        self.btn_add_edge = QPushButton("+ Guardar Arista")
        self.btn_add_edge.clicked.connect(self._on_add_edge)
        edge_layout.addWidget(self.btn_add_edge)

        self.btn_del_edge = QPushButton("Eliminar Arista")
        self.btn_del_edge.setObjectName("btnDanger")
        self.btn_del_edge.clicked.connect(self._on_del_edge)
        edge_layout.addWidget(self.btn_del_edge)

        edge_layout.addStretch()

        lbl_drag_hint = QLabel("💡 Arrastra los nodos con el mouse para reubicarlos")
        lbl_drag_hint.setStyleSheet("color: #64748b; font-size: 11px;")
        edge_layout.addWidget(lbl_drag_hint)

        left_layout.addWidget(edge_box)
        self.splitter.addWidget(left_widget)

        # Right Widget: Tabbed Details (Stage Tables, Comparison, Steps, All Edges)
        right_widget = QWidget()
        right_widget.setMinimumWidth(440)
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        self.detail_tabs = QTabWidget()
        self.detail_tabs.setStyleSheet("QTabBar::tab { padding: 7px 14px; font-size: 12px; }")

        # Sub-tab 1: Stage Decision Tables
        self.stage_table_view = StageTableView()
        self.detail_tabs.addTab(self.stage_table_view, "Tablas por Etapas (DP)")

        # Sub-tab 2: Algorithm Comparison
        self.tab_comparison = QWidget()
        comp_layout = QVBoxLayout(self.tab_comparison)
        comp_layout.setContentsMargins(8, 8, 8, 8)
        comp_layout.setSpacing(8)

        self.table_comparison = QTableWidget()
        self.table_comparison.setColumnCount(4)
        self.table_comparison.setHorizontalHeaderLabels(["Algoritmo", "Costo", "Ruta Hallada", "Complejidad"])
        self.table_comparison.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table_comparison.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table_comparison.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table_comparison.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table_comparison.verticalHeader().setVisible(False)
        self.table_comparison.setAlternatingRowColors(True)
        comp_layout.addWidget(self.table_comparison)

        self.lbl_comp_summary = QLabel("")
        self.lbl_comp_summary.setWordWrap(True)
        self.lbl_comp_summary.setStyleSheet("background: #090e17; padding: 10px; border-radius: 6px; color: #cbd5e1; font-size: 12px;")
        comp_layout.addWidget(self.lbl_comp_summary)

        self.detail_tabs.addTab(self.tab_comparison, "Comparativa de Algoritmos")

        # Sub-tab 3: Step-by-step Explanation
        self.tab_explanation = QWidget()
        exp_layout = QVBoxLayout(self.tab_explanation)
        exp_layout.setContentsMargins(8, 8, 8, 8)
        self.txt_explanation = QTextEdit()
        self.txt_explanation.setReadOnly(True)
        exp_layout.addWidget(self.txt_explanation)
        self.detail_tabs.addTab(self.tab_explanation, "Explicación Paso a Paso")

        # Sub-tab 4: Current Edge List
        self.tab_edges = QWidget()
        edges_list_layout = QVBoxLayout(self.tab_edges)
        edges_list_layout.setContentsMargins(8, 8, 8, 8)
        self.table_all_edges = QTableWidget()
        self.table_all_edges.setColumnCount(3)
        self.table_all_edges.setHorizontalHeaderLabels(["Nodo Origen", "Nodo Destino", "Peso"])
        self.table_all_edges.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_all_edges.verticalHeader().setVisible(False)
        self.table_all_edges.setAlternatingRowColors(True)
        self.table_all_edges.cellClicked.connect(self._on_edge_table_clicked)
        edges_list_layout.addWidget(self.table_all_edges)
        self.detail_tabs.addTab(self.tab_edges, "Lista de Aristas")

        right_layout.addWidget(self.detail_tabs)
        self.splitter.addWidget(right_widget)

        # Proportions: 60% canvas on left, 40% tables on right
        self.splitter.setStretchFactor(0, 6)
        self.splitter.setStretchFactor(1, 4)

        main_layout.addWidget(self.splitter, 1)

        # Initial load & solve
        self.reload_from_controller()
        self._on_solve_clicked()

    def reload_from_controller(self):
        graph = self.controller.get_graph()
        nodes = graph.get_node_ids()

        self.combo_source.blockSignals(True)
        self.combo_dest.blockSignals(True)
        self.combo_source.clear()
        self.combo_dest.clear()

        for nid in nodes:
            label = graph.nodes[nid].label
            self.combo_source.addItem(label, nid)
            self.combo_dest.addItem(label, nid)

        # Defaults: 1 and 13
        idx_1 = nodes.index(1) if 1 in nodes else 0
        idx_13 = nodes.index(13) if 13 in nodes else (len(nodes) - 1)
        self.combo_source.setCurrentIndex(idx_1)
        self.combo_dest.setCurrentIndex(idx_13)

        self.combo_source.blockSignals(False)
        self.combo_dest.blockSignals(False)

        self.canvas.set_graph(graph, 1, 13)
        self._refresh_edge_table()

    def _refresh_edge_table(self):
        edges = sorted(self.controller.get_graph().edges, key=lambda e: (e.source, e.target))
        self.table_all_edges.setRowCount(len(edges))
        for r, e in enumerate(edges):
            self.table_all_edges.setItem(r, 0, QTableWidgetItem(f"Nodo {e.source}"))
            self.table_all_edges.setItem(r, 1, QTableWidgetItem(f"Nodo {e.target}"))
            self.table_all_edges.setItem(r, 2, QTableWidgetItem(f"{e.weight:.1f}"))

    def _on_edge_table_clicked(self, row: int, col: int):
        edges = sorted(self.controller.get_graph().edges, key=lambda e: (e.source, e.target))
        if 0 <= row < len(edges):
            e = edges[row]
            self.spin_edge_u.setValue(e.source)
            self.spin_edge_v.setValue(e.target)
            self.spin_edge_w.setValue(e.weight)

    def _on_reset_graph(self):
        self.controller.reset_to_default_graph()
        self.reload_from_controller()
        self._on_solve_clicked()

    def _on_add_edge(self):
        u = self.spin_edge_u.value()
        v = self.spin_edge_v.value()
        w = self.spin_edge_w.value()
        self.controller.add_edge(u, v, w)
        self.canvas.set_graph(self.controller.get_graph(), self.combo_source.currentData(), self.combo_dest.currentData())
        self._refresh_edge_table()
        self._on_solve_clicked()

    def _on_del_edge(self):
        u = self.spin_edge_u.value()
        v = self.spin_edge_v.value()
        w = self.spin_edge_w.value()
        self.controller.remove_edge(u, v)
        self.canvas.set_graph(self.controller.get_graph(), self.combo_source.currentData(), self.combo_dest.currentData())
        self._refresh_edge_table()
        self._on_solve_clicked()

    def _on_solve_clicked(self):
        src = self.combo_source.currentData()
        dst = self.combo_dest.currentData()
        algo = self.combo_algo.currentData()

        if src is None or dst is None:
            return

        try:
            res, comparison = self.controller.solve(src, dst, algo)
            self.lbl_cost.setText(f"{res.total_cost:.1f}")
            path_str = " → ".join(str(n) for n in res.optimal_path)
            self.lbl_path.setText(path_str)

            self.canvas.set_endpoints(src, dst)
            self.canvas.set_optimal_path(res.optimal_path)

            self.stage_table_view.set_stages(res.stages)

            # Update comparison tab
            if comparison:
                self._update_comparison_table(comparison)
            else:
                _, comp_full = self.controller.solve(src, dst, "all")
                if comp_full:
                    self._update_comparison_table(comp_full)

            self.txt_explanation.setPlainText(res.explanation)
        except Exception as e:
            QMessageBox.critical(self, "Error al Resolver", str(e))

    def _update_comparison_table(self, comparison: AlgorithmComparison):
        algos = comparison.algorithms_evaluated
        self.table_comparison.setRowCount(len(algos))

        font_bold = QFont()
        font_bold.setBold(True)

        for r, a in enumerate(algos):
            item_a = QTableWidgetItem(a)
            item_a.setFont(font_bold)
            self.table_comparison.setItem(r, 0, item_a)

            cost_val = comparison.costs[a]
            item_c = QTableWidgetItem(f"{cost_val:.1f}")
            item_c.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_comparison.setItem(r, 1, item_c)

            path_val = " → ".join(str(n) for n in comparison.paths[a])
            item_p = QTableWidgetItem(path_val)
            self.table_comparison.setItem(r, 2, item_p)

            item_comp = QTableWidgetItem(comparison.complexities[a])
            self.table_comparison.setItem(r, 3, item_comp)

        self.lbl_comp_summary.setText(
            f"<b>Resumen de Consenso:</b> {comparison.summary}<br><br>"
            f"<b>Fundamentación Teórica:</b><br>{comparison.theoretical_notes.replace(chr(10), '<br>')}"
        )
