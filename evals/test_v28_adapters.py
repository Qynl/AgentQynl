from minecraft.v28_production_adapter import ProductionAdapter, ScreenFrame, WorldState
from minecraft.v28_vision_schema import validate_vision_result
from minecraft.v28_world_state import WorldStateTracker

class Screen:
    def __init__(self): self.n = 0
    def capture(self):
        self.n += 1
        return ScreenFrame(object(), float(self.n), 1920, 1080)

class Input:
    def __init__(self): self.events = []
    def key_down(self, key): self.events.append(("down", key))
    def key_up(self, key): self.events.append(("up", key))
    def mouse_move(self, dx, dy): self.events.append(("move", dx, dy))
    def mouse_button(self, button, down): self.events.append(("mouse", button, down))
    def emergency_stop(self): self.events.append(("emergency",))

class Vision:
    def analyze(self, frame):
        return {"confidence": 0.8, "player": {"position": (0,0,0)}, "visible_blocks": [], "entities": [], "ui": {}}


def test_production_observation():
    adapter = ProductionAdapter(Screen(), Input(), Vision())
    state = adapter.observe()
    assert state.confidence == 0.8
    assert state.player["position"] == (0,0,0)


def test_emergency_stop_releases_keys():
    inp = Input()
    adapter = ProductionAdapter(Screen(), inp, Vision())
    adapter.emergency_stop()
    assert ("emergency",) in inp.events


def test_schema_rejects_invalid_confidence():
    bad = {"confidence": 2, "player": {}, "visible_blocks": [], "entities": [], "ui": {}}
    try:
        validate_vision_result(bad)
        assert False
    except ValueError:
        pass


def test_world_delta_tracks_position():
    tracker = WorldStateTracker()
    a = WorldState(1, {"position": (0,0,0)}, (), (), {}, 1)
    b = WorldState(2, {"position": (1,0,0)}, (), (), {}, 1)
    tracker.update(a)
    assert tracker.update(b).position_changed
