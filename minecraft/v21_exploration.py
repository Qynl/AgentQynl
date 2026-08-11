"""V21 exploration manager: chooses bounded information-gathering behavior."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ExplorationDecision:
    action: str
    reason: str
    information_gain: float

class ExplorationManager:
    def choose(self, *, confidence: float, repeated_state: bool, unknown_area: bool, danger: bool) -> ExplorationDecision:
        if danger:
            return ExplorationDecision("retreat_or_stop", "hazard detected", 0.1)
        if confidence < 0.45:
            return ExplorationDecision("reobserve", "low perception confidence", 0.8)
        if repeated_state:
            return ExplorationDecision("look_around", "repeated state; gather new visual evidence", 0.75)
        if unknown_area:
            return ExplorationDecision("small_scan", "area has insufficient evidence", 0.7)
        return ExplorationDecision("continue_goal", "sufficient current evidence", 0.2)
