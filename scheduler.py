from threading import Thread
from heapq import heapify, heappush, heappop
from clock import Clock
from schedulerProcess import SchedulerProcess
from parser import Parser
import logging

from schedulerProcessStates import SchedulerProcessState


class Scheduler(Thread):
    def __init__(self, lock) -> None:
        super(Scheduler, self).__init__()
        self.activeQueue = []
        self.expiredQueue = []
        heapify(self.expiredQueue)
        self.numberOfProcesses: int = 0
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

        # Start the parser
        parser = Parser()

        # busy wait till time is 1000ms == second 1
        while clock.currentTime < 1000:
            continue

        while True:
            # wait for lock from Clock thread
            with self.lock:
                logger.debug("Acquired lock from Clock thread")

                # check if at this time, any process arrived
                for process in parser.listOfUserProcesses:
                    if process.state == SchedulerProcessState.ARRIVED:
                        self.insertIntoExpiredQueue(process)
                        heapify(self.expiredQueue)
                        logger.debug(
                            f"{process.PID} arrived at time {clock.currentTime} and was put into Expired Queue"
                        )
                        logger.debug(
                            f"The current processes in the active queue are: {self.activeQueue}"
                        )
                        logger.debug(
                            f"The current processes in the expired queue are: {self.expiredQueue}"
                        )

                # If the active queue is empty, swap the flags of the two queues
                while not self.activeQueue:
                    logger.debug(f"Current time is {clock.currentTime}")
                    self.switchFlagsOfQueues()
                    logger.debug("Switched flags for the queues!")
                    logger.debug(
                        f"The current processes in the active queue are: {self.activeQueue}"
                    )
                    logger.debug(
                        f"The current processes in the expired queue are: {self.expiredQueue}"
                    )

                while self.activeQueue:
                    # Get time slice/slot for the first process in the active queue
                    process: SchedulerProcess = heappop(self.activeQueue)[1]
                    self.getTimeSliceForProcess(process)
                    logger.debug(
                        f"Process {process.PID} got allocated {process.currentTimeSlice} milliseconds"
                    )

            break

            # Start the process and other stuffs

    def switchFlagsOfQueues(self) -> None:
        self.activeQueue, self.expiredQueue = self.expiredQueue, self.activeQueue

    # push into the expired queue the tuple. Expired queue is a min heap.
    def insertIntoExpiredQueue(self, schedulerProcess) -> None:
        heappush(self.expiredQueue, schedulerProcess)

    # push into active queue the tuple
    def insertIntoActiveQueue(self, schedulerProcess) -> None:
        self.activeQueue.append(schedulerProcess)

    # get time slice for the process, this is the duration that the CPU will give the process
    def getTimeSliceForProcess(self, schedulerProcess) -> None:
        if schedulerProcess.priority < 100:
            schedulerProcess.currentTimeSlice = (140 - schedulerProcess.priority) * 20
        else:
            schedulerProcess.currentTimeSlice = (140 - schedulerProcess.priority) * 5
