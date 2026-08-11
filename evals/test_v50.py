from minecraft.v50_agent_state import AgentState, AgentStateMachine
from minecraft.v50_event_bus import EventBus
from minecraft.v50_memory_store import MemoryStore
from minecraft.v50_mission_engine import Mission, MissionStatus
from minecraft.v50_safety_supervisor import SafetySupervisor
from minecraft.v50_observation_buffer import ObservationBuffer
from minecraft.v50_runtime import V50Runtime


def test_state_machine_rejects_invalid_transition():
    machine = AgentStateMachine()
    try:
        machine.transition(AgentState.ACT)
        assert False
    except ValueError:
        pass


def test_event_bus_dispatches():
    bus = EventBus()
    seen = []
    bus.subscribe("x", lambda event: seen.append(event.payload["v"]))
    bus.publish("x", {"v": 3})
    assert seen == [3]


def test_memory_is_bounded():
    memory = MemoryStore(max_items=2)
    memory.put("world", "a", "1", 1)
    memory.put("world", "b", "2", 1)
    memory.put("world", "c", "3", 1)
    assert len(memory.items) == 2


def test_mission_progress_and_completion():
    mission = Mission("m1", "collect", ["wood", "craft"])
    mission.start()
    mission.complete_subtask("wood")
    assert mission.progress == .5
    mission.complete_subtask("craft")
    assert mission.status == MissionStatus.COMPLETE


def test_safety_stops_after_failure_budget():
    safety = SafetySupervisor(max_failures=2)
    safety.record_result(False)
    safety.record_result(False)
    assert safety.emergency_stop


def test_observation_buffer_is_temporal_and_bounded():
    buffer = ObservationBuffer(max_frames=2)
    buffer.add({"x": 1}, .8)
    buffer.add({"x": 2}, .8)
    buffer.add({"x": 3}, .8)
    assert len(buffer.recent()) == 2
    assert buffer.latest().state["x"] == 3


def test_runtime_emergency_stop():
    runtime = V50Runtime()
    runtime.boot()
    runtime.emergency_stop()
    assert runtime.safety.emergency_stop
    assert runtime.states.state == AgentState.ABORTED
