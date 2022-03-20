from threading import Thread, Lock
from heapq import heapify, heappush
from time import sleep
from typing import Optional
from parser import timeDeque
from clock import checkProcessArrivalTime
from schedulerProcess import SchedulerProcess
from parser import (
    listOfUserProcesses,
    schedulerProcessesToUserProcessesMapping,
    userProcessesToSchedulerProcessesMapping,
    schedulerDone,
)
import logging

from schedulerProcessStates import SchedulerProcessState
from userProcess import UserProcess


# UserProcess is a class that models a process from itself's POV
# SchedulerProcess is a class that models how the scheduler views a process
class Scheduler(Thread):
    def __init__(self, lock) -> None:
        super(Scheduler, self).__init__()

        # 2 queues for active and inactive processes
        self.activeQueue: list[SchedulerProcess] = []
        self.expiredQueue: list[SchedulerProcess] = []

        # holder for when process is still running
        # but popped out of active queue
        # defaults to None
        self.runningSchedulerProcess: Optional[SchedulerProcess] = None

        self.numOfProcessesTerminated: int = 0

        # lock shared with clock thread
        self.lock = lock

        # python dict of number of times a process been granted time slot,
        # if a process's been given 2 time slots, its priority is updated
        self.processesNumberOfTimeSlices: dict[UserProcess, int] = dict([])

        # python dict of timeslices been given to an user process
        self.processesTimeSliceMapping: dict[UserProcess, int] = dict([])

    def run(self) -> None:
        logger = logging.getLogger(f"{__name__} thread")

        logger.debug("Scheduler running")

        lockForProcess = Lock()

        while True:
            # sync the sleeping time with the clock thread to make sure two threads
            # get the same amount of time to execute their tasks
            sleep(0.02)
            # wait for lock from Clock thread
            with self.lock:
                logger.debug("Accquired lock from clock thread")

                # check if a process should be paused due to running out of time slice/slot
                if self.runningSchedulerProcess is not None:
                    userProcess = schedulerProcessesToUserProcessesMapping[
                        self.runningSchedulerProcess
                    ]
                    if (
                        self.runningSchedulerProcess.currentTimeSlice
                        == userProcess.timeSpentInCPU
                    ):
                        # insert this process that is no longer allowed to run
                        # into the expired Queue
                        self.insertIntoExpiredQueue(self.runningSchedulerProcess)
                        logger.info(
                            f"Time {timeDeque[-1]}, {self.runningSchedulerProcess.PID}, Paused"
                        )
                        self.runningSchedulerProcess = None

                # check if at this time, any process arrived
                for userProcess in listOfUserProcesses:
                    checkProcessArrivalTime(userProcess)
                    if userProcess.state == SchedulerProcessState.ARRIVED:
                        # context switching from user process to scheduler process
                        schedulerProcess: SchedulerProcess = (
                            userProcessesToSchedulerProcessesMapping[userProcess]
                        )

                        self.insertIntoExpiredQueue(schedulerProcess)
                        heapify(self.expiredQueue)

                        userProcess.state = SchedulerProcessState.PAUSED

                        logger.debug(
                            f"The current processes in the active queue are: {self.activeQueue}"
                        )
                        logger.debug(
                            f"The current processes in the expired queue are: {self.expiredQueue}"
                        )
                        logger.debug(
                            f"The current process running is : {self.runningSchedulerProcess}"
                        )
                        logger.info(
                            f"Time {timeDeque[-1]}, {schedulerProcess.PID}, Arrived"
                        )

                        # immediately switch the flags but at second 1 only
                        # This is because in the example, P1 did NOT arrive at second 1
                        # But instead started at second 1
                        if timeDeque[-1] == 1000 and not self.activeQueue:
                            logger.debug(f"Current time is {timeDeque[-1]}")
                            self.switchFlagsOfQueues()
                            logger.debug("Switched flags for the queues!")
                            logger.debug(
                                f"The current processes in the active queue are: {self.activeQueue}"
                            )
                            logger.debug(
                                f"The current processes in the expired queue are: {self.expiredQueue}"
                            )

                    # check if a process is terminated
                    elif userProcess.state == SchedulerProcessState.TERMINATED:
                        # stop the userProcess thread
                        userProcess.join()
                        schedulerProcess = userProcessesToSchedulerProcessesMapping[
                            userProcess
                        ]
                        logger.info(
                            f"Time {timeDeque[-1]}, {schedulerProcess.PID}, Terminated"
                        )
                        self.numOfProcessesTerminated += 1

                # if all processes are terminated, this scheduler can be stopped
                if self.numOfProcessesTerminated == len(listOfUserProcesses):
                    schedulerDone = True
                    break

                # skip if both queues are empty
                elif not self.activeQueue and not self.expiredQueue:
                    continue

                # if the active queue is not empty, execute time slot for the first process
                elif self.activeQueue:
                    # pop the first process in the active queue
                    runningSchedulerProcess: SchedulerProcess = self.activeQueue.pop(0)

                    # find the user process from the scheduler process
                    runningUserProcess: UserProcess = (
                        schedulerProcessesToUserProcessesMapping[
                            runningSchedulerProcess
                        ]
                    )

                    # check if the process has already got allocated 2 time slices/slots
                    # if yes, update its priority
                    if runningUserProcess in self.processesNumberOfTimeSlices:
                        if self.processesNumberOfTimeSlices[runningUserProcess] >= 2:
                            runningSchedulerProcess.updatePriority(
                                timeDeque[-1], runningUserProcess.arrivalTime
                            )
                            logger.info(
                                f"Time {timeDeque[-1]}, {runningSchedulerProcess.PID}, priority updated to {runningSchedulerProcess.priority}"
                            )

                    # Increment the number of time slices or set it to 1 if it doesnt exist
                    self.processesNumberOfTimeSlices[runningUserProcess] = (
                        self.processesNumberOfTimeSlices.setdefault(
                            runningUserProcess, 1
                        )
                        + 1
                    )

                    # get time slice for the process
                    timeSlice: int = self.getTimeSliceForProcess(
                        runningSchedulerProcess
                    )
                    runningSchedulerProcess.currentTimeSlice = timeSlice

                    # store the time slice for this user process into the dictionary
                    self.processesTimeSliceMapping.update(
                        {runningUserProcess: timeSlice}
                    )

                    logger.debug(
                        f"Process {runningSchedulerProcess.PID} got allocated {runningSchedulerProcess.currentTimeSlice} milliseconds"
                    )

                    if self.processesNumberOfTimeSlices[runningUserProcess] > 1:
                        logger.info(
                            f"Time {timeDeque[-1]}, {runningSchedulerProcess.PID}, Resumed"
                        )
                    else:
                        logger.info(
                            f"Time {timeDeque[-1]}, {runningSchedulerProcess.PID}, Started, Granted {timeSlice}"
                        )

                    # update this process waiting time
                    runningSchedulerProcess.updateWaitingTime(
                        arrivalTime=runningUserProcess.arrivalTime,
                        timeSpentInCPU=runningUserProcess.timeSpentInCPU,
                        currentTime=timeDeque[-1],
                    )
                    logger.debug(
                        f"This process {runningSchedulerProcess.PID}'s waiting time is {runningSchedulerProcess.waitingTime}"
                    )

                    # check if it's alive or not
                    # if not, start the thread
                    if not runningUserProcess.is_alive():
                        if runningUserProcess.state != SchedulerProcessState.TERMINATED:
                            logger.debug("Gave lock to an userProcess")
                            runningUserProcess.setLock(lockForProcess)
                            logger.debug("Started an userProcess")
                            runningUserProcess.start()
                    

                    runningUserProcess.state = SchedulerProcessState.RESUMED
                    self.runningSchedulerProcess = runningSchedulerProcess

                    logger.debug(
                        f"The current process running is : {self.runningSchedulerProcess}"
                    )
                    continue

                # If the active queue is empty, swap the flags of the two queues
                elif not self.activeQueue:
                    logger.debug(f"Current time is {timeDeque[-1]}")
                    self.switchFlagsOfQueues()
                    logger.debug("Switched flags for the queues!")
                    logger.debug(
                        f"The current processes in the active queue are: {self.activeQueue}"
                    )
                    logger.debug(
                        f"The current processes in the expired queue are: {self.expiredQueue}"
                    )

                logger.debug("Gave lock back to clock thread")

    # switching flags for the two active and expired queues
    def switchFlagsOfQueues(self) -> None:
        self.activeQueue, self.expiredQueue = self.expiredQueue, self.activeQueue

    # push into the expired queue the tuple. Expired queue is a min heap.
    def insertIntoExpiredQueue(self, schedulerProcess) -> None:
        heappush(self.expiredQueue, schedulerProcess)

    # push into active queue the tuple
    def insertIntoActiveQueue(self, schedulerProcess) -> None:
        self.activeQueue.append(schedulerProcess)

    # get time slice for the process, this is the duration that the CPU will give the process
    def getTimeSliceForProcess(self, schedulerProcess) -> int:
        if schedulerProcess.priority < 100:
            timeSlice = schedulerProcess.currentTimeSlice = (
                140 - schedulerProcess.priority
            ) * 20
        else:
            timeSlice = schedulerProcess.currentTimeSlice = (
                140 - schedulerProcess.priority
            ) * 5
        return timeSlice
