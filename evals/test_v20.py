from minecraft.v20_world_model import WorldModel
from minecraft.v13_state import TemporalState, EntityObservation
from minecraft.v20_planner import CandidateScore


def test_world_model_persists_objects():
    model = WorldModel()
    state = TemporalState("forest", (EntityObservation("cow", .9, "left"),), ("tree",), (), ("hotbar",), .9, 0)
    model.update(state)
    context = model.context()
    assert context["objects"][0]["label"] == "cow"
    assert "tree" in context["landmarks"]


def test_candidate_scores_sort_descending():
    values = sorted([CandidateScore("a", .2, ""), CandidateScore("b", .9, "")], key=lambda x: x.utility, reverse=True)
    assert values[0].action == "b"
