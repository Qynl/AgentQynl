"""V3.7 high-level task decomposition for common Minecraft goals."""
from __future__ import annotations

RECIPES={
 "wood": ["find oak_log", "approach target", "attack target", "verify inventory"],
 "crafting_table": ["ensure oak logs", "craft planks", "craft crafting table", "verify inventory"],
 "stone_tools": ["find stone", "approach target", "mine stone", "craft stone tools", "verify inventory"],
 "food": ["find food source", "approach target", "interact/attack", "verify food"],
}

def decompose_goal(goal: str) -> list[str]:
    key=goal.strip().lower().replace(" ","_")
    for name, steps in RECIPES.items():
        if name in key: return list(steps)
    return ["observe environment", "identify required resources", "plan next safe action", "execute short action", "verify progress"]
