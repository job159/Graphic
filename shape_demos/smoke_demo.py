import math

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QColor, QLinearGradient, QPainter, QPen, QRadialGradient


class SmokeDemo:
    mode = "smoke"
    label = "Smoke"
    shape_subtitle = "A math-driven plume layers deterministic particles, curl flow, and diffusion."
    show_grid = False
    show_axes = False
    show_helpers = False
    show_vector = False
    show_point = False
    particle_count = 26
    detached_count = 8
    source_offsets = (-22, 0, 22)

    def density(self, radians: float) -> float:
        return 0.58 + 0.22 * (math.sin(radians - 0.35) ** 2) + 0.16 * math.sin(4 * radians + 0.25)

    def curl(self, radians: float) -> float:
        return 18 * math.sin(radians * 0.85) + 10 * math.sin(radians * 2.6 + 0.3)

    def plume_height(self, radians: float) -> float:
        return 124 + 56 * self.density(radians)

    def plume_spread(self, radians: float) -> float:
        return 44 + 18 * (0.5 + 0.5 * math.sin(radians * 1.6 - 0.25))

    def particle_state(
        self,
        center_x: int,
        center_y: int,
        radians: float,
        index: int,
    ) -> tuple[float, float, float, float, int, float]:
        density = self.density(radians)
        curl = self.curl(radians)
        base_y = center_y + 128
        age = ((radians * (0.36 + index * 0.019)) / math.tau + index * 0.137) % 1.0
        source_offset = self.source_offsets[index % len(self.source_offsets)] * (1.0 - 0.18 * age)
        rise = 18 + age * (126 + 64 * density)
        stream_pull = curl * (0.22 + 0.86 * age)
        wander = 18 * math.sin(radians * 0.82 + index * 1.17 + age * 4.8)
        micro_turbulence = 7 * (1.0 - age) * math.sin(radians * 2.6 + index * 0.9)
        x = center_x + source_offset + stream_pull + wander + micro_turbulence
        y = base_y - rise + 7 * math.sin(radians * 1.08 + index * 0.7 + age * 3.2)
        radius_x = 10 + age * (22 + 10 * density) + 2.5 * math.sin(index * 0.7 + radians)
        radius_y = 8 + age * (18 + 18 * density)
        alpha = int(64 * ((1.0 - age) ** 1.28) * (0.72 + 0.28 * density))
        return x, y, max(6.0, radius_x), max(5.0, radius_y), alpha, age

    def calculate_demo_point(
        self, center_x: int, center_y: int, radians: float, angle_degrees: float
    ) -> tuple[float, float, list[str]]:
        tracked_index = self.particle_count // 2
        point_x, point_y, _, _, _, age = self.particle_state(center_x, center_y, radians, tracked_index)
        density = self.density(radians)
        curl = self.curl(radians)
        plume_height = self.plume_height(radians)
        spread = self.plume_spread(radians)

        info_lines = [
            f"angle = {angle_degrees:6.1f} deg",
            f"radian = {radians:6.3f}",
            f"density = {density:6.3f}",
            f"height = {plume_height:6.1f} px",
            f"curl = {curl:6.1f} px, spread = {spread:5.1f} px",
            f"tracked puff age = {age:4.2f}, x = {point_x - center_x:6.1f}",
        ]
        return point_x, point_y, info_lines

    def draw_reference_shape(self, painter: QPainter, center_x: int, center_y: int) -> None:
        base_y = center_y + 146

        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)

        shadow = QRadialGradient(center_x, base_y + 22, 104)
        shadow.setColorAt(0.0, QColor(45, 53, 60, 46))
        shadow.setColorAt(1.0, QColor(45, 53, 60, 0))
        painter.setBrush(shadow)
        painter.drawEllipse(QPointF(center_x, base_y + 20), 116, 24)

        tray_gradient = QLinearGradient(center_x, base_y - 10, center_x, base_y + 32)
        tray_gradient.setColorAt(0.0, QColor("#7a848e"))
        tray_gradient.setColorAt(0.55, QColor("#5f6873"))
        tray_gradient.setColorAt(1.0, QColor("#444c55"))
        painter.setBrush(tray_gradient)
        painter.drawRoundedRect(center_x - 92, base_y + 10, 184, 28, 13, 13)

        vent_gradient = QLinearGradient(center_x, base_y - 30, center_x, base_y + 14)
        vent_gradient.setColorAt(0.0, QColor("#aab2bb"))
        vent_gradient.setColorAt(0.5, QColor("#7a838d"))
        vent_gradient.setColorAt(1.0, QColor("#58616b"))
        painter.setBrush(vent_gradient)
        painter.drawRoundedRect(center_x - 34, base_y - 10, 68, 28, 12, 12)

        painter.setBrush(QColor("#2d3339"))
        painter.drawEllipse(QPointF(center_x, base_y + 4), 18, 8)

        rim_glow = QRadialGradient(center_x, base_y + 2, 34)
        rim_glow.setColorAt(0.0, QColor(225, 231, 238, 58))
        rim_glow.setColorAt(1.0, QColor(225, 231, 238, 0))
        painter.setBrush(rim_glow)
        painter.drawEllipse(QPointF(center_x, base_y + 2), 34, 12)

        painter.setPen(QPen(QColor("#cfd6df"), 2))
        painter.drawLine(center_x - 132, base_y + 6, center_x + 132, base_y + 6)
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

        density = self.density(radians)
        curl = self.curl(radians)

        painter.save()
        self.draw_backlight(painter, center_x + curl * 0.1, center_y + 24, 138, QColor(198, 210, 221, 34))
        self.draw_emitter_haze(painter, center_x, center_y, radians, density)

        for lane_index, lane_offset in enumerate(self.source_offsets):
            self.draw_stream_band(
                painter,
                center_x,
                center_y,
                radians,
                density,
                curl,
                lane_index,
                lane_offset,
            )

        particle_states = [
            self.particle_state(center_x, center_y, radians, index) + (index,)
            for index in range(self.particle_count)
        ]
        particle_states.sort(key=lambda item: item[5], reverse=True)

        for x, y, radius_x, radius_y, alpha, age, index in particle_states:
            if alpha <= 4:
                continue

            self.draw_soft_ellipse(painter, x, y, radius_x, radius_y, QColor("#7b858f"), alpha)
            self.draw_soft_ellipse(
                painter,
                x + 6 * math.sin(radians + index * 0.7),
                y - 4,
                radius_x * 0.62,
                radius_y * 0.56,
                QColor("#c6ced4"),
                int(alpha * 0.58),
            )
            self.draw_soft_ellipse(
                painter,
                x - 4 * math.sin(radians * 0.7 + index),
                y + 3,
                radius_x * (0.68 + 0.12 * age),
                radius_y * 0.6,
                QColor("#5c636c"),
                int(alpha * 0.34),
            )

        self.draw_detached_particles(painter, center_x, center_y, radians, density, curl)
        painter.restore()

    def draw_backlight(self, painter: QPainter, x: float, y: float, radius: int, color: QColor) -> None:
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
        gradient.setColorAt(0.42, inner)
        gradient.setColorAt(1.0, outer)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(gradient)
        painter.drawEllipse(QPointF(x, y), radius_x, radius_y)

    def draw_emitter_haze(
        self,
        painter: QPainter,
        center_x: int,
        center_y: int,
        radians: float,
        density: float,
    ) -> None:
        base_y = center_y + 128
        base_radius = 36 + 10 * density
        drift = self.curl(radians) * 0.08
        self.draw_soft_ellipse(
            painter,
            center_x + drift,
            base_y - 10,
            base_radius,
            16 + 4 * density,
            QColor("#616973"),
            int(58 + 14 * density),
        )
        self.draw_soft_ellipse(
            painter,
            center_x + drift * 0.6,
            base_y - 4,
            base_radius * 0.58,
            9 + 3 * density,
            QColor("#c2c9cf"),
            int(34 + 10 * density),
        )

    def draw_stream_band(
        self,
        painter: QPainter,
        center_x: int,
        center_y: int,
        radians: float,
        density: float,
        curl: float,
        lane_index: int,
        lane_offset: float,
    ) -> None:
        base_y = center_y + 124
        samples = 9

        for sample_index in range(samples):
            u = sample_index / max(1, samples - 1)
            rise = 10 + u * (112 + 42 * density)
            x = center_x + lane_offset * (1.0 - 0.22 * u) + curl * (0.16 + 0.52 * u)
            x += 12 * math.sin(radians * 0.76 + lane_index * 1.12 + u * 5.4)
            x += 5 * math.sin(radians * 2.1 + lane_index * 0.8 + u * 8.3) * (1.0 - u)
            y = base_y - rise + 6 * math.sin(radians * 1.1 + lane_index + u * 4.6) * (1.0 - 0.28 * u)
            radius_x = 9 + u * (18 + 9 * density)
            radius_y = 7 + u * (14 + 10 * density)
            alpha = int((1.0 - 0.42 * u) * 46 * (0.62 + 0.38 * density))
            band_color = QColor("#737c86" if lane_index == 1 else "#68717a")
            self.draw_soft_ellipse(painter, x, y, radius_x, radius_y, band_color, alpha)

    def draw_detached_particles(
        self,
        painter: QPainter,
        center_x: int,
        center_y: int,
        radians: float,
        density: float,
        curl: float,
    ) -> None:
        base_y = center_y + 86

        for index in range(self.detached_count):
            age = ((radians * (0.2 + index * 0.028)) / math.tau + index * 0.173) % 1.0
            x = center_x + curl * 0.56 + 30 * math.sin(radians * 0.58 + index * 1.2 + age * 2.9)
            y = base_y - 28 - age * (82 + 18 * density)
            radius = 2.2 + age * 3.4
            alpha = int(34 * (1.0 - age) * (0.7 + 0.3 * density))
            self.draw_soft_ellipse(painter, x, y, radius * 1.2, radius, QColor("#9ca3aa"), alpha)

    def formula_value_for_graph(self, radians: float) -> float:
        return self.density(radians) - 0.7

    def formula_descriptions(self) -> tuple[str, str]:
        return (
            "Smoke Density Field",
            "y = 0.58 + 0.22*sin^2(t - 0.35) + 0.16*sin(4t + 0.25)",
        )

    def status_text(self, angle_degrees: int) -> str:
        radians = math.radians(angle_degrees)
        return (
            f"{self.label} | angle = {angle_degrees} deg | "
            f"density = {self.density(radians):.3f} | "
            f"height = {self.plume_height(radians):.1f}px | "
            f"curl = {self.curl(radians):.1f}px | "
            f"particles = {self.particle_count}"
        )
