# Qynl Agent

Qynl is a **Minecraft-only AI agent**. Its job is simple: see Minecraft, understand Minecraft, play Minecraft, remember useful experiences, and improve through evaluation.

It is **not** a general computer-use assistant. The agent is intentionally restricted to a configured Minecraft capture surface and a bounded Minecraft action interface.

> **Status: V5.** V5 adds the first real capture, input, and gameplay-loop components. Real computer input remains explicitly opt-in and should be tested in an isolated Minecraft environment.

## V5 highlights

- 🎮 Minecraft-only scope
- 👁️ Real opt-in Minecraft screen capture through MSS
- 🧠 Provider abstraction for NVIDIA NIM, Ollama and OpenAI-compatible endpoints
- 🎯 Structured Minecraft observations and actions
- 🖱️ Restricted real keyboard/mouse Minecraft adapter
- 🔁 Real observe → plan → validate → act loop
- 🛡️ Deny-by-default ActionPolicy
- 🚨 Operator-only Force ESC hard stop
- 🧪 Dry-run executor for safe testing
- 📝 Bounded Minecraft action audit log
- 🧠 Bounded episodic learning foundation
- 🖥️ TSX desktop control surface

## What V5 can actually do

V5 now contains the physical integration path required to let a planner interact with Minecraft:

```text
Minecraft
   ↓
MSS capture of configured Minecraft region
   ↓
MinecraftObservation
   ↓
Vision / reasoning planner
   ↓
MinecraftAction
   ↓
ActionPolicy
   ↓
Force ESC checkpoint
   ↓
Restricted input adapter
   ↓
Minecraft
```

The loop in `minecraft/run_v5.py` performs one bounded action per observation. This is intentionally slower and easier to debug than immediately unleashing a high-frequency autonomous loop upon the unsuspecting block world.

## Minecraft-only boundary

Qynl may eventually receive:

- Minecraft screenshots
- Minecraft-focused structured state
- inventory information
- health and food
- current Minecraft goal
- bounded action history
- bounded learning experiences

Qynl must not receive or control:

- arbitrary desktop windows
- arbitrary applications
- shell commands
- process creation
- unrestricted filesystem operations
- arbitrary keyboard APIs
- arbitrary mouse APIs
- credentials or secrets

The real input adapter accepts only the structured Minecraft actions produced by the safety layer.

## V5 capture

`minecraft/real_capture.py` provides an optional MSS adapter.

The operator configures an explicit capture rectangle. The adapter captures that region only and returns a Minecraft capture frame.

Screenshot persistence is optional. If persistence is disabled, the capture layer does not write screenshots to disk.

The safe `DisabledCapture` remains available and does not inspect the desktop.

## V5 real input

`minecraft/input_adapter.py` provides a restricted PyAutoGUI adapter.

It supports only the action types represented by the existing `MinecraftAction` contract. It does not accept arbitrary shell commands, application names, arbitrary scripts, or model-generated key names outside the policy.

PyAutoGUI's own failsafe remains enabled.

Every real input passes through:

```text
MinecraftAction
      ↓
ActionPolicy
      ↓
Force ESC
      ↓
MinecraftInput
```

## Gameplay loop

`minecraft/run_v5.py` connects the capture and executor layers:

```text
1. Capture Minecraft
2. Create MinecraftObservation
3. Ask the planner for one MinecraftAction
4. Validate the action
5. Check Force ESC
6. Send the restricted input
7. Capture the next observation
8. Repeat
```

The planner is model-agnostic. NVIDIA NIM, Ollama, and compatible providers can be connected through the provider abstraction.

V5 does **not** claim that an arbitrary vision model is already a competent Minecraft player. The physical control loop exists; a strong Minecraft planner and robust visual/state understanding still need to be integrated and evaluated.

## Force ESC 🚨

Force ESC is an **operator-only emergency stop**.

The model cannot:

- trigger it
- clear it
- disable it
- override it

The real input adapter checks it before and after input. The gameplay loop also checks it before planning/execution.

The desktop application should bind Force ESC to a local operator shortcut and keep the control available even if the agent is confused or stuck.

