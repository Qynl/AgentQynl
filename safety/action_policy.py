"""Minecraft-only, deny-by-default action policy."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

ActionType = Literal["key", "mouse_move", "mouse_button", "wait"]
ALLOWED_KEYS = frozenset({"w","a","s","d","space","shift","ctrl","e","q","f","esc","1","2","3","4","5","6","7","8","9"})

@dataclass(frozen=True)
class MinecraftAction:
    type: ActionType
    key: str | None = None
    x: int | None = None
    y: int | None = None
    button: Literal["left", "right"] | None = None
    duration_ms: int = 0

    @property
    def kind(self) -> str:
        return self.type

    @property
    def dx(self) -> int:
        return self.x or 0

    @property
    def dy(self) -> int:
        return self.y or 0

    @property
    def duration(self) -> float:
        return self.duration_ms / 1000.0

@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str

class ActionPolicy:
    def __init__(self, max_key_hold_ms: int = 1500, max_wait_ms: int = 2000, max_mouse_delta: int = 350) -> None:
        self.max_key_hold_ms = max_key_hold_ms
        self.max_wait_ms = max_wait_ms
        self.max_mouse_delta = max_mouse_delta

    def validate(self, action: MinecraftAction) -> PolicyDecision:
        if action.type == "key":
            if action.key not in ALLOWED_KEYS: return PolicyDecision(False, "key is not allowlisted")
            if not 0 <= action.duration_ms <= self.max_key_hold_ms: return PolicyDecision(False, "key duration exceeds policy")
            return PolicyDecision(True, "allowed Minecraft key action")
        if action.type == "mouse_move":
            if action.x is None or action.y is None: return PolicyDecision(False, "mouse coordinates are required")
            if abs(action.x) > self.max_mouse_delta or abs(action.y) > self.max_mouse_delta: return PolicyDecision(False, "mouse movement exceeds policy")
            return PolicyDecision(True, "allowed bounded mouse movement")
        if action.type == "mouse_button":
            if action.button not in {"left", "right"}: return PolicyDecision(False, "mouse button is not allowlisted")
            if not 0 <= action.duration_ms <= self.max_key_hold_ms: return PolicyDecision(False, "mouse duration exceeds policy")
            return PolicyDecision(True, "allowed Minecraft mouse action")
        if action.type == "wait":
            if not 0 <= action.duration_ms <= self.max_wait_ms: return PolicyDecision(False, "wait duration exceeds policy")
            return PolicyDecision(True, "allowed wait")
        return PolicyDecision(False, "unknown action type")
