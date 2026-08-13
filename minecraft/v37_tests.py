from minecraft.v37_gameplay import Target, TargetSelector, RecoveryPlanner
from minecraft.v37_tasks import decompose_goal
from minecraft.v37_inventory import has_item

class S:
    confidence=.9; timestamp=10
    visible_blocks=({"name":"oak_log","distance":4},)
    entities=()
    ui={"inventory":{"slots":[{"item":"oak_log","count":3,"confidence":.9}]}}

def test_target_selector():
    assert TargetSelector().nearest(S(), Target("block","oak_log"))["distance"] == 4

def test_inventory_requires_evidence():
    assert has_item(S(),"oak_log",2)

def test_goal_decomposition():
    assert len(decompose_goal("crafting_table")) >= 3

def test_recovery_is_bounded():
    assert RecoveryPlanner().next(999) == "reobserve"
