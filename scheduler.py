from threading import Thread
from heapq import heapify, heappush
from clock import Clock
import logging


class Scheduler(Thread):
    schedulerTotalProcessesQueue = []

    def __init__(self) -> None:
        super(Scheduler, self).__init__()
        self.activeQueue = []
        heapify(self.activeQueue)
        self.expiredQueue = []
        heapify(self.expiredQueue)
        self.numberOfProcesses: int = 0
        self.schedulerTotalProcessesQueue = []
        self.noMoreInput = False

    def run(self) -> None:
        # setup logging to output.txt
        logging.basicConfig(
            filename="output.txt",
            filemode="w",
            force=True,
            level=logging.DEBUG,
            format="{message}",
            style="{",
        )

        # start the logger
        logger = logging.getLogger(__name__)

        # start the clock thread
        clock = Clock()
        clock.start()

        while True:
            # If the active queue is empty, swap the flags of the two queues
            if not self.activeQueue:
                self.switchFlagsOfQueues()
            else:
                # check if at this time, any process arrived
                self.schedulerTotalProcessesQueue

    def switchFlagsOfQueues(self) -> None:
        tmp = self.activeQueue
        self.activeQueue = self.expiredQueue
        self.expiredQueue = tmp

    # push into the expired queue the tuple. Expired queue is a min heap.
    def insertIntoExpiredQueue(self, schedulerProcess) -> None:
        heappush(self.expiredQueue, (schedulerProcess.priority, schedulerProcess))

    def insertIntoActiveQueue(self, schedulerProcess) -> None:
        heappush(self.activeQueue, (schedulerProcess.priority, schedulerProcess))

    def getTimeSliceForProcess(self, schedulerProcess) -> None:
        if schedulerProcess.priority < 100:
            schedulerProcess.currentTimeSlice = (140 - schedulerProcess.priority) * 20
        else:
            schedulerProcess.currentTimeSlice = (140 - schedulerProcess.priority) * 5
