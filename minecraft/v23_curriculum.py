"""V23 curriculum manager for progressively harder Minecraft goals."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CurriculumTask:
    id: str
    description: str
    difficulty: float

class CurriculumManager:
    def __init__(self, tasks: list[CurriculumTask] | None = None) -> None:
        self.tasks = sorted(tasks or [], key=lambda t: t.difficulty)
        self.completed: set[str] = set()

    def next_task(self, capability: float) -> CurriculumTask | None:
        for task in self.tasks:
            if task.id not in self.completed and task.difficulty <= capability + 0.15:
                return task
        return None

    def mark_complete(self, task_id: str) -> None:
        self.completed.add(task_id)
