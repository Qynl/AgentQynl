# Qynl Agent V16

Qynl is a **Minecraft-only AI agent with temporal perception, hierarchical tasks, explicit goal evaluation, episodic skill memory, reliability controls and bounded recovery**.

## V16: recovery + adaptive control

V16 builds on V15 by adding a dedicated recovery layer. The agent can detect common failure patterns and choose a bounded recovery strategy instead of blindly repeating the same behavior.

```text
User goal
   ↓
Task / Subtask
   ↓
Shared Blackboard
   ↓
Temporal state + Adaptive Memory
   ↓
Planner
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
Post-action verification
   ↓
Progress?
 ┌──┴──┐
YES   NO
 ↓     ↓
next  Recovery Manager
       ↓
 reobserve / look around /
 reposition / change action /
 abort
       ↓
    Planner
```

## V16 improvements

- 🧭 **Bounded Recovery Manager**
- 🔎 **Failure diagnosis** using repeated state/action and confidence
- 🔁 **Anti-loop recovery**
- 👁️ **Re-observation recovery** for uncertain perception
- 🧭 **Look-around recovery** for unchanged scenes
- 🚶 **Reposition recovery** after failed actions
- 🛑 **Recovery budget** with explicit abort
- 🧠 **Positive + negative adaptive memory**
- ⏱️ **Action rate limiter**
- 🧪 V16 recovery/memory/rate-limit tests
- 📚 Complete V16 documentation

## Recovery Manager

`minecraft/v16_recovery.py` handles the question:

> What should Qynl do when the current approach stops working?

It considers:

- repeated visual state
- repeated action pattern
- low perception confidence
- recent failures

Possible modes:

```text
reobserve
look_around
reposition
change_action
abort
```

The priority is conservative. Low confidence causes re-observation first. Repeated actions trigger a change of approach. Repeated unchanged states trigger exploration. Too many failures eventually cause an abort instead of an infinite loop.

## Adaptive memory

`minecraft/v16_memory.py` stores both successful and unsuccessful lessons.

Example:

```text
Goal: find village
Situation: plains
Lesson: do not keep walking in the same direction
Reward: -1
```

Negative experiences are useful because they can tell the planner what **not** to repeat.

Memory retrieval remains bounded and retrieval-based. V16 does not secretly modify model weights during gameplay.

## Action rate limiting

`minecraft/v16_rate_limiter.py` enforces a minimum interval between actions. This provides another runtime boundary against accidental action bursts.

## V15 → V16

V15 answered:

```text
Is this action bounded and did the world change?
```

V16 adds:

```text
If it didn't work, WHY might it have failed?
What is the safest useful recovery?
Should we observe again, move, change the action, or stop?
```

The resulting loop is:

```text
Act → Verify → Diagnose → Recover → Act
```

instead of:

```text
Act → Fail → Repeat → Fail → Repeat forever
```

## Safety chain

```text
Model output
    ↓
Strict Minecraft parser
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

Recovery decisions cannot execute OS commands or bypass Force ESC.

## Minecraft-only boundary

The agent is limited to Minecraft-focused visual state, goals, bounded memory and Minecraft actions. No shell access, arbitrary desktop automation, credentials or unrestricted computer control is introduced.

## Real gameplay

V16 retains the existing real-input runtime. Real input remains opt-in with `QYNL_DRY_RUN=0`.

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
│   ├── executor.py
│   └── input_adapter.py
├── memory/
├── safety/
├── evals/
└── docs/
    └── V16.md
```

## Tests

V16 adds tests for:

- low-confidence recovery
- recovery budget exhaustion
- negative-memory retrieval
- action rate limiting

Run the complete test suite before real-input testing.

## Limitations

V16 improves failure handling and adaptive control but does not guarantee that its diagnosis is correct. Recovery is deliberately bounded and conservative. Actual Minecraft performance still depends on perception, planning models, latency, Minecraft version/UI and task complexity.

## License

Not specified yet.
