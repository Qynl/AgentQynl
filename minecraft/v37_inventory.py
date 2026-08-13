"""V3.7 inventory reasoning from vision evidence, without inventing slots."""
from __future__ import annotations

def visible_items(state):
    inv=state.ui.get("inventory", {})
    slots=inv.get("slots", []) if isinstance(inv,dict) else []
    return [s for s in slots if isinstance(s,dict) and s.get("confidence",0) >= .7 and s.get("item")]

def has_item(state, item: str, count: int=1) -> bool:
    total=0
    for slot in visible_items(state):
        if slot.get("item") == item: total += int(slot.get("count",1))
    return total >= count
