"""V3.5 goal decomposition and progress tracking."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Goal:
    name: str
    target: dict
    progress: float = 0.0
    status: str = "pending"
    attempts: int = 0

class GoalManager:
    def __init__(self) -> None:
        self.goals: list[Goal] = []

    def set_goal(self, name: str, target: dict) -> Goal:
        goal = Goal(name, dict(target))
        self.goals = [goal]
        return goal

    def update(self, progress: float) -> Goal | None:
        if not self.goals: return None
        goal = self.goals[0]
        goal.progress = max(goal.progress, min(1.0, float(progress)))
        goal.status = "complete" if goal.progress >= 1.0 else "running"
        return goal

    def fail_attempt(self) -> None:
        if self.goals:
            self.goals[0].attempts += 1
