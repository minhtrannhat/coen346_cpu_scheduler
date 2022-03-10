from queue import PriorityQueue
from threading import Thread


class Scheduler(Thread):
    schedulerTotalProcessesQueue = []

    def __init__(self):
        super(Scheduler, self).__init__()
        self.activeQueue = PriorityQueue()
        self.expiredQueue = PriorityQueue()
        self.numberOfProcesses: int = 0

    def run(self) -> None:
        return super().run()

    def switchFlagsOfQueues(self) -> None:
        tmp = self.activeQueue
        self.activeQueue = self.expiredQueue
        self.expiredQueue = tmp

    def insertIntoExpiredQueue(self, schedulerProcess) -> None:
        self.expiredQueue.put(schedulerProcess.priority, schedulerProcess.PID)

    def insertIntoActiveQueue(self, schedulerProcess) -> None:
        self.activeQueue.put(schedulerProcess.priority, schedulerProcess.PID)
