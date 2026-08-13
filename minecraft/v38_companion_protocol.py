"""V3.8 companion protocol.

Defines the transport-neutral contract between the Qynl desktop runtime and a
Minecraft companion bridge/mod. The bridge owns the in-game player entity;
Qynl owns planning and reasoning.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import json, time
from typing import Any

PROTOCOL_VERSION = "1.0"

@dataclass
class CompanionMessage:
    type: str
    payload: dict[str, Any] = field(default_factory=dict)
    request_id: str | None = None
    version: str = PROTOCOL_VERSION

    def encode(self) -> str:
        return json.dumps({"v": self.version, "type": self.type, "request_id": self.request_id, "payload": self.payload}, separators=(",", ":"))

    @staticmethod
    def decode(raw: str) -> "CompanionMessage":
        obj=json.loads(raw)
        if obj.get("v") != PROTOCOL_VERSION: raise ValueError("unsupported companion protocol")
        if not isinstance(obj.get("type"),str) or not isinstance(obj.get("payload"),dict): raise ValueError("invalid companion message")
        return CompanionMessage(obj["type"], obj["payload"], obj.get("request_id"), obj["v"])

def hello(client_id: str) -> CompanionMessage:
    return CompanionMessage("hello", {"client_id":client_id, "capabilities":["chat","observe","move","interact","inventory","follow","guard","gather","craft","build"]})

def command(request_id: str, action: str, args: dict[str,Any] | None=None) -> CompanionMessage:
    return CompanionMessage("command", {"action":action,"args":args or {},"issued_at":time.time()}, request_id)

def chat(text: str) -> CompanionMessage:
    return CompanionMessage("chat", {"text":text[:1000]})

def observe(state: dict[str,Any]) -> CompanionMessage:
    return CompanionMessage("state", state)
