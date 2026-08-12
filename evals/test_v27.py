from minecraft.v26_pathfinding import Node
from minecraft.v27_runtime import MinecraftRuntime, RuntimeObservation

class FakeAdapter:
    def __init__(self): self.calls = []
    def move(self, dx, dy, dz): self.calls.append(("move", dx, dy, dz))
    def stop(self): self.calls.append(("stop",))
    def emergency_stop(self): self.calls.append(("esc",))

def test_low_confidence_never_executes_input():
    adapter = FakeAdapter(); runtime = MinecraftRuntime(adapter)
    decision = runtime.decide(RuntimeObservation(Node(0,0,0), Node(3,0,0), confidence=.2))
    assert decision.action == "reobserve"
    runtime.execute(decision, Node(0,0,0))
    assert adapter.calls == [("stop",)]

def test_runtime_produces_bounded_path_step():
    adapter = FakeAdapter(); runtime = MinecraftRuntime(adapter)
    decision = runtime.decide(RuntimeObservation(Node(0,0,0), Node(2,0,0), frozenset({Node(1,0,0)})))
    assert decision.action == "move_to"
    assert decision.target != Node(1,0,0)

def test_emergency_stop_pauses_runtime():
    adapter = FakeAdapter(); runtime = MinecraftRuntime(adapter)
    runtime.emergency_stop()
    decision = runtime.decide(RuntimeObservation(Node(0,0,0), Node(2,0,0)))
    assert decision.action == "stop"
    assert adapter.calls == [("esc",)]
