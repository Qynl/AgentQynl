"""V30 typed contracts shared by perception, planning, execution and evaluation."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from time import time

class ConfidenceBand(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass(frozen=True)
class Observation:
    tick: int
    timestamp: float
    scene_key: str
    confidence: float
    inventory: tuple[str, ...] = ()
    nearby: tuple[str, ...] = ()
    position: tuple[int, int, int] | None = None

    @property
    def band(self) -> ConfidenceBand:
        if self.confidence < 0.4:
            return ConfidenceBand.LOW
        if self.confidence < 0.75:
            return ConfidenceBand.MEDIUM
        return ConfidenceBand.HIGH

@dataclass(frozen=True)
class CandidateAction:
    name: str
    args: tuple[str, ...] = ()
    risk: float = 0.0
    expected_progress: float = 0.0

@dataclass(frozen=True)
class Decision:
    action: CandidateAction | None
    reason: str
    confidence: float
    created_at: float = field(default_factory=time)

@dataclass(frozen=True)
class Verification:
    success: bool
    progress: float
    confidence: float
    reason: str
