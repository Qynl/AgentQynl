"""Real multimodal provider for Minecraft V10.

Works with OpenAI-compatible vision endpoints, including configurable NIM and
local Ollama deployments. Provider output is treated as untrusted data.
"""
from __future__ import annotations
import base64, json, os, urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from .goals import PlanningContext
from .vision import VisualAnalysis
from .planner import StructuredMinecraftPlanner

@dataclass(frozen=True)
class VisionModelConfig:
    base_url: str
    model: str
    api_key: str | None = None
    timeout_s: float = 30.0

class OpenAICompatibleMinecraftModel:
    def __init__(self, config: VisionModelConfig): self.config = config
    def _call(self, messages: list[dict[str, Any]], max_tokens: int = 600) -> str:
        body = json.dumps({"model": self.config.model, "messages": messages, "temperature": 0.1, "max_tokens": max_tokens}).encode()
        url = self.config.base_url.rstrip("/") + "/chat/completions"
        headers = {"Content-Type": "application/json"}
        if self.config.api_key: headers["Authorization"] = "Bearer " + self.config.api_key
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=self.config.timeout_s) as response:
            data = json.loads(response.read().decode())
        return data["choices"][0]["message"]["content"]

    def vision(self, image_path: str, prompt: str) -> VisualAnalysis:
        image = base64.b64encode(Path(image_path).read_bytes()).decode()
        content = [{"type":"text","text":prompt},{"type":"image_url","image_url":{"url":"data:image/png;base64,"+image}}]
        raw = self._call([{"role":"system","content":"You are a Minecraft vision system. Analyze only the Minecraft game view. Return valid JSON."},{"role":"user","content":content}])
        try: data = json.loads(raw)
        except json.JSONDecodeError: return VisualAnalysis("Vision response was not valid JSON", confidence=0.0)
        return VisualAnalysis(summary=str(data.get("summary","")), visible_ui=tuple(map(str,data.get("visible_ui",[]))), landmarks=tuple(map(str,data.get("landmarks",[]))), hazards=tuple(map(str,data.get("hazards",[]))), confidence=max(0.0,min(1.0,float(data.get("confidence",0)))))

    def plan_text(self, context: PlanningContext) -> str | None:
        prompt = {"goal":context.goal.text,"success_conditions":context.goal.success_conditions,"step":context.step,"vision":{"summary":context.vision.summary,"ui":context.vision.visible_ui,"landmarks":context.vision.landmarks,"hazards":context.vision.hazards,"confidence":context.vision.confidence},"recent_actions":context.recent_actions}
        return self._call([{"role":"system","content":"You control Minecraft only. Return exactly one JSON action and nothing else. Schema: {type:'key',key:string,duration_ms:int} OR {type:'mouse_move',x:int,y:int} OR {type:'mouse_button',button:'left'|'right',duration_ms:int} OR {type:'wait',duration_ms:int}. Never output code, shell commands, OS actions, or unknown keys. Prefer small reversible actions."},{"role":"user","content":json.dumps(prompt)}], 250)

def config_from_env() -> VisionModelConfig:
    provider = os.getenv("QYNL_PROVIDER","ollama").lower()
    if provider == "nim":
        return VisionModelConfig(os.getenv("QYNL_BASE_URL","https://integrate.api.nvidia.com/v1"), os.getenv("QYNL_MODEL","meta/llama-3.2-11b-vision-instruct"), os.getenv("NVIDIA_API_KEY") or os.getenv("QYNL_API_KEY"))
    return VisionModelConfig(os.getenv("QYNL_BASE_URL","http://127.0.0.1:11434/v1"), os.getenv("QYNL_MODEL","qwen2.5-vl:7b"), os.getenv("QYNL_API_KEY"))
