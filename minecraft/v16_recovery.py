"""V16 bounded recovery: diagnose stalls and choose a reversible recovery mode."""
from __future__ import annotations
from dataclasses import dataclass
from collections import deque

@dataclass(frozen=True)
class RecoveryDecision:
    mode: str
    reason: str
    cooldown_steps: int = 1

class RecoveryManager:
    MODES = ("reobserve", "look_around", "reposition", "change_action", "abort")

    def __init__(self, max_attempts: int = 3) -> None:
        self.max_attempts = max_attempts
        self.attempts = 0
        self.history: deque[str] = deque(maxlen=12)

    def diagnose(self, *, repeated_state: bool, repeated_action: bool,
                 low_confidence: bool, recent_failures: int) -> RecoveryDecision:
        if recent_failures >= self.max_attempts:
            return RecoveryDecision("abort", "recovery budget exhausted", 0)
        if low_confidence:
            return RecoveryDecision("reobserve", "perception confidence is low")
        if repeated_action:
            return RecoveryDecision("change_action", "same action pattern repeated")
        if repeated_state:
            return RecoveryDecision("look_around", "state has not changed")
        if recent_failures:
            return RecoveryDecision("reposition", "recent action failure")
        return RecoveryDecision("reobserve", "insufficient evidence")

    def record(self, decision: RecoveryDecision) -> None:
        self.attempts += 1
        self.history.append(decision.mode)

    def reset(self) -> None:
        self.attempts = 0
        self.history.clear()
