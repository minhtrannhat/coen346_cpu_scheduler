from userProcess import UserProcess
from scheduler import Scheduler
from schedulerProcess import SchedulerProcess


class Parser:
    numberOfProcesses = 0
    listOfUserProcesses = []

    def __init__(self) -> None:
        with open("input.txt", "r") as file:
            # get the number of processes
            for _ in range(1):
                self.numberOfProcesses = int(next(file))
            # get the Arrival Time and Burst Time of each process
            for line in file:
                self.listOfUserProcesses.append(
                    UserProcess(line.split()[1], line.split()[2])
                )
                Scheduler.schedulerTotalProcessesQueue.append(
                    SchedulerProcess(line.split()[0], line.split()[3])
                )

    def getNumberofProcesses(self) -> int:
        return self.numberOfProcesses
