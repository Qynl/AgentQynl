"""Emergency Force-Escape controller for the Qynl Minecraft agent.

This is intentionally independent from the model/provider layer. The escape
key is a local operator control and must never be callable by model output.
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import Event, Lock


@dataclass(frozen=True)
class ForceEscapeState:
    engaged: bool
    reason: str | None = None


class ForceEscape:
    """Thread-safe emergency latch for immediately stopping agent actions."""

    def __init__(self) -> None:
        self._event = Event()
        self._lock = Lock()
        self._reason: str | None = None

    def trigger(self, reason: str = "operator force escape") -> None:
        with self._lock:
            self._reason = reason
            self._event.set()

    def clear(self) -> None:
        with self._lock:
            self._reason = None
            self._event.clear()

    def is_engaged(self) -> bool:
        return self._event.is_set()

    def checkpoint(self) -> None:
        """Raise immediately when an action loop reaches a safety checkpoint."""
        if self._event.is_set():
            raise RuntimeError("Qynl Force ESC engaged: agent actions halted")

    def state(self) -> ForceEscapeState:
        with self._lock:
            return ForceEscapeState(self._event.is_set(), self._reason)
