# Qynl Agent V2.8

Qynl is a **Minecraft-only autonomous AI agent** with visual perception, temporal state, hierarchical planning, persistent world state, verified learning, mission-level autonomy, recovery, typed actions, deterministic evaluation and explicit runtime safety.

## V2.8: Production Minecraft Vision

V2.8 now contains the production adapter boundary **and a Minecraft-focused vision layer**. Screen frames can be passed through deterministic CV for cheap, explainable geometry signals and through an optional semantic vision backend for richer scene understanding.

### V2.8 additions

- production screen-capture interface
- optional MSS screen backend
- optional PyAutoGUI input backend
- Minecraft crosshair detection hint
- Minecraft HUD region extraction
- hotbar/health/food region metadata
- inventory-region metadata
- structured block/entity detection schema
- optional semantic vision backend interface
- strict vision-result validation
- temporal world-state delta tracking
- emergency-stop propagation
- adapter and vision regression tests

## Real-session architecture

```text
MINECRAFT WINDOW
      ↓
SCREEN CAPTURE
      ↓
┌──────────────────────────────┐
│ Minecraft Vision              │
│                              │
│ deterministic CV + model CV │
└──────────────┬───────────────┘
               ↓
       VALIDATED WORLD STATE
               ↓
       TEMPORAL STATE TRACKER
               ↓
       MISSION / PLAN / PATHFIND
               ↓
          V30 / V31 / V50
               ↓
       PRODUCTION INPUT
               ↓
        KEYBOARD / MOUSE
               ↓
           MINECRAFT
               ↓
          NEW FRAME ↺
```

The core rule remains: **the model can propose; the runtime decides.**

## Minecraft vision

`minecraft/v28_minecraft_vision.py`

`MinecraftVision` is the deterministic baseline. It extracts information that can be justified from pixels and deliberately leaves information unknown when a screenshot cannot establish it reliably.

### Crosshair

The detector inspects the center of the frame for a high-contrast crosshair hint and returns its pixel location and confidence.

This is a **hint**, not a guarantee that the server/client uses the vanilla crosshair.

### HUD

The baseline provides Minecraft-oriented regions for:

- hotbar
- health
- food

These are geometry signals. Exact hearts, hunger values, item names and counts require a semantic/UI recognition backend.

### Inventory

The baseline exposes the expected center inventory region but returns `open: null` until a classifier/model can actually establish whether an inventory screen is open.

### Player position

A screenshot alone does **not** provide authoritative 3D world coordinates. V2.8 therefore returns:

```text
position = null
yaw = null
pitch = null
```

until a world-state/depth backend supplies them. Qynl does not fabricate coordinates from a 2D image.

## Semantic vision backend

`minecraft/v28_vision_backends.py`

The runtime accepts a small injectable interface:

```python
image + system_prompt → structured JSON
```

The backend must return:

```text
confidence
player
visible_blocks
entities
ui
```

`validate_vision_result()` rejects malformed or unsafe schema output before it becomes trusted state.

This makes the vision provider replaceable. A local model, NVIDIA-backed vision service, or another compatible provider can be connected without changing the Minecraft runtime.

## Production adapter

`minecraft/v28_production_adapter.py`

Defines:

```text
ScreenCapture
MinecraftInput
VisionBackend
```

The adapter now validates every vision result before producing `WorldState`.

## World-state extraction

`minecraft/v28_world_state.py`

Consecutive observations produce:

```text
position_changed
visible_block_count_delta
entity_count_delta
```

This lets the planner reason over change instead of treating every screenshot as an isolated image.

## Reference desktop backends

`minecraft/v28_backends.py`

- `MSSScreenCapture` for desktop capture
- `PyAutoGUIInput` for keyboard/mouse transport

These are transport adapters. They do not pretend to solve Minecraft semantics themselves.

## Safety boundary

```text
AI / memory / learning
        ↓
candidate decision
        ↓
typed Minecraft action
        ↓
confidence + freshness
        ↓
V30 decision gate
        ↓
V31 validator
        ↓
V50 safety supervisor
        ↓
V22 pacing guard
        ↓
watchdog / Force ESC
        ↓
Production Input Adapter
        ↓
Minecraft
```

Vision, pathfinding and world-state extraction cannot bypass execution safety.

## Safe real-Minecraft workflow

```text
1. Dedicated test world
2. Dry-run
3. Verify screen capture
4. Verify deterministic CV
5. Verify semantic vision + schema
6. Verify world-state deltas
7. Test Force ESC
8. Short bounded real sessions
9. Inspect traces and verification
10. Increase autonomy gradually
```

Do not run an untested adapter unattended.

## Tests

- `evals/test_v28_adapters.py`
- `evals/test_v28_vision.py`

Coverage includes adapter observations, emergency stop, malformed vision output, temporal state changes and semantic backend validation.

## Versioning

```text
V2.0 = V50 architecture baseline
V2.1 = observation + feedback reliability
V2.2 = debugability + progress measurement + pacing
V2.5 = gameplay reliability + navigation/recovery foundations
V2.6 = pathfinding + navigation feedback
V2.7 = usable runtime boundary
V2.8 = production adapters + Minecraft vision
V3.0 = only for a genuinely major architectural change
```

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

Install the repository dependencies. For the vision baseline, install the optional packages from `requirements-vision.txt`.

For the TSX desktop app:

```bash
cd apps/desktop
npm install
npm run dev
```

## Limitations

V2.8 is now a real screen-to-structured-state foundation, but it does **not** claim perfect Minecraft perception. Exact 3D coordinates, block identity, entity identity, health values, inventory contents and semantic interactions require a trained/connected vision backend or game-state source.

The architecture intentionally follows:

**observe → validate → decide → safely act → observe again**

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
