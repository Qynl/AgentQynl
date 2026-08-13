"""V3.5 post-action verification."""
from __future__ import annotations

class ActionVerifier:
    def verify(self, before: dict, after: dict, action: str) -> dict:
        player_before = before.get("player", {}).get("screen_position")
        player_after = after.get("player", {}).get("screen_position")
        moved = player_before != player_after if player_before is not None and player_after is not None else None
        return {"action": action, "moved": moved, "state_changed": before != after,
                "verified": moved is True or before != after}
