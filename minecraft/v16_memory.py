"""V16 confidence-aware memory retrieval with positive and negative lessons."""
from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class MemoryHit:
    goal: str
    situation: str
    lesson: str
    reward: float
    relevance: float

class AdaptiveMemory:
    def __init__(self, capacity: int = 500) -> None:
        self.capacity = capacity
        self.items: list[MemoryHit] = []

    def add(self, goal: str, situation: str, lesson: str, reward: float) -> None:
        self.items.append(MemoryHit(goal, situation, lesson, max(-1.0, min(1.0, reward)), 0.0))
        if len(self.items) > self.capacity:
            del self.items[:len(self.items) - self.capacity]

    def retrieve(self, goal: str, situation: str, limit: int = 6) -> list[MemoryHit]:
        query = self._terms(goal + " " + situation)
        ranked = []
        for item in self.items:
            terms = self._terms(item.goal + " " + item.situation + " " + item.lesson)
            overlap = len(query & terms)
            if overlap:
                score = overlap + item.reward * 0.35
                ranked.append(MemoryHit(item.goal, item.situation, item.lesson, item.reward, score))
        ranked.sort(key=lambda x: x.relevance, reverse=True)
        return ranked[:limit]

    @staticmethod
    def _terms(text: str) -> set[str]:
        return set(re.findall(r"[a-z0-9]+", text.lower()))
