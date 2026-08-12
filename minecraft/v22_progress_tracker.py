"""V2.2: bounded mission progress tracking with regression detection."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ProgressSnapshot:
    progress: float
    delta: float
    regressed: bool

class ProgressTracker:
    def __init__(self) -> None:
        self.previous = 0.0

    def update(self, progress: float) -> ProgressSnapshot:
        progress = max(0.0, min(1.0, progress))
        delta = progress - self.previous
        result = ProgressSnapshot(progress, delta, delta < -0.05)
        self.previous = progress
        return result
