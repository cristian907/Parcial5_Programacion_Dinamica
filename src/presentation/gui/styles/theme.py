"""Modern Dark Theme Stylesheet for PyQt6 GUI."""

DARK_THEME_QSS = """
/* Global Window & Typography */
QWidget {
    background-color: #0d131f;
    color: #f1f5f9;
    font-family: 'Segoe UI', 'Ubuntu', 'Roboto', sans-serif;
    font-size: 13px;
    selection-background-color: #0284c7;
    selection-color: #ffffff;
}

/* Main Window */
QMainWindow {
    background-color: #090e17;
}

/* Tab Widget & Tabs */
QTabWidget::pane {
    border: 1px solid #1e293b;
    background-color: #0f172a;
    border-radius: 8px;
    top: -1px;
}

QTabBar::tab {
    background-color: #1e293b;
    color: #94a3b8;
    padding: 10px 22px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: 600;
    font-size: 13px;
    border: 1px solid #334155;
    border-bottom: none;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0284c7, stop:1 #0369a1);
    color: #ffffff;
    border-color: #38bdf8;
}

QTabBar::tab:hover:!selected {
    background-color: #334155;
    color: #f8fafc;
}

/* Group Boxes / Cards */
QGroupBox {
    background-color: #131d2e;
    border: 1px solid #1e2e48;
    border-radius: 10px;
    margin-top: 24px;
    padding-top: 20px;
    font-weight: 700;
    font-size: 13px;
    color: #38bdf8;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 10px;
    left: 14px;
    background-color: #0f172a;
    border: 1px solid #0284c7;
    border-radius: 5px;
    color: #38bdf8;
}

/* Buttons */
QPushButton {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 7px 16px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #334155;
    border-color: #475569;
}

QPushButton:pressed {
    background-color: #0f172a;
}

QPushButton#btnPrimary {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #06b6d4);
    color: #ffffff;
    border: 1px solid #38bdf8;
}

QPushButton#btnPrimary:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0369a1, stop:1 #0891b2);
}

QPushButton#btnSuccess {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #10b981);
    color: #ffffff;
    border: 1px solid #34d399;
}

QPushButton#btnSuccess:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #047857, stop:1 #059669);
}

QPushButton#btnDanger {
    background-color: rgba(239, 68, 68, 0.2);
    border: 1px solid #ef4444;
    color: #fca5a5;
}

QPushButton#btnDanger:hover {
    background-color: rgba(239, 68, 68, 0.35);
}

/* Input Fields & Combos */
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: #090e17;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 10px;
    color: #f8fafc;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid #38bdf8;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #131d2e;
    border: 1px solid #334155;
    selection-background-color: #0284c7;
    color: #f8fafc;
}

/* Tables */
QTableWidget {
    background-color: #090e17;
    alternate-background-color: #111827;
    gridline-color: #1e293b;
    border: 1px solid #1e293b;
    border-radius: 8px;
    color: #f8fafc;
}

QTableWidget::item {
    padding: 6px;
}

QTableWidget::item:selected {
    background-color: #0369a1;
    color: #ffffff;
}

QHeaderView::section {
    background-color: #1e293b;
    color: #94a3b8;
    padding: 8px;
    border: none;
    border-right: 1px solid #334155;
    border-bottom: 2px solid #0284c7;
    font-weight: 700;
    font-size: 12px;
}

/* Text Edit / Code Preview */
QTextEdit, QPlainTextEdit {
    background-color: #070b12;
    border: 1px solid #1e293b;
    border-radius: 8px;
    color: #cbd5e1;
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    padding: 10px;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #0d131f;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #334155;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #475569;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: #0d131f;
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background: #334155;
    min-width: 20px;
    border-radius: 5px;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    height: 0px;
}

/* Status Bar */
QStatusBar {
    background-color: #090e17;
    color: #64748b;
    border-top: 1px solid #1e293b;
}

QLabel {
    color: #e2e8f0;
}
"""
