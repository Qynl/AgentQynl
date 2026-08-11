"""V22 lightweight hierarchical subtask graph."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Subtask:
    id: str
    description: str
    parent: str | None = None
    status: str = "pending"
    progress: float = 0.0
    children: list[str] = field(default_factory=list)

class SubtaskGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, Subtask] = {}

    def add(self, node: Subtask) -> None:
        self.nodes[node.id] = node
        if node.parent and node.parent in self.nodes and node.id not in self.nodes[node.parent].children:
            self.nodes[node.parent].children.append(node.id)

    def next_pending(self) -> Subtask | None:
        for node in self.nodes.values():
            if node.status == "pending":
                return node
        return None

    def complete(self, node_id: str) -> None:
        if node_id in self.nodes:
            self.nodes[node_id].status = "complete"
            self.nodes[node_id].progress = 1.0
