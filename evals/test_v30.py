from minecraft.v30_contracts import CandidateAction, Observation
from minecraft.v30_decision_gate import DecisionGate
from minecraft.v30_health import HealthMonitor
from minecraft.v30_benchmark import Benchmark, BenchmarkCase


def obs(confidence=0.9):
    return Observation(1, 0.0, "overworld", confidence)


def test_low_confidence_stops_decision():
    decision = DecisionGate().choose(obs(.2), [CandidateAction("move", expected_progress=.8)])
    assert decision.action is None


def test_risky_action_is_rejected():
    decision = DecisionGate().choose(obs(), [CandidateAction("lava", risk=.9, expected_progress=.9)])
    assert decision.action is None


def test_bounded_utility_choice():
    decision = DecisionGate().choose(obs(), [
        CandidateAction("safe", risk=.1, expected_progress=.4),
        CandidateAction("better", risk=.2, expected_progress=.7),
    ])
    assert decision.action.name == "better"


def test_health_detects_stale_verification():
    monitor = HealthMonitor(max_verification_age_s=0)
    assert not monitor.snapshot(0).healthy


def test_benchmark_score():
    benchmark = Benchmark()
    cases = [BenchmarkCase("safe", obs(), (CandidateAction("move", expected_progress=.4),), "move")]
    results = benchmark.run(cases)
    assert benchmark.score(results) == 1.0
