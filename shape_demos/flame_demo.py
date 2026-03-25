import math

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath, QPen, QPolygonF, QRadialGradient


class FlameDemo:
    mode = "flame"
    label = "Flame"
    shape_subtitle = "Three layered peaks form a 山-shaped flame with smoke and ember particles."
    show_grid = False
    show_axes = False
    show_helpers = False
    show_vector = False
    show_point = False
    spark_count = 8
    smoke_count = 7
    peak_offsets = (-38, 0, 38)

    def intensity(self, radians: float) -> float:
        return 0.62 + 0.26 * (math.sin(radians) ** 2) + 0.12 * math.sin(6 * radians)

    def sway(self, radians: float) -> float:
        return 16 * math.sin(radians) + 6 * math.sin(3 * radians)

    def curl(self, radians: float) -> float:
        return 12 * math.sin(radians * 1.65 - 0.5)

    def flame_height(self, radians: float) -> float:
        return 138 + 66 * self.intensity(radians)

    def tip_position(self, center_x: int, center_y: int, radians: float) -> tuple[float, float]:
        base_y = center_y + 132
        tip_x = center_x + self.sway(radians) * 0.54 + self.curl(radians) * 0.18
        tip_y = base_y - self.flame_height(radians) * 1.04
        return tip_x, tip_y

    def calculate_demo_point(
        self, center_x: int, center_y: int, radians: float, angle_degrees: float
    ) -> tuple[float, float, list[str]]:
        tip_x, tip_y = self.tip_position(center_x, center_y, radians)
        intensity = self.intensity(radians)
        sway = self.sway(radians)
        flame_height = self.flame_height(radians)
        spark_lift = 54 + 24 * (0.5 + 0.5 * math.sin(radians * 2.2))

        info_lines = [
            f"angle = {angle_degrees:6.1f} deg",
            f"radian = {radians:6.3f}",
            f"intensity = {intensity:6.3f}",
            f"height = {flame_height:6.1f} px",
            f"sway = {sway:6.1f} px",
            f"peaks = 3, sparks = {self.spark_count}, lift = {spark_lift:5.1f}",
        ]
        return tip_x, tip_y, info_lines

    def draw_reference_shape(self, painter: QPainter, center_x: int, center_y: int) -> None:
        base_y = center_y + 142

        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)

        tray_gradient = QLinearGradient(center_x, base_y - 8, center_x, base_y + 28)
        tray_gradient.setColorAt(0.0, QColor("#727c87"))
        tray_gradient.setColorAt(0.55, QColor("#5a636e"))
        tray_gradient.setColorAt(1.0, QColor("#434b54"))
        painter.setBrush(tray_gradient)
        painter.drawRoundedRect(center_x - 68, base_y + 8, 136, 26, 11, 11)

        ember_bed = QRadialGradient(center_x, base_y + 8, 78)
        ember_bed.setColorAt(0.0, QColor(255, 188, 84, 105))
        ember_bed.setColorAt(0.45, QColor(255, 125, 52, 55))
        ember_bed.setColorAt(1.0, QColor(255, 110, 48, 0))
        painter.setBrush(ember_bed)
        painter.drawEllipse(QPointF(center_x, base_y + 18), 82, 34)

        painter.setBrush(QColor("#2e343b"))
        painter.drawRoundedRect(center_x - 50, base_y + 10, 40, 12, 6, 6)
        painter.drawRoundedRect(center_x - 10, base_y + 9, 46, 13, 6, 6)
        painter.drawRoundedRect(center_x + 28, base_y + 11, 30, 11, 5, 5)

        painter.setPen(QPen(QColor("#cfd6df"), 2))
        painter.drawLine(center_x - 124, base_y, center_x + 124, base_y)
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
        del point_x, point_y, angle_degrees

        intensity = self.intensity(radians)
        sway = self.sway(radians)
        curl = self.curl(radians)

        base_shell = self.flame_points(
            center_x,
            center_y + 42,
            radians + 0.04,
            width_scale=1.16,
            height_scale=0.50,
        )
        left_outer = self.flame_points(
            center_x - 42 + sway * 0.08,
            center_y + 26,
            radians + 0.55,
            width_scale=0.42,
            height_scale=0.74,
        )
        center_outer = self.flame_points(
            center_x + sway * 0.05,
            center_y - 10,
            radians + 0.06,
            width_scale=0.58,
            height_scale=0.78,
        )
        right_outer = self.flame_points(
            center_x + 42 + curl * 0.07,
            center_y + 24,
            radians + 0.88,
            width_scale=0.40,
            height_scale=0.70,
        )
        left_mid = self.flame_points(
            center_x - 30 + sway * 0.06,
            center_y + 42,
            radians + 0.40,
            width_scale=0.27,
            height_scale=0.34,
        )
        center_mid = self.flame_points(
            center_x + sway * 0.03,
            center_y + 8,
            radians + 0.22,
            width_scale=0.40,
            height_scale=0.82,
        )
        right_mid = self.flame_points(
            center_x + 30 + curl * 0.05,
            center_y + 40,
            radians + 0.73,
            width_scale=0.25,
            height_scale=0.52,
        )
        left_core = self.flame_points(
            center_x - 18,
            center_y + 58,
            radians + 0.34,
            width_scale=0.16,
            height_scale=0.18,
        )
        center_core = self.flame_points(
            center_x,
            center_y + 28,
            radians + 0.28,
            width_scale=0.24,
            height_scale=0.30,
        )
        right_core = self.flame_points(
            center_x + 18,
            center_y + 58,
            radians + 0.62,
            width_scale=0.15,
            height_scale=0.17,
        )
        blue_core_points = self.flame_points(
            center_x,
            center_y + 56,
            radians + 0.22,
            width_scale=0.12,
            height_scale=0.16,
        )

        painter.save()
        self.draw_smoke_wisps(painter, center_x, center_y, radians, intensity)
        self.draw_flame_glow(
            painter,
            center_x + sway * 0.12,
            center_y + 88,
            184,
            QColor(255, 159, 72, 98),
        )
        self.draw_flame_glow(
            painter,
            center_x + sway * 0.08,
            center_y + 54,
            122,
            QColor(255, 212, 122, 82),
        )
        for peak_offset, peak_radius in zip(self.peak_offsets, (56, 72, 56)):
            self.draw_flame_glow(
                painter,
                center_x + peak_offset + sway * 0.06,
                center_y + 36 if peak_offset == 0 else center_y + 58,
                peak_radius,
                QColor(255, 176, 84, 40),
            )
        self.draw_base_ember_particles(painter, center_x, center_y, radians, intensity)
        self.draw_flame_layer(
            painter,
            base_shell,
            QColor("#ffd98e"),
            QColor("#ff9644"),
            QColor("#c9451d"),
            outline=QColor(130, 52, 16, 44),
        )
        self.draw_flame_layer(
            painter,
            left_outer,
            QColor("#fff0b4"),
            QColor("#ffab4d"),
            QColor("#db5220"),
            outline=QColor(152, 58, 18, 52),
        )
        self.draw_flame_layer(
            painter,
            right_outer,
            QColor("#fff0b4"),
            QColor("#ffab4d"),
            QColor("#db5220"),
            outline=QColor(152, 58, 18, 52),
        )
        self.draw_flame_layer(
            painter,
            center_outer,
            QColor("#fff5c8"),
            QColor("#ffb75a"),
            QColor("#df5b22"),
            outline=QColor(152, 58, 18, 60),
        )
        self.draw_flame_layer(
            painter,
            left_mid,
            QColor("#fff9da"),
            QColor("#ffd96f"),
            QColor("#ff8f34"),
            outline=QColor(171, 91, 19, 36),
        )
        self.draw_flame_layer(
            painter,
            right_mid,
            QColor("#fff9da"),
            QColor("#ffd96f"),
            QColor("#ff8f34"),
            outline=QColor(171, 91, 19, 36),
        )
        self.draw_flame_layer(
            painter,
            center_mid,
            QColor("#fffce8"),
            QColor("#ffe07c"),
            QColor("#ff9838"),
            outline=QColor(171, 91, 19, 44),
        )
        self.draw_flame_layer(
            painter,
            left_core,
            QColor("#fffef4"),
            QColor("#fff0b4"),
            QColor("#ffc44d"),
            outline=QColor(212, 164, 62, 20),
        )
        self.draw_flame_layer(
            painter,
            right_core,
            QColor("#fffef4"),
            QColor("#fff0b4"),
            QColor("#ffc44d"),
            outline=QColor(212, 164, 62, 20),
        )
        self.draw_flame_layer(
            painter,
            center_core,
            QColor("#ffffff"),
            QColor("#fff6c6"),
            QColor("#ffcb52"),
            outline=QColor(212, 164, 62, 30),
        )
        self.draw_flame_layer(
            painter,
            blue_core_points,
            QColor("#ebfcff"),
            QColor("#a2ddff"),
            QColor("#397cff"),
            outline=QColor(36, 98, 182, 20),
        )
        self.draw_spark_particles(painter, center_x, center_y, radians, intensity)
        self.draw_ash_particles(painter, center_x, center_y, radians)
        painter.restore()

    def flame_points(
        self,
        center_x: int,
        center_y: int,
        radians: float,
        *,
        width_scale: float,
        height_scale: float,
    ) -> list[tuple[float, float]]:
        base_y = center_y + 142
        flame_height = self.flame_height(radians) * height_scale
        sway = self.sway(radians) * width_scale
        curl = self.curl(radians) * width_scale
        base_width = 68 * width_scale
        sample_count = 24
        points: list[tuple[float, float]] = []

        for index in range(sample_count + 1):
            u = index / sample_count
            width = base_width * (math.sin(math.pi * u) ** 0.86) * (1.0 - 0.17 * u)
            width *= 0.94 + 0.14 * math.sin(radians * 2.4 + u * 4.8) + 0.04 * math.sin(radians * 5.8 + u * 10.0)
            lift = flame_height * (u**0.9)
            curve = sway * ((1.0 - u) ** 0.72) + curl * u * (1.0 - 0.35 * u)
            flutter = 9 * width_scale * math.sin(radians * 4.2 + u * 6.4) * math.sin(math.pi * u)
            tip_pull = 11 * width_scale * math.sin(radians * 2.1 - 0.4) * (u**1.65)
            x = center_x - width + curve - flutter - tip_pull
            y = base_y - lift + 5 * width_scale * math.sin(radians * 3.6 + u * 4.4) * (1.0 - u)
            points.append((x, y))

        for index in range(sample_count, -1, -1):
            u = index / sample_count
            width = base_width * (math.sin(math.pi * u) ** 0.86) * (1.0 - 0.17 * u)
            width *= 0.94 + 0.14 * math.sin(radians * 2.4 + u * 4.8) + 0.04 * math.sin(radians * 5.8 + u * 10.0)
            lift = flame_height * (u**0.9)
            curve = sway * ((1.0 - u) ** 0.72) + curl * u * (1.0 - 0.35 * u)
            flutter = 9 * width_scale * math.sin(radians * 4.2 + u * 6.4) * math.sin(math.pi * u)
            tip_pull = 11 * width_scale * math.sin(radians * 2.1 - 0.4) * (u**1.65)
            x = center_x + width + curve + flutter - tip_pull * 0.42
            y = base_y - lift - 3 * width_scale * math.sin(radians * 3.1 + u * 5.7) * (1.0 - u)
            points.append((x, y))

        return points

    def draw_flame_layer(
        self,
        painter: QPainter,
        points: list[tuple[float, float]],
        tip_color: QColor,
        middle_color: QColor,
        base_color: QColor,
        *,
        outline: QColor,
    ) -> None:
        polygon = QPolygonF(QPointF(x, y) for x, y in points)
        path = QPainterPath()
        path.addPolygon(polygon)
        path.closeSubpath()

        min_y = min(point[1] for point in points)
        max_y = max(point[1] for point in points)
        gradient = QLinearGradient(0, min_y, 0, max_y)
        gradient.setColorAt(0.0, tip_color)
        gradient.setColorAt(0.35, middle_color)
        gradient.setColorAt(1.0, base_color)

        painter.fillPath(path, gradient)
        painter.setPen(QPen(outline, 1.2))
        painter.drawPath(path)

    def draw_flame_glow(self, painter: QPainter, x: float, y: float, radius: int, color: QColor) -> None:
        gradient = QRadialGradient(x, y, radius)
        gradient.setColorAt(0.0, color)
        fade = QColor(color)
        fade.setAlpha(0)
        gradient.setColorAt(1.0, fade)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(gradient)
        painter.drawEllipse(QPointF(x, y), radius, radius)

    def draw_soft_ellipse(
        self,
        painter: QPainter,
        x: float,
        y: float,
        radius_x: float,
        radius_y: float,
        color: QColor,
        alpha: int,
    ) -> None:
        if alpha <= 0:
            return

        gradient = QRadialGradient(x, y, max(radius_x, radius_y))
        inner = QColor(color)
        inner.setAlpha(min(255, alpha))
        outer = QColor(color)
        outer.setAlpha(0)
        gradient.setColorAt(0.0, inner)
        gradient.setColorAt(0.45, inner)
        gradient.setColorAt(1.0, outer)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(gradient)
        painter.drawEllipse(QPointF(x, y), radius_x, radius_y)

    def draw_smoke_wisps(
        self,
        painter: QPainter,
        center_x: int,
        center_y: int,
        radians: float,
        intensity: float,
    ) -> None:
        base_y = center_y + 42
        stream_bias = self.sway(radians) * 0.12 + self.curl(radians) * 0.12

        for index in range(self.smoke_count):
            age = ((radians * (0.2 + index * 0.022)) / math.tau + index * 0.173) % 1.0
            source_offset = self.peak_offsets[index % 3] * 0.6
            rise = 24 + age * 154
            drift = source_offset + stream_bias + 20 * math.sin(radians * 0.62 + index * 1.17 + age * 2.6)
            puff_x = center_x + drift
            puff_y = base_y - rise
            puff_rx = 14 + age * 18 + 3 * math.sin(index + radians * 0.8)
            puff_ry = 10 + age * 14
            alpha = int((1.0 - age) * 52 * (0.65 + 0.35 * intensity))
            self.draw_soft_ellipse(painter, puff_x, puff_y, puff_rx, puff_ry, QColor("#68707b"), alpha)
            self.draw_soft_ellipse(
                painter,
                puff_x + 8 * math.sin(index + radians),
                puff_y - 5,
                puff_rx * 0.62,
                puff_ry * 0.58,
                QColor("#8d949c"),
                int(alpha * 0.55),
            )

    def draw_base_ember_particles(
        self,
        painter: QPainter,
        center_x: int,
        center_y: int,
        radians: float,
        intensity: float,
    ) -> None:
        base_y = center_y + 154

        for index in range(10):
            phase = radians * 1.9 + index * 0.73
            ember_x = center_x - 42 + index * 9 + 3.5 * math.sin(phase)
            ember_y = base_y + 2.2 * math.sin(phase * 1.35)
            ember_size = 2.1 + 1.9 * (0.5 + 0.5 * math.sin(phase * 2.1))
            ember_alpha = int(118 + 82 * intensity * (0.4 + 0.6 * (0.5 + 0.5 * math.sin(phase * 1.7))))
            ember_color = QColor("#ffd874") if index % 3 == 0 else QColor("#ff9f43")
            self.draw_soft_ellipse(painter, ember_x, ember_y, ember_size, ember_size * 0.8, ember_color, ember_alpha)

    def draw_spark_particles(
        self,
        painter: QPainter,
        center_x: int,
        center_y: int,
        radians: float,
        intensity: float,
    ) -> None:
        base_y = center_y + 118

        for index in range(self.spark_count):
            age = ((radians * (0.86 + index * 0.055)) / math.tau + index * 0.119) % 1.0
            source_offset = self.peak_offsets[index % 3]
            rise = 14 + age * (64 + index * 6.0)
            drift = (
                source_offset * (0.62 + 0.25 * (index % 2))
                + self.sway(radians) * 0.16
                + 18 * math.sin(radians * 0.95 + index * 0.91 + age * 4.0)
                + 7 * math.sin(radians * 2.1 + index)
            )
            spark_x = center_x + drift
            spark_y = base_y - rise
            spark_size = 1.5 + 2.4 * (1.0 - age) * (0.55 + 0.45 * math.sin(index * 1.3 + radians))
            spark_alpha = int(212 * ((1.0 - age) ** 1.5) * (0.65 + 0.35 * intensity))

            if spark_alpha <= 10:
                continue

            trail_dx = 4 * math.sin(radians * 0.9 + index * 1.4)
            trail_dy = 10 + 18 * age
            trail_color = QColor("#ffb45a")
            trail_color.setAlpha(int(spark_alpha * 0.42))
            painter.setPen(
                QPen(
                    trail_color,
                    max(1.0, spark_size * 0.36),
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                )
            )
            painter.drawLine(
                QPointF(spark_x - trail_dx, spark_y + trail_dy),
                QPointF(spark_x, spark_y),
            )
            self.draw_soft_ellipse(
                painter,
                spark_x,
                spark_y,
                spark_size * 1.75,
                spark_size * 1.35,
                QColor("#ffd27a"),
                spark_alpha,
            )
            self.draw_soft_ellipse(
                painter,
                spark_x,
                spark_y,
                max(0.8, spark_size * 0.72),
                max(0.8, spark_size * 0.6),
                QColor("#fff9d6"),
                min(255, int(spark_alpha * 1.1)),
            )

    def draw_ash_particles(self, painter: QPainter, center_x: int, center_y: int, radians: float) -> None:
        base_y = center_y + 92

        for index in range(6):
            age = ((radians * (0.34 + index * 0.03)) / math.tau + index * 0.163) % 1.0
            source_offset = self.peak_offsets[index % 3] * 0.38
            drift = source_offset + self.sway(radians) * 0.06 + 14 * math.sin(radians * 0.54 + index * 1.1 + age * 2.4)
            ash_x = center_x + drift
            ash_y = base_y - (34 + age * 118)
            ash_size = 1.2 + 0.9 * age
            ash_alpha = int(52 * (1.0 - age))
            self.draw_soft_ellipse(painter, ash_x, ash_y, ash_size, ash_size, QColor("#9aa0a8"), ash_alpha)

    def formula_value_for_graph(self, radians: float) -> float:
        return self.intensity(radians) - 0.74

    def formula_descriptions(self) -> tuple[str, str]:
        return (
            "Flame Intensity",
            "y = 0.62 + 0.26*sin^2(t) + 0.12*sin(6t)",
        )

    def status_text(self, angle_degrees: int) -> str:
        radians = math.radians(angle_degrees)
        return (
            f"{self.label} | angle = {angle_degrees} deg | "
            f"intensity = {self.intensity(radians):.3f} | "
            f"height = {self.flame_height(radians):.1f}px | "
            f"sway = {self.sway(radians):.1f}px | "
            f"peaks = 3 | sparks = {self.spark_count}"
        )
