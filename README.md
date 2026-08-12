# Qynl Agent V2.8

Qynl is a **Minecraft-only autonomous AI agent** with visual perception, temporal state, hierarchical planning, persistent world state, verified learning, mission-level autonomy, recovery, typed actions, deterministic evaluation and explicit runtime safety.

## V2.8: Production Adapter Layer

V2.8 adds the production boundary between the agent and a real Minecraft desktop session: screen capture, vision analysis, keyboard/mouse input, and temporal world-state extraction are now represented by explicit interfaces.

The design deliberately keeps platform-specific dependencies outside the AI core.

### V2.8 additions

- production screen-capture interface
- optional MSS screen backend
- optional PyAutoGUI input backend
- strict vision-result schema validation
- structured world-state extraction
- temporal world-state delta tracking
- emergency-stop propagation
- bounded key tap duration
- adapter regression tests

## Real-session architecture

```text
MINECRAFT WINDOW
      ↓
SCREEN CAPTURE
      ↓
VISION BACKEND
      ↓
VALIDATED WORLD STATE
      ↓
TEMPORAL STATE TRACKER
      ↓
MISSION / PLAN / PATHFIND
      ↓
V30 / V31 / V50 SAFETY
      ↓
PRODUCTION INPUT ADAPTER
      ↓
KEYBOARD / MOUSE
      ↓
MINECRAFT
      ↓
NEW SCREEN FRAME
      ↺
```

The core rule remains: **the model can propose; the runtime decides.**

## Production adapter

`minecraft/v28_production_adapter.py`

Defines three injected interfaces:

```text
ScreenCapture
MinecraftInput
VisionBackend
```

The `ProductionAdapter` turns them into a structured `WorldState` and exposes controlled input primitives.

### Screen

A `ScreenFrame` contains:

- image/frame object
- monotonic timestamp
- width
- height

Timestamps are checked so stale/out-of-order frames cannot silently become the newest world state.

### Vision

The vision backend returns:

```text
confidence
player
visible_blocks
entities
ui
```

Confidence is bounded to `[0, 1]` before entering the runtime.

### Input

The input interface supports:

```text
key_down()
key_up()
mouse_move()
mouse_button()
emergency_stop()
```

`stop()` releases the movement keys used by the adapter. `emergency_stop()` additionally forwards the emergency-stop event to the backend.

## Reference desktop backends

`minecraft/v28_backends.py`

### MSS

`MSSScreenCapture` uses the optional `mss` package for desktop capture. The dependency is imported lazily, so installations that do not use this backend do not need to import it.

### PyAutoGUI

`PyAutoGUIInput` uses the optional `pyautogui` package for keyboard/mouse control. It tracks pressed keys so emergency stop can release them.

PyAutoGUI's failsafe is enabled by the adapter.

These are **reference transport adapters**, not a claim that every Minecraft version/window configuration is automatically solved.

## World-state extraction

`minecraft/v28_world_state.py`

`WorldStateTracker` compares consecutive observations and produces a compact delta:

```text
position_changed
visible_block_count_delta
entity_count_delta
```

This gives the planner/runtime a temporal signal rather than treating every screenshot as an isolated image.

## Vision schema validation

`minecraft/v28_vision_schema.py`

Vision output is checked before entering the world-state layer.

Invalid results are rejected when:

- the result is not a mapping
- required fields are missing
- confidence is outside `[0, 1]`
- blocks/entities are not sequences
- player/UI are not mappings

This prevents malformed model output from becoming trusted runtime state.

## Safe real-Minecraft workflow

```text
1. Start Minecraft in a dedicated test world
2. Start Qynl in dry-run mode
3. Verify screen capture
4. Verify vision output + confidence
5. Verify world-state extraction
6. Verify keyboard/mouse adapter without autonomous actions
7. Test Force ESC / emergency stop
8. Run short bounded sessions
9. Inspect traces and verification results
10. Only then enable autonomous input
```

Do not run an untested adapter unattended.

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

Screen capture, vision, world-state extraction and input adapters do not bypass the safety supervisor.

## Tests

`evals/test_v28_adapters.py` verifies:

- production observations are converted into structured state
- emergency stop propagates
- invalid vision confidence is rejected
- temporal position changes are detected

## Versioning

```text
V2.0 = V50 architecture baseline
V2.1 = observation + feedback reliability
V2.2 = debugability + progress measurement + pacing
V2.5 = gameplay reliability + navigation/recovery foundations
V2.6 = pathfinding + navigation feedback
V2.7 = usable runtime boundary
V2.8 = production screen/input/world-state adapters
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

Install the repository dependencies. If you use the reference desktop adapters, install their optional packages as documented by the project.

For the TSX desktop app:

```bash
cd apps/desktop
npm install
npm run dev
```

## Limitations

V2.8 provides the real desktop integration boundary, but it does **not** claim perfect Minecraft perception or gameplay. A vision model still has to reliably infer Minecraft state from frames, and Minecraft-specific movement, combat, inventory, crafting and interaction policies still need dedicated tested implementations.

The production architecture is intentionally incremental: observe → validate → decide → safely act → observe again.

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
