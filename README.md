# Qynl Agent V21

Qynl is a **Minecraft-only AI agent with temporal perception, hierarchical tasks, explicit goal evaluation, episodic skill memory, recovery, a persistent world model, utility planning, prediction and information-gathering behavior**.

## V21: Prediction + Exploration

V21 adds a decision layer for uncertainty. Qynl can now distinguish between **acting toward the goal** and **gathering information needed to act toward the goal**.

```text
Minecraft screen
      ↓
Vision
      ↓
World Model + Spatial Memory
      ↓
Goal + Skill Memory
      ↓
Candidate Planner
      ↓
Transition Predictor
      ↓
V21 Controller
   ┌──┼─────────────┐
 goal  explore   safe-stop
  ↓      ↓           ↓
rank   reobserve   no action
  ↓    look around
  ↓    small scan
  ↓      ↓
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
Verification
      ↓
World Model update
```

## V21 improvements

- 🧭 **Bounded Spatial Memory** for relative landmark observations
- 🔁 **Landmark revisitation detection**
- 🔎 **Information-gain exploration manager**
- 👁️ **Uncertainty-driven re-observation**
- 🔄 **Repeated-state exploration**
- 🧠 **Transition outcome prediction**
- ⚖️ **Expected progress vs. risk ranking**
- 🛑 **Hazard-aware safe stop**
- 🎯 **Dedicated V21 decision controller**
- 🧪 V21 exploration/prediction tests
- 📚 Complete V21 documentation

## Spatial Memory

`minecraft/v21_spatial_memory.py` stores bounded relative observations such as:

```text
village → ahead
village → left
forest  → behind
```

Each observation includes confidence and a temporal tick. This gives Qynl evidence about revisitation without pretending screen-only perception provides exact world coordinates.

## Exploration

`minecraft/v21_exploration.py` handles situations where acting is less useful than learning more about the current scene.

```text
low confidence   → reobserve
repeated state   → look around
unknown area     → small scan
hazard detected  → retreat or stop
sufficient info  → continue goal
```

Exploration is deliberately bounded. It is not permission to wander forever.

## Transition Prediction

`minecraft/v21_predictor.py` estimates each existing candidate's:

```text
expected progress
uncertainty
risk
```

The predictor is a ranking signal, not a Minecraft simulator. It does not claim knowledge that was not observed.

## V21 Controller

`minecraft/v21_controller.py` combines confidence, world-state repetition, unknown-area signals, hazards and candidate predictions.

```text
Enough information + safe
        ↓
    choose action

Not enough information
        ↓
      explore

Danger
        ↓
    safe stop

No viable action
        ↓
      replan
```

The controller never directly bypasses the normal execution gates.

## V20 → V21

```text
V20:
Observe → World Model → Generate Options → Rank → Act → Verify

V21:
Observe → World Model + Spatial Memory
       → Generate Options
       → Predict outcomes
       → Decide: ACT or EXPLORE or STOP
       → Safety gates
       → Verify
       → Update
```

The important change is that **uncertainty becomes an explicit decision variable**.

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
V21  Prediction + spatial memory + information-gain exploration
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

Exploration, prediction and spatial memory cannot bypass this chain.

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
│   ├── executor.py
│   └── input_adapter.py
├── memory/
├── safety/
├── evals/
└── docs/
    └── V21.md
```

## Tests

V21 adds tests for:

- spatial landmark revisitation
- uncertainty-driven exploration
- risk-aware candidate prediction
- hazard safe-stop

Run the complete test suite before real-input testing.

## Limitations

V21 predictions are estimates and spatial memory is coarse. Qynl cannot infer unseen Minecraft state with certainty. Exploration is bounded and conservative, and actual gameplay quality still depends on perception, models, latency, Minecraft version/UI and the environment.

## License

Not specified yet.
