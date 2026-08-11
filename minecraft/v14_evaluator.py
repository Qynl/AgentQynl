"""V14 goal and action evaluation without pretending visual change means success."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Evaluation:
    success: bool
    score: float
    evidence: str

class GoalEvaluator:
    def __init__(self, model) -> None:
        self.model = model

    def evaluate(self, goal: str, success_hint: str, before, after) -> Evaluation:
        prompt = (
            "Minecraft-only evaluator. Decide whether the stated subtask is visibly satisfied. "
            "Use only evidence in the two observations. If uncertain, return success=false. "
            "Return JSON only: {success:boolean,score:number,evidence:string}.\n"
            f"GOAL={goal}\nSUCCESS_HINT={success_hint}\nBEFORE={before}\nAFTER={after}"
        )
        data = self.model.parse_json(self.model.text(prompt))
        if not isinstance(data, dict):
            return Evaluation(False, 0.0, "invalid evaluator output")
        success = data.get("success") is True
        try:
            score = max(0.0, min(1.0, float(data.get("score", 1.0 if success else 0.0))))
        except (TypeError, ValueError):
            score = 0.0
        return Evaluation(success, score, str(data.get("evidence", "")))
