"""V3.8 Minecraft action vocabulary and bounded controller."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
import time

Action = Literal["forward","back","left","right","jump","sprint","sneak","attack","use","pick_block","drop_item","swap_hands","inventory","chat","pause","hotbar_1","hotbar_2","hotbar_3","hotbar_4","hotbar_5","hotbar_6","hotbar_7","hotbar_8","hotbar_9","look","look_left","look_right","look_up","look_down","stop"]
ALLOWED={"forward","back","left","right","jump","sprint","sneak","attack","use","pick_block","drop_item","swap_hands","inventory","chat","pause",*(f"hotbar_{i}" for i in range(1,10)),"look","look_left","look_right","look_up","look_down","stop"}
KEYS={"forward":"w","back":"s","left":"a","right":"d","jump":"space","sprint":"ctrl","sneak":"shift","drop_item":"q","swap_hands":"f","inventory":"e","chat":"t","pause":"esc"}
@dataclass(frozen=True)
class ActionCommand:
    action: Action; duration_ms:int=80; dx:int=0; dy:int=0
class ActionController:
    def __init__(self,adapter,max_duration_ms:int=750,max_look_pixels:int=500): self.adapter=adapter; self.max_duration_ms=max(20,max_duration_ms); self.max_look_pixels=max(1,max_look_pixels)
    def _duration(self,v:int)->float: return max(20,min(self.max_duration_ms,int(v)))/1000.0
    def _tap(self,key:str,d:float)->None:
        self.adapter.input.key_down(key)
        try: time.sleep(d)
        finally: self.adapter.input.key_up(key)
    def execute(self,command:ActionCommand)->None:
        if command.action not in ALLOWED: raise ValueError(f"action is not allowed: {command.action}")
        a=command.action; d=self._duration(command.duration_ms)
        if a=="stop": self.adapter.stop(); return
        if a=="pick_block": self.adapter.input.mouse_button("middle",True); self.adapter.input.mouse_button("middle",False); return
        if a in KEYS: self._tap(KEYS[a],d); return
        if a.startswith("hotbar_") and a[-1].isdigit(): self._tap(a[-1],d); return
        if a=="attack":
            self.adapter.input.mouse_button("left",True)
            try: time.sleep(d)
            finally: self.adapter.input.mouse_button("left",False)
            return
        if a=="use":
            self.adapter.input.mouse_button("right",True)
            try: time.sleep(d)
            finally: self.adapter.input.mouse_button("right",False)
            return
        if a=="look":
            dx=max(-self.max_look_pixels,min(self.max_look_pixels,int(command.dx))); dy=max(-self.max_look_pixels,min(self.max_look_pixels,int(command.dy))); self.adapter.input.mouse_move(dx,dy); return
        if a in {"look_left","look_right","look_up","look_down"}:
            amount=max(1,min(self.max_look_pixels,abs(int(command.dx or command.dy or 80)))); self.adapter.input.mouse_move(-amount if a=="look_left" else amount if a=="look_right" else 0,-amount if a=="look_up" else amount if a=="look_down" else 0); return
        raise RuntimeError(f"unhandled action: {a}")
