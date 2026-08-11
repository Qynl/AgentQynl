from minecraft.v26_mission_control import Mission, MissionControl, MissionStatus
from minecraft.v26_mission_memory import MissionMemory, MissionResult
from minecraft.v26_recovery import RecoveryManager, RecoveryStep


def test_mission_lifecycle():
    mission = Mission("starter", "collect wood")
    control = MissionControl()
    control.load(mission)
    mission.start()
    assert control.tick() == MissionStatus.RUNNING
    mission.update(1.0)
    assert control.tick() == MissionStatus.COMPLETED


def test_unverified_mission_result_is_ignored():
    memory = MissionMemory()
    memory.record(MissionResult("x", "success", False, 1.0, "bad evidence"))
    assert memory.results == []


def test_recovery_escalates_and_eventually_aborts():
    recovery = RecoveryManager(max_attempts=2)
    assert recovery.next_step(stalled=True) == RecoveryStep.REPLAN
    assert recovery.next_step(stalled=True) == RecoveryStep.BACKTRACK
    assert recovery.next_step(stalled=True) == RecoveryStep.ABORT
