from process import Process


class Parser:
    numberOfProcesses = 0
    listOfProcesses = []

    def __init__(self) -> None:
        with open("input.txt", "r") as file:
            # get the number of processes
            for _ in range(1):
                self.numberOfProcesses = int(next(file))
            # get the Arrival Time and Burst Time of each process
            for line in file:
                self.listOfProcesses.append(Process(line.split()[1], line.split()[2]))

    def getNumberofProcesses(self) -> int:
        return self.numberOfProcesses
