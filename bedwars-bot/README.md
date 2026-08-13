# Qynl BedWars 1.8.9 Training Agent

A dedicated **private-server training agent** for Minecraft 1.8.9. It shares Qynl's local Ollama reasoning layer, but keeps high-frequency movement/combat decisions in a fast local controller.

> **Scope:** private worlds, LAN test servers, bot arenas and training environments. Do not use this project to automate competitive public-server matches or bypass anti-cheat systems.

## Design

```text
Minecraft 1.8.9
      │
      ├── Perception ───────────────┐
      │   target / health / blocks  │
      │   bed / void / inventory    │
      │                             ▼
      │                     Combat State
      │                             │
      │             ┌───────────────┼──────────────┐
      │             ▼               ▼              ▼
      │          Target          Movement       Objective
      │             │               │              │
      │             └───────────────┼──────────────┘
      │                             ▼
      │                    Fast Action Controller
      │                             │
      │                    verify → recover
      │                             │
      ▼                             ▼
  Minecraft ◄────────────────── Action Executor

                         ▲
                         │
                  Strategy / Planning
                         │
                    Ollama (local)
```

The local controller runs the time-sensitive loop. Ollama is deliberately **not** called for every click or frame. This keeps the agent responsive and makes temporary model latency recoverable.

## Core systems

### Combat

- target selection with confidence
- distance and angle state
- strafing state machine
- sprint-state management
- attack timing
- hit confirmation
- combo tracking
- knockback/recovery state
- disengage logic
- void and fall-risk checks
- configurable reaction/decision rates

### BedWars awareness

- bed/objective state
- resource awareness
- upgrade/shop planning hooks
- teammate/opponent awareness
- defend / attack / retreat strategy states
- death/reset recovery

### Training telemetry

Record local, non-sensitive metrics such as:

- hits and misses
- damage dealt/received
- longest combo
- fight duration
- deaths
- disengages
- objective results
- movement/reaction statistics

Use these for replay review and local training evaluation rather than for bypassing server protections.

## Ollama

Default local endpoint:

`http://127.0.0.1:11434`

Recommended architecture:

```text
Ollama → strategic goal
           ↓
Fast local controller → movement/combat
           ↓
Minecraft state → verification
           ↓
Recovery / next goal
```

Inference must remain off the latency-sensitive 1.8.9 render/input loop. If Ollama is unavailable, the controller should continue in a safe fallback state or pause, never block the client thread.

## Emergency controls

The training client should provide an immediate manual takeover and emergency stop. A human-controlled state always has priority over the agent.

## Development priorities

1. deterministic local game-state adapter
2. target/movement controller
3. combat state machine
4. objective planner
5. Ollama strategy adapter
6. telemetry/replay
7. private-server training scenarios
8. regression tests for movement/combat state transitions

## Important

This project is intentionally scoped to controlled training environments. It does not contain anti-cheat bypasses, stealth behavior, or public-server automation features.
