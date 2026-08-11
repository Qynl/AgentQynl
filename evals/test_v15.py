from minecraft.v15_blackboard import Blackboard
from minecraft.v15_watchdog import RuntimeWatchdog
from minecraft.v15_action_verifier import ActionVerifier
from minecraft.v13_state import TemporalState


def state(summary, landmarks=(), hazards=(), ui=()):
    return TemporalState(summary, (), landmarks, hazards, ui, 1.0, 0)


def test_blackboard_is_bounded():
    board = Blackboard(goal="get wood")
    for i in range(100):
        board.fail(str(i))
        board.event(str(i))
    assert len(board.failures) == 12
    assert len(board.events) == 40


def test_watchdog_rejects_long_action():
    watchdog = RuntimeWatchdog(max_action_ms=500)
    assert not watchdog.check_action(501).allowed


def test_action_verifier_detects_change():
    before = state("tree", ("tree",))
    after = state("wood", ("wood",))
    result = ActionVerifier().verify(before, after, "key")
    assert result.executed
    assert result.observable_change
    assert result.score > 0
