# Qynl Agent V2.9

Qynl is a **Minecraft-only autonomous AI agent** with visual perception, temporal state, hierarchical planning, persistent world state, verified learning, mission-level autonomy, recovery, typed actions, deterministic evaluation and explicit runtime safety.

## V2.9: Full Hybrid Minecraft Vision

V2.9 turns the earlier vision boundary into a real hybrid perception stack:

```text
SCREENSHOT
   ↓
LOCAL CV ─────────────┐
   │                  │
   ├─ crosshair       │
   ├─ HUD geometry    │
   ├─ UI/inventory    │
   └─ block geometry  │
                      ↓
                FUSION / TRACKING
                      ↑
                OPTIONAL VLM
                      │
                 NIM / OTHER
                      │
               semantic labels
                      ↓
              VALIDATED WORLD STATE
```

### V2.9 additions

- hybrid deterministic-CV + semantic vision engine
- NVIDIA NIM VLM adapter
- base64 screenshot transport to OpenAI-compatible NIM `/v1/chat/completions`
- automatic NIM model discovery when no model is configured
- conservative JSON parsing
- temporal block/entity tracking with stable IDs
- short occlusion tolerance
- optional OCR for Minecraft tooltips/chat/item text
- rate-limited semantic inference so the VLM does not have to process every frame
- expanded regression tests

## Minecraft vision engine

`minecraft/v29_vision_engine.py`

The engine deliberately separates what can be established cheaply from pixels from what benefits from semantic AI.

### Local CV signals

- crosshair location/hint
- HUD geometry
- heart-like and food-like pixel regions
- hotbar region
- inventory grid evidence
- block-face geometry candidates
- player screen center

The local CV layer does **not** invent block names or world coordinates.

### Semantic VLM signals

The VLM can supply:

- visible block identities
- visible entity identities
- bounding boxes
- readable inventory contents
- selected item information
- HUD values when visually readable
- other screen-grounded Minecraft semantics

The prompt explicitly requires unknown values to remain `null` instead of hallucinating coordinates or state.

## NVIDIA NIM

`minecraft/v29_nim_vlm.py`

Qynl includes a standard-library HTTP adapter for NVIDIA NIM VLM. Current NIM VLM documentation exposes an OpenAI-compatible `/v1/chat/completions` endpoint and `/v1/models`; the adapter uses those endpoints and sends screenshots as JPEG data URLs.

Configure a local NIM endpoint such as:

```text
http://localhost:8000/v1
```

and optionally provide the served model name. If no model is supplied, Qynl queries `/v1/models` and uses the first available model.

The NIM adapter is intentionally provider-specific only at this boundary. The rest of Qynl uses the generic `SemanticBackend` interface.

## Hybrid runtime

`minecraft/v29_hybrid_backend.py`

Semantic inference is rate-limited:

```text
Frame 1 → local CV + VLM
Frame 2 → local CV
Frame 3 → local CV
Frame 4 → local CV + VLM
...
```

This keeps the fast perception path responsive while allowing richer semantic refreshes.

Every block/entity detection passes through temporal tracking.

## Temporal tracking

`minecraft/v29_temporal_vision.py`

Detections receive stable `track_id` values when consecutive bounding boxes overlap sufficiently.

A short disappearance is treated as an occlusion rather than immediately creating a new object:

```text
cow #4
  ↓
visible
  ↓
not visible for 1 frame
  ↓
still track #4
  ↓
visible again
  ↓
track #4
```

This prevents the planner from interpreting normal frame-to-frame flicker as dozens of new entities.

## OCR

`minecraft/v29_ocr.py`

Optional Tesseract OCR can read screen text such as:

- item tooltips
- readable inventory names
- chat text

OCR is supplemental. It is never treated as authoritative merely because text was detected.

## World-state pipeline

```text
Minecraft
   ↓
MSS / ScreenCapture
   ↓
Frame timestamp
   ↓
Local CV
   ↓
Optional NIM VLM
   ↓
Fusion
   ↓
Schema validation
   ↓
Temporal tracking
   ↓
WorldState
   ↓
Mission / Planner
   ↓
V2.6 A* Pathfinding
   ↓
V2.7 Runtime
   ↓
V30 / V31 / V50 Safety
   ↓
Input Adapter
   ↓
Minecraft
```

## What the screenshot can and cannot tell us

A screenshot can provide visual evidence, but it is not a direct game-state API.

Therefore Qynl follows these rules:

- no invented world XYZ
- no invented yaw/pitch
- no invented inventory contents
- no invented entity identity
- unknown values remain unknown
- every semantic result carries confidence
- stale observations are not silently treated as current

If authoritative coordinates are eventually needed, the correct architecture is to add a **separate game-state source** rather than hallucinating them from pixels.

## Safety boundary

```text
AI / memory / learning
        ↓
candidate decision
        ↓
typed Minecraft action
        ↓
confidence + freshness
        ↓
V30 decision gate
        ↓
V31 validator
        ↓
V50 safety supervisor
        ↓
V22 pacing guard
        ↓
watchdog / Force ESC
        ↓
Production Input Adapter
        ↓
Minecraft
```

Vision, VLM output, tracking and pathfinding cannot bypass execution safety.

## Installation

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

Install vision dependencies:

```bash
pip install -r requirements-vision.txt
```

The NIM adapter itself uses Python's standard library for HTTP. A compatible NIM VLM must be running separately.

For the TSX desktop app:

```bash
cd apps/desktop
npm install
npm run dev
```

## Safe real-Minecraft workflow

```text
1. Dedicated test world
2. Dry-run
3. Verify screen capture
4. Verify local CV
5. Verify VLM JSON + schema
6. Verify temporal tracking
7. Test Force ESC
8. Run short bounded sessions
9. Inspect traces and verification
10. Increase autonomy gradually
```

Do not run an untested adapter unattended.

## Tests

- `evals/test_v28_adapters.py`
- `evals/test_v28_vision.py`
- `evals/test_v29_vision.py`

V2.9 tests include stable tracking IDs, short occlusion handling and NIM JSON parsing.

## Versioning

```text
V2.0 = V50 architecture baseline
V2.1 = observation + feedback reliability
V2.2 = debugability + progress measurement + pacing
V2.5 = gameplay reliability + navigation/recovery foundations
V2.6 = pathfinding + navigation feedback
V2.7 = usable runtime boundary
V2.8 = production screen/input/world-state adapters
V2.9 = full hybrid Minecraft vision
V3.0 = only for a genuinely major architectural change
```

## Limitations

V2.9 is a serious screen-perception stack, but no screenshot-only system can guarantee perfect game-state reconstruction. Visual occlusion, resource packs, shaders, UI scaling, camera effects, low resolution and model errors can reduce accuracy.

For maximum reliability, visual perception should eventually be combined with a Minecraft-side telemetry/state source where appropriate. The screen/VLM path remains the human-visible perception channel.

## License

See [`LICENSE`](LICENSE). The project uses the **Qynl Agent Proprietary License** unless a specific file states otherwise.
