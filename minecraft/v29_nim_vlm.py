"""NVIDIA NIM VLM adapter for Minecraft screenshots.

NIM VLM exposes an OpenAI-compatible /v1/chat/completions endpoint. This
adapter uses only Python's standard library, sends the screenshot as a data
URL, and parses JSON conservatively.
"""
from __future__ import annotations
import base64
import json
import re
import urllib.request
from typing import Any

class NIMVisionBackend:
    def __init__(self, base_url: str = "http://localhost:8000/v1", model: str | None = None,
                 api_key: str = "not-used", timeout_s: float = 8.0, max_tokens: int = 900) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.timeout_s = timeout_s
        self.max_tokens = max_tokens

    def analyze(self, image: Any, prompt: str) -> dict[str, Any]:
        payload = {
            "model": self._model_name(),
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": self._data_url(image)}}
            ]}],
            "temperature": 0,
            "max_tokens": self.max_tokens,
        }
        request = urllib.request.Request(
            self.base_url + "/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
            body = json.loads(response.read().decode("utf-8"))
        content = body["choices"][0]["message"]["content"]
        return self._parse_json(content)

    def _model_name(self) -> str:
        if self.model:
            return self.model
        request = urllib.request.Request(self.base_url + "/models", headers={"Authorization": f"Bearer {self.api_key}"})
        with urllib.request.urlopen(request, timeout=min(self.timeout_s, 3.0)) as response:
            data = json.loads(response.read().decode("utf-8"))
        models = data.get("data", [])
        if not models:
            raise RuntimeError("NIM returned no models")
        return models[0]["id"]

    @staticmethod
    def _data_url(image: Any) -> str:
        import cv2
        import numpy as np
        arr = np.asarray(image)
        if arr.ndim != 3:
            raise ValueError("image must be HxWxC")
        if arr.shape[2] == 4:
            arr = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
        ok, encoded = cv2.imencode(".jpg", arr, [cv2.IMWRITE_JPEG_QUALITY, 82])
        if not ok:
            raise ValueError("could not JPEG encode screenshot")
        return "data:image/jpeg;base64," + base64.b64encode(encoded.tobytes()).decode("ascii")

    @staticmethod
    def _parse_json(content: str) -> dict[str, Any]:
        text = content.strip()
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.I | re.S).strip()
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, flags=re.S)
            if not match:
                raise ValueError("NIM vision response did not contain JSON")
            value = json.loads(match.group(0))
        if not isinstance(value, dict):
            raise ValueError("NIM vision response must be an object")
        return value
