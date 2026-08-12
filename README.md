# Qynl Agent V2.2

Qynl is a **Minecraft-only autonomous AI agent** with visual perception, temporal state, hierarchical planning, persistent world state, verified learning, mission-level autonomy, recovery, typed actions, deterministic evaluation and explicit runtime safety.

## V2.2: Debuggable, Measurable Runtime

V2.2 builds on the V50 architecture and V2.1 reliability work. The goal is not another rewrite. It makes Qynl's decisions easier to inspect, mission progress easier to measure, and action execution more deliberately paced.

### V2.2 additions

- bounded decision traces
- mission progress regression detection
- action pacing guard
- expanded regression coverage

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
LEARN / RECOVER / REPLAN
```

The core rule remains: **the model can propose; the runtime decides.**

## V2.2 components

### Decision traces

`minecraft/v22_decision_trace.py`

Stores a bounded history of chosen action, confidence, short reason and timestamp. This makes long-session debugging practical without allowing an unbounded in-memory log.

### Mission progress tracker

`minecraft/v22_progress_tracker.py`

Normalizes mission progress to `[0, 1]`, calculates change since the previous observation, and flags meaningful regressions. A regression is a signal for verification/recovery, not automatic proof that the world is broken.

### Action pacing

`minecraft/v22_action_cooldown.py`

Adds a small configurable minimum interval between action marks to reduce runaway input loops. This is a pacing guard, not a substitute for the V30/V31/V50 safety layers.

## Versioning

V50 remains the major architecture milestone. V2.1 and V2.2 are the new product/versioning line built on that architecture.

```text
V2.0 = V50 architecture baseline
V2.1 = observation + feedback reliability
V2.2 = debugability + progress measurement + pacing
V2.3 = next incremental improvement
...
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

Then install the dependencies specified by the repository's dependency files.

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

Then verify capture, perception, planning, action validation, watchdog, Force ESC, missions, telemetry and V50 safety before enabling real Minecraft input.

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

Learning and memory do not bypass execution safety.

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

V2.2 improves observability and runtime discipline. It does not by itself guarantee strong autonomous Minecraft gameplay. Real performance still depends on perception quality, model quality, latency, input handling and reliable verification.

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
