"""Reference backends for V2.8 production integration."""
from __future__ import annotations
from .v28_production_adapter import ScreenFrame

class MSSScreenCapture:
    def __init__(self, monitor: dict | None = None) -> None:
        self.monitor = monitor

    def capture(self) -> ScreenFrame:
        import mss, time
        with mss.mss() as sct:
            monitor = self.monitor or sct.monitors[1]
            shot = sct.grab(monitor)
            return ScreenFrame(shot, time.monotonic(), shot.width, shot.height)

class PyAutoGUIInput:
    def __init__(self) -> None:
        import pyautogui
        self._pyautogui = pyautogui
        self._pressed: set[str] = set()
        self._pyautogui.PAUSE = 0.0
        self._pyautogui.FAILSAFE = True

    def key_down(self, key: str) -> None:
        self._pyautogui.keyDown(key)
        self._pressed.add(key)

    def key_up(self, key: str) -> None:
        self._pyautogui.keyUp(key)
        self._pressed.discard(key)

    def mouse_move(self, dx: int, dy: int) -> None:
        self._pyautogui.moveRel(dx, dy, duration=0)

    def mouse_button(self, button: str, down: bool) -> None:
        fn = self._pyautogui.mouseDown if down else self._pyautogui.mouseUp
        fn(button=button)

    def scroll(self, clicks: int) -> None:
        self._pyautogui.scroll(int(clicks))

    def emergency_stop(self) -> None:
        for key in tuple(self._pressed):
            try:
                self._pyautogui.keyUp(key)
            finally:
                self._pressed.discard(key)
