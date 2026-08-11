# Qynl Agent V14

Qynl is a **Minecraft-only AI agent with temporal perception, hierarchical tasks, explicit goal evaluation and episodic skill memory**.

## V14: task + skill layer

V14 builds on V13 and adds the missing longer-term control layer:

```text
User goal
   ↓
Task Decomposer
   ↓
Subtask
   ↓
Temporal Minecraft state
   ↓
Relevant past skills
   ↓
Planner
   ↓
ONE MinecraftAction
   ↓
ActionPolicy
   ↓
Force ESC
   ↓
Minecraft
   ↓
New observation
   ↓
Goal Evaluator
   ↓
Success / failure evidence
   ↓
Skill Memory
   ↓
next subtask / recovery
```

## V14 improvements

- 🎯 **Hierarchical task decomposition** into bounded observable subtasks
- ✅ **Explicit goal evaluator** that can say "not proven" instead of assuming success
- 🧠 **Episodic skill memory** for reusable experience
- 🔎 **Relevant-memory retrieval** based on the current goal and situation
- 📈 **Outcome/reward records** for past attempts
- 🔄 **Subtask progression** only after explicit evaluation
- 🧪 V14 memory/task tests
- 📚 Complete V14 documentation

## Example task flow

A large goal such as `build a small shelter` can become:

```text
1. collect wood
       ↓ verified
2. craft tools
       ↓ verified
3. collect blocks
       ↓ verified
4. choose location
       ↓ verified
5. build shelter
       ↓ verified
6. check result
```

The exact subtasks are generated conservatively and capped. Model text is treated as data and never executed as code.

## Goal evaluation

`minecraft/v14_evaluator.py` provides a separate evaluator for subtasks.

It compares the before/after observations against the subtask's success condition and returns:

```text
success
score: 0..1
evidence
```

If the evaluator is uncertain or malformed, V14 defaults to **failure / not proven**. That is intentional. A bot confidently declaring "I built the house" while standing in a forest is not artificial intelligence, it is customer support.

## Episodic skill memory

`minecraft/v14_memory.py` stores bounded experiences:

```text
goal
situation
action type
outcome
reward
lesson
```

When Qynl encounters a similar goal/situation, it can retrieve relevant successful or failed experiences as planning context.

This is **retrieval-based memory**, not automatic model-weight training. The model does not silently modify itself during gameplay.

## Why V14 matters

V13 gave Qynl short-term temporal awareness:

```text
What changed recently?
```

V14 adds longer-term task awareness:

```text
What am I trying to accomplish?
What subtask am I on?
Did it actually succeed?
What worked in similar situations before?
```

That makes the architecture substantially closer to a task-oriented Minecraft agent.

## Safety

V14 does not expand computer permissions.

All model-generated actions still pass through:

```text
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

Task decomposition, evaluation and memory are planning data. They cannot directly execute OS commands.

## Minecraft-only boundary

The agent is limited to Minecraft-focused visual state, goals, bounded history and Minecraft actions.

It does not receive shell access, arbitrary desktop automation, process creation, unrestricted filesystem access, credentials, or generic computer-control tools.

## Real gameplay

V14 retains the existing real-input runtime. Real input remains opt-in with `QYNL_DRY_RUN=0`.

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
│   ├── executor.py
│   └── input_adapter.py
├── memory/
├── safety/
├── evals/
└── docs/
    └── V14.md
```

## Tests

V14 adds tests for:

- successful skill retrieval
- task-plan progression

Run the complete test suite before real-input testing.

## Limitations

V14 still depends on the selected vision/planning model, capture quality, latency, Minecraft version/UI and task complexity. Memory is retrieval, not magical self-training, and evaluation is conservative when visual evidence is ambiguous.

## License

Not specified yet.
