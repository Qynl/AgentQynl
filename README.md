# Qynl Agent V3.8

Qynl is a Minecraft-only autonomous AI agent focused on screen perception, world-state reasoning, navigation, inventory interaction, bounded actions, task decomposition, verification and runtime safety.

## V3.8: Inventory + Gameplay Interaction

V3.8 expands the gameplay layer substantially. Qynl can now reason about verified inventory evidence and interact with inventory slots, including moving a verified item toward the hotbar. Hotbar selection uses Minecraft's normal **1-9 number keys**, not mouse-wheel simulation.

### New

- evidence-based inventory state
- inventory item lookup by confidence
- inventory slot coordinate validation
- click/drag-ready slot interaction boundary
- shift-click quick-move toward hotbar
- explicit hotbar slots 1-9
- number-key hotbar selection
- removed wheel-based hotbar actions
- safer inventory interaction when vision confidence is low

## Hotbar

The action language now treats Minecraft's hotbar as nine explicit slots:

```text
hotbar_1
hotbar_2
hotbar_3
hotbar_4
hotbar_5
hotbar_6
hotbar_7
hotbar_8
hotbar_9
```

Internally these map to the real keyboard keys `1` through `9`.

The old `hotbar_next` / `hotbar_prev` wheel actions are removed. This avoids pretending that a wheel event is a normal Minecraft hotbar-selection primitive.

## Inventory interaction

`minecraft/v38_inventory_state.py` converts vision output into verified item evidence.

An item is usable for an inventory plan only when the vision layer supplies:

- item identifier
- count
- slot index
- confidence
- screen coordinates when an interaction is required

Example:

```text
Vision
 ↓
slot 12
item = oak_log
count = 3
confidence = 0.91
x/y = verified
 ↓
InventoryPlanner
 ↓
quick-move / click plan
 ↓
InventoryController
 ↓
Minecraft
 ↓
re-observe inventory
 ↓
verify result
```

### Moving an item toward the hotbar

`minecraft/v38_inventory_controller.py` supports:

```text
select_hotbar(1..9)
click_slot(...)
quick_move_to_hotbar(...)
```

`quick_move_to_hotbar` uses Minecraft's normal Shift-click behavior. It requires a sufficiently confident, coordinate-bearing inventory observation first.

The controller does **not** guess where a slot is on screen.

## Why this matters

Inventory is one of the biggest differences between a demo agent and a useful Minecraft agent.

The agent must be able to reason about:

```text
What do I have?
      ↓
What do I need?
      ↓
Where is it?
      ↓
Which hotbar slot should hold it?
      ↓
Move/select it
      ↓
Verify the new inventory state
```

V3.8 creates the interaction boundary for this loop while keeping perception evidence separate from input execution.

## Full runtime

```text
SCREEN
  ↓
HYBRID VISION
  ↓
VALIDATED WORLD STATE
  ↓
FRESHNESS + CONFIDENCE
  ↓
GOAL DECOMPOSITION
  ↓
TARGET / INVENTORY REASONING
  ↓
A* + CAMERA NAVIGATION
  ↓
SAFETY
  ↓
STRUCTURED ACTION
  ↓
MINECRAFT
  ↓
OBSERVE
  ↓
VERIFY
  ↓
PROGRESS / RECOVER / REPLAN
  ↺
```

## V3.8 action examples

```text
hotbar_1
```

Selects slot 1.

```text
hotbar_7
```

Selects slot 7.

```text
inventory
```

Opens/closes the inventory using Minecraft's normal `E` key binding.

```text
look(dx=120, dy=-15)
```

Moves the camera through the mouse adapter, with bounded deltas.

Inventory actions are deliberately represented separately from generic movement actions so the planner can reason about UI state.

## Existing gameplay systems

V3.8 builds on:

```text
V2.6  A* pathfinding
V2.8  production adapters
V2.9  hybrid Minecraft vision + optional NIM VLM
V3.5  closed-loop runtime
V3.6  structured Minecraft action language
V3.7  gameplay reliability + task decomposition
V3.8  inventory interaction + explicit hotbar control
```

## Safety

The model still does not get arbitrary OS input access:

```text
AI / VLM
 ↓
structured Minecraft command
 ↓
confidence + freshness
 ↓
safety supervisor
 ↓
bounded controller
 ↓
Minecraft
```

Inventory interactions additionally require confidence-bearing slot coordinates.

Emergency stop remains outside the model's control.

## Important limitation

Screen-only inventory interaction is inherently sensitive to Minecraft GUI scale, window position, resolution, resource packs and UI layout. V3.8 therefore treats coordinates as **vision evidence**, not hard-coded universal positions.

A failed inventory transfer must be followed by a new observation and verification rather than assumed successful.

## Tests

Run:

```bash
pytest evals/ minecraft/v37_tests.py
```

Add V3.8 controller tests before enabling autonomous inventory interaction on a real world.

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
