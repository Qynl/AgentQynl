"""V3.8 companion runtime orchestration.

Keeps perception, planning and Minecraft embodiment separate. The runtime can
operate through a future/installed companion bridge without taking over the
human player's input.
"""
from __future__ import annotations
from dataclasses import dataclass
import time

@dataclass
class RuntimeConfig:
    observation_interval_s: float = .25
    planner_interval_s: float = 1.0
    max_action_ms: int = 500
    require_state_after_action: bool = True

class CompanionRuntime:
    def __init__(self, vision, bridge, planner, safety, memory, config=None):
        self.vision=vision; self.bridge=bridge; self.planner=planner; self.safety=safety; self.memory=memory; self.config=config or RuntimeConfig()
        self.running=False; self.last_state=None; self.pending=None

    def on_chat(self, text: str):
        task=self.planner.parse_chat(text)
        self.memory.goal=task.goal
        self.memory.remember_event("chat", {"text":text})
        return task

    def tick(self, screenshot: bytes | None = None):
        if not self.running: return None
        state=self.bridge.get_state()
        if state is None: return None
        self.last_state=state
        decision=self.planner.next(self.memory.context(), state)
        if decision is None: return None
        if not self.safety.allow(decision, state):
            self.bridge.stop(); return None
        result=self.bridge.execute(decision)
        self.memory.remember_event("action", {"action":decision, "result":result})
        return result

    def stop(self):
        self.running=False
        self.bridge.stop()
