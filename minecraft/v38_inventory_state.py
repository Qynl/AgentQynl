"""Evidence-first inventory state and transfer planning."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ItemEvidence:
    item: str
    count: int
    slot_index: int
    confidence: float
    x: int | None = None
    y: int | None = None

class InventoryPlanner:
    def __init__(self, min_confidence: float = .75): self.min_confidence=min_confidence

    def verified_items(self, state) -> list[ItemEvidence]:
        inv=state.ui.get("inventory", {}) if isinstance(state.ui,dict) else {}
        result=[]
        for s in inv.get("slots", []) if isinstance(inv,dict) else []:
            if not isinstance(s,dict): continue
            c=float(s.get("confidence",0))
            if s.get("item") and c >= self.min_confidence:
                result.append(ItemEvidence(str(s["item"]), int(s.get("count",1)), int(s.get("index",-1)), c, s.get("x"), s.get("y")))
        return result

    def find(self, state, item: str) -> ItemEvidence | None:
        matches=[x for x in self.verified_items(state) if x.item==item]
        return max(matches,key=lambda x:(x.confidence,x.count),default=None)

    def plan_hotbar_transfer(self, state, item: str) -> dict | None:
        evidence=self.find(state,item)
        if evidence is None or evidence.x is None or evidence.y is None: return None
        return {"source": evidence, "requires_inventory_ui": True, "method": "shift_click_or_drag"}
