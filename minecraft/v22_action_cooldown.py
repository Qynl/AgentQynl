"""V2.2: bounded action pacing to reduce runaway input loops."""
from __future__ import annotations
from time import monotonic

class ActionCooldown:
    def __init__(self, minimum_interval_s: float = 0.05) -> None:
        if minimum_interval_s < 0:
            raise ValueError("minimum_interval_s cannot be negative")
        self.minimum_interval_s = minimum_interval_s
        self._last = 0.0

    def ready(self, now: float | None = None) -> bool:
        current = monotonic() if now is None else now
        return current - self._last >= self.minimum_interval_s

    def mark(self, now: float | None = None) -> None:
        self._last = monotonic() if now is None else now
