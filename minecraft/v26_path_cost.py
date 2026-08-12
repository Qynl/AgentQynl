"""V2.6: path cost scoring for planner selection."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class PathScore:
    length: int
    risk: float
    score: float

def score_path(length: int, risk: float = 0.0) -> PathScore:
    length = max(0, length)
    risk = max(0.0, min(1.0, risk))
    return PathScore(length, risk, length + risk * max(1, length))
