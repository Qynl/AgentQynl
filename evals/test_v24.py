from minecraft.v24_realtime_runtime import RealtimeRuntime, RuntimeConfig
from minecraft.v24_task_executor import GuardedTaskExecutor
from minecraft.v24_session import SessionTelemetry


def test_runtime_stops_after_failure_budget():
    runtime = RealtimeRuntime(RuntimeConfig(max_consecutive_failures=2))
    runtime.start()
    runtime.record_result(False)
    assert runtime.can_continue()
    runtime.record_result(False)
    assert not runtime.can_continue()


def test_dry_run_never_executes():
    result = GuardedTaskExecutor(dry_run=True).execute("move", permitted=True)
    assert not result.executed
    assert result.reason == "dry run"


def test_emergency_stop_wins():
    result = GuardedTaskExecutor(dry_run=False).execute("move", permitted=True, emergency_stop=True)
    assert not result.executed


def test_telemetry_is_bounded_and_verification_scoped():
    telemetry = SessionTelemetry(max_events=2)
    telemetry.record("a", verified=True, reward=1)
    telemetry.record("b", verified=False, reward=1)
    telemetry.record("c", verified=True, reward=.5)
    assert telemetry.stats()["events"] == 2
    assert telemetry.stats()["verified_reward"] == .5
