"""V3.7 Minecraft gameplay helpers: perception-driven tasks and recovery."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class TaskState(str, Enum):
    RUNNING="running"; SUCCESS="success"; RETRY="retry"; FAILED="failed"

@dataclass(frozen=True)
class Target:
    kind: str
    name: str | None = None
    max_distance: float = 12.0

class PerceptionPolicy:
    def __init__(self, min_confidence: float=.55, max_age_s: float=1.0):
        self.min_confidence=min_confidence; self.max_age_s=max_age_s
    def accept(self, state, now: float) -> bool:
        return state.confidence >= self.min_confidence and now-state.timestamp <= self.max_age_s

class RecoveryPlanner:
    STEPS=("stop","look_left","look_right","back","jump","reobserve")
    def next(self, attempt: int) -> str:
        return self.STEPS[min(max(attempt,0), len(self.STEPS)-1)]

class TargetSelector:
    def nearest(self, state, target: Target):
        candidates=[]
        for obj in state.visible_blocks if target.kind=="block" else state.entities:
            if target.name and obj.get("name") != target.name: continue
            d=obj.get("distance")
            if isinstance(d,(int,float)) and d <= target.max_distance:
                candidates.append(obj)
        return min(candidates,key=lambda x:x["distance"]) if candidates else None

class GameplayTask:
    def __init__(self, target: Target, selector: TargetSelector|None=None):
        self.target=target; self.selector=selector or TargetSelector(); self.attempts=0
    def evaluate(self,state):
        obj=self.selector.nearest(state,self.target)
        if obj is None: return TaskState.RETRY,None
        return TaskState.SUCCESS,obj
