from threading import Thread, Lock
from typing import Optional
from schedulerProcessStates import SchedulerProcessState
from time import sleep
import logging

# A process from the process itself POV.
# According to the requirements, a process should only know its arrival time and burst time
# And only once userProcess should be running at any given time
class UserProcess(Thread):
    def __init__(self, arrivalTime, burstTime):
        super(UserProcess, self).__init__()
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.state = SchedulerProcessState.IDLE
        self.timeSpentInCPU: int = 0
        self.timeLeftToFinish: int = burstTime
        self.lock: Optional[Lock] = None

    def run(self):
        # start the logger
        logger = logging.getLogger(__name__)
        while True:
            sleep(0.02)
            if self.lock is not None:
                with self.lock:
                    logger.debug(f"Acquired lock")
                    if self.timeLeftToFinish == 0:
                        self.state = SchedulerProcessState.TERMINATED
                        logger.debug(f"Process Terminated")
                        break
                    self.timeSpentInCPU += 5
                    logger.debug(f"Process time spent in CPU is {self.timeSpentInCPU}")
                    self.timeLeftToFinish -= 5
                    logger.debug(
                        f"Process time left to finish is {self.timeLeftToFinish}"
                    )
                    logger.debug(f"Released lock")

    def setLock(self, lock) -> None:
        self.lock = lock
