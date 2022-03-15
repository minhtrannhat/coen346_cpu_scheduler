from enum import Enum, unique, auto


@unique
class SchedulerProcessState(Enum):
    STARTED = auto()
    PAUSED = auto()
    RESUMED = auto()
