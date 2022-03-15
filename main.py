from parser import Parser
from scheduler import Scheduler
from clock import Clock
from schedulerProcess import SchedulerProcess


def main():
    # create the clock object
    clock = Clock()

    # # start the clock thread
    clock.start()
    # clock.join()

    # start the parser to get the necessary data
    parser = Parser()

    # logger.info(
    #     "The number of processes to schedule is %d", parser.getNumberofProcesses()
    # )

    # for process in parser.listOfUserProcesses:
    #     logger.info(f"process's arrival time is {process.arrivalTime}")
    #     logger.info(f"process's burst time is {process.burstTime}")

    # for process in Scheduler.schedulerTotalProcessesQueue:
    #     logger.info(f"process's PID is {process.PID}")
    #     logger.info(f"process's priority is {process.priority}")

    # Create a lock here and pass this global lock to all threads as argument


if __name__ == "__main__":
    main()
