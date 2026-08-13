# Qynl Agent V3.5

Qynl is a **Minecraft-only autonomous AI agent** built around screen perception, semantic vision, temporal state, hierarchical planning, pathfinding, bounded actions, verification, recovery and explicit runtime safety.

## V3.5: Playable Closed-Loop Runtime

V3.5 is the big gameplay-runtime release. The previous releases established perception, pathfinding and the production adapter boundary. V3.5 connects those pieces into a tighter **observe → decide → safely act → observe → verify** loop and adds bounded Minecraft action primitives and goal tracking.

```text
Minecraft
   ↓
Screen Capture
   ↓
Hybrid Minecraft Vision
   ↓
Validated World State
   ↓
Short-Term Observation Memory
   ↓
Goal / Planner
   ↓
A* Pathfinding
   ↓
Safety Gate
   ↓
Bounded Action Controller
   ↓
Minecraft
   ↓
New Observation
   ↓
Action Verification
   ↓
Progress / Recovery
   ↺
```

## V3.5 additions

- closed-loop Minecraft runtime
- bounded movement action controller
- explicit allowlisted action vocabulary
- action duration limits
- post-action verification
- short-term observation memory
- monotonic goal progress tracking
- bounded goal attempts
- low-confidence action refusal
- safety-gate integration point
- regression tests for the new gameplay layer

## Bounded Minecraft actions

`minecraft/v35_action_controller.py`

The controller does **not** accept arbitrary keyboard strings from the AI. It exposes a small Minecraft-specific vocabulary:

```text
forward
back
left
right
jump
sprint
attack
use
hotbar_next
hotbar_prev
stop
```

Movement actions are deliberately short and capped by `max_duration_ms`.

This is important for a screen-driven agent. Instead of:

```text
"hold W for 20 seconds"
```

the runtime can do:

```text
observe
→ forward 80 ms
→ observe
→ verify
→ forward 80 ms
→ observe
```

The exact duration can be tuned by the planner, but the controller remains bounded.

## Closed-loop runtime

`minecraft/v35_runtime_loop.py`

The runtime implements:

```text
OBSERVE
   ↓
confidence check
   ↓
safety gate
   ↓
ONE SHORT ACTION
   ↓
OBSERVE AGAIN
   ↓
VERIFY
   ↓
CONTINUE / REPLAN / STOP
```

If perception confidence is too low, the runtime stops rather than blindly acting.

If the safety gate rejects an action, it is not executed.

The runtime never turns an AI proposal directly into unrestricted OS input.

## Action verification

`minecraft/v35_action_verifier.py`

After every bounded action, the new observation is compared with the previous state.

The verifier records whether:

- the player screen position changed
- the observed state changed
- the action has observable evidence of success

A movement command that produces no expected change can therefore feed the existing stuck/recovery logic instead of being silently counted as progress.

## Observation memory

`minecraft/v35_observation_memory.py`

A bounded deque stores recent observations.

This gives the planner temporal context without creating unbounded memory growth:

```text
frame t-3
frame t-2
frame t-1
frame t
```

Recent observations can be compared for state changes and progress.

## Goal management

`minecraft/v35_goal_manager.py`

Goals now have:

- name
- target data
- progress
- status
- attempt count

Progress is monotonic within a goal, so a noisy observation cannot accidentally turn `80%` progress into `20%`.

Example:

```text
Goal: collect oak logs

0.00 ────────┐
0.35         │
0.60         │
0.80         │
1.00 ────────┘ COMPLETE
```

The goal manager is deliberately generic. Minecraft-specific task decomposition can sit above it.

## V2.9 Vision → V3.5 Runtime

The previous vision stack now has a direct place in the runtime:

```text
MSS
 ↓
V2.9 Hybrid Vision
 ├─ OpenCV geometry
 ├─ HUD
 ├─ crosshair
 ├─ inventory evidence
 ├─ block candidates
 ├─ entity candidates
 └─ optional NIM VLM semantics
 ↓
Validated WorldState
 ↓
V3.5 Runtime
```

The runtime still follows the rule:

> **The model proposes. The runtime decides.**

## V2.6 Pathfinding → V3.5 Actions

Pathfinding does not directly press keys.

```text
A* path
   ↓
next node
   ↓
planner
   ↓
ActionCommand
   ↓
safety gate
   ↓
ActionController
   ↓
short input
   ↓
verification
```

This separation means pathfinding can be improved independently from OS input.

## Safety architecture

```text
                 AI / VLM
                    ↓
               candidate action
                    ↓
             typed ActionCommand
                    ↓
             confidence / freshness
                    ↓
                V30 Gate
                    ↓
               V31 Validator
                    ↓
              V50 Supervisor
                    ↓
               V22 Pacing
                    ↓
              Watchdog / ESC
                    ↓
            ActionController
                    ↓
                 Minecraft
```

V3.5 does **not** bypass the safety architecture.

The controller only accepts the allowlisted actions and clamps durations.

## Real Minecraft workflow

### 1. Install

```bash
git clone https://github.com/Qynl/AgentQynl.git
cd AgentQynl
python -m venv .venv
```

Windows:

```bash
.venv\\Scripts\\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install the required dependencies for the repository and vision layer.

### 2. Desktop app

```bash
cd apps/desktop
npm install
npm run dev
```

The desktop app is the intended place for runtime configuration, status, safety controls and diagnostics.

### 3. Start safely

Use a dedicated Minecraft test world first.

```text
DRY RUN
  ↓
Screen capture
  ↓
Vision
  ↓
World state
  ↓
Planning
  ↓
Action proposal
  ↓
NO INPUT
```

Then test bounded real input with Force ESC immediately available.

### 4. Increase autonomy

```text
one action
 ↓
verify
 ↓
short sequence
 ↓
verify
 ↓
short mission
 ↓
verify
 ↓
longer mission
```

Do not start by giving an untested agent unrestricted control of a real world/server.

## What V3.5 does NOT pretend

V3.5 is a major runtime step, but it does not magically solve every Minecraft task.

A screen-driven agent still has hard problems to solve:

- exact block identity under visual ambiguity
- hidden blocks behind the camera
- precise 3D coordinates from 2D images
- jumping/falling physics
- inventory manipulation
- crafting UI interaction
- combat timing
- resource gathering policies
- long-horizon planning
- server latency
- shaders/resource packs/UI scaling

When a fact cannot be established from the available observation, the correct behavior is to remain uncertain and observe again.

## Tests

`evals/test_v35.py` covers:

- monotonic goal progress
- action-duration clamping
- post-action state verification

The earlier V2.8/V2.9 vision and adapter test suites remain part of the regression surface.

## Version history

```text
V2.0 = V50 architecture baseline
V2.1 = observation + feedback reliability
V2.2 = debugability + progress measurement + pacing
V2.5 = gameplay reliability + recovery foundations
V2.6 = bounded A* pathfinding
V2.7 = runtime boundary
V2.8 = production screen/input/world-state adapters
V2.9 = hybrid Minecraft vision + NIM
V3.5 = closed-loop playable runtime
```

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