## Safety

Qynl uses a layered safety model:

1. **Minecraft scope** limits what the agent is intended to observe.
2. **Structured actions** prevent free-form model commands from reaching input.
3. **ActionPolicy** denies unknown or excessive actions.
4. **Force ESC** provides an independent operator hard stop.
5. **Executor** is the only layer allowed to send Minecraft input.
6. **Dry-run mode** allows testing without real input.

Use a dedicated Minecraft instance or isolated environment for real-input testing. Do not run experimental computer-control software against a machine containing sensitive applications or data.

## Providers

Qynl is provider-agnostic:

- **NVIDIA NIM**
- **Ollama** for local models
- **OpenAI-compatible APIs**

The provider generates reasoning/structured output. It does not receive direct OS-control APIs.

Credentials must stay outside Git. Never commit `.env`, API keys, access tokens, or private screenshots.

## Learning

Qynl uses bounded episodic memory rather than silently changing model weights during gameplay.

An experience can contain:

```text
Goal
Observation
Proposed action
Validated action
Outcome
Reward / feedback
```

Future versions can add goal-conditioned retrieval, skill memory, reward models, offline training, or fine-tuning without weakening the Minecraft action boundary.

## Desktop application

The desktop UI is built around TSX and is intended to make the Minecraft agent understandable:

- **Dashboard**: current goal and agent status
- **Minecraft**: capture preview and connection state
- **Actions**: proposed/approved/rejected actions
- **Memory**: experiences
- **Learning**: feedback and evaluation
- **Providers**: NIM/Ollama/compatible configuration
- **Safety**: Safe Mode, limits, approvals and Force ESC
- **Settings**: Minecraft agent configuration

The UI is not the safety authority. The core Python layers validate actions independently.

## Project structure

```text
AgentQynl/
├── apps/
│   └── desktop/          # TSX desktop UI
├── core/                 # Agent settings, audit and abstractions
├── minecraft/
│   ├── capture.py        # Capture protocol + safe disabled capture
│   ├── observation.py    # Minecraft observation contract
│   ├── real_capture.py   # Opt-in MSS capture
│   ├── executor.py       # Dry-run + safe executor
│   ├── input_adapter.py  # Restricted real Minecraft input
│   └── run_v5.py         # Observe → act loop
├── memory/               # Bounded episodic learning
├── safety/               # ActionPolicy + Force ESC
├── evals/                # Evaluation and safety tests
└── docs/                 # Versioned architecture notes
```

## Roadmap

### V5.0 real control

- [x] Minecraft-only scope
- [x] Structured observation contract
- [x] Opt-in MSS capture adapter
- [x] Restricted PyAutoGUI Minecraft adapter
- [x] Real observe/act loop
- [x] Dry-run executor
- [x] Deny-by-default ActionPolicy
- [x] Force ESC foundation
- [x] Bounded action audit log
- [x] V5 documentation

### V5.1 vision

- [ ] Vision provider integration
- [ ] Screenshot encoding for selected models
- [ ] Minecraft UI/state recognition
- [ ] Inventory recognition
- [ ] Cross-frame visual memory

### V5.2 actual Minecraft skills

- [ ] Camera/look control
- [ ] Walking and navigation
- [ ] Mining
- [ ] Item pickup
- [ ] Inventory management
- [ ] Crafting
- [ ] Food/health management
- [ ] Basic combat in controlled tests

### V5.3 learning

- [ ] Goal-conditioned memory retrieval
- [ ] Skill memory
- [ ] Reward/evaluation loop
- [ ] Failure recovery
- [ ] Replayable test scenarios

### V6

- [ ] Long-horizon Minecraft planning
- [ ] Better world-state tracking
- [ ] Multi-step skill execution
- [ ] Optional autonomous mode in a dedicated Minecraft test instance

## Development

The repository defaults to safe behavior. Real input is opt-in and should only be enabled deliberately after the Minecraft capture region and safety controls have been verified.

A roadmap checkbox means the feature exists in the repository, not that an AI model is magically good at Minecraft yet. We still have to teach the silicon creature where the crafting table is.

## License

Not specified yet.
