"""V2.6: converts a planned path into bounded navigation steps."""
from __future__ import annotations
from dataclasses import dataclass
from .v26_pathfinding import Node

@dataclass(frozen=True)
class NavigationStep:
    action: str
    target: Node

class PathNavigator:
    def next_step(self, path: tuple[Node, ...]) -> NavigationStep | None:
        if len(path) < 2:
            return None
        return NavigationStep("move_to", path[1])
