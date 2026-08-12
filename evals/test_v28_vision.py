from minecraft.v28_vision_schema import validate_vision_result
from minecraft.v28_vision_backends import JsonVisionBackend

VALID = {"confidence": .9, "player": {"position": None}, "visible_blocks": [], "entities": [], "ui": {}}

def test_json_backend_validates_output():
    backend = JsonVisionBackend(lambda image, prompt: VALID)
    assert backend.analyze(object())["confidence"] == .9

def test_json_backend_rejects_bad_model_output():
    backend = JsonVisionBackend(lambda image, prompt: {"confidence": 2})
    try:
        backend.analyze(object())
        assert False
    except (ValueError, TypeError, KeyError):
        pass

def test_schema_accepts_unknown_player_position():
    assert validate_vision_result(VALID)["player"]["position"] is None
