"""V14 episodic skill memory with bounded retrieval."""
from __future__ import annotations
from dataclasses import dataclass
from collections import deque
import re

@dataclass(frozen=True)
class SkillEpisode:
    goal: str
    situation: str
    action_type: str
    outcome: str
    reward: float
    lesson: str = ""

class SkillMemory:
    def __init__(self, capacity: int = 500) -> None:
        self.items: deque[SkillEpisode] = deque(maxlen=capacity)

    def add(self, episode: SkillEpisode) -> None:
        self.items.append(episode)

    def retrieve(self, goal: str, situation: str, limit: int = 6) -> list[SkillEpisode]:
        terms = set(re.findall(r"[a-z0-9]+", (goal + " " + situation).lower()))
        scored = []
        for item in self.items:
            item_terms = set(re.findall(r"[a-z0-9]+", (item.goal + " " + item.situation + " " + item.lesson).lower()))
            overlap = len(terms & item_terms)
            score = overlap + max(0.0, item.reward) * 0.5
            if overlap:
                scored.append((score, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:limit]]

    def successful(self, goal: str, limit: int = 5) -> list[SkillEpisode]:
        return [x for x in reversed(self.items) if x.reward > 0 and goal.lower() in x.goal.lower()][:limit]
