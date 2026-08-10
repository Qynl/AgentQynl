"""Minecraft-only executor boundary.

V4 deliberately ships a dry-run executor first. A future real executor must
validate through ActionPolicy and ForceEscape immediately before input.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from safety.action_policy import ActionPolicy, MinecraftAction
from safety.force_escape import ForceEscape


@dataclass(frozen=True)
class ExecutionResult:
    executed: bool
    reason: str


class MinecraftInput(Protocol):
    def send(self, action: MinecraftAction) -> None:
        """Send one already-validated Minecraft action."""


class DryRunExecutor:
    """Never sends OS input. Useful for UI and end-to-end policy testing."""

    def __init__(self, policy: ActionPolicy | None = None, escape: ForceEscape | None = None) -> None:
        self.policy = policy or ActionPolicy()
        self.escape = escape or ForceEscape()

    def execute(self, action: MinecraftAction) -> ExecutionResult:
        decision = self.policy.validate(action)
        if not decision.allowed:
            return ExecutionResult(False, decision.reason)
        if self.escape.is_engaged():
            return ExecutionResult(False, "Force ESC engaged")
        return ExecutionResult(True, "dry-run: action validated but not sent")


class SafeMinecraftExecutor:
    """Real-input boundary; requires an explicitly supplied Minecraft input adapter."""

    def __init__(self, input_adapter: MinecraftInput, policy: ActionPolicy | None = None, escape: ForceEscape | None = None) -> None:
        self.input = input_adapter
        self.policy = policy or ActionPolicy()
        self.escape = escape or ForceEscape()

    def execute(self, action: MinecraftAction) -> ExecutionResult:
        decision = self.policy.validate(action)
        if not decision.allowed:
            return ExecutionResult(False, decision.reason)
        self.escape.checkpoint()
        self.input.send(action)
        return ExecutionResult(True, "Minecraft action sent")
