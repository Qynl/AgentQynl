"""V2.6: bounded A* pathfinding for Minecraft navigation planning."""
from __future__ import annotations
from dataclasses import dataclass
from heapq import heappop, heappush

@dataclass(frozen=True)
class Node:
    x: int
    y: int
    z: int

@dataclass(frozen=True)
class PathResult:
    path: tuple[Node, ...]
    complete: bool
    expanded: int

class AStarPathfinder:
    def __init__(self, max_expansions: int = 4096) -> None:
        if max_expansions < 1:
            raise ValueError("max_expansions must be positive")
        self.max_expansions = max_expansions

    @staticmethod
    def _h(a: Node, b: Node) -> int:
        return abs(a.x-b.x) + abs(a.y-b.y) + abs(a.z-b.z)

    def find(self, start: Node, goal: Node, blocked: set[Node] | None = None) -> PathResult:
        blocked = blocked or set()
        if start in blocked or goal in blocked:
            return PathResult((), False, 0)
        frontier: list[tuple[int, int, Node]] = [(self._h(start, goal), 0, start)]
        came_from: dict[Node, Node | None] = {start: None}
        cost: dict[Node, int] = {start: 0}
        counter, expanded = 0, 0
        while frontier and expanded < self.max_expansions:
            _, _, current = heappop(frontier)
            expanded += 1
            if current == goal:
                path: list[Node] = []
                node: Node | None = current
                while node is not None:
                    path.append(node)
                    node = came_from[node]
                path.reverse()
                return PathResult(tuple(path), True, expanded)
            for nxt in self._neighbors(current):
                if nxt in blocked:
                    continue
                new_cost = cost[current] + 1
                if new_cost < cost.get(nxt, 10**9):
                    cost[nxt] = new_cost
                    came_from[nxt] = current
                    counter += 1
                    heappush(frontier, (new_cost + self._h(nxt, goal), counter, nxt))
        return PathResult((), False, expanded)

    @staticmethod
    def _neighbors(node: Node) -> tuple[Node, ...]:
        x, y, z = node.x, node.y, node.z
        return (Node(x+1,y,z), Node(x-1,y,z), Node(x,y+1,z), Node(x,y-1,z), Node(x,y,z+1), Node(x,y,z-1))
