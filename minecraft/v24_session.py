"""V24 real-session telemetry without credentials or raw screen retention."""
from __future__ import annotations
from dataclasses import dataclass
from time import time

@dataclass(frozen=True)
class SessionEvent:
    timestamp: float
    kind: str
    verified: bool
    reward: float

class SessionTelemetry:
    def __init__(self, max_events: int = 2048) -> None:
        self.max_events = max_events
        self.events: list[SessionEvent] = []

    def record(self, kind: str, *, verified: bool = False, reward: float = 0.0) -> None:
        reward = max(-1.0, min(1.0, float(reward)))
        self.events.append(SessionEvent(time(), kind, verified, reward))
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]

    def stats(self) -> dict[str, float | int]:
        verified = [e for e in self.events if e.verified]
        return {
            "events": len(self.events),
            "verified": len(verified),
            "verified_reward": round(sum(e.reward for e in verified), 4),
        }
