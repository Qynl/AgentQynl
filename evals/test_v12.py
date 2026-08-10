from minecraft.v12_state import GameState, StateTracker
from minecraft.v12_strategy import StrategyController


def test_transition_progress_detects_visual_change():
    tracker = StateTracker()
    before = GameState("tree", ("tree",), (), ())
    after = GameState("wood", (), (), ())
    transition = tracker.record_transition(before, after, "key")
    assert transition.changed
    assert transition.novelty > 0
    assert tracker.progress_score(transition) > 0


def test_strategy_varies_repeated_actions():
    strategy = StrategyController(repeat_limit=2)
    strategy.observe_action("key", True)
    strategy.observe_action("key", True)
    assert strategy.decide(0, 1.0).mode == "vary"


def test_low_confidence_is_cautious():
    strategy = StrategyController()
    assert strategy.decide(0, 0.2).mode == "cautious"
