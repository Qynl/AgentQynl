"""Deterministic BedWars training combat state machine.

Simulator/private-training oriented. No network, mouse automation, or
anti-cheat interaction lives here.
"""
from dataclasses import dataclass
from enum import Enum

class CombatMode(Enum):
    IDLE="idle"; APPROACH="approach"; STRAFE="strafe"; ATTACK="attack"; RECOVER="recover"; DISENGAGE="disengage"

@dataclass(frozen=True)
class CombatObservation:
    target_visible: bool
    distance: float
    target_health: float
    self_health: float
    on_ground: bool
    void_risk: bool
    recently_hit: bool
    target_moving: bool

@dataclass(frozen=True)
class CombatIntent:
    mode: CombatMode
    move_x: float=0.0
    move_z: float=0.0
    attack: bool=False
    sprint: bool=False
    reason: str=""

class CombatController:
    def __init__(self, attack_range=3.1, retreat_health=4.0):
        self.mode=CombatMode.IDLE; self.combo=0; self.attack_range=attack_range; self.retreat_health=retreat_health

    def reset(self):
        self.mode=CombatMode.IDLE; self.combo=0

    def decide(self, o: CombatObservation) -> CombatIntent:
        if o.void_risk:
            self.mode=CombatMode.DISENGAGE; return CombatIntent(self.mode, move_z=-1, reason="void-risk")
        if not o.target_visible:
            self.mode=CombatMode.IDLE; self.combo=0; return CombatIntent(self.mode, reason="no-target")
        if o.self_health <= self.retreat_health and o.target_health > o.self_health:
            self.mode=CombatMode.DISENGAGE; return CombatIntent(self.mode, move_x=-1, sprint=True, reason="low-health")
        if not o.on_ground:
            self.mode=CombatMode.RECOVER; return CombatIntent(self.mode, move_z=-1, sprint=True, reason="airborne")
        if o.distance > self.attack_range:
            self.mode=CombatMode.APPROACH; return CombatIntent(self.mode, move_z=1, sprint=True, reason="close-distance")
        self.mode=CombatMode.STRAFE if o.target_moving else CombatMode.ATTACK
        side=-1.0 if self.combo % 2 else 1.0
        if o.recently_hit: self.combo += 1
        return CombatIntent(self.mode, move_x=side, attack=True, sprint=True, reason="pressure")
