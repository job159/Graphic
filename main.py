import math
import sys

from PyQt6.QtCore import QRectF, QTimer, Qt
from PyQt6.QtGui import QColor, QFont, QLinearGradient, QPainter, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from shape_demos import CircleDemo, EllipseDemo, FlameDemo, LightningDemo, SkewEllipseDemo


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 720

CIRCLE_MODE = "circle"
ELLIPSE_MODE = "ellipse"
SKEW_ELLIPSE_MODE = "skew_ellipse"
LIGHTNING_MODE = "lightning"
FLAME_MODE = "flame"

MODE_LABELS = {
    CIRCLE_MODE: "Circle",
    ELLIPSE_MODE: "Ellipse",
    SKEW_ELLIPSE_MODE: "Skew Ellipse",
    LIGHTNING_MODE: "Lightning",
    FLAME_MODE: "Flame",
}

ALIGN_LEFT_TOP_WRAP = (
    Qt.AlignmentFlag.AlignLeft.value
    | Qt.AlignmentFlag.AlignTop.value
    | Qt.TextFlag.TextWordWrap.value
)
ALIGN_LEFT_VCENTER = Qt.AlignmentFlag.AlignLeft.value | Qt.AlignmentFlag.AlignVCenter.value
ALIGN_CENTER = Qt.AlignmentFlag.AlignCenter.value

BACKGROUND_TOP = "#f5f7fa"
BACKGROUND_BOTTOM = "#edf1f5"
CARD_FILL = "#ffffff"
CARD_BORDER = "#d7dee7"
CARD_SHADOW = "#b6c1cc"
TEXT_PRIMARY = "#25313c"
TEXT_MUTED = "#667381"
ACCENT_BLUE = "#3277a8"
ACCENT_GREEN = "#58a56b"
ACCENT_ORANGE = "#d98d4a"
INFO_FILL = "#f7f9fb"
INFO_BORDER = "#dfe5ec"


