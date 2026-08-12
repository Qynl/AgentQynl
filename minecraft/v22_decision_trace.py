"""V2.2: compact, bounded decision traces for debugging agent choices."""
from __future__ import annotations
from dataclasses import dataclass
from collections import deque
from time import monotonic

@dataclass(frozen=True)
class DecisionTrace:
    action: str
    confidence: float
    reason: str
    timestamp: float

class DecisionTraceStore:
    def __init__(self, max_items: int = 256) -> None:
        if max_items < 1:
            raise ValueError("max_items must be positive")
        self.items = deque(maxlen=max_items)

    def record(self, action: str, confidence: float, reason: str) -> DecisionTrace:
        trace = DecisionTrace(action, max(0.0, min(1.0, confidence)), reason, monotonic())
        self.items.append(trace)
        return trace

    def recent(self, limit: int = 20) -> list[DecisionTrace]:
        return list(self.items)[-max(0, limit):]
