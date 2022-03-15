from math import floor
from schedulerProcessStates import SchedulerProcessState


class SchedulerProcess:
    PID: str = ""
    priority: int = 0
    currentTimeSlice: int = 0
    numberOfTimeSlots: int = 0
    waitingTime: int = 0
    arrivalTime: int = 0

    def __init__(self, pid: str, arrivalTime: int, priority: int):
        self.PID = pid
        self.arrivalTime = arrivalTime
        self.priority = priority
        self.state: SchedulerProcessState = SchedulerProcessState.STARTED

    def getPID(self) -> str:
        return self.PID

    def getPriority(self) -> int:
        return self.priority

    def getTimeSlice(self) -> int:
        return self.currentTimeSlice

    def updateWaitingTime(self) -> None:
        pass

    def updatePriority(self, currentTime) -> None:
        if self.numberOfTimeSlots == 2:
            bonus: int = floor(10 * self.waitingTime / (currentTime - self.arrivalTime))
            self.priority = max(100, min(self.priority - bonus + 5, 139))
        else:
            return
