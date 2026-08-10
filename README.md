# Qynl Agent V12

Qynl is a **Minecraft-only AI agent that closes the gameplay loop**: capture Minecraft, perceive the game, choose one bounded action, validate it, execute it, verify the result, track state transitions, and adapt when progress stalls.

## V12: adaptive state + strategy

V12 builds directly on V11. It does not replace the real Minecraft runtime. It adds a richer state representation and a strategy layer that helps the planner react to uncertainty, repeated states and repetitive actions.

```text
Minecraft
   ↓
Vision
   ↓
GameState
   ↓
Goal + Strategy
   ↓
Planner
   ↓
MinecraftAction
   ↓
ActionPolicy
   ↓
Force ESC
   ↓
Minecraft
   ↓
new observation
   ↓
Transition + progress signal
   ↓
Memory
   ↓
Strategy update
   ↓
next action
```

## V12 improvements

- 🧠 **Normalized GameState** with summary, landmarks, hazards, UI and confidence
- 🔄 **Transition tracking** between observations
- 📈 **Visual novelty/progress heuristic**
- 🎯 **Adaptive strategy controller**
- 🤔 **Low-confidence cautious mode**
- 🧭 **Repeated-state exploration mode**
- 🔁 **Repeated-action variation mode**
- 🧪 V12 state/strategy tests
- 📚 Complete V12 documentation

## State tracking

`minecraft/v12_state.py` converts the vision result into a normalized `GameState`.

A transition contains:

```text
before state
    ↓
action
    ↓
after state
    ↓
changed?
    ↓
novelty score
```

The tracker keeps a bounded history, preventing a long Minecraft session from growing memory forever.

The novelty score is a **heuristic**, not proof that a goal succeeded. For example, turning around changes the image but does not magically mean the house is built. Humanity remains trapped in the age of needing actual verification.

## Adaptive strategy

`minecraft/v12_strategy.py` gives the planner a mode based on current conditions.

### Cautious

When confidence is below the configured threshold, the agent is told to re-observe and prefer short, reversible actions.

### Explore

When the same visual state repeats several times, the agent is encouraged to change camera or position rather than continuing the same loop.

### Vary

When the same action type repeats too often, the strategy asks for a different useful Minecraft action.

### Normal

When the state is not repeating and confidence is acceptable, the agent continues toward its current goal.

The strategy layer **does not execute anything**. It only changes planning context. The action parser, ActionPolicy, Force ESC and executor remain authoritative.

## V11 → V12

V11 added:

- action verification
- episodic memory
- stuck detection
- recovery planning

V12 adds:

- richer state representation
- explicit transition history
- novelty/progress signal
- confidence-aware strategy
- action repetition avoidance
- exploration behavior for repeated states

## Minecraft-only boundary

The agent can reason about Minecraft screenshots, Minecraft visual observations, Minecraft goals, bounded Minecraft state/history and Minecraft actions.

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

V12 retains the V10/V11 real runtime path. Real input remains opt-in with `QYNL_DRY_RUN=0`.

Start with dry-run and a dedicated Minecraft test world before enabling real input.

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
│   ├── executor.py
│   └── input_adapter.py
├── memory/
├── safety/
├── evals/
└── docs/
    └── V12.md
```

## Tests

V12 adds tests for:

- state transition novelty
- progress scoring
- repeated-action variation
- low-confidence cautious mode

Run the project test suite before real-input testing.

## Important limitation

V12 improves the agent's control loop and state awareness. It does not claim that a vision model automatically understands every Minecraft scene or that visual novelty equals task success. Actual gameplay quality still depends on model quality, capture quality, latency, Minecraft version/UI and task complexity.

The goal of V12 is to make those limitations manageable: observe more carefully, track what changed, avoid obvious loops, and give the planner better information for the next decision.

## License

Not specified yet.
