"""V31 lightweight state confidence and freshness estimator."""
from __future__ import annotations
from dataclasses import dataclass
from time import monotonic

@dataclass
class StateEstimate:
    confidence: float = 0.0
    observed_at: float = 0.0

class StateEstimator:
    def __init__(self, stale_after_s: float = 1.5) -> None:
        if stale_after_s <= 0:
            raise ValueError("stale_after_s must be positive")
        self.stale_after_s = stale_after_s
        self.state = StateEstimate()

    def update(self, confidence: float) -> StateEstimate:
        self.state = StateEstimate(max(0.0, min(1.0, confidence)), monotonic())
        return self.state

    def is_fresh(self) -> bool:
        return self.state.observed_at > 0 and monotonic() - self.state.observed_at <= self.stale_after_s
