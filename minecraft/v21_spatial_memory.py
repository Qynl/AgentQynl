"""V21 spatial memory: bounded relative landmarks and revisitation evidence."""
from __future__ import annotations
from dataclasses import dataclass
from collections import deque

@dataclass(frozen=True)
class SpatialObservation:
    landmark: str
    relation: str
    confidence: float
    tick: int

class SpatialMemory:
    def __init__(self, capacity: int = 128) -> None:
        self.items: deque[SpatialObservation] = deque(maxlen=capacity)

    def observe(self, landmark: str, relation: str, confidence: float, tick: int) -> None:
        if not landmark:
            return
        self.items.append(SpatialObservation(landmark, relation, max(0.0, min(1.0, confidence)), tick))

    def context(self, limit: int = 16) -> list[SpatialObservation]:
        return list(self.items)[-limit:]

    def revisited(self, landmark: str) -> bool:
        return sum(x.landmark == landmark for x in self.items) >= 2
