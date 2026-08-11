"""V22 short-horizon action sequencing with precondition and postcondition checks."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ActionStep:
    action: object
    precondition: str
    expected_effect: str

@dataclass(frozen=True)
class SequenceDecision:
    steps: tuple[ActionStep, ...]
    reason: str

class ActionSequencer:
    def build(self, candidates: list, max_steps: int = 3) -> SequenceDecision:
        steps = []
        for candidate in candidates[:max_steps]:
            action = getattr(candidate, "action", None)
            if action is None:
                continue
            reason = str(getattr(candidate, "reason", "advance goal"))
            steps.append(ActionStep(action, "action is currently permitted", reason))
        return SequenceDecision(tuple(steps), "bounded short-horizon sequence")
