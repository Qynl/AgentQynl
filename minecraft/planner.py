"""Structured Minecraft planner contract for V6.1."""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Protocol

from safety.action_policy import MinecraftAction
from .goals import PlanningContext


class PlannerProvider(Protocol):
    def plan(self, context: PlanningContext) -> MinecraftAction | None: ...


@dataclass(frozen=True)
class PlannerLimits:
    max_output_chars: int = 4096


class StructuredMinecraftPlanner:
    """Converts provider JSON into one validated Minecraft action object.

    Provider output is data only. It is never executed as code.
    """

    def __init__(self, provider: Any, limits: PlannerLimits | None = None) -> None:
        self.provider = provider
        self.limits = limits or PlannerLimits()

    def plan(self, context: PlanningContext) -> MinecraftAction | None:
        raw = self.provider.plan(context)
        if raw is None:
            return None
        if isinstance(raw, MinecraftAction):
            return raw
        if not isinstance(raw, str) or len(raw) > self.limits.max_output_chars:
            return None
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            return None
        if not isinstance(payload, dict):
            return None
        return self._parse_action(payload)

    @staticmethod
    def _parse_action(payload: dict[str, Any]) -> MinecraftAction | None:
        action_type = payload.get("type")
        if not isinstance(action_type, str):
            return None
        allowed = {"key_down", "key_up", "mouse_move", "mouse_button", "wait"}
        if action_type not in allowed:
            return None
        try:
            if action_type in {"key_down", "key_up"}:
                key = payload["key"]
                if not isinstance(key, str):
                    return None
                return MinecraftAction(type=action_type, key=key)
            if action_type == "mouse_move":
                return MinecraftAction(type=action_type, dx=float(payload["dx"]), dy=float(payload["dy"]))
            if action_type == "mouse_button":
                button = payload["button"]
                if not isinstance(button, str):
                    return None
                return MinecraftAction(type=action_type, button=button)
            return MinecraftAction(type="wait", duration=float(payload["duration"]))
        except (KeyError, TypeError, ValueError):
            return None
