# Qynl Agent

Qynl is an experimental, safety-first AI agent focused on **computer-use and Minecraft gameplay**. The long-term goal is an agent that can see Minecraft through its screen, reason about what it sees, perform bounded keyboard/mouse actions, remember experiences, and improve through structured feedback.

> **Status:** Early development. The desktop UI and core safety architecture are being built before autonomous gameplay is enabled.

## What Qynl is becoming

```text
Minecraft
   │
   ▼
Screen Capture → Vision / Perception
                     │
                     ▼
              Qynl Agent Core
          ┌──────────┼──────────┐
          │          │          │
       Planner     Memory     Safety
          │          │          │
          └──────────┼──────────┘
                     ▼
              Action Executor
                     │
              Keyboard / Mouse
                     │
                     ▼
                 Minecraft
```

## Desktop app

Qynl is designed as a real desktop application rather than a single monolithic script.

The desktop interface is intended to expose the important controls clearly:

- **Dashboard**: agent status, current goal and recent activity
- **Minecraft**: capture and gameplay controls
- **Providers**: model provider, endpoint and model configuration
- **Memory**: inspect and manage learning episodes
- **Learning**: feedback, rewards and experience history
- **Safety**: permissions, approval requirements, rate limits and emergency stop
- **Settings**: general application and agent configuration

The UI uses TypeScript/TSX so the agent's state and controls can be understood without digging through the agent core.

## Model providers

Qynl is provider-agnostic. The architecture is intended to support:

- **NVIDIA NIM** for hosted inference
- **Ollama** for local models
- **OpenAI-compatible endpoints**
- Additional providers through adapters

Credentials belong in environment variables or a secure local configuration mechanism. They must never be committed to Git.

## Learning architecture

Qynl does not treat an LLM conversation as permanent learning. Gameplay experience is stored as bounded episodes:

```text
Goal
  ↓
Observation
  ↓
Action
  ↓
Outcome
  ↓
Reward / feedback
  ↓
Bounded memory
```

This makes experiments reproducible and gives the system useful context without allowing unbounded memory growth.

## Safety model

Safety is a core design requirement, especially because computer-use software can affect the host machine.

Qynl should follow these principles:

- **Safe Mode enabled by default**
- Minecraft actions are allowlisted
- Keyboard and mouse actions have bounded duration/rate
- Destructive or externally consequential actions require approval
- No arbitrary shell access from the gameplay agent
- No arbitrary application launching
- No unrestricted filesystem access
- Emergency stop must immediately halt agent actions
- Provider endpoints are explicitly configured rather than supplied by model output
- Secrets are never placed in prompts, source code, logs, or Git commits
- Screenshots should not be persisted unless explicitly enabled
- Learning memory is bounded and locally controllable

The Minecraft agent should receive only the permissions required to play Minecraft, not general control over the user's computer.

## Project structure

```text
AgentQynl/
├── apps/
│   └── desktop/          # TSX desktop interface
├── core/                 # Agent, planning and provider abstractions
├── minecraft/            # Minecraft capture, state and controls
├── memory/               # Bounded episodic learning
├── safety/               # Action permissions and safety gates
├── evals/                # Evaluation and test scenarios
└── docs/                 # Architecture and development notes
```

The exact implementation is evolving, so new modules should preserve this separation instead of turning the project back into one enormous script. Humanity has suffered enough from files named `final_final_v2.py`.

## Development roadmap

### Phase 1: Foundation

- [x] Provider abstraction
- [x] Safety gate foundation
- [x] Bounded episodic memory foundation
- [x] Desktop UI foundation
- [ ] Automated tests and CI

### Phase 2: Minecraft perception

- [ ] Screen-capture adapter
- [ ] Vision-model adapter
- [ ] Minecraft observation schema
- [ ] Inventory/state extraction
- [ ] Configurable observation frequency

### Phase 3: Controlled gameplay

- [ ] Keyboard/mouse action adapter
- [ ] Strict Minecraft action allowlist
- [ ] Action preview/approval mode
- [ ] Pause and emergency-stop integration
- [ ] Basic navigation tasks
- [ ] Basic resource-gathering tasks

### Phase 4: Learning

- [ ] Reward/feedback system
- [ ] Experience retrieval
- [ ] Skill/task memory
- [ ] Offline evaluation suite
- [ ] Regression tests for learned behaviors

### Phase 5: Advanced agent

- [ ] Long-horizon planning
- [ ] Better world-state tracking
- [ ] Recovery from failed actions
- [ ] Optional autonomous mode inside an isolated Minecraft environment

## Security notes

Do not run experimental computer-use features with unrestricted administrator privileges. Prefer a dedicated Minecraft instance, separate OS user, VM/container where practical, and explicit network/filesystem restrictions.

Never commit `.env`, API keys, access tokens, private screenshots, or personal data.

## Development

This repository is experimental. Features marked as planned are **not** automatically available just because they appear in the roadmap. Autonomous computer control should only be enabled after its action and safety layers have been implemented and tested.

## License

Not specified yet.
