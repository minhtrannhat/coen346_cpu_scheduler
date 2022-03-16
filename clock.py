from threading import Thread
from time import sleep
from userProcess import UserProcess
from schedulerProcessStates import SchedulerProcessState
from parser import Parser


class Clock(Thread):
    def __init__(self, lock):
        super(Clock, self).__init__()
        self.currentTime: int = 0
        self.lock = lock

    def run(self):
        while True:
            # TODO Change this into 100 ms since the TA said this is too strict
            # sleep for 10 milliseconds
            sleep(0.01)
            # increment clock by 5 milliseconds
            with self.lock:
                self.currentTime += 5

    def __str__(self) -> str:
        return str(self.currentTime)

    def checkProccessArrivalTime(self, listOfUserProcesses: list[UserProcess]):
        # start the logger
        for process in listOfUserProcesses:
            if process.arrivalTime == self.currentTime:
                process.state = SchedulerProcessState.ARRIVED
