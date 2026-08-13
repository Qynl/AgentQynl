"""Safety and manual-takeover gate for the private training client."""
from enum import Enum

class ControlMode(Enum):
    MANUAL="manual"; TRAINING="training"; PAUSED="paused"; STOPPED="stopped"

class SafetyGate:
    def __init__(self): self.mode=ControlMode.MANUAL
    def start(self):
        if self.mode is not ControlMode.STOPPED: self.mode=ControlMode.TRAINING
    def pause(self): self.mode=ControlMode.PAUSED
    def resume(self):
        if self.mode is not ControlMode.STOPPED: self.mode=ControlMode.TRAINING
    def manual_takeover(self): self.mode=ControlMode.MANUAL
    def emergency_stop(self): self.mode=ControlMode.STOPPED
    def allows_actions(self): return self.mode is ControlMode.TRAINING
