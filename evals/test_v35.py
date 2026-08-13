from minecraft.v35_goal_manager import GoalManager
from minecraft.v35_action_controller import ActionController, ActionCommand
from minecraft.v35_action_verifier import ActionVerifier

class Adapter:
    def __init__(self): self.events=[]
    def tap(self,k,d): self.events.append((k,d))
    def stop(self): self.events.append(("stop",))


def test_goal_progress_is_monotonic():
    g=GoalManager(); g.set_goal("wood", {"item":"oak_log"}); g.update(.8); g.update(.2)
    assert g.goals[0].progress == .8


def test_controller_limits_duration():
    a=Adapter(); ActionController(a, 100).execute(ActionCommand("forward", 9999))
    assert a.events[0][0] == "w" and a.events[0][1] == .1


def test_verifier_detects_state_change():
    before={"player":{"screen_position":[1,1]}}
    after={"player":{"screen_position":[2,1]}}
    assert ActionVerifier().verify(before,after,"forward")["verified"]
