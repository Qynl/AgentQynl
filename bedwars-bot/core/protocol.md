# Qynl BedWars Desktop Protocol

The desktop app and the private 1.8.9 training client communicate over a loopback-only authenticated channel.

## Principles

- Bind to `127.0.0.1` only.
- Generate a random session token at startup.
- Never accept commands without the current token.
- Keep `STOP` and manual takeover highest priority.
- The client must remain usable if the desktop app or Ollama disappears.
- Ollama is strategic only; latency-sensitive combat remains local.

## Message envelope

```json
{"v":1,"type":"status","requestId":"...","token":"...","payload":{}}
```

Supported types:

- `hello`
- `status`
- `state`
- `metrics`
- `settings`
- `goal`
- `pause`
- `resume`
- `stop`
- `manual_takeover`

## Safety

`stop` and `manual_takeover` are idempotent and must be processed before any queued action. The client rejects malformed JSON, unknown message types, oversized payloads and invalid numeric values.
