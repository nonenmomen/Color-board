"""Simple gesture helpers for hover actions."""

from __future__ import annotations

import time


class HoverSelector:
    def __init__(self, activation_seconds: float) -> None:
        self._activation_seconds = activation_seconds
        self._current_target: str | None = None
        self._start_ts: float | None = None

    def reset(self) -> None:
        self._current_target = None
        self._start_ts = None

    def update(self, target_id: str | None) -> str | None:
        if target_id is None:
            self.reset()
            return None

        now = time.monotonic()
        if target_id != self._current_target:
            self._current_target = target_id
            self._start_ts = now
            return None

        if self._start_ts is None:
            self._start_ts = now
            return None

        if now - self._start_ts >= self._activation_seconds:
            self._start_ts = now
            return target_id
        return None
