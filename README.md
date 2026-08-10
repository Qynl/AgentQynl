# Qynl Agent

Qynl is an experimental, safety-first AI agent focused on **computer-use and Minecraft gameplay**. V3 adds a deny-by-default action boundary so the model can propose Minecraft actions without receiving direct operating-system control.

> **Status:** V3 architecture in development. Autonomous gameplay remains disabled until perception, execution, evaluation, and safety layers are implemented and tested.

## V3 highlights

- 🖥️ TSX desktop control surface
- 🧠 Modular agent/planner architecture
- 👁️ Screenshot-based Minecraft perception architecture
- 🎮 Structured, bounded Minecraft actions
- 🧩 NVIDIA NIM, Ollama and OpenAI-compatible provider adapters
- 🧠 Bounded episodic memory and learning feedback
- 🛡️ **Deny-by-default ActionPolicy**
- 🚨 **Force ESC** operator-only emergency stop
- 🔒 No model-controlled shell, process launching, or unrestricted filesystem access

## Architecture

```text
                         ┌─────────────────────┐
                         │     Minecraft       │
                         └──────────┬──────────┘
                                    │
                              screenshots
                                    ▼
                         ┌─────────────────────┐
                         │ Vision / Perception │
                         └──────────┬──────────┘
                                    ▼
┌──────────────┐        ┌─────────────────────┐        ┌──────────────┐
│ NIM / Ollama │───────▶│    Qynl Agent Core  │◀──────▶│   Memory     │
│ / compatible │        │ Plan → Decide → Eval│        │   / Learning │
└──────────────┘        └──────────┬──────────┘        └──────────────┘
                                    │
                              proposed action
                                    ▼
                         ┌─────────────────────┐
                         │  ActionPolicy       │
                         │  deny by default    │◀──── Force ESC
                         └──────────┬──────────┘
                                    │
                               approved action
                                    ▼
                         ┌─────────────────────┐
                         │ Minecraft Executor  │
                         └─────────────────────┘
```

## V3 ActionPolicy

The model produces a structured `MinecraftAction`. It never gets direct access to keyboard APIs, mouse APIs, the shell, or arbitrary OS controls.

`Safety/ActionPolicy` validates every proposed action before execution:

- allowlisted Minecraft-oriented keys only
- bounded key-hold duration
- bounded mouse movement
- left/right mouse buttons only
- bounded waits
- unknown action types are rejected
- invalid values are rejected

Anything not explicitly allowed is denied.

The policy is only the validation layer. The real executor must still check **Force ESC immediately before sending input** and apply any operator approval requirements.

## Desktop app

The desktop app is intended to make the agent understandable and controllable without digging through source code.

Planned/active panels:

- **Dashboard**: agent status, goal, current step and activity
- **Minecraft**: capture state and gameplay controls
- **Providers**: provider, endpoint, model and connection settings
- **Memory**: inspect and clear learning episodes
- **Learning**: rewards, feedback and evaluation results
- **Safety**: permissions, limits, approvals and Force ESC
- **Settings**: general application configuration

The UI uses TypeScript/TSX and is deliberately separated from the agent core.

## Model providers

Qynl uses a provider abstraction so the gameplay system is not tied to one AI vendor.

Supported/planned adapters include:

- **NVIDIA NIM**
- **Ollama** for local inference
- **OpenAI-compatible APIs**
- Additional providers through isolated adapters

API keys and tokens must be stored outside source control. Provider configuration must never be accepted directly from model output.

## Minecraft computer-use loop

```text
1. Capture Minecraft
2. Build a structured observation
3. Give observation + goal to the model
4. Receive a proposed MinecraftAction
5. Validate through ActionPolicy
6. Check Force ESC
7. Check approval/rate limits
8. Execute only the allowed action
9. Capture the result
10. Evaluate the outcome
11. Store a bounded experience
12. Repeat
```

