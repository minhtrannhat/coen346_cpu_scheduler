from threading import Thread
from time import sleep
from userProcess import UserProcess
from schedulerProcessStates import SchedulerProcessState
from parser import timeDeque, schedulerDone
import logging


class Clock(Thread):
    def __init__(self, lock):
        super(Clock, self).__init__()
        self.currentTime: int = 0
        self.lock = lock

    def run(self):
        while True:
            logger = logging.getLogger(f"{__name__} thread")
            # sleep for 10 milliseconds
            sleep(0.005)
            with self.lock:
                # stop the clock thread if the scheduler is done executing
                if schedulerDone:
                    break
                logger.debug(f"Accquired lock from scheduler thread")
                # increment clock by 5 milliseconds
                self.currentTime += 5
                print(self.currentTime)
                timeDeque.append(self.currentTime)
                logger.debug(f"Current time is {self.currentTime}")
                logger.debug(f"Gave the lock back to the scheduler thread")

    def __str__(self) -> str:
        return str(self.currentTime)


def checkProcessArrivalTime(process: UserProcess):
    logger = logging.getLogger(f"{__name__} thread")
    if process.arrivalTime == timeDeque[-1]:
        process.state = SchedulerProcessState.ARRIVED
        logger.debug(f"Changed the state of a process to ARRIVED")
