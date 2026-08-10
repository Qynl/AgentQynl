"""Minecraft-only visual perception interfaces for V6."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .observation import MinecraftObservation


@dataclass(frozen=True)
class VisualAnalysis:
    summary: str
    visible_ui: tuple[str, ...] = ()
    landmarks: tuple[str, ...] = ()
    hazards: tuple[str, ...] = ()
    confidence: float = 0.0


class MinecraftVisionProvider(Protocol):
    def analyze(self, observation: MinecraftObservation) -> VisualAnalysis: ...


class NullVisionProvider:
    """Safe fallback that never invents visual facts."""

    def analyze(self, observation: MinecraftObservation) -> VisualAnalysis:
        return VisualAnalysis(summary="No vision provider configured", confidence=0.0)
