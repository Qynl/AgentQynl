"""V22 hierarchical goal monitor with explicit progress, stall and completion states."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class GoalStatus(str, Enum):
    ACTIVE = "active"
    PROGRESS = "progress"
    STALLED = "stalled"
    COMPLETE = "complete"
    FAILED = "failed"

@dataclass(frozen=True)
class GoalSignal:
    status: GoalStatus
    progress: float
    confidence: float
    reason: str

class GoalMonitor:
    def evaluate(self, *, progress_delta: float, completion_evidence: float,
                 failure_count: int, confidence: float) -> GoalSignal:
        progress_delta = float(progress_delta)
        completion_evidence = max(0.0, min(1.0, float(completion_evidence)))
        confidence = max(0.0, min(1.0, float(confidence)))
        if completion_evidence >= 0.9 and confidence >= 0.55:
            return GoalSignal(GoalStatus.COMPLETE, 1.0, confidence, "strong completion evidence")
        if failure_count >= 5:
            return GoalSignal(GoalStatus.FAILED, 0.0, confidence, "failure budget reached")
        if progress_delta > 0.03:
            return GoalSignal(GoalStatus.PROGRESS, min(0.99, 0.5 + progress_delta), confidence, "observable progress")
        if progress_delta < -0.03 or failure_count >= 2:
            return GoalSignal(GoalStatus.STALLED, max(0.0, 0.5 + progress_delta), confidence, "progress stalled or regressed")
        return GoalSignal(GoalStatus.ACTIVE, max(0.0, min(0.99, 0.5 + progress_delta)), confidence, "goal remains active")
