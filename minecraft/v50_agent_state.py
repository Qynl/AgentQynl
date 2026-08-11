"""V50 explicit finite-state runtime for long Minecraft sessions."""
from __future__ import annotations
from enum import Enum

class AgentState(str, Enum):
    BOOT = "boot"
    OBSERVE = "observe"
    THINK = "think"
    ACT = "act"
    VERIFY = "verify"
    RECOVER = "recover"
    PAUSED = "paused"
    COMPLETE = "complete"
    ABORTED = "aborted"

_ALLOWED = {
    AgentState.BOOT: {AgentState.OBSERVE, AgentState.ABORTED},
    AgentState.OBSERVE: {AgentState.THINK, AgentState.PAUSED, AgentState.ABORTED},
    AgentState.THINK: {AgentState.ACT, AgentState.OBSERVE, AgentState.PAUSED, AgentState.ABORTED},
    AgentState.ACT: {AgentState.VERIFY, AgentState.RECOVER, AgentState.PAUSED, AgentState.ABORTED},
    AgentState.VERIFY: {AgentState.OBSERVE, AgentState.RECOVER, AgentState.COMPLETE, AgentState.ABORTED},
    AgentState.RECOVER: {AgentState.OBSERVE, AgentState.PAUSED, AgentState.ABORTED},
    AgentState.PAUSED: {AgentState.OBSERVE, AgentState.ABORTED},
    AgentState.COMPLETE: set(),
    AgentState.ABORTED: set(),
}

class AgentStateMachine:
    def __init__(self) -> None:
        self.state = AgentState.BOOT

    def transition(self, target: AgentState) -> None:
        if target not in _ALLOWED[self.state]:
            raise ValueError(f"invalid transition: {self.state} -> {target}")
        self.state = target
