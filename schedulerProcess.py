from math import floor

# the processes from the scheduler's POV
class SchedulerProcess:
    PID: str = ""
    priority: int = 0
    currentTimeSlice: int = 0
    waitingTime: int = 0

    def __init__(self, pid: str, priority: int):
        self.PID = pid
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __cmp__(self, other):
        if self.priority < other.priority:
            return -1
        elif self.priority > other.priority:
            return 1
        else:
            return 0

    def updateWaitingTime(self, currentTime, timeSpentInCPU, arrivalTime) -> None:
        self.waitingTime = currentTime - timeSpentInCPU - arrivalTime

    def updatePriority(self, currentTime, arrivalTime: int) -> None:
        bonus: int = floor(10 * self.waitingTime / (currentTime - arrivalTime))
        self.priority = max(100, min(self.priority - bonus + 5, 139))
