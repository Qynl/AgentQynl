"""V15 runtime watchdog: bounds latency, repeated failures and action duration."""
from __future__ import annotations
from dataclasses import dataclass
import time

@dataclass(frozen=True)
class WatchdogDecision:
    allowed: bool
    reason: str = ""

class RuntimeWatchdog:
    def __init__(self, max_failures: int = 5, max_action_ms: int = 1500, max_step_seconds: float = 8.0) -> None:
        self.max_failures = max_failures
        self.max_action_ms = max_action_ms
        self.max_step_seconds = max_step_seconds
        self.failures = 0

    def check_action(self, duration_ms: int) -> WatchdogDecision:
        if duration_ms < 0 or duration_ms > self.max_action_ms:
            return WatchdogDecision(False, "action duration outside watchdog limit")
        if self.failures >= self.max_failures:
            return WatchdogDecision(False, "failure budget exhausted")
        return WatchdogDecision(True)

    def record(self, success: bool) -> None:
        self.failures = 0 if success else self.failures + 1

    def step_budget_ok(self, started: float) -> WatchdogDecision:
        if time.monotonic() - started > self.max_step_seconds:
            return WatchdogDecision(False, "step time budget exhausted")
        return WatchdogDecision(True)
