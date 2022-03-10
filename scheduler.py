from queue import PriorityQueue


class Scheduler:
    schedulerTotalProcessesQueue = []
    schedulerQ1 = PriorityQueue()
    schedulerQ2 = PriorityQueue()
    numberOfProcesses: int = 0

    activeQueue = schedulerQ1
    expiredQueue = schedulerQ2

    def __init__(self) -> None:
        pass

    def switchFlagsOfQueues(self) -> None:
        tmp = self.activeQueue
        self.activeQueue = self.expiredQueue
        self.expiredQueue = tmp

    def insertIntoExpiredQueue(self, schedulerProcess) -> None:
        self.expiredQueue.put(schedulerProcess.priority, schedulerProcess.PID)

    def insertIntoActiveQueue(self, schedulerProcess) -> None:
        self.activeQueue.put(schedulerProcess.priority, schedulerProcess.PID)
