from __future__ import annotations

import cv2

from config import (
    BRUSH_SIZE,
    CLEAR_HOVER_SECONDS,
    COLOR_HOVER_SECONDS,
    COLORS,
    CURSOR_RADIUS,
    FRAME_HEIGHT,
    FRAME_WIDTH,
    MP_DETECTION_CONFIDENCE,
    MP_MAX_NUM_HANDS,
    MP_TRACKING_CONFIDENCE,
    PANEL_WIDTH,
    WINDOW_NAME,
)
from src.camera import Camera
from src.canvas import DrawingCanvas
from src.gesture import HoverSelector
from src.hand_tracker import HandTracker
from src.ui.panel import SidePanel
from src.ui.renderer import draw_cursor


def main() -> None:
    camera = Camera(width=FRAME_WIDTH, height=FRAME_HEIGHT)
    tracker = HandTracker(
        max_num_hands=MP_MAX_NUM_HANDS,
        min_detection_confidence=MP_DETECTION_CONFIDENCE,
        min_tracking_confidence=MP_TRACKING_CONFIDENCE,
    )
    canvas = DrawingCanvas(width=FRAME_WIDTH, height=FRAME_HEIGHT)
    panel = SidePanel(width=PANEL_WIDTH, frame_height=FRAME_HEIGHT, colors=COLORS)

    color_selector = HoverSelector(activation_seconds=COLOR_HOVER_SECONDS)
    clear_selector = HoverSelector(activation_seconds=CLEAR_HOVER_SECONDS)

    active_color_index = 0
    prev_draw_point: tuple[int, int] | None = None

    while True:
        frame = camera.read()
        if frame is None:
            break

        frame = cv2.flip(frame, 1)
        point = tracker.get_index_finger_tip(frame)

        # Cursor in panel area -> interaction mode, drawing is paused.
        if point is not None and point.x < PANEL_WIDTH:
            prev_draw_point = None
            hit = panel.hit_test(point.x, point.y)

            if hit and hit.startswith("color:"):
                clear_selector.reset()
                selected = color_selector.update(hit)
                if selected:
                    active_color_index = int(selected.split(":")[1])
            elif hit == "action:clear":
                color_selector.reset()
                selected = clear_selector.update(hit)
                if selected:
                    canvas.clear()
            else:
                color_selector.reset()
                clear_selector.reset()

        elif point is not None:
            color_selector.reset()
            clear_selector.reset()
            current_point = (point.x, point.y)
            if prev_draw_point is not None:
                canvas.draw_line(prev_draw_point, current_point, COLORS[active_color_index], BRUSH_SIZE)
            prev_draw_point = current_point
        else:
            prev_draw_point = None
            color_selector.reset()
            clear_selector.reset()

        output = canvas.blend_with(frame)
        panel.draw(output, active_color_id=f"color:{active_color_index}")

        cv2.putText(
            output,
            "Press Q or ESC to exit",
            (PANEL_WIDTH + 20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (240, 240, 240),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            output,
            "Use index finger as cursor",
            (PANEL_WIDTH + 20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (220, 220, 220),
            2,
            cv2.LINE_AA,
        )

        if point is not None:
            draw_cursor(output, (point.x, point.y), COLORS[active_color_index], CURSOR_RADIUS)

        cv2.imshow(WINDOW_NAME, output)
        key = cv2.waitKey(1) & 0xFF
        if key in (27, ord("q"), ord("Q")):
            break

    tracker.close()
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
