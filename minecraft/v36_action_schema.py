"""Structured V3.6 action schema for planner/VLM output."""
from __future__ import annotations
from dataclasses import asdict
from .v35_action_controller import ActionCommand, ALLOWED

REQUIRED = {"action"}

def parse_action(value: dict) -> ActionCommand:
    if not isinstance(value, dict) or not REQUIRED.issubset(value):
        raise ValueError("action object must contain action")
    action = value["action"]
    if action not in ALLOWED:
        raise ValueError(f"unknown Minecraft action: {action}")
    duration = int(value.get("duration_ms", 80))
    dx = int(value.get("dx", 0))
    dy = int(value.get("dy", 0))
    return ActionCommand(action=action, duration_ms=duration, dx=dx, dy=dy)

def action_to_dict(command: ActionCommand) -> dict:
    return asdict(command)
