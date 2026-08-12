"""Temporal fusion for screen-based Minecraft detections."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import math

@dataclass(frozen=True)
class Track:
    id: int
    kind: str
    label: str | None
    bbox: tuple[int,int,int,int]
    confidence: float
    age: int
    missed: int

def _iou(a: tuple[int,int,int,int], b: tuple[int,int,int,int]) -> float:
    ax, ay, aw, ah = a; bx, by, bw, bh = b
    x1, y1 = max(ax,bx), max(ay,by)
    x2, y2 = min(ax+aw,bx+bw), min(ay+ah,by+bh)
    inter = max(0,x2-x1)*max(0,y2-y1)
    union = aw*ah + bw*bh - inter
    return inter / union if union else 0.0

class TemporalVisionTracker:
    def __init__(self, max_missed: int = 4, iou_threshold: float = 0.25) -> None:
        self.max_missed = max_missed
        self.iou_threshold = iou_threshold
        self._next_id = 1
        self.tracks: dict[int, Track] = {}

    def update(self, detections: list[dict[str, Any]]) -> list[dict[str, Any]]:
        used: set[int] = set()
        updated: dict[int, Track] = {}
        for det in detections:
            bbox = tuple(map(int, det.get("bbox", [0,0,0,0])))
            kind = str(det.get("kind", "unknown"))
            label = det.get("label")
            best_id, best_score = None, 0.0
            for tid, old in self.tracks.items():
                if tid in used or old.kind != kind:
                    continue
                score = _iou(old.bbox, bbox)
                if score >= self.iou_threshold and score > best_score:
                    best_id, best_score = tid, score
            tid = best_id or self._allocate()
            old = self.tracks.get(tid)
            track = Track(tid, kind, label, bbox, float(det.get("confidence", 0.0)),
                          (old.age + 1 if old else 1), 0)
            updated[tid] = track
            used.add(tid)
        for tid, old in self.tracks.items():
            if tid not in used and old.missed + 1 <= self.max_missed:
                updated[tid] = Track(old.id, old.kind, old.label, old.bbox,
                                     old.confidence * 0.85, old.age + 1, old.missed + 1)
        self.tracks = updated
        return [self._as_dict(t) for t in self.tracks.values()]

    def _allocate(self) -> int:
        tid = self._next_id
        self._next_id += 1
        return tid

    @staticmethod
    def _as_dict(track: Track) -> dict[str, Any]:
        return {"track_id": track.id, "kind": track.kind, "label": track.label,
                "bbox": list(track.bbox), "confidence": track.confidence,
                "age": track.age, "missed": track.missed}
