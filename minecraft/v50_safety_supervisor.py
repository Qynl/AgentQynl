"""V50 independent safety supervisor."""
from __future__ import annotations
from dataclasses import dataclass
from time import monotonic

@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    reason: str

class SafetySupervisor:
    def __init__(self, max_action_ms: int = 1000, max_failures: int = 5) -> None:
        self.max_action_ms = max_action_ms
        self.max_failures = max_failures
        self.failures = 0
        self.emergency_stop = False
        self.last_verified = monotonic()

    def verify(self, *, action_ms: int, confidence: float, state_fresh: bool) -> SafetyDecision:
        if self.emergency_stop:
            return SafetyDecision(False, "emergency stop")
        if action_ms < 0 or action_ms > self.max_action_ms:
            return SafetyDecision(False, "action duration limit")
        if not state_fresh:
            return SafetyDecision(False, "stale state")
        if confidence < 0.45:
            return SafetyDecision(False, "low confidence")
        return SafetyDecision(True, "approved")

    def record_result(self, verified: bool) -> None:
        if verified:
            self.failures = 0
            self.last_verified = monotonic()
        else:
            self.failures += 1
            if self.failures >= self.max_failures:
                self.emergency_stop = True

    def stop(self) -> None:
        self.emergency_stop = True
