# Qynl Agent V20

Qynl is a **Minecraft-only AI agent with temporal perception, hierarchical tasks, explicit goal evaluation, episodic skill memory, recovery, a persistent world model and utility-based planning**.

## V20: World Model + Utility Planning

V20 is a major architecture update. Instead of treating each screenshot as an isolated decision, Qynl now maintains a compact structured world model and ranks multiple bounded action candidates before execution.

```text
Minecraft screen
      ↓
Vision observation
      ↓
Persistent World Model
      ↓
Goal + relevant memory
      ↓
Utility Planner
      ↓
Candidate actions
      ↓
Rate Limiter
      ↓
Runtime Watchdog
      ↓
ActionPolicy
      ↓
Force ESC
      ↓
Minecraft
      ↓
Post-action observation
      ↓
Verification / Recovery
      ↓
World Model update
```

## V20 improvements

- 🌍 **Persistent Minecraft World Model**
- 🧍 **Tracked observed entities** with confidence and coarse position hints
- 🗺️ **Persistent landmarks, hazards and UI state**
- 📝 **Recent world events**
- 🎯 **Utility-based candidate planning**
- 🔀 **Multiple candidate actions instead of one-shot planning**
- 🧠 **Relevant memory integrated into planning**
- 🔒 **Every candidate still passes the complete safety pipeline**
- 🔄 **Integrated closed-loop orchestrator**
- 🧪 V20 world-model/planner tests
- 📚 Complete V20 documentation

## Persistent World Model

`minecraft/v20_world_model.py` provides `WorldModel`.

It stores only observed evidence:

```text
entities / objects
confidence
coarse position hints
landmarks
hazards
visible UI
recent events
```

It is deliberately **not** an invented 3D map. If Qynl has not observed something, the world model does not pretend to know it.

## Utility Planner

`minecraft/v20_planner.py` changes planning from:

```text
"give me one action"
```

to:

```text
"give me a small set of possible actions and rank them"
```

Candidates are scored using model-estimated utility based on expected progress, observability, risk, recovery mode and relevant memory.

The score does **not** grant execution authority. Every candidate is independently validated by the runtime.

## Integrated V20 loop

`minecraft/v20_loop.py` orchestrates the major components:

1. Force ESC checkpoint
2. Minecraft capture
3. Vision observation
4. World-model update
5. Memory retrieval
6. Candidate generation/ranking
7. Rate limiting
8. Runtime watchdog
9. ActionPolicy validation
10. Force ESC checkpoint
11. One Minecraft action
12. Post-action observation and existing verification/recovery flow

Invalid or rejected candidates are discarded.

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
V20  Persistent world model + utility planning + integrated loop
```

The architecture is now centered around:

```text
OBSERVE
  ↓
MODEL THE WORLD
  ↓
REMEMBER RELEVANT EXPERIENCE
  ↓
GENERATE OPTIONS
  ↓
RANK OPTIONS
  ↓
VALIDATE
  ↓
ACT
  ↓
OBSERVE AGAIN
  ↓
VERIFY / RECOVER
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

The world model, memory and utility score cannot bypass this chain.

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
│   ├── executor.py
│   └── input_adapter.py
├── memory/
├── safety/
├── evals/
└── docs/
    └── V20.md
```

## Tests

V20 adds tests for:

- persistent world-object tracking
- utility candidate ordering

Run the complete test suite before real-input testing.

## Limitations

V20 is a stronger control architecture, not a guarantee of human-level Minecraft gameplay. Visual perception can be wrong, the world model only knows observed evidence, and utility scores are model estimates. Verification and bounded recovery remain essential.

## License

Not specified yet.
