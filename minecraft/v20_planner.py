"""V20 utility planner: scores bounded Minecraft actions against goals and evidence."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CandidateScore:
    action: object
    utility: float
    reason: str

class UtilityPlanner:
    def __init__(self, model, max_candidates: int = 5) -> None:
        self.model = model
        self.max_candidates = max_candidates

    def rank(self, goal: str, state_context: dict, memories: list, recovery_mode: str = "normal") -> list[CandidateScore]:
        prompt = (
            "Minecraft-only action ranking. Return JSON array of at most " + str(self.max_candidates) +
            " candidates. Each item must contain action, utility (0..1), reason. "
            "Actions must be bounded Minecraft controls only. No code or OS commands. "
            "Prefer observable progress, low risk, and variety after failures.\n"
            f"GOAL={goal}\nMODE={recovery_mode}\nSTATE={state_context}\nMEMORY={memories}"
        )
        data = self.model.parse_json(self.model.text(prompt))
        if not isinstance(data, list):
            return []
        results = []
        for item in data[: self.max_candidates]:
            if not isinstance(item, dict):
                continue
            action = item.get("action")
            try:
                utility = max(0.0, min(1.0, float(item.get("utility", 0))))
            except (TypeError, ValueError):
                continue
            if action is not None:
                results.append(CandidateScore(action, utility, str(item.get("reason", ""))))
        return sorted(results, key=lambda x: x.utility, reverse=True)
