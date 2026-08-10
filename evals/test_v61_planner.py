from minecraft.planner import StructuredMinecraftPlanner


def test_invalid_provider_output_is_rejected():
    class Provider:
        def plan(self, context):
            return '{"type":"run_shell","command":"whoami"}'

    planner = StructuredMinecraftPlanner(Provider())
    assert planner.plan(None) is None


def test_valid_wait_is_parsed():
    class Provider:
        def plan(self, context):
            return '{"type":"wait","duration":0.25}'

    action = StructuredMinecraftPlanner(Provider()).plan(None)
    assert action is not None
    assert action.type == "wait"
    assert action.duration == 0.25
