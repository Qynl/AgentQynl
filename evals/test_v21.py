from minecraft.v21_spatial_memory import SpatialMemory
from minecraft.v21_exploration import ExplorationManager
from minecraft.v21_predictor import TransitionPredictor
from minecraft.v21_controller import V21Controller
from minecraft.v20_planner import CandidateScore
from minecraft.v21_observation_smoother import ObservationSmoother
from minecraft.v21_action_feedback import ActionFeedback, ActionOutcome


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


def test_observation_smoothing_bounds_confidence():
    smoother = ObservationSmoother(window=3)
    result = smoother.add({"health": 20}, 2.0)
    assert result.confidence == 1.0
    assert result.samples == 1


def test_observation_window_is_bounded():
    smoother = ObservationSmoother(window=2)
    smoother.add({"x": 1}, .5)
    smoother.add({"x": 2}, .5)
    result = smoother.add({"x": 3}, 1.0)
    assert result.samples == 2
    assert result.state["x"] == 3


def test_feedback_progress_bounds():
    try:
        ActionFeedback(ActionOutcome.SUCCESS, 1.1)
        assert False
    except ValueError:
        pass


def test_unknown_feedback_is_not_verified():
    assert not ActionFeedback(ActionOutcome.UNKNOWN, 0).verified
    assert ActionFeedback(ActionOutcome.SUCCESS, .2).verified
