from parser import Parser
from scheduler import Scheduler
from clock import Clock
from threading import Lock


def main():
    # start the parser to get the necessary data
    parser = Parser()

    # create a lock for both the scheduler and the clock
    lock = Lock()

    scheduler = Scheduler(parser.listOfSchedulerProcesses, lock)

    # the scheduler also starts the clock
    scheduler.start()
    scheduler.join()


if __name__ == "__main__":
    main()
