from minecraft.v16_recovery import RecoveryManager
from minecraft.v16_memory import AdaptiveMemory
from minecraft.v16_rate_limiter import ActionRateLimiter


def test_recovery_prioritizes_low_confidence():
    d = RecoveryManager().diagnose(repeated_state=True, repeated_action=True, low_confidence=True, recent_failures=0)
    assert d.mode == "reobserve"


def test_recovery_aborts_after_budget():
    d = RecoveryManager(max_attempts=2).diagnose(repeated_state=False, repeated_action=False, low_confidence=False, recent_failures=2)
    assert d.mode == "abort"


def test_memory_keeps_negative_lessons():
    m = AdaptiveMemory()
    m.add("find village", "plains", "do not keep walking in the same direction", -1)
    hits = m.retrieve("find village", "plains")
    assert hits and hits[0].reward < 0


def test_rate_limiter_blocks_immediate_repeat():
    limiter = ActionRateLimiter(1000)
    assert limiter.allow()
    assert not limiter.allow()
