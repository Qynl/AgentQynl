"""Local Ollama vision client for Qynl.

The client is deliberately provider-agnostic above this layer so Ollama can be
replaced without changing the Minecraft planner.
"""
from __future__ import annotations
import base64, json, urllib.request

class OllamaVisionClient:
    def __init__(self, base_url="http://127.0.0.1:11434", model="llama3.2-vision:11b", timeout=30):
        self.base_url=base_url.rstrip('/'); self.model=model; self.timeout=timeout

    def analyze(self, image_bytes: bytes, prompt: str) -> dict:
        payload={
            "model":self.model,
            "prompt":prompt,
            "images":[base64.b64encode(image_bytes).decode("ascii")],
            "stream":False,
            "format":"json",
            "options":{"temperature":0.1}
        }
        req=urllib.request.Request(self.base_url+"/api/generate",data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=self.timeout) as r:
            response=json.loads(r.read().decode())
        raw=response.get("response", "")
        try: return json.loads(raw)
        except json.JSONDecodeError as e: raise ValueError("Ollama returned non-JSON vision output") from e

VISION_PROMPT='''You are Qynl, a Minecraft co-op companion. Analyze only visible evidence. Never invent hidden blocks, inventory slots, coordinates, entities, health, or actions. Return JSON only with keys: player, hud, scene, inventory, ui, uncertainty. Use confidence 0..1 for every detected object. screen_x/screen_y are pixel coordinates in the supplied image. If unsure, omit the field or use low confidence.''' 
