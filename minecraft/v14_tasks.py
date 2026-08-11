"""V14 hierarchical Minecraft task decomposition."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Subtask:
    id: str
    description: str
    success_hint: str

@dataclass
class TaskPlan:
    goal: str
    subtasks: list[Subtask]
    current: int = 0

    @property
    def active(self) -> Subtask | None:
        return self.subtasks[self.current] if 0 <= self.current < len(self.subtasks) else None

    def advance(self) -> None:
        if self.current < len(self.subtasks):
            self.current += 1

    @property
    def complete(self) -> bool:
        return self.current >= len(self.subtasks)

class TaskDecomposer:
    """Conservative decomposition: the model proposes a short list, never code."""
    def __init__(self, model, max_subtasks: int = 8) -> None:
        self.model = model
        self.max_subtasks = max_subtasks

    def decompose(self, goal: str, state_summary: str) -> TaskPlan | None:
        prompt = (
            "Minecraft-only task decomposition. Break the goal into at most " + str(self.max_subtasks) +
            " observable subtasks. Each subtask must be achievable through normal Minecraft controls. "
            "Return JSON array only: [{id,description,success_hint}]. No code, no OS actions.\n" +
            "GOAL: " + goal + "\nSTATE: " + state_summary
        )
        raw = self.model.text(prompt)
        data = self.model.parse_json(raw)
        if not isinstance(data, list) or not data:
            return None
        subtasks = []
        for i, item in enumerate(data[: self.max_subtasks]):
            if not isinstance(item, dict):
                continue
            if not all(isinstance(item.get(k), str) for k in ("description", "success_hint")):
                continue
            subtasks.append(Subtask(str(item.get("id", i + 1)), item["description"], item["success_hint"]))
        return TaskPlan(goal, subtasks) if subtasks else None
