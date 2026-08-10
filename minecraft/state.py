"""Short-term Minecraft state tracking for V7."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from time import monotonic

from .vision import VisualAnalysis


@dataclass(frozen=True)
class StateSnapshot:
    frame_id: int
    summary: str
    landmarks: tuple[str, ...]
    hazards: tuple[str, ...]
    confidence: float
    timestamp: float


class MinecraftStateTracker:
    """Keeps a small rolling state history and detects obvious stagnation."""

    def __init__(self, history_size: int = 12) -> None:
        self.history: deque[StateSnapshot] = deque(maxlen=history_size)

    def update(self, frame_id: int, analysis: VisualAnalysis) -> StateSnapshot:
        snap = StateSnapshot(
            frame_id=frame_id,
            summary=analysis.summary,
            landmarks=analysis.landmarks,
            hazards=analysis.hazards,
            confidence=analysis.confidence,
            timestamp=monotonic(),
        )
        self.history.append(snap)
        return snap

    def is_stuck(self, window: int = 5) -> bool:
        if len(self.history) < window:
            return False
        recent = list(self.history)[-window:]
        signatures = {(x.summary, x.landmarks, x.hazards) for x in recent}
        return len(signatures) == 1

    def recent(self, limit: int = 8) -> tuple[StateSnapshot, ...]:
        return tuple(self.history)[-limit:]
