"""V2.8 production boundary for real Minecraft screen/input integration."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Any
import time
from .v28_vision_schema import validate_vision_result

@dataclass(frozen=True)
class ScreenFrame:
    image: Any
    timestamp: float
    width: int
    height: int

class ScreenCapture(Protocol):
    def capture(self) -> ScreenFrame: ...

class MinecraftInput(Protocol):
    def key_down(self, key: str) -> None: ...
    def key_up(self, key: str) -> None: ...
    def mouse_move(self, dx: int, dy: int) -> None: ...
    def mouse_button(self, button: str, down: bool) -> None: ...
    def emergency_stop(self) -> None: ...

class VisionBackend(Protocol):
    def analyze(self, frame: ScreenFrame) -> dict[str, Any]: ...

@dataclass(frozen=True)
class WorldState:
    timestamp: float
    player: dict[str, Any]
    visible_blocks: tuple[dict[str, Any], ...]
    entities: tuple[dict[str, Any], ...]
    ui: dict[str, Any]
    confidence: float

class ProductionAdapter:
    def __init__(self, screen: ScreenCapture, input_backend: MinecraftInput, vision: VisionBackend) -> None:
        self.screen, self.input, self.vision = screen, input_backend, vision
        self._last_frame_at = 0.0

    def observe(self) -> WorldState:
        frame = self.screen.capture()
        if frame.timestamp < self._last_frame_at:
            raise RuntimeError("screen timestamps moved backwards")
        self._last_frame_at = frame.timestamp
        raw = validate_vision_result(self.vision.analyze(frame))
        return WorldState(frame.timestamp, dict(raw["player"]), tuple(raw["visible_blocks"]), tuple(raw["entities"]), dict(raw["ui"]), float(raw["confidence"]))

    def stop(self) -> None:
        for key in ("w", "a", "s", "d", "space", "shift", "ctrl"):
            self.input.key_up(key)

    def emergency_stop(self) -> None:
        self.stop()
        self.input.emergency_stop()

    def tap(self, key: str, duration_s: float = 0.05) -> None:
        if not key or duration_s < 0 or duration_s > 2.0:
            raise ValueError("invalid key or duration")
        self.input.key_down(key)
        try:
            time.sleep(duration_s)
        finally:
            self.input.key_up(key)