The model does **not** directly control the operating system. It proposes actions to a restricted Minecraft executor.

## Force ESC 🚨

**Force ESC is an operator-only hard stop.**

It is intentionally outside the model's tool registry, meaning the AI cannot call it, disable it, or override it through generated output.

When triggered:

1. New Minecraft actions are blocked.
2. Action loops stop at their safety checkpoint.
3. The desktop UI enters an emergency state.
4. The operator must explicitly clear the emergency state before control can resume.

The implementation lives in `safety/force_escape.py` as a thread-safe emergency latch. It should be bound to a local keyboard shortcut handled by the desktop process, not by the model.

## Learning architecture

Qynl does not treat every model response as permanent learning. Experiences are stored as bounded episodes:

```text
Goal
  ↓
Observation
  ↓
Proposed Action
  ↓
Validated Action
  ↓
Outcome
  ↓
Reward / Feedback
  ↓
Bounded Memory
```

This allows experiments to be evaluated and retrieved without uncontrolled memory growth.

## Safety model

Computer-use software deserves stronger boundaries than an ordinary chatbot. Qynl follows these principles:

- **Safe Mode enabled by default**
- Deny-by-default Minecraft action policy
- Keyboard/mouse durations and rates are bounded
- Every action is validated before execution
- High-impact actions can require operator approval
- **Force ESC cannot be invoked or disabled by the model**
- No arbitrary shell access from the Minecraft agent
- No arbitrary application launching
- No unrestricted filesystem access
- Provider endpoints are configured by the operator
- Secrets are never placed in prompts, source code, logs, or Git commits
- Screenshots are not persisted unless explicitly enabled
- Learning memory is bounded and locally controllable

For testing, use a dedicated Minecraft instance or an isolated environment rather than a computer containing sensitive applications or data.

## Project structure

```text
AgentQynl/
├── apps/
│   └── desktop/          # TSX desktop application
├── core/                 # Agent, planning and provider abstractions
├── minecraft/            # Capture, state and Minecraft controls
├── memory/               # Bounded episodic learning
├── safety/               # ActionPolicy and Force ESC
├── evals/                # Evaluation scenarios and regression tests
└── docs/                 # Architecture and development notes
```

Keep these boundaries intact. Do not turn V3 back into one enormous script. The species has already invented enough files called `main_final_really_final.py`.

## Roadmap

### V3.0 Safety + action foundation

- [x] Provider abstraction
- [x] Safety gate foundation
- [x] Bounded episodic memory foundation
- [x] Desktop UI foundation
- [x] Force ESC emergency latch
- [x] Deny-by-default ActionPolicy
- [x] Structured Minecraft action schema
- [x] V3 architecture documentation
- [ ] Automated policy tests and CI

### V3.1 Perception

- [ ] Screen-capture adapter
- [ ] Vision-model adapter
- [ ] Minecraft observation schema
- [ ] Inventory/state extraction
- [ ] Configurable observation frequency

### V3.2 Controlled gameplay

- [ ] Keyboard/mouse action executor
- [ ] Desktop Force ESC global shortcut
- [ ] Action preview/approval mode
- [ ] Action audit log
- [ ] Basic navigation tasks
- [ ] Basic resource-gathering tasks

### V3.3 Learning

- [ ] Reward/feedback system
- [ ] Experience retrieval
- [ ] Skill/task memory
- [ ] Offline evaluation suite
- [ ] Regression tests for learned behaviors

### V3.4 Advanced agent

- [ ] Long-horizon planning
- [ ] Better world-state tracking
- [ ] Recovery from failed actions
- [ ] Optional autonomous mode inside an isolated Minecraft environment

## Development

This repository is experimental. A roadmap item is not automatically implemented merely because it is listed here. Autonomous computer control should only be enabled after its action and safety layers have been implemented and tested.

Never commit `.env`, API keys, access tokens, private screenshots, or personal data.

## License

Not specified yet.
