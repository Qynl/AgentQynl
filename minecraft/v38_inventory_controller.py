"""V3.8 inventory + hotbar controller.

Uses Minecraft's normal keyboard inventory controls. Inventory placement is
performed through explicit slot coordinates supplied by the vision layer;
coordinates are never invented by this module.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class InventorySlot:
    index: int
    x: int
    y: int
    confidence: float = 0.0

class InventoryController:
    def __init__(self, input_adapter, min_confidence: float = .75):
        self.input = input_adapter
        self.min_confidence = min_confidence

    def select_hotbar(self, slot: int) -> None:
        if not 1 <= slot <= 9:
            raise ValueError("hotbar slot must be 1..9")
        self.input.key_down(str(slot)); self.input.key_up(str(slot))

    def click_slot(self, slot: InventorySlot, button: str = "left") -> None:
        if slot.confidence < self.min_confidence:
            raise ValueError("inventory slot confidence too low")
        self.input.mouse_move(slot.x, slot.y)
        self.input.mouse_button(button, True)
        self.input.mouse_button(button, False)

    def move_to_hotbar(self, slot: InventorySlot) -> None:
        self.click_slot(slot, "left")

    def quick_move_to_hotbar(self, slot: InventorySlot) -> None:
        """Shift-click a verified inventory slot into Minecraft's hotbar."""
        if slot.confidence < self.min_confidence:
            raise ValueError("inventory slot confidence too low")
        self.input.mouse_move(slot.x, slot.y)
        self.input.key_down("shift")
        try:
            self.input.mouse_button("left", True); self.input.mouse_button("left", False)
        finally:
            self.input.key_up("shift")
