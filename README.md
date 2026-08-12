# Qynl Agent V2.7

Qynl is a **Minecraft-only autonomous AI agent** with visual perception, temporal state, hierarchical planning, persistent world state, verified learning, mission-level autonomy, recovery, typed actions, deterministic evaluation and explicit runtime safety.

## V2.7: Usable Minecraft Runtime

V2.7 turns the V2.6 navigation primitives into a bounded runtime loop that can be wired to a real Minecraft input adapter. The release focuses on the practical boundary between AI decisions and actual Minecraft control.

### V2.7 additions

- practical runtime controller
- injectable Minecraft input adapter
- bounded observe → decide → execute → verify session loop
- low-confidence input suppression
- runtime pause/resume
- emergency-stop integration
- movement verification
- navigation-stall handling
- runtime regression tests

## Core control loop

```text
MINECRAFT
    ↓
OBSERVE
    ↓
CONFIDENCE CHECK
    ↓
WORLD STATE
    ↓
MISSION / GOAL
    ↓
PLAN + PATHFIND
    ↓
TRACE DECISION
    ↓
SAFETY
    ↓
EXECUTE ONE STEP
    ↓
FRESH OBSERVATION
    ↓
VERIFY
    ↓
PROGRESS / STUCK CHECK
    ↓
CONTINUE / REOBSERVE / REPLAN / STOP
```

The core rule remains: **the model can propose; the runtime decides.**

## V2.7 runtime

`minecraft/v27_runtime.py`

`MinecraftRuntime` provides the execution boundary. It accepts an injected `InputAdapter` instead of directly depending on a keyboard/mouse library.

The adapter must provide:

```text
move(dx, dy, dz)
stop()
emergency_stop()
```

This keeps the AI/planning layer separate from real input and makes the runtime testable without controlling a real Minecraft window.

### Low-confidence behavior

If observation confidence falls below the runtime threshold, Qynl returns:

```text
reobserve
```

and does not generate movement input.

### Emergency stop

`emergency_stop()` pauses the runtime and forwards the stop request to the adapter. While paused, decisions are `stop` until an explicit resume occurs.

## Bounded session loop

`minecraft/v27_session.py`

The session controller repeatedly:

1. obtains a fresh observation
2. makes one bounded decision
3. executes at most one navigation step
4. obtains another observation
5. verifies movement
6. continues, replans or stops

A maximum step budget prevents an unattended session loop from running forever.

## Pathfinding

V2.7 uses the V2.6 navigation stack:

```text
World observation
      ↓
bounded A*
      ↓
path scoring
      ↓
next path node
      ↓
V50 safety
      ↓
input adapter
```

The path is never blindly executed as one giant command. Minecraft is dynamic, so every step is followed by fresh observation.

## Tests

`evals/test_v27.py` verifies:

- low confidence produces no movement decision
- runtime uses bounded pathfinding
- emergency stop pauses the runtime

The V2.6 regression suite remains part of the project as well.

## Real Minecraft setup

V2.7 provides the runtime boundary, but **the repository is not claiming plug-and-play autonomous Minecraft gameplay yet**. To use it in a real session, a deployment still needs:

- a reliable screen/vision observer
- a Minecraft-aware `InputAdapter`
- model/provider configuration
- world-state extraction
- environment-aware movement handling
- the existing V30/V31/V50 safety stack

Start with a dedicated test world and dry-run mode. Do not connect a new input adapter directly to an unattended survival world before it has passed deterministic and short-session tests.

## Versioning

V50 remains the major architecture milestone. The public product line continues from V2.0.

```text
V2.0 = V50 architecture baseline
V2.1 = observation + feedback reliability
V2.2 = debugability + progress measurement + pacing
V2.5 = gameplay reliability + navigation/recovery foundations
V2.6 = pathfinding + navigation feedback
V2.7 = usable runtime boundary
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

Install the dependencies specified by the repository's dependency files.

For the TSX desktop app:

```bash
cd apps/desktop
npm install
npm run dev
```

Use the scripts in `apps/desktop/package.json` if the project defines different commands.

## Safe first run

Start with:

```text
QYNL_DRY_RUN=1
```

Then verify capture, perception, planning, pathfinding, action validation, navigation, recovery, watchdog, Force ESC, missions, telemetry and V50 safety before enabling real Minecraft input.

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
Input Adapter
        ↓
Minecraft
```

Planning, pathfinding and recovery do not bypass execution validation or the safety supervisor.

## Project structure

```text
AgentQynl/
├── apps/desktop/
├── core/
├── minecraft/
│   ├── v20_*.py
│   ├── v21_*.py
│   ├── v22_*.py
│   ├── v23_*.py
│   ├── v24_*.py
│   ├── v25_*.py
│   ├── v26_*.py
│   ├── v27_*.py
│   ├── v30_*.py
│   ├── v31_*.py
│   ├── v50_*.py
│   └── executor.py
├── memory/
├── safety/
├── evals/
└── docs/
```

## Limitations

V2.7 makes the core runtime practical to integrate, but it does not claim human-level Minecraft gameplay or fully solve vision, combat, inventory management, crafting, terrain physics or arbitrary-world navigation. Those capabilities require their own tested Minecraft-specific systems.

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
