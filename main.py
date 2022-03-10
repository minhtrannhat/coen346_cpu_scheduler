from parser import Parser

# start the parser to get the necessary data
parser = Parser()

print(f"The number of processes to schedule is {parser.getNumberofProcesses()}")

for process in parser.listOfProcesses:
    print(f"process's arrival time is {process.arrivalTime}")
    print(f"process's burst time is {process.burstTime}")
