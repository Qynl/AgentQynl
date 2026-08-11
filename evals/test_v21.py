from minecraft.v21_spatial_memory import SpatialMemory
from minecraft.v21_exploration import ExplorationManager
from minecraft.v21_predictor import TransitionPredictor
from minecraft.v21_controller import V21Controller
from minecraft.v20_planner import CandidateScore


def test_spatial_memory_detects_revisit():
    m = SpatialMemory()
    m.observe("village", "ahead", .9, 1)
    m.observe("village", "left", .8, 8)
    assert m.revisited("village")


def test_exploration_prefers_reobserve_when_uncertain():
    d = ExplorationManager().choose(confidence=.2, repeated_state=False, unknown_area=False, danger=False)
    assert d.action == "reobserve"


def test_predictor_accounts_for_risk():
    candidates = [CandidateScore("a", .9, ""), CandidateScore("b", .5, "")]
    result = TransitionPredictor().predict(candidates, failure_rate=.2)
    assert result
    assert result[0].expected_progress >= result[-1].expected_progress


def test_controller_stops_for_danger():
    d = V21Controller().choose([], confidence=1, repeated_state=False, unknown_area=False, danger=True)
    assert d.mode == "safe_stop"
    assert d.action is None
