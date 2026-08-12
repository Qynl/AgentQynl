"""V2.6: detect navigation stalls without issuing input itself."""
from __future__ import annotations

class StuckDetector:
    def __init__(self, max_no_progress: int = 8) -> None:
        if max_no_progress < 1:
            raise ValueError("max_no_progress must be positive")
        self.max_no_progress = max_no_progress
        self.no_progress = 0

    def update(self, moved: bool) -> bool:
        self.no_progress = 0 if moved else self.no_progress + 1
        return self.no_progress >= self.max_no_progress

    def reset(self) -> None:
        self.no_progress = 0
