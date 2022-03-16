from math import floor
from schedulerProcessStates import SchedulerProcessState

# the processes from the scheduler's POV
class SchedulerProcess:
    PID: str = ""
    priority: int = 0
    currentTimeSlice: int = 0
    numberOfTimeSlots: int = 0
    waitingTime: int = 0
    state: SchedulerProcessState = SchedulerProcessState.IDLE

    def __init__(self, pid: str, priority: int):
        self.PID = pid
        self.priority = priority
        self.state: SchedulerProcessState = SchedulerProcessState.IDLE

    def __lt__(self, other):
        return self.priority < other.priority

    def __cmp__(self, other):
        if self.priority < other.priority:
            return -1
        elif self.priority > other.priority:
            return 1
        else:
            return 0

    def getPID(self) -> str:
        return self.PID

    def getPriority(self) -> int:
        return self.priority

    def getTimeSlice(self) -> int:
        return self.currentTimeSlice

    def updateWaitingTime(self) -> None:
        # waiting time = current time - cpu burst time - arrival time
        pass

    def updatePriority(self, currentTime, arrivalTime: int) -> None:
        if self.numberOfTimeSlots == 2:
            bonus: int = floor(10 * self.waitingTime / (currentTime - arrivalTime))
            self.priority = max(100, min(self.priority - bonus + 5, 139))
        else:
            return
