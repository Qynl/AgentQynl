"""Small V4 safety regression suite using only the dry-run executor."""

import pytest

from minecraft.executor import DryRunExecutor
from safety.action_policy import MinecraftAction
from safety.force_escape import ForceEscape


def test_dry_run_never_sends_input() -> None:
    result = DryRunExecutor().execute(MinecraftAction(type="key", key="w", duration_ms=100))
    assert result.executed is True
    assert result.reason.startswith("dry-run")


def test_unknown_key_is_denied() -> None:
    result = DryRunExecutor().execute(MinecraftAction(type="key", key="F12", duration_ms=10))
    assert result.executed is False


def test_force_escape_blocks_dry_run() -> None:
    escape = ForceEscape()
    escape.trigger("test")
    result = DryRunExecutor(escape=escape).execute(MinecraftAction(type="key", key="w", duration_ms=10))
    assert result.executed is False
    assert "Force ESC" in result.reason


def test_force_escape_stops_real_executor_before_input() -> None:
    class FakeInput:
        def __init__(self) -> None:
            self.calls = 0

        def send(self, action: MinecraftAction) -> None:
            self.calls += 1

    from minecraft.executor import SafeMinecraftExecutor

    fake = FakeInput()
    escape = ForceEscape()
    escape.trigger("test")
    executor = SafeMinecraftExecutor(fake, escape=escape)
    with pytest.raises(RuntimeError):
        executor.execute(MinecraftAction(type="key", key="w", duration_ms=10))
    assert fake.calls == 0
