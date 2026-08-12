"""Temporal world-state extraction helpers for screen-based Minecraft play."""
from __future__ import annotations
from dataclasses import dataclass
from .v28_production_adapter import WorldState

@dataclass(frozen=True)
class WorldDelta:
    position_changed: bool
    visible_block_count_delta: int
    entity_count_delta: int

class WorldStateTracker:
    def __init__(self) -> None:
        self.previous: WorldState | None = None

    def update(self, state: WorldState) -> WorldDelta:
        old = self.previous
        self.previous = state
        if old is None:
            return WorldDelta(False, len(state.visible_blocks), len(state.entities))
        old_pos = old.player.get("position")
        new_pos = state.player.get("position")
        return WorldDelta(
            old_pos != new_pos,
            len(state.visible_blocks) - len(old.visible_blocks),
            len(state.entities) - len(old.entities),
        )
