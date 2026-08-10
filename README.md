# Qynl Agent V7

Qynl is a **Minecraft-only AI agent** built to actually play Minecraft rather than merely demonstrate computer-control plumbing.

V7 focuses on the things that make an agent competent: focused perception, short-horizon action, frequent re-observation, state tracking, stuck detection, reusable micro-skills, strict structured outputs, and conservative recovery.

It is **not** a general computer-use assistant. The model is never given arbitrary desktop, shell, process, filesystem, or unrestricted input control.

> **Status: V7.** V7 is the first version designed around a practical closed-loop gameplay controller. Real autonomy remains opt-in and should be validated in a dedicated Minecraft test world.

## V7 highlights

- 🎮 Minecraft-only agent boundary
- 👁️ Focused visual perception
- 🧠 Goal-conditioned planning
- 🔄 Frequent observe → act → re-observe loop
- 🧭 Rolling Minecraft state tracker
- 🛑 Stuck-state detection
- 🧩 Reusable Minecraft micro-skills
- 🎯 Small, reversible actions instead of giant open-loop plans
- 📋 Strict JSON action output
- 🛡️ Canonical deny-by-default ActionPolicy
- 🚨 Independent Force ESC
- 🧪 Dry-run execution
- 📝 Bounded audit and episodic memory foundations
- 🖥️ TSX desktop control surface

## Why V7 should play better

A weak computer agent often does this:

```text
Screenshot → think for ages → execute 20 actions → hope
```

V7 is designed to do this:

```text
Screenshot
   ↓
Understand
   ↓
Choose ONE small action
   ↓
Execute
   ↓
Screenshot again
   ↓
Did the world change as expected?
   ↓
Update state
   ↓
Choose the next action
```

This is much better suited to Minecraft because camera orientation, collisions, block breaking, menus, terrain, mobs, and inventory state can change after almost every action.

## V7 architecture

```text
                         ┌──────────────────────┐
                         │      Minecraft       │
                         └──────────┬───────────┘
                                    │
                              MSS Capture
                                    ▼
                         ┌──────────────────────┐
                         │ MinecraftObservation │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Vision Model      │
                         │ UI / landmarks /     │
                         │ hazards / confidence │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   State Tracker      │
                         │ history / stuck      │
                         └──────────┬───────────┘
                                    │
                                    ▼
┌──────────────┐         ┌──────────────────────┐
│ NIM / Ollama │────────▶│ Goal + Planner       │
│ Compatible   │         │ one next action      │
└──────────────┘         └──────────┬───────────┘
                                    │
                              MinecraftAction
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   ActionPolicy       │
                         │   DENY BY DEFAULT    │
                         └──────────┬───────────┘
                                    │
                               Force ESC
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Minecraft Executor   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                                 Minecraft
```

## V7 improvements

### 1. Correct action contract

V7 uses the repository's actual `MinecraftAction` schema everywhere:

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

Provider output is treated as untrusted data and parsed into this schema. It is never executed as code.

### 2. Short-horizon control

The planner is explicitly instructed to select **one small next action** and then wait for another observation. This reduces catastrophic open-loop behavior.

### 3. State tracking

`minecraft/state.py` maintains a rolling history of:

- frame IDs
- visual summaries
- landmarks
- hazards
- confidence
- timing

It can detect repeated identical visual states, giving the controller a signal that it may be stuck.

### 4. Micro-skills

`minecraft/skills.py` provides reusable primitives such as:

- walking
- looking
- interacting
- stopping

Higher-level Minecraft skills can compose these rather than inventing raw input sequences every time.

### 5. Focused Minecraft prompt

`minecraft/prompts.py` tells the model exactly what it is: a Minecraft player. It explicitly rejects shell, filesystem, code, and generic computer actions and requires structured JSON output.

## Real gameplay loop

```text
1. Capture Minecraft
2. Build observation
3. Ask vision model what is visible
4. Update rolling state
5. Check for stuck/recovery conditions
6. Add current goal + recent actions
7. Ask planner for ONE next action
8. Parse structured JSON
9. Run ActionPolicy
10. Check Force ESC
11. Execute the action
12. Observe again
13. Evaluate whether the world changed as expected
14. Repeat
```

The important part is step 12. Qynl does not assume that pressing a key means the intended thing happened.

## Practical skill progression

V7 is designed to build competence from small verified skills.

### Movement

- forward/back/strafe
- jumping
- sprinting
- camera control
- stopping
- recovering from collisions

### First survival loop

```text
Find tree
 ↓
Approach tree
 ↓
Look at trunk
 ↓
Hold attack briefly
 ↓
Observe block/dropped item change
 ↓
Repeat
 ↓
Open inventory
 ↓
Craft
 ↓
Verify result
```

Every stage is observable and recoverable.

### Later skills

- tool crafting
- food gathering
- navigation
- mining
- inventory management
- caves
- villages
- controlled combat
- Nether preparation
- long-horizon survival

