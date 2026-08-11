# Qynl Agent V22

Qynl is a **Minecraft-only AI agent with temporal perception, hierarchical tasks, explicit goal monitoring, episodic skill memory, recovery, a persistent world model, utility planning, prediction, exploration and short-horizon replanning**.

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

Not specified yet.
