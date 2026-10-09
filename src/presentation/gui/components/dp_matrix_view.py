"""Dynamic Programming 2D Matrix View for Cargo Volume problem in PyQt6."""
from typing import List, Optional
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QFont
from PyQt6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class DPMatrixView(QWidget):
    """Visualizes the Cargo Volume DP Matrix V[i][w]."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

    def set_matrix(
        self,
        dp_table: List[List[float]],
        weights_header: List[float],
        items_header: List[str],
    ):
        if not dp_table:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        rows = len(dp_table)
        cols = len(weights_header) + 1  # 1 extra for item name column

        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)

        headers = ["Etapa / Producto"] + [f"{int(w)} kg" for w in weights_header]
        self.table.setHorizontalHeaderLabels(headers)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for c in range(1, cols):
            self.table.horizontalHeader().setSectionResizeMode(c, QHeaderView.ResizeMode.Stretch)

        font_bold = QFont()
        font_bold.setBold(True)

        for i in range(rows):
            # Item Name
            item_name = items_header[i] if i < len(items_header) else f"Etapa {i}"
            item_lbl = QTableWidgetItem(item_name)
            item_lbl.setFont(font_bold)
            self.table.setItem(i, 0, item_lbl)

            # Cells
            for w in range(len(weights_header)):
                val = dp_table[i][w]
                is_max = (i == rows - 1 and w == len(weights_header) - 1)

                cell_item = QTableWidgetItem(f"${val:.0f}")
                cell_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                if is_max:
                    cell_item.setBackground(QBrush(QColor(16, 185, 129, 60)))
                    cell_item.setForeground(QColor("#34d399"))
                    cell_item.setFont(font_bold)

                self.table.setItem(i, w + 1, cell_item)
