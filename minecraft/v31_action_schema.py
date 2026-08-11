"""V31 strict Minecraft action schema."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class ActionKind(str, Enum):
    LOOK = "look"
    MOVE = "move"
    JUMP = "jump"
    ATTACK = "attack"
    USE = "use"
    INVENTORY = "inventory"
    WAIT = "wait"

@dataclass(frozen=True)
class MinecraftAction:
    kind: ActionKind
    duration_ms: int = 0
    yaw_delta: float = 0.0
    pitch_delta: float = 0.0

    def __post_init__(self) -> None:
        if not 0 <= self.duration_ms <= 2000:
            raise ValueError("duration_ms outside safe bound")
        if not -180 <= self.yaw_delta <= 180:
            raise ValueError("yaw_delta outside safe bound")
        if not -90 <= self.pitch_delta <= 90:
            raise ValueError("pitch_delta outside safe bound")
