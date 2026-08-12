"""V2.7: bounded session controller for observe-decide-execute-verify loops."""
from __future__ import annotations
from dataclasses import dataclass
from .v27_runtime import MinecraftRuntime, RuntimeObservation

@dataclass(frozen=True)
class SessionResult:
    steps: int
    completed: bool
    stopped: bool
    reason: str

class MinecraftSession:
    def __init__(self, runtime: MinecraftRuntime, max_steps: int = 256) -> None:
        if max_steps < 1:
            raise ValueError("max_steps must be positive")
        self.runtime = runtime
        self.max_steps = max_steps

    def run(self, observe) -> SessionResult:
        for step in range(1, self.max_steps + 1):
            observation: RuntimeObservation = observe()
            decision = self.runtime.decide(observation)
            if decision.action == "stop" and observation.position == observation.goal:
                return SessionResult(step, True, False, "goal_reached")
            if decision.action in {"stop", "reobserve", "replan"}:
                if decision.action == "stop":
                    return SessionResult(step, False, True, decision.reason)
                continue
            self.runtime.execute(decision, observation.position)
            updated = observe()
            self.runtime.verify_movement(observation.position, updated.position)
            if self.runtime.stuck.no_progress >= self.runtime.stuck.max_no_progress:
                return SessionResult(step, False, True, "navigation_stalled")
        return SessionResult(self.max_steps, False, True, "step_budget_exhausted")
