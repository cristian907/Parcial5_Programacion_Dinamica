"""Problem Report Export Tab in PyQt6."""
import os
from typing import Optional
from PyQt6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from ...controllers import ReportController


class ReportTab(QWidget):
    """Tab to generate, preview, and save the official text report."""

    def __init__(self, controller: ReportController, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.controller = controller

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        header_layout = QHBoxLayout()
        v_title = QVBoxLayout()
        lbl_title = QLabel("3. Generador de Reporte del Problema")
        lbl_title.setStyleSheet("font-size: 16px; font-weight: 800; color: #38bdf8;")
        v_title.addWidget(lbl_title)

        lbl_sub = QLabel("Salidas completas del programa con todos los pasos de resolución computacional.")
        lbl_sub.setStyleSheet("color: #94a3b8; font-size: 12px;")
        v_title.addWidget(lbl_sub)
        header_layout.addLayout(v_title)

        header_layout.addStretch()

        self.btn_generate = QPushButton("Actualizar Reporte")
        self.btn_generate.clicked.connect(self._on_generate_clicked)
        header_layout.addWidget(self.btn_generate)

        self.btn_save = QPushButton("Guardar Archivo .txt")
        self.btn_save.setObjectName("btnSuccess")
        self.btn_save.clicked.connect(self._on_save_clicked)
        header_layout.addWidget(self.btn_save)

        layout.addLayout(header_layout)

        # Monospace Text Preview
        grp_preview = QGroupBox("Vista Previa del Archivo 'reporte_problema.txt'")
        prev_layout = QVBoxLayout(grp_preview)

        self.txt_preview = QTextEdit()
        self.txt_preview.setReadOnly(True)
        prev_layout.addWidget(self.txt_preview)

        layout.addWidget(grp_preview)

        # Initial generation
        self._on_generate_clicked()

    def _on_generate_clicked(self):
        try:
            content = self.controller.generate_report(file_path="reporte_problema.txt")
            self.txt_preview.setPlainText(content)
        except Exception as e:
            QMessageBox.critical(self, "Error al generar reporte", str(e))

    def _on_save_clicked(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Reporte del Problema",
            "reporte_problema.txt",
            "Archivos de Texto (*.txt);;Todos los archivos (*)"
        )
        if path:
            try:
                self.controller.generate_report(file_path=path)
                QMessageBox.information(self, "Éxito", f"Reporte guardado con éxito en:\n{path}")
            except Exception as e:
                QMessageBox.critical(self, "Error al guardar", str(e))
