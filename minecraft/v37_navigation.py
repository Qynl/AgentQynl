"""V3.7 navigation controller with camera-aware recovery."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class NavCommand:
    action: str
    duration_ms: int

class NavigationController:
    def __init__(self, max_step_ms: int=350): self.max_step_ms=max_step_ms
    def choose(self, target, player):
        dx=target.get("screen_x",0)-player.get("screen_x",0)
        dy=target.get("screen_y",0)-player.get("screen_y",0)
        if abs(dx)>35: return NavCommand("look_right" if dx>0 else "look_left", min(160, abs(int(dx))*2))
        if abs(dy)>25: return NavCommand("look_down" if dy>0 else "look_up", min(120, abs(int(dy))*2))
        return NavCommand("forward", min(self.max_step_ms, 140))
