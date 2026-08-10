"""Capture boundary for Minecraft-only screen observations.

The capture layer returns opaque screenshot references. It does not expose
arbitrary desktop windows or filesystem paths to the model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .observation import MinecraftObservation


@dataclass(frozen=True)
class CaptureFrame:
    width: int
    height: int
    screenshot_ref: str | None
    game_focused: bool


class MinecraftCapture(Protocol):
    def capture(self) -> CaptureFrame:
        """Capture only the configured Minecraft surface."""


class DisabledCapture:
    """Safe default used until a real Minecraft capture adapter is configured."""

    def capture(self) -> CaptureFrame:
        return CaptureFrame(width=1, height=1, screenshot_ref=None, game_focused=False)


def observe(capture: MinecraftCapture, frame_id: int) -> MinecraftObservation:
    frame = capture.capture()
    return MinecraftObservation.create(
        frame_id,
        frame.width,
        frame.height,
        screenshot_ref=frame.screenshot_ref,
        game_focused=frame.game_focused,
    )
