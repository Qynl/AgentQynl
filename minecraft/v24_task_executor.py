"""V24 guarded task executor for real Minecraft sessions."""
from __future__ import annotations
from dataclasses import dataclass
from time import monotonic

@dataclass(frozen=True)
class ExecutionResult:
    executed: bool
    reason: str
    elapsed_s: float

class GuardedTaskExecutor:
    def __init__(self, dry_run: bool = True, timeout_s: float = 2.0) -> None:
        if timeout_s <= 0:
            raise ValueError("timeout_s must be positive")
        self.dry_run = dry_run
        self.timeout_s = timeout_s

    def execute(self, action, *, permitted: bool, emergency_stop: bool = False) -> ExecutionResult:
        started = monotonic()
        if emergency_stop:
            return ExecutionResult(False, "emergency stop", monotonic() - started)
        if not permitted:
            return ExecutionResult(False, "action rejected by policy", monotonic() - started)
        if self.dry_run:
            return ExecutionResult(False, "dry run", monotonic() - started)
        if action is None:
            return ExecutionResult(False, "empty action", monotonic() - started)
        # The actual input adapter is intentionally injected by the application.
        # This layer only authorizes a bounded action; it does not expose OS commands.
        return ExecutionResult(True, "authorized for injected Minecraft adapter", monotonic() - started)
