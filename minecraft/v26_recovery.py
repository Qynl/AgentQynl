"""V26 deterministic recovery ladder for stalled Minecraft missions."""
from __future__ import annotations
from enum import Enum

class RecoveryStep(str, Enum):
    REOBSERVE = "reobserve"
    RELOCALIZE = "relocalize"
    REPLAN = "replan"
    BACKTRACK = "backtrack"
    PAUSE = "pause"
    ABORT = "abort"

class RecoveryManager:
    def __init__(self, max_attempts: int = 5) -> None:
        self.max_attempts = max_attempts
        self.attempts = 0

    def next_step(self, *, perception_uncertain: bool = False, stalled: bool = False) -> RecoveryStep:
        self.attempts += 1
        if self.attempts > self.max_attempts:
            return RecoveryStep.ABORT
        if perception_uncertain:
            return RecoveryStep.REOBSERVE
        if self.attempts == 2:
            return RecoveryStep.RELOCALIZE
        if stalled and self.attempts <= 3:
            return RecoveryStep.REPLAN
        if stalled:
            return RecoveryStep.BACKTRACK
        return RecoveryStep.PAUSE

    def reset(self) -> None:
        self.attempts = 0
