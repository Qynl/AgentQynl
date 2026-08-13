# Qynl Agent V3.7

Qynl is a Minecraft-only autonomous AI agent focused on screen-based perception, world-state reasoning, pathfinding, bounded actions, task decomposition, verification and runtime safety.

## V3.7: Gameplay Reliability Update

V3.7 targets the biggest remaining weaknesses from V3.5/V3.6: weak long-horizon task decomposition, fragile navigation, acting on stale perception, and inventory reasoning without evidence.

### New

- perception freshness/confidence policy
- target selection from observed blocks/entities
- camera-aware navigation decisions
- bounded recovery ladder
- common Minecraft goal decomposition
- evidence-based inventory checks
- gameplay regression tests

## Closed loop

```text
SCREEN
  ↓
VISION
  ↓
VALIDATED WORLD STATE
  ↓
FRESHNESS + CONFIDENCE GATE
  ↓
GOAL DECOMPOSITION
  ↓
TARGET SELECTION
  ↓
PATH / CAMERA NAVIGATION
  ↓
SAFETY
  ↓
SHORT ACTION
  ↓
OBSERVE
  ↓
VERIFY
  ↓
PROGRESS / RECOVER / REPLAN
  ↺
```

## Perception reliability

`minecraft/v37_gameplay.py` adds a `PerceptionPolicy` that rejects observations that are either too old or below the configured confidence threshold.

This matters because a screen agent must never treat an old screenshot as if it represented the current Minecraft world.

Default policy:

```text
minimum confidence: 0.55
maximum observation age: 1.0 second
```

These values are configuration defaults, not claims of universal accuracy.

## Target selection

The `TargetSelector` chooses a visible target only when the target has compatible observed metadata and a usable numeric distance.

It does not invent a target's distance or position.

Example:

```text
Goal: collect oak logs
       ↓
visible blocks
       ↓
oak_log candidates
       ↓
nearest valid candidate
       ↓
navigation
```

## Camera-aware navigation

`minecraft/v37_navigation.py` provides a small navigation controller that first attempts to align the camera toward a visible target before moving forward.

```text
target left  → look_left
 target right → look_right
 target above → look_up
 target below → look_down
 aligned      → forward
```

Actions remain bounded and are still passed through the existing safety/action layer.

This is not a replacement for full 3D pathfinding. It is a practical visual-navigation layer between 2D perception and the existing A* system.

## Recovery

`RecoveryPlanner` uses a bounded ladder:

```text
stop
 ↓
look_left
 ↓
look_right
 ↓
back
 ↓
jump
 ↓
reobserve
```

The recovery ladder is deterministic and bounded. Repeated failure is therefore surfaced to the higher-level planner instead of looping forever.

## Task decomposition

`minecraft/v37_tasks.py` adds reusable decomposition for common early-game objectives:

- wood
- crafting table
- stone tools
- food

For example:

```text
crafting table
 ↓
ensure oak logs
 ↓
craft planks
 ↓
craft crafting table
 ↓
verify inventory
```

Unknown goals fall back to a generic observe → identify → plan → act → verify cycle instead of pretending the task is understood.

## Inventory reasoning

`minecraft/v37_inventory.py` only counts an item when the vision state contains a slot with:

- an item identifier
- a count
- sufficient confidence

No invisible inventory slots are fabricated.

## Existing architecture

V3.7 builds on:

```text
V2.6  A* pathfinding
V2.8  production screen/input/world-state adapters
V2.9  hybrid Minecraft vision + optional NIM VLM
V3.5  closed-loop runtime
V3.6  structured Minecraft action language
V3.7  gameplay reliability + task decomposition
```

## Safety

The safety boundary remains mandatory:

```text
AI / VLM
 ↓
structured action
 ↓
confidence + freshness
 ↓
safety supervisor
 ↓
bounded action controller
 ↓
Minecraft
```

The V3.7 gameplay layer does not grant arbitrary keyboard/mouse access and does not bypass emergency stop.

## What V3.7 improves

### Basic navigation

Better because Qynl can select observed targets, align the camera, move in bounded steps and recover when progress stops.

### Long tasks

Better because common goals are decomposed into verifiable subtasks instead of being treated as one giant instruction.

### Inventory

Better because inventory claims now require visual evidence.

### Vision mistakes

Safer because stale or low-confidence observations can be rejected before action selection.

### Stuck situations

Better because recovery is explicit and bounded.

## Important limitations

V3.7 still cannot guarantee perfect Minecraft play from screenshots alone. Exact 3D localization, hidden terrain, complex inventories, crafting grids, combat, physics and long-horizon survival remain difficult perception/planning problems.

The architecture intentionally handles uncertainty by observing again, recovering, or escalating rather than fabricating state.

## Test

Run the existing test suite plus:

```bash
pytest evals/ minecraft/v37_tests.py
```

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
