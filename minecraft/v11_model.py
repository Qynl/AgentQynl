"""V11 model helpers: action parsing and recovery prompts."""
from __future__ import annotations
import json
from safety.action_policy import MinecraftAction


def parse_minecraft_action(raw: str | None) -> MinecraftAction | None:
    if not raw or len(raw) > 4096:
        return None
    try:
        data = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    typ = data.get("type")
    try:
        if typ == "key":
            return MinecraftAction("key", key=str(data["key"]), duration_ms=int(data["duration_ms"]))
        if typ == "mouse_move":
            return MinecraftAction("mouse_move", x=int(data["x"]), y=int(data["y"]))
        if typ == "mouse_button":
            return MinecraftAction("mouse_button", button=str(data["button"]), duration_ms=int(data["duration_ms"]))
        if typ == "wait":
            return MinecraftAction("wait", duration_ms=int(data["duration_ms"]))
    except (KeyError, TypeError, ValueError):
        return None
    return None


def recovery_prompt(failures: list[str]) -> str:
    return (
        "You are playing Minecraft. Recovery mode is active because recent actions did not produce visible progress. "
        "Analyze the current Minecraft screenshot and choose ONE small reversible action. "
        "Do not repeat a failed action unless the screenshot clearly shows the situation changed. "
        "Return JSON only using the Minecraft action schema. Recent failures: " + json.dumps(failures[-8:])
    )
