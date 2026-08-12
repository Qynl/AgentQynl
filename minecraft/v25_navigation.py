"""V2.5: bounded navigation helpers for Minecraft waypoint following."""
from __future__ import annotations
from dataclasses import dataclass
from math import hypot

@dataclass(frozen=True)
class Waypoint:
    x: float
    y: float
    z: float
    name: str = "waypoint"

@dataclass(frozen=True)
class NavigationDecision:
    action: str
    distance: float
    reason: str

class Navigator:
    def __init__(self, arrival_radius: float = 1.5) -> None:
        if arrival_radius <= 0:
            raise ValueError("arrival_radius must be positive")
        self.arrival_radius = arrival_radius

    def choose(self, position: tuple[float, float, float], target: Waypoint) -> NavigationDecision:
        x, y, z = position
        distance = hypot(hypot(target.x - x, target.z - z), target.y - y)
        if distance <= self.arrival_radius:
            return NavigationDecision("arrived", distance, "within arrival radius")
        return NavigationDecision("move_to_waypoint", distance, f"target={target.name}")
