"""Camera capture utilities."""

from __future__ import annotations

import cv2


class Camera:
    def __init__(self, width: int, height: int, camera_id: int = 0) -> None:
        self._capture = cv2.VideoCapture(camera_id)
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self):
        ok, frame = self._capture.read()
        if not ok:
            return None
        return frame

    def release(self) -> None:
        self._capture.release()
