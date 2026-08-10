# Qynl Agent V10

Qynl is a **Minecraft-only AI agent that can actually close the loop**: capture Minecraft, send the game image to a vision-capable model, choose one bounded Minecraft action, validate it, execute it, and observe Minecraft again.

V10 is deliberately not a general computer-use agent. The model receives Minecraft context and can only produce the canonical Minecraft action schema.

## V10: the full loop

```text
Minecraft
   ↓
MSS capture
   ↓
MinecraftObservation
   ↓
Vision-capable model
   ↓
VisualAnalysis
   ↓
Goal + context
   ↓
Planner
   ↓
Strict MinecraftAction JSON
   ↓
ActionPolicy
   ↓
Force ESC
   ↓
PyAutoGUI Minecraft adapter
   ↓
Minecraft
   ↓
new screenshot
```

This is the important change from the earlier versions: the model transport, image input, structured planning, policy and real executor are wired together in `minecraft/run_v10.py`.

## What V10 actually does

- 📸 Captures a configured Minecraft region with MSS
- 👁️ Sends the frame to a multimodal vision model
- 🧠 Gives the model the active Minecraft goal and current visual analysis
- 🎯 Requests exactly one next Minecraft action
- 📋 Parses the result into the repository's canonical `MinecraftAction`
- 🛡️ Validates it with deny-by-default `ActionPolicy`
- 🚨 Checks independent Force ESC immediately before input
- 🎮 Sends the action through the restricted Minecraft PyAutoGUI adapter
- 🔄 Captures the next frame and repeats
- 🧪 Defaults to dry-run so the complete perception/planning path can be tested without input

## Supported provider architecture

V10 uses an OpenAI-compatible multimodal HTTP transport, so the same agent can connect to:

- **NVIDIA NIM**
- **Ollama** with a vision-capable model
- other OpenAI-compatible multimodal endpoints

No provider receives shell access, arbitrary desktop tools, or unrestricted keyboard/mouse APIs.

## Quick start

Install the Python dependencies from `requirements.txt`, configure the model and capture region, then run the agent in dry-run mode first:

```text
QYNL_PROVIDER=ollama
QYNL_BASE_URL=http://127.0.0.1:11434/v1
QYNL_MODEL=<your-vision-model>
QYNL_CAPTURE_LEFT=0
QYNL_CAPTURE_TOP=0
QYNL_CAPTURE_WIDTH=1280
QYNL_CAPTURE_HEIGHT=720
QYNL_DRY_RUN=1
QYNL_ONCE=1
python -m minecraft.run_v10
```

For NIM:

```text
QYNL_PROVIDER=nim
NVIDIA_API_KEY=<your-key>
QYNL_BASE_URL=<your-NIM-compatible-base-url>
QYNL_MODEL=<your-vision-capable-model>
```

The NIM URL/model are configurable because deployments and available models can change. Do not put keys into Git.

## Real Minecraft input

After verifying the capture and model output in dry-run mode, real input can be enabled:

```text
QYNL_DRY_RUN=0
python -m minecraft.run_v10
```

Use a dedicated Minecraft test world/account. Human beings have spent decades learning that testing autonomous software on the important thing first is a bad idea.

## Canonical action schema

The model may return only one action per cycle:

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

The parser rejects unknown action types and malformed fields. The policy then independently checks allowlisted keys, mouse bounds and duration limits.

## Why V10 should work substantially better

The old architecture stopped at interfaces. V10 actually connects the important components.

### Closed-loop perception

The model sees a new Minecraft frame after each action cycle. It does not blindly execute a long script based on an old screenshot.

### One-action planning

The model chooses one bounded action, then gets another observation. This is much more robust for Minecraft because movement, camera orientation, collisions, block breaking, menus and mobs change the state constantly.

### Real multimodal input

The vision provider receives the actual captured Minecraft image, not a placeholder screenshot reference or a text-only description.

### Canonical action contract

Vision/planning output is converted into the same `MinecraftAction` object understood by the policy and executor. The previous V6/V7 schema mismatch is removed.

### Safety remains outside the model

The model can request an action. It cannot authorize itself to execute it.

## Minecraft-only boundary

The model is allowed to reason about:

- Minecraft screenshots
- Minecraft visual observations
- Minecraft goals
- Minecraft inventory/state when available
- bounded Minecraft action history

It is not given:

- arbitrary desktop screenshots
- shell execution
- process creation
- filesystem commands
- credentials/secrets
- unrestricted keyboard APIs
- unrestricted mouse APIs
- arbitrary application control

## Force ESC 🚨

Force ESC is independent of the model.

The model cannot trigger, disable, clear or override it. The executor checks it immediately before real input.

If it is engaged, real input remains blocked until the operator explicitly resets it.

## Project structure

```text
AgentQynl/
├── apps/desktop/           # TSX desktop UI
├── core/                   # settings, audit, provider abstractions
├── minecraft/
│   ├── capture.py          # capture contract
│   ├── real_capture.py     # MSS Minecraft-region capture
│   ├── observation.py      # model-facing observation
│   ├── vision.py           # vision contract
│   ├── providers.py        # provider-neutral adapters
│   ├── v10_provider.py     # real multimodal HTTP provider
│   ├── planner.py          # strict action parser
│   ├── goals.py            # goal/context management
│   ├── state.py            # rolling state
│   ├── skills.py           # Minecraft micro-skills
│   ├── executor.py         # dry-run/real executors
│   ├── input_adapter.py    # restricted PyAutoGUI adapter
│   └── run_v10.py          # complete runnable V10 loop
├── memory/
├── safety/
│   └── action_policy.py    # canonical action schema + policy
├── evals/
└── docs/
    └── V10.md
```

## Safety defaults

V10 starts with:

```text
QYNL_DRY_RUN=1
```

So you can verify the complete model/capture/planning pipeline without letting the agent control Minecraft.

The safety chain is:

```text
Untrusted model output
        ↓
Strict JSON parser
        ↓
MinecraftAction
        ↓
Deny-by-default ActionPolicy
        ↓
Bounded action
        ↓
Force ESC
        ↓
Minecraft executor
```

## Learning and competence

V10 provides the real interaction loop needed for later skill learning, but it does not pretend that a generic vision model is automatically a Minecraft expert.

For good gameplay, the model still needs strong visual reasoning and useful task context. The important difference is that **the actual runtime path now exists**. There is no longer a missing "next version" whose job is mysteriously to connect the AI to Minecraft.

Useful skill benchmarks include:

- camera/look control
- movement
- wood gathering
- crafting
- food gathering
- navigation
- mining
- inventory management
- recovery from being stuck
- controlled combat
- long-horizon survival

## Documentation

See `docs/V10.md` for provider configuration, capture setup, action format and safe real-input testing.

## License

Not specified yet.
