from userProcess import UserProcess
from schedulerProcess import SchedulerProcess


class Parser:
    numberOfProcesses = 0
    listOfUserProcesses = []
    listOfSchedulerProcesses = []

    def __init__(self) -> None:
        with open("input.txt", "r") as file:
            # get the number of processes
            for _ in range(1):
                self.numberOfProcesses = int(next(file))
            for line in file:
                # get the Arrival Time and Burst Time of each process
                self.listOfUserProcesses.append(
                    UserProcess(line.split()[1], line.split()[2])
                )
                # get the PID and priority of the processes
                self.listOfSchedulerProcesses.append(
                    SchedulerProcess(
                        line.split()[0], int(line.split()[3])
                    )
                )

    def getNumberofProcesses(self) -> int:
        return self.numberOfProcesses
