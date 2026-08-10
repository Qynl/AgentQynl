# Qynl Agent V13

Qynl is a **Minecraft-only AI agent with temporal perception**. It captures Minecraft, understands the current scene, tracks what changed across frames, chooses one bounded action, validates it, executes it, and feeds the resulting state back into planning.

## V13: temporal world awareness

V13 builds directly on the V12 adaptive loop. The major improvement is that the agent no longer treats screenshots as isolated observations. It maintains a short-lived temporal state and gives the planner explicit state deltas, recent history, confidence, entities, UI, landmarks and hazards.

```text
Minecraft
   ↓
Screenshot
   ↓
Vision
   ↓
Temporal State Tracker
   ↓
Current State + Delta + Recent States
   ↓
Goal + Planner Evidence
   ↓
ONE MinecraftAction
   ↓
ActionPolicy
   ↓
Force ESC
   ↓
Minecraft
   ↓
new screenshot
   ↓
state transition
   ↓
next decision
```

## V13 improvements

- 👁️ **Temporal perception** instead of isolated screenshots
- 🧍 **Entity observations** with confidence and position hints
- 🧠 **Short-term world-state history**
- 🔎 **State delta detection** for entities, UI, landmarks and hazards
- 📉 **Confidence tracking over time**
- 🎯 **Temporal planner evidence**
- 🔁 **Recent failure context** in planning
- 🧪 V13 temporal perception tests
- 📚 Complete V13 documentation

## Why temporal perception matters

A single frame can be ambiguous. A sequence provides evidence about causality:

```text
Frame 1 → tree ahead
Frame 2 → tree closer
Frame 3 → tree damaged
Frame 4 → log disappeared
```

Instead of merely asking "what is on screen?", V13 can give the planner information about **what changed**.

This is particularly useful for:

- movement
- breaking blocks
- entities moving
- inventory/UI changes
- hazards appearing/disappearing
- camera changes
- verifying whether an action had an observable effect

## State model

`minecraft/v13_state.py` provides:

- `EntityObservation`
- `TemporalState`
- `StateDelta`
- `TemporalStateTracker`

A `TemporalState` contains:

```text
summary
entities
landmarks
hazards
visible UI
confidence
frame index
```

A `StateDelta` describes what changed since the previous observation.

The history is bounded so long-running sessions do not accumulate unlimited state in memory.

## Planner

`minecraft/v13_planner.py` builds `PlannerEvidence` containing:

- current state
- state delta
- recent states
- recent failures

The planner is instructed to:

- use temporal evidence instead of guessing
- choose one small action
- prefer actions whose effects can be verified
- be cautious when confidence is low
- avoid repeating failed actions without evidence that the situation changed

The model still outputs only a structured Minecraft action.

## Integrated controller

`minecraft/v13_controller.py` connects the temporal tracker to the existing runtime:

```text
Vision
  ↓
TemporalStateTracker
  ↓
PlannerEvidence
  ↓
Model
  ↓
MinecraftAction
  ↓
Policy
  ↓
Force ESC
  ↓
Executor
```

It has a bounded step budget and records recent failures for subsequent planning decisions.

## Action schema

The model may only request:

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

Unknown or malformed actions are rejected before execution.

## Minecraft-only boundary

The model receives Minecraft-focused visual state, goals and bounded action history.

It does not receive shell access, arbitrary desktop automation, process creation, unrestricted filesystem access, credentials, or generic computer-control tools.

## Safety chain

```text
Model
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

Force ESC remains independent of the model and cannot be disabled by it.

## Real gameplay

V13 retains the existing real-input runtime. Real input remains opt-in with `QYNL_DRY_RUN=0`.

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
│   ├── executor.py
│   └── input_adapter.py
├── memory/
├── safety/
├── evals/
└── docs/
    └── V13.md
```

## Tests

V13 adds tests covering:

- temporal entity changes
- planner evidence generation

Run the complete test suite before real-input testing.

## Important limitation

V13 substantially improves temporal state awareness, but perception quality still depends on the selected vision model, capture quality, latency, Minecraft version/UI and task complexity. State change is evidence, not automatic proof that a goal was completed.

## License

Not specified yet.
