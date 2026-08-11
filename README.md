# Qynl Agent V22

Qynl is a **Minecraft-only AI agent with temporal perception, hierarchical tasks, explicit goal monitoring, episodic skill memory, recovery, a persistent world model, utility planning, prediction, exploration and short-horizon replanning**.

## License / Ownership

**Qynl Agent Proprietary License. All rights reserved.**

The Qynl Agent source code and original project materials belong to Qynl unless a file or dependency explicitly states otherwise. You may inspect and evaluate the project for personal, non-commercial use, but you may not redistribute, rebrand, sell, sublicense, copy substantial portions, create a competing derivative project, remove attribution, or claim the project or its substantial source code as your own without written permission.

Third-party dependencies remain under their own licenses. See [`LICENSE`](LICENSE) for the full project license.

This license is intended to make ownership and permitted use explicit. It does not magically override copyright law, third-party licenses, or rights that cannot legally be waived. Humanity has unfortunately invented lawyers for this exact reason.

## Installation & First Minecraft Session

This section takes you from a fresh download to actually running Qynl with Minecraft.

### 1. Download Qynl

Clone the repository:

```bash
git clone https://github.com/Qynl/AgentQynl.git
cd AgentQynl
```

Or download the repository as a ZIP from GitHub and extract it.

### 2. Install prerequisites

Install the versions required by the files in the repository before running the agent. At minimum, you need:

- Git, if cloning
- Python for the agent backend
- Node.js + npm for the TSX desktop application
- Minecraft Java Edition
- A supported Minecraft version/configuration used by this repository

Then install the project's Python dependencies and desktop dependencies using the dependency files already included in the repository:

```bash
# Python environment
python -m venv .venv

# Windows
.venv\\Scripts\\activate

# Linux/macOS
source .venv/bin/activate

# Install Python dependencies if requirements.txt exists
pip install -r requirements.txt
```

For the desktop app:

```bash
cd apps/desktop
npm install
cd ../..
```

If the repository's dependency files specify different commands or versions, follow those files. They are the source of truth.

### 3. Configure the AI provider

Qynl can use the model provider supported by the current provider configuration. Put provider credentials in the expected environment configuration rather than hard-coding keys into source code.

Never commit API keys to GitHub.

For a safe first run, keep real input disabled:

```text
QYNL_DRY_RUN=1
```

### 4. Start Minecraft

Launch Minecraft and enter a **dedicated test world**.

Do not begin by testing on a valuable survival world. The entire point of a test environment is that when the AI does something impressively stupid, your house does not have to become part of the experiment.

Keep the Minecraft window visible and use the game's normal input configuration expected by the current input adapter.

### 5. Test capture and perception first

Start Qynl in dry-run mode. Confirm that it can:

1. capture the Minecraft screen
2. recognize the Minecraft scene
3. produce observations
4. build/update its world model
5. generate candidate actions
6. avoid executing real input

Do not enable real gameplay until those checks work.

### 6. Test Force ESC

Before real input, verify the emergency stop.

The intended safety chain is:

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
Force ESC
 ↓
Minecraft
```

If Force ESC does not reliably stop the agent, **do not enable real input**.

### 7. Enable real gameplay

Once dry-run and the emergency stop have been verified, enable the real-input configuration used by the current runtime:

```text
QYNL_DRY_RUN=0
```

Start Minecraft first, then start Qynl. Begin with a simple goal such as exploration or collecting a basic resource rather than immediately asking it to complete an entire Minecraft speedrun. The latter is an excellent way to produce a very sophisticated failure report.

### 8. What happens while it plays

The V22 loop is approximately:

```text
Minecraft screen
 ↓
Vision
 ↓
World Model + Spatial Memory
 ↓
Goal Monitor
 ↓
Subtask Graph
 ↓
Candidate Planner
 ↓
Prediction
 ↓
Short-Horizon Plan
 ↓
Safety validation
 ↓
One action
 ↓
Observe again
 ↓
Verify progress
 ↓
Update memory/world/goal
 ↓
Replan if needed
```

Qynl should repeatedly observe and correct itself instead of blindly executing a long precomputed sequence.

## Desktop App

The TSX desktop application is the recommended way to operate Qynl when its current build supports the required backend controls.

### Start the desktop app

From the repository:

```bash
cd apps/desktop
npm install
npm run dev
```

Use the script names defined in `apps/desktop/package.json` if the current project uses different names.

### Desktop workflow

The intended workflow is:

```text
Open Qynl Desktop
 ↓
Select/configure provider
 ↓
Check Minecraft connection/capture
 ↓
Check safety status
 ↓
Keep DRY RUN enabled initially
 ↓
Start observation
 ↓
Review detected state
 ↓
Set Minecraft goal
 ↓
Start agent
 ↓
Monitor actions
 ↓
Use Force ESC if necessary
```

### Recommended desktop settings

Before real gameplay, check:

- **Provider:** correct model/provider configuration
- **Dry Run:** ON for initial testing
- **Action Rate:** conservative
- **Watchdog:** enabled
- **Force ESC:** enabled and tested
- **Vision confidence:** do not disable uncertainty handling
- **Recovery:** enabled
- **Memory:** bounded
- **Goal:** simple and testable

Do not paste API keys into screenshots, issues, Discord messages, or GitHub commits.

## V22: Hierarchical Planning + Closed-Loop Execution

V22 turns the previous planning components into a more explicit hierarchy: **goal → subtask → short action sequence → one verified action → update → replan**.

```text
Goal
 ↓
