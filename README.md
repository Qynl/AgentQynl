# Qynl Agent V15

Qynl is a **Minecraft-only AI agent with temporal perception, hierarchical tasks, explicit goal evaluation, episodic skill memory and a reliability-controlled runtime**.

## V15: reliable agent loop

V15 builds on V14 by giving the different agent layers one bounded shared control state and adding independent runtime safeguards plus explicit action verification.

```text
User goal
   ↓
Task / Subtask
   ↓
┌─────────────────────────┐
│     V15 Blackboard      │
│ goal / state / mode /   │
│ failures / evaluation   │
└─────────────────────────┘
   ↓
Temporal perception + skill memory
   ↓
Planner
   ↓
Strict action parser
   ↓
Runtime Watchdog
   ↓
ActionPolicy
   ↓
Force ESC
   ↓
Minecraft executor
   ↓
Post-action perception
   ↓
Action Verifier
   ↓
Goal Evaluator
   ↓
Skill Memory + Blackboard
   ↓
next action / subtask / recovery
```

## V15 improvements

- 🧠 **Shared Blackboard** for consistent cross-layer state
- 🛡️ **Runtime Watchdog** independent of the model
- ⏱️ **Action duration limits**
- 🔢 **Consecutive failure budget**
- ⌛ **Per-step time budget**
- 🔎 **Dedicated action verification** using pre/post observations
- 🔄 **Observable-change scoring**
- 🧪 V15 reliability tests
- 📚 Complete V15 documentation

## Shared Blackboard

`minecraft/v15_blackboard.py` provides one bounded source of truth for:

```text
goal
active subtask
success hint
current state
latest delta
last action
last evaluation
strategy mode
recent failures
events
```

This prevents the planner, evaluator and recovery system from maintaining unrelated versions of what Qynl currently believes is happening.

All histories are bounded.

## Runtime Watchdog

`minecraft/v15_watchdog.py` provides runtime limits that the model cannot override.

It can reject:

- an action exceeding the configured duration
- further actions after too many consecutive failures
- a step exceeding its time budget

This is deliberately separate from the model's reasoning.

The model can propose **what might help**. The runtime decides whether the proposal is allowed to execute.

## Action verification

`minecraft/v15_action_verifier.py` compares the temporal state before and after an action.

It checks for observable changes involving:

- entities
- landmarks
- hazards
- UI
- overall state

This is an action-effect signal, not proof that the complete Minecraft goal succeeded. The V14 goal evaluator remains the authority for subtask success.

## V14 → V15

V14 added:

- hierarchical task decomposition
- explicit goal evaluation
- episodic skill memory

V15 adds the reliability layer:

```text
V14
Task → Plan → Action → Evaluate → Remember

V15
Task → Shared State → Plan → Watchdog → Action → Verify → Evaluate → Remember → Shared State
```

That makes failures and state changes available consistently to the next decision instead of being scattered across independent components.

## Safety chain

```text
Model output
    ↓
Strict Minecraft parser
    ↓
Runtime Watchdog
    ↓
ActionPolicy
    ↓
Force ESC
    ↓
Minecraft executor
```

No shell access, arbitrary desktop automation, process creation, credentials or unrestricted computer control is introduced.

## Minecraft-only boundary

The agent is limited to Minecraft-focused visual state, goals, bounded memory and Minecraft actions.

## Real gameplay

V15 retains the existing real-input runtime. Real input remains opt-in with `QYNL_DRY_RUN=0`.

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
│   ├── executor.py
│   └── input_adapter.py
├── memory/
├── safety/
├── evals/
└── docs/
    └── V15.md
```

## Tests

V15 adds tests for:

- bounded blackboard history
- action duration limits
- action verification

Run the complete test suite before real-input testing.

## Limitations

V15 improves runtime coordination and reliability. It does not make visual perception infallible or guarantee that an observable change means a task succeeded. Actual gameplay quality still depends on the selected models, capture quality, latency, Minecraft version/UI and task complexity.

## License

Not specified yet.
