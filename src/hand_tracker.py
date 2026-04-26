"""MediaPipe hand tracking wrapper."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import mediapipe as mp


@dataclass
class HandPoint:
    x: int
    y: int


class HandTracker:
    def __init__(
        self,
        max_num_hands: int,
        min_detection_confidence: float,
        min_tracking_confidence: float,
    ) -> None:
        self._mp_hands = mp.solutions.hands
        self._hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def get_index_finger_tip(self, frame) -> HandPoint | None:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self._hands.process(rgb)
        if not results.multi_hand_landmarks:
            return None

        hand = results.multi_hand_landmarks[0]
        tip = hand.landmark[self._mp_hands.HandLandmark.INDEX_FINGER_TIP]
        h, w = frame.shape[:2]
        return HandPoint(x=int(tip.x * w), y=int(tip.y * h))

    def close(self) -> None:
        self._hands.close()
