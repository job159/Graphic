import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPen


class SkewEllipseDemo:
    mode = "skew_ellipse"
    label = "Skew Ellipse"
    radius_x = 140
    radius_y = 95
    phi_degrees = 60

    def phi_radians(self) -> float:
        return math.radians(self.phi_degrees)

    def parametric_point(self, center_x: int, center_y: int, radians: float) -> tuple[float, float]:
        phi = self.phi_radians()
        x_offset = (
            self.radius_x * math.cos(radians) * math.cos(phi)
            - self.radius_y * math.sin(radians) * math.sin(phi)
        )
        y_offset = (
            self.radius_x * math.cos(radians) * math.sin(phi)
            + self.radius_y * math.sin(radians) * math.cos(phi)
        )
        return center_x + x_offset, center_y - y_offset

    def calculate_demo_point(
        self, center_x: int, center_y: int, radians: float, angle_degrees: float
    ) -> tuple[float, float, list[str]]:
        point_x, point_y = self.parametric_point(center_x, center_y, radians)
        x_offset = point_x - center_x
        y_offset = center_y - point_y

        info_lines = [
            f"angle = {angle_degrees:6.1f} deg",
            f"radian = {radians:6.3f}",
            f"a = {self.radius_x}, b = {self.radius_y}, phi = {self.phi_degrees} deg",
            "x = a*cos(t)*cos(phi) - b*sin(t)*sin(phi)",
            "y = a*cos(t)*sin(phi) + b*sin(t)*cos(phi)",
            f"x offset = {x_offset:6.1f}, y offset = {y_offset:6.1f}",
        ]
        return point_x, point_y, info_lines

    def draw_reference_shape(self, painter: QPainter, center_x: int, center_y: int) -> None:
        painter.setPen(QPen(QColor("#3d405b"), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)

        previous_point = None
        for degree in range(0, 361, 3):
            radians = math.radians(degree)
            x, y = self.parametric_point(center_x, center_y, radians)

            if previous_point is not None:
                painter.drawLine(int(previous_point[0]), int(previous_point[1]), int(x), int(y))

            previous_point = (x, y)

    def formula_value_for_graph(self, radians: float) -> float:
        phi = self.phi_radians()
        return (
            self.radius_x * math.cos(radians) * math.sin(phi)
            + self.radius_y * math.sin(radians) * math.cos(phi)
        ) / self.radius_x

    def formula_descriptions(self) -> tuple[str, str]:
        return "Rotated Ellipse Vertical Motion", "y = a*cos(t)*sin(phi) + b*sin(t)*cos(phi)"

    def status_text(self, angle_degrees: int) -> str:
        radians = math.radians(angle_degrees)
        phi = self.phi_radians()
        x_offset = (
            self.radius_x * math.cos(radians) * math.cos(phi)
            - self.radius_y * math.sin(radians) * math.sin(phi)
        )
        y_offset = (
            self.radius_x * math.cos(radians) * math.sin(phi)
            + self.radius_y * math.sin(radians) * math.cos(phi)
        )
        return (
            f"{self.label} | angle = {angle_degrees} deg | "
            f"phi = {self.phi_degrees} deg | "
            f"x offset = {x_offset:.1f} | y offset = {y_offset:.1f}"
        )
