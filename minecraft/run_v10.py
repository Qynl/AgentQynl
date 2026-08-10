"""One-command V10 Minecraft agent runner.

Environment:
  QYNL_PROVIDER=ollama|nim
  QYNL_MODEL=vision-capable-model
  QYNL_BASE_URL=provider-base-url
  QYNL_API_KEY=... (or NVIDIA_API_KEY for NIM)
  QYNL_GOAL=collect wood
  QYNL_CAPTURE_DIR=./runtime/capture
  QYNL_CAPTURE_LEFT/TOP/WIDTH/HEIGHT
  QYNL_DRY_RUN=1 by default; set 0 only for real input.
"""
from __future__ import annotations
import os, time
from pathlib import Path
from .real_capture import MssMinecraftCapture, CaptureRegion
from .observation import MinecraftObservation
from .v10_provider import OpenAICompatibleMinecraftModel, config_from_env
from .vision import VisualAnalysis
from .goals import GoalManager, MinecraftGoal, PlanningContext
from .planner import StructuredMinecraftPlanner
from .executor import DryRunExecutor, SafeMinecraftExecutor, ExecutionResult
from .input_adapter import PyAutoGuiMinecraftInput
from safety.action_policy import ActionPolicy
from safety.force_escape import ForceEscape

class V10Agent:
    def __init__(self) -> None:
        out = Path(os.getenv("QYNL_CAPTURE_DIR", "runtime/capture")); out.mkdir(parents=True, exist_ok=True)
        region = CaptureRegion(int(os.getenv("QYNL_CAPTURE_LEFT","0")), int(os.getenv("QYNL_CAPTURE_TOP","0")), int(os.getenv("QYNL_CAPTURE_WIDTH","1280")), int(os.getenv("QYNL_CAPTURE_HEIGHT","720")))
        self.capture = MssMinecraftCapture(region, str(out))
        self.model = OpenAICompatibleMinecraftModel(config_from_env())
        self.escape = ForceEscape()
        self.policy = ActionPolicy()
        self.goals = GoalManager(); self.goals.set_goal(MinecraftGoal(os.getenv("QYNL_GOAL","survive and collect wood"), ("goal progress is visible",), int(os.getenv("QYNL_MAX_STEPS","10000"))))
        self.executor = DryRunExecutor(self.policy, self.escape) if os.getenv("QYNL_DRY_RUN","1") != "0" else SafeMinecraftExecutor(PyAutoGuiMinecraftInput(self.escape), self.policy, self.escape)
        self.step_id = 0

    def step(self) -> ExecutionResult:
        self.escape.checkpoint()
        frame = self.capture.capture()
        obs = MinecraftObservation.create(self.step_id, frame.width, frame.height, screenshot_ref=frame.screenshot_ref, game_focused=frame.game_focused)
        if not obs.screenshot_ref: return ExecutionResult(False, "capture did not produce an image")
        visual = self.model.vision(obs.screenshot_ref, "Return JSON with summary, visible_ui, landmarks, hazards, confidence. Identify only visible Minecraft facts; do not guess.")
        context = self.goals.context(visual, ())
        if context is None: return ExecutionResult(False, "no goal configured")
        raw = self.model.plan_text(context)
        action = StructuredMinecraftPlanner(type("Provider", (), {"plan": lambda _self, _ctx: raw})()).plan(context)
        if action is None: return ExecutionResult(False, "model produced no valid Minecraft action")
        result = self.executor.execute(action)
        self.goals.advance(); self.step_id += 1
        return result

def main() -> None:
    agent = V10Agent()
    interval = max(0.15, float(os.getenv("QYNL_LOOP_INTERVAL","0.4")))
    while True:
        result = agent.step()
        print(f"[V10] executed={result.executed} reason={result.reason}", flush=True)
        if os.getenv("QYNL_ONCE","0") == "1": break
        time.sleep(interval)

if __name__ == "__main__": main()
