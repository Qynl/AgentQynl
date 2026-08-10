"""Restricted real input adapter for Minecraft."""
from __future__ import annotations
import time
from typing import Any
from safety.action_policy import MinecraftAction
from safety.force_escape import ForceEscape

class PyAutoGuiMinecraftInput:
    def __init__(self, escape: ForceEscape | None = None) -> None:
        self.escape = escape or ForceEscape()
        self._pyautogui: Any = None
    def _client(self) -> Any:
        if self._pyautogui is None:
            import pyautogui
            pyautogui.PAUSE = 0.02
            pyautogui.FAILSAFE = True
            self._pyautogui = pyautogui
        return self._pyautogui
    def send(self, action: MinecraftAction) -> None:
        self.escape.checkpoint()
        py = self._client()
        if action.type == "key":
            if action.key == "esc":
                py.press("esc")
            elif action.duration_ms == 0:
                py.press(action.key)
            else:
                py.keyDown(action.key)
                try: time.sleep(action.duration)
                finally: py.keyUp(action.key)
        elif action.type == "mouse_move":
            py.moveRel(action.x or 0, action.y or 0, duration=0)
        elif action.type == "mouse_button":
            py.click(button=action.button)
        elif action.type == "wait":
            time.sleep(action.duration)
        else:
            raise ValueError("unsupported Minecraft action")
        self.escape.checkpoint()
