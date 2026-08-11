"""V50 bounded, typed memory layers."""
from __future__ import annotations
from dataclasses import dataclass
from collections import deque
from time import monotonic

@dataclass(frozen=True)
class MemoryItem:
    namespace: str
    key: str
    value: str
    confidence: float
    created_at: float

class MemoryStore:
    def __init__(self, max_items: int = 2048) -> None:
        self.items = deque(maxlen=max_items)

    def put(self, namespace: str, key: str, value: str, confidence: float) -> None:
        confidence = max(0.0, min(1.0, confidence))
        self.items.append(MemoryItem(namespace, key, value, confidence, monotonic()))

    def query(self, namespace: str, key: str) -> list[MemoryItem]:
        return [x for x in reversed(self.items) if x.namespace == namespace and x.key == key]

    def clear_namespace(self, namespace: str) -> None:
        self.items = deque((x for x in self.items if x.namespace != namespace), maxlen=self.items.maxlen)
