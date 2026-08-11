"""V15 shared blackboard: one bounded source of truth for the controller stack."""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
from typing import Any

@dataclass
class Blackboard:
    goal: str = ""
    active_subtask: str = ""
    success_hint: str = ""
    state: Any = None
    recent_delta: Any = None
    last_action: Any = None
    last_evaluation: Any = None
    mode: str = "normal"
    failures: deque[str] = field(default_factory=lambda: deque(maxlen=12))
    events: deque[str] = field(default_factory=lambda: deque(maxlen=40))

    def event(self, message: str) -> None:
        self.events.append(message)

    def fail(self, reason: str) -> None:
        self.failures.append(reason)
        self.event("failure: " + reason)

    def snapshot(self) -> dict[str, Any]:
        return {
            "goal": self.goal,
            "active_subtask": self.active_subtask,
            "success_hint": self.success_hint,
            "mode": self.mode,
            "failures": list(self.failures),
            "events": list(self.events),
        }