class GraphicsCanvas(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.angle_degrees = 30.0
        self.current_mode = CIRCLE_MODE
        self.demos = {
            CIRCLE_MODE: CircleDemo(),
            ELLIPSE_MODE: EllipseDemo(),
            SKEW_ELLIPSE_MODE: SkewEllipseDemo(),
            LIGHTNING_MODE: LightningDemo(),
            FLAME_MODE: FlameDemo(),
        }
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT - 120)

    def set_angle(self, angle_degrees: float) -> None:
        self.angle_degrees = angle_degrees
        self.update()

    def set_mode(self, mode: str) -> None:
        self.current_mode = mode
        self.update()

    def current_demo(self):
        return self.demos[self.current_mode]

    def panel_rects(self) -> tuple[QRectF, QRectF]:
        side_margin = 28
        top_margin = 86
        bottom_margin = 22
        gap = 18
        panel_width = (self.width() - side_margin * 2 - gap) / 2
        panel_height = self.height() - top_margin - bottom_margin
        left_rect = QRectF(side_margin, top_margin, panel_width, panel_height)
        right_rect = QRectF(left_rect.right() + gap, top_margin, panel_width, panel_height)
        return left_rect, right_rect

    def draw_card(self, painter: QPainter, rect: QRectF, fill: str = CARD_FILL) -> None:
        shadow_rect = rect.adjusted(0, 2, 0, 2)
        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(CARD_SHADOW + "12"))
        painter.drawRoundedRect(shadow_rect, 18, 18)
        painter.setBrush(QColor(fill))
        painter.setPen(QPen(QColor(CARD_BORDER), 1))
        painter.drawRoundedRect(rect, 18, 18)
        painter.restore()

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.draw_background(painter)

        self.draw_title(painter)
        self.draw_shape_demo(painter)
        self.draw_formula_demo(painter)

    def draw_background(self, painter: QPainter) -> None:
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(BACKGROUND_TOP))
        gradient.setColorAt(0.55, QColor("#f1f4f7"))
        gradient.setColorAt(1.0, QColor(BACKGROUND_BOTTOM))
        painter.fillRect(self.rect(), gradient)

    def draw_title(self, painter: QPainter) -> None:
        painter.setPen(QColor(TEXT_PRIMARY))
        painter.setFont(QFont("Segoe UI Semibold", 19))
        painter.drawText(36, 42, "PyQt6 Math Visualizer")

        painter.setPen(QColor(TEXT_MUTED))
        painter.setFont(QFont("Segoe UI", 10))
        painter.drawText(
            36,
            64,
            f"Current mode: {MODE_LABELS[self.current_mode]}  |  Geometry and formula stay in sync.",
        )

    def draw_shape_demo(self, painter: QPainter) -> None:
        panel_rect, _ = self.panel_rects()
        self.draw_card(painter, panel_rect)
        demo = self.current_demo()

        center_x = int(panel_rect.center().x())
        center_y = int(panel_rect.top() + panel_rect.height() * 0.42)
        radians = math.radians(self.angle_degrees)
        point_x, point_y, info_lines = demo.calculate_demo_point(center_x, center_y, radians, self.angle_degrees)

        painter.setPen(QColor(TEXT_PRIMARY))
        painter.setFont(QFont("Segoe UI Semibold", 12))
        painter.drawText(
            int(panel_rect.left()) + 24,
            int(panel_rect.top()) + 34,
            f"{MODE_LABELS[self.current_mode]} View",
        )
        painter.setPen(QColor(TEXT_MUTED))
        painter.setFont(QFont("Segoe UI", 9))
        painter.drawText(
            int(panel_rect.left()) + 24,
            int(panel_rect.top()) + 58,
            getattr(demo, "shape_subtitle", "Projection lines show where the current angle lands."),
        )

        axis_pen = QPen(QColor("#9aa7b3"), 2)
        grid_pen = QPen(QColor("#e0e6ed"), 1)
        vector_pen = QPen(QColor(ACCENT_BLUE), 4)
        helper_pen = QPen(QColor(ACCENT_ORANGE), 2, Qt.PenStyle.DashLine)
        show_grid = getattr(demo, "show_grid", True)
        show_axes = getattr(demo, "show_axes", True)
        show_helpers = getattr(demo, "show_helpers", True)
        show_vector = getattr(demo, "show_vector", True)
        show_point = getattr(demo, "show_point", True)
        point_color = getattr(demo, "point_color", ACCENT_BLUE)

        if show_grid:
            for offset in range(-140, 141, 35):
                painter.setPen(grid_pen)
                painter.drawLine(center_x - 150, center_y + offset, center_x + 150, center_y + offset)
                painter.drawLine(center_x + offset, center_y - 150, center_x + offset, center_y + 150)

        if show_axes:
            painter.setPen(axis_pen)
            painter.drawLine(center_x - 160, center_y, center_x + 160, center_y)
            painter.drawLine(center_x, center_y - 160, center_x, center_y + 160)

        demo.draw_reference_shape(painter, center_x, center_y)

        if show_helpers:
            painter.setPen(helper_pen)
            painter.drawLine(center_x, center_y, int(point_x), center_y)
            painter.drawLine(int(point_x), center_y, int(point_x), int(point_y))

        effect = getattr(demo, "draw_effect", None)
        if effect is not None:
            effect(painter, center_x, center_y, point_x, point_y, radians, self.angle_degrees)

        if show_vector:
            painter.setPen(vector_pen)
            painter.drawLine(center_x, center_y, int(point_x), int(point_y))

        if show_point:
            painter.setBrush(QColor(point_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(int(point_x) - 6, int(point_y) - 6, 12, 12)

        info_box_height = 30 + len(info_lines) * 14
        info_box = QRectF(
            panel_rect.left() + 18,
            panel_rect.bottom() - info_box_height - 18,
            panel_rect.width() - 36,
            info_box_height,
        )
        painter.setPen(QPen(QColor(INFO_BORDER), 1))
        painter.setBrush(QColor(INFO_FILL))
        painter.drawRoundedRect(info_box, 14, 14)

        painter.setPen(QColor(TEXT_PRIMARY))
        painter.setFont(QFont("Consolas", 9))
        line_y = int(info_box.top()) + 20
        for line in info_lines:
            painter.drawText(
                QRectF(info_box.left() + 14, line_y - 10, info_box.width() - 28, 16),
                ALIGN_LEFT_VCENTER,
                line,
            )
            line_y += 14

        if show_axes:
            painter.drawText(center_x + 148, center_y - 8, "x")
            painter.drawText(center_x + 8, center_y - 148, "y")

    def draw_formula_demo(self, painter: QPainter) -> None:
        _, panel_rect = self.panel_rects()
        self.draw_card(painter, panel_rect)

        formula_title, formula_text = self.current_demo().formula_descriptions()
        footer_box = QRectF(
            panel_rect.left() + 24,
            panel_rect.bottom() - 58,
            panel_rect.width() - 48,
            34,
        )
        graph_rect = QRectF(
            panel_rect.left() + 24,
            panel_rect.top() + 110,
            panel_rect.width() - 48,
            footer_box.top() - panel_rect.top() - 126,
        )
        mid_y = graph_rect.center().y()

        painter.setPen(QColor(TEXT_PRIMARY))
        painter.setFont(QFont("Segoe UI Semibold", 12))
        painter.drawText(int(panel_rect.left()) + 24, int(panel_rect.top()) + 36, formula_title)
        painter.setPen(QColor(TEXT_MUTED))
        painter.setFont(QFont("Consolas", 10))
        painter.drawText(
            QRectF(panel_rect.left() + 24, panel_rect.top() + 50, panel_rect.width() - 48, 38),
            ALIGN_LEFT_TOP_WRAP,
            formula_text,
        )
        painter.setPen(QPen(QColor(CARD_BORDER), 1))
        painter.drawLine(
            int(panel_rect.left()) + 24,
            int(panel_rect.top()) + 96,
            int(panel_rect.right()) - 24,
            int(panel_rect.top()) + 96,
        )

        painter.setPen(QPen(QColor("#e1e7ee"), 1))
        row_step = max(28, int(graph_rect.height() / 8))
        col_step = max(42, int(graph_rect.width() / 8))
        for row in range(0, int(graph_rect.height()) + 1, row_step):
            painter.drawLine(
                int(graph_rect.left()),
                int(graph_rect.top()) + row,
                int(graph_rect.right()),
                int(graph_rect.top()) + row,
            )
        for col in range(0, int(graph_rect.width()) + 1, col_step):
            painter.drawLine(
                int(graph_rect.left()) + col,
                int(graph_rect.top()),
                int(graph_rect.left()) + col,
                int(graph_rect.bottom()),
            )

        painter.setPen(QPen(QColor("#9aa6b2"), 2))
        painter.drawLine(int(graph_rect.left()), int(mid_y), int(graph_rect.right()), int(mid_y))
        painter.drawLine(
            int(graph_rect.left()),
            int(graph_rect.top()),
            int(graph_rect.left()),
            int(graph_rect.bottom()),
        )

        wave_pen = QPen(QColor(ACCENT_GREEN), 3)
        painter.setPen(wave_pen)

        previous_x = graph_rect.left()
        previous_y = mid_y
        current_radian = math.radians(self.angle_degrees)
        sample_values = [
            self.current_demo().formula_value_for_graph((pixel_x / max(1, int(graph_rect.width()))) * math.tau)
            for pixel_x in range(int(graph_rect.width()) + 1)
        ]
        max_value = max(1.0, max(abs(value) for value in sample_values))
        amplitude = (graph_rect.height() * 0.36) / max_value

        for pixel_x in range(int(graph_rect.width()) + 1):
            ratio = pixel_x / max(1, int(graph_rect.width()))
            x_radian = ratio * math.tau
            y_value = self.current_demo().formula_value_for_graph(x_radian)
            draw_x = graph_rect.left() + pixel_x
            draw_y = mid_y - amplitude * y_value

            if pixel_x > 0:
                painter.drawLine(int(previous_x), int(previous_y), int(draw_x), int(draw_y))

            previous_x = draw_x
            previous_y = draw_y

        highlight_x = graph_rect.left() + (current_radian / math.tau) * graph_rect.width()
        current_value = self.current_demo().formula_value_for_graph(current_radian)
        highlight_y = mid_y - amplitude * current_value

        painter.setPen(QPen(QColor(ACCENT_ORANGE), 2, Qt.PenStyle.DashLine))
        painter.drawLine(int(highlight_x), mid_y, int(highlight_x), int(highlight_y))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(ACCENT_ORANGE))
        painter.drawEllipse(int(highlight_x) - 6, int(highlight_y) - 6, 12, 12)

        painter.setPen(QColor(TEXT_MUTED))
        painter.setFont(QFont("Consolas", 9))
        painter.drawText(
            QRectF(graph_rect.left(), graph_rect.bottom() + 6, 40, 18),
            ALIGN_LEFT_VCENTER,
            "0",
        )
        painter.drawText(
            QRectF(graph_rect.center().x() - 20, graph_rect.bottom() + 6, 40, 18),
            ALIGN_CENTER,
            "pi",
        )
        painter.drawText(
            QRectF(graph_rect.right() - 44, graph_rect.bottom() + 6, 44, 18),
            ALIGN_CENTER,
            "2pi",
        )

        painter.setPen(QPen(QColor(INFO_BORDER), 1))
        painter.setBrush(QColor(INFO_FILL))
        painter.drawRoundedRect(footer_box, 12, 12)
        painter.setPen(QColor(TEXT_PRIMARY))
        painter.setFont(QFont("Consolas", 10))
        painter.drawText(
            footer_box.adjusted(14, 0, -14, 0),
            ALIGN_LEFT_VCENTER,
            f"angle {self.angle_degrees:5.1f} deg    rad {current_radian:6.3f}    value {current_value:6.3f}",
        )

    def sizeHint(self):
        return self.minimumSize()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Basic 2D Graphics with PyQt6")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.canvas = GraphicsCanvas()
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setMinimumHeight(42)
        self.info_label.setStyleSheet(
            """
            QLabel {
                font-family: Segoe UI;
                font-size: 12px;
                font-weight: 600;
                color: #25313c;
                background: #ffffff;
                border: 1px solid #d7dee7;
                border-radius: 10px;
                padding: 8px 12px;
            }
            """
        )

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 360)
        self.slider.setValue(30)
        self.slider.valueChanged.connect(self.on_slider_changed)
        self.slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                height: 6px;
                background: #d8e0e8;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: #58a56b;
                border-radius: 4px;
            }
            QSlider::add-page:horizontal {
                background: #edf1f5;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                width: 16px;
                margin: -5px 0;
                background: #3277a8;
                border: 2px solid #ffffff;
                border-radius: 8px;
            }
            """
        )

        self.auto_timer = QTimer(self)
        self.auto_timer.timeout.connect(self.animate)
        self.auto_timer.start(40)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 12, 16, 16)
        layout.setSpacing(10)
        layout.addWidget(self.canvas)
        layout.addWidget(self.info_label)
        layout.addWidget(self.slider)

        container = QWidget()
        container.setLayout(layout)
        container.setStyleSheet("background: #eef2f6;")
        self.setCentralWidget(container)
        self.setStyleSheet(
            """
            QMainWindow {
                background: #eef2f6;
            }
            QMenuBar {
                background: #f7f9fb;
                color: #25313c;
                border-bottom: 1px solid #d7dee7;
                padding: 4px 10px;
                font-family: Segoe UI;
                font-size: 10pt;
            }
            QMenuBar::item:selected {
                background: #e8eef4;
                border-radius: 4px;
            }
            QMenu {
                background: #ffffff;
                color: #25313c;
                border: 1px solid #d7dee7;
                padding: 4px;
            }
            QMenu::item:selected {
                background: #e8eef4;
                border-radius: 4px;
            }
            """
        )

        self.build_menu()
        self.on_slider_changed(self.slider.value())

    def build_menu(self) -> None:
        mode_menu = self.menuBar().addMenu("Modes")

        circle_action = mode_menu.addAction("Circle")
        circle_action.triggered.connect(lambda: self.set_mode(CIRCLE_MODE))

        ellipse_action = mode_menu.addAction("Ellipse")
        ellipse_action.triggered.connect(lambda: self.set_mode(ELLIPSE_MODE))

        skew_ellipse_action = mode_menu.addAction("Skew Ellipse")
        skew_ellipse_action.triggered.connect(lambda: self.set_mode(SKEW_ELLIPSE_MODE))

        lightning_action = mode_menu.addAction("Lightning")
        lightning_action.triggered.connect(lambda: self.set_mode(LIGHTNING_MODE))

        flame_action = mode_menu.addAction("Flame")
        flame_action.triggered.connect(lambda: self.set_mode(FLAME_MODE))

    def set_mode(self, mode: str) -> None:
        self.canvas.set_mode(mode)
        self.on_slider_changed(self.slider.value())

    def on_slider_changed(self, value: int) -> None:
        self.canvas.set_angle(float(value))
        self.info_label.setText(self.canvas.current_demo().status_text(value))

    def animate(self) -> None:
        next_value = (self.slider.value() + 1) % 361
        self.slider.blockSignals(True)
        self.slider.setValue(next_value)
        self.slider.blockSignals(False)
        self.on_slider_changed(next_value)


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
