"""Ready-to-wire hybrid Minecraft vision backend.

Local CV always runs first. Semantic VLM inference is optional and can be
rate-limited because screenshots arrive faster than a VLM can reason.
"""
from __future__ import annotations
from typing import Any
import time
from .v29_vision_engine import MinecraftVisionEngine
from .v29_temporal_vision import TemporalVisionTracker

class HybridMinecraftVisionBackend:
    def __init__(self, semantic=None, semantic_interval_s: float = 0.20) -> None:
        self.engine = MinecraftVisionEngine(semantic)
        self.semantic = semantic
        self.semantic_interval_s = max(0.0, semantic_interval_s)
        self.last_semantic_at = -float("inf")
        self.block_tracker = TemporalVisionTracker()
        self.entity_tracker = TemporalVisionTracker()

    def analyze(self, image: Any) -> dict[str, Any]:
        now = time.monotonic()
        use_semantic = self.semantic is not None and now - self.last_semantic_at >= self.semantic_interval_s
        if use_semantic:
            self.last_semantic_at = now
            state = self.engine.analyze(image)
        else:
            state = self.engine._deterministic(image)
            state = {"confidence": 0.25, "player": state["player"],
                     "visible_blocks": state["blocks"], "entities": state["entities"],
                     "ui": {"crosshair": state["crosshair"], "hud": state["hud"], "inventory": state["inventory"]}}
        state["visible_blocks"] = self.block_tracker.update(list(state.get("visible_blocks", [])))
        state["entities"] = self.entity_tracker.update(list(state.get("entities", [])))
        state["ui"]["vision_mode"] = "hybrid_semantic" if use_semantic else "local_cv"
        state["ui"]["semantic_age_s"] = None if use_semantic else max(0.0, now - self.last_semantic_at)
        return state
