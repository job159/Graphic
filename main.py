import math
import sys

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from shape_demos import CircleDemo, EllipseDemo, SkewEllipseDemo


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 720

CIRCLE_MODE = "circle"
ELLIPSE_MODE = "ellipse"
SKEW_ELLIPSE_MODE = "skew_ellipse"

MODE_LABELS = {
    CIRCLE_MODE: "Circle",
    ELLIPSE_MODE: "Ellipse",
    SKEW_ELLIPSE_MODE: "Skew Ellipse",
}


class GraphicsCanvas(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.angle_degrees = 30.0
        self.current_mode = CIRCLE_MODE
        self.demos = {
            CIRCLE_MODE: CircleDemo(),
            ELLIPSE_MODE: EllipseDemo(),
            SKEW_ELLIPSE_MODE: SkewEllipseDemo(),
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

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#f7f4ea"))

        self.draw_title(painter)
        self.draw_shape_demo(painter)
        self.draw_formula_demo(painter)

    def draw_title(self, painter: QPainter) -> None:
        painter.setPen(QColor("#22333b"))
        painter.setFont(QFont("Consolas", 16, QFont.Weight.Bold))
        painter.drawText(24, 36, "PyQt6 2D Graphics: Trigonometry and Basic Math")
        painter.setFont(QFont("Consolas", 11))
        painter.drawText(24, 60, f"Current mode: {MODE_LABELS[self.current_mode]}")

    def draw_shape_demo(self, painter: QPainter) -> None:
        panel_x = 40
        panel_y = 70
        panel_w = 420
        panel_h = 420

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#fffdf8"))
        painter.drawRoundedRect(panel_x, panel_y, panel_w, panel_h, 16, 16)

        center_x = panel_x + panel_w // 2
        center_y = panel_y + panel_h // 2
        radians = math.radians(self.angle_degrees)
        point_x, point_y, info_lines = self.current_demo().calculate_demo_point(
            center_x, center_y, radians, self.angle_degrees
        )

        axis_pen = QPen(QColor("#9aa6b2"), 2)
        grid_pen = QPen(QColor("#d9e0e6"), 1)
        vector_pen = QPen(QColor("#1f7a8c"), 4)
        helper_pen = QPen(QColor("#e07a5f"), 2, Qt.PenStyle.DashLine)

        for offset in range(-140, 141, 35):
            painter.setPen(grid_pen)
            painter.drawLine(center_x - 150, center_y + offset, center_x + 150, center_y + offset)
            painter.drawLine(center_x + offset, center_y - 150, center_x + offset, center_y + 150)

        painter.setPen(axis_pen)
        painter.drawLine(center_x - 160, center_y, center_x + 160, center_y)
        painter.drawLine(center_x, center_y - 160, center_x, center_y + 160)

        self.current_demo().draw_reference_shape(painter, center_x, center_y)

        painter.setPen(helper_pen)
        painter.drawLine(center_x, center_y, int(point_x), center_y)
        painter.drawLine(int(point_x), center_y, int(point_x), int(point_y))

        painter.setPen(vector_pen)
        painter.drawLine(center_x, center_y, int(point_x), int(point_y))

        painter.setBrush(QColor("#1f7a8c"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(point_x) - 6, int(point_y) - 6, 12, 12)

        painter.setPen(QColor("#22333b"))
        painter.setFont(QFont("Consolas", 11))
        painter.drawText(panel_x + 20, panel_y + 30, f"Left: {MODE_LABELS[self.current_mode]} Demo")
        for index, line in enumerate(info_lines):
            painter.drawText(panel_x + 20, panel_y + 56 + index * 26, line)

        painter.drawText(center_x + 148, center_y - 8, "x")
        painter.drawText(center_x + 8, center_y - 148, "y")

    def draw_formula_demo(self, painter: QPainter) -> None:
        panel_x = 500
        panel_y = 70
        panel_w = 450
        panel_h = 420

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#fffdf8"))
        painter.drawRoundedRect(panel_x, panel_y, panel_w, panel_h, 16, 16)

        graph_left = panel_x + 24
        graph_top = panel_y + 70
        graph_width = 390
        graph_height = 260
        mid_y = graph_top + graph_height // 2

        painter.setPen(QPen(QColor("#d9e0e6"), 1))
        for row in range(0, graph_height + 1, 32):
            painter.drawLine(graph_left, graph_top + row, graph_left + graph_width, graph_top + row)
        for col in range(0, graph_width + 1, 48):
            painter.drawLine(graph_left + col, graph_top, graph_left + col, graph_top + graph_height)

        painter.setPen(QPen(QColor("#9aa6b2"), 2))
        painter.drawLine(graph_left, mid_y, graph_left + graph_width, mid_y)
        painter.drawLine(graph_left, graph_top, graph_left, graph_top + graph_height)

        wave_pen = QPen(QColor("#81b29a"), 3)
        painter.setPen(wave_pen)

        previous_x = graph_left
        previous_y = mid_y
        amplitude = 90
        current_radian = math.radians(self.angle_degrees)

        for pixel_x in range(graph_width + 1):
            ratio = pixel_x / graph_width
            x_radian = ratio * math.tau
            y_value = self.current_demo().formula_value_for_graph(x_radian)
            draw_x = graph_left + pixel_x
            draw_y = mid_y - amplitude * y_value

            if pixel_x > 0:
                painter.drawLine(int(previous_x), int(previous_y), int(draw_x), int(draw_y))

            previous_x = draw_x
            previous_y = draw_y

        highlight_x = graph_left + (current_radian / math.tau) * graph_width
        current_value = self.current_demo().formula_value_for_graph(current_radian)
        highlight_y = mid_y - amplitude * current_value

        painter.setPen(QPen(QColor("#e07a5f"), 2, Qt.PenStyle.DashLine))
        painter.drawLine(int(highlight_x), mid_y, int(highlight_x), int(highlight_y))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#e07a5f"))
        painter.drawEllipse(int(highlight_x) - 6, int(highlight_y) - 6, 12, 12)

        painter.setPen(QColor("#22333b"))
        painter.setFont(QFont("Consolas", 11))
        formula_title, formula_text = self.current_demo().formula_descriptions()
        painter.drawText(panel_x + 20, panel_y + 30, f"Right: {formula_title}")
        painter.drawText(panel_x + 20, panel_y + 56, formula_text)
        painter.drawText(panel_x + 20, panel_y + 360, f"current x = {current_radian:6.3f} rad")
        painter.drawText(panel_x + 20, panel_y + 386, f"current value = {current_value:6.3f}")

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
        self.info_label.setStyleSheet(
            "font-family: Consolas; font-size: 14px; color: #22333b; padding: 8px;"
        )

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 360)
        self.slider.setValue(30)
        self.slider.valueChanged.connect(self.on_slider_changed)

        self.auto_timer = QTimer(self)
        self.auto_timer.timeout.connect(self.animate)
        self.auto_timer.start(40)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.info_label)
        layout.addWidget(self.slider)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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
