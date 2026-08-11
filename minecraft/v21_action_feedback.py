"""V2.1: verified action feedback used by replanning and metrics."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class ActionOutcome(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class ActionFeedback:
    outcome: ActionOutcome
    progress_delta: float
    reason: str = ""

    def __post_init__(self) -> None:
        if not -1.0 <= self.progress_delta <= 1.0:
            raise ValueError("progress_delta must be between -1 and 1")

    @property
    def verified(self) -> bool:
        return self.outcome is not ActionOutcome.UNKNOWN
