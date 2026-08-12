"""V2.9 production Minecraft vision engine.

Hybrid design:
- deterministic CV extracts geometry/UI signals that pixels can justify;
- an optional semantic VLM supplies labels for blocks/entities/inventory;
- results are merged conservatively and confidence is explicit.

Exact world XYZ, yaw/pitch, and hidden inventory contents are not inferred from
pixels when they cannot be established. Unknown values remain unknown.
"""
from __future__ import annotations
from typing import Any, Protocol

class SemanticBackend(Protocol):
    def analyze(self, image: Any, prompt: str) -> dict[str, Any]: ...

class MinecraftVisionEngine:
    def __init__(self, semantic: SemanticBackend | None = None) -> None:
        self.semantic = semantic

    def analyze(self, image: Any) -> dict[str, Any]:
        cv = self._deterministic(image)
        semantic = {}
        if self.semantic is not None:
            try:
                semantic = self.semantic.analyze(image, self._prompt())
            except Exception:
                semantic = {}
        merged = self._merge(cv, semantic)
        merged["confidence"] = self._scene_confidence(merged)
        return merged

    @staticmethod
    def _prompt() -> str:
        return '''Analyze this Minecraft gameplay screenshot. Return JSON only with keys:
player, crosshair, blocks, entities, hud, inventory, confidence.
Use bbox [x,y,width,height]. Identify visible block/entity names only when visually supported.
Never invent world XYZ, yaw or pitch. Set unknown values to null. Report screen-relative
positions only when visible. For HUD report hearts/food/armor, selected hotbar slot and
visible item names/counts when readable. For inventory report open state and visible slots.
Confidence must be 0..1.'''

    def _deterministic(self, image: Any) -> dict[str, Any]:
        import cv2
        import numpy as np
        arr = np.asarray(image)
        if arr.ndim != 3 or arr.shape[2] not in (3, 4):
            raise ValueError("expected HxWx3/4 image")
        if arr.shape[2] == 4:
            arr = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
        h, w = arr.shape[:2]
        return {
            "player": {"position": None, "screen_position": [w // 2, h // 2], "yaw": None, "pitch": None, "source": "screen"},
            "crosshair": self._crosshair(arr),
            "blocks": self._grid_geometry(arr),
            "entities": [],
            "hud": self._hud(arr),
            "inventory": self._inventory(arr),
        }

    @staticmethod
    def _crosshair(arr: Any) -> dict[str, Any]:
        import cv2
        import numpy as np
        h, w = arr.shape[:2]
        cx, cy = w // 2, h // 2
        r = max(4, int(min(w, h) * 0.02))
        crop = arr[max(0,cy-r):cy+r+1, max(0,cx-r):cx+r+1]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 80, 180)
        bright = float(np.mean(gray > 180))
        line_score = float(np.mean(edges > 0))
        return {"x": cx, "y": cy, "visible_hint": bright > 0.01 or line_score > 0.02,
                "confidence": min(1.0, bright * 10 + line_score * 4)}

    @staticmethod
    def _hud(arr: Any) -> dict[str, Any]:
        import cv2
        import numpy as np
        h, w = arr.shape[:2]
        roi = arr[int(h*.76):int(h*.94), int(w*.18):int(w*.82)]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        red = cv2.inRange(hsv, np.array([0,120,80]), np.array([12,255,255]))
        red |= cv2.inRange(hsv, np.array([165,120,80]), np.array([179,255,255]))
        amber = cv2.inRange(hsv, np.array([8,100,80]), np.array([35,255,255]))
        red_components = MinecraftVisionEngine._components(red, 4)
        amber_components = MinecraftVisionEngine._components(amber, 4)
        return {
            "health": {"visible": bool(red_components), "heart_like_regions": len(red_components), "value": None},
            "food": {"visible": bool(amber_components), "food_like_regions": len(amber_components), "value": None},
            "armor": {"value": None},
            "hotbar_region": [int(w*.25), int(h*.84), int(w*.50), int(h*.14)],
            "confidence": min(1.0, (len(red_components)+len(amber_components))*0.06),
        }

    @staticmethod
    def _inventory(arr: Any) -> dict[str, Any]:
        import cv2
        h, w = arr.shape[:2]
        center = arr[int(h*.12):int(h*.88), int(w*.22):int(w*.78)]
        gray = cv2.cvtColor(center, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 70, 160)
        lines = cv2.HoughLinesP(edges, 1, 3.14159265/180, threshold=max(20, min(center.shape[:2])//12), minLineLength=max(20, min(center.shape[:2])//10), maxLineGap=4)
        vertical = horizontal = 0
        if lines is not None:
            for x1,y1,x2,y2 in lines[:,0]:
                if abs(x2-x1) < 3: vertical += 1
                if abs(y2-y1) < 3: horizontal += 1
        score = min(1.0, (vertical + horizontal) / 40)
        return {"open": score > 0.45, "confidence": score, "slot_count": None, "slots": []}

    @staticmethod
    def _grid_geometry(arr: Any) -> list[dict[str, Any]]:
        import cv2
        h, w = arr.shape[:2]
        gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 70, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        out = []
        area_min = max(100, int(w*h*0.00015))
        for c in contours:
            x,y,bw,bh = cv2.boundingRect(c)
            area = bw*bh
            if area < area_min or bw < 10 or bh < 10:
                continue
            ratio = bw / max(1, bh)
            if 0.45 <= ratio <= 2.2 and bw < int(w*.8) and bh < int(h*.8):
                rect = cv2.contourArea(c) / max(1, area)
                if rect > 0.35:
                    out.append({"label": None, "confidence": min(0.8, rect), "bbox": [x,y,bw,bh], "kind": "block_face_candidate"})
            if len(out) >= 80:
                break
        return out

    @staticmethod
    def _components(mask: Any, min_area: int) -> list[tuple[int,int,int,int]]:
        import cv2
        n, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
        return [tuple(map(int, s[:4])) for s in stats[1:] if int(s[4]) >= min_area]

    @staticmethod
    def _merge(cv: dict[str, Any], semantic: dict[str, Any]) -> dict[str, Any]:
        if not semantic:
            return {"confidence": 0.25, "player": cv["player"], "visible_blocks": cv["blocks"], "entities": cv["entities"],
                    "ui": {"crosshair": cv["crosshair"], "hud": cv["hud"], "inventory": cv["inventory"]}}
        blocks = semantic.get("blocks", cv["blocks"])
        entities = semantic.get("entities", cv["entities"])
        player = dict(cv["player"])
        player.update({k:v for k,v in semantic.get("player", {}).items() if v is not None})
        ui = {"crosshair": semantic.get("crosshair", cv["crosshair"]),
              "hud": {**cv["hud"], **semantic.get("hud", {})},
              "inventory": {**cv["inventory"], **semantic.get("inventory", {})}}
        return {"confidence": float(semantic.get("confidence", 0.4)), "player": player,
                "visible_blocks": blocks, "entities": entities, "ui": ui}

    @staticmethod
    def _scene_confidence(state: dict[str, Any]) -> float:
        values = [float(state.get("confidence", 0)), float(state.get("ui",{}).get("crosshair",{}).get("confidence",0)),
                  float(state.get("ui",{}).get("hud",{}).get("confidence",0))]
        return max(0.0, min(1.0, sum(values)/len(values)))
