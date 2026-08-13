"""V3.5 bounded Minecraft action controller.

Converts high-level intents into short, verifiable input primitives. It does
not bypass the existing safety supervisor or directly accept arbitrary keys.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

Action = Literal["forward", "back", "left", "right", "jump", "sprint", "attack", "use", "hotbar_next", "hotbar_prev", "stop"]
ALLOWED = {"forward","back","left","right","jump","sprint","attack","use","hotbar_next","hotbar_prev","stop"}
KEYS = {"forward":"w","back":"s","left":"a","right":"d","jump":"space","sprint":"ctrl"}

@dataclass(frozen=True)
class ActionCommand:
    action: Action
    duration_ms: int = 80

class ActionController:
    def __init__(self, adapter, max_duration_ms: int = 750) -> None:
        self.adapter = adapter
        self.max_duration_ms = max_duration_ms

    def execute(self, command: ActionCommand) -> None:
        if command.action not in ALLOWED:
            raise ValueError("action is not allowed")
        duration = max(20, min(self.max_duration_ms, int(command.duration_ms)))
        if command.action == "stop":
            self.adapter.stop(); return
        if command.action in KEYS:
            self.adapter.tap(KEYS[command.action], duration / 1000.0)
            return
        if command.action == "attack":
            self.adapter.input.mouse_button("left", True)
            try: self.adapter.input.mouse_button("left", False)
            finally: self.adapter.stop()
            return
        if command.action == "use":
            self.adapter.input.mouse_button("right", True)
            try: self.adapter.input.mouse_button("right", False)
            finally: self.adapter.stop()
            return
        if command.action == "hotbar_next":
            self.adapter.input.mouse_move(120, 0); return
        if command.action == "hotbar_prev":
            self.adapter.input.mouse_move(-120, 0); return
