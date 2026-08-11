# Qynl Agent V23

Qynl is a **Minecraft-only AI agent with temporal perception, hierarchical tasks, explicit goal monitoring, episodic skill memory, recovery, a persistent world model, utility planning, prediction, exploration, short-horizon replanning and verified experience learning**.

## License / Ownership

**Qynl Agent Proprietary License. All rights reserved.**

The Qynl Agent source code and original project materials belong to Qynl unless a file or dependency explicitly states otherwise. You may inspect and evaluate the project for personal, non-commercial use, but you may not redistribute, rebrand, sell, sublicense, copy substantial portions, create a competing derivative project, remove attribution, or claim the project or its substantial source code as your own without written permission.

Third-party dependencies remain under their own licenses. See [`LICENSE`](LICENSE) for the full project license.

## Installation & First Minecraft Session

This section takes you from a fresh download to actually running Qynl with Minecraft.

### 1. Download Qynl

```bash
git clone https://github.com/Qynl/AgentQynl.git
cd AgentQynl
```

Or download the repository as a ZIP from GitHub and extract it.

### 2. Install prerequisites

At minimum:

- Git, if cloning
- Python for the agent backend
- Node.js + npm for the TSX desktop application
- Minecraft Java Edition
- The Minecraft version/configuration supported by the current repository

Set up the Python environment using the dependency files in the repository:

```bash
python -m venv .venv

# Windows
.venv\\Scripts\\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

Then install the desktop dependencies:

```bash
cd apps/desktop
npm install
cd ../..
```

If the repository's dependency files specify different versions or commands, follow those files.

### 3. Configure the AI provider

Use the provider configuration supported by the current build. Keep credentials in environment configuration and never hard-code API keys into source files.

For the first run:

```text
QYNL_DRY_RUN=1
```

### 4. Start Minecraft

Launch Minecraft Java Edition and enter a **dedicated test world**. Do not start by testing on a valuable survival world. When an AI agent makes a questionable decision, your carefully built house does not need to participate in the scientific process.

### 5. Test perception in dry-run mode

Confirm that Qynl can:

1. capture Minecraft
2. recognize the scene
3. create observations
4. update the world model
5. generate candidate actions
6. avoid executing real input

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
Force ESC
 ↓
Minecraft
```

If Force ESC does not work reliably, keep real input disabled.

### 7. Enable real gameplay

After dry-run and Force ESC have been verified:

```text
QYNL_DRY_RUN=0
```

Start Minecraft first, then Qynl. Begin with simple goals such as looking around, exploring or collecting a basic resource.

### 8. Gameplay loop

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
Learn from verified result
 ↓
Update memory/world/goal
 ↓
Replan if needed
```

## Desktop App

The TSX desktop application is the recommended control interface when the current build supports the required backend controls.

### Start it

```bash
cd apps/desktop
npm install
npm run dev
```

Use the scripts defined in `apps/desktop/package.json` if the current build uses different names.

### Desktop workflow

```text
Open Qynl Desktop
 ↓
Configure provider
 ↓
Check Minecraft capture
 ↓
Check safety status
 ↓
Keep DRY RUN ON
 ↓
Start observation
 ↓
Review detected state
 ↓
Set Minecraft goal
 ↓
Start agent
 ↓
Monitor actions / learning
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

## V23: Verified Learning + Curriculum

V23 closes the loop between gameplay and learning. Qynl can now use **verified successful experiences** to influence future action ranking and progressively choose harder Minecraft tasks.

```text
Observe
 ↓
Understand
 ↓
Plan
 ↓
Act
 ↓
Verify
 ↓
Episode Recorder
 ↓
Skill Learner
 ↓
Capability Estimate
 ↓
Curriculum
 ↓
Future planning
```

### Verified Skill Learning

`minecraft/v23_skill_learner.py` records compact experience only after the runtime verifies the outcome.

Each example contains:

- context
- action
- bounded reward
- verification status

Unverified events are ignored. A hallucinated success is not allowed to become a learned skill.

### Episode Recorder

`minecraft/v23_episode.py` keeps a bounded record of recent interactions and separates verified outcomes from uncertain ones.

```text
interaction
 ↓
verification
 ↓
learning data
```

### Progressive Curriculum

`minecraft/v23_curriculum.py` lets Qynl select progressively harder goals based on its conservative capability estimate.

Example:

```text
1  look around
2  collect wood
3  craft tools
4  build shelter
5  explore caves
...
```

The curriculum is configurable and its difficulty values are only heuristics.

### Capability Estimation

`minecraft/v23_capability.py` updates capability only from verified outcomes. Recovery-heavy successes have reduced influence, while unverified outcomes have no influence.

This prevents one lucky or uncertain event from suddenly convincing the agent that it has become a Minecraft professional. Humans already have enough confidence inflation; the software does not need it.

## V22: Hierarchical Planning

V22 established the structure V23 learns from:

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

V23 adds verified learning to this loop.

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
```

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
Force ESC
        ↓
Minecraft executor
```

The learner is only a ranking signal. It cannot directly execute actions or bypass safety gates.

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
│   ├── v23_skill_learner.py
│   ├── v23_episode.py
│   ├── v23_curriculum.py
│   ├── v23_capability.py
│   ├── executor.py
│   └── input_adapter.py
├── memory/
├── safety/
├── evals/
└── docs/
    ├── V22.md
    └── V23.md
```

## Tests

V23 adds tests for:

- rejecting unverified learning data
- verified skill ranking
- verified episode accounting
- curriculum capability bounds
- conservative capability updates

Run the complete test suite before real-input testing.

## Limitations

V23 is a bounded experience-learning layer, not full reinforcement learning or automatic foundation-model training. Its improvements depend on perception quality, verification quality, model quality, latency and the Minecraft environment.

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
