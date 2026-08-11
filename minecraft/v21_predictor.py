"""V21 lightweight transition predictor for action selection."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class PredictedOutcome:
    action: object
    expected_progress: float
    uncertainty: float
    risk: float

class TransitionPredictor:
    def predict(self, candidates: list, *, observed_progress: float = 0.0, failure_rate: float = 0.0) -> list[PredictedOutcome]:
        results = []
        for candidate in candidates:
            utility = float(getattr(candidate, "utility", 0.0))
            uncertainty = min(1.0, 0.35 + failure_rate * 0.25)
            progress = max(0.0, min(1.0, utility * (1.0 - uncertainty * 0.5) + observed_progress * 0.15))
            risk = max(0.0, min(1.0, uncertainty * 0.6))
            results.append(PredictedOutcome(candidate.action, progress, uncertainty, risk))
        return sorted(results, key=lambda x: x.expected_progress - x.risk, reverse=True)
