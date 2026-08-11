"""V30 deterministic benchmark harness for agent decision quality."""
from __future__ import annotations
from dataclasses import dataclass
from .v30_contracts import CandidateAction, Observation
from .v30_decision_gate import DecisionGate

@dataclass(frozen=True)
class BenchmarkCase:
    name: str
    observation: Observation
    candidates: tuple[CandidateAction, ...]
    expected_action: str | None

@dataclass(frozen=True)
class BenchmarkResult:
    name: str
    passed: bool
    selected: str | None
    expected: str | None

class Benchmark:
    def __init__(self, gate: DecisionGate | None = None) -> None:
        self.gate = gate or DecisionGate()

    def run(self, cases: list[BenchmarkCase]) -> list[BenchmarkResult]:
        results = []
        for case in cases:
            decision = self.gate.choose(case.observation, list(case.candidates))
            selected = decision.action.name if decision.action else None
            results.append(BenchmarkResult(case.name, selected == case.expected_action, selected, case.expected_action))
        return results

    @staticmethod
    def score(results: list[BenchmarkResult]) -> float:
        if not results:
            return 0.0
        return sum(r.passed for r in results) / len(results)
