# Qynl Agent

A personal AI agent inspired by modern computer-use assistants, built around the Qynl identity.

## Goals

- Natural-language task planning
- Tool calling and function execution
- File and project management
- Web/API integrations
- Coding assistance
- Safe approval gates for sensitive actions
- Extensible provider architecture

## Architecture

```text
User
  ↓
Qynl Agent Core
  ├── Planner / Reasoner
  ├── Tool Router
  ├── Memory
  ├── Approval Manager
  └── Provider Adapter
          ↓
       Tools / APIs
```

## Safety

The agent should request explicit approval before destructive actions, external side effects, credential changes, purchases, or publishing changes. Secrets must never be hard-coded or committed.

## Status

Early development.
