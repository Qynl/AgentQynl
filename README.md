# Qynl Agent V2.6

Qynl is a **Minecraft-only autonomous AI agent** with visual perception, temporal state, hierarchical planning, persistent world state, verified learning, mission-level autonomy, recovery, typed actions, deterministic evaluation and explicit runtime safety.

## V2.6: Pathfinding + Navigation Intelligence

V2.6 is the navigation-focused release. It adds a bounded A* pathfinding primitive, path scoring, navigation-step generation and stuck detection while keeping the V50 safety architecture underneath execution.

### V2.6 additions

- bounded 3D A* pathfinding
- blocked-cell avoidance
- expansion limits
- path length/risk scoring
- path-to-navigation-step bridge
- navigation stall detection
- expanded Minecraft regression tests

## Core control loop

```text
MINECRAFT
    ↓
OBSERVE
    ↓
STATE / WORLD MODEL
    ↓
MISSION
    ↓
PLAN
    ↓
PATHFIND
    ↓
SCORE PATH
    ↓
TRACE DECISION
    ↓
SAFETY
    ↓
PACE ACTION
    ↓
EXECUTE
    ↓
VERIFY
    ↓
STUCK CHECK
    ↓
PROGRESS
    ↓
LEARN / RECOVER / REPLAN
```

The core rule remains: **the model can propose; the runtime decides.**

## V2.6 components

### Bounded A* pathfinding

`minecraft/v26_pathfinding.py`

The new pathfinder searches a discrete 3D grid using A* and a configurable expansion budget.

```text
start
  ↓
known blocked cells
  ↓
A*
  ↓
path / failure
```

The expansion limit is deliberate. A bad or huge path request cannot consume unbounded compute.

### Path navigation

`minecraft/v26_navigation.py`

Converts a planned path into the next bounded navigation step. The path planner does not directly bypass the existing executor or safety layers.

### Stuck detection

`minecraft/v26_stuck_detector.py`

Tracks repeated observations with no movement and signals when navigation has stalled.

The detector does not issue input itself. It feeds the existing recovery/replanning system.

### Path scoring

`minecraft/v26_path_cost.py`

Provides a small scoring primitive based on path length and bounded risk. This lets higher-level planning compare candidate routes rather than blindly selecting the first valid route.

## V2.6 navigation architecture

```text
           WORLD OBSERVATION
                  ↓
          ┌───────────────┐
          │ World / State │
          └───────┬───────┘
                  ↓
          ┌───────────────┐
          │   A* Search   │
          └───────┬───────┘
                  ↓
             candidate paths
                  ↓
          ┌───────────────┐
          │ Path Scoring  │
          └───────┬───────┘
                  ↓
            selected route
                  ↓
          ┌───────────────┐
          │ Next Nav Step │
          └───────┬───────┘
                  ↓
             SAFETY STACK
                  ↓
              EXECUTION
                  ↓
              VERIFY
             ↙       ↘
          moved      stalled
            ↓           ↓
         continue    recover/replan
```

## Important limitation

V2.6's pathfinder is a **planning primitive**, not a finished Minecraft movement controller.

Real Minecraft navigation still needs environment-aware handling for things such as:

- collision geometry
- jumping and falling
- terrain height changes
- water and lava
- ladders and climbing
- doors and interactable blocks
- dynamic entities
- newly discovered obstacles
- path invalidation after world changes

The correct architecture is therefore **plan → execute one bounded step → observe → verify → replan**, rather than blindly executing an entire path.

## Tests

`evals/test_v26.py` covers both existing V2.6 mission/recovery behavior and the new navigation layer:

- A* routes around blocked cells
- A* respects its expansion budget
- navigation selects the next path node
- stuck detector triggers after repeated no-progress observations
- path-risk values are bounded
- mission lifecycle
- verified mission memory
- recovery escalation

## Versioning

V50 remains the major architecture milestone. The public product line continues from V2.0.

```text
V2.0 = V50 architecture baseline
V2.1 = observation + feedback reliability
V2.2 = debugability + progress measurement + pacing
V2.5 = gameplay reliability + navigation/recovery foundations
V2.6 = pathfinding + navigation feedback
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

Start in dry-run mode:

```text
QYNL_DRY_RUN=1
```

Then verify capture, perception, planning, pathfinding, action validation, navigation, recovery, watchdog, Force ESC, missions, telemetry and V50 safety before enabling real Minecraft input.

Use a dedicated test world for early sessions.

## Testing philosophy

```text
change
 ↓
unit tests
 ↓
deterministic benchmark
 ↓
dry run
 ↓
short real mission
 ↓
measure
 ↓
fix
 ↓
repeat
```

Benchmarks are regression barriers, not proof of human-level Minecraft gameplay.

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
Minecraft
```

Pathfinding, navigation and recovery can recommend what should happen next, but they do not bypass execution validation or the safety supervisor.

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

V2.6 significantly improves navigation planning, but it does not claim arbitrary-terrain autonomous Minecraft movement. Real performance still depends on perception quality, world-state accuracy, model quality, latency, input handling and reliable verification.

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
