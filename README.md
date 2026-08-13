# Qynl Agent V3.8

Qynl is a Minecraft-only autonomous **co-op AI companion**. The goal is not to take over the player's Minecraft window as a remote-control demo. Qynl is designed to exist alongside the player as an embodied teammate with its own goals, inventory, navigation, memory, chat and world interaction.

## V3.8: Co-op Companion + Local Vision

V3.8 adds the core pieces needed to move Qynl toward a real Minecraft teammate:

- local Ollama vision backend
- Llama 3.2 11B Vision default configuration
- structured JSON perception
- no direct model-to-input execution
- persistent companion memory
- natural-language task intake from Minecraft chat
- goal ownership and task timeout/replanning
- inventory interaction and evidence-based slot selection
- explicit hotbar `1`-`9` control
- bounded navigation and recovery
- observe → act → verify loops

The architecture is intentionally similar to the useful parts of modern AI companion mods: the AI decides what it wants to accomplish, while deterministic game systems handle movement, interaction and safety.

## The intended experience

You should be able to have an actual teammate in your world:

```text
YOU                         QYNL
 │                            │
 │  "get me some wood"       │
 ├───────────────────────────►│
 │                            │
 │                     understand request
 │                            │
 │                     find a tree
 │                            │
 │                     navigate there
 │                            │
 │                     collect wood
 │                            │
 │                     verify inventory
 │                            │
 │  "got 12 logs"            │
 ◄────────────────────────────┤
```

The important distinction is that Qynl is a **co-player**, not a chat box that only tells you how to perform the task.

## Local Ollama + Llama Vision

`minecraft/v38_ollama.py` provides a local HTTP client for Ollama's chat/vision endpoint.

Default configuration:

```text
Endpoint: http://127.0.0.1:11434/api/chat
Model:    llama3.2-vision:11b
```

The model receives a Minecraft frame plus compact structured state and returns JSON perception. The returned text is never passed directly to the keyboard/mouse controller.

### Why this architecture

```text
Minecraft frame
      ↓
Ollama / Llama Vision
      ↓
structured perception JSON
      ↓
validation
      ↓
world state
      ↓
planner
      ↓
structured Minecraft action
      ↓
safety controller
      ↓
Minecraft
      ↓
verification frame
```

This prevents a vision model from becoming an unrestricted input driver.

## Ollama setup

Install Ollama separately and make the configured vision model available locally. Then start the Ollama service on the default local endpoint.

Qynl expects a vision-capable model configured as:

```text
llama3.2-vision:11b
```

If the local Ollama installation uses a different model tag, change `OllamaConfig.model`.

The backend uses only Python's standard-library HTTP/JSON functionality, so it does not require an Ollama Python SDK.

## Companion memory

`minecraft/v38_companion.py` adds a small persistent runtime memory layer:

```text
recent chat
current goal
completed tasks
known facts
```

It gives the companion continuity between individual actions instead of resetting its intent after every screenshot.

## Chat commands as natural language

The companion accepts natural-language intent through its planner boundary. The user should not need to memorize an action vocabulary.

Examples:

```text
"follow me"
"stay here"
"get some wood"
"find food"
"mine stone"
"get iron"
"help me fight this mob"
"bring me what I need for a crafting table"
"come back"
"go to our base"
```

The planner converts intent into short, verifiable subgoals.

## Inventory

V3.8 supports evidence-based inventory reasoning and interaction.

A transfer requires:

- item identifier
- count
- slot index
- confidence
- screen coordinates when a click is required

The controller supports:

```text
select_hotbar(1..9)
click_slot(...)
quick_move_to_hotbar(...)
```

Hotbar selection uses the real number keys:

```text
1 2 3 4 5 6 7 8 9
```

There is no wheel-based hotbar action.

## Autonomous gameplay loop

Qynl is designed around short closed-loop actions:

```text
OBSERVE
  ↓
UNDERSTAND
  ↓
SELECT GOAL
  ↓
PLAN ONE SMALL STEP
  ↓
SAFETY CHECK
  ↓
ACT
  ↓
OBSERVE AGAIN
  ↓
VERIFY
  ↓
UPDATE MEMORY
  ↓
CONTINUE / RECOVER / REPLAN
```

This is deliberately different from giving the model a giant prompt such as `play Minecraft` and allowing it to spam inputs.

## Co-op behavior

The long-term target is for Qynl to behave like a useful additional player:

### Exploration

- follow the player
- stay at a location
- navigate to a known target
- recover from being stuck
- return to the player

### Resources

- identify visible resources
- gather requested resources
- use appropriate inventory items
- verify collected items

### Crafting

- determine missing resources
- collect prerequisites
- use inventory/crafting UI
- verify the resulting item

### Survival

- monitor health/food when visible
- react to nearby threats
- avoid blindly walking into obvious hazards
- retreat/recover when an action fails

### Communication

Qynl should report useful state rather than narrating every keystroke:

```text
"I'm low on food. I'm going to look for something nearby."
"I found iron, but I need a pickaxe first."
"I'm stuck in this cave. Replanning."
"I have enough wood. Coming back."
```

## Important implementation boundary

Qynl is not supposed to fake being a Minecraft player by merely moving the user's mouse and keyboard while pretending to be a separate teammate.

The intended final architecture is an **embodied companion connection**:

```text
Minecraft world
      │
      ├── companion entity/player presence
      ├── chat
      ├── inventory
      ├── world interaction
      └── game state
              │
              ▼
         Qynl Runtime
              │
       ┌──────┴──────┐
       ▼             ▼
   Ollama Vision   Planner
       │             │
       └──────┬──────┘
              ▼
        Skill / Task layer
              ▼
        Minecraft executor
```

The current V3.8 screen/input systems remain useful as a fallback and for testing perception, but the companion architecture is the direction for real co-op play.

## Existing gameplay systems

```text
V2.6  A* pathfinding
V2.8  production adapters
V2.9  hybrid Minecraft vision + optional NIM VLM
V3.5  closed-loop runtime
V3.6  structured Minecraft action language
V3.7  gameplay reliability + task decomposition
V3.8  inventory + explicit hotbar + Ollama/Llama vision + companion memory
```

## Safety

The model does not get unrestricted OS control. The intended chain is:

```text
AI / VLM
 ↓
structured intent
 ↓
planner
 ↓
validated Minecraft action
 ↓
safety supervisor
 ↓
bounded executor
 ↓
Minecraft
```

Emergency stop remains outside model control.

## Current limitations

V3.8 is the architecture for a serious co-op agent, not a guarantee that every Minecraft task already works autonomously.

The difficult remaining engineering areas are:

- embodied in-world companion connection
- robust Minecraft state extraction
- exact 3D navigation
- reliable crafting-grid interaction
- combat behavior
- long-horizon skill learning
- modded-item/recipe discovery
- persistent world memory
- recovery from unusual physics/network situations

The runtime should prefer observing again and replanning over inventing missing state.

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
