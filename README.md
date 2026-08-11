# Qynl Agent V26

Qynl is a **Minecraft-only autonomous AI agent** with visual perception, hierarchical planning, persistent world state, verified learning, real-time runtime controls, mission-level autonomy and bounded recovery.

## License / Ownership

**Qynl Agent Proprietary License. All rights reserved.**

See [`LICENSE`](LICENSE). Third-party dependencies remain under their own licenses.

## V26: Long-Running Mission Autonomy

V26 is about making Qynl behave like one coherent agent across an entire Minecraft mission rather than a sequence of disconnected actions.

```text
MISSION
  ↓
OBJECTIVE
  ↓
SUBTASKS
  ↓
WORLD MODEL + MEMORY
  ↓
PLAN
  ↓
ONE BOUNDED ACTION
  ↓
VERIFY
  ↓
UPDATE PROGRESS
  ↓
LEARN VERIFIED LESSON
  ↓
CONTINUE / RECOVER / REPLAN
  ↓
MISSION RESULT
```

### Mission Control

`minecraft/v26_mission_control.py` adds an explicit mission state machine:

- `IDLE`
- `RUNNING`
- `PAUSED`
- `COMPLETED`
- `FAILED`
- `ABORTED`

Missions have a progress value, blockers and a maximum runtime. A mission that exceeds its runtime budget fails instead of continuing forever.

Operators can pause or abort a mission without giving the planner unrestricted control.

### Mission Memory

`minecraft/v26_mission_memory.py` stores compact **verified** mission results:

- mission identifier
- outcome
- verified status
- bounded reward
- short lesson

Unverified results are discarded. Memory size and lesson length are bounded.

### Deterministic Recovery

`minecraft/v26_recovery.py` provides a bounded recovery ladder for uncertainty and stalls:

```text
REOBSERVE
   ↓
RELOCALIZE
   ↓
REPLAN
   ↓
BACKTRACK
   ↓
PAUSE
   ↓
ABORT
```

The recovery budget prevents endless loops. When recovery is exhausted, the mission aborts.

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
- the Minecraft version/configuration supported by this repository

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

Follow the actual dependency files in the repository if they specify different commands.

### 3. Configure the provider

Keep provider credentials in environment configuration. Never hard-code or commit API keys.

Start safely:

```text
QYNL_DRY_RUN=1
```

### 4. Start Minecraft

Use a **dedicated test world**. Do not use a valuable survival world for the first autonomous sessions. Humans spent thousands of years inventing civilization, and then we gave the computer permission to punch trees.

### 5. Dry-run first

Verify:

- screen capture
- visual perception
- world model
- goals/subtasks
- planning
- verification
- V23 learning
- V26 mission control
- recovery
- Force ESC
- watchdog

No real input should execute in dry-run mode.

### 6. Run a real mission

Only after the dry-run checks pass:

```text
QYNL_DRY_RUN=0
```

Start with an objectively verifiable mission:

```text
Collect 16 logs
Craft a stone pickaxe
Build a shelter
Reach a specified location
```

Avoid vague objectives such as `play Minecraft well`. A machine cannot reliably verify something humans themselves argue about on Reddit for six hours.

### 7. Monitor the mission

The runtime should continuously provide:

```text
Mission status
Progress
Current subtask
Current action
Verification result
Recovery state
Runtime health
Learning events
```

Keep early real sessions supervised.

## Desktop App

The TSX desktop app is intended to be the main operator interface.

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
Observe
 ↓
Create mission
 ↓
Start
 ↓
Monitor
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

## Architecture

```text
                   ┌──────────────────┐
                   │  Mission Control │
                   └────────┬─────────┘
                            ↓
                    Goal / Subtasks
                            ↓
              ┌─────────────┴─────────────┐
              ↓                           ↓
        World Model                  Mission Memory
              ↓                           ↑
         Perception                      │
              ↓                           │
       Planner / Predictor               │
              ↓                           │
        Action Policy                    │
              ↓                           │
       Guarded Executor                  │
              ↓                           │
          Minecraft ─────→ Verification ─┘
              ↑                 ↓
              └──── Recovery / Replan
```

## Safety boundary

```text
Mission / planner / learned lesson
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

V26 does not introduce unrestricted shell access, arbitrary OS commands or credential access.

## Version history

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
│   ├── executor.py
│   └── input_adapter.py
├── memory/
├── safety/
├── evals/
└── docs/
    ├── V22.md
    ├── V23.md
    ├── V24.md
    └── V26.md
```

## Tests

V26 adds tests for:

- mission lifecycle
- completion state
- ignoring unverified mission results
- deterministic recovery escalation
- recovery abort behavior

Run the full test suite before real-input testing.

## What V26 does not claim

V26 is a serious autonomy architecture update, not proof that Qynl can already complete arbitrary Minecraft missions flawlessly. Reliability still depends on the complete perception, model, planning, input and verification stack.

The important change is that long-running failures are now represented explicitly, bounded, recoverable and measurable instead of being hidden inside an endless action loop.

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
