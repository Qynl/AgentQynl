"""V26 structured mission memory with bounded, verified summaries."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class MissionResult:
    mission: str
    outcome: str
    verified: bool
    reward: float
    lesson: str

class MissionMemory:
    def __init__(self, max_results: int = 256) -> None:
        self.max_results = max_results
        self.results: list[MissionResult] = []

    def record(self, result: MissionResult) -> None:
        if not result.verified:
            return
        bounded = MissionResult(
            result.mission,
            result.outcome,
            True,
            max(-1.0, min(1.0, result.reward)),
            result.lesson[:500],
        )
        self.results.append(bounded)
        if len(self.results) > self.max_results:
            self.results = self.results[-self.max_results:]

    def lessons(self, mission: str) -> list[str]:
        return [r.lesson for r in self.results if r.mission == mission]
