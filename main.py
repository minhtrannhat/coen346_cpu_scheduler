from scheduler import Scheduler
from clock import Clock
from parser import parse
from threading import Lock
import logging


def main():
    # setup logging to output.txt
    logging.basicConfig(
        filename="output.txt",
        filemode="w",
        force=True,
        level=logging.DEBUG,
        format="{name} - {levelname} - {message}",
        style="{",
    )

    # start the logger
    logger = logging.getLogger(__name__)

    # create a condition for both the scheduler and the clock
    logger.debug("Created a lock for both the scheduler and the clock")
    lock = Lock()

    # parse the input.txt for processes
    parse()

    # start the threads and let them share the mutex
    scheduler = Scheduler(lock)

    scheduler.start()

    scheduler.join()


if __name__ == "__main__":
    main()
