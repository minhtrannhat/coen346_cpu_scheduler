from parser import Parser
from scheduler import Scheduler
from clock import Clock
from threading import Lock


def main():
    # create a lock for both the scheduler and the clock
    lock = Lock()

    scheduler = Scheduler(lock)

    # the scheduler also starts the clock
    scheduler.start()
    scheduler.join()


if __name__ == "__main__":
    main()
