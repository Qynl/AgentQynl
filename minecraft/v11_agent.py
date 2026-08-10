"""V11 adaptive Minecraft agent: vision, memory, verification and recovery."""
from __future__ import annotations
from dataclasses import dataclass
import time
from collections import deque
from typing import Callable
from safety.action_policy import MinecraftAction, ActionPolicy

@dataclass(frozen=True)
class ObservationSignature:
    summary: str
    landmarks: tuple[str, ...]
    hazards: tuple[str, ...]

@dataclass(frozen=True)
class Episode:
    before: ObservationSignature
    action: MinecraftAction
    after: ObservationSignature | None
    success: bool
    reason: str

class V11Memory:
    def __init__(self, max_episodes: int = 200) -> None:
        self.episodes: deque[Episode] = deque(maxlen=max_episodes)

    def add(self, episode: Episode) -> None:
        self.episodes.append(episode)

    def recent_failures(self, n: int = 8) -> list[Episode]:
        return [e for e in list(self.episodes)[-n:] if not e.success]

class StuckDetector:
    def __init__(self, window: int = 6) -> None:
        self.window = window
        self.signatures: deque[ObservationSignature] = deque(maxlen=window)

    def push(self, sig: ObservationSignature) -> None:
        self.signatures.append(sig)

    def stuck(self) -> bool:
        if len(self.signatures) < self.window:
            return False
        return len(set(self.signatures)) <= 2

class V11Controller:
    """Adds closed-loop verification around an existing V10 model.

    The controller never executes a model action before ActionPolicy validation.
    """
    def __init__(self, model, capture, executor, goals, escape, policy: ActionPolicy | None = None) -> None:
        self.model = model
        self.capture = capture
        self.executor = executor
        self.goals = goals
        self.escape = escape
        self.policy = policy or ActionPolicy()
        self.memory = V11Memory()
        self.stuck_detector = StuckDetector()
        self.frame_id = 0

    def _signature(self, vision) -> ObservationSignature:
        return ObservationSignature(vision.summary, tuple(vision.landmarks), tuple(vision.hazards))

    def step(self) -> tuple[bool, str]:
        self.escape.checkpoint()
        frame = self.capture.capture()
        if not frame.screenshot_ref:
            return False, "capture unavailable"
        before = self.model.vision(frame.screenshot_ref, "Return JSON only. Analyze visible Minecraft facts. Track changes from previous context if provided. Do not guess.")
        before_sig = self._signature(before)
        self.stuck_detector.push(before_sig)
        context = self.goals.context(before, tuple(e.action.type for e in self.memory.episodes[-8:]))
        if context is None:
            return False, "no goal"

        if self.stuck_detector.stuck():
            raw = self.model.plan_recovery(context, [e.reason for e in self.memory.recent_failures()])
        else:
            raw = self.model.plan_text(context)
        action = self.model.parse_action(raw)
        if action is None:
            return False, "invalid model action"
        decision = self.policy.validate(action)
        if not decision.allowed:
            return False, "policy rejected: " + decision.reason
        self.escape.checkpoint()
        result = self.executor.execute(action)
        if not result.executed:
            self.memory.add(Episode(before_sig, action, None, False, result.reason))
            return False, result.reason

        time.sleep(min(0.35, max(0.05, action.duration)))
        self.escape.checkpoint()
        after_frame = self.capture.capture()
        after = self.model.vision(after_frame.screenshot_ref, "Return JSON only. Analyze visible Minecraft facts and identify what changed after the last action.") if after_frame.screenshot_ref else None
        after_sig = self._signature(after) if after else None
        changed = after_sig is not None and after_sig != before_sig
        self.memory.add(Episode(before_sig, action, after_sig, changed, "verified change" if changed else "no visible change"))
        self.frame_id += 1
        return True, "verified change" if changed else "action executed; no visible change"
