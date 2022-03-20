from enum import Enum, unique


@unique
class SchedulerProcessState(Enum):
    ARRIVED = "Arrived"
    PAUSED = "Paused"
    RESUMED = "Resumed"  # can also be understood as running
    # all processes will be idled till they arrive
    IDLE = "Idle"
    TERMINATED = "Terminated"
