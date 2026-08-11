# Qynl Agent V50

Qynl is a **Minecraft-only autonomous AI agent** with visual perception, temporal state, hierarchical planning, persistent world state, verified learning, mission-level autonomy, recovery, typed actions, deterministic evaluation and an explicit runtime safety architecture.

## V50: Architecture Reset

V50 is the largest architectural update so far. Instead of continuing to bolt features onto the agent, V50 introduces explicit runtime primitives and connects them around a single control loop.

```text
MINECRAFT
    ↓
OBSERVATION BUFFER
    ↓
WORLD / STATE MODEL
    ↓
MISSION ENGINE
    ↓
PLANNER + MODEL
    ↓
TYPED MINECRAFT ACTION
    ↓
INDEPENDENT SAFETY SUPERVISOR
    ↓
INPUT ADAPTER
    ↓
MINECRAFT
    ↓
VERIFY
    ↓
MEMORY + LEARNING
    ↓
REPLAN
```

The critical rule remains: **the model can propose; the runtime decides.**

## What V50 adds

### 1. Explicit agent state machine

`minecraft/v50_agent_state.py`

Qynl now has explicit states:

```text
BOOT → OBSERVE → THINK → ACT → VERIFY
                    ↑             ↓
                    └── RECOVER ──┘

PAUSED / COMPLETE / ABORTED
```

Invalid state transitions are rejected instead of silently accepted.

### 2. Event-driven runtime

`minecraft/v50_event_bus.py`

A bounded deterministic event bus lets components communicate through explicit events such as:

```text
runtime.started
observation.updated
mission.started
action.proposed
action.rejected
action.executed
action.verified
mission.completed
runtime.emergency_stop
```

### 3. Temporal observation buffer

`minecraft/v50_observation_buffer.py`

Qynl now retains a bounded sequence of recent observations with:

- frame ID
- interpreted state
- confidence
- timestamp

This gives the higher-level system temporal context rather than forcing every decision to depend on one screenshot.

### 4. Bounded typed memory

`minecraft/v50_memory_store.py`

Memory is explicitly namespaced and bounded. Entries contain a key, value, confidence and timestamp.

Example namespaces:

```text
world
mission
skill
session
```

The memory layer is deliberately replaceable. It is storage, not a magical second brain.

### 5. Mission engine

`minecraft/v50_mission_engine.py`

Missions now have a deterministic lifecycle and explicit subtask progress.

Example:

```text
Mission: survive first night

[✓] collect wood
[✓] craft tools
[ ] find food
[ ] build shelter
[ ] survive night
```

### 6. Independent safety supervisor

`minecraft/v50_safety_supervisor.py`

Safety is separated from planning.

The supervisor can reject actions because of:

- emergency stop
- action-duration limits
- stale state
- low confidence
- repeated verification failures

Repeated failures can force an emergency stop.

The model cannot override the supervisor.

### 7. Integrated runtime

`minecraft/v50_runtime.py` connects the state machine, event bus, observation buffer and safety supervisor and provides an explicit emergency-stop path.

### 8. System integration tests

`evals/test_v50.py` covers:

- invalid state transitions
- event dispatch
- bounded memory
- mission completion
- safety failure budgets
- bounded observations
- integrated emergency stop

## V50 control loop

```text
┌──────────────────────┐
│      OBSERVE         │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  UPDATE WORLD STATE  │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  CHECK MISSION       │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  PLAN NEXT ACTION    │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  SAFETY SUPERVISOR   │──── reject ───→ REOBSERVE / RECOVER
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  EXECUTE ONE ACTION  │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  VERIFY RESULT       │
└───────┬────────┬─────┘
        │        │
     success   failure
        │        │
        ↓        ↓
     LEARN    RECOVER
        │        │
        └───┬────┘
            ↓
          REPLAN
```

## Serious real-session workflow

### 1. Download

```bash
git clone https://github.com/Qynl/AgentQynl.git
cd AgentQynl
```

Or download the repository ZIP from GitHub.

### 2. Install

At minimum:

- Python for the backend
- Node.js + npm for the TSX desktop app
- Minecraft Java Edition
- Git if cloning
- the Minecraft version/configuration supported by the repository

```bash
python -m venv .venv

# Windows
.venv\\Scripts\\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt

cd apps/desktop
npm install
cd ../..
```

Follow repository dependency files if they specify different commands.

### 3. Configure provider

Keep credentials in environment configuration. Never hard-code or commit API keys.

Start with:

```text
QYNL_DRY_RUN=1
```

### 4. Start Minecraft

Use a dedicated test world. Humanity invented civilization and then taught a computer to punch trees, so give it a sandbox.

### 5. Dry-run verification

Verify:

- capture
- perception
- temporal observations
- world model
- goals/subtasks
- planning
- V31 action validation
- V30 decision gate
- V23 learning
- V26 missions
- V24 runtime
- V50 safety supervisor
- Force ESC
- watchdog

