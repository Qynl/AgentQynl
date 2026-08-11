"""V15 verifies actions using pre/post evidence and watchdog constraints."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ActionVerification:
    executed: bool
    observable_change: bool
    score: float
    reason: str

class ActionVerifier:
    def verify(self, before, after, action_type: str) -> ActionVerification:
        if before is None or after is None:
            return ActionVerification(False, False, 0.0, "missing observation")
        changed = before != after
        before_entities = {getattr(x, "label", str(x)) for x in getattr(before, "entities", ())}
        after_entities = {getattr(x, "label", str(x)) for x in getattr(after, "entities", ())}
        entity_change = before_entities != after_entities
        structural = (
            before.landmarks != after.landmarks or
            before.hazards != after.hazards or
            before.ui != after.ui
        )
        score = 1.0 if changed else 0.0
        if entity_change or structural:
            score = min(1.0, score + 0.25)
        return ActionVerification(True, changed, score, "observable state change" if changed else "no observable state change")
