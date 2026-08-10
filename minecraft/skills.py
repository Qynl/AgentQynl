"""Reusable, model-independent Minecraft micro-skills for V7."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from safety.action_policy import MinecraftAction


@dataclass(frozen=True)
class SkillStep:
    name: str
    action: MinecraftAction


@dataclass(frozen=True)
class SkillResult:
    success: bool
    reason: str


class SkillLibrary:
    """Small deterministic primitives the planner can compose safely."""

    @staticmethod
    def stop() -> tuple[SkillStep, ...]:
        return (
            SkillStep("release_w", MinecraftAction(type="key", key="w", duration_ms=0)),
            SkillStep("release_a", MinecraftAction(type="key", key="a", duration_ms=0)),
            SkillStep("release_s", MinecraftAction(type="key", key="s", duration_ms=0)),
            SkillStep("release_d", MinecraftAction(type="key", key="d", duration_ms=0)),
        )

    @staticmethod
    def look(dx: int, dy: int) -> tuple[SkillStep, ...]:
        return (SkillStep("look", MinecraftAction(type="mouse_move", x=dx, y=dy)),)

    @staticmethod
    def walk(key: str, duration_ms: int) -> tuple[SkillStep, ...]:
        if key not in {"w", "a", "s", "d"}:
            raise ValueError("walk key is not a Minecraft movement key")
        return (SkillStep("walk", MinecraftAction(type="key", key=key, duration_ms=duration_ms)),)

    @staticmethod
    def interact(button: str = "right") -> tuple[SkillStep, ...]:
        return (SkillStep("interact", MinecraftAction(type="mouse_button", button=button, duration_ms=80)),)
