"""V16 action rate limiting and cooldowns."""
from __future__ import annotations
import time

class ActionRateLimiter:
    def __init__(self, min_interval_ms: int = 60) -> None:
        self.min_interval = max(0, min_interval_ms) / 1000.0
        self.last = 0.0

    def allow(self) -> bool:
        now = time.monotonic()
        if now - self.last < self.min_interval:
            return False
        self.last = now
        return True

    def reset(self) -> None:
        self.last = 0.0
