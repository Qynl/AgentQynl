from minecraft.v25_navigation import Navigator, Waypoint
from minecraft.v25_recovery import RecoveryPolicy


def test_navigation_arrival():
    decision = Navigator().choose((0, 64, 0), Waypoint(1, 64, 0, "spawn"))
    assert decision.action == "arrived"


def test_navigation_far_target():
    decision = Navigator().choose((0, 64, 0), Waypoint(20, 64, 0, "village"))
    assert decision.action == "move_to_waypoint"
    assert decision.distance > 1.5


def test_recovery_reobserves_on_low_confidence():
    assert RecoveryPolicy().choose(0, 0, .2).mode == "reobserve"


def test_recovery_replans_after_regression():
    assert RecoveryPolicy().choose(1, -.2, .8).mode == "replan"


def test_recovery_has_retry_budget():
    assert RecoveryPolicy(max_retries=2).choose(2, 0, .9).mode == "reobserve"
