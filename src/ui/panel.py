"""Side panel rendering and hit testing."""

from __future__ import annotations

from dataclasses import dataclass

import cv2

from config import PANEL_BG_COLOR


@dataclass
class ColorItem:
    id: str
    center: tuple[int, int]
    radius: int
    color: tuple[int, int, int]


@dataclass
class RectButton:
    id: str
    x1: int
    y1: int
    x2: int
    y2: int
    label: str


class SidePanel:
    def __init__(self, width: int, frame_height: int, colors: list[tuple[int, int, int]]) -> None:
        self.width = width
        self.frame_height = frame_height
        self.items: list[ColorItem] = []

        top_offset = 80
        gap = 70
        radius = 22
        cx = width // 2
        for idx, color in enumerate(colors):
            self.items.append(
                ColorItem(
                    id=f"color:{idx}",
                    center=(cx, top_offset + idx * gap),
                    radius=radius,
                    color=color,
                )
            )

        self.clear_button = RectButton(
            id="action:clear",
            x1=30,
            y1=frame_height - 100,
            x2=width - 30,
            y2=frame_height - 45,
            label="Clear",
        )

    def draw(self, frame, active_color_id: str | None) -> None:
        cv2.rectangle(frame, (0, 0), (self.width, self.frame_height), PANEL_BG_COLOR, -1)
        cv2.putText(frame, "Colors", (28, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (220, 220, 220), 2, cv2.LINE_AA)

        for item in self.items:
            cv2.circle(frame, item.center, item.radius, item.color, -1)
            border_color = (255, 255, 255) if item.id == active_color_id else (80, 80, 80)
            cv2.circle(frame, item.center, item.radius + 3, border_color, 2)

        btn = self.clear_button
        cv2.rectangle(frame, (btn.x1, btn.y1), (btn.x2, btn.y2), (50, 50, 50), -1)
        cv2.rectangle(frame, (btn.x1, btn.y1), (btn.x2, btn.y2), (200, 200, 200), 2)
        cv2.putText(
            frame,
            btn.label,
            (btn.x1 + 42, btn.y1 + 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (240, 240, 240),
            2,
            cv2.LINE_AA,
        )

    def hit_test(self, x: int, y: int) -> str | None:
        for item in self.items:
            dx = x - item.center[0]
            dy = y - item.center[1]
            if dx * dx + dy * dy <= item.radius * item.radius:
                return item.id

        btn = self.clear_button
        if btn.x1 <= x <= btn.x2 and btn.y1 <= y <= btn.y2:
            return btn.id
        return None
