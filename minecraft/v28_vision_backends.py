"""Optional semantic vision backends.

The backend contract is intentionally tiny: image -> validated Minecraft
observations. A local CV implementation remains the fallback; model-backed
vision can be injected without changing the runtime.
"""
from __future__ import annotations
import json
from typing import Any, Callable
from .v28_vision_schema import validate_vision_result

SYSTEM_PROMPT = """You are a Minecraft screen-state extractor. Return ONLY JSON with keys confidence, player, visible_blocks, entities, ui. Never invent 3D coordinates. Use null when pixels cannot establish a value. Bounding boxes are [x,y,width,height]. Confidence is 0..1."""

class CallableVisionBackend:
    def __init__(self, infer: Callable[[Any, str], dict[str, Any]]):
        self.infer = infer

    def analyze(self, frame):
        return validate_vision_result(self.infer(frame.image, SYSTEM_PROMPT))

class JsonVisionBackend:
    """Adapter for a vision service returning a JSON string or mapping."""
    def __init__(self, request: Callable[[Any, str], str | dict[str, Any]]):
        self.request = request

    def analyze(self, frame):
        raw = self.request(frame.image, SYSTEM_PROMPT)
        if isinstance(raw, str):
            raw = json.loads(raw)
        return validate_vision_result(raw)
