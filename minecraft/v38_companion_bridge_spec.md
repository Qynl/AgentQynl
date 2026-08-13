# Qynl V3.8 Companion Bridge

The companion bridge is the missing embodiment layer for Qynl.

## Goal

Qynl should appear in the player's Minecraft world as a separate companion/player entity, rather than taking over the user's keyboard.

The Minecraft-side bridge/mod is responsible for:

- spawning/connecting the Qynl companion
- receiving structured commands
- executing Minecraft-native actions
- reading safe game state
- sending chat messages
- sending inventory/entity/player state
- reporting command results
- reconnecting after temporary disconnects

The desktop Qynl runtime is responsible for:

- Ollama/VLM inference
- memory
- planning
- task decomposition
- navigation decisions
- action selection
- safety policy

## Transport

Use a local WebSocket or localhost HTTP/WebSocket bridge for single-player/LAN development. The bridge must authenticate the local session with a random session token.

Never expose the control endpoint publicly by default.

## Message contract

Every message has:

```json
{
  "v": "1.0",
  "type": "...",
  "request_id": "...",
  "payload": {}
}
```

### Client → bridge

`hello`

`command`

`chat`

### Bridge → client

`state`

`chat`

`result`

`error`

`event`

## Command examples

```json
{
  "v":"1.0",
  "type":"command",
  "request_id":"abc123",
  "payload":{
    "action":"follow",
    "args":{}
  }
}
```

```json
{
  "v":"1.0",
  "type":"command",
  "request_id":"abc124",
  "payload":{
    "action":"gather",
    "args":{"item":"oak_log","count":8}
  }
}
```

The bridge must validate actions against an allowlist and reject malformed or unsafe requests.

## State

The bridge should periodically send:

- companion UUID/entity ID
- player position/rotation
- nearby entities
- nearby blocks when available
- health/food
- inventory and hotbar
- selected slot
- current dimension
- current game mode
- current screen/UI state
- nearby player position
- current action status

Avoid sending unnecessary sensitive/local machine data.

## Chat

Minecraft chat is a first-class interface:

```text
User → Minecraft chat → bridge → Qynl
Qynl → bridge → Minecraft chat
```

Natural-language messages are converted into goals by Qynl. The bridge must never execute arbitrary natural-language text directly.

## Companion behavior

Core high-level commands:

- follow
- stay
- come_here
- gather
- mine
- explore
- find
- craft
- build
- guard
- attack_target
- eat
- return_to_base
- stop

Each high-level command becomes a task in Qynl's planner and produces progress/result events.

## Co-op design

The companion should behave like a second player:

```text
You                    Qynl
 │                       │
 ├── chat instruction ──►│
 │                       ├── plan
 │                       ├── navigate
 │                       ├── interact
 │                       ├── verify
 │                       │
 │◄──── progress/chat ───┤
 │                       │
 └──── next instruction ─►
```

Qynl should not take control of the user's own player. The bridge controls only the companion entity.

## Reconnection

If the bridge disconnects:

1. stop issuing commands
2. mark companion offline
3. preserve the current goal
4. reconnect with a new handshake
5. request fresh state
6. revalidate the goal
7. resume only after state synchronization

Never resume from stale coordinates or stale inventory.
