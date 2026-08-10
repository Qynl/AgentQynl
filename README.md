# Qynl Agent V6

Qynl is a **Minecraft-only AI agent** whose entire job is to play Minecraft: see the game, understand the current situation, pursue a Minecraft goal, act through a restricted Minecraft controller, remember useful experiences, and improve through evaluation.

It is **not** a general computer-use assistant. The model is never given arbitrary desktop, shell, process, filesystem, or unrestricted input control.

> **Status: V6.** V6 adds the perception/goal/planning architecture needed to turn the V5 physical control path into a real Minecraft agent. Real autonomy remains opt-in and should be tested in a dedicated Minecraft environment.

## V6 highlights

- 🎮 Minecraft-only agent boundary
- 👁️ Minecraft vision/perception contract
- 🧠 Goal-conditioned planning context
- 🔁 Observation → vision → goal → plan → safety → action loop
- 🖱️ Restricted real Minecraft input
- 📸 Opt-in MSS capture
- 🧩 NVIDIA NIM, Ollama and OpenAI-compatible provider architecture
- 🛡️ Deny-by-default ActionPolicy
- 🚨 Independent operator Force ESC
- 🧪 Dry-run executor
- 📝 Bounded action audit
- 🧠 Episodic learning foundation
- 🖥️ TSX desktop control surface

## The V6 architecture

```text
                          ┌──────────────────────┐
                          │      Minecraft       │
                          └──────────┬───────────┘
                                     │
                              Screen Capture
                                     ▼
                          ┌──────────────────────┐
                          │ MinecraftObservation │
                          └──────────┬───────────┘
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │   Vision Provider    │
                          │ landmarks / hazards  │
                          │ UI / confidence      │
                          └──────────┬───────────┘
                                     │
                                     ▼
┌──────────────┐          ┌──────────────────────┐
│ NIM / Ollama │─────────▶│    Goal + Planner    │
│ Compatible   │          │ Minecraft-only       │
└──────────────┘          └──────────┬───────────┘
                                     │
                              MinecraftAction
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │    ActionPolicy      │
                          │    DENY BY DEFAULT   │
                          └──────────┬───────────┘
                                     │
                               Force ESC
                                     │
                               rate / approval
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │ Minecraft Executor   │
                          └──────────┬───────────┘
                                     │
                                     ▼
                                 Minecraft
                                     │
                                     └──────► next observation
```

The model proposes a **Minecraft action**, not a computer action. The executor is the final authority.

## What changed from V5

V5 gave Qynl the physical path to send restricted input. That alone does not make a competent Minecraft player. V6 adds the missing agent-level structure:

### 1. Minecraft vision contract

`minecraft/vision.py` defines `MinecraftVisionProvider` and `VisualAnalysis`.

A vision provider can return:

- visual summary
- visible Minecraft UI elements
- landmarks
- hazards
- confidence

The default `NullVisionProvider` refuses to invent observations when no model is configured.

### 2. Goal manager

`minecraft/goals.py` separates the Minecraft objective from the model's reasoning.

A goal contains:

- goal text
- success conditions
- maximum planning steps

The planner receives a `PlanningContext` containing the goal, visual analysis, recent Minecraft actions, and current step.

### 3. Real V6 agent loop

`minecraft/loop_v6.py` connects the pieces:

```text
Capture
  ↓
Observation
  ↓
Vision
  ↓
Goal context
  ↓
Planner
  ↓
MinecraftAction
  ↓
ActionPolicy
  ↓
Force ESC
  ↓
Executor
  ↓
Result
  ↓
Next observation
```

Force ESC is checked before observation and again immediately before execution.

## Minecraft-only permissions

The model may receive Minecraft screenshots, Minecraft-focused visual analysis, Minecraft inventory/state, health/food information, the active Minecraft goal, bounded Minecraft action history, and bounded learning experiences.

The model must not receive arbitrary desktop screenshots, arbitrary application control, shell execution, process creation, unrestricted filesystem access, unrestricted keyboard/mouse APIs, credentials, or secrets.

The entire permission boundary is designed around **one application: Minecraft**.

## V6 perception

The capture layer remains explicitly scoped to the configured Minecraft surface. A future production capture adapter should identify the selected Minecraft window/region and reject ambiguous or unavailable targets.

The vision layer is provider-independent. A vision result is treated as **advisory perception**, not as permission to act. The action policy remains authoritative.

## V6 planning

Qynl separates:

**Goal:** What are we trying to accomplish in Minecraft?

**Perception:** What appears to be happening in Minecraft right now?

**Action:** What single bounded Minecraft action should happen next?

This makes each stage independently testable instead of hiding everything inside one mysterious AI loop.

## Actual gameplay path

With the opt-in real adapters enabled:

```text
Minecraft window
      ↓
MSS capture
      ↓
Minecraft observation
      ↓
Vision model
      ↓
Goal-conditioned planner
      ↓
Structured MinecraftAction
      ↓
ActionPolicy
      ↓
Force ESC
      ↓
PyAutoGUI Minecraft adapter
      ↓
Minecraft
```

V6 is therefore much closer to an actual playing agent than V5. It still requires a properly connected vision/planning provider and task-specific evaluation before autonomous play should be trusted.

## Minecraft skills roadmap

