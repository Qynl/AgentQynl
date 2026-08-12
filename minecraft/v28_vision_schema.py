"""Strict schema validation for vision/world-state extraction."""
from __future__ import annotations

REQUIRED_TOP_LEVEL = {"confidence", "player", "visible_blocks", "entities", "ui"}

def validate_vision_result(value: object) -> dict:
    if not isinstance(value, dict):
        raise ValueError("vision result must be a mapping")
    missing = REQUIRED_TOP_LEVEL - value.keys()
    if missing:
        raise ValueError(f"vision result missing fields: {sorted(missing)}")
    confidence = float(value["confidence"])
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence must be between 0 and 1")
    for key in ("visible_blocks", "entities"):
        if not isinstance(value[key], (list, tuple)):
            raise ValueError(f"{key} must be a list or tuple")
    if not isinstance(value["player"], dict) or not isinstance(value["ui"], dict):
        raise ValueError("player and ui must be mappings")
    return value
