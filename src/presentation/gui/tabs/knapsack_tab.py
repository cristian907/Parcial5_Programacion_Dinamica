"""Cargo Volume (Knapsack) Tab in PyQt6."""
from typing import Optional
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from ....domain.entities import Item, KnapsackProblem
from ....domain.models import KnapsackResult
from ...controllers import KnapsackController
from ..components.dp_matrix_view import DPMatrixView


class KnapsackTab(QWidget):
    """Tab to configure, edit, and solve the Cargo Volume (Knapsack) problem."""

    def __init__(self, controller: KnapsackController, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.controller = controller

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(14)

        # -------------------------------------------------------------
        # Left Panel: Problem Configuration & Items Table (Width 380px)
        # -------------------------------------------------------------
        left_panel = QWidget()
        left_panel.setFixedWidth(380)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        grp_config = QGroupBox("Problema 2: Volumen de Carga")
        cfg_layout = QVBoxLayout(grp_config)
        cfg_layout.setSpacing(8)

        self.btn_reset = QPushButton("Restablecer Datos del Parcial V (10 kg)")
        self.btn_reset.clicked.connect(self._on_reset_clicked)
        cfg_layout.addWidget(self.btn_reset)

        h_cap = QHBoxLayout()
        h_cap.addWidget(QLabel("Capacidad Máxima (kg):"))
        self.spin_capacity = QDoubleSpinBox()
        self.spin_capacity.setRange(1.0, 500.0)
        self.spin_capacity.setValue(10.0)
        h_cap.addWidget(self.spin_capacity)
        cfg_layout.addLayout(h_cap)

        h_mode = QHBoxLayout()
        h_mode.addWidget(QLabel("Modo:"))
        self.combo_mode = QComboBox()
        self.combo_mode.addItem("0/1 Sin Repetición (Selección Única)", False)
        self.combo_mode.addItem("No Acotada (Con Repetición de Unidades)", True)
        h_mode.addWidget(self.combo_mode)
        cfg_layout.addLayout(h_mode)

        # Items Table
        cfg_layout.addWidget(QLabel("Productos Disponibles:"))
        self.table_items = QTableWidget()
        self.table_items.setColumnCount(3)
        self.table_items.setHorizontalHeaderLabels(["Producto", "Peso (kg)", "Precio ($)"])
        self.table_items.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table_items.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table_items.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table_items.verticalHeader().setVisible(False)
        self.table_items.setMaximumHeight(150)
        cfg_layout.addWidget(self.table_items)

        # Add Item inputs
        h_add = QHBoxLayout()
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Nombre")
        h_add.addWidget(self.input_name, 2)

        self.spin_weight = QDoubleSpinBox()
        self.spin_weight.setRange(0.5, 100.0)
        self.spin_weight.setValue(2.0)
        self.spin_weight.setPrefix("w:")
        h_add.addWidget(self.spin_weight, 1)

        self.spin_price = QDoubleSpinBox()
        self.spin_price.setRange(1.0, 9999.0)
        self.spin_price.setValue(40.0)
        self.spin_price.setPrefix("$:")
        h_add.addWidget(self.spin_price, 1)
        cfg_layout.addLayout(h_add)

        h_item_btns = QHBoxLayout()
        self.btn_add_item = QPushButton("+ Añadir Producto")
        self.btn_add_item.clicked.connect(self._on_add_item)
        h_item_btns.addWidget(self.btn_add_item)

        self.btn_del_item = QPushButton("- Eliminar Sel.")
        self.btn_del_item.setObjectName("btnDanger")
        self.btn_del_item.clicked.connect(self._on_del_item)
        h_item_btns.addWidget(self.btn_del_item)
        cfg_layout.addLayout(h_item_btns)

        self.btn_solve = QPushButton("Ejecutar Algoritmo VolumenCarga")
        self.btn_solve.setObjectName("btnPrimary")
        self.btn_solve.clicked.connect(self._on_solve_clicked)
        cfg_layout.addWidget(self.btn_solve)

        left_layout.addWidget(grp_config)

        # Summary Metrics
        grp_summary = QGroupBox("Resultados Óptimos")
        sum_layout = QVBoxLayout(grp_summary)
        sum_layout.setSpacing(6)

        h_m1 = QHBoxLayout()
        h_m1.addWidget(QLabel("Valor Total Máximo:"))
        self.lbl_value = QLabel("$0.00")
        self.lbl_value.setStyleSheet("font-size: 20px; font-weight: 800; color: #10b981;")
        h_m1.addWidget(self.lbl_value)
        sum_layout.addLayout(h_m1)

        h_m2 = QHBoxLayout()
        h_m2.addWidget(QLabel("Peso Total Ocupado:"))
        self.lbl_weight = QLabel("0.0 kg")
        self.lbl_weight.setStyleSheet("font-size: 14px; font-weight: bold; color: #38bdf8;")
        h_m2.addWidget(self.lbl_weight)
        sum_layout.addLayout(h_m2)

        h_m3 = QHBoxLayout()
        h_m3.addWidget(QLabel("Espacio Libre (Holgura):"))
        self.lbl_slack = QLabel("0.0 kg")
        self.lbl_slack.setStyleSheet("font-size: 14px; font-weight: bold; color: #f59e0b;")
        h_m3.addWidget(self.lbl_slack)
        sum_layout.addLayout(h_m3)

        sum_layout.addWidget(QLabel("Paquetes Seleccionados:"))
        self.lbl_items = QLabel("--")
        self.lbl_items.setWordWrap(True)
        self.lbl_items.setStyleSheet("font-weight: bold; color: #f1f5f9; padding: 4px; background: #090e17; border-radius: 4px;")
        sum_layout.addWidget(self.lbl_items)

        left_layout.addWidget(grp_summary)
        left_layout.addStretch()

        main_layout.addWidget(left_panel)

        # -------------------------------------------------------------
        # Right Panel: Matrix & Academic Explanation
        # -------------------------------------------------------------
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Top: DP Matrix V[i][w]
        grp_matrix = QGroupBox("Matriz de Estados de Programación Dinámica V[i][w]")
        mat_layout = QVBoxLayout(grp_matrix)
        self.matrix_view = DPMatrixView()
        mat_layout.addWidget(self.matrix_view)
        splitter.addWidget(grp_matrix)

        # Bottom: Academic Steps and Conclusions
        grp_conclusions = QGroupBox("Pasos por Etapas y Conclusiones del Examen")
        conc_layout = QVBoxLayout(grp_conclusions)
        self.txt_conclusions = QTextEdit()
        self.txt_conclusions.setReadOnly(True)
        conc_layout.addWidget(self.txt_conclusions)
        splitter.addWidget(grp_conclusions)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        main_layout.addWidget(splitter, 1)

        # Initial load
        self.reload_from_controller()
        self._on_solve_clicked()

    def reload_from_controller(self):
        problem = self.controller.get_problem()
        self.spin_capacity.setValue(problem.capacity)
        idx_rep = 1 if problem.allow_repetition else 0
        self.combo_mode.setCurrentIndex(idx_rep)

        self._refresh_items_table()

    def _refresh_items_table(self):
        items = self.controller.get_problem().items
        self.table_items.setRowCount(len(items))
        for row, it in enumerate(items):
            self.table_items.setItem(row, 0, QTableWidgetItem(it.name))
            self.table_items.setItem(row, 1, QTableWidgetItem(f"{it.weight:.1f}"))
            self.table_items.setItem(row, 2, QTableWidgetItem(f"{it.price:.0f}"))

    def _on_reset_clicked(self):
        self.controller.reset_to_default()
        self.reload_from_controller()
        self._on_solve_clicked()

    def _on_add_item(self):
        name = self.input_name.text().strip()
        if not name:
            name = f"Producto {len(self.controller.get_problem().items) + 1}"
        w = self.spin_weight.value()
        p = self.spin_price.value()

        self.controller.add_item(name, w, p)
        self.input_name.clear()
        self._refresh_items_table()
        self._on_solve_clicked()

    def _on_del_item(self):
        row = self.table_items.currentRow()
        if row >= 0:
            items = self.controller.get_problem().items
            if row < len(items):
                self.controller.remove_item(items[row].id)
                self._refresh_items_table()
                self._on_solve_clicked()

    def _on_solve_clicked(self):
        cap = self.spin_capacity.value()
        rep = self.combo_mode.currentData()

        try:
            res: KnapsackResult = self.controller.solve(cap, rep)
            self.lbl_value.setText(f"${res.total_value:.2f}")
            self.lbl_weight.setText(f"{res.total_weight:.1f} kg")
            self.lbl_slack.setText(f"{res.slack_capacity:.1f} kg")

            selected_strs = [f"{it.name} ({it.weight:.0f}kg, ${it.price:.0f})" for it in res.selected_items]
            self.lbl_items.setText(", ".join(selected_strs) if selected_strs else "Ninguno")

            self.matrix_view.set_matrix(res.dp_table, res.weights_header, res.items_header)

            full_text = "\n\n".join(res.stage_explanations) + "\n\n" + ("=" * 60) + "\n\n" + res.conclusion
            self.txt_conclusions.setPlainText(full_text)
        except Exception as e:
            QMessageBox.critical(self, "Error al Resolver Volumen de Carga", str(e))
