"""V23 episode recorder: converts verified interactions into compact learning data."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class EpisodeStep:
    state_key: str
    action: str
    reward: float
    verified: bool
    outcome: str

class EpisodeRecorder:
    def __init__(self, max_steps: int = 256) -> None:
        self.max_steps = max_steps
        self.steps: list[EpisodeStep] = []

    def add(self, state_key: str, action: str, reward: float, verified: bool, outcome: str) -> None:
        self.steps.append(EpisodeStep(state_key, action, max(-1.0, min(1.0, reward)), verified, outcome))
        if len(self.steps) > self.max_steps:
            self.steps = self.steps[-self.max_steps:]

    def verified_steps(self) -> list[EpisodeStep]:
        return [step for step in self.steps if step.verified]

    def summary(self) -> dict:
        verified = self.verified_steps()
        return {
            "steps": len(self.steps),
            "verified_steps": len(verified),
            "reward": round(sum(s.reward for s in verified), 4),
        }
