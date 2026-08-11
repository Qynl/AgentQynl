"""V26 mission-control layer for long-running Minecraft autonomy.

Keeps high-level mission state separate from individual actions and provides
explicit pause/resume/abort semantics. It is intentionally policy-only: it
cannot execute OS commands or bypass the existing action safety chain.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from time import monotonic

class MissionStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"

@dataclass
class Mission:
    name: str
    objective: str
    max_runtime_s: float = 1800.0
    status: MissionStatus = MissionStatus.IDLE
    started_at: float | None = None
    progress: float = 0.0
    blockers: list[str] = field(default_factory=list)

    def start(self) -> None:
        if self.status not in {MissionStatus.IDLE, MissionStatus.PAUSED}:
            raise RuntimeError(f"cannot start mission in {self.status}")
        if self.started_at is None:
            self.started_at = monotonic()
        self.status = MissionStatus.RUNNING

    def pause(self, reason: str = "") -> None:
        if self.status == MissionStatus.RUNNING:
            self.status = MissionStatus.PAUSED
            if reason:
                self.blockers.append(reason)

    def abort(self, reason: str = "operator abort") -> None:
        self.status = MissionStatus.ABORTED
        if reason:
            self.blockers.append(reason)

    def update(self, progress: float) -> None:
        if self.status != MissionStatus.RUNNING:
            return
        self.progress = max(0.0, min(1.0, progress))
        if self.progress >= 1.0:
            self.status = MissionStatus.COMPLETED

    def expired(self) -> bool:
        return self.started_at is not None and monotonic() - self.started_at >= self.max_runtime_s

class MissionControl:
    def __init__(self) -> None:
        self.current: Mission | None = None

    def load(self, mission: Mission) -> None:
        if self.current and self.current.status == MissionStatus.RUNNING:
            raise RuntimeError("cannot replace a running mission")
        self.current = mission

    def tick(self) -> MissionStatus:
        if not self.current:
            return MissionStatus.IDLE
        if self.current.status == MissionStatus.RUNNING and self.current.expired():
            self.current.status = MissionStatus.FAILED
            self.current.blockers.append("mission timeout")
        return self.current.status
