"""V7 structured Minecraft planner using the canonical action schema."""
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
    """Parse untrusted provider JSON into one MinecraftAction; never execute it."""

    def __init__(self, provider: Any, limits: PlannerLimits | None = None) -> None:
        self.provider = provider
        self.limits = limits or PlannerLimits()

    def plan(self, context: PlanningContext) -> MinecraftAction | None:
        raw = self.provider.plan(context)
        if isinstance(raw, MinecraftAction):
            return raw
        if not isinstance(raw, str) or len(raw) > self.limits.max_output_chars:
            return None
        try:
            payload = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return None
        if not isinstance(payload, dict):
            return None
        return self._parse_action(payload)

    @staticmethod
    def _parse_action(payload: dict[str, Any]) -> MinecraftAction | None:
        action_type = payload.get("type")
        if action_type == "key":
            key = payload.get("key")
            if not isinstance(key, str):
                return None
            duration = _int(payload.get("duration_ms"))
            if duration is None:
                return None
            return MinecraftAction(type="key", key=key.lower(), duration_ms=duration)
        if action_type == "mouse_move":
            x, y = _int(payload.get("x")), _int(payload.get("y"))
            if x is None or y is None:
                return None
            return MinecraftAction(type="mouse_move", x=x, y=y)
        if action_type == "mouse_button":
            button = payload.get("button")
            duration = _int(payload.get("duration_ms"))
            if not isinstance(button, str) or duration is None:
                return None
            return MinecraftAction(type="mouse_button", button=button.lower(), duration_ms=duration)
        if action_type == "wait":
            duration = _int(payload.get("duration_ms"))
            if duration is None:
                return None
            return MinecraftAction(type="wait", duration_ms=duration)
        return None


def _int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
