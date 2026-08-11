"""V21 decision controller combining prediction, exploration and existing safety gates."""
from __future__ import annotations
from dataclasses import dataclass
from .v21_predictor import TransitionPredictor

@dataclass(frozen=True)
class Decision:
    action: object | None
    mode: str
    reason: str

class V21Controller:
    def __init__(self, predictor: TransitionPredictor | None = None) -> None:
        self.predictor = predictor or TransitionPredictor()

    def choose(self, candidates: list, *, confidence: float, repeated_state: bool, unknown_area: bool, danger: bool, failure_rate: float = 0.0) -> Decision:
        if danger:
            return Decision(None, "safe_stop", "hazard signal")
        if confidence < 0.45 or repeated_state or unknown_area:
            return Decision(None, "explore", "insufficient information for confident goal-directed action")
        predicted = self.predictor.predict(candidates, failure_rate=failure_rate)
        if not predicted:
            return Decision(None, "replan", "no viable predicted outcomes")
        best = predicted[0]
        return Decision(best.action, "goal", f"predicted progress={best.expected_progress:.2f}, risk={best.risk:.2f}")
