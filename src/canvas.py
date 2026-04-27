"""Drawing canvas abstraction."""

from __future__ import annotations

import cv2
import numpy as np


class DrawingCanvas:
    def __init__(self, width: int, height: int) -> None:
        self._canvas = np.zeros((height, width, 3), dtype=np.uint8)

    def clear(self) -> None:
        self._canvas[:] = 0

    def draw_line(self, p1: tuple[int, int], p2: tuple[int, int], color: tuple[int, int, int], thickness: int) -> None:
        cv2.line(self._canvas, p1, p2, color, thickness, lineType=cv2.LINE_AA)

    def blend_with(self, frame, alpha: float = 1.0):
        if alpha >= 1.0:
            return cv2.add(frame, self._canvas)
        return cv2.addWeighted(frame, 1.0, self._canvas, alpha, 0)
