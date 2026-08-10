"""V13 temporal Minecraft perception: tracks entities, UI, motion and uncertainty."""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
from typing import Iterable

@dataclass(frozen=True)
class EntityObservation:
    label: str
    confidence: float = 0.0
    position_hint: str = ""

@dataclass(frozen=True)
class TemporalState:
    summary: str
    entities: tuple[EntityObservation, ...] = ()
    landmarks: tuple[str, ...] = ()
    hazards: tuple[str, ...] = ()
    ui: tuple[str, ...] = ()
    confidence: float = 0.0
    frame_index: int = 0

@dataclass(frozen=True)
class StateDelta:
    added_entities: tuple[str, ...]
    removed_entities: tuple[str, ...]
    changed_ui: bool
    changed_landmarks: bool
    changed_hazards: bool
    confidence_delta: float

class TemporalStateTracker:
    def __init__(self, max_states: int = 24) -> None:
        self.history: deque[TemporalState] = deque(maxlen=max_states)
        self.frame_index = 0

    def update(self, vision) -> tuple[TemporalState, StateDelta]:
        current = TemporalState(
            summary=str(vision.summary),
            entities=self._entities(vision),
            landmarks=tuple(vision.landmarks),
            hazards=tuple(vision.hazards),
            ui=tuple(getattr(vision, "visible_ui", ())),
            confidence=max(0.0, min(1.0, float(getattr(vision, "confidence", 0.0)))),
            frame_index=self.frame_index,
        )
        previous = self.history[-1] if self.history else current
        old = {e.label for e in previous.entities}
        new = {e.label for e in current.entities}
        delta = StateDelta(
            tuple(sorted(new - old)), tuple(sorted(old - new)),
            previous.ui != current.ui,
            previous.landmarks != current.landmarks,
            previous.hazards != current.hazards,
            current.confidence - previous.confidence,
        )
        self.history.append(current)
        self.frame_index += 1
        return current, delta

    @staticmethod
    def _entities(vision) -> tuple[EntityObservation, ...]:
        raw = getattr(vision, "entities", ())
        result: list[EntityObservation] = []
        for item in raw:
            if isinstance(item, str): result.append(EntityObservation(item, 0.5))
            elif isinstance(item, dict) and isinstance(item.get("label"), str):
                result.append(EntityObservation(item["label"], float(item.get("confidence", 0.0)), str(item.get("position", ""))))
        return tuple(result)

    def recent(self, n: int = 6) -> tuple[TemporalState, ...]:
        return tuple(list(self.history)[-n:])
