from minecraft.v26_mission_control import Mission, MissionControl, MissionStatus
from minecraft.v26_mission_memory import MissionMemory, MissionResult
from minecraft.v26_recovery import RecoveryManager, RecoveryStep
from minecraft.v26_pathfinding import AStarPathfinder, Node
from minecraft.v26_navigation import PathNavigator
from minecraft.v26_stuck_detector import StuckDetector
from minecraft.v26_path_cost import score_path


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


def test_astar_routes_around_block():
    start, goal = Node(0,0,0), Node(2,0,0)
    result = AStarPathfinder().find(start, goal, {Node(1,0,0)})
    assert result.complete
    assert result.path[0] == start
    assert result.path[-1] == goal
    assert Node(1,0,0) not in result.path


def test_astar_respects_expansion_bound():
    result = AStarPathfinder(max_expansions=1).find(Node(0,0,0), Node(20,0,0))
    assert not result.complete
    assert result.expanded <= 1


def test_navigator_returns_next_path_node():
    path = (Node(0,0,0), Node(1,0,0), Node(2,0,0))
    assert PathNavigator().next_step(path).target == Node(1,0,0)


def test_stuck_detector_triggers_after_limit():
    detector = StuckDetector(3)
    assert not detector.update(False)
    assert not detector.update(False)
    assert detector.update(False)


def test_path_score_bounds_risk():
    score = score_path(10, 2)
    assert score.risk == 1.0
    assert score.score >= score.length
