"""V50 top-level runtime wiring state, safety, missions and observations."""
from __future__ import annotations
from .v50_agent_state import AgentState, AgentStateMachine
from .v50_event_bus import EventBus
from .v50_observation_buffer import ObservationBuffer
from .v50_safety_supervisor import SafetySupervisor

class V50Runtime:
    def __init__(self) -> None:
        self.states = AgentStateMachine()
        self.events = EventBus()
        self.observations = ObservationBuffer()
        self.safety = SafetySupervisor()

    def boot(self) -> None:
        self.states.transition(AgentState.OBSERVE)
        self.events.publish("runtime.started")

    def emergency_stop(self) -> None:
        self.safety.stop()
        if self.states.state not in {AgentState.COMPLETE, AgentState.ABORTED}:
            self.states.transition(AgentState.ABORTED)
        self.events.publish("runtime.emergency_stop")
