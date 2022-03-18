from threading import Thread
from time import sleep
from userProcess import UserProcess
from schedulerProcessStates import SchedulerProcessState
from parser import listOfUserProcesses
import logging


class Clock(Thread):
    def __init__(self, lock):
        super(Clock, self).__init__()
        self.currentTime: int = 0
        self.lock = lock

    def run(self):
        while True:
            logger = logging.getLogger(f"{__name__} thread")
            # TODO Change this into 100 ms since the TA said this is too strict
            # sleep for 10 milliseconds
            sleep(0.01)
            # increment clock by 5 milliseconds
            with self.lock:
                logger.debug(f"Accquired lock from scheduler thread")
                self.currentTime += 5
                logger.debug(f"Current time is {self.currentTime}")
                logger.debug(f"Gave the lock back to the scheduler thread")

    def __str__(self) -> str:
        return str(self.currentTime)

    def checkProcessArrivalTime(self, listOfUserProcess: list[UserProcess]):
        logger = logging.getLogger(f"{__name__} thread")
        for process in listOfUserProcess:
            if process.arrivalTime == self.currentTime:
                process.state = SchedulerProcessState.ARRIVED
                logger.debug(f"Changed the state of a process to ARRIVED")