## Learning

V7 is designed around **experience retrieval and evaluation**, not uncontrolled self-modification.

A useful episode can contain:

```text
Goal
Observation
Visual analysis
State before
Action
Policy decision
Result
State after
Reward / feedback
```

The agent can later use successful experiences as context for similar Minecraft situations.

Model weights are not silently changed by normal gameplay.

## Recovery behavior

A competent player needs to recover, not just act.

V7 provides the foundation for:

- detecting repeated frames
- abandoning a failed micro-plan
- re-observing after unexpected results
- using a safe wait/stop action
- changing camera/movement strategy
- returning to the current goal after recovery

Future skill evaluators should score recovery separately from task success.

## Force ESC 🚨

Force ESC remains completely independent from the model.

The AI cannot trigger, disable, clear, or override it.

The intended execution boundary is:

```text
Model
 ↓
Structured Action
 ↓
ActionPolicy
 ↓
Force ESC
 ↓
Minecraft Executor
```

If Force ESC is engaged, real Minecraft input stays blocked until an explicit operator reset.

## Provider architecture

V7 remains provider-neutral:

- **NVIDIA NIM**
- **Ollama**
- **OpenAI-compatible vision/planning APIs**

Providers should only implement perception/planning interfaces. They never receive arbitrary computer APIs.

## Desktop app

The TSX desktop app is intended to expose the entire Minecraft agent clearly:

- **Dashboard**: goal, state, confidence, current action
- **Minecraft**: capture preview
- **Vision**: current analysis
- **State**: landmarks, hazards, history, stuck detector
- **Planner**: current context and proposed action
- **Actions**: validation and execution history
- **Skills**: reusable Minecraft skills
- **Memory**: experiences
- **Learning**: rewards/evaluations
- **Providers**: model configuration
- **Safety**: limits, approvals and Force ESC

The UI is not the security boundary. Core Python safety code remains authoritative.

## Safety

Every action passes through:

```text
Untrusted model output
        ↓
Strict JSON parser
        ↓
MinecraftAction
        ↓
Deny-by-default ActionPolicy
        ↓
Rate/duration limits
        ↓
Force ESC checkpoint
        ↓
Minecraft executor
```

No arbitrary shell commands, executable model output, unrestricted filesystem operations, or general desktop control are exposed.

For real autonomous testing, use a dedicated Minecraft instance/world and verify Force ESC before enabling real input.

## Project structure

```text
AgentQynl/
├── apps/desktop/         # TSX desktop UI
├── core/                 # agent/settings/audit foundations
├── minecraft/
│   ├── capture.py
│   ├── real_capture.py
│   ├── observation.py
│   ├── vision.py
│   ├── providers.py
│   ├── prompts.py
│   ├── planner.py
│   ├── goals.py
│   ├── state.py          # V7 rolling state tracker
│   ├── skills.py         # V7 Minecraft micro-skills
│   ├── executor.py
│   ├── input_adapter.py
│   └── loop_v6.py
├── memory/
├── safety/
├── evals/
└── docs/
```

## Roadmap

### V7.0 closed-loop gameplay

- [x] Minecraft-only scope
- [x] Real opt-in capture
- [x] Restricted Minecraft input
- [x] Vision contract
- [x] Goal manager
- [x] Structured planner
- [x] Canonical action schema
- [x] Rolling state tracker
- [x] Stuck detection foundation
- [x] Minecraft micro-skills
- [x] Focused Minecraft prompts
- [x] Force ESC

### V7.1 actual model adapters

- [ ] NVIDIA NIM vision adapter
- [ ] Ollama vision adapter
- [ ] OpenAI-compatible vision adapter
- [ ] Structured planner transport
- [ ] Confidence-aware action gating
- [ ] Automatic retry/recovery

### V7.2 competence

- [ ] Reliable camera calibration
- [ ] Movement benchmark
- [ ] Wood gathering benchmark
- [ ] Crafting benchmark
- [ ] Food benchmark
- [ ] Navigation benchmark
- [ ] Mining benchmark
- [ ] Inventory benchmark

### V7.3 learning

- [ ] Goal-conditioned experience retrieval
- [ ] Skill memory
- [ ] Outcome scoring
- [ ] Recovery training/evaluation
- [ ] Replayable benchmark worlds

### V8

- [ ] Long-horizon survival
- [ ] Persistent world model
- [ ] Multi-skill planning
- [ ] Stronger Minecraft state estimation
- [ ] Autonomous benchmark suite

## Development

Start in dry-run mode. Verify the Minecraft capture region, verify the action policy, test Force ESC, then enable real input in a dedicated test world.

V7 is designed to make actual gameplay competence possible. It does not pretend that adding an LLM magically teaches Minecraft. Competence comes from good perception, short feedback loops, reliable actions, skills, recovery, and measurable evaluation.

## License

Not specified yet.
