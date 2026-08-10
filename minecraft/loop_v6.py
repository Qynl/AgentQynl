"""V6 observe -> perceive -> goal-context -> plan -> validate -> act loop."""
from __future__ import annotations

from collections.abc import Callable

from safety.action_policy import MinecraftAction
from safety.force_escape import ForceEscape
from .capture import MinecraftCapture, observe
from .executor import ExecutionResult, SafeMinecraftExecutor
from .goals import GoalManager
from .vision import MinecraftVisionProvider

Planner = Callable[[object], MinecraftAction | None]


class MinecraftV6Loop:
    def __init__(self, capture: MinecraftCapture, vision: MinecraftVisionProvider,
                 executor: SafeMinecraftExecutor, goals: GoalManager,
                 escape: ForceEscape | None = None) -> None:
        self.capture = capture
        self.vision = vision
        self.executor = executor
        self.goals = goals
        self.escape = escape or ForceEscape()
        self.frame_id = 0
        self.recent_actions: list[str] = []

    def step(self, planner: Planner) -> ExecutionResult:
        self.escape.checkpoint()
        observation = observe(self.capture, self.frame_id)
        self.frame_id += 1
        if not observation.game_focused or not observation.screenshot_ref:
            return ExecutionResult(False, "Minecraft capture is not ready/focused")

        visual = self.vision.analyze(observation)
        context = self.goals.context(visual, tuple(self.recent_actions[-12:]))
        if context is None:
            return ExecutionResult(False, "No Minecraft goal configured")

        self.escape.checkpoint()
        action = planner(context)
        if action is None:
            return ExecutionResult(False, "planner returned no action")

        self.escape.checkpoint()
        result = self.executor.execute(action)
        self.recent_actions.append(action.type)
        self.goals.advance()
        return result
