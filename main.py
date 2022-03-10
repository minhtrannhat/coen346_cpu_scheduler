from parser import Parser
from scheduler import Scheduler

# start the parser to get the necessary data
parser = Parser()

print(f"The number of processes to schedule is {parser.getNumberofProcesses()}")

for process in parser.listOfUserProcesses:
    print(f"process's arrival time is {process.arrivalTime}")
    print(f"process's burst time is {process.burstTime}")

for process in Scheduler.schedulerTotalProcessesQueue:
    print(f"process's PID is {process.PID}")
    print(f"process's priority is {process.priority}")
