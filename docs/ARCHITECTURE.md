# Qynl Agent architecture

## Provider layer

Qynl is provider-agnostic. The first-class targets are NVIDIA NIM, Ollama/local models, and OpenAI-compatible endpoints. API credentials are supplied through the runtime environment or OS credential storage, never committed.

## Perception

The desktop client captures only the selected Minecraft window when possible. Frames are resized before inference and are not persisted by default.

## Action boundary

The model never receives a raw shell, PowerShell, filesystem, registry, browser, or arbitrary process tool. It can emit only a small Minecraft action schema. Every action passes the safety gate before execution.

## Learning

Qynl stores bounded episodic records: goal, compact observation summary, action, outcome and reward. It does not silently upload recordings or screenshots. Learning data is local by default and can be cleared from the UI.

## Safe defaults

- Safe mode ON
- Kill switch always available
- Selected-window capture only
- No arbitrary command execution
- Keyboard actions are allowlisted
- Mouse actions are gated
- Action durations are bounded
- Provider endpoints are validated
- Credentials are never written to source files
