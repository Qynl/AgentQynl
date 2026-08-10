"""Goal and planning contracts for Minecraft-only V6."""
from __future__ import annotations

from dataclasses import dataclass, field

from .vision import VisualAnalysis


@dataclass(frozen=True)
class MinecraftGoal:
    text: str
    success_conditions: tuple[str, ...] = ()
    max_steps: int = 100


@dataclass(frozen=True)
class PlanningContext:
    goal: MinecraftGoal
    vision: VisualAnalysis
    recent_actions: tuple[str, ...] = ()
    step: int = 0


class GoalManager:
    """Small deterministic goal state machine; model planning stays separate."""

    def __init__(self) -> None:
        self._goal: MinecraftGoal | None = None
        self._step = 0

    def set_goal(self, goal: MinecraftGoal) -> None:
        self._goal = goal
        self._step = 0

    @property
    def goal(self) -> MinecraftGoal | None:
        return self._goal

    def context(self, vision: VisualAnalysis, recent_actions: tuple[str, ...] = ()) -> PlanningContext | None:
        if self._goal is None:
            return None
        return PlanningContext(self._goal, vision, recent_actions, self._step)

    def advance(self) -> None:
        self._step += 1
