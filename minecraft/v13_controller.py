"""V13 closed-loop controller with temporal perception and adaptive planning."""
from __future__ import annotations
import time
from .v13_state import TemporalStateTracker
from .v13_planner import PlannerEvidence, build_v13_prompt

class V13Controller:
    def __init__(self, model, capture, executor, policy, escape, goal, max_steps: int = 1000):
        self.model = model
        self.capture = capture
        self.executor = executor
        self.policy = policy
        self.escape = escape
        self.goal = goal
        self.max_steps = max_steps
        self.steps = 0
        self.states = TemporalStateTracker()
        self.failures: list[str] = []

    def step(self) -> tuple[bool, str]:
        if self.steps >= self.max_steps:
            return False, "step budget exhausted"
        self.escape.checkpoint()
        frame = self.capture.capture()
        if not frame.screenshot_ref:
            return False, "capture unavailable"
        vision = self.model.vision(frame.screenshot_ref, "Return JSON only. Analyze Minecraft only. Include summary, entities, visible_ui, landmarks, hazards, confidence. Do not guess uncertain facts.")
        current, delta = self.states.update(vision)
        evidence = PlannerEvidence(current, delta, self.states.recent(6), tuple(self.failures[-6:]))
        raw = self.model._call([{"role":"system","content":"Minecraft-only planner. " + build_v13_prompt(self.goal.text, tuple(self.goal.success_conditions), evidence)}], 250)
        action = self.model.parse_action(raw)
        if action is None:
            self.failures.append("invalid action")
            return False, "invalid model action"
        decision = self.policy.validate(action)
        if not decision.allowed:
            self.failures.append("policy: " + decision.reason)
            return False, decision.reason
        self.escape.checkpoint()
        result = self.executor.execute(action)
        if not result.executed:
            self.failures.append(result.reason)
            return False, result.reason
        time.sleep(min(0.4, max(0.05, action.duration_ms / 1000.0)))
        self.steps += 1
        return True, "executed"
