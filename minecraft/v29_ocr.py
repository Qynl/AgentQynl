"""Optional OCR for Minecraft text such as item tooltips and chat."""
from __future__ import annotations
from typing import Any

class MinecraftOCR:
    def __init__(self, lang: str = "eng") -> None:
        self.lang = lang

    def read(self, image: Any, roi: tuple[int,int,int,int] | None = None) -> dict:
        import cv2
        import numpy as np
        import pytesseract
        arr = np.asarray(image)
        if roi:
            x,y,w,h = roi
            arr = arr[max(0,y):y+h, max(0,x):x+w]
        if arr.ndim == 3:
            gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
        else:
            gray = arr
        scale = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        clean = cv2.threshold(scale, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        data = pytesseract.image_to_data(clean, lang=self.lang, config="--psm 6", output_type=pytesseract.Output.DICT)
        words = []
        for i, text in enumerate(data["text"]):
            text = text.strip()
            conf = float(data["conf"][i])
            if text and conf >= 35:
                words.append({"text": text, "confidence": min(1.0, conf/100),
                              "bbox": [int(data["left"][i]/2), int(data["top"][i]/2), int(data["width"][i]/2), int(data["height"][i]/2)]})
        return {"text": " ".join(x["text"] for x in words), "words": words,
                "confidence": sum((x["confidence"] for x in words), 0.0) / len(words) if words else 0.0}
