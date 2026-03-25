import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QLinearGradient, QPainter, QPen, QRadialGradient


class LightningDemo:
    mode = "lightning"
    label = "Lightning"
    shape_subtitle = "Layered channels, branch leaders, and impact flash mimic a storm strike."
    show_grid = False
    show_axes = False
    show_helpers = False
    show_vector = False
    show_point = False

    def strike_origin(self, center_x: int, center_y: int) -> tuple[float, float]:
        return center_x, center_y - 26

    def calculate_demo_point(
        self, center_x: int, center_y: int, radians: float, angle_degrees: float
    ) -> tuple[float, float, list[str]]:
        horizontal = 84 * math.sin(radians * 1.15) + 26 * math.sin(radians * 2.8 + 0.35)
        vertical = 136 + 22 * (0.5 + 0.5 * math.sin(radians * 2.1 - 0.55))
        point_x = center_x + horizontal
        point_y = center_y + vertical
        energy = self.formula_value_for_graph(radians)
        reach = math.hypot(horizontal, vertical)
        branches = 3 + int((math.sin(radians * 2.7) + 1.0) * 1.1)
        spread = 34 + 18 * (0.5 + 0.5 * math.sin(radians * 2.3 + 0.8))

        info_lines = [
            f"angle = {angle_degrees:6.1f} deg",
            f"radian = {radians:6.3f}",
            f"energy = {energy:6.3f}",
            f"reach = {reach:6.1f} px",
            f"branches = {branches}, spread = {spread:5.1f} px",
            f"impact x = {horizontal:6.1f}, y = {vertical:6.1f}",
        ]
        return point_x, point_y, info_lines

    def draw_reference_shape(self, painter: QPainter, center_x: int, center_y: int) -> None:
        origin_x, origin_y = self.strike_origin(center_x, center_y)
        ground_y = center_y + 156

        painter.save()

        sky_glow = QRadialGradient(origin_x, origin_y + 8, 138)
        sky_glow.setColorAt(0.0, QColor(210, 225, 255, 110))
        sky_glow.setColorAt(0.55, QColor(185, 205, 240, 40))
        sky_glow.setColorAt(1.0, QColor(185, 205, 240, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(sky_glow)
        painter.drawEllipse(int(origin_x - 138), int(origin_y - 98), 276, 196)

        cloud_gradient = QLinearGradient(origin_x, origin_y - 44, origin_x, origin_y + 38)
        cloud_gradient.setColorAt(0.0, QColor("#5d6875"))
        cloud_gradient.setColorAt(0.55, QColor("#46515c"))
        cloud_gradient.setColorAt(1.0, QColor("#38414b"))
        painter.setBrush(cloud_gradient)
        painter.drawEllipse(int(origin_x - 94), int(origin_y - 34), 74, 46)
        painter.drawEllipse(int(origin_x - 46), int(origin_y - 48), 94, 62)
        painter.drawEllipse(int(origin_x + 14), int(origin_y - 34), 82, 46)
        painter.drawRoundedRect(int(origin_x - 80), int(origin_y - 6), 160, 40, 18, 18)

        painter.setBrush(QColor(255, 255, 255, 30))
        painter.drawEllipse(int(origin_x - 36), int(origin_y - 36), 52, 18)
        painter.drawEllipse(int(origin_x + 24), int(origin_y - 24), 40, 14)

        ground_gradient = QLinearGradient(center_x, ground_y - 10, center_x, ground_y + 12)
        ground_gradient.setColorAt(0.0, QColor("#cfd7e0"))
        ground_gradient.setColorAt(1.0, QColor("#eef2f6"))
        painter.setBrush(ground_gradient)
        painter.drawRoundedRect(int(center_x - 156), ground_y - 2, 312, 18, 8, 8)

        painter.restore()

    def draw_effect(
        self,
        painter: QPainter,
        center_x: int,
        center_y: int,
        point_x: float,
        point_y: float,
        radians: float,
        angle_degrees: float,
    ) -> None:
        origin_x, origin_y = self.strike_origin(center_x, center_y)
        energy = self.energy_ratio(radians)
        main_points = self.bolt_points(
            origin_x,
            origin_y,
            point_x,
            point_y,
            angle_degrees,
            phase_shift=0.0,
            segments=11,
            irregularity=1.0,
        )

        painter.save()
        self.draw_flash_halo(painter, origin_x, origin_y + 10, 132, QColor(210, 228, 255, 80))
        self.draw_flash_halo(painter, point_x, point_y, 64, QColor(255, 237, 181, 95))
        self.draw_ground_flash(painter, point_x, point_y)
        self.draw_channel(painter, main_points, 11.0 + 3.0 * energy, 2.2)

        branch_count = 3 + int((math.sin(radians * 2.7) + 1.0) * 1.1)
        spread_base = 30 + 18 * energy
        for branch_index in range(branch_count):
            anchor_index = min(len(main_points) - 2, 2 + branch_index * 2)
            anchor_x, anchor_y = main_points[anchor_index]
            direction = -1.0 if branch_index % 2 == 0 else 1.0
            spread = spread_base + branch_index * 12
            branch_end_x = anchor_x + direction * spread + 10 * math.sin(radians * 1.6 + branch_index)
            branch_end_y = anchor_y + 30 + branch_index * 14 + 6 * math.sin(radians * 2.1 + branch_index * 0.7)
            branch_points = self.bolt_points(
                anchor_x,
                anchor_y,
                branch_end_x,
                branch_end_y,
                angle_degrees,
                phase_shift=0.85 + branch_index * 0.55,
                segments=5,
                irregularity=0.68,
            )
            base_width = max(2.0, 5.4 - branch_index * 0.5)
            self.draw_channel(painter, branch_points, base_width, 1.2, glow_alpha=86, core_alpha=232)

        painter.restore()

    def bolt_points(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        angle_degrees: float,
        *,
        phase_shift: float,
        segments: int,
        irregularity: float,
    ) -> list[tuple[float, float]]:
        dx = end_x - start_x
        dy = end_y - start_y
        length = max(1.0, math.hypot(dx, dy))
        normal_x = -dy / length
        normal_y = dx / length
        angle_radians = math.radians(angle_degrees)
        points = [(start_x, start_y)]

        for step in range(1, segments):
            t = step / segments
            base_x = start_x + dx * t
            base_y = start_y + dy * t
            envelope = 0.32 + 0.68 * math.sin(math.pi * t)
            jitter = irregularity * envelope * (
                18 * math.sin(angle_radians * 1.45 + phase_shift + t * 6.8)
                + 9 * math.sin(angle_radians * 3.25 + phase_shift * 1.3 + t * 12.5)
                + 5 * (0.45 - t) * math.sin(angle_radians * 5.1 + t * 18.0)
            )
            surge = irregularity * 5.0 * math.sin(angle_radians * 2.15 + phase_shift + t * 9.2)
            points.append((base_x + normal_x * jitter, base_y + normal_y * jitter * 0.36 + surge))

        points.append((end_x, end_y))
        return points

    def draw_channel(
        self,
        painter: QPainter,
        points: list[tuple[float, float]],
        start_width: float,
        end_width: float,
        *,
        glow_alpha: int = 108,
        core_alpha: int = 245,
    ) -> None:
        self.draw_channel_layer(
            painter,
            points,
            start_width * 2.2,
            end_width * 1.8,
            QColor(150, 214, 255, glow_alpha),
        )
        self.draw_channel_layer(
            painter,
            points,
            start_width,
            end_width,
            QColor(186, 232, 255, min(255, glow_alpha + 56)),
        )
        self.draw_channel_layer(
            painter,
            points,
            max(1.4, start_width * 0.28),
            max(0.9, end_width * 0.4),
            QColor(255, 250, 232, core_alpha),
        )

    def draw_channel_layer(
        self,
        painter: QPainter,
        points: list[tuple[float, float]],
        start_width: float,
        end_width: float,
        color: QColor,
    ) -> None:
        segment_count = max(1, len(points) - 1)
        for index, (start, end) in enumerate(zip(points, points[1:])):
            ratio = index / max(1, segment_count - 1)
            width = start_width + (end_width - start_width) * ratio
            painter.setPen(
                QPen(
                    color,
                    width,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin,
                )
            )
            painter.drawLine(int(start[0]), int(start[1]), int(end[0]), int(end[1]))

    def draw_flash_halo(self, painter: QPainter, x: float, y: float, radius: int, color: QColor) -> None:
        gradient = QRadialGradient(x, y, radius)
        gradient.setColorAt(0.0, color)
        fade = QColor(color)
        fade.setAlpha(0)
        gradient.setColorAt(1.0, fade)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(gradient)
        painter.drawEllipse(int(x - radius), int(y - radius), radius * 2, radius * 2)

    def draw_ground_flash(self, painter: QPainter, point_x: float, point_y: float) -> None:
        self.draw_flash_halo(painter, point_x, point_y + 6, 46, QColor(255, 233, 182, 72))

        painter.setPen(QPen(QColor(255, 246, 214, 210), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        for direction in (-1, 1):
            painter.drawLine(int(point_x), int(point_y), int(point_x + direction * 16), int(point_y + 12))
            painter.drawLine(int(point_x), int(point_y + 2), int(point_x + direction * 10), int(point_y + 20))

    def energy_ratio(self, radians: float) -> float:
        return max(0.18, min(1.0, (self.formula_value_for_graph(radians) + 1.05) / 2.05))

    def formula_value_for_graph(self, radians: float) -> float:
        return 0.72 * math.sin(radians) + 0.24 * math.sin(5 * radians) + 0.14 * math.cos(9 * radians - 0.4)

    def formula_descriptions(self) -> tuple[str, str]:
        return (
            "Electric Arc Intensity",
            "y = 0.72*sin(t) + 0.24*sin(5t) + 0.14*cos(9t - 0.4)",
        )

    def status_text(self, angle_degrees: int) -> str:
        radians = math.radians(angle_degrees)
        point_x = 84 * math.sin(radians * 1.15) + 26 * math.sin(radians * 2.8 + 0.35)
        point_y = 136 + 22 * (0.5 + 0.5 * math.sin(radians * 2.1 - 0.55))
        reach = math.hypot(point_x, point_y)
        return (
            f"{self.label} | angle = {angle_degrees} deg | "
            f"energy = {self.formula_value_for_graph(radians):.3f} | "
            f"reach = {reach:.1f}px"
        )
