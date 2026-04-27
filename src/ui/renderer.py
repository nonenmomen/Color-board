"""Frame composition and helper drawing."""

from __future__ import annotations

import cv2


def draw_cursor(frame, point: tuple[int, int], color: tuple[int, int, int], radius: int) -> None:
    cv2.circle(frame, point, radius, color, 2)
    cv2.circle(frame, point, 3, color, -1)
