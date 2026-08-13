# Qynl BedWars Training Bot

A separate 1.8.9-oriented combat/training agent sharing Qynl's local Ollama reasoning stack.

## Scope

This module is intended for **private worlds, LAN test servers, bot arenas, and training environments**. It is not designed to automate competitive public-server matches or evade anti-cheat systems.

## Architecture

```text
Minecraft 1.8.9 / test arena
        |
        +-- game state / screenshots
        |
        v
   BedWars Perception
        |
        v
   Combat State Machine
        |
   +----+-----+----------------+
   |          |                |
 Target     Movement        Objective
   |          |                |
   +----------+----------------+
              |
              v
      Ollama / local model
              |
              v
       bounded decision
              |
              v
       Action Executor
              |
              v
          Minecraft
```

The fast combat loop is deterministic. The LLM is used for higher-level decisions, not per-frame mouse jitter.

## Combat goals

- target selection
- distance/angle control
- strafing
- sprint reset timing
- hit confirmation
- combo training
- disengage when outnumbered
- void/death risk awareness
- bed/objective awareness
- recovery after missed actions

## Ollama

Default endpoint:

`http://127.0.0.1:11434`

The model can be configured without changing the combat engine. Keep inference off the 1.8.9 render/input tick.

## Safety

Do not use this module to automate public competitive matches or bypass server anti-cheat. Use it for local testing and training.
