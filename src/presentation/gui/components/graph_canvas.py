"""Interactive Graph Canvas Widget built with PyQt6 QPainter with responsive layout."""
import math
from typing import Dict, List, Optional, Set, Tuple
from PyQt6.QtCore import QPointF, QRectF, Qt, pyqtSignal
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QLinearGradient,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPen,
)
from PyQt6.QtWidgets import QWidget
from ....domain.entities import Edge, Graph, Node


class GraphCanvas(QWidget):
    """Interactive canvas widget to visualize, drag, and highlight graph nodes and edges."""

    node_selected = pyqtSignal(int)
    node_moved = pyqtSignal(int, float, float)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setMinimumSize(480, 380)
        self.setMouseTracking(True)

        self._graph: Optional[Graph] = None
        self._source: Optional[int] = 1
        self._destination: Optional[int] = 13
        self._optimal_path: List[int] = []

        # Local transformed positions for rendering & dragging: node_id -> QPointF
        self._node_positions: Dict[int, QPointF] = {}
        self._custom_dragged: Set[int] = set()

        # Dragging state
        self._dragged_node_id: Optional[int] = None
        self._drag_offset: QPointF = QPointF(0, 0)

        # Visual dimensions
        self.node_radius = 24.0

    def set_graph(self, graph: Graph, source: Optional[int] = 1, destination: Optional[int] = 13):
        self._graph = graph
        self._source = source
        self._destination = destination
        self._optimal_path = []
        self._recompute_layout()
        self.update()

    def set_optimal_path(self, path: List[int]):
        self._optimal_path = path or []
        self.update()

    def set_endpoints(self, source: int, destination: int):
        self._source = source
        self._destination = destination
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._recompute_layout()

    def _recompute_layout(self):
        """Scales graph node coordinates smoothly to fit the canvas dimensions."""
        if not self._graph or not self._graph.nodes:
            self._node_positions.clear()
            return

        w = max(400, self.width())
        h = max(350, self.height())
        padding_x = 70.0
        padding_y = 55.0

        xs = [n.x for n in self._graph.nodes.values()]
        ys = [n.y for n in self._graph.nodes.values()]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        range_x = (max_x - min_x) if max_x > min_x else 1.0
        range_y = (max_y - min_y) if max_y > min_y else 1.0

        available_w = w - 2 * padding_x
        available_h = h - 2 * padding_y

        for nid, node in self._graph.nodes.items():
            if nid in self._custom_dragged and nid in self._node_positions:
                continue  # Keep user's custom drag position

            # Normalized coordinate
            norm_x = (node.x - min_x) / range_x
            norm_y = (node.y - min_y) / range_y

            screen_x = padding_x + norm_x * available_w
            screen_y = padding_y + norm_y * available_h
            self._node_positions[nid] = QPointF(screen_x, screen_y)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        # Background
        painter.fillRect(self.rect(), QColor("#090e17"))

        # Subtle grid dots
        painter.setPen(QPen(QColor(255, 255, 255, 12), 1))
        step = 32
        for x in range(0, self.width(), step):
            for y in range(0, self.height(), step):
                painter.drawPoint(x, y)

        if not self._graph or not self._node_positions:
            painter.setPen(QColor("#64748b"))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No hay grafo cargado.")
            return

        # Prepare path edge lookup
        opt_edges: Set[Tuple[int, int]] = set()
        if len(self._optimal_path) > 1:
            for i in range(len(self._optimal_path) - 1):
                opt_edges.add((self._optimal_path[i], self._optimal_path[i + 1]))

        # 1. Draw Edges
        for edge in self._graph.edges:
            p1 = self._node_positions.get(edge.source)
            p2 = self._node_positions.get(edge.target)
            if not p1 or not p2:
                continue

            is_opt = (edge.source, edge.target) in opt_edges
            self._draw_edge(painter, p1, p2, edge.weight, is_opt)

        # 2. Draw Nodes
        for nid, node in self._graph.nodes.items():
            pt = self._node_positions.get(nid)
            if not pt:
                continue

            is_opt = nid in self._optimal_path
            is_src = nid == self._source
            is_dst = nid == self._destination
            self._draw_node(painter, nid, node.label, pt, is_src, is_dst, is_opt)

    def _draw_edge(self, painter: QPainter, p1: QPointF, p2: QPointF, weight: float, is_optimal: bool):
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()
        dist = math.hypot(dx, dy)
        if dist == 0:
            return

        ux = dx / dist
        uy = dy / dist

        # Clip endpoints to node circles
        start_pt = QPointF(p1.x() + ux * self.node_radius, p1.y() + uy * self.node_radius)
        end_pt = QPointF(p2.x() - ux * self.node_radius, p2.y() - uy * self.node_radius)

        if is_optimal:
            # Outer glowing halo
            glow_pen = QPen(QColor(16, 185, 129, 65), 10)
            painter.setPen(glow_pen)
            painter.drawLine(start_pt, end_pt)

            pen = QPen(QColor("#10b981"), 3.8)
            painter.setPen(pen)
            painter.drawLine(start_pt, end_pt)
            self._draw_arrow_head(painter, end_pt, ux, uy, QColor("#10b981"), size=11)
        else:
            pen = QPen(QColor("#334155"), 2.2)
            painter.setPen(pen)
            painter.drawLine(start_pt, end_pt)
            self._draw_arrow_head(painter, end_pt, ux, uy, QColor("#64748b"), size=8.5)

        # Draw weight badge along edge
        mid_x = (start_pt.x() + end_pt.x()) / 2.0
        mid_y = (start_pt.y() + end_pt.y()) / 2.0

        # Perpendicular offset so label does not overlap the line
        perp_x = -uy * 13
        perp_y = ux * 13
        label_x = mid_x + perp_x
        label_y = mid_y + perp_y

        weight_str = f"{weight:.0f}" if weight.is_integer() else f"{weight:.1f}"

        font = QFont("JetBrains Mono", 8, QFont.Weight.Bold)
        painter.setFont(font)

        badge_rect = QRectF(label_x - 15, label_y - 10, 30, 20)
        painter.setBrush(QBrush(QColor("#0f172a")))
        painter.setPen(QPen(QColor("#10b981" if is_optimal else "#334155"), 1.2))
        painter.drawRoundedRect(badge_rect, 4, 4)

        painter.setPen(QColor("#34d399" if is_optimal else "#cbd5e1"))
        painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, weight_str)

    def _draw_arrow_head(self, painter: QPainter, tip: QPointF, ux: float, uy: float, color: QColor, size: float):
        px = -uy
        py = ux

        left = QPointF(tip.x() - ux * size + px * (size * 0.6), tip.y() - uy * size + py * (size * 0.6))
        right = QPointF(tip.x() - ux * size - px * (size * 0.6), tip.y() - uy * size - py * (size * 0.6))

        path = QPainterPath()
        path.moveTo(tip)
        path.lineTo(left)
        path.lineTo(right)
        path.closeSubpath()

        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)

    def _draw_node(self, painter: QPainter, nid: int, label: str, center: QPointF, is_source: bool, is_dest: bool, is_optimal: bool):
        r = self.node_radius

        # Halos / glow
        if is_optimal:
            painter.setBrush(QBrush(QColor(16, 185, 129, 50)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(center, r + 8, r + 8)

        # Gradient fill
        grad = QLinearGradient(center.x() - r, center.y() - r, center.x() + r, center.y() + r)
        if is_source:
            grad.setColorAt(0.0, QColor("#0284c7"))
            grad.setColorAt(1.0, QColor("#0369a1"))
            border_color = QColor("#38bdf8")
        elif is_dest:
            grad.setColorAt(0.0, QColor("#be123c"))
            grad.setColorAt(1.0, QColor("#881337"))
            border_color = QColor("#fb7185")
        elif is_optimal:
            grad.setColorAt(0.0, QColor("#059669"))
            grad.setColorAt(1.0, QColor("#065f46"))
            border_color = QColor("#34d399")
        else:
            grad.setColorAt(0.0, QColor("#1e293b"))
            grad.setColorAt(1.0, QColor("#0f172a"))
            border_color = QColor("#475569")

        painter.setBrush(QBrush(grad))
        border_width = 3.2 if (is_optimal or is_source or is_dest) else 2.2
        painter.setPen(QPen(border_color, border_width))
        painter.drawEllipse(center, r, r)

        # Node ID text
        painter.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        painter.setPen(QColor("#ffffff"))
        text_rect = QRectF(center.x() - r, center.y() - r, 2 * r, 2 * r)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, str(nid))

        # Office sub-labels
        if nid in (1, 13) or "Oficina" in label:
            painter.setFont(QFont("Segoe UI", 8, QFont.Weight.DemiBold))
            painter.setPen(QColor("#38bdf8" if is_source else ("#fda4af" if is_dest else "#94a3b8")))
            office_str = "Oficina anterior" if nid == 1 else ("Oficina nueva" if nid == 13 else label)
            y_offset = -r - 18 if nid == 1 else (-r - 18)
            lbl_rect = QRectF(center.x() - 65, center.y() + y_offset, 130, 16)
            painter.drawText(lbl_rect, Qt.AlignmentFlag.AlignCenter, office_str)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self._graph:
            pos = event.position()
            for nid, pt in self._node_positions.items():
                d = math.hypot(pt.x() - pos.x(), pt.y() - pos.y())
                if d <= self.node_radius + 5:
                    self._dragged_node_id = nid
                    self._drag_offset = QPointF(pt.x() - pos.x(), pt.y() - pos.y())
                    self.node_selected.emit(nid)
                    break

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._dragged_node_id is not None:
            pos = event.position()
            new_x = max(self.node_radius + 15, min(self.width() - self.node_radius - 15, pos.x() + self._drag_offset.x()))
            new_y = max(self.node_radius + 25, min(self.height() - self.node_radius - 15, pos.y() + self._drag_offset.y()))

            self._node_positions[self._dragged_node_id] = QPointF(new_x, new_y)
            self._custom_dragged.add(self._dragged_node_id)
            self.node_moved.emit(self._dragged_node_id, new_x, new_y)
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragged_node_id = None
