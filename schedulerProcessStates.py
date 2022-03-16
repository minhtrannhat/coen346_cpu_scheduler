from enum import Enum, unique, auto


@unique
class SchedulerProcessState(Enum):
    ARRIVED = "Arrived"
    PAUSED = "Paused"
    RESUMED = "Resumed"
    IDLE = "Idle"
