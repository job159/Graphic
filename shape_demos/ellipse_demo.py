import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPen


class EllipseDemo:
    mode = "ellipse"
    label = "Ellipse"

    def calculate_demo_point(
        self, center_x: int, center_y: int, radians: float, angle_degrees: float
    ) -> tuple[float, float, list[str]]:
        radius_x = 160
        radius_y = 95
        point_x = center_x + radius_x * math.cos(radians)
        point_y = center_y - radius_y * math.sin(radians)

        info_lines = [
            f"angle = {angle_degrees:6.1f} deg",
            f"radian = {radians:6.3f}",
            f"a = {radius_x}, b = {radius_y}",
            f"x = a * cos(theta) = {point_x - center_x:6.1f}",
            f"y = b * sin(theta) = {center_y - point_y:6.1f}",
            "ellipse keeps x/y with different radii",
        ]
        return point_x, point_y, info_lines

    def draw_reference_shape(self, painter: QPainter, center_x: int, center_y: int) -> None:
        radius_x = 160
        radius_y = 95
        painter.setPen(QPen(QColor("#3d405b"), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(
            int(center_x - radius_x),
            int(center_y - radius_y),
            radius_x * 2,
            radius_y * 2,
        )

    def formula_value_for_graph(self, radians: float) -> float:
        return 0.75 * math.sin(radians)

    def formula_descriptions(self) -> tuple[str, str]:
        return "Ellipse Vertical Motion", "y = b * sin(theta), scaled for ellipse height"

    def status_text(self, angle_degrees: int) -> str:
        radians = math.radians(angle_degrees)
        return (
            f"{self.label} | angle = {angle_degrees} deg | "
            f"x = 160*cos(theta) = {160 * math.cos(radians):.1f} | "
            f"y = 95*sin(theta) = {95 * math.sin(radians):.1f}"
        )
