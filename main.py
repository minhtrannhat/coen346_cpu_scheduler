from parser import Parser
from scheduler import Scheduler
from clock import Clock
import logging


def main():
    # setup logging to output.txt
    logging.basicConfig(
        filename="output.txt",
        filemode="w",
        force=True,
        level=logging.INFO,
        # TODO how to get logging to display clock time and PID
        format="Time {clock.currentTime} - {message}",
        style="{",
    )

    # start the logger
    logger = logging.getLogger()

    # start the clock thread
    clock = Clock()
    clock.start()
    clock.join()

    # start the parser to get the necessary data
    parser = Parser()

    logger.info(
        f"The number of processes to schedule is {parser.getNumberofProcesses()}"
    )

    for process in parser.listOfUserProcesses:
        logger.info(f"process's arrival time is {process.arrivalTime}")
        logger.info(f"process's burst time is {process.burstTime}")

    for process in Scheduler.schedulerTotalProcessesQueue:
        logger.info(f"process's PID is {process.PID}")
        logger.info(f"process's priority is {process.priority}")

    # Create a lock here and pass this global lock to all threads as argument


if __name__ == "__main__":
    main()
