"""V2.7: practical Minecraft runtime primitives.

The platform-specific input adapter is intentionally injected so execution
remains isolated from planning and can be tested without controlling a real
Minecraft window.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
from .v26_pathfinding import AStarPathfinder, Node
from .v26_stuck_detector import StuckDetector

class InputAdapter(Protocol):
    def move(self, dx: int, dy: int, dz: int) -> None: ...
    def stop(self) -> None: ...
    def emergency_stop(self) -> None: ...

@dataclass(frozen=True)
class RuntimeObservation:
    position: Node
    goal: Node
    blocked: frozenset[Node] = frozenset()
    confidence: float = 1.0

@dataclass(frozen=True)
class RuntimeDecision:
    action: str
    target: Node | None
    reason: str

class MinecraftRuntime:
    def __init__(self, adapter: InputAdapter, max_expansions: int = 4096, stuck_limit: int = 8) -> None:
        self.adapter = adapter
        self.pathfinder = AStarPathfinder(max_expansions)
        self.stuck = StuckDetector(stuck_limit)
        self.paused = False

    def emergency_stop(self) -> None:
        self.paused = True
        self.adapter.emergency_stop()

    def resume(self) -> None:
        self.paused = False

    def decide(self, observation: RuntimeObservation) -> RuntimeDecision:
        if self.paused:
            return RuntimeDecision("stop", None, "runtime_paused")
        confidence = max(0.0, min(1.0, observation.confidence))
        if confidence < 0.35:
            return RuntimeDecision("reobserve", None, "low_observation_confidence")
        if observation.position == observation.goal:
            return RuntimeDecision("stop", observation.goal, "goal_reached")
        result = self.pathfinder.find(observation.position, observation.goal, set(observation.blocked))
        if not result.complete or len(result.path) < 2:
            return RuntimeDecision("replan", None, "no_verified_path")
        return RuntimeDecision("move_to", result.path[1], "verified_path_step")

    def execute(self, decision: RuntimeDecision, current: Node) -> None:
        if self.paused or decision.action != "move_to" or decision.target is None:
            self.adapter.stop()
            return
        target = decision.target
        self.adapter.move(target.x - current.x, target.y - current.y, target.z - current.z)

    def verify_movement(self, previous: Node, current: Node) -> bool:
        moved = current != previous
        if self.stuck.update(moved):
            self.adapter.stop()
            return False
        return moved
