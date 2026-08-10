# Qynl Agent

Qynl is an experimental, safety-first AI agent focused on **computer-use and Minecraft gameplay**. V2 moves the project toward a modular desktop application that can observe Minecraft, reason about goals, perform tightly bounded inputs, remember experiences, and improve through structured feedback.

> **Status:** V2 architecture in development. Autonomous gameplay remains disabled until the perception, action, evaluation, and safety layers are implemented and tested.

## V2 highlights

- 🖥️ TSX-based desktop control surface
- 🧠 Modular agent/planner architecture
- 👁️ Screenshot-based Minecraft perception
- 🎮 Bounded Minecraft keyboard/mouse actions
- 🧩 NVIDIA NIM, Ollama and OpenAI-compatible provider adapters
- 🧠 Bounded episodic memory and learning feedback
- 🛡️ Strict action validation and approval gates
- 🚨 **Force ESC** operator emergency stop
- 🔒 No model-controlled arbitrary shell or application launching

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
                         │  Safety / Validator │◀──── Force ESC
                         └──────────┬──────────┘
                                    │
                             allowed input
                                    ▼
                         ┌─────────────────────┐
                         │ Minecraft Controls  │
                         └─────────────────────┘
```

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

The intended gameplay loop is:

```text
1. Capture Minecraft
2. Build a structured observation
3. Give the observation + goal to the model
4. Receive a proposed Minecraft action
5. Validate the action
6. Check Force ESC and safety limits
7. Execute only an allowed action
8. Capture the result
9. Evaluate the outcome
10. Store a bounded experience
11. Repeat
```

The model does **not** directly control the operating system. It proposes actions to a restricted Minecraft executor.

## Force ESC 🚨

**Force ESC is an operator-only hard stop.**

It is intentionally outside the model's tool registry, meaning the AI cannot call it, disable it, or override it through generated output.

When triggered:

1. New Minecraft actions are blocked.
2. The action loop hits a safety checkpoint and stops.
3. The desktop UI shows the emergency state.
4. The operator must explicitly clear the emergency state before control can resume.

The implementation lives in `safety/force_escape.py` and is designed as a thread-safe emergency latch.

Force ESC should be bound to a local keyboard shortcut handled by the desktop process. It should remain available even when the agent is confused, stuck, or producing bad actions.

## Safety model

Computer-use software deserves stronger boundaries than an ordinary chatbot. Qynl follows these principles:

- **Safe Mode enabled by default**
- Minecraft actions are explicitly allowlisted
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

## Project structure

```text
AgentQynl/
├── apps/
│   └── desktop/          # TSX desktop application
├── core/                 # Agent, planning and provider abstractions
├── minecraft/            # Capture, state and Minecraft controls
├── memory/               # Bounded episodic learning
├── safety/               # Action gates and Force ESC
├── evals/                # Evaluation scenarios and regression tests
└── docs/                 # Architecture and development notes
```

Keep these boundaries intact. Do not turn V2 back into one enormous script. The species has already invented enough files called `main_final_really_final.py`.

## Roadmap

### V2.0 Foundation

- [x] Provider abstraction
- [x] Safety gate foundation
- [x] Bounded episodic memory foundation
- [x] Desktop UI foundation
- [x] Force ESC emergency latch
- [x] V2 architecture documentation
- [ ] Automated tests and CI

### V2.1 Perception

- [ ] Screen-capture adapter
- [ ] Vision-model adapter
- [ ] Minecraft observation schema
- [ ] Inventory/state extraction
- [ ] Configurable observation frequency

### V2.2 Controlled gameplay

- [ ] Keyboard/mouse action adapter
- [ ] Strict Minecraft action allowlist
- [ ] Action preview/approval mode
- [ ] Force ESC desktop integration
- [ ] Basic navigation tasks
- [ ] Basic resource-gathering tasks

### V2.3 Learning

- [ ] Reward/feedback system
- [ ] Experience retrieval
- [ ] Skill/task memory
- [ ] Offline evaluation suite
- [ ] Regression tests for learned behaviors

### V2.4 Advanced agent

- [ ] Long-horizon planning
- [ ] Better world-state tracking
- [ ] Recovery from failed actions
- [ ] Optional autonomous mode inside an isolated Minecraft environment

## Development

This repository is experimental. A roadmap item is not automatically implemented merely because it is listed here. Autonomous computer control should only be enabled after its action and safety layers have been implemented and tested.

Never commit `.env`, API keys, access tokens, private screenshots, or personal data.

## License

Not specified yet.
