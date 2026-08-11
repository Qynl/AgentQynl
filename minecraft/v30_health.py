"""V30 runtime health monitor."""
from __future__ import annotations
from dataclasses import dataclass
from time import monotonic

@dataclass(frozen=True)
class HealthSnapshot:
    loop_lag_ms: float
    consecutive_failures: int
    last_verification_age_s: float
    healthy: bool
    reason: str

class HealthMonitor:
    def __init__(self, max_lag_ms: float = 1500.0, max_failures: int = 4, max_verification_age_s: float = 8.0) -> None:
        self.max_lag_ms = max_lag_ms
        self.max_failures = max_failures
        self.max_verification_age_s = max_verification_age_s
        self.failures = 0
        self.last_verification = monotonic()

    def record_verification(self) -> None:
        self.last_verification = monotonic()
        self.failures = 0

    def record_failure(self) -> None:
        self.failures += 1

    def snapshot(self, loop_lag_ms: float) -> HealthSnapshot:
        age = monotonic() - self.last_verification
        reasons: list[str] = []
        if loop_lag_ms > self.max_lag_ms:
            reasons.append("loop lag")
        if self.failures >= self.max_failures:
            reasons.append("failure budget")
        if age > self.max_verification_age_s:
            reasons.append("verification stale")
        return HealthSnapshot(loop_lag_ms, self.failures, age, not reasons, ", ".join(reasons) or "healthy")
