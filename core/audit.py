"""Bounded audit records for Minecraft agent actions."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone

from safety.action_policy import MinecraftAction


@dataclass(frozen=True)
class AuditRecord:
    timestamp: datetime
    stage: str
    action_type: str
    allowed: bool
    reason: str


class AuditLog:
    """In-memory bounded audit log. No screenshots, secrets, or arbitrary OS data."""

    def __init__(self, max_records: int = 1000) -> None:
        if max_records < 1:
            raise ValueError("max_records must be positive")
        self._records: deque[AuditRecord] = deque(maxlen=max_records)

    def record(self, stage: str, action: MinecraftAction, allowed: bool, reason: str) -> None:
        self._records.append(
            AuditRecord(datetime.now(timezone.utc), stage, action.type, allowed, reason)
        )

    def records(self) -> tuple[AuditRecord, ...]:
        return tuple(self._records)

    def clear(self) -> None:
        self._records.clear()
