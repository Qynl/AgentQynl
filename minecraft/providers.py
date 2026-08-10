"""Provider-neutral adapters for Minecraft vision/planning in V6.1.

Network/API transport is deliberately kept behind a tiny interface so secrets
and provider-specific SDKs never enter the Minecraft executor.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .goals import PlanningContext
from .vision import MinecraftVisionProvider, VisualAnalysis


@dataclass(frozen=True)
class VisionRequest:
    image_ref: str
    prompt: str


class CallbackVisionProvider:
    def __init__(self, callback: Callable[[VisionRequest], dict[str, Any]]) -> None:
        self.callback = callback

    def analyze(self, observation) -> VisualAnalysis:
        if not observation.screenshot_ref:
            return VisualAnalysis("No Minecraft frame available", confidence=0.0)
        data = self.callback(VisionRequest(
            image_ref=observation.screenshot_ref,
            prompt="Analyze only the Minecraft game view. Return JSON with summary, visible_ui, landmarks, hazards, confidence.",
        ))
        if not isinstance(data, dict):
            return VisualAnalysis("Vision provider returned invalid data", confidence=0.0)
        return VisualAnalysis(
            summary=str(data.get("summary", "")),
            visible_ui=tuple(str(x) for x in data.get("visible_ui", []) if isinstance(x, (str, int, float))),
            landmarks=tuple(str(x) for x in data.get("landmarks", []) if isinstance(x, (str, int, float))),
            hazards=tuple(str(x) for x in data.get("hazards", []) if isinstance(x, (str, int, float))),
            confidence=max(0.0, min(1.0, float(data.get("confidence", 0.0)))),
        )


class CallbackPlannerProvider:
    def __init__(self, callback: Callable[[PlanningContext], str | None]) -> None:
        self.callback = callback

    def plan(self, context: PlanningContext) -> str | None:
        return self.callback(context)