Goal Monitor
 ↓
Subtask Graph
 ↓
World Model + Spatial Memory + Skill Memory
 ↓
Candidate Planner
 ↓
Transition Predictor
 ↓
Short-Horizon Sequencer
 ↓
Replan Policy
 ↓
Rate Limiter
 ↓
Watchdog
 ↓
ActionPolicy
 ↓
Force ESC
 ↓
Minecraft
 ↓
Verify
 ↓
Goal/Subtask update
```

## V22 improvements

- 🎯 **Explicit Goal Monitor** with ACTIVE / PROGRESS / STALLED / COMPLETE / FAILED
- 🌳 **Hierarchical Subtask Graph**
- 🧩 **Bounded short-horizon action sequencing**
- 🔄 **Deterministic replanning triggers**
- 🧠 **Goal/subtask progress feedback**
- 🛑 **Terminal-state handling** so completed/failed goals are not endlessly replanned
- 🔒 **Every action still passes the existing safety pipeline**
- 🧪 V22 goal/sequencing/replanning tests
- 📚 Complete V22 documentation

## Goal Monitor

`minecraft/v22_goal_monitor.py` gives the current objective an explicit state:

```text
ACTIVE
PROGRESS
STALLED
COMPLETE
FAILED
```

Completion requires strong completion evidence **and** enough confidence. A single uncertain visual cue is not treated as proof that the objective is complete.

## Hierarchical Subtasks

`minecraft/v22_subtasks.py` represents larger Minecraft objectives as smaller pieces.

Example:

```text
Survive first night
├── collect wood
├── craft tools
├── collect food
└── build shelter
```

The immediate action can therefore serve a specific subtask while the monitor tracks the larger objective.

## Short-Horizon Sequencing

`minecraft/v22_action_sequence.py` can build a small sequence from already-ranked candidates.

The sequence is deliberately short. Qynl does **not** blindly execute a huge macro:

```text
Plan 2–3 steps
 ↓
Execute ONE
 ↓
Observe
 ↓
Verify
 ↓
Continue / modify / abort
```

This preserves the agent's ability to react to the actual Minecraft state.

## Replanning

`minecraft/v22_replan.py` provides explicit replanning triggers:

- selected action rejected
- repeated state without progress
- high uncertainty
- recovery exhausted

Terminal goal states do not trigger pointless replanning.

## V21 → V22

V21 made uncertainty explicit:

```text
Observe → Predict → ACT / EXPLORE / STOP → Verify
```

V22 adds hierarchy and persistent plan control:

```text
Goal
 ↓
Subtask
 ↓
Plan short horizon
 ↓
Execute one step
 ↓
Verify
 ↓
Update
 ↓
Replan if necessary
```

The agent now has a clearer separation between:

- **what** it wants
- **what subgoal** it is currently pursuing
- **which action** it should perform
- **whether the plan is still valid**

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
```

## Safety chain

```text
Model output
    ↓
Strict Minecraft action representation
    ↓
Action Rate Limiter
    ↓
Runtime Watchdog
    ↓
ActionPolicy
    ↓
Force ESC
    ↓
Minecraft executor
```

Short-horizon sequences, subtasks and replanning cannot bypass this chain.

No shell access, arbitrary OS commands, credentials or unrestricted desktop automation is introduced.

## Minecraft-only boundary

Qynl is designed around Minecraft-focused visual state, Minecraft goals, bounded memory and Minecraft actions.

## Real gameplay

Real input remains opt-in with `QYNL_DRY_RUN=0`.

Use a dedicated Minecraft test world and verify Force ESC before enabling real input.

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
│   ├── v10_provider.py
│   ├── planner.py
│   ├── goals.py
│   ├── v11_model.py
│   ├── v11_agent.py
│   ├── v12_state.py
│   ├── v12_strategy.py
│   ├── v13_state.py
│   ├── v13_planner.py
│   ├── v13_controller.py
│   ├── v14_tasks.py
│   ├── v14_evaluator.py
│   ├── v14_memory.py
│   ├── v15_blackboard.py
│   ├── v15_watchdog.py
│   ├── v15_action_verifier.py
│   ├── v16_recovery.py
│   ├── v16_memory.py
│   ├── v16_rate_limiter.py
│   ├── v20_world_model.py
│   ├── v20_planner.py
│   ├── v20_loop.py
│   ├── v21_spatial_memory.py
│   ├── v21_exploration.py
│   ├── v21_predictor.py
│   ├── v21_controller.py
│   ├── v22_goal_monitor.py
│   ├── v22_action_sequence.py
│   ├── v22_subtasks.py
│   ├── v22_replan.py
│   ├── executor.py
│   └── input_adapter.py
├── memory/
├── safety/
├── evals/
└── docs/
    └── V22.md
```

## Tests

V22 adds tests for:

- goal completion confidence
- stalled-goal detection
- bounded action sequences
- hierarchical subtasks
- deterministic replanning

Run the complete test suite before real-input testing.

## Limitations

V22 is still a screen-based agent. It cannot guarantee unseen world state, perfect goal recognition or perfect predictions. Short-horizon planning is deliberately bounded so Qynl can correct itself frequently.

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
