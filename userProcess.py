from threading import Thread
from schedulerProcessStates import SchedulerProcessState

# A process from the process itself POV.
# According to the requirements, a process should only know its arrival time and burst time
class UserProcess(Thread):
    def __init__(self, arrivalTime, burstTime):
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self._state = SchedulerProcessState.IDLE
        self.timeSpentInCPU: int = 0
        self.timeLeftToFinish: int = burstTime

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state: SchedulerProcessState):
        self._state = new_state

    def getTimeSpentInCPU(self) -> int:
        return self.timeSpentInCPU

    def getTimeLeftToFinish(self) -> int:
        return self.timeLeftToFinish
