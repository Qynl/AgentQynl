import pytest
from minecraft.v31_action_schema import ActionKind, MinecraftAction
from minecraft.v31_state_estimator import StateEstimator
from minecraft.v31_action_validator import ActionValidator


def test_action_bounds():
    with pytest.raises(ValueError):
        MinecraftAction(ActionKind.MOVE, duration_ms=2001)


def test_stale_state_is_rejected():
    state = StateEstimator()
    result = ActionValidator().validate(MinecraftAction(ActionKind.MOVE), state=state)
    assert not result.allowed
    assert result.reason == "state is stale"


def test_low_confidence_is_rejected():
    state = StateEstimator()
    state.update(.2)
    result = ActionValidator().validate(MinecraftAction(ActionKind.MOVE), state=state)
    assert not result.allowed


def test_emergency_stop_wins():
    state = StateEstimator()
    state.update(1.0)
    result = ActionValidator().validate(MinecraftAction(ActionKind.MOVE), state=state, emergency_stop=True)
    assert not result.allowed
    assert result.reason == "emergency stop"


def test_valid_fresh_state_allows_action():
    state = StateEstimator()
    state.update(.9)
    result = ActionValidator().validate(MinecraftAction(ActionKind.MOVE, duration_ms=250), state=state)
    assert result.allowed
