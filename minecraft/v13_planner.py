"""V13 planner context: temporal evidence, uncertainty and action intent."""
from __future__ import annotations
from dataclasses import dataclass
import json

@dataclass(frozen=True)
class PlannerEvidence:
    current: object
    delta: object
    recent: tuple[object, ...]
    failures: tuple[str, ...] = ()

    def compact(self) -> dict:
        def state(s):
            return {
                "summary": s.summary,
                "entities":[e.label for e in s.entities],
                "landmarks":list(s.landmarks),
                "hazards":list(s.hazards),
                "ui":list(s.ui),
                "confidence":s.confidence,
            }
        return {
            "current": state(self.current),
            "delta": {
                "added_entities": list(self.delta.added_entities),
                "removed_entities": list(self.delta.removed_entities),
                "changed_ui": self.delta.changed_ui,
                "changed_landmarks": self.delta.changed_landmarks,
                "changed_hazards": self.delta.changed_hazards,
                "confidence_delta": self.delta.confidence_delta,
            },
            "recent": [state(s) for s in self.recent],
            "failures": list(self.failures[-6:]),
        }

def build_v13_prompt(goal_text: str, success_conditions: tuple[str, ...], evidence: PlannerEvidence) -> str:
    return (
        "You are the action planner for a Minecraft-only agent.\n"
        "Use the temporal evidence, not guesses. Choose ONE small action.\n"
        "Prefer actions whose effect can be verified on the next frame.\n"
        "If confidence is low, observe/wait or use a very small reversible action.\n"
        "Do not repeat a failed action unless evidence shows the state changed.\n"
        "Return JSON only. Allowed schema: {type:'key',key:string,duration_ms:int}, "
        "{type:'mouse_move',x:int,y:int}, {type:'mouse_button',button:'left'|'right',duration_ms:int}, "
        "or {type:'wait',duration_ms:int}. Never output code or OS commands.\n\n"
        + json.dumps({"goal":goal_text,"success_conditions":success_conditions,"evidence":evidence.compact()}, separators=(",",":"))
    )
