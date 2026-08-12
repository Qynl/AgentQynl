# Qynl Agent V2.5

Qynl is a **Minecraft-only autonomous AI agent** with visual perception, temporal state, hierarchical planning, persistent world state, verified learning, mission-level autonomy, recovery, typed actions, deterministic evaluation and explicit runtime safety.

## V2.5: Gameplay Reliability Update

V2.5 builds on the V50 architecture and the V2.1/V2.2 reliability work. This release focuses on practical Minecraft behavior: navigation targets, bounded recovery and better regression testing.

### V2.5 additions

- bounded waypoint navigation helper
- explicit arrival detection
- confidence-aware recovery
- mission-regression recovery
- bounded retry budgets
- Minecraft-specific regression tests

## Core control loop

```text
MINECRAFT
    ↓
OBSERVE
    ↓
STATE
    ↓
MISSION
    ↓
PLAN
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
TRACK PROGRESS
    ↓
NAVIGATE / RECOVER / REPLAN
    ↓
LEARN
```

The core rule remains: **the model can propose; the runtime decides.**

## V2.5 components

### Navigation

`minecraft/v25_navigation.py`

V2.5 introduces a small deterministic navigation layer for waypoint-based tasks.

A waypoint contains:

- X coordinate
- Y coordinate
- Z coordinate
- optional name

The navigator calculates distance and distinguishes between:

```text
arrived
move_to_waypoint
```

This is intentionally a navigation primitive, not a claim that Qynl can already pathfind perfectly around arbitrary Minecraft terrain. Higher-level pathfinding can build on it.

### Recovery policy

`minecraft/v25_recovery.py`

Recovery now considers three signals:

- consecutive action failures
- mission progress regression
- perception confidence

Possible decisions are:

```text
continue
retry_once
replan
reobserve
```

A bounded retry budget prevents an agent from repeating a failed action forever.

### Tests

`evals/test_v25.py` covers:

- waypoint arrival
- distant waypoint handling
- low-confidence recovery
- progress-regression replanning
- retry-budget exhaustion

## Versioning

V50 remains the major architecture milestone. The public product line continues from V2.0 without carrying the old V50 number into every release.

```text
V2.0 = V50 architecture baseline
V2.1 = observation + feedback reliability
V2.2 = debugability + progress measurement + pacing
V2.5 = gameplay reliability + navigation + recovery
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

Then verify capture, perception, planning, action validation, navigation, recovery, watchdog, Force ESC, missions, telemetry and V50 safety before enabling real Minecraft input.

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

Navigation and recovery can recommend what should happen next, but they do not bypass the safety supervisor or execution validation.

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

V2.5 improves navigation and recovery primitives. It does not by itself guarantee strong autonomous Minecraft gameplay or solve arbitrary terrain pathfinding. Real performance still depends on perception quality, model quality, latency, input handling and reliable verification.

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
