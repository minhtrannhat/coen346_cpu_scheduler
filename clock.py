from threading import Thread
from time import sleep


class Clock(Thread):
    def __init__(self, lock):
        super(Clock, self).__init__()
        self.currentTime: int = 0
        self.lock = lock

    def run(self):
        while True:
            # sleep for 50 milliseconds
            sleep(0.020)

            # increment clock by 5 milliseconds
            with self.lock:
                self.currentTime += 5

    def __str__(self) -> str:
        return str(self.currentTime)
