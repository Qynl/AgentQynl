"""V20 high-level closed loop. It orchestrates existing safety layers; it does not bypass them."""
from __future__ import annotations
from dataclasses import dataclass
import time
from .v20_world_model import WorldModel
from .v20_planner import UtilityPlanner

@dataclass(frozen=True)
class LoopResult:
    status: str
    reason: str

class V20Loop:
    def __init__(self, vision, planner_model, capture, executor, policy, watchdog, rate_limiter, escape, memory, recovery):
        self.vision = vision
        self.planner = UtilityPlanner(planner_model)
        self.capture = capture
        self.executor = executor
        self.policy = policy
        self.watchdog = watchdog
        self.rate_limiter = rate_limiter
        self.escape = escape
        self.memory = memory
        self.recovery = recovery
        self.world = WorldModel()

    def run_once(self, goal: str, recovery_mode: str = "normal") -> LoopResult:
        started = time.monotonic()
        self.escape.checkpoint()
        frame = self.capture.capture()
        if not getattr(frame, "screenshot_ref", None):
            return LoopResult("blocked", "capture unavailable")
        state = self.vision.observe(frame.screenshot_ref)
        self.world.update(state)
        memories = self.memory.retrieve(goal, str(self.world.context()))
        ranked = self.planner.rank(goal, self.world.context(), memories, recovery_mode)
        if not ranked:
            return LoopResult("blocked", "planner produced no valid candidates")
        for candidate in ranked:
            action = self.planner.model.parse_action(candidate.action) if isinstance(candidate.action, str) else candidate.action
            if action is None:
                continue
            if not self.rate_limiter.allow():
                return LoopResult("blocked", "rate limit")
            if not self.watchdog.step_budget_ok(started).allowed:
                return LoopResult("blocked", "step time budget")
            duration = int(getattr(action, "duration_ms", 0))
            if not self.watchdog.check_action(duration).allowed:
                continue
            decision = self.policy.validate(action)
            if not decision.allowed:
                continue
            self.escape.checkpoint()
            result = self.executor.execute(action)
            if not result.executed:
                self.watchdog.record(False)
                continue
            self.watchdog.record(True)
            return LoopResult("executed", candidate.reason)
        return LoopResult("blocked", "all candidates rejected")
