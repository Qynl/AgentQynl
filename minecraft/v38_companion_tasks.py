"""V3.8 companion task planner: natural language -> bounded goals."""
from __future__ import annotations
from dataclasses import dataclass, field
import re

@dataclass
class CompanionTask:
    goal: str
    steps: list[str]
    index: int = 0
    status: str = "queued"
    memory: dict = field(default_factory=dict)

    @property
    def current(self): return self.steps[self.index] if self.index < len(self.steps) else None
    @property
    def done(self): return self.index >= len(self.steps)

    def advance(self):
        self.index += 1
        self.status = "done" if self.done else "running"

PATTERNS=[
 (r"\b(follow|komm mit|folg mir)\b", ["locate player","follow player","maintain safe distance","verify following"]),
 (r"\b(stay|bleib)\b", ["choose safe position","stay near position","watch for threats"]),
 (r"\b(get|hol|sammle).*(wood|holz)\b", ["find wood","navigate to wood","gather wood","verify inventory"]),
 (r"\b(get|hol|find|suche).*(food|essen)\b", ["find food","navigate to food","collect food","verify food"]),
 (r"\b(mine|abbau).*(stone|stein)\b", ["find stone","navigate to stone","mine stone","verify inventory"]),
 (r"\b(come here|komm her)\b", ["locate player","navigate to player","stop nearby","report arrival"]),
 (r"\b(stop|stopp)\b", ["stop current task"]),
]

def parse_chat(text: str) -> CompanionTask:
    normalized=text.strip().lower()
    for pattern, steps in PATTERNS:
        if re.search(pattern, normalized):
            return CompanionTask(text.strip(), list(steps), status="running")
    return CompanionTask(text.strip(), ["understand request","inspect world state","plan safe action","execute short step","verify result","report progress"], status="running")
