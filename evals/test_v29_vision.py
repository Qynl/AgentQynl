from minecraft.v29_temporal_vision import TemporalVisionTracker
from minecraft.v29_nim_vlm import NIMVisionBackend


def test_tracker_assigns_stable_ids():
    tracker = TemporalVisionTracker()
    a = tracker.update([{"kind":"entity","label":"cow","bbox":[10,10,30,30],"confidence":0.9}])
    b = tracker.update([{"kind":"entity","label":"cow","bbox":[12,11,30,30],"confidence":0.9}])
    assert a[0]["track_id"] == b[0]["track_id"]


def test_tracker_keeps_short_occlusion():
    tracker = TemporalVisionTracker(max_missed=2)
    tracker.update([{"kind":"entity","label":"pig","bbox":[10,10,30,30],"confidence":0.9}])
    result = tracker.update([])
    assert len(result) == 1
    assert result[0]["missed"] == 1


def test_nim_json_parser_handles_fenced_json():
    value = NIMVisionBackend._parse_json('```json\n{"confidence": 0.8}\n```')
    assert value["confidence"] == 0.8
