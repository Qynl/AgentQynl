"""Typed V4 settings limited to the Minecraft agent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Provider = Literal["NVIDIA_NIM", "OLLAMA", "OPENAI_COMPATIBLE"]


@dataclass(frozen=True)
class AgentSettings:
    provider: Provider = "NVIDIA_NIM"
    model: str = ""
    endpoint: str = ""
    safe_mode: bool = True
    require_approval: bool = True
    capture_fps: float = 2.0
    max_actions_per_minute: int = 120
    persist_screenshots: bool = False

    def validate(self) -> None:
        if not 0.1 <= self.capture_fps <= 10:
            raise ValueError("capture_fps must be between 0.1 and 10")
        if not 1 <= self.max_actions_per_minute <= 600:
            raise ValueError("max_actions_per_minute must be between 1 and 600")
        if self.provider not in {"NVIDIA_NIM", "OLLAMA", "OPENAI_COMPATIBLE"}:
            raise ValueError("unsupported provider")
