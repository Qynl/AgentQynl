"""V12 richer Minecraft state estimation and action-effect scoring."""
from __future__ import annotations
from dataclasses import dataclass
from collections import deque
import math

@dataclass(frozen=True)
class GameState:
    summary: str
    landmarks: tuple[str, ...] = ()
    hazards: tuple[str, ...] = ()
    ui: tuple[str, ...] = ()
    confidence: float = 0.0

@dataclass(frozen=True)
class Transition:
    before: GameState
    after: GameState
    action_type: str
    changed: bool
    novelty: float

class StateTracker:
    def __init__(self, max_states: int = 32) -> None:
        self.history: deque[GameState] = deque(maxlen=max_states)
        self.transitions: deque[Transition] = deque(maxlen=max_states)

    @staticmethod
    def from_vision(vision) -> GameState:
        return GameState(
            summary=str(vision.summary),
            landmarks=tuple(vision.landmarks),
            hazards=tuple(vision.hazards),
            ui=tuple(getattr(vision, "visible_ui", ())),
            confidence=max(0.0, min(1.0, float(getattr(vision, "confidence", 0.0)))),
        )

    def push(self, state: GameState) -> None:
        self.history.append(state)

    def record_transition(self, before: GameState, after: GameState, action_type: str) -> Transition:
        before_tokens = set(before.landmarks) | set(before.hazards) | set(before.ui)
        after_tokens = set(after.landmarks) | set(after.hazards) | set(after.ui)
        union = before_tokens | after_tokens
        novelty = 0.0 if not union else len(before_tokens ^ after_tokens) / len(union)
        transition = Transition(before, after, action_type, before != after, novelty)
        self.transitions.append(transition)
        return transition

    def repeated_state_count(self, state: GameState, window: int = 8) -> int:
        return sum(s == state for s in list(self.history)[-window:])

    def progress_score(self, transition: Transition) -> float:
        """Heuristic feedback, not a claim that visual change equals task success."""
        if not transition.changed:
            return -1.0
        return min(1.0, transition.novelty)
