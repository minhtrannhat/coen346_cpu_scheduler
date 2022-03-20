from userProcess import UserProcess
from schedulerProcess import SchedulerProcess
from collections import deque

numberOfProcesses = 0
listOfUserProcesses: list[UserProcess] = []
listOfSchedulerProcesses: list[SchedulerProcess] = []

# we want to map UserProcesses to SchedulerProcesses for ease of context switching
schedulerProcessesToUserProcessesMapping: dict[SchedulerProcess, UserProcess] = dict([])

# and reverse
userProcessesToSchedulerProcessesMapping: dict[UserProcess, SchedulerProcess] = dict([])

# to get time from the clock thread, we access this double ended queue
timeDeque = deque()
timeDeque.append(0)

# check if scheduler is done
schedulerDone: bool = False


def parse() -> None:
    with open("input.txt", "r") as file:
        # get the number of processes
        for _ in range(1):
            numberOfProcesses = int(next(file))
        for line in file:

            # get the Arrival Time and Burst Time of each process
            currentUserProcess: UserProcess = UserProcess(
                int(line.split()[1]), int(line.split()[2])
            )
            listOfUserProcesses.append(currentUserProcess)

            # get the PID and priority of the processes
            currentSchedulerProcess: SchedulerProcess = SchedulerProcess(
                line.split()[0], int(line.split()[3])
            )
            listOfSchedulerProcesses.append(currentSchedulerProcess)

            schedulerProcessesToUserProcessesMapping.update(
                {currentSchedulerProcess: currentUserProcess}
            )

            userProcessesToSchedulerProcessesMapping.update(
                {currentUserProcess: currentSchedulerProcess}
            )
