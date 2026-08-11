"""V30 single decision gate: uncertainty and risk are handled before execution."""
from __future__ import annotations
from dataclasses import dataclass
from .v30_contracts import CandidateAction, Observation, Decision

@dataclass(frozen=True)
class GateConfig:
    min_confidence: float = 0.55
    max_risk: float = 0.65
    max_action_cost: float = 1.0

class DecisionGate:
    def __init__(self, config: GateConfig | None = None) -> None:
        self.config = config or GateConfig()

    def choose(self, observation: Observation, candidates: list[CandidateAction]) -> Decision:
        if observation.confidence < self.config.min_confidence:
            return Decision(None, "observation confidence too low", observation.confidence)
        valid = [
            c for c in candidates
            if 0.0 <= c.risk <= self.config.max_risk
            and max(0.0, c.expected_progress) <= self.config.max_action_cost
        ]
        if not valid:
            return Decision(None, "no candidate passed the decision gate", observation.confidence)
        chosen = max(valid, key=lambda c: c.expected_progress - c.risk * 0.5)
        return Decision(chosen, "highest bounded utility candidate", observation.confidence)