No real input should execute in dry-run mode.

### 6. First real mission

Only after the safety checks pass, enable real input using the configuration supported by the current runtime.

Start with objectively verifiable goals:

```text
Collect 16 logs
Craft a stone pickaxe
Build a shelter
Reach a specified location
```

Do not begin with an undefined objective like `play Minecraft well`.

### 7. Monitor

During early real sessions monitor:

```text
Mission status
Progress
Current subtask
Current state
Current decision
Current action
Verification result
Confidence
Safety state
Recovery state
Learning events
Runtime health
```

Keep early real sessions supervised.

## Desktop App

The TSX desktop application is intended to be the operator interface when the current build supports the required backend controls.

Typical development startup:

```bash
cd apps/desktop
npm install
npm run dev
```

Use the scripts defined by `apps/desktop/package.json` if they differ.

Recommended workflow:

```text
Open Qynl Desktop
 ↓
Provider
 ↓
Minecraft capture
 ↓
Safety check
 ↓
DRY RUN
 ↓
Run tests / benchmarks
 ↓
Observe
 ↓
Create mission
 ↓
Start
 ↓
Monitor runtime
 ↓
Pause / Abort / Force ESC
 ↓
Review mission result
```

## Version evolution

```text
V13  Temporal awareness
 ↓
V14  Tasks + evaluation + skill memory
 ↓
V15  Shared state + watchdog + verification
 ↓
V16  Recovery + adaptive memory + rate limiting
 ↓
V20  Persistent world model + utility planning
 ↓
V21  Prediction + spatial memory + exploration
 ↓
V22  Goal hierarchy + short-horizon planning + replanning
 ↓
V23  Verified learning + capability + progressive curriculum
 ↓
V24  Real-time runtime + guarded execution + telemetry
 ↓
V26  Long-running missions + structured mission memory + recovery
 ↓
V30  Typed contracts + decision gate + health + deterministic benchmarks
 ↓
V31  Strict actions + state freshness + execution validation
 ↓
V50  Unified runtime architecture + mission + memory + eventing + safety supervisor
```

## Project structure

```text
AgentQynl/
├── apps/desktop/
├── core/
├── minecraft/
│   ├── real_capture.py
│   ├── observation.py
│   ├── vision.py
│   ├── providers.py
│   ├── planner.py
│   ├── goals.py
│   ├── v20_world_model.py
│   ├── v20_planner.py
│   ├── v21_spatial_memory.py
│   ├── v21_exploration.py
│   ├── v21_predictor.py
│   ├── v22_goal_monitor.py
│   ├── v22_action_sequence.py
│   ├── v22_subtasks.py
│   ├── v22_replan.py
│   ├── v23_skill_learner.py
│   ├── v23_episode.py
│   ├── v23_curriculum.py
│   ├── v23_capability.py
│   ├── v24_realtime_runtime.py
│   ├── v24_task_executor.py
│   ├── v24_session.py
│   ├── v26_mission_control.py
│   ├── v26_mission_memory.py
│   ├── v26_recovery.py
│   ├── v30_contracts.py
│   ├── v30_decision_gate.py
│   ├── v30_health.py
│   ├── v30_benchmark.py
│   ├── v31_action_schema.py
│   ├── v31_state_estimator.py
│   ├── v31_action_validator.py
│   ├── v50_event_bus.py
│   ├── v50_agent_state.py
│   ├── v50_memory_store.py
│   ├── v50_mission_engine.py
│   ├── v50_safety_supervisor.py
│   ├── v50_observation_buffer.py
│   ├── v50_runtime.py
│   ├── executor.py
│   └── input_adapter.py
├── memory/
├── safety/
├── evals/
└── docs/
    ├── V22.md
    ├── V23.md
    ├── V24.md
    ├── V26.md
    ├── V30.md
    └── V50.md
```

## Testing philosophy

V50 changes the development loop from:

```text
add feature → hope
```

to:

```text
change
 ↓
unit tests
 ↓
deterministic benchmarks
 ↓
dry-run
 ↓
short real mission
 ↓
measure failures
 ↓
fix
 ↓
repeat
```

The benchmark suite is not a substitute for real Minecraft evaluation. It is a fast regression barrier.

## Safety boundary

```text
Model / memory / learning
            ↓
      Candidate decision
            ↓
      Typed Minecraft Action
            ↓
  State freshness / confidence
            ↓
   Independent Supervisor
            ↓
      Rate Limiter
            ↓
        Watchdog
            ↓
       Guarded Executor
            ↓
        Force ESC
            ↓
         Minecraft
```

Learning, memory and missions are **not execution authorities**.

## Limitations

V50 is a major architecture foundation, not proof of perfect autonomous Minecraft gameplay. Real reliability still depends on perception, model quality, latency, input handling, verification and the Minecraft environment.

The purpose of V50 is to make those failures explicit, bounded, testable and much easier to improve systematically.

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
