# Qynl Agent

Qynl is a **Minecraft-only AI agent**. The project is designed around one job: let an AI observe a Minecraft game, reason about Minecraft goals, perform tightly bounded Minecraft inputs, remember useful experiences, and improve through evaluation.

It is **not** a general computer-use assistant. The model should not receive arbitrary desktop, shell, process, or filesystem control.

> **Status:** V4 foundation in development. The real screen-capture and input adapters remain opt-in and are not enabled by the repository's safe defaults.

## V4 highlights

- 🖥️ TSX desktop control surface
- 🎮 Minecraft-only agent scope
- 👁️ Minecraft observation/capture boundary
- 🧠 Provider abstraction for NVIDIA NIM, Ollama and OpenAI-compatible endpoints
- 🎯 Structured Minecraft action policy
- 🛡️ Deny-by-default safety validation
- 🚨 Operator-only Force ESC hard stop
- 🧪 Dry-run Minecraft executor for safe testing
- 📝 Bounded Minecraft action audit log
- ⚙️ Typed Minecraft agent settings
- 🧠 Bounded episodic learning foundation
- 🔒 No model-controlled shell, process launching or unrestricted filesystem access

## V4 architecture

```text
                         ┌──────────────────────┐
                         │      Minecraft       │
                         └──────────┬───────────┘
                                    │
                           Minecraft Capture
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Observation       │
                         │ frame + game state   │
                         └──────────┬───────────┘
                                    │
                                    ▼
┌─────────────────┐       ┌──────────────────────┐       ┌─────────────────┐
│ NVIDIA NIM      │──────▶│     Qynl Brain       │◀─────▶│ Memory /        │
│ Ollama          │       │ observe → plan → act │       │ Learning        │
│ Compatible API  │       └──────────┬───────────┘       └─────────────────┘
└─────────────────┘                  │
                              MinecraftAction
                                     │
                                     ▼
                           ┌──────────────────────┐
                           │     ActionPolicy     │
                           │     DENY BY DEFAULT  │
                           └──────────┬───────────┘
                                      │
                              Force ESC checkpoint
                                      │
                              approval / rate limit
                                      │
                                      ▼
                           ┌──────────────────────┐
                           │ Minecraft Executor   │
                           └──────────┬───────────┘
                                      │
                                      ▼
                                  Minecraft
```

Every model-proposed action goes through the safety boundary before it can reach an input adapter.

## Minecraft-only scope

Qynl is intentionally restricted to Minecraft context.

The model may eventually receive:

- Minecraft screenshots
- Minecraft-focused structured state
- inventory information
- health/food information
- the current Minecraft goal
- bounded action history
- bounded learning experiences

The model should **not** receive or control:

- arbitrary desktop windows
- arbitrary applications
- shell commands
- process creation
- unrestricted filesystem operations
- arbitrary mouse/keyboard APIs
- credentials or secrets

The distinction matters. A Minecraft agent should play Minecraft, not accidentally become a general-purpose remote-control daemon because someone forgot to put a permission check in a Friday-night commit.

## V4 Minecraft observation layer

`minecraft/observation.py` defines the model-facing observation contract.

`minecraft/capture.py` defines the capture boundary. The default `DisabledCapture` produces no screenshot and does not inspect the desktop.

A real capture adapter should be responsible for selecting **only the configured Minecraft surface** and returning an opaque screenshot reference. It should not expose arbitrary desktop content to the agent.

## V4 executor

`minecraft/executor.py` contains two deliberately separate paths:

### DryRunExecutor

The default testing boundary. It validates actions but never sends OS input.

Use this for:

- UI development
- policy testing
- agent evaluation
- debugging model outputs

### SafeMinecraftExecutor

The real-input boundary. It requires an explicitly supplied Minecraft input adapter and performs:

```text
ActionPolicy validation
        ↓
Force ESC checkpoint
        ↓
Minecraft input adapter
```

The model never calls the input adapter directly.

## Action safety

V3's deny-by-default `ActionPolicy` remains the core safety boundary.

Current supported action categories are deliberately small:

- allowlisted Minecraft keys
- bounded key holds
- bounded mouse movement
- left/right mouse buttons
- bounded waits

Unknown actions are rejected.

The policy does not expose arbitrary key codes, shell commands, process launching, or filesystem operations.

## Force ESC 🚨

Force ESC is an **operator-only emergency stop** and is intentionally outside the model tool system.

The model cannot:

- trigger Force ESC
- disable Force ESC
- clear Force ESC
- override Force ESC

The real executor checks the emergency latch immediately before sending input. If it is engaged, no Minecraft input is sent.

