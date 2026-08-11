"""V22 deterministic replanning triggers."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ReplanDecision:
    required: bool
    reason: str

class ReplanPolicy:
    def should_replan(self, *, goal_status: str, repeated_state: bool,
                      high_uncertainty: bool, action_rejected: bool,
                      recovery_exhausted: bool) -> ReplanDecision:
        if goal_status in {"complete", "failed"}:
            return ReplanDecision(False, "terminal goal state")
        if recovery_exhausted:
            return ReplanDecision(True, "recovery exhausted")
        if action_rejected:
            return ReplanDecision(True, "selected action rejected")
        if repeated_state:
            return ReplanDecision(True, "state repeated without progress")
        if high_uncertainty:
            return ReplanDecision(True, "uncertainty too high")
        return ReplanDecision(False, "current plan remains usable")
