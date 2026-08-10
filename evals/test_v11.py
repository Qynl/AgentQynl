from minecraft.v11_model import parse_minecraft_action
from minecraft.v11_agent import StuckDetector, ObservationSignature


def test_parser_rejects_non_minecraft_payload():
    assert parse_minecraft_action('{"type":"shell","command":"echo bad"}') is None


def test_parser_accepts_canonical_key_action():
    action = parse_minecraft_action('{"type":"key","key":"w","duration_ms":120}')
    assert action is not None
    assert action.type == "key"
    assert action.key == "w"


def test_stuck_detector_requires_repeated_state():
    detector = StuckDetector(window=4)
    sig = ObservationSignature("same", (), ())
    for _ in range(3):
        detector.push(sig)
        assert detector.stuck() is False
    detector.push(sig)
    assert detector.stuck() is True
