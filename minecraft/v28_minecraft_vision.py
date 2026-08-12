"""Minecraft-focused screen vision for V2.8.

Deterministic CV extracts only signals justified by pixels. Semantic 3D
coordinates remain unknown unless another backend supplies them.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class Detection:
    kind: str
    label: str
    confidence: float
    bbox: tuple[int, int, int, int]
    distance_hint: float | None = None

@dataclass(frozen=True)
class MinecraftFrameAnalysis:
    crosshair: dict[str, Any]
    hud: dict[str, Any]
    inventory: dict[str, Any]
    player: dict[str, Any]
    blocks: tuple[Detection, ...]
    entities: tuple[Detection, ...]
    scene_confidence: float

    def to_world_state_payload(self) -> dict[str, Any]:
        return {
            "confidence": self.scene_confidence,
            "player": self.player,
            "visible_blocks": [asdict(x) for x in self.blocks],
            "entities": [asdict(x) for x in self.entities],
            "ui": {"crosshair": self.crosshair, "hud": self.hud, "inventory": self.inventory},
        }

class MinecraftVision:
    """Cheap, deterministic Minecraft UI/scene geometry extractor."""
    def __init__(self, crosshair_ratio: float = 0.015) -> None:
        self.crosshair_ratio = crosshair_ratio

    def analyze(self, frame) -> dict[str, Any]:
        image = self._to_bgr(frame.image)
        h, w = image.shape[:2]
        result = MinecraftFrameAnalysis(
            crosshair=self._find_crosshair(image),
            hud=self._hud_regions(w, h),
            inventory=self._inventory_region(w, h),
            player={"position": None, "yaw": None, "pitch": None, "source": "screen_unknown"},
            blocks=(), entities=(), scene_confidence=0.35,
        )
        return result.to_world_state_payload()

    @staticmethod
    def _to_bgr(image):
        import cv2
        import numpy as np
        if image is None or not hasattr(image, "__array__"):
            raise TypeError("frame image must expose the NumPy array protocol")
        arr = np.asarray(image)
        if arr.ndim != 3 or arr.shape[2] not in (3, 4):
            raise ValueError("expected a 3- or 4-channel color image")
        return cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR) if arr.shape[2] == 4 else arr

    def _find_crosshair(self, image) -> dict[str, Any]:
        import cv2
        import numpy as np
        h, w = image.shape[:2]
        cx, cy = w // 2, h // 2
        r = max(3, int(min(w, h) * self.crosshair_ratio))
        crop = image[max(0, cy-r):cy+r+1, max(0, cx-r):cx+r+1]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        bright = float(np.mean(gray > 180))
        return {"x": cx, "y": cy, "visible_hint": bright > 0.015, "confidence": min(1.0, bright * 8.0)}

    @staticmethod
    def _hud_regions(w: int, h: int) -> dict[str, Any]:
        return {"hotbar_region": (int(w*.25), int(h*.86), int(w*.75), int(h*.99)), "health_region": (int(w*.25), int(h*.80), int(w*.50), int(h*.91)), "food_region": (int(w*.50), int(h*.80), int(w*.75), int(h*.91)), "confidence": 0.2}

    @staticmethod
    def _inventory_region(w: int, h: int) -> dict[str, Any]:
        return {"center_region": (int(w*.30), int(h*.15), int(w*.70), int(h*.85)), "open": None, "confidence": 0.0}
