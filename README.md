# Qynl Agent V30

Qynl is a **Minecraft-only autonomous AI agent** with visual perception, hierarchical planning, persistent world state, verified learning, real-time runtime controls, mission-level autonomy, bounded recovery, decision gating, runtime health monitoring and deterministic evaluation.

## License / Ownership

**Qynl Agent Proprietary License. All rights reserved.**

See [`LICENSE`](LICENSE). Third-party dependencies remain under their own licenses.

## V30: Reliability + Evaluation

V30 is the major engineering update that turns Qynl from a growing collection of agent modules into a more measurable control system.

```text
OBSERVE
   ↓
UNDERSTAND
   ↓
GENERATE CANDIDATES
   ↓
DECISION GATE
   ↓
EXECUTE ONE BOUNDED ACTION
   ↓
VERIFY
   ↓
HEALTH CHECK
   ↓
LEARN / REPLAN
```

The key rule is simple: **learning and planning can suggest actions, but neither can bypass the safety/execution boundary.**

## What V30 adds

### 1. Typed agent contracts

`minecraft/v30_contracts.py`

Introduces explicit representations for:

- observations
- confidence bands
- candidate actions
- decisions
- verification results

This reduces implicit state passing between perception, planning, execution and evaluation.

### 2. Uncertainty-aware Decision Gate

`minecraft/v30_decision_gate.py`

Before selecting an action, V30 checks:

- observation confidence
- action risk
- expected progress
- bounded action cost

If confidence is too low or every candidate fails, the result is **no action**. The controller can re-observe or enter recovery instead.

### 3. Runtime Health Monitor

`minecraft/v30_health.py`

Tracks:

- loop lag
- consecutive failures
- time since last verified result

An unhealthy runtime can be stopped or routed into recovery by the higher-level controller.

### 4. Deterministic Benchmark Harness

`minecraft/v30_benchmark.py`

Decision changes can now be measured using controlled benchmark cases before they are trusted in real Minecraft sessions.

Each case contains:

```text
Observation
Candidate actions
Expected decision
```

The benchmark reports per-case results and an overall score.

### 5. V30 tests

`evals/test_v30.py` covers:

- low-confidence rejection
- risky-action rejection
- bounded utility selection
- stale-verification health detection
- benchmark scoring

## Architecture

```text
                    MISSION CONTROL
                          │
                    GOAL / SUBTASK
                          │
                    WORLD MODEL
                          │
                    PERCEPTION
                          │
                 CANDIDATE GENERATION
                          │
                    DECISION GATE
                     /          \\
                  ACT             STOP
                   │                │
             GUARDED EXECUTOR   REOBSERVE
                   │
                MINECRAFT
                   │
               VERIFICATION
                   │
          ┌────────┴─────────┐
          │                  │
       LEARNING           HEALTH
          │                  │
          └────────┬─────────┘
                   ↓
                REPLAN
```

## Safety boundary

```text
Model / memory / learning
            ↓
      Candidate actions
            ↓
       Decision Gate
            ↓
        ActionPolicy
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

Learning, mission memory and recovery are **not execution authorities**.

V30 does not introduce unrestricted shell access, arbitrary OS commands or credential access.

## Serious real-session workflow

### 1. Download

```bash
git clone https://github.com/Qynl/AgentQynl.git
cd AgentQynl
```

Or download the repository ZIP from GitHub.

### 2. Install prerequisites

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

Follow the dependency files in the repository if they specify different commands.

### 3. Configure the provider

Keep credentials in environment configuration. Never hard-code or commit API keys.

Start safely with dry-run enabled:

```text
QYNL_DRY_RUN=1
```

### 4. Start Minecraft

Use a **dedicated test world**. Do not use a valuable survival world for initial autonomous sessions. Humanity invented civilization and then taught a computer to punch trees. It deserves a sandbox.

### 5. Run benchmarks

Run the deterministic V30 decision tests before changing the real gameplay configuration.

### 6. Dry-run

Verify:

- screen capture
- visual perception
- world model
- goals/subtasks
- planning
- decision gate
- verification
- V23 learning
- V26 mission control
- recovery
- Force ESC
- watchdog
- V30 health state

No real input should execute in dry-run mode.

### 7. Real mission

Only after the above checks pass:

```text
QYNL_DRY_RUN=0
```

Start with objectively verifiable missions:

```text
Collect 16 logs
Craft a stone pickaxe
Build a shelter
Reach a specified location
```

Avoid vague objectives such as `play Minecraft well`.

### 8. Monitor

During early real sessions, monitor:

```text
Mission status
Progress
Current subtask
Current decision
Current action
Verification result
Decision confidence
Health
Recovery state
Learning events
```

Keep early real sessions supervised.

## Desktop App

The TSX desktop app is intended to be the main operator interface when the current build supports the required backend controls.

Typical development startup:

```bash
cd apps/desktop
npm install
npm run dev
```

Use the scripts actually defined in `apps/desktop/package.json` if they differ.

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
Run benchmarks
 ↓
Observe
 ↓
Create mission
 ↓
Start
 ↓
Monitor health + decisions
 ↓
Pause / Abort / Force ESC when necessary
 ↓
Review mission result
```

Recommended initial settings:

- **Dry Run:** ON
- **Watchdog:** ON
- **Force ESC:** ON and tested
- **Action Rate:** conservative
- **Recovery:** ON
- **Bounded Memory:** ON
- **Simple verified mission:** ON

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
V26  Long-running missions + structured mission memory + deterministic recovery
 ↓
V30  Typed contracts + decision gate + health + deterministic benchmarks
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
    └── V30.md
```

## Testing philosophy

V30 changes the development loop from:

```text
add feature → hope
```

to:

```text
change
 ↓
benchmark
 ↓
test
 ↓
dry-run
 ↓
short real mission
 ↓
measure failure
 ↓
fix
 ↓
repeat
```

The deterministic benchmark is not a substitute for real Minecraft evaluation. It is a fast regression barrier that catches obvious decision-quality regressions before they reach live sessions.

## Limitations

V30 is a major reliability/evaluation architecture update, not proof that Qynl can already solve arbitrary Minecraft tasks flawlessly. Real reliability still depends on the actual vision model, Minecraft input adapter, model latency, verification quality and environment.

The important change is that more of those failures can now be represented explicitly and measured rather than hidden inside an endless action loop.

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