The desktop application should bind Force ESC to a local operator shortcut and keep it available even when the agent is busy or unresponsive.

## Audit log

`core/audit.py` provides a bounded in-memory audit log for Minecraft actions.

Records contain only:

- timestamp
- pipeline stage
- Minecraft action type
- allow/deny result
- validation reason

The audit layer does not store screenshots, API keys, arbitrary desktop data, or model secrets.

## Settings

`core/settings.py` provides typed configuration for the Minecraft agent:

- provider
- model
- endpoint
- safe mode
- approval requirement
- capture rate
- action rate limit
- screenshot persistence preference

Safe defaults are intentionally conservative.

## Providers

Qynl is provider-agnostic at the agent layer.

Supported/planned providers:

- **NVIDIA NIM**
- **Ollama** for local models
- **OpenAI-compatible APIs**

Provider output must be converted into the structured Minecraft action interface before it can reach the safety layer.

Credentials must stay outside Git. Never commit `.env` files, API keys, access tokens, or private data.

## Minecraft loop

```text
Capture Minecraft
      ↓
Create observation
      ↓
Vision / reasoning model
      ↓
Propose MinecraftAction
      ↓
ActionPolicy
      ↓
Force ESC checkpoint
      ↓
Approval / rate limits
      ↓
Minecraft Executor
      ↓
Observe result
      ↓
Evaluate
      ↓
Bounded memory
      ↓
Next step
```

The system is designed so that a model failure produces a rejected/failed Minecraft action rather than unrestricted computer control.

## Learning

Qynl uses bounded episodic memory rather than silently modifying model weights during gameplay.

An experience can contain:

```text
Goal
Observation
Proposed action
Validated action
Outcome
Reward / feedback
```

This makes learning experiments inspectable and testable. Later versions can add skill retrieval, reward models, offline training or fine-tuning without weakening the action boundary.

## Desktop application

The desktop UI is built around TSX and is intended to expose the Minecraft agent clearly:

- **Dashboard**: current goal, status and activity
- **Minecraft**: capture preview and connection state
- **Actions**: proposed/approved/rejected Minecraft actions
- **Memory**: bounded experiences
- **Learning**: feedback and evaluations
- **Providers**: NIM/Ollama/compatible configuration
- **Safety**: Safe Mode, approvals, limits and Force ESC
- **Settings**: Minecraft agent configuration

The UI is not itself an authority. The Python safety/core layers remain responsible for validating actions.

## Project structure

```text
AgentQynl/
├── apps/
│   └── desktop/          # TSX desktop UI
├── core/                 # Agent settings, audit and core abstractions
├── minecraft/            # Minecraft-only capture, observation and execution
├── memory/               # Bounded episodic learning
├── safety/               # ActionPolicy + Force ESC
├── evals/                # Safety and agent evaluation
└── docs/                 # Versioned architecture notes
```

## V4 roadmap

### V4.0 foundation

- [x] Minecraft-only scope
- [x] Structured observation contract
- [x] Capture boundary with safe disabled default
- [x] Dry-run executor
- [x] Safe real-input executor boundary
- [x] Deny-by-default ActionPolicy
- [x] Force ESC foundation
- [x] Bounded action audit log
- [x] Typed agent settings
- [x] V4 safety regression tests

### V4.1 perception

- [ ] Real Minecraft window/surface capture adapter
- [ ] Vision provider adapter
- [ ] Minecraft-focused visual observation schema
- [ ] Inventory/state extraction
- [ ] Frame-rate controls

### V4.2 gameplay

- [ ] Minecraft-only keyboard adapter
- [ ] Minecraft-only mouse adapter
- [ ] Desktop Force ESC shortcut
- [ ] Action queue and approval UI
- [ ] Action replay/evaluation tools
- [ ] Basic movement/navigation tasks

### V4.3 learning

- [ ] Experience retrieval
- [ ] Goal-conditioned memory
- [ ] Reward/feedback UI
- [ ] Offline evaluation scenarios
- [ ] Skill/task abstraction

### V4.4 autonomous Minecraft

- [ ] Long-horizon Minecraft planning
- [ ] World-state tracking
- [ ] Recovery from failed actions
- [ ] Optional autonomous mode in a dedicated Minecraft test instance

## Safety and testing

Do not test real computer-control adapters on a machine containing sensitive applications or data. Prefer a dedicated Minecraft instance, separate OS account, VM or other isolated environment where practical.

The V4 repository defaults to dry-run behavior. A roadmap checkbox does not mean a feature is already implemented.

## License

Not specified yet.
