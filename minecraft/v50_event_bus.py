"""V50 deterministic event bus for the Minecraft agent runtime."""
from __future__ import annotations
from dataclasses import dataclass
from collections import deque
from time import monotonic
from typing import Any, Callable

@dataclass(frozen=True)
class AgentEvent:
    kind: str
    payload: dict[str, Any]
    timestamp: float

class EventBus:
    def __init__(self, max_events: int = 512) -> None:
        if max_events < 1:
            raise ValueError("max_events must be positive")
        self.events = deque(maxlen=max_events)
        self.handlers: dict[str, list[Callable[[AgentEvent], None]]] = {}

    def subscribe(self, kind: str, handler: Callable[[AgentEvent], None]) -> None:
        self.handlers.setdefault(kind, []).append(handler)

    def publish(self, kind: str, payload: dict[str, Any] | None = None) -> AgentEvent:
        event = AgentEvent(kind, payload or {}, monotonic())
        self.events.append(event)
        for handler in tuple(self.handlers.get(kind, [])):
            handler(event)
        return event
