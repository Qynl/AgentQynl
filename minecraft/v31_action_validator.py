"""V31 action validation before an input adapter can execute anything."""
from __future__ import annotations
from dataclasses import dataclass
from .v31_action_schema import MinecraftAction
from .v31_state_estimator import StateEstimator

@dataclass(frozen=True)
class ValidationResult:
    allowed: bool
    reason: str

class ActionValidator:
    def __init__(self, min_confidence: float = 0.45) -> None:
        self.min_confidence = min_confidence

    def validate(self, action: MinecraftAction, *, state: StateEstimator, emergency_stop: bool = False) -> ValidationResult:
        if emergency_stop:
            return ValidationResult(False, "emergency stop")
        if not state.is_fresh():
            return ValidationResult(False, "state is stale")
        if state.state.confidence < self.min_confidence:
            return ValidationResult(False, "state confidence too low")
        return ValidationResult(True, "validated")
