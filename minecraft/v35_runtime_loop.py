"""V3.5 closed-loop Minecraft runtime.

Observe -> decide externally -> safety -> short action -> observe -> verify.
"""
from __future__ import annotations
from dataclasses import dataclass
from .v35_action_verifier import ActionVerifier
from .v35_observation_memory import ObservationMemory

@dataclass(frozen=True)
class RuntimeResult:
    executed: bool
    verification: dict

class MinecraftClosedLoop:
    def __init__(self, adapter, controller, vision, safety_gate, max_steps: int = 100) -> None:
        self.adapter, self.controller, self.vision, self.safety = adapter, controller, vision, safety_gate
        self.max_steps = max_steps
        self.memory = ObservationMemory()
        self.verifier = ActionVerifier()

    def observe(self):
        state = self.adapter.observe()
        data = {"player": state.player, "blocks": state.visible_blocks, "entities": state.entities, "ui": state.ui, "confidence": state.confidence}
        self.memory.add(data)
        return data

    def step(self, command):
        before = self.observe()
        if before["confidence"] < 0.35:
            self.adapter.stop()
            return RuntimeResult(False, {"verified": False, "reason": "low_confidence"})
        allowed = self.safety(command)
        if not allowed:
            self.adapter.stop()
            return RuntimeResult(False, {"verified": False, "reason": "safety_rejected"})
        self.controller.execute(command)
        after = self.observe()
        return RuntimeResult(True, self.verifier.verify(before, after, command.action))
