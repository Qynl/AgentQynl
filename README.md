# Qynl Agent V3.6

Qynl is a **Minecraft-only autonomous AI agent** built around screen perception, semantic vision, temporal state, hierarchical planning, pathfinding, a rich typed action language, verification, recovery and explicit runtime safety.

## V3.6: Full Minecraft Action Layer

V3.6 expands the tiny V3.5 action set into a much more useful Minecraft control vocabulary and gives the planner a structured action schema.

### Action vocabulary

```text
MOVEMENT
forward, back, left, right
jump, sprint, sneak

COMBAT / INTERACTION
attack, use, pick_block

INVENTORY / ITEMS
inventory, drop_item, swap_hands
hotbar_1 ... hotbar_9
hotbar_next, hotbar_prev

UI
chat, pause

CAMERA
look(dx, dy)
look_left, look_right, look_up, look_down

CONTROL
stop
```

This is intentionally much richer than the previous 11-action vocabulary.

## Structured actions

`minecraft/v36_action_schema.py` converts planner/VLM JSON into a validated `ActionCommand`.

Example:

```json
{
  "action": "forward",
  "duration_ms": 120
}
```

Camera action:

```json
{
  "action": "look",
  "dx": 90,
  "dy": -20
}
```

Unknown actions are rejected before they reach the desktop adapter.

## Bounded control

All actions remain bounded.

- movement duration is clamped
- camera movement is clamped
- keyboard actions use press/release cleanup
- attack/use release the mouse button in `finally`
- `stop()` releases movement keys
- the existing Force ESC / watchdog / safety layers remain above the adapter

The model still cannot emit arbitrary OS key names.

## Real control pipeline

```text
                  SCREEN
                    ↓
              Minecraft Vision
                    ↓
              World State
                    ↓
           Memory / Progress
                    ↓
        Goal + Planner + A*
                    ↓
            ActionCommand
                    ↓
          Schema Validation
                    ↓
          Safety Supervisor
                    ↓
        Bounded ActionController
                    ↓
       Keyboard / Mouse Adapter
                    ↓
                 MINECRAFT
                    ↓
                 OBSERVE
                    ↺
```

## Production mouse wheel

The production input contract now includes `scroll(clicks)`, and the PyAutoGUI backend implements it. Hotbar scrolling therefore uses the real mouse wheel path instead of pretending a wheel event is a mouse button.

## Why this matters

A Minecraft agent needs more than WASD.

For example, a simple task such as:

> Find a tree, approach it, look at a log, break it, collect the item, open inventory, craft planks, and continue.

requires combinations of:

```text
look
forward
jump
attack
use
hotbar selection
inventory
camera correction
stop
```

V3.6 provides the action vocabulary needed to represent those behaviors. Higher-level gameplay policies decide **when** to use them.

## Safety boundary

```text
AI / VLM proposal
      ↓
Action schema
      ↓
confidence + freshness
      ↓
V30 Gate
      ↓
V31 Validator
      ↓
V50 Supervisor
      ↓
V22 pacing
      ↓
Force ESC / watchdog
      ↓
ActionController
      ↓
Minecraft
```

The action vocabulary does not bypass these layers.

## Version history

```text
V2.0 = V50 architecture baseline
V2.1 = observation + feedback reliability
V2.2 = debugability + progress measurement + pacing
V2.5 = gameplay reliability + recovery foundations
V2.6 = bounded A* pathfinding
V2.7 = runtime boundary
V2.8 = production screen/input/world-state adapters
V2.9 = hybrid Minecraft vision + NIM
V3.5 = closed-loop playable runtime
V3.6 = full typed Minecraft action layer
```

## Tests

The V3.5 tests remain the regression suite for goal tracking, action clamping and verification. The V3.6 schema is intentionally small and deterministic so planner output can be validated before execution.

## Installation

```bash
git clone https://github.com/Qynl/AgentQynl.git
cd AgentQynl
python -m venv .venv
```

Windows:

```bash
.venv\\Scripts\\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

For the desktop application:

```bash
cd apps/desktop
npm install
npm run dev
```

## Limitations

The action vocabulary is now broad enough to represent normal Minecraft interaction, but an action vocabulary alone does not create gameplay intelligence. Reliable Minecraft play still depends on accurate vision, state estimation, task planning, physics-aware movement, inventory/crafting policies and repeated verification.

When perception is uncertain, the agent should observe again instead of inventing state.

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
