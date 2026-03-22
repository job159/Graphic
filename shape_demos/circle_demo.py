import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPen


class CircleDemo:
    mode = "circle"
    label = "Circle"

    def calculate_demo_point(
        self, center_x: int, center_y: int, radians: float, angle_degrees: float
    ) -> tuple[float, float, list[str]]:
        radius = 140
        cos_value = math.cos(radians)
        sin_value = math.sin(radians)
        point_x = center_x + radius * cos_value
        point_y = center_y - radius * sin_value

        info_lines = [
            f"angle = {angle_degrees:6.1f} deg",
            f"radian = {radians:6.3f}",
            f"cos(theta) = {cos_value:6.3f}",
            f"sin(theta) = {sin_value:6.3f}",
            f"x = r * cos(theta) = {point_x - center_x:6.1f}",
            f"y = r * sin(theta) = {center_y - point_y:6.1f}",
        ]
        return point_x, point_y, info_lines

    def draw_reference_shape(self, painter: QPainter, center_x: int, center_y: int) -> None:
        radius = 140
        painter.setPen(QPen(QColor("#3d405b"), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(int(center_x - radius), int(center_y - radius), radius * 2, radius * 2)

    def formula_value_for_graph(self, radians: float) -> float:
        return math.sin(radians)

    def formula_descriptions(self) -> tuple[str, str]:
        return "Sine Wave Demo", "y = sin(x), x from 0 to 2pi"

    def status_text(self, angle_degrees: int) -> str:
        radians = math.radians(angle_degrees)
        return (
            f"{self.label} | angle = {angle_degrees} deg | radian = {radians:.3f} | "
            f"cos = {math.cos(radians):.3f} | sin = {math.sin(radians):.3f}"
        )
