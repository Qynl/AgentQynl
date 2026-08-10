# Qynl Agent

Qynl is a personal, tool-using AI agent inspired by modern computer-use assistants.

## Current features

- OpenAI Responses API agent loop
- Tool calling
- File reading and directory inspection
- File writing with explicit approval
- Shell command execution with explicit approval
- Configurable model and step limit
- Environment-based secrets, never committed
- Extensible Python tool registry

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put your API key in `.env`, then run:

```bash
python qynl_agent.py
```

## Architecture

```text
User
  ↓
Qynl Agent Core
  ├── Reasoning / planning
  ├── Tool router
  ├── File tools
  ├── Shell tool + approval gate
  ├── Memory (next)
  └── Web / computer tools (next)
          ↓
       External systems
```

## Safety

Qynl does not hard-code credentials. Filesystem writes and shell commands require interactive approval. Add new tools behind the same approval model when they can cause external side effects.

## Roadmap

1. Persistent conversation/memory
2. Web search and browser automation adapters
3. Computer-use adapter
4. Better sandboxing and permission scopes
5. Streaming UI
6. Local-model/provider adapters

## License

Not specified yet.