The agent should be evaluated incrementally rather than thrown into a fresh survival world and expected to discover civilization in one afternoon.

### Basic control

- camera/look control
- forward/back/strafe
- jumping
- sprinting
- reliable stopping

### Survival fundamentals

- locate trees
- break logs
- collect drops
- craft planks
- craft crafting table
- craft tools
- locate stone
- collect food

### Exploration

- recognize terrain
- navigate toward landmarks
- avoid hazards
- recover from getting stuck
- maintain a useful position

### Mining

- identify mineable blocks
- choose safe routes
- manage tool durability
- collect ores
- return toward a known location

### Inventory/crafting

- recognize inventory slots
- move items safely
- choose recipes
- verify crafting results
- avoid accidental item loss

### Advanced

- controlled combat
- caves
- villages
- Nether preparation
- long-horizon objectives
- multi-skill task composition

## Learning system

V6 keeps learning **structured and bounded**.

An experience can contain:

```text
Goal
Observation
Visual analysis
Proposed action
Validated action
Outcome
Reward / feedback
```

The system can later retrieve relevant experiences for similar Minecraft goals. Ordinary gameplay does **not** silently rewrite model weights. Learning experiments should be measurable and reversible.

## Force ESC 🚨

Force ESC is an independent operator emergency stop. The AI cannot trigger it, disable it, clear it, or override it.

The executor checks the escape latch immediately before sending input. The desktop app should expose a large emergency control and local keyboard shortcut. If Force ESC is engaged, real Minecraft input remains blocked until an explicit operator reset.

## Desktop app

The TSX desktop app is the control center for the Minecraft agent:

- **Dashboard:** goal, state, current step, confidence
- **Minecraft:** capture preview and connection
- **Vision:** visual analysis and confidence
- **Planner:** current plan and proposed action
- **Actions:** action queue and validation results
- **Memory:** experiences and retrieval
- **Learning:** rewards and evaluations
- **Providers:** NIM/Ollama/compatible configuration
- **Safety:** Safe Mode, approvals, limits and Force ESC
- **Settings:** Minecraft-specific configuration

The UI is not the security boundary. Python core/safety code validates actions independently.

## Safety model

Every real action must pass:

```text
Model proposal
     ↓
Structured action parser
     ↓
Minecraft-only ActionPolicy
     ↓
Rate / duration limits
     ↓
Force ESC checkpoint
     ↓
Optional operator approval
     ↓
Minecraft executor
```

Unknown actions are rejected. The model cannot provide executable code or arbitrary input commands.

## Providers

Qynl is provider-agnostic at the planning/vision layer:

- **NVIDIA NIM**
- **Ollama** for local models
- **OpenAI-compatible APIs**

A provider outputs structured Minecraft reasoning/actions. It never receives generic computer-control APIs. Credentials remain outside Git.

## Project structure

```text
AgentQynl/
├── apps/
│   └── desktop/          # TSX desktop UI
├── core/                 # settings, audit, agent abstractions
├── minecraft/
│   ├── capture.py        # capture protocol
│   ├── real_capture.py   # opt-in MSS capture
│   ├── observation.py    # Minecraft observation
│   ├── vision.py         # V6 vision contract
│   ├── goals.py          # goal/context management
│   ├── executor.py       # safe executors
│   ├── input_adapter.py  # restricted Minecraft input
│   ├── run_v5.py         # V5 loop
│   └── loop_v6.py        # V6 agent loop
├── memory/               # episodic learning
├── safety/               # ActionPolicy + Force ESC
├── evals/                # evaluation and safety tests
└── docs/
    └── V6.md             # V6 architecture
```

## Roadmap

### V6.0 agent architecture

- [x] Minecraft-only scope
- [x] Real opt-in capture
- [x] Restricted real input
- [x] Vision provider contract
- [x] Goal manager
- [x] Goal-conditioned planning context
- [x] Observe → perceive → plan → validate → act loop
- [x] Force ESC integration
- [x] Dry-run executor
- [x] V6 documentation

### V6.1 model integration

- [ ] NVIDIA NIM vision adapter
- [ ] Ollama vision adapter
- [ ] OpenAI-compatible vision adapter
- [ ] Structured planner output parser
- [ ] Automatic model confidence handling
- [ ] Model failure/retry policy

### V6.2 Minecraft skills

- [ ] Camera control
- [ ] Navigation
- [ ] Wood gathering
- [ ] Crafting
- [ ] Food gathering
- [ ] Mining
- [ ] Inventory management
- [ ] Controlled combat

### V6.3 learning

- [ ] Goal-conditioned experience retrieval
- [ ] Skill memory
- [ ] Reward/evaluation system
- [ ] Failure recovery
- [ ] Replayable benchmark worlds

### V7

- [ ] Long-horizon survival agent
- [ ] Persistent world knowledge
- [ ] Multi-skill planning
- [ ] Stronger world-state estimation
- [ ] Autonomous Minecraft benchmark suite

## Development

Real computer input is opt-in. Start with dry-run mode and a test world, verify Force ESC, verify the capture region, then enable one skill at a time.

The repository does not claim that a model is automatically good at Minecraft merely because the control loop exists. V6 builds the architecture needed to make competence measurable and trainable.

## License

Not specified yet.
