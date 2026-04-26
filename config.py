"""Global configuration for FingerBoard."""

from __future__ import annotations

WINDOW_NAME = "FingerBoard"

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

PANEL_WIDTH = 220
PANEL_BG_COLOR = (32, 32, 32)

COLORS = [
    (0, 0, 255),      # Red
    (0, 255, 0),      # Green
    (255, 0, 0),      # Blue
    (0, 255, 255),    # Yellow
    (255, 255, 255),  # White
    (255, 0, 255),    # Magenta
]

BRUSH_SIZE = 6
CURSOR_RADIUS = 10

COLOR_HOVER_SECONDS = 0.5
CLEAR_HOVER_SECONDS = 0.5

MP_MAX_NUM_HANDS = 1
MP_DETECTION_CONFIDENCE = 0.7
MP_TRACKING_CONFIDENCE = 0.6
