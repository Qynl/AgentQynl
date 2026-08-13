# Qynl BedWars Desktop Protocol

Private-training control protocol between the TSX desktop app and the 1.8.9 training client.

## Rules

- Bind to loopback only (`127.0.0.1`).
- Authenticate every session with a short-lived random token.
- Every request has a unique ID and timeout.
- `emergency_stop` and `manual_takeover` always override autonomous state.
- The desktop UI never sends raw Minecraft commands or arbitrary code.
- Telemetry is local and contains only training metrics.

## Messages

`hello`, `heartbeat`, `status`, `settings`, `goal`, `pause`, `resume`, `manual_takeover`, `emergency_stop`, `metrics`, `session_end`.

Goals are bounded to the private training planner and must be validated by the client before execution.

## Reconnect

The client sends a heartbeat periodically. Missing heartbeats put the agent into `PAUSED` rather than continuing autonomous behavior. A fresh authenticated session is required to resume.
