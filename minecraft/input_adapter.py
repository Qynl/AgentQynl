"""Restricted keyboard/mouse adapter for Minecraft only.

The adapter requires an explicit screen region and checks Force ESC before every
input. It deliberately exposes only Minecraft-oriented actions and never accepts
arbitrary key strings or shell commands from model output.
"""
from __future__ import annotations

import time
from typing import Any

from safety.action_policy import MinecraftAction
from safety.force_escape import ForceEscape


class PyAutoGuiMinecraftInput:
    """Send allowlisted input after an operator has configured Minecraft focus."""

    def __init__(self, escape: ForceEscape | None = None) -> None:
        self.escape = escape or ForceEscape()
        self._pyautogui: Any = None

    def _client(self) -> Any:
        if self._pyautogui is None:
            import pyautogui
            pyautogui.PAUSE = 0.03
            pyautogui.FAILSAFE = True
            self._pyautogui = pyautogui
        return self._pyautogui

    def send(self, action: MinecraftAction) -> None:
        self.escape.checkpoint()
        py = self._client()
        kind = action.kind
        if kind == "key_down":
            py.keyDown(action.key)
        elif kind == "key_up":
            py.keyUp(action.key)
        elif kind == "mouse_move":
            py.moveRel(action.dx, action.dy, duration=0)
        elif kind == "mouse_button":
            py.click(button=action.button)
        elif kind == "wait":
            time.sleep(action.duration)
        else:
            raise ValueError(f"unsupported Minecraft action: {kind}")
        self.escape.checkpoint()
