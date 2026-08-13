"""Bounded companion memory for co-op continuity."""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
import time

@dataclass
class CompanionMemory:
    max_events: int = 200
    events: deque = field(default_factory=lambda: deque(maxlen=200))
    facts: dict = field(default_factory=dict)
    goal: str | None = None

    def remember_event(self, kind: str, data: dict): self.events.append({"time":time.time(),"kind":kind,"data":data})
    def remember_fact(self, key: str, value): self.facts[key]=value
    def context(self) -> dict: return {"goal":self.goal,"facts":dict(self.facts),"recent_events":list(self.events)[-30:]}
    def clear_goal(self): self.goal=None
