"""V2.5: bounded recovery policy for repeated Minecraft action failures."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class RecoveryDecision:
    mode: str
    reason: str

class RecoveryPolicy:
    def __init__(self, max_retries: int = 3) -> None:
        if max_retries < 1:
            raise ValueError("max_retries must be positive")
        self.max_retries = max_retries

    def choose(self, failures: int, progress_delta: float, confidence: float) -> RecoveryDecision:
        if failures >= self.max_retries:
            return RecoveryDecision("reobserve", "retry budget exhausted")
        if confidence < 0.45:
            return RecoveryDecision("reobserve", "confidence too low")
        if progress_delta < -0.05:
            return RecoveryDecision("replan", "mission progress regressed")
        if failures > 0:
            return RecoveryDecision("retry_once", "recoverable action failure")
        return RecoveryDecision("continue", "no recovery required")
