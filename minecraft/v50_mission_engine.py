"""V50 mission engine: deterministic mission lifecycle with bounded progress."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class MissionStatus(str, Enum):
    PLANNED = "planned"
    RUNNING = "running"
    BLOCKED = "blocked"
    COMPLETE = "complete"
    FAILED = "failed"
    ABORTED = "aborted"

@dataclass
class Mission:
    id: str
    objective: str
    subtasks: list[str]
    status: MissionStatus = MissionStatus.PLANNED
    completed: set[str] = field(default_factory=set)

    def start(self) -> None:
        if self.status != MissionStatus.PLANNED:
            raise ValueError("mission cannot start from current state")
        self.status = MissionStatus.RUNNING

    def complete_subtask(self, subtask: str) -> None:
        if self.status != MissionStatus.RUNNING or subtask not in self.subtasks:
            raise ValueError("invalid subtask completion")
        self.completed.add(subtask)
        if len(self.completed) == len(self.subtasks):
            self.status = MissionStatus.COMPLETE

    @property
    def progress(self) -> float:
        return len(self.completed) / len(self.subtasks) if self.subtasks else 1.0
