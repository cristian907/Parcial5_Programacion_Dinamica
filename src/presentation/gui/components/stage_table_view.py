"""Stage Table View Component for Operations Research DP stages in PyQt6."""
from typing import List, Optional
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from ....domain.models import StageTable


class StageTableView(QWidget):
    """Widget to display stage decision tables for Forward/Backward Dynamic Programming."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._stages: List[StageTable] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        # Stage selector
        self.combo_stage = QComboBox()
        self.combo_stage.currentIndexChanged.connect(self._on_stage_changed)
        layout.addWidget(self.combo_stage)

        self.lbl_description = QLabel("")
        self.lbl_description.setWordWrap(True)
        self.lbl_description.setStyleSheet("color: #94a3b8; font-size: 11.5px; margin-bottom: 2px;")
        layout.addWidget(self.lbl_description)

        # Decision Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Estado (s)",
            "Evaluaciones",
            "f*(s) Mín",
            "Decisión x*",
        ])
        
        # Proportional header resize
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)

    def set_stages(self, stages: List[StageTable]):
        self._stages = stages or []
        self.combo_stage.blockSignals(True)
        self.combo_stage.clear()

        for idx, st in enumerate(self._stages):
            self.combo_stage.addItem(f"{st.stage_name}", idx)

        self.combo_stage.blockSignals(False)

        if self._stages:
            self._render_stage(0)
        else:
            self.table.setRowCount(0)
            self.lbl_description.setText("No hay etapas disponibles.")

    def _on_stage_changed(self, index: int):
        if 0 <= index < len(self._stages):
            self._render_stage(index)

    def _render_stage(self, stage_idx: int):
        stage = self._stages[stage_idx]
        self.lbl_description.setText(stage.description)

        self.table.setRowCount(len(stage.rows))

        font_bold = QFont()
        font_bold.setBold(True)

        for row_idx, r in enumerate(stage.rows):
            # State
            item_state = QTableWidgetItem(f"Nodo {r.state}")
            item_state.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_state.setFont(font_bold)
            self.table.setItem(row_idx, 0, item_state)

            # Evaluations string
            eval_parts = []
            for target, cost in sorted(r.evaluations.items()):
                is_opt = target == r.optimal_decision
                mark = "✓" if is_opt else ""
                eval_parts.append(f"{target}→{cost:.0f}{mark}")
            eval_text = "  |  ".join(eval_parts) if eval_parts else "Sin transiciones"
            item_evals = QTableWidgetItem(eval_text)
            self.table.setItem(row_idx, 1, item_evals)

            # Optimal cost
            cost_str = f"{r.optimal_cost:.1f}" if r.optimal_cost < float("inf") else "∞"
            item_cost = QTableWidgetItem(cost_str)
            item_cost.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_cost.setForeground(QColor("#34d399"))
            item_cost.setFont(font_bold)
            self.table.setItem(row_idx, 2, item_cost)

            # Optimal decision
            dec_str = f"Nodo {r.optimal_decision}" if r.optimal_decision is not None else "-"
            item_dec = QTableWidgetItem(dec_str)
            item_dec.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_dec.setFont(font_bold)
            self.table.setItem(row_idx, 3, item_dec)
