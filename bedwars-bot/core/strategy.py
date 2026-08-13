"""Provider-neutral strategic decision layer for private training."""
from dataclasses import dataclass

@dataclass(frozen=True)
class GameState:
    health: float
    target_health: float
    target_visible: bool
    distance: float
    own_bed_alive: bool
    target_bed_alive: bool
    resources: dict
    in_void_danger: bool

ALLOWED_GOALS={"fight","retreat","defend","gather","attack_bed","explore","recover","idle"}

class Strategy:
    def choose_fallback(self, s: GameState) -> str:
        if s.in_void_danger: return "recover"
        if s.health <= 4 and s.target_health >= s.health: return "retreat"
        if s.target_visible and s.distance <= 8: return "fight"
        if not s.own_bed_alive: return "defend"
        if s.target_bed_alive: return "gather"
        return "explore"

    def validate_goal(self, goal: str) -> str:
        return goal if goal in ALLOWED_GOALS else "idle"
