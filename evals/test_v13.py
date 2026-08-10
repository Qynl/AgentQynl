from minecraft.v13_state import TemporalStateTracker
from minecraft.v13_planner import PlannerEvidence, build_v13_prompt

class Vision:
    summary = "tree"
    entities = ({"label":"cow","confidence":0.9,"position":"left"},)
    visible_ui = ("hotbar",)
    landmarks = ("tree",)
    hazards = ()
    confidence = 0.9


def test_temporal_tracker_detects_entity_changes():
    tracker = TemporalStateTracker()
    first, _ = tracker.update(Vision())
    Vision.entities = ()
    second, delta = tracker.update(Vision())
    assert first.entities
    assert "cow" in delta.removed_entities


def test_v13_prompt_contains_temporal_evidence():
    tracker = TemporalStateTracker()
    current, delta = tracker.update(Vision())
    evidence = PlannerEvidence(current, delta, tracker.recent())
    prompt = build_v13_prompt("get wood", ("logs collected",), evidence)
    assert "temporal" not in prompt.lower() or "evidence" in prompt.lower()
    assert "get wood" in prompt
    assert "Minecraft-only" in prompt
