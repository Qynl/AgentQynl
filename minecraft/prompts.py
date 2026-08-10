"""Focused prompts for Minecraft vision/planning models."""
from __future__ import annotations

from .goals import PlanningContext


SYSTEM_PROMPT = """You are Qynl, an AI that plays Minecraft and ONLY Minecraft.
Never output code, shell commands, filesystem operations, or generic computer actions.
Choose exactly one small, reversible Minecraft input action at a time.
Prefer short movement/look actions and re-observe frequently. Do not assume an action succeeded.
If perception is uncertain, choose a safe observation/wait action rather than guessing.
Return JSON only with one of:
{"type":"key","key":"w|a|s|d|space|shift|ctrl|e|q|f|1-9","duration_ms":N}
{"type":"mouse_move","x":N,"y":N}
{"type":"mouse_button","button":"left|right","duration_ms":N}
{"type":"wait","duration_ms":N}
"""


def build_planner_prompt(context: PlanningContext) -> str:
    recent = ", ".join(context.recent_actions[-8:]) or "none"
    return (
        f"GOAL: {context.goal.text}\n"
        f"SUCCESS CONDITIONS: {', '.join(context.goal.success_conditions) or 'not specified'}\n"
        f"STEP: {context.step}/{context.goal.max_steps}\n"
        f"VISUAL SUMMARY: {context.vision.summary}\n"
        f"VISIBLE UI: {', '.join(context.vision.visible_ui) or 'none'}\n"
        f"LANDMARKS: {', '.join(context.vision.landmarks) or 'none'}\n"
        f"HAZARDS: {', '.join(context.vision.hazards) or 'none'}\n"
        f"VISION CONFIDENCE: {context.vision.confidence:.2f}\n"
        f"RECENT ACTIONS: {recent}\n"
        "Choose the safest useful next Minecraft action. Return JSON only."
    )
