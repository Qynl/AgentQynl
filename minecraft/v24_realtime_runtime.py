"""V24 real-time runtime coordinator.

Keeps perception, planning, execution and learning on separate bounded loops.
The runtime never grants learned data direct execution authority.
"""
from __future__ import annotations
from dataclasses import dataclass
from time import monotonic

@dataclass(frozen=True)
class RuntimeConfig:
    observe_hz: float = 5.0
    max_action_latency_s: float = 2.0
    max_consecutive_failures: int = 5
    dry_run: bool = True

class RealtimeRuntime:
    def __init__(self, config: RuntimeConfig) -> None:
        if config.observe_hz <= 0 or config.max_action_latency_s <= 0:
            raise ValueError("runtime limits must be positive")
        self.config = config
        self.failures = 0
        self.last_tick = monotonic()
        self.running = False

    @property
    def interval(self) -> float:
        return 1.0 / self.config.observe_hz

    def can_continue(self) -> bool:
        return self.running and self.failures < self.config.max_consecutive_failures

    def start(self) -> None:
        self.running = True
        self.last_tick = monotonic()

    def stop(self) -> None:
        self.running = False

    def record_result(self, success: bool) -> None:
        self.failures = 0 if success else self.failures + 1
        if self.failures >= self.config.max_consecutive_failures:
            self.stop()
