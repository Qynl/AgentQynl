"""V50 temporal observation buffer for short-term perception context."""
from __future__ import annotations
from dataclasses import dataclass
from collections import deque
from time import monotonic
from typing import Any

@dataclass(frozen=True)
class Observation:
    frame_id: int
    state: dict[str, Any]
    confidence: float
    timestamp: float

class ObservationBuffer:
    def __init__(self, max_frames: int = 12) -> None:
        self.frames = deque(maxlen=max_frames)
        self.next_id = 0

    def add(self, state: dict[str, Any], confidence: float) -> Observation:
        item = Observation(self.next_id, dict(state), max(0.0, min(1.0, confidence)), monotonic())
        self.next_id += 1
        self.frames.append(item)
        return item

    def latest(self) -> Observation | None:
        return self.frames[-1] if self.frames else None

    def recent(self) -> list[Observation]:
        return list(self.frames)
