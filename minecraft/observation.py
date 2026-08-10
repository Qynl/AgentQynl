"""Minecraft-only observation contracts used by the V4 agent loop."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Mapping


@dataclass(frozen=True)
class MinecraftObservation:
    """A model-facing observation containing only Minecraft context."""

    frame_id: int
    captured_at: datetime
    width: int
    height: int
    screenshot_ref: str | None = None
    game_focused: bool = False
    inventory: Mapping[str, int] | None = None
    health: float | None = None
    food: float | None = None

    @classmethod
    def create(
        cls,
        frame_id: int,
        width: int,
        height: int,
        *,
        screenshot_ref: str | None = None,
        game_focused: bool = False,
        inventory: Mapping[str, int] | None = None,
        health: float | None = None,
        food: float | None = None,
    ) -> "MinecraftObservation":
        if frame_id < 0 or width <= 0 or height <= 0:
            raise ValueError("invalid Minecraft observation dimensions or frame id")
        return cls(
            frame_id=frame_id,
            captured_at=datetime.now(timezone.utc),
            width=width,
            height=height,
            screenshot_ref=screenshot_ref,
            game_focused=game_focused,
            inventory=dict(inventory) if inventory else None,
            health=health,
            food=food,
        )
