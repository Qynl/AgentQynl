"""V23 bounded skill learning from verified Minecraft episodes."""
from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=True)
class SkillExample:
    context_key: str
    action: str
    reward: float
    verified: bool

class SkillLearner:
    def __init__(self, max_examples: int = 512) -> None:
        self.max_examples = max_examples
        self.examples: list[SkillExample] = []
        self.scores = defaultdict(float)

    def record(self, context_key: str, action: str, reward: float, verified: bool) -> None:
        if not verified or not action:
            return
        self.examples.append(SkillExample(context_key, action, max(-1.0, min(1.0, reward)), verified))
        if len(self.examples) > self.max_examples:
            self.examples = self.examples[-self.max_examples:]
        self.scores[(context_key, action)] = self.scores[(context_key, action)] * 0.8 + reward * 0.2

    def rank(self, context_key: str, actions: list[str]) -> list[tuple[str, float]]:
        return sorted(((a, self.scores[(context_key, a)]) for a in actions), key=lambda x: x[1], reverse=True)
