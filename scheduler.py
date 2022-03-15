from threading import Thread
from heapq import heapify, heappush, heappop
from clock import Clock
from schedulerProcess import SchedulerProcess
from userProcess import UserProcess
import logging


class Scheduler(Thread):
    def __init__(self, schedulerTotalProcessesQueueGlobal, lock) -> None:
        super(Scheduler, self).__init__()
        self.activeQueue = []
        heapify(self.activeQueue)
        self.expiredQueue = []
        heapify(self.expiredQueue)
        self.numberOfProcesses: int = 0
        self.schedulerTotalProcessesQueue: list[
            SchedulerProcess
        ] = schedulerTotalProcessesQueueGlobal
        self.lock = lock

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
        clock = Clock(self.lock)
        clock.start()

        # busy wait till time is 1000ms == second 1
        while clock.currentTime < 1000:
            continue

        while True:
            # wait for lock from Clock thread
            with self.lock:
                # If the active queue is empty, swap the flags of the two queues
                if not self.activeQueue:
                    logger.debug(f"Current time is {clock.currentTime}")
                    self.switchFlagsOfQueues()
                    logger.debug(
                        f"The current processes in the active queue are: {self.activeQueue}"
                    )
                    logger.debug(
                        f"The current processes in the expired queue are: {self.expiredQueue}"
                    )
                    logger.debug("Switching flags for the queues!")
                    break
                else:
                    # check if at this time, any process arrived
                    for process in self.schedulerTotalProcessesQueue:
                        if process.arrivalTime == clock.currentTime:
                            self.insertIntoExpiredQueue(process)

                    # Get time slice/slot for the first process in the active queue
                    self.getTimeSliceForProcess(heappop(self.activeQueue))

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
