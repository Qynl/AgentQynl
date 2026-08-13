"""V3.8 embodied co-op companion state machine."""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
import time

@dataclass
class CompanionMemory:
    recent_chat: deque[str] = field(default_factory=lambda: deque(maxlen=24))
    completed_tasks: deque[str] = field(default_factory=lambda: deque(maxlen=32))
    current_goal: str | None = None
    facts: dict = field(default_factory=dict)

class Companion:
    def __init__(self, planner, max_task_seconds: float = 180.0):
        self.planner=planner; self.memory=CompanionMemory(); self.max_task_seconds=max_task_seconds; self.started_at=0.0
    def hear(self, message: str) -> None:
        message=message.strip()
        if not message: return
        self.memory.recent_chat.append(message)
        goal=self.planner.interpret_chat(message, dict(self.memory.facts))
        if goal:
            self.memory.current_goal=goal; self.started_at=time.monotonic()
    def tick(self, world_state: dict) -> dict | None:
        if not self.memory.current_goal: return None
        if time.monotonic()-self.started_at > self.max_task_seconds:
            return {"type":"replan","reason":"task_timeout","goal":self.memory.current_goal}
        return self.planner.next_step(self.memory.current_goal, world_state, list(self.memory.recent_chat))
    def verify(self, result: dict) -> None:
        if result.get("success"):
            if self.memory.current_goal: self.memory.completed_tasks.append(self.memory.current_goal)
            self.memory.current_goal=None
        elif result.get("needs_replan"):
            self.memory.current_goal=result.get("goal",self.memory.current_goal)
