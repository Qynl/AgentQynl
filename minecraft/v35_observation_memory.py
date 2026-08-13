"""Short-term visual memory for Minecraft."""
from __future__ import annotations
from collections import deque

class ObservationMemory:
    def __init__(self, size: int = 16) -> None:
        self.frames = deque(maxlen=max(1, size))

    def add(self, state) -> None:
        self.frames.append(state)

    def latest(self):
        return self.frames[-1] if self.frames else None

    def changed(self, key: str) -> bool:
        if len(self.frames) < 2: return False
        return self.frames[-1].get(key) != self.frames[-2].get(key)
