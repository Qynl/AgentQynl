"""V3.6 Minecraft action vocabulary and bounded controller.

The agent speaks in typed Minecraft actions rather than arbitrary OS keys.
Every action is validated and bounded before reaching the desktop adapter.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
import time

Action = Literal[
    "forward", "back", "left", "right", "jump", "sprint", "sneak",
    "attack", "use", "pick_block", "drop_item", "swap_hands",
    "inventory", "chat", "pause", "hotbar_1", "hotbar_2", "hotbar_3",
    "hotbar_4", "hotbar_5", "hotbar_6", "hotbar_7", "hotbar_8", "hotbar_9",
    "hotbar_next", "hotbar_prev", "look", "look_left", "look_right",
    "look_up", "look_down", "stop",
]

ALLOWED = {
    "forward", "back", "left", "right", "jump", "sprint", "sneak",
    "attack", "use", "pick_block", "drop_item", "swap_hands",
    "inventory", "chat", "pause",
    *(f"hotbar_{i}" for i in range(1, 10)),
    "hotbar_next", "hotbar_prev", "look", "look_left", "look_right",
    "look_up", "look_down", "stop",
}

KEYS = {
    "forward": "w", "back": "s", "left": "a", "right": "d",
    "jump": "space", "sprint": "ctrl", "sneak": "shift",
    "pick_block": "middle", "drop_item": "q", "swap_hands": "f",
    "inventory": "e", "chat": "t", "pause": "esc",
}

@dataclass(frozen=True)
class ActionCommand:
    action: Action
    duration_ms: int = 80
    dx: int = 0
    dy: int = 0

class ActionController:
    """Translate typed Minecraft actions into short adapter operations."""

    def __init__(self, adapter, max_duration_ms: int = 750, max_look_pixels: int = 500) -> None:
        self.adapter = adapter
        self.max_duration_ms = max(20, max_duration_ms)
        self.max_look_pixels = max(1, max_look_pixels)

    def _duration(self, value: int) -> float:
        return max(20, min(self.max_duration_ms, int(value))) / 1000.0

    def _tap(self, key: str, duration_s: float) -> None:
        self.adapter.input.key_down(key)
        try:
            time.sleep(duration_s)
        finally:
            self.adapter.input.key_up(key)

    def execute(self, command: ActionCommand) -> None:
        if command.action not in ALLOWED:
            raise ValueError(f"action is not allowed: {command.action}")

        action = command.action
        duration = self._duration(command.duration_ms)

        if action == "stop":
            self.adapter.stop()
            return

        if action in KEYS:
            key = KEYS[action]
            # Mouse buttons use their dedicated adapter operation.
            if key == "middle":
                self.adapter.input.mouse_button("middle", True)
                self.adapter.input.mouse_button("middle", False)
            else:
                self._tap(key, duration)
            return

        if action.startswith("hotbar_") and action[-1].isdigit():
            self._tap(action[-1], duration)
            return

        if action == "hotbar_next":
            self.adapter.input.mouse_move(0, 0)
            self.adapter.input.mouse_button("wheel_down", False)
            return

        if action == "hotbar_prev":
            self.adapter.input.mouse_move(0, 0)
            self.adapter.input.mouse_button("wheel_up", False)
            return

        if action == "attack":
            self.adapter.input.mouse_button("left", True)
            try:
                time.sleep(duration)
            finally:
                self.adapter.input.mouse_button("left", False)
            return

        if action == "use":
            self.adapter.input.mouse_button("right", True)
            try:
                time.sleep(duration)
            finally:
                self.adapter.input.mouse_button("right", False)
            return

        if action == "look":
            dx = max(-self.max_look_pixels, min(self.max_look_pixels, int(command.dx)))
            dy = max(-self.max_look_pixels, min(self.max_look_pixels, int(command.dy)))
            self.adapter.input.mouse_move(dx, dy)
            return

        if action in {"look_left", "look_right", "look_up", "look_down"}:
            amount = max(1, min(self.max_look_pixels, abs(int(command.dx or command.dy or 80))))
            dx = -amount if action == "look_left" else amount if action == "look_right" else 0
            dy = -amount if action == "look_up" else amount if action == "look_down" else 0
            self.adapter.input.mouse_move(dx, dy)
            return

        raise RuntimeError(f"unhandled action: {action}")
