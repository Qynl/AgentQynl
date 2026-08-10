"""Minimal V5 Minecraft control loop.

This is intentionally model-agnostic: a planner supplies already validated
MinecraftAction objects. The loop captures Minecraft, executes one action, and
captures the result. It never exposes arbitrary desktop actions.
"""
from __future__ import annotations

from collections.abc import Callable

from safety.action_policy import MinecraftAction
from safety.force_escape import ForceEscape
from .capture import observe, MinecraftCapture
from .executor import ExecutionResult, SafeMinecraftExecutor


Planner = Callable[[object], MinecraftAction | None]


class MinecraftAgentLoop:
    def __init__(self, capture: MinecraftCapture, executor: SafeMinecraftExecutor, escape: ForceEscape | None = None) -> None:
        self.capture = capture
        self.executor = executor
        self.escape = escape or ForceEscape()
        self.frame_id = 0

    def step(self, planner: Planner) -> ExecutionResult:
        self.escape.checkpoint()
        observation = observe(self.capture, self.frame_id)
        self.frame_id += 1
        if not observation.game_focused or not observation.screenshot_ref:
            return ExecutionResult(False, "Minecraft capture is not ready/focused")
        action = planner(observation)
        if action is None:
            return ExecutionResult(False, "planner returned no action")
        self.escape.checkpoint()
        return self.executor.execute(action)
