"""Optional real Minecraft capture adapter.

Uses MSS to capture a user-configured rectangle only. No desktop-wide capture
is exposed to the model. The adapter is opt-in and fails closed when disabled.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .capture import CaptureFrame


@dataclass(frozen=True)
class CaptureRegion:
    left: int
    top: int
    width: int
    height: int

    def validate(self) -> None:
        if self.left < 0 or self.top < 0 or self.width <= 0 or self.height <= 0:
            raise ValueError("invalid Minecraft capture region")


class MssMinecraftCapture:
    def __init__(self, region: CaptureRegion, output_dir: str | None = None) -> None:
        region.validate()
        self.region = region
        self.output_dir = Path(output_dir) if output_dir else None
        if self.output_dir:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        self._mss: Any = None

    def _client(self) -> Any:
        if self._mss is None:
            import mss
            self._mss = mss.mss()
        return self._mss

    def capture(self) -> CaptureFrame:
        shot = self._client().grab({
            "left": self.region.left,
            "top": self.region.top,
            "width": self.region.width,
            "height": self.region.height,
        })
        ref = None
        if self.output_dir:
            from mss.tools import to_png
            path = self.output_dir / "latest.png"
            to_png(shot.rgb, shot.size, output=str(path))
            ref = str(path)
        return CaptureFrame(
            width=self.region.width,
            height=self.region.height,
            screenshot_ref=ref,
            game_focused=True,
        )
