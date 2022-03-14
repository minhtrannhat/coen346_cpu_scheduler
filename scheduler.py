from queue import PriorityQueue
from threading import Thread


class Scheduler(Thread):
    schedulerTotalProcessesQueue = []

    def __init__(self) -> None:
        super(Scheduler, self).__init__()
        self.activeQueue = PriorityQueue()
        self.expiredQueue = PriorityQueue()
        self.numberOfProcesses: int = 0
        self.schedulerTotalProcessesQueue = []
        self.noMoreInput = False

    # def run(self) -> None:
    #     while True:
    #         # stop the scheduler thread
    #         if self.noMoreInput:
    #             break
    #         # put all incoming processes into the expired queue
    #         if self.schedulerTotalProcessesQueue

    def switchFlagsOfQueues(self) -> None:
        tmp = self.activeQueue
        self.activeQueue = self.expiredQueue
        self.expiredQueue = tmp

    def insertIntoExpiredQueue(self, schedulerProcess) -> None:
        self.expiredQueue.put(schedulerProcess.priority, schedulerProcess.PID)

    def insertIntoActiveQueue(self, schedulerProcess) -> None:
        self.activeQueue.put(schedulerProcess.priority, schedulerProcess.PID)

    def getTimeSliceForProcess(self, schedulerProcess) -> None:
        if schedulerProcess.priority < 100:
            schedulerProcess.currentTimeSlice = (140 - schedulerProcess.priority) * 20
        else:
            schedulerProcess.currentTimeSlice = (140 - schedulerProcess.priority) * 5
