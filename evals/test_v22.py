from minecraft.v22_goal_monitor import GoalMonitor, GoalStatus
from minecraft.v22_action_sequence import ActionSequencer
from minecraft.v22_subtasks import Subtask, SubtaskGraph
from minecraft.v22_replan import ReplanPolicy
from minecraft.v20_planner import CandidateScore


def test_goal_monitor_completion_requires_evidence_and_confidence():
    signal = GoalMonitor().evaluate(progress_delta=.1, completion_evidence=.95, failure_count=0, confidence=.8)
    assert signal.status == GoalStatus.COMPLETE


def test_goal_monitor_stalls_after_failures():
    signal = GoalMonitor().evaluate(progress_delta=0, completion_evidence=0, failure_count=2, confidence=.7)
    assert signal.status == GoalStatus.STALLED


def test_action_sequence_is_bounded():
    candidates = [CandidateScore(str(i), .9, "") for i in range(10)]
    assert len(ActionSequencer().build(candidates, 3).steps) == 3


def test_subtask_graph_returns_pending_node():
    graph = SubtaskGraph()
    graph.add(Subtask("root", "get resources"))
    graph.add(Subtask("wood", "get wood", "root"))
    assert graph.next_pending().id == "root"


def test_replan_after_repeated_state():
    decision = ReplanPolicy().should_replan(goal_status="active", repeated_state=True, high_uncertainty=False, action_rejected=False, recovery_exhausted=False)
    assert decision.required
