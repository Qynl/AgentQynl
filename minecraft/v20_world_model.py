"""V20 compact Minecraft world model built from temporal observations."""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque

@dataclass(frozen=True)
class WorldObject:
    label: str
    confidence: float
    position: str = ""
    last_seen: int = 0

@dataclass
class WorldModel:
    tick: int = 0
    objects: dict[str, WorldObject] = field(default_factory=dict)
    landmarks: set[str] = field(default_factory=set)
    hazards: set[str] = field(default_factory=set)
    ui: set[str] = field(default_factory=set)
    events: deque[str] = field(default_factory=lambda: deque(maxlen=32))

    def update(self, state) -> None:
        self.tick += 1
        seen = set()
        for entity in getattr(state, "entities", ()):
            label = str(getattr(entity, "label", entity))
            seen.add(label)
            self.objects[label] = WorldObject(label, float(getattr(entity, "confidence", 0.0)), str(getattr(entity, "position_hint", "")), self.tick)
        self.landmarks = set(getattr(state, "landmarks", ()))
        self.hazards = set(getattr(state, "hazards", ()))
        self.ui = set(getattr(state, "ui", ()))
        for label in seen:
            self.events.append(f"seen:{label}")

    def context(self, limit: int = 12) -> dict:
        objects = sorted(self.objects.values(), key=lambda x: x.last_seen, reverse=True)[:limit]
        return {
            "tick": self.tick,
            "objects": [o.__dict__ for o in objects],
            "landmarks": sorted(self.landmarks),
            "hazards": sorted(self.hazards),
            "ui": sorted(self.ui),
            "events": list(self.events),
        }
