"""V12 strategy layer: action cooldowns, exploration and failure avoidance."""
from __future__ import annotations
from dataclasses import dataclass
from collections import deque

@dataclass(frozen=True)
class StrategyDecision:
    mode: str
    instruction: str

class StrategyController:
    def __init__(self, repeat_limit: int = 2, history_size: int = 24) -> None:
        self.repeat_limit = repeat_limit
        self.actions: deque[str] = deque(maxlen=history_size)
        self.failures: deque[str] = deque(maxlen=history_size)

    def observe_action(self, action_type: str, success: bool, reason: str = "") -> None:
        self.actions.append(action_type)
        if not success:
            self.failures.append(reason or action_type)

    def decide(self, repeated_state_count: int, confidence: float) -> StrategyDecision:
        if confidence < 0.35:
            return StrategyDecision("cautious", "Re-observe before taking a risky action. Prefer a short, reversible action.")
        if repeated_state_count >= 4:
            return StrategyDecision("explore", "The state is repeating. Change camera or position with one small reversible action.")
        if len(self.actions) >= self.repeat_limit and len(set(list(self.actions)[-self.repeat_limit:])) == 1:
            return StrategyDecision("vary", "The same action has repeated. Choose a different useful Minecraft action.")
        return StrategyDecision("normal", "Continue toward the current Minecraft goal with one bounded action.")

    def failure_context(self) -> tuple[str, ...]:
        return tuple(self.failures)
