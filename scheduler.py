from threading import Thread
from heapq import heapify, heappush
from time import sleep
from parser import timeDeque
from clock import checkProcessArrivalTime
from schedulerProcess import SchedulerProcess
from parser import listOfUserProcesses, listOfSchedulerProcesses
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
        logger = logging.getLogger(f"{__name__} thread")

        logger.debug(f"Scheduler running")

        while True:
            sleep(0.02)
            # wait for lock from Clock thread
            with self.lock:
                logger.debug(f"Accquired lock from clock thread")

                # check if at this time, any process arrived
                for processNum, process in enumerate(listOfUserProcesses):
                    checkProcessArrivalTime(process)
                    if process.state == SchedulerProcessState.ARRIVED:
                        self.insertIntoExpiredQueue(
                            listOfSchedulerProcesses[processNum]
                        )
                        heapify(self.expiredQueue)
                        process.state = SchedulerProcessState.PAUSED
                        logger.debug(
                            f"{listOfSchedulerProcesses[processNum].PID} arrived at time {timeDeque[-1]} and was put into Expired Queue"
                        )
                        logger.debug(
                            f"The current processes in the active queue are: {self.activeQueue}"
                        )
                        logger.debug(
                            f"The current processes in the expired queue are: {self.expiredQueue}"
                        )
                logger.debug(f"Gave lock back to clock thread")

                # # If the active queue is empty, swap the flags of the two queues
                # if not self.activeQueue:
                #     with self.lock:
                #         logger.debug(f"Current time is {clock.currentTime}")
                #         self.switchFlagsOfQueues()
                #         logger.debug("Switched flags for the queues!")
                #         logger.debug(
                #             f"The current processes in the active queue are: {self.activeQueue}"
                #         )
                #         logger.debug(
                #             f"The current processes in the expired queue are: {self.expiredQueue}"
                #         )
                #         # Get time slice/slot for the first process in the active queue
                #         process: SchedulerProcess = heappop(self.activeQueue)[1]
                #         self.getTimeSliceForProcess(process)
                #         logger.debug(
                #             f"Process {process.PID} got allocated {process.currentTimeSlice} milliseconds"
                #         )

                # # Start the process and other stuffs

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
