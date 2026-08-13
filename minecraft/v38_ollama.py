"""V3.8 local Ollama vision backend for Minecraft."""
from __future__ import annotations
import base64
import json
import urllib.request
from dataclasses import dataclass

@dataclass(frozen=True)
class OllamaConfig:
    endpoint: str = "http://127.0.0.1:11434/api/chat"
    model: str = "llama3.2-vision:11b"
    timeout_s: float = 30.0
    temperature: float = 0.1

SYSTEM_PROMPT = """You are Qynl, a Minecraft co-op companion. Analyze only the supplied Minecraft frame and provided state. Never invent unseen blocks, entities, inventory slots, coordinates, health, or actions. Return JSON only. Separate observations from guesses. Prefer short, verifiable next goals. You are a teammate, not a narrator."""

class OllamaVision:
    def __init__(self, config: OllamaConfig | None = None):
        self.config = config or OllamaConfig()

    def analyze(self, image_bytes: bytes, state: dict | None = None, user_instruction: str | None = None) -> dict:
        payload={
            "model": self.config.model,
            "stream": False,
            "format": "json",
            "options": {"temperature": self.config.temperature},
            "messages": [
                {"role":"system","content":SYSTEM_PROMPT},
                {"role":"user","content": self._prompt(state, user_instruction), "images":[base64.b64encode(image_bytes).decode("ascii")]}
            ]
        }
        req=urllib.request.Request(self.config.endpoint, data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=self.config.timeout_s) as response:
            body=json.loads(response.read().decode())
        content=body.get("message",{}).get("content","")
        result=json.loads(content)
        if not isinstance(result,dict): raise ValueError("Ollama returned non-object JSON")
        return result

    @staticmethod
    def _prompt(state: dict | None, instruction: str | None) -> str:
        return json.dumps({
            "task":"perceive_minecraft",
            "current_state":state or {},
            "player_instruction":instruction or "Continue helping the player safely.",
            "required_fields":["observations","targets","inventory","threats","ui","next_goal","confidence"],
            "rules":["Use null/[] when unknown.","Confidence is 0..1.","Do not output keyboard or mouse commands."]
        })
