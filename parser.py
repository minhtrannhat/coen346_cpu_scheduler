from userProcess import UserProcess
from schedulerProcess import SchedulerProcess


numberOfProcesses = 0
listOfUserProcesses = []
listOfSchedulerProcesses = []


def parse() -> None:
    with open("input.txt", "r") as file:
        # get the number of processes
        for _ in range(1):
            numberOfProcesses = int(next(file))
        for line in file:
            # get the Arrival Time and Burst Time of each process
            listOfUserProcesses.append(
                UserProcess(int(line.split()[1]), int(line.split()[2]))
            )
            # get the PID and priority of the processes
            listOfSchedulerProcesses.append(
                SchedulerProcess(line.split()[0], int(line.split()[3]))
            )
