# Qynl Agent V11

Qynl is a **Minecraft-only AI agent that closes the gameplay loop**: capture Minecraft, perceive the game, choose one bounded action, validate it, execute it, verify the result, remember the outcome, and recover when progress stalls.

## V11: adaptive closed-loop gameplay

```text
Minecraft
   ↓
MSS capture
   ↓
Vision model
   ↓
State signature + goal context
   ↓
Planner
   ↓
MinecraftAction
   ↓
ActionPolicy
   ↓
Force ESC
   ↓
Minecraft executor
   ↓
new screenshot
   ↓
result verification
   ↓
episode memory
   ↓
normal planning OR recovery
```

V11 is an improvement release, not a new permission model. It keeps the V10 Minecraft-only boundary and makes the agent less likely to blindly repeat bad actions.

## V11 improvements

- 🔁 **Closed-loop action verification**: every executed action is followed by another visual observation
- 🧠 **Episode memory**: stores bounded before/action/after/outcome records
- 🛑 **Stuck detection**: detects repeated visual states
- 🔧 **Recovery planning**: switches to a recovery strategy after repeated non-progress
- 🚫 **No blind retries**: recovery receives recent failure reasons
- 📋 **Canonical action parser**: one strict parser for model output
- 🛡️ **Policy re-validation** immediately before execution
- 🚨 **Force ESC** remains independent of the model
- 🧪 **V11 tests** for parser safety and stuck detection

## What V11 fixes conceptually

V10 already had the real path from screenshot to model to Minecraft input. The weak point was that an executed action was not meaningfully evaluated before the next decision.

V11 changes that:

```text
Action: press W for 250 ms
        ↓
Minecraft changes?
        ↓
YES → remember successful transition
NO  → remember failure
        ↓
Repeated failures?
        ↓
YES → recovery mode
NO  → normal planning
```

This matters because Minecraft is stateful. A good agent cannot assume that an action worked just because the input API reported that it was sent.

## Memory

`minecraft/v11_agent.py` provides a bounded `V11Memory` containing episodes:

```text
before visual state
      ↓
action
      ↓
after visual state
      ↓
success / failure
      ↓
reason
```

Memory is intentionally bounded so an endless Minecraft session does not create an endless in-memory history.

The memory currently improves **context and recovery**. It does not silently train or rewrite model weights.

## Stuck detection

`StuckDetector` tracks recent visual signatures. If several recent observations collapse into the same small set of states, V11 enters recovery mode.

Recovery is not allowed to bypass the normal safety pipeline. Recovery still produces one ordinary `MinecraftAction`, which must pass `ActionPolicy` and Force ESC.

## Recovery behavior

Recovery prompts tell the model:

- the agent is stuck
- what recent failures occurred
- choose one small reversible action
- do not repeat a failed action unless the visible situation changed
- output only the canonical Minecraft action JSON

This prevents the classic autonomous-agent strategy of pressing W repeatedly for several minutes while confidently accomplishing absolutely nothing.

## Canonical action schema

The model can request only:

```json
{"type":"key","key":"w","duration_ms":250}
```

```json
{"type":"mouse_move","x":35,"y":-8}
```

```json
{"type":"mouse_button","button":"left","duration_ms":80}
```

```json
{"type":"wait","duration_ms":150}
```

Unknown types, malformed JSON and malformed fields are rejected.

## Minecraft-only boundary

The model can reason about Minecraft screenshots, Minecraft visual observations, Minecraft goals, bounded Minecraft state/history and Minecraft actions.

It does not receive shell access, arbitrary desktop automation, process creation, unrestricted filesystem access, credentials, or generic computer-control tools.

## Safety chain

```text
Model output
    ↓
Strict parser
    ↓
MinecraftAction
    ↓
ActionPolicy
    ↓
Force ESC
    ↓
Minecraft executor
```

Force ESC cannot be disabled or cleared by the model.

## Real gameplay

V11 retains the V10 real runtime path and adds the adaptive controller around it. Real input remains opt-in with `QYNL_DRY_RUN=0`.

Start with dry-run and a dedicated Minecraft test world before enabling real input.

## Project structure

```text
AgentQynl/
├── apps/desktop/           # TSX desktop UI
├── core/
├── minecraft/
│   ├── real_capture.py     # MSS capture
│   ├── observation.py      # Minecraft observations
│   ├── vision.py           # vision contract
│   ├── providers.py        # provider adapters
│   ├── v10_provider.py     # multimodal provider
│   ├── planner.py          # structured planning
│   ├── goals.py            # goal/context management
│   ├── v11_model.py        # strict parser + recovery prompt
│   ├── v11_agent.py        # adaptive closed-loop controller
│   ├── executor.py         # safe/real executors
│   └── input_adapter.py    # Minecraft-only input
├── memory/
├── safety/
│   └── action_policy.py
├── evals/
└── docs/
```

## Tests

V11 adds tests covering:

- rejection of non-Minecraft action payloads
- parsing of canonical Minecraft actions
- repeated-state stuck detection

Run the project's test suite before real-input testing.

## Important limitation

V11 makes the **runtime architecture** substantially more robust. It does not magically turn every vision model into a Minecraft pro. Actual skill still depends on the chosen model, prompt, capture quality, latency, Minecraft version/UI, and task complexity.

The difference is that V11 can now detect when an action appears not to have produced progress and react instead of blindly assuming success.

## License

Not specified yet.
