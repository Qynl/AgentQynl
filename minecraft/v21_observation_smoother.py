"""V2.1: lightweight temporal smoothing for noisy Minecraft observations."""
from __future__ import annotations
from dataclasses import dataclass
from collections import deque
from typing import Any

@dataclass(frozen=True)
class SmoothedObservation:
    state: dict[str, Any]
    confidence: float
    samples: int

class ObservationSmoother:
    def __init__(self, window: int = 3) -> None:
        if window < 1:
            raise ValueError("window must be positive")
        self.window = window
        self._history: deque[tuple[dict[str, Any], float]] = deque(maxlen=window)

    def add(self, state: dict[str, Any], confidence: float) -> SmoothedObservation:
        self._history.append((dict(state), max(0.0, min(1.0, confidence))))
        latest = self._history[-1][0]
        confidence_avg = sum(c for _, c in self._history) / len(self._history)
        return SmoothedObservation(dict(latest), confidence_avg, len(self._history))
