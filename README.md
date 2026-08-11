# Qynl Agent V24

Qynl is a **Minecraft-only AI agent with temporal perception, hierarchical tasks, explicit goal monitoring, episodic skill memory, recovery, a persistent world model, utility planning, prediction, exploration, short-horizon replanning, verified experience learning and a guarded real-time runtime**.

## License / Ownership

**Qynl Agent Proprietary License. All rights reserved.**

The Qynl Agent source code and original project materials belong to Qynl unless a file or dependency explicitly states otherwise. You may inspect and evaluate the project for personal, non-commercial use, but you may not redistribute, rebrand, sell, sublicense, copy substantial portions, create a competing derivative project, remove attribution, or claim the project or its substantial source code as your own without written permission.

Third-party dependencies remain under their own licenses. See [`LICENSE`](LICENSE) for the full project license.

## Installation & First Minecraft Session

### 1. Download

```bash
git clone https://github.com/Qynl/AgentQynl.git
cd AgentQynl
```

Or download the repository as a ZIP from GitHub and extract it.

### 2. Prerequisites

At minimum:

- Git, if cloning
- Python for the agent backend
- Node.js + npm for the TSX desktop application
- Minecraft Java Edition
- The Minecraft version/configuration supported by the current repository

Set up Python:

```bash
python -m venv .venv

# Windows
.venv\\Scripts\\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

Install desktop dependencies:

```bash
cd apps/desktop
npm install
cd ../..
```

Follow repository dependency files if they specify different versions or commands.

### 3. Configure the AI provider

Use the provider configuration supported by the current build. Keep credentials in environment configuration and never hard-code API keys into source files.

First run:

```text
QYNL_DRY_RUN=1
```

### 4. Start Minecraft

Launch Minecraft Java Edition and enter a **dedicated test world**. Do not start on a valuable survival world. An AI agent is perfectly capable of turning your house into a case study.

### 5. Dry-run verification

Confirm that Qynl can:

1. capture Minecraft
2. recognize the scene
3. create observations
4. update the world model
5. generate candidate actions
6. learn only from verified outcomes
7. avoid executing real input

### 6. Test Force ESC

Before real input, verify that the emergency stop reliably interrupts the agent.

```text
AI
 ↓
Action validation
 ↓
Rate limiter
 ↓
Runtime watchdog
 ↓
ActionPolicy
 ↓
Guarded Executor
 ↓
Force ESC
 ↓
Minecraft
```

If Force ESC does not work reliably, keep real input disabled.

## Desktop App

The TSX desktop application is the recommended control interface when the current build supports the required backend controls.

Start it with the scripts defined by `apps/desktop/package.json`. The typical development command is:

```bash
cd apps/desktop
npm install
npm run dev
```

Desktop workflow:

```text
Open Qynl Desktop
 ↓
Configure provider
 ↓
Check Minecraft capture
 ↓
Check safety status
 ↓
DRY RUN ON
 ↓
Start observation
 ↓
Review state
 ↓
Set Minecraft goal
 ↓
Start agent
 ↓
Monitor actions + telemetry
 ↓
Use Force ESC if necessary
```

Recommended initial settings:

- **Dry Run:** ON
- **Watchdog:** ON
- **Force ESC:** ON and tested
- **Action Rate:** conservative
- **Recovery:** ON
- **Memory:** bounded
- **Goal:** simple and measurable

Never paste API keys into screenshots, issues, Discord messages or commits.

## V24: Real-Time Runtime

V24 is the **real-session engineering update**. The focus is no longer just adding smarter modules. Qynl now treats actual Minecraft gameplay as a controlled runtime with explicit limits, failure handling, telemetry and a guarded execution boundary.

```text
Minecraft Capture
 ↓
Perception
 ↓
World Model / Memory
 ↓
Goal + Subtasks
 ↓
Planner + Predictor
 ↓
Verified Learning
 ↓
ActionPolicy
 ↓
Guarded Executor
 ↓
Minecraft Input Adapter
 ↓
Observe Result
 ↓
Telemetry + Verification
 ↓
Learn / Replan
```

### Real-Time Runtime

`minecraft/v24_realtime_runtime.py` adds:

- bounded observation rate
- bounded action latency
- consecutive failure budget
- explicit start/stop state
- dry-run isolation

If the configured failure budget is exhausted, the runtime stops instead of continuing blindly.

### Guarded Executor

`minecraft/v24_task_executor.py` checks:

1. emergency stop
2. policy permission
3. dry-run state
4. action validity

The planner and learned preferences do not directly receive unrestricted OS control.

### Session Telemetry

`minecraft/v24_session.py` keeps bounded session statistics:

- event count
- verified events
- verified reward

It does not store credentials or raw screenshots in this component.

## How to run a serious real session

1. Create a dedicated Minecraft test world.
2. Start Qynl in **DRY RUN**.
3. Confirm screen capture and perception.
4. Confirm goals and subtasks work.
5. Test Force ESC.
6. Run a short dry-run session.
7. Inspect failures and telemetry.
8. Enable real input only after those checks pass.
9. Start with a simple goal.
10. Monitor the first real session.
11. Review verified outcomes and failures.
12. Improve the system based on measured failures, not guesses.

The goal of V24 is to make this cycle repeatable:

```text
RUN
 ↓
MEASURE
 ↓
VERIFY
 ↓
LEARN
 ↓
IMPROVE
 ↓
RUN AGAIN
```

## V23: Verified Learning

V23 introduced learning from verified Minecraft outcomes. `minecraft/v23_skill_learner.py` changes future action ranking only from verified experiences. `minecraft/v23_episode.py` keeps bounded interaction history. `minecraft/v23_curriculum.py` selects progressively harder tasks, and `minecraft/v23_capability.py` estimates capability conservatively.

Unverified events do not become skills.

## V22: Hierarchical Planning

V22 established:

```text
Goal
 ↓
Subtask
 ↓
Short plan
 ↓
One action
 ↓
Verify
 ↓
Update
 ↓
Replan
```

## Evolution

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
```

## Safety invariants

V24 deliberately enforces these principles:

- **Dry run must never execute a real action.**
- **Emergency stop takes priority over execution.**
- **Policy rejection prevents execution.**
- **Learned data is not an execution authority.**
- **The runtime stops after its failure budget is exhausted.**
- **Telemetry is bounded.**
- **Credentials are not part of session telemetry.**

## Safety chain

```text
Model / learned preference
        ↓
Strict Minecraft action representation
        ↓
Action Rate Limiter
        ↓
Runtime Watchdog
        ↓
ActionPolicy
        ↓
Guarded Executor
        ↓
Force ESC
        ↓
Minecraft executor
```

## Minecraft-only boundary

Qynl is designed around Minecraft-focused visual state, Minecraft goals, bounded memory and Minecraft actions.

## Real gameplay

Real input remains opt-in with `QYNL_DRY_RUN=0`.

Use a dedicated Minecraft test world and verify Force ESC before enabling real input. Keep the first real sessions supervised.

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
│   ├── executor.py
│   └── input_adapter.py
├── memory/
├── safety/
├── evals/
└── docs/
    ├── V22.md
    ├── V23.md
    └── V24.md
```

## Tests

V24 adds tests for:

- failure-budget shutdown
- dry-run isolation
- emergency-stop priority
- bounded telemetry
- verification-scoped session statistics

Run the complete test suite before real-input testing.

## Limitations

V24 is a serious runtime foundation, not a claim of perfect autonomous Minecraft gameplay. Reliability still depends on perception, model quality, latency, input handling, verification and the actual Minecraft environment. The point of V24 is that failures are now measurable, bounded and much easier to improve systematically.

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
