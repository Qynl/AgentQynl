"""V23 conservative capability estimator from verified outcomes."""
from __future__ import annotations

class CapabilityEstimator:
    def __init__(self, initial: float = 0.25) -> None:
        self.value = max(0.0, min(1.0, initial))

    def update(self, reward: float, verified: bool, recovery_used: bool = False) -> float:
        if not verified:
            return self.value
        reward = max(-1.0, min(1.0, reward))
        delta = reward * 0.04
        if recovery_used:
            delta *= 0.5
        self.value = max(0.0, min(1.0, self.value + delta))
        return self.value
